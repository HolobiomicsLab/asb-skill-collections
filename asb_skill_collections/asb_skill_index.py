"""Canonical offline selector for collection skills, workflows and tools.

The CLI and MCP import this module. ``scripts/router_shape.py`` embeds its
source verbatim in standalone retrieval scripts. Retrieval needs only the
standard library; the package's separate source-file layout helper is loaded
lazily by ``item_source_path`` and is not needed to search an installed unit.

The two historical scoring rules share resolution, fields, filters, result
explanations and score/slug ordering. The measured default and the temporary
compatibility option are documented in ``docs/selection.md``.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import TypedDict

STOP = frozenset(
    "the a an of for and or to in on with from by use when need data your this that "
    "is are be using into across over per via".split()
)
MAX_TOOLS = 25  # leaves advertising more tools are registry/meta artifacts
ROUTER_STOP = frozenset(
    "a an and are as at be by for from how in is it of on or that the to use using "
    "with what which when data set my our this these those i need want".split()
)
SELECTOR_NAME = "asb-keyword"
SELECTOR_VERSION = "1.0.0"
DEFAULT_SELECTOR = "package"
SELECTOR_ENV = "ASB_SELECTOR_RULE"
SELECTORS = ("package", "router")
TARGETS = {
    "skills": ("skills_index.json",),
    "workflows": ("workflows/workflows_index.json", "workflows_index.json"),
    "tools": ("tools_index.json",),
}


class SelectorIdentity(TypedDict):
    """Versioned scoring implementation, independent of the calling surface."""

    name: str
    version: str
    rule: str


class SelectionFilters(TypedDict):
    """Normalised filters actually applied to the index rows."""

    technique: str | None
    tool: str | None
    edam: str | None
    max_tools: int


class SearchHit(TypedDict):
    """A candidate and its portable, collection-qualified explanation."""

    slug: str
    name: str
    description: str
    score: float
    techniques: list[str]
    tools: list[str]
    collection: str
    target: str
    qualified_slug: str
    selector: SelectorIdentity
    matched_fields: dict[str, list[str]]
    filters: SelectionFilters
    fallback: str


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
    # Uniform tuple element type so mixed numeric/alpha components (e.g. "2" vs
    # "2-rc") compare without TypeError; numeric sorts after alpha within a part.
    return tuple((1, int(p)) if p.isdigit() else (0, p) for p in str(v).split("."))


def unit_root(collection_dir: str | os.PathLike) -> Path:
    """Accept a collection root or its workflow-index directory."""
    base = Path(collection_dir).resolve()
    root_markers = ("skills_index.json", "tools_index.json", "collection.yaml", "kb_bundle.json")
    if base.name != "workflows" or any((base / name).is_file() for name in root_markers):
        return base
    if (base / "workflows_index.json").is_file() or any(
        (base.parent / name).is_file() for name in root_markers
    ):
        return base.parent
    return base


def index_path(collection_dir: Path, target: str) -> Path:
    """Resolve a supported target from the root or inside ``workflows/``.

    Prefer the nested workflow index, with the historical flat layout as a
    fallback. Unknown targets are errors rather than silent skill searches.
    """
    if target not in TARGETS:
        raise ValueError(f"unknown search target: {target!r}")
    base = unit_root(collection_dir)
    candidates = [base / name for name in TARGETS[target]]
    return next((path for path in candidates if path.is_file()), candidates[0])


def load_rows(collection_dir: Path, target: str) -> list[dict]:
    """Read an index, or return no rows for an unpublished target."""
    path = index_path(collection_dir, target)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []


def collection_id(collection_dir: Path) -> str:
    """Qualify a unit using its portable bundle metadata, then its directory.

    Technique packs retain their parent collection/version in ``kb_bundle``.
    Version-directory checkouts and small independent units need no metadata.
    """
    base = unit_root(collection_dir)
    bundle = base / "kb_bundle.json"
    if bundle.is_file():
        metadata = json.loads(bundle.read_text(encoding="utf-8"))
        if metadata.get("collection") and metadata.get("version") is not None:
            version = str(metadata["version"])
            version = version[1:] if version.startswith("v") else version
            return f"{metadata['collection']}/v{version}"
    return f"{base.parent.name}/{base.name}"


def resolve_selector(selector: str | None = None) -> str:
    """Resolve an explicit rule, the CLI environment option, or the default."""
    chosen = selector if selector is not None else os.environ.get(SELECTOR_ENV, DEFAULT_SELECTOR)
    if chosen not in SELECTORS:
        raise ValueError(f"unknown selector: {chosen!r}; choose {', '.join(SELECTORS)}")
    return chosen


def _strings(value) -> list[str]:
    if value is None:
        return []
    return [value] if isinstance(value, str) else [str(item) for item in value]


def entry_tools(row: dict) -> list[str]:
    """Read the tool field used by either a leaf or a composite workflow."""
    return _strings(row.get("tools") or row.get("member_tools"))


def row_fields(row: dict) -> dict[str, str]:
    """Build searchable text once, retaining source field names for explanations."""
    tool_field = "tools" if row.get("tools") else "member_tools"
    return {
        "name": str(row.get("name") or "").lower(),
        "description": str(row.get("description") or "").lower(),
        tool_field: " ".join(entry_tools(row)).lower(),
        "techniques": " ".join(_strings(row.get("techniques"))).lower(),
    }


def row_text(row: dict) -> str:
    """Return the common name, description, tool and technique text."""
    return " ".join(row_fields(row).values())


def tokenize(text: str, selector: str | None = None) -> list[str]:
    """Tokenise with the selected historical rule, without domain vocabulary.

    Package scoring retains repeated Unicode alphanumeric terms of length at
    least three. Router scoring uses unique ASCII terms of length at least two.
    """
    rule = resolve_selector(selector)
    if rule == "router":
        tokens = re.findall(r"[a-z0-9]+", str(text).lower())
        return sorted({term for term in tokens if len(term) > 1 and term not in ROUTER_STOP})
    tokens = "".join(c.lower() if c.isalnum() else " " for c in str(text)).split()
    return [term for term in tokens if len(term) > 2 and term not in STOP]


def _field_matches(fields: dict, terms: list[str], rule: str) -> dict[str, list[str]]:
    if rule == "router":
        return {field: sorted(set(terms) & set(tokenize(text, rule)))
                for field, text in fields.items() if field != "techniques"}
    return {field: sorted({term for term in terms if term in text})
            for field, text in fields.items()}


def _score_row(row: dict, terms: list[str], rule: str) -> tuple[float, dict]:
    fields = row_fields(row)
    matched = {field: values for field, values in _field_matches(fields, terms, rule).items() if values}
    if rule == "router":
        overlap = {term for values in matched.values() for term in values}
        boost = 2.0 if set(terms) & {tool.lower() for tool in entry_tools(row)} else 0.0
        return float(len(overlap)) + boost, matched
    text = " ".join(fields.values())
    score = sum(text.count(term) for term in terms)
    score += 3 * sum(term in fields["name"] for term in terms)
    return float(score), matched


def _normalise_filter(value: str | None) -> str | None:
    return value.strip().casefold() if value else None


def matches_filters(row: dict, filters: SelectionFilters) -> bool:
    """Apply exact technique/tool and EDAM substring filters to either row kind."""
    techniques = {_normalise_filter(tag) for tag in _strings(row.get("techniques"))}
    tools = entry_tools(row)
    if filters["technique"] and filters["technique"] not in techniques:
        return False
    if filters["tool"] and filters["tool"] not in {_normalise_filter(tool) for tool in tools}:
        return False
    if filters["max_tools"] and len(tools) > filters["max_tools"]:
        return False
    edam = [str(row.get("edam_operation") or ""), *_strings(row.get("edam_topics"))]
    return not filters["edam"] or any(filters["edam"] in value.casefold() for value in edam)


def _hit(row: dict, score: float, matched: dict, context: dict) -> SearchHit:
    slug = str(row.get("slug") or "")
    return {
        "slug": slug, "name": str(row.get("name") or ""), "score": score,
        "description": str(row.get("description") or "").strip(),
        "techniques": _strings(row.get("techniques")), "tools": entry_tools(row)[:6],
        "collection": context["collection"], "target": context["target"],
        "qualified_slug": f"{context['collection']}/{context['target']}/{slug}",
        "selector": {"name": SELECTOR_NAME, "version": SELECTOR_VERSION, "rule": context["rule"]},
        "matched_fields": matched, "filters": dict(context["filters"]), "fallback": context["fallback"],
    }


def result_order(hit: dict) -> tuple:
    """Order by descending score, then slug, then collection for duplicate slugs."""
    return -hit["score"], hit["slug"], hit["collection"]


def keyword_search(rows, query, technique=None, k=10, max_tools=None, *,
                   collection="unknown", target="skills", selector=None,
                   tool=None, edam=None, fallback="keyword") -> list[SearchHit]:
    """Filter and rank rows with a typed explanation on every result.

    Pass a qualified ``collection`` when searching rows without a directory.
    Empty text permits browsing/filter-only requests; nonempty text consisting
    only of discarded tokens matches nothing. ``k <= 0`` returns no results.
    The registry guard applies to skills only, never curated workflows/tools.
    """
    if target not in TARGETS:
        raise ValueError(f"unknown search target: {target!r}")
    rule = resolve_selector(selector)
    limit = MAX_TOOLS if max_tools is None else max_tools
    if limit < 0:
        raise ValueError("max_tools must be nonnegative")
    filters: SelectionFilters = {
        "technique": _normalise_filter(technique), "tool": _normalise_filter(tool),
        "edam": _normalise_filter(edam), "max_tools": limit if target == "skills" else 0,
    }
    terms = tokenize(query, rule)
    if k <= 0 or (str(query).strip() and not terms):
        return []
    context = {"collection": collection, "target": target, "rule": rule,
               "filters": filters, "fallback": fallback}
    results = []
    for row in rows:
        if not matches_filters(row, filters):
            continue
        score, matched = _score_row(row, terms, rule) if terms else (1.0, {})
        if score > 0:
            results.append(_hit(row, score, matched, context))
    return sorted(results, key=result_order)[:k]


def item_source_path(collection_dir: Path, target: str, slug: str) -> Path:
    """On-disk path of one item, honouring the collection's layout.

    A router-shaped collection keeps its leaf corpus in ``leaves/`` and only a
    couple of entry points in ``skills/``; a legacy one keeps everything in
    ``skills/``. Hardcoding either name makes every leaf unreachable in the
    other layout, so resolution goes through the canonical resolver.
    """
    from asb_skill_collections import layout

    if target == "workflows":
        return collection_dir / "workflows" / slug / "SKILL.md"
    if target == "tools":
        return collection_dir / "tools" / f"{slug}.yaml"
    for root in layout.skill_dirs(collection_dir):
        candidate = root / slug / "SKILL.md"
        if candidate.is_file():
            return candidate
    return layout.leaf_dir(collection_dir) / slug / "SKILL.md"


def get_item_text(collection: str, target: str, slug: str,
                  root: str | os.PathLike | None = None) -> str | None:
    """Return the raw SKILL.md / tool.yaml text for an item, or None."""
    col_dir = resolve_collection_dir(collection, root)
    if not col_dir:
        return None
    p = item_source_path(col_dir, target, slug)
    return p.read_text() if p.is_file() else None


def search(collection, target, query, technique=None, k=10,
           root: str | os.PathLike | None = None, *, selector=None, tool=None,
           edam=None, max_tools=None, fallback="keyword") -> list[SearchHit]:
    """Discover -> load -> keyword-rank in one call. `collection` may be
    'slug/vN', a bare 'slug' (latest), or None (search every collection)."""
    results = []
    rule = resolve_selector(selector)
    if target not in TARGETS:
        raise ValueError(f"unknown search target: {target!r}")
    if collection:
        col_dir = resolve_collection_dir(collection, root)
        targets = [col_dir] if col_dir else []
    else:
        targets = [Path(c["dir"]) for c in discover_collections(root)]
    for col_dir in targets:
        rows = load_rows(col_dir, target)
        results.extend(keyword_search(
            rows, query, technique, k, max_tools, collection=collection_id(col_dir),
            target=target, selector=rule, tool=tool, edam=edam, fallback=fallback,
        ))
    return sorted(results, key=result_order)[:max(0, k)]
