#!/usr/bin/env python3
"""Build the per-domain search index of the docs site from domain checkouts.

The index is a directory, ``docs-site/search_index/``, with one ``<slug>.json``
per registry domain and a ``manifest.json`` that records, for each domain, the
file's sha256 and size, the indexed collections and their counts, and a
``registry_digest`` over the registry fields that determine that file.

A domain is rebuilt only from a ``--checkout slug=path``, and only after every
release it indexes has been verified against the registry (tree digest and
counts, as ``scripts/check_collections_manifest.py`` does). A domain without a
checkout keeps its existing file when the manifest still matches it and the
registry; otherwise the build is refused and nothing is written. No domain is
dropped silently.

The output depends only on the trees: no build time is recorded, every walk is
in sorted path order and JSON keys are sorted, so two builds of the same trees
are byte-identical.

``--check-manifest`` reads no checkout: it verifies that the committed files
and their manifest still match ``collections.yaml``. CI runs it.

Usage:
    python docs-site/build_search_index.py --checkout metabolomics=/path/to/domain
    python docs-site/build_search_index.py --check-manifest
    python docs-site/build_search_index.py --default-domain metabolomics

Stdlib + PyYAML only (no other deps).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write(
        "PyYAML is required: pip install pyyaml (or use the project's env)\n"
    )
    sys.exit(1)

# Repo root = parent of docs-site/
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from asb_skill_collections import layout  # noqa: E402  (needs REPO_ROOT on the path)
from scripts.check_collections_manifest import (  # noqa: E402
    parse_checkout,
    release_path_drift,
    validate_checkout,
)
from scripts.skill_index import split_frontmatter  # noqa: E402
DOCS_SITE = Path(__file__).resolve().parent
INDEX_DIR = DOCS_SITE / "search_index"
MANIFEST_NAME = "manifest.json"

SCHEMA_VERSION = "0.2"
MANIFEST_SCHEMA_VERSION = "1"
INITIAL_DEFAULT_DOMAINS = ("metabolomics",)
SUMMARY_CHAR_LIMIT = 500
_COLLECTIONS: dict[Path, dict] = {}


def _strip_html(text: str) -> str:
    """Remove rudimentary HTML tags (titles sometimes contain <i>...</i>)."""
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text)


def _collection_label(collection: str, version: int | str) -> str:
    """Render '<slug>/v<N>' for display + grouping."""
    return f"{collection}/v{version}"


def _load_yaml(path: Path) -> dict | None:
    try:
        with path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except (OSError, yaml.YAMLError) as exc:
        sys.stderr.write(f"warn: failed to parse {path}: {exc}\n")
        return None


def _parse_skill_md(path: Path) -> tuple[dict | None, str]:
    """Return (frontmatter_dict, body_text) via the canonical SKILL.md parser."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"warn: failed to read {path}: {exc}\n")
        return None, ""
    frontmatter, body = split_frontmatter(raw)
    if frontmatter is None:
        sys.stderr.write(f"warn: bad frontmatter in {path}\n")
    return frontmatter, body


