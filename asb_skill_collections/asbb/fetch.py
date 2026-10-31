"""Download chosen skills from the published repository, without a checkout.

The named ref is resolved once to a commit through the GitHub commits API, and
every file is then read from the raw file host at that commit: the leaves,
together with the collection's ``skills_index.json``, which validates the
request and supplies each skill's licence tier. Files land under
``<dest>/<slug>/`` beside a ``PROVENANCE.json`` that records the ref, the commit
it resolved to, where each file came from and its SHA-256.

Every network read goes through :func:`_request`, called as
``transport(url)`` or ``transport(url, accept=...)``. Tests pass a transport in
its place, so nothing else in this module touches the network.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from ..layout import LEAF_DIRNAME

REPOSITORY = "HolobiomicsLab/asb-skill-collections"
REPOSITORY_URL = f"https://github.com/{REPOSITORY}"
RAW_HOST = "https://raw.githubusercontent.com"
API_HOST = "https://api.github.com"
#: Asks the commits API for the bare commit id instead of a JSON document.
SHA_MEDIA_TYPE = "application/vnd.github.sha"
#: A full commit id: SHA-1, or SHA-256 for a repository that uses it.
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
DEFAULT_REF = "main"
PROVENANCE_FILE = "PROVENANCE.json"
PROVENANCE_SCHEMA = "asbb-fetch/1"
TIMEOUT_SECONDS = 60
USER_AGENT = "asbb-fetch"
#: ``<collection slug>/v<N>``: the published path of one collection version.
COLLECTION_PATTERN = re.compile(r"[a-z0-9][a-z0-9_-]*/v[0-9]+")
#: A leaf directory name: one path segment, never ``.`` or ``..``.
SLUG_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
#: A branch, tag or commit: slash-separated segments, none starting with ``.``.
REF_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*(?:/[A-Za-z0-9][A-Za-z0-9._-]*)*")


class FetchError(RuntimeError):
    """A fetch that cannot proceed; nothing has been written when it is raised."""


@dataclass(frozen=True)
class FetchRequest:
    """Which skills of which collection version, at which ref of the repository."""

    collection: str
    slugs: tuple[str, ...]
    ref: str = DEFAULT_REF


def _request(url: str, accept: str | None = None) -> bytes:
    """GET one URL and return its body. The only network call in this module."""
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        raise FetchError(f"{url}: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise FetchError(f"{url}: {exc.reason}") from exc


def raw_url(ref: str, path: str) -> str:
    """The raw-file URL of one repository path at one ref."""
    return f"{RAW_HOST}/{REPOSITORY}/{urllib.parse.quote(ref, safe='/')}/{path}"


def commit_url(ref: str) -> str:
    """The commits API URL that resolves one ref of the repository."""
    return f"{API_HOST}/repos/{REPOSITORY}/commits/{urllib.parse.quote(ref, safe='/')}"


def resolve_commit(ref: str, transport) -> str:
    """Return the commit ``ref`` names now, asked once of the commits API.

    A branch moves, so a fetch recorded against ``main`` alone cannot be
    repeated. Every file is read at the commit returned here, and both the ref
    and the commit are recorded. A ref that is already a full commit id names
    itself and is returned without a call, so a pinned fetch does not depend
    on the API's rate limit.
    """
    if COMMIT_PATTERN.fullmatch(ref):
        return ref
    url = commit_url(ref)
    try:
        body = transport(url, accept=SHA_MEDIA_TYPE)
    except FetchError as exc:
        hint = ""
        if str(exc).endswith(("HTTP 403", "HTTP 429")):
            hint = (
                " (the unauthenticated GitHub API allows 60 requests an hour"
                " per address; retry later, or pass --ref <full commit id>)"
            )
        raise FetchError(f"cannot resolve ref {ref!r} to a commit: {exc}{hint}") from exc
    commit = body.decode("ascii", errors="replace").strip()
    if not COMMIT_PATTERN.fullmatch(commit):
        raise FetchError(f"{url}: expected a commit id, got {commit[:80]!r}")
    return commit


def leaf_path(collection: str, slug: str) -> str:
    """Repository path of a leaf in a router-shaped collection.

    The remote tree cannot be inspected for its shape the way
    :func:`asb_skill_collections.layout.leaf_dir` inspects a local one, so a
    legacy-shaped collection answers HTTP 404 here rather than a partial result.
    """
    return f"collections/{collection}/{LEAF_DIRNAME}/{slug}/SKILL.md"


def _check_request(request: FetchRequest) -> None:
    """Refuse a request whose parts could leave the repository's raw-file tree.

    The ref is checked as strictly as the slugs: the raw host resolves ``..``
    in a URL path, so a ref such as ``x/../main`` or ``../../<owner>/<repo>/main``
    would read another tree while PROVENANCE.json still names this repository.
    """
    if not REF_PATTERN.fullmatch(request.ref) or ".." in request.ref:
        raise FetchError(f"not a git ref: {request.ref!r}")
    if not COLLECTION_PATTERN.fullmatch(request.collection):
        raise FetchError(
            f"collection {request.collection!r} must be <slug>/v<N>, e.g. metabolomics/v2"
        )
    if not request.slugs:
        raise FetchError("the selection is empty: name at least one skill slug")
    malformed = [slug for slug in request.slugs if not SLUG_PATTERN.fullmatch(slug)]
    if malformed:
        raise FetchError(f"not a skill slug: {', '.join(malformed)}")


def _check_destination(request: FetchRequest, dest: Path) -> None:
    """Refuse to overwrite: a destination holds one fetch and its provenance."""
    taken = [name for name in (PROVENANCE_FILE, *request.slugs) if (dest / name).exists()]
    if taken:
        raise FetchError(
            f"{dest} already holds {', '.join(taken)}; fetch into a new or empty directory"
        )


def _license_tiers(request: FetchRequest, commit: str, transport) -> dict[str, str]:
    """Read the remote index at ``commit``, refuse unknown slugs, return each tier."""
    url = raw_url(commit, f"collections/{request.collection}/skills_index.json")
    rows = json.loads(transport(url))
    if not isinstance(rows, list):
        raise FetchError(f"{url}: expected a JSON list of skill rows")
    tiers = {row.get("slug"): row.get("license_tier") for row in rows if isinstance(row, dict)}
    unknown = [slug for slug in request.slugs if slug not in tiers]
    if unknown:
        raise FetchError(
            f"{len(unknown)} slug(s) not in {request.collection} at {request.ref}: "
            + ", ".join(unknown)
        )
    return {slug: tiers[slug] or "unrecorded" for slug in request.slugs}


def _provenance(request: FetchRequest, commit: str, tiers: dict, files: dict) -> dict:
    return {
        "schema": PROVENANCE_SCHEMA,
        "repository": REPOSITORY_URL,
        "ref": request.ref,
        "commit": commit,
        "collection": request.collection,
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "slugs": list(request.slugs),
        "license_tiers": tiers,
        "files": {
            rel: {"url": url, "sha256": hashlib.sha256(body).hexdigest()}
            for rel, (url, body) in files.items()
        },
    }


def fetch(request: FetchRequest, dest: Path, transport=None) -> dict:
    """Download the requested leaves into ``dest`` and return the provenance written.

    Everything is validated and downloaded before the first write, so a refused
    request or a failed download leaves the destination as it was.
    """
    transport = transport or _request
    request = FetchRequest(request.collection, tuple(dict.fromkeys(request.slugs)), request.ref)
    dest = Path(dest)
    _check_request(request)
    _check_destination(request, dest)
    commit = resolve_commit(request.ref, transport)
    tiers = _license_tiers(request, commit, transport)
    files = {}
    for slug in request.slugs:
        url = raw_url(commit, leaf_path(request.collection, slug))
        files[f"{slug}/SKILL.md"] = (url, transport(url))
    for rel, (_, body) in files.items():
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        (dest / rel).write_bytes(body)
    provenance = _provenance(request, commit, tiers, files)
    (dest / PROVENANCE_FILE).write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return provenance
