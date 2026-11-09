#!/usr/bin/env python3
"""Prepare a Zenodo deposit for one collection release, up to a reviewed draft.

Four subcommands, in the order a maintainer runs them:

  archive  build the release zip of collections/<domain>/<vN>/ and print its
           sha256 and size. The zip is deterministic: sorted entries, fixed
           timestamps and modes, no bytecode caches, no dotfiles except
           .zenodo.json.
  plan     print what a deposit would send (target host, metadata, files),
           any metadata key the deposit API would reject, and a refusal when
           the template's creators differ from scripts/release_creators.yaml.
           No network.
  draft    create a NEW VERSION draft of an existing Zenodo record, replace its
           inherited files with the archive, and set the metadata.
  create   create a first-release draft as a new record, without inherited
           metadata or a previous record to version from.

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
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

import yaml

ZENODO_URL = "https://zenodo.org"
SANDBOX_URL = "https://sandbox.zenodo.org"
TOKEN_ENV = "ZENODO_TOKEN"
SANDBOX_TOKEN_ENV = "ZENODO_SANDBOX_TOKEN"
METADATA_FILE = ".zenodo.json"
# The release creators list (owner decision 2026-09-19); the collector writes
# CITATION.cff authors from it, and the template's creators must equal it.
CREATORS_FILE = "scripts/release_creators.yaml"
DEFAULT_OUT_DIR = Path("dist") / "zenodo"
ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)
ERROR_BODY_LIMIT = 300
REQUEST_TIMEOUT_SECONDS = 600
DEFAULT_TOOLING_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMMUNITY = "asb_skill_collections"

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
ORCID_PATTERN = re.compile(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]")


class ZenodoError(RuntimeError):
    """A deposit step cannot proceed; the message says why and never holds the token."""


@dataclass(frozen=True)
class Archive:
    """A built release zip: where it is, its sha256, size and entry count."""

    path: Path
    sha256: str
    size: int
    entries: int


@dataclass(frozen=True)
class ExtraFile:
    """An additional bucket upload: its source path, digest and size."""

    path: Path
    sha256: str
    size: int


def _request(method, url, token, body=None):
    """Send one HTTP request and return (status, parsed JSON or None).

    `body` is a dict (sent as JSON), a Path (streamed as the raw file), or None.
    HTTP error statuses are returned, not raised; callers decide what is fatal.
    """
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
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


def _tooling_root(path=None) -> Path:
    return Path(path).resolve() if path is not None else None


def _source_path(repo_root: Path, tooling_root: Path, relative: str):
    roots = [("repository root", repo_root)]
    if tooling_root is not None:
        roots.append(("tooling root", tooling_root))
    for root_name, root in roots:
        candidate = root / relative
        if candidate.is_file():
            return candidate, root_name
    return None, None


def _required_source(repo_root: Path, tooling_root: Path, relative: str, kind: str) -> Path:
    path, _ = _source_path(repo_root, tooling_root, relative)
    if path is None:
        roots = f"{repo_root} or {tooling_root}" if tooling_root is not None else str(repo_root)
        raise ZenodoError(f"{kind} not found: {relative} under {roots}")
    return path


def _archive_members(repo_root: Path, domain: str, version: str, tooling_root=None):
    """Return (archive name, source path) pairs, sorted by archive name."""
    tooling_root = _tooling_root(tooling_root)
    collection = _collection_dir(repo_root, domain, version)
    prefix = f"{domain}/{version}"
    members = {}
    for path in collection.rglob("*"):
        relative = path.relative_to(collection)
        if path.is_file() and _is_shipped(relative):
            members[f"{prefix}/{relative.as_posix()}"] = path
    for source, target in BUNDLED_FILES:
        path, _ = _source_path(repo_root, tooling_root, source)
        if path is not None:
            members[f"{prefix}/{target}"] = path
    for relative in LICENSE_FILES:
        path = _required_source(repo_root, tooling_root, relative, "license text")
        members[f"{prefix}/{relative}"] = path
    return sorted(members.items())


def _zip_info(name: str, source: Path) -> zipfile.ZipInfo:
    """Return a zip header with a fixed timestamp and a mode taken from the exec bit only."""
    info = zipfile.ZipInfo(name, date_time=ZIP_EPOCH)
    executable = source.stat().st_mode & stat.S_IXUSR
    info.external_attr = (0o755 if executable else 0o644) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    return info


def build_archive(repo_root: Path, domain: str, version: str, out_dir: Path,
                  tooling_root=None) -> Archive:
    """Write <out_dir>/<domain>-<version>.zip and return its digest.

    Entries are sorted, timestamps and modes are fixed, so the same tree gives the
    same bytes under one zlib build. The zip differs across zlib builds because
    DEFLATE output is not specified bit for bit; compare sha256 values from one
    machine.
    """
    members = _archive_members(Path(repo_root), domain, version, tooling_root)
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


def _zenodo_creator(entry) -> dict:
    """Convert one release_creators.yaml entry to the deposit API's creator form."""
    if not isinstance(entry, dict):
        raise ZenodoError(f"{CREATORS_FILE}: a creator entry is not a mapping: {entry!r}")
    if entry.get("name"):
        return {"name": entry["name"]}
    if not (entry.get("family") and entry.get("given")):
        raise ZenodoError(f"{CREATORS_FILE}: a person entry needs family and given: {entry!r}")
    creator = {"name": f"{entry['family']}, {entry['given']}"}
    if entry.get("orcid"):
        creator["orcid"] = str(entry["orcid"]).rstrip("/").rsplit("/", 1)[-1]
    if entry.get("affiliation"):
        creator["affiliation"] = entry["affiliation"]
    return creator


