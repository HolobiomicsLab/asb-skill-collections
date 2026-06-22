#!/usr/bin/env python3
"""Build search_index.json for the static docs-site full-text search.

Walks `collections/**` and `staged-collections/**` from the repo root,
extracts searchable fields from corpus.yaml, SKILL.md, and tool YAMLs,
and emits docs-site/search_index.json.

Stdlib + PyYAML only (no other deps). Idempotent — overwrites the index
in place. Maintainers re-run this after promote, before committing.

Usage:
    python3 docs-site/build_search_index.py

Output:
    docs-site/search_index.json
    stdout summary: "Indexed N papers, M skills, K tools."
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
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
DOCS_SITE = Path(__file__).resolve().parent
OUTPUT = DOCS_SITE / "search_index.json"

SCHEMA_VERSION = "0.1"
SUMMARY_CHAR_LIMIT = 500


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
    """Return (frontmatter_dict, body_text). Body is everything after the
    closing '---' delimiter; frontmatter is parsed as YAML."""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"warn: failed to read {path}: {exc}\n")
        return None, ""
    if not raw.startswith("---"):
        return None, raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return None, raw
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        sys.stderr.write(f"warn: bad frontmatter in {path}: {exc}\n")
        fm = None
    return fm, parts[2]


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
    paths: list[Path] = []
    for root_name in ("collections", "staged-collections"):
        root = REPO_ROOT / root_name
        if not root.exists():
            continue
        paths.extend(sorted(root.glob("*/v*/corpus.yaml")))
    return paths


def _iter_skill_files() -> list[Path]:
    paths: list[Path] = []
    for root_name in ("collections", "staged-collections"):
        root = REPO_ROOT / root_name
        if not root.exists():
            continue
        paths.extend(sorted(root.glob("*/v*/skills/*/SKILL.md")))
    return paths


def _iter_tool_files() -> list[Path]:
    paths: list[Path] = []
    for root_name in ("collections", "staged-collections"):
        root = REPO_ROOT / root_name
        if not root.exists():
            continue
        paths.extend(sorted(root.glob("*/v*/tools/*.yaml")))
    return paths


def _collection_from_path(path: Path) -> str:
    """Path like .../collections/metabolomics/v1/... -> 'metabolomics/v1'."""
    parts = path.relative_to(REPO_ROOT).parts
    # parts[0] in {collections, staged-collections}; parts[1]=slug; parts[2]=vN
    if len(parts) >= 3:
        return f"{parts[1]}/{parts[2]}"
    return ""


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
                "md_path": str(spath.relative_to(REPO_ROOT)),
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
        canonical_url = data.get("canonical_url") or ""
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
                    canonical_url,
                ],
            )
        )
        out.append(
            {
                "slug": slug,
                "name": name,
                "canonical_url": canonical_url,
                "license_spdx": license_spdx,
                "evidence_text": evidence_text,
                "collection": coll_label,
                "source_doi": source_doi,
                "yaml_path": str(tpath.relative_to(REPO_ROOT)),
                "search_text": search_text,
            }
        )
    return out


def main() -> int:
    papers = index_papers()
    skills = index_skills()
    tools = index_tools()
    collections = sorted(
        {r["collection"] for r in papers + skills + tools if r.get("collection")}
    )

    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "collections": collections,
        "papers": papers,
        "skills": skills,
        "tools": tools,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    size = OUTPUT.stat().st_size
    print(
        f"Indexed {len(papers)} papers, {len(skills)} skills, {len(tools)} tools "
        f"across {len(collections)} collections. "
        f"Wrote {OUTPUT.relative_to(REPO_ROOT)} ({size:,} bytes)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
