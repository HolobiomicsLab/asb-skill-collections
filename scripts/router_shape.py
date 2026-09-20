#!/usr/bin/env python3
"""Convert a skill unit to the router-shaped layout.

A plugin host advertises every skill under a unit's ``skills/`` directory by
injecting its name and description into the session prompt, so a unit with
hundreds or thousands of leaves costs more context than a session can spare
just by being installed. This moves the leaf corpus to ``leaves/`` — still
shipped, still installed, but read on demand — and leaves behind a single
router skill plus the retrieval script and index it needs.

Idempotent: re-running on an already-shaped unit refreshes the router,
retrieval script and index without moving anything.

    python scripts/router_shape.py packs/metabolomics/lc-ms \\
        --index collections/metabolomics/v2/skills_index.json
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from asb_skill_collections import layout
from scripts.skill_index import parse_frontmatter

REPO = Path(__file__).resolve().parent.parent
SEARCH_SCRIPT = REPO / "collections" / "metabolomics" / "v2" / "bin" / "search_skills.py"
SELECTOR_SOURCE = REPO / "asb_skill_collections" / "asb_skill_index.py"
SELECTOR_BEGIN = b"# BEGIN VENDORED SELECTOR\n"
SELECTOR_END = b"# END VENDORED SELECTOR\n"
ROUTER_SLUG = "_router"
MAX_CONTRACT_LEAVES = 20
TOOL_FIELDS = ("tools", "metadata.tools")
SOURCE_FIELDS = ("derived_from", "provenance.source_papers")

APPLY_WITH_EVIDENCE = """## 2. Apply

Read the chosen `leaves/<slug>/SKILL.md`. Its frontmatter carries {tool_keys} (what
to install or invoke), {source_keys} (source paper DOIs) and `evidence_spans`
(verbatim anchors from the paper or repo). Follow the body."""

APPLY_WITH_BODY_EVIDENCE = """## 2. Apply

Read the chosen `leaves/<slug>/SKILL.md`. Its frontmatter carries {tool_keys} (what
to install or invoke) and {source_keys} (source paper DOIs). Find
verbatim evidence lines in the body, then follow the procedure."""

GROUND_WITH_BINDER = """## 3. Ground (recommended)

Before trusting a parameter, threshold or default, verify it against the paper
the skill was built from. `kb_bundle.json` maps each skill to its source KBs:

```bash
python bin/perspicacite_kb_bind.py query --skill <slug> \\
  --question "<what you need to verify>"
```{guide}"""

GROUND_FROM_DOIS = """## 3. Ground (recommended)

Before trusting a parameter, threshold or default, verify it against the
source-paper DOIs of the leaf{source_pointer}.{guide}"""

ROUTER_TEMPLATE = """---
name: {router_name}
description: {description}
license: CC-BY-4.0
metadata:
  skills_count: {count}
  leaf_dir: leaves
  retrieval: bin/search_skills.py
  indexes:
  - skills_index.json
schema_version: 0.2.0
---

# {title} — router

Entry point for **{count:,} evidence-grounded skills**, each distilled from a
peer-reviewed method paper and its public code repository.

## How this unit is laid out

The leaf skills live in **`leaves/<slug>/SKILL.md`**, not in `skills/`. A plugin
host loads the name and description of everything under `skills/` into the
session prompt, so advertising the whole corpus would cost far more context than
the work itself. Only this router is advertised; the corpus ships beside it as
data.

**Do not enumerate `leaves/`, and do not read `skills_index.json` whole.**
Search it, then read the one skill you need.

## 1. Search

```bash
python bin/search_skills.py --query "<the user's task>" -k 10
```

Standard library only — no network, no API key. Narrow with `--tool <name>`,
`--technique <tag>` or `--edam <iri-substring>` when the user is already
specific. Each hit prints the exact path to read.

{apply_section}

{grounding_section}

## Licence tiers

