"""CI gate: every staged community-skill proposal is structurally valid.

Validates each ``proposals/skills/*/SKILL.md`` against the SAME discipline a
published skill must satisfy, plus the community-proposal invariants, so a
maintainer's review is about quality/fit — not structure. For each staged skill:

* ``metadata.provenance_tier == "community"`` and a ``related_skills`` key is
  present (the community provenance invariant);
* top-level ``status == "hold"`` (the proposal-rail invariant);
* ``normalize_skill.frontmatter_violations`` is empty (description discipline,
  EDAM IRI shape, valid ``license_tier``);
* every ``metadata.tools_used`` slug resolves in ``tools_index.json``.

A collection with no ``proposals/`` (or no staged skills) yields no violations.
``main`` exits 1 on any violation, 0 otherwise. Mirrors
scripts/check_tools_index.py and scripts/check_provenance_tiers.py.
"""
from __future__ import annotations

import json
import pathlib
import sys

import yaml

from scripts.normalize_skill import frontmatter_violations


def check_collection(collection_dir) -> list:
    d = pathlib.Path(collection_dir)
    violations: list = []

    skills_dir = d / "proposals" / "skills"
    if not skills_dir.is_dir():
        return violations

    md_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not md_files:
        return violations

    # tool slugs available to resolve tools_used against.
    tool_slugs: set = set()
    tools_path = d / "tools_index.json"
    if tools_path.is_file():
        tools = json.loads(tools_path.read_text(encoding="utf-8"))
        tool_slugs = {t.get("slug") for t in tools}

    for md in md_files:
        slug = md.parent.name
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            violations.append(f"{md}: no frontmatter block")
            continue
        try:
            fm = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        except yaml.YAMLError as e:
            violations.append(f"{md}: invalid frontmatter YAML: {e}")
            continue
        if not isinstance(fm, dict):
            violations.append(f"{md}: frontmatter is not a mapping")
            continue

        meta = fm.get("metadata") or {}

        # community provenance invariant
        prov = meta.get("provenance_tier")
        if prov != "community":
            violations.append(
                f"{md}: metadata.provenance_tier {prov!r} != 'community'"
            )
        if "related_skills" not in fm:
            violations.append(f"{md}: community proposal requires related_skills key")

        # proposal-rail invariant
        status = fm.get("status")
        if status != "hold":
            violations.append(f"{md}: status {status!r} != 'hold'")

        # description + EDAM + license_tier discipline (CI parity)
        for msg in frontmatter_violations(fm):
            violations.append(f"{md}: {msg}")

        # tools_used slugs must resolve in the tool catalog
        for ref in meta.get("tools_used") or []:
            if ref not in tool_slugs:
                violations.append(
                    f"{md}: tools_used {ref!r} not in tools_index.json"
                )

    return violations


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: check_proposals <collection_dir> [...]", file=sys.stderr)
        return 2
    failed = False
    for col in argv:
        v = check_collection(col)
        if v:
            failed = True
            print(f"FAIL {col}:")
            for x in v:
                print(f"  - {x}")
        else:
            print(f"OK   {col}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
