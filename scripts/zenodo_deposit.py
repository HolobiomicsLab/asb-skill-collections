#!/usr/bin/env python3
"""Prepare a Zenodo deposit for one collection release, up to a reviewed draft.

Three subcommands, in the order a maintainer runs them:

  archive  build the release zip of collections/<domain>/<vN>/ and print its
           sha256 and size. The zip is deterministic: sorted entries, fixed
           timestamps and modes, no bytecode caches, no dotfiles except
           .zenodo.json.
  plan     print what a deposit would send (target host, metadata, files) and
           any metadata key the deposit API would reject. No network.
  draft    create a NEW VERSION draft of an existing Zenodo record, replace its
           inherited files with the archive, and set the metadata.

This tool never publishes. Publishing mints the DOI and cannot be undone, so it
stays a manual step in the Zenodo web interface after the draft is checked.

The token is read from the environment only (ZENODO_TOKEN, or
ZENODO_SANDBOX_TOKEN with --sandbox) and is never printed. Every request goes
through `_request`, the single network seam.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

ZENODO_URL = "https://zenodo.org"
SANDBOX_URL = "https://sandbox.zenodo.org"
TOKEN_ENV = "ZENODO_TOKEN"
SANDBOX_TOKEN_ENV = "ZENODO_SANDBOX_TOKEN"
METADATA_FILE = ".zenodo.json"
DEFAULT_OUT_DIR = Path("dist") / "zenodo"
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)
ERROR_BODY_LIMIT = 300
REQUEST_TIMEOUT_SECONDS = 600

# Files bundled beside the collection so the deposit runs grounding on its own.
# They match the bundle the release workflow builds.
BUNDLED_FILES = (
    ("scripts/perspicacite_kb_bind.py", "scripts/perspicacite_kb_bind.py"),
    ("scripts/requirements.txt", "scripts/requirements.txt"),
    ("AGENTS.md", "AGENTS.md"),
)
# License texts the archive must carry, at their repository paths: LICENSING.md
# says which license covers which layer, LICENSE is the Apache-2.0 text it points
# to, and LICENSE_TIERS.md defines the per-skill license tiers. A missing one
# stops the build. The release workflow bundles the same files.
LICENSE_FILES = (
    "LICENSING.md",
    "LICENSE",
    "governance/LICENSE_TIERS.md",
)

# Deposition metadata keys of the Zenodo REST API, copied from
# https://developers.zenodo.org (section "Deposit metadata").
API_METADATA_KEYS = frozenset({
    "upload_type", "publication_type", "image_type", "publication_date", "title",
    "creators", "description", "access_right", "license", "embargo_date",
    "access_conditions", "doi", "prereserve_doi", "keywords", "notes",
    "related_identifiers", "contributors", "references", "communities", "grants",
    "journal_title", "journal_volume", "journal_issue", "journal_pages",
    "conference_title", "conference_acronym", "conference_dates", "conference_place",
    "conference_url", "conference_session", "conference_session_part",
    "imprint_publisher", "imprint_isbn", "imprint_place", "partof_title",
    "partof_pages", "thesis_supervisors", "thesis_university", "subjects",
    "version", "language", "locations", "dates", "method",
})
REQUIRED_KEYS = ("upload_type", "title", "creators", "description", "access_right")
UPLOAD_TYPES = frozenset({
    "publication", "poster", "presentation", "dataset", "image", "video",
    "software", "lesson", "physicalobject", "other",
})
ACCESS_RIGHTS = frozenset({"open", "embargoed", "restricted", "closed"})
LICENSE_REQUIRED_FOR = frozenset({"open", "embargoed"})
API_RELATIONS = frozenset({
    "isCitedBy", "cites", "isSupplementTo", "isSupplementedBy", "isContinuedBy",
    "continues", "isDescribedBy", "describes", "hasMetadata", "isMetadataFor",
    "isNewVersionOf", "isPreviousVersionOf", "isPartOf", "hasPart", "isReferencedBy",
    "references", "isDocumentedBy", "documents", "isCompiledBy", "compiles",
    "isVariantFormOf", "isOriginalFormof", "isIdenticalTo", "isAlternateIdentifier",
    "isReviewedBy", "reviews", "isDerivedFrom", "isSourceOf", "requires",
    "isRequiredBy", "isObsoletedBy", "obsoletes",
})
# Lineage relations the template may carry. They name the record to version from
# and are not sent: the API does not accept isVersionOf, and Zenodo links the
# versions of a record itself.
LINEAGE_RELATIONS = frozenset({"isVersionOf", "hasVersion"})
# Relations whose target is the published record to version from. isPreviousVersionOf
# and hasVersion name a later or child record, so they are not read.
SOURCE_RECORD_RELATIONS = frozenset({"isVersionOf", "isNewVersionOf"})
# Metadata the API sets itself; never sent back from a draft.
READ_ONLY_KEYS = frozenset({"doi", "prereserve_doi"})
RECORD_ID_PATTERN = re.compile(r"zenodo[./](\d+)")


class ZenodoError(RuntimeError):
    """A deposit step cannot proceed; the message says why and never holds the token."""


@dataclass(frozen=True)
class Archive:
    """A built release zip: where it is, its sha256, size and entry count."""

    path: Path
    sha256: str
    size: int
    entries: int


def _request(method, url, token, body=None):
    """Send one HTTP request and return (status, parsed JSON or None).

    `body` is a dict (sent as JSON), a Path (streamed as the raw file), or None.
    HTTP error statuses are returned, not raised; callers decide what is fatal.
    """
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    data = None
    if isinstance(body, Path):
        headers["Content-Type"] = "application/octet-stream"
        headers["Content-Length"] = str(body.stat().st_size)
        data = body.open("rb")
    elif body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            status, raw = response.status, response.read()
    except urllib.error.HTTPError as error:
        status, raw = error.code, error.read()
    except urllib.error.URLError as error:
        raise ZenodoError(f"{method} {url} failed: {error.reason}") from None
    finally:
        if hasattr(data, "close"):
            data.close()
    return status, _parse_json(raw)


def _parse_json(raw):
    """Return the decoded JSON body, or None when it is empty or not JSON."""
    try:
        return json.loads(raw) if raw else None
    except ValueError:
        return None


def _call(step, method, url, token, body=None):
    """Run one request through `_request` and fail with the step name on non-2xx."""
    status, payload = _request(method, url, token, body)
    if not 200 <= status < 300:
        detail = json.dumps(payload)[:ERROR_BODY_LIMIT] if payload else "no body"
        raise ZenodoError(f"{step}: {method} answered HTTP {status} ({detail})")
    return payload


def _token(sandbox):
    """Return the API token for the target host, read from the environment only."""
    name = SANDBOX_TOKEN_ENV if sandbox else TOKEN_ENV
    value = os.environ.get(name, "").strip()
    if not value:
        raise ZenodoError(f"{name} is not set in the environment")
    return value


def _is_shipped(relative: Path) -> bool:
    """True for a file the archive carries: no bytecode cache, no dotfile but .zenodo.json."""
    for part in relative.parts:
        if part == "__pycache__":
            return False
        if part.startswith(".") and part != METADATA_FILE:
            return False
    return True


def _collection_dir(repo_root: Path, domain: str, version: str) -> Path:
    path = repo_root / "collections" / domain / version
    if not path.is_dir():
        raise ZenodoError(f"collection directory not found: {path}")
    return path


def _archive_members(repo_root: Path, domain: str, version: str):
    """Return (archive name, source path) pairs, sorted by archive name."""
    collection = _collection_dir(repo_root, domain, version)
    prefix = f"{domain}/{version}"
    members = {}
    for path in collection.rglob("*"):
        relative = path.relative_to(collection)
        if path.is_file() and _is_shipped(relative):
            members[f"{prefix}/{relative.as_posix()}"] = path
    for source, target in BUNDLED_FILES:
        if (repo_root / source).is_file():
            members[f"{prefix}/{target}"] = repo_root / source
    for relative in LICENSE_FILES:
        if not (repo_root / relative).is_file():
            raise ZenodoError(f"license text not found: {relative}")
        members[f"{prefix}/{relative}"] = repo_root / relative
    return sorted(members.items())


def _zip_info(name: str, source: Path) -> zipfile.ZipInfo:
    """Return a zip header with a fixed timestamp and a mode taken from the exec bit only."""
    info = zipfile.ZipInfo(name, date_time=ZIP_EPOCH)
    executable = source.stat().st_mode & stat.S_IXUSR
    info.external_attr = (0o755 if executable else 0o644) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def build_archive(repo_root: Path, domain: str, version: str, out_dir: Path) -> Archive:
    """Write <out_dir>/<domain>-<version>.zip and return its digest.

    Entries are sorted, timestamps and modes are fixed, so the same tree gives the
    same bytes under one zlib build. The zip differs across zlib builds because
    DEFLATE output is not specified bit for bit; compare sha256 values from one
    machine.
    """
    members = _archive_members(Path(repo_root), domain, version)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{domain}-{version}.zip"
    with zipfile.ZipFile(target, "w") as archive:
        for name, source in members:
            archive.writestr(_zip_info(name, source), source.read_bytes(), compresslevel=9)
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    return Archive(target, digest, target.stat().st_size, len(members))


def validate_metadata(metadata: dict) -> list[str]:
    """List every reason the deposit API would reject this metadata (empty when none)."""
    problems = [f"unknown metadata key: {key}" for key in sorted(set(metadata) - API_METADATA_KEYS)]
    problems += [f"missing required key: {key}" for key in REQUIRED_KEYS if not metadata.get(key)]
    problems += _vocabulary_problems(metadata)
    for creator in metadata.get("creators") or []:
        if not creator.get("name"):
            problems.append("creators entry without a name")
    for related in metadata.get("related_identifiers") or []:
        relation = related.get("relation")
        if relation not in API_RELATIONS:
            problems.append(f"related_identifiers relation not accepted: {relation}")
    return problems


def _vocabulary_problems(metadata: dict) -> list[str]:
    """Check the controlled-vocabulary fields and the license rule."""
    problems = []
    upload_type = metadata.get("upload_type")
    if upload_type and upload_type not in UPLOAD_TYPES:
        problems.append(f"upload_type not accepted: {upload_type}")
    access = metadata.get("access_right")
    if access and access not in ACCESS_RIGHTS:
        problems.append(f"access_right not accepted: {access}")
    if access in LICENSE_REQUIRED_FOR and not metadata.get("license"):
        problems.append(f"missing required key: license (required when access_right is {access})")
    return problems


def metadata_payload(path: Path, publication_date: str):
    """Read a flat .zenodo.json and return ({"metadata": ...}, dropped lineage relations).

    The file lists the metadata at its top level; the API wants it under
    "metadata". Lineage relations are removed from the payload, and the date is
    set when the file has none, because the draft would otherwise inherit the
    previous version's date.
    """
    try:
        metadata = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ZenodoError(f"{METADATA_FILE} not found: {path}") from None
    related = metadata.get("related_identifiers") or []
    dropped = [r["relation"] for r in related if r.get("relation") in LINEAGE_RELATIONS]
    metadata["related_identifiers"] = [r for r in related if r.get("relation") not in LINEAGE_RELATIONS]
    metadata.setdefault("publication_date", publication_date)
    return {"metadata": metadata}, dropped


def inherit_metadata(draft_metadata, payload):
    """Return (payload, kept): the template laid over the metadata the draft inherited.

    A new-version draft starts from the previous record's metadata, including keys
    set in the web interface such as communities and language. Sending the template
    alone would drop them, so they are kept and the template wins on every key it
    has. Only keys the deposit API documents are carried; read-only ones are not.
    `kept` lists the inherited keys the template does not carry.
    """
    sendable = API_METADATA_KEYS - READ_ONLY_KEYS
    inherited = {key: value for key, value in (draft_metadata or {}).items() if key in sendable}
    kept = sorted(set(inherited) - set(payload["metadata"]))
    return {"metadata": {**inherited, **payload["metadata"]}}, kept


def record_id_from(path: Path) -> str:
    """Return the Zenodo record id named by a lineage relation in the template, or ''."""
    metadata = json.loads(Path(path).read_text(encoding="utf-8"))
    for related in metadata.get("related_identifiers") or []:
        if related.get("relation") in SOURCE_RECORD_RELATIONS:
            match = RECORD_ID_PATTERN.search(str(related.get("identifier", "")))
            if match:
                return match.group(1)
    return ""


def _resolve_record_id(args, template: Path) -> str:
    record = args.record_id or record_id_from(template)
    if not record:
        raise ZenodoError("no record to version from: pass --record-id or add an "
                          "isVersionOf zenodo DOI to the template")
    return record


def _host(sandbox):
    return SANDBOX_URL if sandbox else ZENODO_URL


def _prepare(args, out_dir: Path):
    """Return (host, record id, payload, dropped relations, problems, archive)."""
    repo_root = Path(args.repo_root).resolve()
    template = _collection_dir(repo_root, args.domain, args.version) / METADATA_FILE
    payload, dropped = metadata_payload(template, args.publication_date)
    problems = validate_metadata(payload["metadata"])
    record = _resolve_record_id(args, template)
    archive = build_archive(repo_root, args.domain, args.version, out_dir)
    return _host(args.sandbox), record, payload, dropped, problems, archive


def _describe(host, record, payload, dropped, problems, archive) -> str:
    lines = [
        f"target: {host}",
        f"action: new version of record {record}",
        "metadata:",
        json.dumps(payload, indent=2, ensure_ascii=False),
        "files:",
        f"  {archive.path.name}  {archive.size} bytes  {archive.entries} entries  sha256 {archive.sha256}",
    ]
    lines += [f"relation {name} read from the template and not sent" for name in dropped]
    lines += [f"rejected by the API: {problem}" for problem in problems]
    return "\n".join(lines)


def run_plan(args) -> int:
    """Print the deposit plan without any request; exit 1 when the metadata is rejected."""
    with tempfile.TemporaryDirectory() as scratch:
        prepared = _prepare(args, Path(scratch))
        print(_describe(*prepared))
    return 1 if prepared[4] else 0


def run_archive(args) -> int:
    """Build the archive and print its path, sha256 and size."""
    archive = build_archive(Path(args.repo_root).resolve(), args.domain, args.version,
                            Path(args.out_dir))
    print(f"{archive.path}\nsha256 {archive.sha256}\nsize {archive.size} bytes\n"
          f"entries {archive.entries}")
    return 0


def run_draft(args) -> int:
    """Create the new-version draft and print its URL. Never publishes."""
    token = _token(args.sandbox)
    host, record, template, _, problems, archive = _prepare(args, Path(args.out_dir))
    if problems:
        raise ZenodoError("metadata rejected by the API: " + "; ".join(problems))
    base = f"{host}/api/deposit/depositions"
    created = _call("newversion", "POST", f"{base}/{record}/actions/newversion", token)
    draft = _call("draft fetch", "GET", created["links"]["latest_draft"], token)
    for stale in draft.get("files") or []:
        _call("inherited file delete", "DELETE", f"{base}/{draft['id']}/files/{stale['id']}", token)
    _call("archive upload", "PUT", f"{draft['links']['bucket']}/{archive.path.name}", token, archive.path)
    payload, kept = inherit_metadata(draft.get("metadata"), template)
    _call("metadata update", "PUT", f"{base}/{draft['id']}", token, payload)
    if kept:
        print("inherited metadata not in the template, kept: " + ", ".join(kept))
    url = draft["links"].get("html") or f"{host}/deposit/{draft['id']}"
    print(f"draft {draft['id']} created, not published: {url}\n"
          f"uploaded {archive.path.name} sha256 {archive.sha256}")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    for name, handler, help_text in (
        ("archive", run_archive, "build the release zip"),
        ("plan", run_plan, "print the metadata and files a deposit would send"),
        ("draft", run_draft, "create a new-version draft on Zenodo (never publishes)"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.set_defaults(handler=handler)
        command.add_argument("domain", help="collection domain, e.g. metabolomics")
        command.add_argument("version", help="collection version directory, e.g. v2")
        command.add_argument("--repo-root", default=".")
        command.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
        if name != "archive":
            command.add_argument("--sandbox", action="store_true",
                                 help="use sandbox.zenodo.org and ZENODO_SANDBOX_TOKEN")
            command.add_argument("--record-id", default="",
                                 help="latest published record to version from")
            command.add_argument("--publication-date", default=datetime.date.today().isoformat())
    return parser


def main(argv=None) -> int:
    """Run one subcommand; print errors to stderr and return the exit code."""
    args = _parser().parse_args(argv)
    try:
        return args.handler(args)
    except ZenodoError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
