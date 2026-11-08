#!/usr/bin/env python3
"""Build search_index.json from explicit domain-repository checkouts.

``collections.yaml`` lists released trees. Each ``--checkout slug=path`` adds
that domain's releases and any staged tree to the index. Missing checkouts are
reported and skipped; a build with no checkouts is refused.

Stdlib + PyYAML only (no other deps). Idempotent: overwrites the index
in place. Maintainers re-run this after promote, before committing.

The output depends only on the tree: no build time is recorded and every walk
is in sorted path order, so two builds of one tree are byte-identical. CI
relies on that to compare a fresh build with the committed index.

Usage:
    python docs-site/build_search_index.py --checkout metabolomics=/path/to/domain
    python docs-site/build_search_index.py --output /tmp/search_index.json

Output:
    docs-site/search_index.json, or the --output path
    stdout summary: "Indexed N papers, M skills, K tools."
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
from scripts.check_collections_manifest import parse_checkout  # noqa: E402
from scripts.skill_index import split_frontmatter  # noqa: E402
DOCS_SITE = Path(__file__).resolve().parent
OUTPUT = DOCS_SITE / "search_index.json"

SCHEMA_VERSION = "0.1"
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
    """Map indexed labels to their manifest or staging status."""
    statuses = {info["label"]: info["status"] for info in _COLLECTIONS.values()}
    return {label: statuses.get(label, "staged") for label in labels}


def _indexed_releases(domain: dict, include_superseded: bool) -> list[dict]:
    """The releases of one domain the site indexes.

    The latest published release of a domain plus its legacy trees, unless
    ``include_superseded`` asks for every release: a superseded release doubles
    the index for text the latest release carries in a newer form.
    """
    releases = [r for r in domain.get("releases", []) if isinstance(r, dict)]
    if include_superseded:
        return releases
    published = [r for r in releases if r.get("status") != "legacy"]
    legacy = [r for r in releases if r.get("status") == "legacy"]
    latest = max(published, key=lambda r: int(r["version"]), default=None)
    return ([latest] if latest else []) + legacy


def _discover_collections(
    manifest: dict, checkouts: dict[str, Path], include_superseded: bool = False
) -> None:
    """Resolve manifest releases and staged trees in supplied checkouts."""
    global _COLLECTIONS
    _COLLECTIONS = {}
    for slug, domain in sorted(manifest.get("domains", {}).items()):
        checkout = checkouts.get(slug)
        if checkout is None:
            sys.stderr.write(f"warning: no checkout for {slug}; skipping its releases\n")
            continue
        for release in _indexed_releases(domain, include_superseded):
            collection = checkout / release["path"]
            _COLLECTIONS[collection] = {
                "label": _collection_label(slug, release["version"]),
                "checkout": checkout,
                "commit": release.get("commit"),
                "status": "staged" if release.get("status") == "legacy" else "released",
            }
        staged_root = checkout / "staged-collections" / slug
        for collection in sorted(staged_root.glob("v*")):
            _COLLECTIONS[collection] = {
                "label": f"{slug}/{collection.name}",
                "checkout": checkout,
                "commit": None,
                "status": "staged",
            }


def build_index(
    manifest_path: Path | None = None,
    checkouts: dict[str, Path] | None = None,
    include_superseded: bool = False,
) -> dict:
    """Build a deterministic payload from a manifest and domain checkouts."""
    manifest_path = manifest_path or REPO_ROOT / "collections.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    _discover_collections(manifest, checkouts or {}, include_superseded)
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
        "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
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


def _display(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Build the docs-site full-text search index.")
    ap.add_argument("--manifest", type=Path, default=REPO_ROOT / "collections.yaml")
    ap.add_argument(
        "--checkout",
        action="append",
        type=parse_checkout,
        default=[],
        metavar="SLUG=PATH",
        help="Domain checkout to index; repeatable",
    )
    ap.add_argument(
        "--include-superseded",
        action="store_true",
        help="Index every release of a domain, not only the latest published one and the legacy trees",
    )
    ap.add_argument(
        "--check-manifest",
        type=Path,
        metavar="INDEX_JSON",
        help="Only compare the index's recorded manifest digest with the current one",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write the index here instead of docs-site/search_index.json.",
    )
    args = ap.parse_args(argv)
    if args.check_manifest is not None:
        expected = hashlib.sha256(args.manifest.read_bytes()).hexdigest()
        recorded = json.loads(args.check_manifest.read_text(encoding="utf-8")).get(
            "manifest_sha256"
        )
        if recorded == expected:
            print(f"OK: search index matches {args.manifest}")
            return 0
        print(
            f"error: search index manifest_sha256 {recorded!r} != current {expected!r}",
            file=sys.stderr,
        )
        return 1
    if not args.checkout:
        print(
            "error: at least one --checkout slug=path is required to build the search index",
            file=sys.stderr,
        )
        return 2
    checkouts = dict(args.checkout)
    if len(checkouts) != len(args.checkout):
        print("error: each --checkout slug must be unique", file=sys.stderr)
        return 2
    output = args.output if args.output is not None else OUTPUT

    payload = build_index(args.manifest, checkouts, args.include_superseded)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(serialize(payload), encoding="utf-8")
    size = output.stat().st_size
    staged = sum(1 for v in payload["collection_status"].values() if v != "released")
    print(
        f"Indexed {len(payload['papers'])} papers, {len(payload['skills'])} skills, "
        f"{len(payload['workflows'])} workflows, {len(payload['tools'])} tools across "
        f"{len(payload['collections'])} collections ({staged} staged). "
        f"Wrote {_display(output)} ({size:,} bytes)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