def _extract_summary(body: str) -> str:
    """Pull the '## Summary' section text, up to SUMMARY_CHAR_LIMIT chars.
    Falls back to the first chunk of body if no Summary heading exists."""
    if not body:
        return ""
    m = re.search(
        r"^##\s+Summary\s*\n+(.+?)(?=\n##\s|\Z)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    text = m.group(1).strip() if m else body.strip()
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text[:SUMMARY_CHAR_LIMIT]


def _iter_corpus_files() -> list[Path]:
    return [
        root / "corpus.yaml"
        for root in sorted(_COLLECTIONS)
        if (root / "corpus.yaml").is_file()
    ]


def _iter_skill_files() -> list[Path]:
    """Every leaf SKILL.md, from whichever directory a collection's layout uses.

    Router-shaped collections keep the corpus in `leaves/`, legacy ones in
    `skills/`. Globbing one of them drops the other silently, so resolution
    goes through the same helper the release gate uses.
    """
    return [
        path
        for collection in sorted(_COLLECTIONS)
        for path in layout.iter_skill_md(collection)
    ]


def _iter_workflow_files() -> list[Path]:
    return [
        path
        for collection in sorted(_COLLECTIONS)
        for path in sorted((collection / "workflows").glob("*/SKILL.md"))
        if not path.parent.name.startswith("_")
    ]


def _iter_tool_files() -> list[Path]:
    return [
        path
        for collection in sorted(_COLLECTIONS)
        for path in sorted((collection / "tools").glob("*.yaml"))
    ]


def _collection_from_path(path: Path) -> str:
    """Return the manifest label for a file in an indexed checkout."""
    for collection, info in _COLLECTIONS.items():
        if collection == path or collection in path.parents:
            return info["label"]
    return ""


def _source_path(path: Path) -> str:
    """Return a checkout-relative POSIX source path."""
    for collection, info in _COLLECTIONS.items():
        if collection == path or collection in path.parents:
            return path.relative_to(info["checkout"]).as_posix()
    return path.as_posix()


def index_papers() -> list[dict]:
    out: list[dict] = []
    for cpath in _iter_corpus_files():
        data = _load_yaml(cpath)
        if not data:
            continue
        slug = data.get("collection") or ""
        ver = data.get("collection_version") or ""
        coll_label = (
            _collection_label(slug, ver)
            if slug and ver
            else _collection_from_path(cpath)
        )
        for paper in data.get("papers") or []:
            doi = (paper.get("doi") or "").strip()
            title = _strip_html(paper.get("title") or "")
            rationale = paper.get("rationale") or ""
            status = paper.get("status") or ""
            access = paper.get("access") or {}
            access_type = access.get("type") if isinstance(access, dict) else ""
            derived_skills = paper.get("derived_skills") or 0
            derived_tools = paper.get("derived_tools") or 0
            search_text = " ".join(
                filter(
                    None,
                    [doi, title, rationale, status, access_type or "", coll_label],
                )
            )
            out.append(
                {
                    "doi": doi,
                    "title": title,
                    "rationale": rationale,
                    "collection": coll_label,
                    "status": status,
                    "access_type": access_type or "unknown",
                    "derived_skills": int(derived_skills or 0),
                    "derived_tools": int(derived_tools or 0),
                    "search_text": search_text,
                }
            )
    return out


def index_skills() -> list[dict]:
    out: list[dict] = []
    for spath in _iter_skill_files():
        fm, body = _parse_skill_md(spath)
        if not isinstance(fm, dict):
            continue
        name = fm.get("name") or spath.parent.name
        description = fm.get("description") or ""
        when_negative = fm.get("when_to_use_negative") or []
        if isinstance(when_negative, list):
            when_negative_text = " ".join(str(x) for x in when_negative)
        else:
            when_negative_text = str(when_negative)
        edam_topics = fm.get("edam_topics") or []
        if not isinstance(edam_topics, list):
            edam_topics = [edam_topics]
        provenance = fm.get("provenance") or {}
        source_papers = provenance.get("source_papers") or []
        source_dois = [
            sp.get("doi") for sp in source_papers if isinstance(sp, dict) and sp.get("doi")
        ]
        # Also catch derived_from at top level
        derived_from = fm.get("derived_from") or []
        for d in derived_from:
            if isinstance(d, dict) and d.get("doi"):
                if d["doi"] not in source_dois:
                    source_dois.append(d["doi"])
        summary = _extract_summary(body)
        coll_label = _collection_from_path(spath)
        search_text = " ".join(
            filter(
                None,
                [
                    name,
                    description,
                    when_negative_text,
                    " ".join(str(t) for t in edam_topics),
                    summary,
                    coll_label,
                    " ".join(source_dois),
                ],
            )
        )
        out.append(
            {
                "name": name,
                "description": description,
                "when_to_use_negative": when_negative_text,
                "edam_topics": [str(t) for t in edam_topics],
                "collection": coll_label,
                "summary": summary,
                "source_dois": source_dois,
                "md_path": _source_path(spath),
                "search_text": search_text,
            }
        )
    return out


def index_workflows() -> list[dict]:
    """Index composite-workflow super-skills (one row per workflows/<slug>/SKILL.md)."""
    out: list[dict] = []
    for wpath in _iter_workflow_files():
        fm, body = _parse_skill_md(wpath)
        if not isinstance(fm, dict):
            continue
        name = fm.get("name") or wpath.parent.name
        description = fm.get("description") or ""
        meta = fm.get("metadata") or {}
        techniques = meta.get("techniques") or []
        if not isinstance(techniques, list):
            techniques = [techniques]
        member_skills = meta.get("member_skills") or []
        if not isinstance(member_skills, list):
            member_skills = [member_skills]
        stage_count = meta.get("stage_count") or 0
        summary = _extract_summary(body)
        coll_label = _collection_from_path(wpath)
        search_text = " ".join(
            filter(
                None,
                [
                    name,
                    description,
                    " ".join(str(t) for t in techniques),
                    " ".join(str(s) for s in member_skills),
                    summary,
                    coll_label,
                ],
            )
        )
        out.append(
            {
                "slug": wpath.parent.name,
                "name": name,
                "description": description,
                "techniques": [str(t) for t in techniques],
                "stage_count": stage_count,
                "collection": coll_label,
                "summary": summary,
                "md_path": _source_path(wpath),
                "search_text": search_text,
            }
        )
    return out


def index_tools() -> list[dict]:
    out: list[dict] = []
    for tpath in _iter_tool_files():
        data = _load_yaml(tpath)
        if not isinstance(data, dict):
            continue
        slug = data.get("slug") or tpath.stem
        name = data.get("name") or slug
        # Repositories of the papers that cite this tool -- not the tool's own
        # home. `canonical_url` claimed the latter while holding the former (#42).
        source_repos = [str(r) for r in (data.get("source_repos") or []) if r]
        license_spdx = data.get("license_spdx") or ""
        evidence_spans = data.get("evidence_spans") or []
        if isinstance(evidence_spans, list):
            evidence_text = " ".join(str(x) for x in evidence_spans)
        else:
            evidence_text = str(evidence_spans)
        source_doi = data.get("source_paper_doi") or ""
        coll_label = _collection_from_path(tpath)
        search_text = " ".join(
            filter(
                None,
                [
                    slug,
                    name,
                    license_spdx,
                    evidence_text,
                    source_doi,
                    coll_label,
                    " ".join(source_repos),
                ],
            )
        )
        out.append(
            {
                "slug": slug,
                "name": name,
                "source_paper_repos": source_repos,
                "license_spdx": license_spdx,
                "evidence_text": evidence_text,
                "collection": coll_label,
                "source_doi": source_doi,
                "yaml_path": _source_path(tpath),
                "search_text": search_text,
            }
        )
    return out


def collection_statuses(labels: list[str]) -> dict[str, str]:
    """Map indexed labels to their manifest status ("released" or "staged")."""
    statuses = {info["label"]: info["status"] for info in _COLLECTIONS.values()}
    return {label: statuses.get(label, "staged") for label in labels}


class BuildRefused(Exception):
    """The index cannot be built as asked; nothing has been written."""

    def __init__(self, failures: list[str]):
        super().__init__("\n".join(failures))
        self.failures = failures


def _indexed_releases(domain: dict, include_superseded: bool) -> list[dict]:
    """The releases of one domain the site indexes.

    The latest published release of a domain plus its legacy trees, unless
    ``include_superseded`` asks for every release: a superseded release doubles
    the index for text the latest release carries in a newer form.
    """
    releases = [r for r in (domain or {}).get("releases") or [] if isinstance(r, dict)]
    if include_superseded:
        return releases
    published = [r for r in releases if r.get("status") != "legacy"]
    legacy = [r for r in releases if r.get("status") == "legacy"]
    latest = max(published, key=lambda r: int(r["version"]), default=None)
    return ([latest] if latest else []) + legacy


def registry_digest(slug: str, domain: dict, include_superseded: bool) -> str:
    """sha256 over the registry fields that determine one domain's index file.

    Only the indexed releases count, each by path, version, status, commit and
    tree digest, in version order. A registry edit elsewhere (another domain, a
    DOI, a date, a count) leaves the digest, and so the file, valid.
    """
    rows = sorted(
        (
            {
                "path": release.get("path"),
                "version": release.get("version"),
                "status": release.get("status"),
                "commit": release.get("commit"),
                "tree_digest": release.get("tree_digest"),
            }
            for release in _indexed_releases(domain, include_superseded)
        ),
        key=lambda row: (str(row["version"]), str(row["path"])),
    )
    canonical = json.dumps(
        {"domain": slug, "include_superseded": bool(include_superseded), "releases": rows},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_checkout(slug: str, domain: dict, checkout: Path, include_superseded: bool) -> list[str]:
    """Refuse to index a checkout whose release trees are not the registered ones.

    A release with a ``tree_digest`` is checked as the registry check does it:
    digest of the working tree and counts. A release without one falls back to
    git: its path must hold exactly the bytes of its ``commit``, with no
    untracked file. A release with neither cannot be verified and is refused.
    """
    failures = []
    if not checkout.is_dir():
        return [f"{slug}: checkout is not a directory: {checkout}"]
    for release in _indexed_releases(domain, include_superseded):
        label = _collection_label(slug, release.get("version", "?"))
        if release.get("tree_digest"):
            failures.extend(validate_checkout(label, release, checkout))
        elif release.get("commit"):
            try:
                drift = release_path_drift(checkout, release["commit"], str(release.get("path")))
            except ValueError as error:
                failures.append(f"{label}: cannot verify the checkout: {error}")
                continue
            if drift:
                failures.append(
                    f"{label}: checkout differs from {release['commit']} at "
                    + ", ".join(drift[:5]) + (" ..." if len(drift) > 5 else "")
                )
        else:
            failures.append(f"{label}: registry row has neither tree_digest nor commit to verify against")
    return [
        failure + f" (checkout {checkout} is not the registered release; check out the registered commit)"
        for failure in failures
    ]


def _select_collections(slug: str, domain: dict, checkout: Path | None, include_superseded: bool) -> None:
    """Point the walkers at the indexed releases of one domain in its checkout.

    Staged trees (``staged-collections/``) are not indexed: no registry row
    describes them, so nothing could verify them or tell when they change.
    """
    global _COLLECTIONS
    _COLLECTIONS = {}
    if checkout is None:
        return
    for release in _indexed_releases(domain, include_superseded):
        _COLLECTIONS[checkout / release["path"]] = {
            "label": _collection_label(slug, release["version"]),
            "checkout": checkout,
            "commit": release.get("commit"),
            "status": "staged" if release.get("status") == "legacy" else "released",
        }


def build_domain(
    slug: str, domain: dict, checkout: Path | None, include_superseded: bool = False
) -> dict:
    """Build one domain's payload from its (already verified) checkout."""
    _select_collections(slug, domain, checkout, include_superseded)
    papers = index_papers()
    skills = index_skills()
    workflows = index_workflows()
    tools = index_tools()
    collections = sorted(
        {r["collection"] for r in papers + skills + workflows + tools if r.get("collection")}
    )
    commits = {
        info["label"]: info["commit"]
        for info in _COLLECTIONS.values()
        if info["label"] in collections and info["commit"] is not None
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "domain": slug,
        "collections": collections,
        "collection_status": collection_statuses(collections),
        "collection_commits": dict(sorted(commits.items())),
        "papers": papers,
        "skills": skills,
        "workflows": workflows,
        "tools": tools,
    }


def serialize(payload: dict) -> str:
    """The exact text written to disk, so a byte comparison is meaningful."""
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _manifest_entry(
    slug: str, domain: dict, payload: dict, data: bytes, include_superseded: bool
) -> dict:
    statuses = {info["label"]: info for info in _COLLECTIONS.values()}
    return {
        "file": f"{slug}.json",
        "sha256": _sha256(data),
        "bytes": len(data),
        "include_superseded": bool(include_superseded),
        "registry_digest": registry_digest(slug, domain, include_superseded),
        "collections": [
            {
                "label": label,
                "status": statuses[label]["status"] if label in statuses else "staged",
                "commit": statuses[label]["commit"] if label in statuses else None,
            }
            for label in sorted(statuses)
        ],
        "counts": {key: len(payload[key]) for key in ("papers", "skills", "tools", "workflows")},
    }


def _load_registry(path: Path) -> dict:
    document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    domains = document.get("domains") or {}
    if not isinstance(domains, dict):
        raise BuildRefused([f"{path}: domains must be a mapping"])
    return domains


def _load_index_manifest(index_dir: Path) -> dict | None:
    path = index_dir / MANIFEST_NAME
    if not path.is_file():
        return None
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return document if isinstance(document, dict) else None


def _kept_entry_failure(
    slug: str, domain: dict, entry: dict | None, index_dir: Path, include_superseded: bool
) -> str | None:
    """Why the existing file of a domain without a checkout cannot be kept, or None."""
    hint = f"; pass --checkout {slug}=<path to its registered checkout>"
    if not isinstance(entry, dict):
        return f"{slug}: no index file recorded in the manifest and no checkout{hint}"
    if bool(entry.get("include_superseded")) != bool(include_superseded):
        return f"{slug}: index was built with include_superseded={bool(entry.get('include_superseded'))}{hint}"
    if entry.get("registry_digest") != registry_digest(slug, domain, include_superseded):
        return f"{slug}: index is stale, its registry rows changed{hint}"
    path = index_dir / str(entry.get("file") or "")
    if entry.get("file") != f"{slug}.json" or not path.is_file():
        return f"{slug}: index file {entry.get('file')!r} is missing{hint}"
    if path.stat().st_size != entry.get("bytes") or _file_sha256(path) != entry.get("sha256"):
        return f"{slug}: index file {path.name} does not match its recorded sha256 and size{hint}"
    return None


def build(
    registry_path: Path,
    index_dir: Path,
    checkouts: dict[str, Path],
    include_superseded: bool = False,
    default_domains: list[str] | None = None,
) -> tuple[dict, dict[str, bytes], list[str]]:
    """Plan an index build without writing: manifest, files to write, files to remove.

    Raises ``BuildRefused`` with every reason when a domain cannot be built or kept.
    """
    domains = _load_registry(registry_path)
    failures = [
        f"{slug}: --checkout names a domain that is not in {registry_path.name}"
        for slug in sorted(set(checkouts) - set(domains))
    ]
    previous = _load_index_manifest(index_dir) or {}
    previous_entries = previous.get("domains") if isinstance(previous.get("domains"), dict) else {}
    entries: dict[str, dict] = {}
    writes: dict[str, bytes] = {}
    for slug in sorted(domains):
        domain = domains[slug] or {}
        checkout = checkouts.get(slug)
        if checkout is None and _indexed_releases(domain, include_superseded):
            failure = _kept_entry_failure(
                slug, domain, previous_entries.get(slug), index_dir, include_superseded
            )
            if failure:
                failures.append(failure)
            else:
                entries[slug] = previous_entries[slug]
            continue
        if checkout is not None:
            problems = verify_checkout(slug, domain, checkout, include_superseded)
            if problems:
                failures.extend(problems)
                continue
        payload = build_domain(slug, domain, checkout, include_superseded)
        data = serialize(payload).encode("utf-8")
        entries[slug] = _manifest_entry(slug, domain, payload, data, include_superseded)
        writes[f"{slug}.json"] = data
    if default_domains is not None:
        unknown = sorted(set(default_domains) - set(domains))
        failures.extend(f"--default-domain {slug}: not a registry domain" for slug in unknown)
        defaults = default_domains
    elif isinstance(previous.get("default_domains"), list):
        defaults = [str(slug) for slug in previous["default_domains"]]
    else:
        defaults = list(INITIAL_DEFAULT_DOMAINS)
    if failures:
        raise BuildRefused(failures)
    manifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "default_domains": sorted({slug for slug in defaults if slug in entries}),
        "domains": entries,
    }
    removals = sorted(
        str(entry.get("file"))
        for slug, entry in previous_entries.items()
        if slug not in domains and isinstance(entry, dict) and entry.get("file") == f"{slug}.json"
    )
    return manifest, writes, removals


def _write_atomic(path: Path, data: bytes) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(data)
    temporary.replace(path)


def write_index(index_dir: Path, manifest: dict, writes: dict[str, bytes], removals: list[str]) -> Path:
    """Write the domain files first and the manifest last."""
    index_dir.mkdir(parents=True, exist_ok=True)
    for name, data in sorted(writes.items()):
        _write_atomic(index_dir / name, data)
    for name in removals:
        (index_dir / name).unlink(missing_ok=True)
    path = index_dir / MANIFEST_NAME
    _write_atomic(path, (serialize(manifest) + "\n").encode("utf-8"))
    return path


def check_index(registry_path: Path, target: Path) -> list[str]:
    """Verify a committed index against the registry without any checkout."""
    index_dir = target.parent if target.name == MANIFEST_NAME else target
    manifest_path = index_dir / MANIFEST_NAME
    if not manifest_path.is_file():
        return [f"{manifest_path}: missing"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"{manifest_path}: unreadable: {error}"]
    if not isinstance(manifest, dict) or manifest.get("schema_version") != MANIFEST_SCHEMA_VERSION:
        return [f"{manifest_path}: schema_version must be {MANIFEST_SCHEMA_VERSION!r}"]
    try:
        domains = _load_registry(registry_path)
    except BuildRefused as error:
        return error.failures
    entries = manifest.get("domains")
    if not isinstance(entries, dict):
        return [f"{manifest_path}: domains must be a mapping"]
    failures = []
    for slug in sorted(set(domains) - set(entries)):
        failures.append(f"{slug}: registry domain has no index entry")
    for slug in sorted(set(entries) - set(domains)):
        failures.append(f"{slug}: index entry for a domain that is not in the registry")
    for slug in sorted(set(domains) & set(entries)):
        entry = entries[slug]
        if not isinstance(entry, dict):
            failures.append(f"{slug}: index entry must be a mapping")
            continue
        include = bool(entry.get("include_superseded"))
        if entry.get("registry_digest") != registry_digest(slug, domains[slug] or {}, include):
            failures.append(f"{slug}: registry_digest is stale, the registry rows of this domain changed")
        path = index_dir / str(entry.get("file") or "")
        if entry.get("file") != f"{slug}.json" or not path.is_file():
            failures.append(f"{slug}: index file {entry.get('file')!r} is missing")
            continue
        if path.stat().st_size != entry.get("bytes"):
            failures.append(f"{slug}: {path.name} has {path.stat().st_size} bytes, manifest says {entry.get('bytes')}")
        elif _file_sha256(path) != entry.get("sha256"):
            failures.append(f"{slug}: {path.name} sha256 differs from the manifest")
    defaults = manifest.get("default_domains")
    if not isinstance(defaults, list) or any(slug not in entries for slug in defaults):
        failures.append(f"default_domains {defaults!r} must list indexed domains")
    recorded = {entry.get("file") for entry in entries.values() if isinstance(entry, dict)}
    for path in sorted(index_dir.glob("*.json")):
        if path.name != MANIFEST_NAME and path.name not in recorded:
            failures.append(f"{path.name}: file not recorded in the manifest")
    return failures


def _display(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build the docs-site per-domain search index.")
    ap.add_argument("--manifest", type=Path, default=REPO_ROOT / "collections.yaml",
                    help="Registry to read (default: collections.yaml)")
    ap.add_argument(
        "--checkout",
        action="append",
        type=parse_checkout,
        default=[],
        metavar="SLUG=PATH",
        help="Domain checkout to verify and index; repeatable. Other domains keep their files.",
    )
    ap.add_argument(
        "--include-superseded",
        action="store_true",
        help="Index every release of a domain, not only the latest published one and the legacy trees",
    )
    ap.add_argument(
        "--default-domain",
        action="append",
        default=None,
        metavar="SLUG",
        help="Domain the search page loads by default; repeatable. Absent: keep the manifest's value.",
    )
    ap.add_argument(
        "--check-manifest",
        nargs="?",
        type=Path,
        const=INDEX_DIR,
        default=None,
        metavar="INDEX_DIR_OR_MANIFEST",
        help="Verify the committed index against the registry, reading no checkout",
    )
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=INDEX_DIR,
        help="Index directory (default: docs-site/search_index)",
    )
    args = ap.parse_args(argv)
    if args.check_manifest is not None:
        failures = check_index(args.manifest, args.check_manifest)
        if failures:
            for failure in failures:
                print(f"error: {failure}", file=sys.stderr)
            return 1
        print(f"OK: search index {_display(args.check_manifest)} matches {_display(args.manifest)}")
        return 0
    checkouts = dict(args.checkout)
    if len(checkouts) != len(args.checkout):
        print("error: each --checkout slug must be unique", file=sys.stderr)
        return 2
    try:
        manifest, writes, removals = build(
            args.manifest, args.output_dir, checkouts, args.include_superseded, args.default_domain
        )
    except BuildRefused as refusal:
        for failure in refusal.failures:
            print(f"error: {failure}", file=sys.stderr)
        print("error: search index not written", file=sys.stderr)
        return 1
    path = write_index(args.output_dir, manifest, writes, removals)
    for slug, entry in sorted(manifest["domains"].items()):
        counts = entry["counts"]
        action = "rebuilt" if entry["file"] in writes else "kept"
        print(
            f"{action} {slug}: {counts['papers']} papers, {counts['skills']} skills, "
            f"{counts['workflows']} workflows, {counts['tools']} tools in "
            f"{len(entry['collections'])} collections ({entry['bytes']:,} bytes)"
        )
    for name in removals:
        print(f"removed {name}: its domain left the registry")
    print(f"Wrote {_display(path)}; default domains: {', '.join(manifest['default_domains']) or 'none'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