def expected_creators(repo_root: Path, tooling_root=None) -> list[dict]:
    """Return the creators of scripts/release_creators.yaml as deposit API creators, in order.

    A person becomes `Family, Given` with a bare ORCID iD and the affiliation
    when given; an entity keeps its name.
    """
    repo_root = Path(repo_root)
    tooling_root = _tooling_root(tooling_root)
    path, _ = _source_path(repo_root, tooling_root, CREATORS_FILE)
    if path is None:
        roots = f"{repo_root} or {tooling_root}" if tooling_root is not None else str(repo_root)
        raise ZenodoError(f"{CREATORS_FILE} not found under {roots}")
    try:
        listed = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ZenodoError(f"{CREATORS_FILE} not found under {roots}") from None
    if not isinstance(listed, dict) or not isinstance(listed.get("creators"), list):
        raise ZenodoError(f"{CREATORS_FILE} must define a creators list")
    return [_zenodo_creator(entry) for entry in listed["creators"]]


def _is_added_coauthor(creator) -> bool:
    """True for a person entry of the form scripts/select_release_coauthors.py appends."""
    return (isinstance(creator, dict)
            and set(creator) <= {"name", "orcid", "affiliation"}
            and bool(str(creator.get("name") or "").strip())
            and bool(ORCID_PATTERN.fullmatch(str(creator.get("orcid") or ""))))


def creator_problems(metadata: dict, expected: list[dict]) -> list[str]:
    """Return a refusal when the template's creators do not start with the release list.

    The release list must come first, unchanged and in order. Further entries
    are accepted only as persons with a bare ORCID iD, the co-authors that
    scripts/select_release_coauthors.py --apply appends, each ORCID iD once.
    """
    found = metadata.get("creators") or []
    head, rest = found[:len(expected)], found[len(expected):]
    orcids = [c.get("orcid") for c in found if isinstance(c, dict) and c.get("orcid")]
    if (head == expected and all(_is_added_coauthor(c) for c in rest)
            and len(orcids) == len(set(orcids))):
        return []
    return [f"creators differ from {CREATORS_FILE}: the template has "
            f"{json.dumps(found, ensure_ascii=False)}, the release list gives "
            f"{json.dumps(expected, ensure_ascii=False)}; only persons with an "
            "ORCID iD may follow the release list"]


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


def _dated_entries(dates):
    """Return (entries with a start or an end, number dropped) from an inherited dates list.

    A record edited in the web interface can carry a dates entry with a type and a
    description but no date at all; the deposit API rejects it with 400 "Invalid date
    provided" when it is sent back, so such entries are not carried.
    """
    entries = [d for d in (dates or []) if isinstance(d, dict) and (d.get("start") or d.get("end"))]
    return entries, len(dates or []) - len(entries)


def inherit_metadata(draft_metadata, payload):
    """Return (payload, kept, undated): the template laid over the metadata the draft inherited.

    A new-version draft starts from the previous record's metadata, including keys
    set in the web interface such as communities and language. Sending the template
    alone would drop them, so they are kept and the template wins on every key it
    has. Only keys the deposit API documents are carried; read-only ones are not,
    and inherited dates entries without a start or an end are not (`undated` counts
    them). `kept` lists the inherited keys the template does not carry.
    """
    sendable = API_METADATA_KEYS - READ_ONLY_KEYS
    inherited = {key: value for key, value in (draft_metadata or {}).items() if key in sendable}
    undated = 0
    if "dates" in inherited and "dates" not in payload["metadata"]:
        inherited["dates"], undated = _dated_entries(inherited["dates"])
        if not inherited["dates"]:
            del inherited["dates"]
    kept = sorted(set(inherited) - set(payload["metadata"]))
    return {"metadata": {**inherited, **payload["metadata"]}}, kept, undated


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
    if getattr(args, "first_release", False):
        return ""
    record = args.record_id or record_id_from(template)
    if not record:
        raise ZenodoError("no record to version from: pass --record-id or add an "
                          "isVersionOf zenodo DOI to the template")
    return record


