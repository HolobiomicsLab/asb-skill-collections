"""Shared, dependency-light skill/workflow/tool index access for ASB collections.

Single source of truth for "discover collections" + "keyword-search an index" +
"resolve an item's source file", used by BOTH the `asbb` CLI (`search`/`get`) and
the MCP skill-server (`asb_mcp_server.py`). Keeps the retrieval contract identical
across surfaces (and aligned with each collection's own `bin/semantic_search.py`
keyword mode), with no third-party dependency — pure stdlib, so it ships in the
thin wheel and runs anywhere (uvx, pipx, plain python).

This module is collection-agnostic: it reads slugs/text from the on-disk indexes
and never names a domain, slug, or DOI (generalize-or-stop).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

# Mirror bin/semantic_search.py: stopwords, junk-leaf guard, keyword scoring.
STOP = set(
    "the a an of for and or to in on with from by use when need data your this that "
    "is are be using into across over per via".split()
)
MAX_TOOLS = 25  # leaves advertising more tools are registry/meta artifacts


def collections_root(root: str | os.PathLike | None = None) -> Path:
    """Resolve the directory that contains `collections/`. Honors
    ASB_COLLECTIONS_ROOT, else the given root, else walks up from CWD."""
    if root:
        return Path(root)
    env = os.environ.get("ASB_COLLECTIONS_ROOT")
    if env:
        return Path(env)
    here = Path.cwd()
    for cand in [here, *here.parents]:
        if (cand / "collections").is_dir():
            return cand
    return here


def discover_collections(root: str | os.PathLike | None = None) -> list[dict]:
    """Find every `collections/<slug>/v<N>` with a skills_index.json.

    Returns dicts: {slug, version, dir, skills_count, has_workflows, has_tools}.
    Enriches with title/counts from catalogue.jsonld when present."""
    base = collections_root(root)
    cat = {}
    cat_path = base / "catalogue.jsonld"
    if cat_path.is_file():
        try:
            for c in json.loads(cat_path.read_text()).get("collections", []):
                cat[f"{c.get('slug')}/v{c.get('version')}"] = c
        except (json.JSONDecodeError, OSError):
            pass
    out = []
    cdir = base / "collections"
    if not cdir.is_dir():
        return out
    for skills_idx in sorted(cdir.glob("*/v*/skills_index.json")):
        col_dir = skills_idx.parent
        slug = col_dir.parent.name
        version = col_dir.name.lstrip("v")
        meta = cat.get(f"{slug}/v{version}", {})
        out.append({
            "slug": slug,
            "version": version,
            "id": f"{slug}/v{version}",
            "dir": str(col_dir),
            "title": meta.get("title", f"{slug} v{version}"),
            "skills_count": meta.get("skills_count"),
            "tools_count": meta.get("tools_count"),
            "has_workflows": (col_dir / "workflows" / "workflows_index.json").is_file(),
            "has_tools": (col_dir / "tools_index.json").is_file(),
        })
    return out


def resolve_collection_dir(collection: str, root: str | os.PathLike | None = None) -> Path | None:
    """Map 'metabolomics/v2' (or 'metabolomics' = latest) to its directory."""
    cols = discover_collections(root)
    if not cols:
        return None
    if "/" in collection:
        match = next((c for c in cols if c["id"] == collection), None)
        return Path(match["dir"]) if match else None
    # bare slug -> highest version
    same = [c for c in cols if c["slug"] == collection]
    if not same:
        return None
    best = max(same, key=lambda c: _ver_key(c["version"]))
    return Path(best["dir"])


def _ver_key(v: str):
    return tuple(int(p) if p.isdigit() else p for p in str(v).split("."))


def index_path(collection_dir: Path, target: str) -> Path:
    if target == "workflows":
        return collection_dir / "workflows" / "workflows_index.json"
    if target == "tools":
        return collection_dir / "tools_index.json"
    return collection_dir / "skills_index.json"


def load_rows(collection_dir: Path, target: str) -> list[dict]:
    p = index_path(collection_dir, target)
    return json.loads(p.read_text()) if p.is_file() else []


def _row_text(r: dict) -> str:
    tools = r.get("tools") or r.get("member_tools") or []
    return " ".join([
        r.get("name", ""), r.get("description", ""),
        " ".join(tools), " ".join(r.get("techniques", [])),
    ]).lower()


def _keep(r: dict, technique: str | None, max_tools: int) -> bool:
    if technique and technique.lower() not in [t.lower() for t in r.get("techniques", [])]:
        return False
    if max_tools and len(r.get("tools", [])) > max_tools:
        return False
    return True


def keyword_search(rows, query, technique=None, k=10, max_tools=MAX_TOOLS):
    """Keyword index search identical in spirit to bin/semantic_search.py's
    offline mode (no embedding backend needed)."""
    terms = [t for t in "".join(c.lower() if c.isalnum() else " " for c in query).split()
             if t not in STOP and len(t) > 2]
    scored = []
    for r in rows:
        if not _keep(r, technique, max_tools):
            continue
        text = _row_text(r)
        score = sum(text.count(t) for t in terms) + 3 * sum(t in r.get("name", "").lower() for t in terms)
        if score:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    out = []
    for s, r in scored[:k]:
        out.append({
            "slug": r.get("slug"), "name": r.get("name"), "score": s,
            "description": (r.get("description") or "").strip(),
            "techniques": r.get("techniques", []),
            "tools": (r.get("tools") or r.get("member_tools") or [])[:6],
        })
    return out


def item_source_path(collection_dir: Path, target: str, slug: str) -> Path:
    if target == "workflows":
        return collection_dir / "workflows" / slug / "SKILL.md"
    if target == "tools":
        return collection_dir / "tools" / f"{slug}.yaml"
    return collection_dir / "skills" / slug / "SKILL.md"


def get_item_text(collection: str, target: str, slug: str,
                  root: str | os.PathLike | None = None) -> str | None:
    """Return the raw SKILL.md / tool.yaml text for an item, or None."""
    col_dir = resolve_collection_dir(collection, root)
    if not col_dir:
        return None
    p = item_source_path(col_dir, target, slug)
    return p.read_text() if p.is_file() else None


def search(collection, target, query, technique=None, k=10,
           root: str | os.PathLike | None = None) -> list[dict]:
    """Discover -> load -> keyword-rank in one call. `collection` may be
    'slug/vN', a bare 'slug' (latest), or None (search every collection)."""
    results = []
    if collection:
        col_dir = resolve_collection_dir(collection, root)
        targets = [(collection, col_dir)] if col_dir else []
    else:
        targets = [(c["id"], Path(c["dir"])) for c in discover_collections(root)]
    # workflows guard does not apply to curated composites
    max_tools = MAX_TOOLS if target == "skills" else 0
    for col_id, col_dir in targets:
        rows = load_rows(col_dir, target)
        for hit in keyword_search(rows, query, technique, k, max_tools):
            hit["collection"] = col_id
            results.append(hit)
    results.sort(key=lambda h: -h["score"])
    return results[:k]