Read each candidate's `license_tier` before presenting it. `open` — surface
freely. `noncommercial` — commercial use forbidden without a separate licence;
get explicit confirmation of an academic or non-commercial purpose first.
`restricted` — no clear licence detected; surface that caveat before use.
"""


def leaf_slugs(unit: Path) -> list[str]:
    """Slugs the unit ships, from whichever layout it currently uses."""
    return sorted(d.name for d in layout.slug_dirs(unit))


def move_leaves(unit: Path, keep: set[str]) -> int:
    """Move every skill except `keep` out of the advertised dir. Returns count."""
    advertised = unit / layout.ADVERTISED_DIRNAME
    target = unit / layout.LEAF_DIRNAME
    if not advertised.is_dir():
        return 0
    target.mkdir(exist_ok=True)
    moved = 0
    for child in sorted(advertised.iterdir()):
        if not child.is_dir() or child.name in keep:
            continue
        shutil.move(str(child), str(target / child.name))
        moved += 1
    return moved


def write_index(unit: Path, source_index: Path, slugs: set[str]) -> int:
    """Write the unit's own skills_index.json as a subset of a parent index."""
    rows = json.loads(source_index.read_text(encoding="utf-8"))
    subset = [r for r in rows if r.get("slug") in slugs]
    (unit / "skills_index.json").write_text(
        json.dumps(subset, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return len(subset)


def unit_contract(unit: Path) -> dict:
    """Describe the frontmatter and grounding capabilities a unit ships."""
    leaves = unit / layout.LEAF_DIRNAME
    directories = (
        sorted(path for path in leaves.iterdir() if path.is_dir())
        if leaves.is_dir()
        else layout.slug_dirs(unit)
    )
    skill_files = [
        path / "SKILL.md"
        for path in directories
        if (path / "SKILL.md").is_file()
    ][:MAX_CONTRACT_LEAVES]
    frontmatters = [parse_frontmatter(path) for path in skill_files]
    tool_fields = tuple(
        field for field in TOOL_FIELDS if any(
            (field == "tools" and field in fm)
            or (
                field == "metadata.tools"
                and isinstance(fm.get("metadata"), dict)
                and "tools" in fm["metadata"]
            )
            for fm in frontmatters
        )
    )
    source_fields = tuple(
        field for field in SOURCE_FIELDS if any(
            (field == "derived_from" and field in fm)
            or (
                field == "provenance.source_papers"
                and isinstance(fm.get("provenance"), dict)
                and "source_papers" in fm["provenance"]
            )
            for fm in frontmatters
        )
    )
    tool_keys = " and ".join(f"`{field}`" for field in tool_fields)
    source_keys = " and ".join(f"`{field}`" for field in source_fields)
    has_evidence_spans = any("evidence_spans" in fm for fm in frontmatters)
    has_binder = (unit / "bin" / "perspicacite_kb_bind.py").is_file()
    has_guide = (unit / "GROUNDING.md").is_file()
    apply_template = APPLY_WITH_EVIDENCE if has_evidence_spans else APPLY_WITH_BODY_EVIDENCE
    guide = "\n\nSee `GROUNDING.md` for the backends and tiers." if has_guide else ""
    if has_binder:
        grounding_section = GROUND_WITH_BINDER.format(guide=guide)
    else:
        pointer = f", listed in its {source_keys} frontmatter" if source_keys else ""
        grounding_section = GROUND_FROM_DOIS.format(
            source_pointer=pointer, guide=guide
        )
    return {
        "tool_fields": tool_fields,
        "source_fields": source_fields,
        "tool_keys": tool_keys,
        "source_keys": source_keys,
        "evidence_location": (
            "`evidence_spans`" if has_evidence_spans
            else "verbatim evidence lines in the body"
        ),
        "has_binder": has_binder,
        "has_guide": has_guide,
        "apply_section": apply_template.format(
            tool_keys=tool_keys, source_keys=source_keys
        ),
        "grounding_section": grounding_section,
    }


def _section_is_current(section: str, number: int, contract: dict) -> bool:
    """Return whether one existing router section describes the unit contract."""
    if number == 3:
        has_binder = "perspicacite_kb_bind.py" in section
        has_guide = "GROUNDING.md" in section
        if contract["has_binder"]:
            return has_binder and (not has_guide or contract["has_guide"])
        expected = all(
            f"`{field}`" in section for field in contract["source_fields"]
        )
        absent = set(SOURCE_FIELDS) - set(contract["source_fields"])
        has_phantom = any(f"`{field}`" in section for field in absent)
        points_to_dois = "source-paper DOI" in section
        return (
            not has_binder
            and has_guide == contract["has_guide"]
            and expected
            and points_to_dois
            and not has_phantom
        )

    expected_tools = contract["tool_fields"]
    has_tools = all(f"`{field}`" in section for field in expected_tools)
    legacy_alias = (
        expected_tools == ("metadata.tools",)
        and section.splitlines()[0] != "## 2. Apply"
        and "`tools`" in section
    )
    has_tools = has_tools or legacy_alias
    has_sources = all(
        f"`{field}`" in section for field in contract["source_fields"]
    )
    has_evidence_field = "`evidence_spans`" in section
    has_body_evidence = "verbatim evidence lines in the body" in section
    if contract["evidence_location"] == "`evidence_spans`":
        evidence = has_evidence_field and not has_body_evidence
    else:
        evidence = has_body_evidence and not has_evidence_field
    absent_sources = set(SOURCE_FIELDS) - set(contract["source_fields"])
    has_phantom_source = any(
        f"`{field}`" in section for field in absent_sources
    )
    absent_tools = set(TOOL_FIELDS) - set(expected_tools)
    has_phantom_tool = any(f"`{field}`" in section for field in absent_tools)
    if legacy_alias:
        has_phantom_tool = False
    return (
        has_tools
        and has_sources
        and evidence
        and not has_phantom_source
        and not has_phantom_tool
    )


def _refresh_router_sections(body: str, contract: dict) -> str:
    """Replace only stale Apply/Ground sections in an existing router."""
    rendered = body
    replacements = {2: contract["apply_section"], 3: contract["grounding_section"]}
    for number, replacement in replacements.items():
        pattern = re.compile(rf"^## {number}\.[^\n]*\n.*?(?=^## |\Z)", re.M | re.S)
        match = pattern.search(rendered)
        if match and not _section_is_current(match.group(), number, contract):
            rendered = (
                rendered[:match.start()]
                + replacement
                + "\n\n"
                + rendered[match.end():]
            )
    return rendered


def write_router(unit: Path, count: int) -> None:
    """Write the single advertised entry-point skill."""
    contract = unit_contract(unit)
    out = unit / layout.ADVERTISED_DIRNAME / ROUTER_SLUG / "SKILL.md"
    if out.is_file():
        existing = out.read_text(encoding="utf-8")
        refreshed = _refresh_router_sections(existing, contract)
        if refreshed != existing:
            out.write_text(refreshed, encoding="utf-8")
        return
    meta = json.loads((unit / ".claude-plugin" / "plugin.json").read_text())
    name, description = meta["name"], meta["description"]
    title = description.split(".")[0].strip() or name
    body = ROUTER_TEMPLATE.format(
        router_name=f"{name}-router",
        description=(
            f"Use when a task needs a skill from {title} — search this unit's "
            f"{count:,} evidence-grounded skills, then apply and optionally "
            f"ground the one that fits."
        ),
        title=title,
        count=count,
        apply_section=contract["apply_section"],
        grounding_section=contract["grounding_section"],
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")


def embed_selector(script: bytes) -> bytes:
    """Replace a marked vendor block with the canonical module's exact bytes."""
    if script.count(SELECTOR_BEGIN) != 1 or script.count(SELECTOR_END) != 1:
        raise ValueError("retrieval script must contain exactly one selector block")
    before, body = script.split(SELECTOR_BEGIN)
    _, after = body.split(SELECTOR_END)
    return before + SELECTOR_BEGIN + SELECTOR_SOURCE.read_bytes() + SELECTOR_END + after


def refresh_scripts(unit: Path) -> dict:
    """Regenerate standalone selectors without changing indexes or skill files.

    The collection router supplies the wrapper for technique packs. Existing
    semantic wrappers retain their embedding implementation; only their marked
    keyword selector is regenerated.
    """
    scripts = {unit / "bin" / "search_skills.py": SEARCH_SCRIPT.read_bytes()}
    semantic = unit / "bin" / "semantic_search.py"
    if semantic.is_file():
        scripts[semantic] = semantic.read_bytes()
    updated = []
    for path, template in scripts.items():
        generated = embed_selector(template)
        if not path.is_file() or path.read_bytes() != generated:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(generated)
            updated.append(str(path))
    return {"unit": str(unit), "updated": updated}


def shape(unit: Path, source_index: Path, keep: set[str]) -> dict:
    """Apply the whole conversion to one unit and report what changed."""
    slugs = set(leaf_slugs(unit))
    moved = move_leaves(unit, keep | {ROUTER_SLUG})
    refresh_scripts(unit)
    indexed = write_index(unit, source_index, slugs)
    write_router(unit, indexed or len(slugs))
    return {"unit": str(unit), "moved": moved, "indexed": indexed, "leaves": len(slugs)}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("units", nargs="+", help="unit directories to convert")
    p.add_argument("--index", help="parent skills_index.json to subset (required for conversion)")
    p.add_argument("--keep", default="", help="comma-separated slugs to keep advertised")
    p.add_argument("--scripts-only", action="store_true",
                   help="refresh vendored selectors only; do not move leaves or rewrite indexes")
    args = p.parse_args(argv)
    if not args.scripts_only and not args.index:
        p.error("--index is required unless --scripts-only is used")
    keep = {s for s in args.keep.split(",") if s}
    for raw in args.units:
        if args.scripts_only:
            print(refresh_scripts(Path(raw)))
        else:
            print(shape(Path(raw), Path(args.index), keep))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