def _host(sandbox):
    return SANDBOX_URL if sandbox else ZENODO_URL


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _extra_files(values) -> list[ExtraFile]:
    files = []
    for value in values or []:
        path = Path(value).resolve()
        if not path.is_file():
            raise ZenodoError(f"extra file not found: {path}")
        files.append(ExtraFile(path, _sha256(path), path.stat().st_size))
    return files


def _implicit_tooling_root(repo_root: Path, tooling_root: Path) -> Path | None:
    if any((repo_root / path).exists() for path, _ in BUNDLED_FILES):
        return None
    required = list(LICENSE_FILES) + [CREATORS_FILE]
    if any(not (repo_root / path).exists() and (tooling_root / path).is_file()
           for path in required):
        return tooling_root
    return None


def _source_lines(repo_root: Path, tooling_root: Path) -> list[str]:
    lines = [f"repository root: {repo_root}"]
    if tooling_root is not None:
        lines.append(f"tooling root: {tooling_root}")
    relatives = [source for source, _ in BUNDLED_FILES] + list(LICENSE_FILES) + [CREATORS_FILE]
    for relative in relatives:
        _, root_name = _source_path(repo_root, tooling_root, relative)
        if root_name:
            lines.append(f"source: {relative}  {root_name}")
            if relative == "LICENSING.md" and root_name == "tooling root":
                lines.append("notice: LICENSING.md supplied by tooling root; release text may differ")
    return lines


def _prepare(args, out_dir: Path):
    """Return (host, record id, payload, dropped relations, problems, archive, refusals).

    `problems` are reasons the deposit API would reject the metadata;
    `refusals` are reasons this tool will not deposit it.
    """
    repo_root = Path(args.repo_root).resolve()
    tooling_root = (_implicit_tooling_root(repo_root, DEFAULT_TOOLING_ROOT)
                    if args.tooling_root is None else _tooling_root(args.tooling_root))
    extras = _extra_files(args.extra_file)
    template = _collection_dir(repo_root, args.domain, args.version) / METADATA_FILE
    payload, dropped = metadata_payload(template, args.publication_date)
    problems = validate_metadata(payload["metadata"])
    refusals = creator_problems(payload["metadata"], expected_creators(repo_root, tooling_root))
    if getattr(args, "first_release", False):
        if args.record_id:
            refusals.append("--record-id is not valid for a first release; there is no previous record")
        if any(relation.get("relation") == "isNewVersionOf"
               for relation in payload["metadata"].get("related_identifiers") or []):
            refusals.append("a first release cannot carry an isNewVersionOf relation")
        communities = payload["metadata"].get("communities")
        if not communities and args.community:
            payload["metadata"]["communities"] = [{"identifier": args.community}]
    record = _resolve_record_id(args, template)
    archive = build_archive(repo_root, args.domain, args.version, out_dir, tooling_root)
    sources = _source_lines(repo_root, tooling_root)
    return _host(args.sandbox), record, payload, dropped, problems, archive, refusals, sources, extras


def _describe(host, record, payload, dropped, problems, archive, refusals, sources, extras) -> str:
    action = "new record for a first release" if not record else f"new version of record {record}"
    lines = [
        f"target: {host}",
        f"action: {action}",
        "metadata:",
        json.dumps(payload, indent=2, ensure_ascii=False),
        "files:",
        f"  {archive.path.name}  {archive.size} bytes  {archive.entries} entries  sha256 {archive.sha256}",
    ]
    lines += [f"  {extra.path.name}  {extra.size} bytes  sha256 {extra.sha256}" for extra in extras]
    lines += [f"relation {name} read from the template and not sent" for name in dropped]
    lines += [f"rejected by the API: {problem}" for problem in problems]
    lines += [f"refused: {refusal}" for refusal in refusals]
    lines += sources
    return "\n".join(lines)


def run_plan(args) -> int:
    """Print the deposit plan without any request; exit 1 when the metadata is rejected or refused."""
    with tempfile.TemporaryDirectory() as scratch:
        prepared = _prepare(args, Path(scratch))
        print(_describe(*prepared))
    return 1 if prepared[4] or prepared[6] else 0


def run_archive(args) -> int:
    """Build the archive and print its path, sha256 and size."""
    repo_root = Path(args.repo_root).resolve()
    tooling_root = (_implicit_tooling_root(repo_root, DEFAULT_TOOLING_ROOT)
                    if args.tooling_root is None else _tooling_root(args.tooling_root))
    archive = build_archive(repo_root, args.domain, args.version, Path(args.out_dir), tooling_root)
    print(f"{archive.path}\nsha256 {archive.sha256}\nsize {archive.size} bytes\n"
          f"entries {archive.entries}")
    return 0


