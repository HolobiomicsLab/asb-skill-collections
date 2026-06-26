"""CI gate: every skills_index entry carries a valid provenance_tier (per
scripts.provenance_tier.validate_entry), and each SKILL.md
``metadata.provenance_tier`` matches its skills_index entry. Exit 1 on
violations. Mirrors scripts/check_license_tiers.py.
"""
from __future__ import annotations

import json
import pathlib
import sys

import yaml

from scripts.provenance_tier import validate_entry


def check_collection(collection_dir) -> list[str]:
    d = pathlib.Path(collection_dir)
    violations: list[str] = []

    si = json.loads((d / "skills_index.json").read_text(encoding="utf-8"))
    # Build slug→index_tier map for cross-check against SKILL.md frontmatter.
    slug_to_index_tier: dict[str, str] = {}
    for e in si:
        slug = e.get("slug")
        tier = e.get("provenance_tier")
        for msg in validate_entry(
            tier,
            dois=e.get("dois"),
            synthesized_from=e.get("synthesized_from"),
            related_skills=e.get("related_skills"),
        ):
            violations.append(f"skills_index {slug!r}: {msg}")
        if not validate_entry(tier, dois=e.get("dois")):
            slug_to_index_tier[slug] = tier

    for md in (d / "skills").glob("*/SKILL.md"):
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        fm = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        slug = md.parent.name
        if slug not in slug_to_index_tier:
            continue
        fm_tier = (fm.get("metadata") or {}).get("provenance_tier")
        index_tier = slug_to_index_tier[slug]
        if fm_tier is None:
            violations.append(f"{md}: metadata.provenance_tier missing")
        elif fm_tier != index_tier:
            violations.append(
                f"{md}: metadata.provenance_tier {fm_tier!r} != skills_index {index_tier!r}"
            )
    return violations


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: check_provenance_tiers <collection_dir> [...]", file=sys.stderr)
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
