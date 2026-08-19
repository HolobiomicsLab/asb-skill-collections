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
import shutil
import sys
from pathlib import Path

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from scripts import layout

REPO = Path(__file__).resolve().parent.parent
SEARCH_SCRIPT = REPO / "collections" / "metabolomics" / "v2" / "bin" / "search_skills.py"
ROUTER_SLUG = "_router"

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

## 2. Apply

Read the chosen `leaves/<slug>/SKILL.md`. Its frontmatter carries `tools` (what
to install or invoke), `derived_from` (source paper DOIs) and `evidence_spans`
(verbatim anchors from the paper or repo). Follow the body.

## 3. Ground (recommended)

Before trusting a parameter, threshold or default, verify it against the paper
the skill was built from. `kb_bundle.json` maps each skill to its source KBs:

```bash
python bin/perspicacite_kb_bind.py query --skill <slug> \\
  --question "<what you need to verify>"
```

See `GROUNDING.md` for the backends and tiers.

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


def write_router(unit: Path, count: int) -> None:
    """Write the single advertised entry-point skill."""
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
    )
    out = unit / layout.ADVERTISED_DIRNAME / ROUTER_SLUG
    out.mkdir(parents=True, exist_ok=True)
    (out / "SKILL.md").write_text(body, encoding="utf-8")


def shape(unit: Path, source_index: Path, keep: set[str]) -> dict:
    """Apply the whole conversion to one unit and report what changed."""
    slugs = set(leaf_slugs(unit))
    moved = move_leaves(unit, keep | {ROUTER_SLUG})
    (unit / "bin").mkdir(exist_ok=True)
    shutil.copy2(SEARCH_SCRIPT, unit / "bin" / "search_skills.py")
    indexed = write_index(unit, source_index, slugs)
    write_router(unit, indexed or len(slugs))
    return {"unit": str(unit), "moved": moved, "indexed": indexed, "leaves": len(slugs)}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("units", nargs="+", help="unit directories to convert")
    p.add_argument("--index", required=True, help="parent skills_index.json to subset")
    p.add_argument("--keep", default="", help="comma-separated slugs to keep advertised")
    args = p.parse_args(argv)
    keep = {s for s in args.keep.split(",") if s}
    for raw in args.units:
        print(shape(Path(raw), Path(args.index), keep))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