def validate_prepared(prepared):
    """Stop before a request when preparation found invalid or unsafe metadata."""
    _, _, _, _, problems, _, refusals, _, _ = prepared
    if problems:
        raise ZenodoError("metadata rejected by the API: " + "; ".join(problems))
    if refusals:
        raise ZenodoError("; ".join(refusals))


def upload_files(draft, archive, extras, token):
    """Upload the release archive followed by the extras, in the order supplied."""
    _call("archive upload", "PUT", f"{draft['links']['bucket']}/{archive.path.name}", token, archive.path)
    for extra in extras:
        name = urllib.parse.quote(extra.path.name)
        _call("extra file upload", "PUT", f"{draft['links']['bucket']}/{name}", token, extra.path)


def update_metadata(draft, template, token, base, inherited=True):
    """Apply the template, optionally over metadata inherited by a new-version draft."""
    if inherited:
        payload, kept, undated = inherit_metadata(draft.get("metadata"), template)
    else:
        payload, kept, undated = template, [], 0
    _call("metadata update", "PUT", f"{base}/{draft['id']}", token, payload)
    if kept:
        print("inherited metadata not in the template, kept: " + ", ".join(kept))
    if undated:
        print(f"inherited dates entry without start or end dropped: {undated}")


def print_uploaded_files(archive, extras):
    """Print the exact names and digests sent to the draft bucket."""
    print(f"uploaded {archive.path.name} sha256 {archive.sha256}")
    for extra in extras:
        print(f"uploaded {extra.path.name} sha256 {extra.sha256}")


def create_record(prepared, token):
    """Create an empty deposition and return it without publishing."""
    host = prepared[0]
    return _call("new record", "POST", f"{host}/api/deposit/depositions", token, {})


def run_draft(args) -> int:
    """Create the new-version draft and print its URL. Never publishes."""
    token = _token(args.sandbox)
    prepared = _prepare(args, Path(args.out_dir))
    validate_prepared(prepared)
    host, record, template, _, _, archive, _, _, extras = prepared
    base = f"{host}/api/deposit/depositions"
    created = _call("newversion", "POST", f"{base}/{record}/actions/newversion", token)
    draft = _call("draft fetch", "GET", created["links"]["latest_draft"], token)
    for stale in draft.get("files") or []:
        _call("inherited file delete", "DELETE", f"{base}/{draft['id']}/files/{stale['id']}", token)
    upload_files(draft, archive, extras, token)
    update_metadata(draft, template, token, base)
    url = draft["links"].get("html") or f"{host}/deposit/{draft['id']}"
    print(f"draft {draft['id']} created, not published: {url}")
    print_uploaded_files(archive, extras)
    return 0


def run_create(args) -> int:
    """Create a first-release draft as a new record and print its URL. Never publishes."""
    token = _token(args.sandbox)
    prepared = _prepare(args, Path(args.out_dir))
    validate_prepared(prepared)
    host, _, template, _, _, archive, _, _, extras = prepared
    draft = create_record(prepared, token)
    upload_files(draft, archive, extras, token)
    update_metadata(draft, template, token, f"{host}/api/deposit/depositions", inherited=False)
    url = draft["links"].get("html") or f"{host}/deposit/{draft['id']}"
    print(f"draft {draft['id']} created as a new record, not published: {url}")
    print(f"conceptrecid {draft['conceptrecid']}")
    print_uploaded_files(archive, extras)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    for name, handler, help_text in (
        ("archive", run_archive, "build the release zip"),
        ("plan", run_plan, "print the metadata and files a deposit would send"),
        ("draft", run_draft, "create a new-version draft on Zenodo (never publishes)"),
        ("create", run_create, "create a first-release draft as a new record on Zenodo; never publishes"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.set_defaults(handler=handler)
        command.add_argument("domain", help="collection domain, e.g. metabolomics")
        command.add_argument("version", help="collection version directory, e.g. v2")
        command.add_argument("--repo-root", required=True, help="domain checkout root")
        command.add_argument("--tooling-root", default=None,
                             help="fallback root for tooling and governance files")
        command.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
        if name != "archive":
            command.add_argument("--extra-file", action="append", default=[],
                                 help="additional file to list and upload; repeatable")
            command.add_argument("--sandbox", action="store_true",
                                 help="use sandbox.zenodo.org and ZENODO_SANDBOX_TOKEN")
            command.add_argument("--record-id", default="",
                                 help=("latest published record to version from" if name != "create"
                                       else "invalid: a first release has no previous record"))
            command.add_argument("--publication-date", default=datetime.date.today().isoformat())
        if name in {"draft", "create"}:
            command.set_defaults(first_release=name == "create")
        if name == "create":
            command.add_argument("--community", default=DEFAULT_COMMUNITY,
                                 help="community used when the template has none")
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
