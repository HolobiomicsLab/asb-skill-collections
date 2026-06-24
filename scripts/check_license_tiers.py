"""CI gate: every corpus + skills_index entry carries a valid license_tier, and
each SKILL.md tool_license block is internally consistent. Exit 1 on violations.
"""
from __future__ import annotations

import json
import pathlib
import sys

import yaml

from scripts.license_tier import ack_required

_VALID = {"open", "noncommercial", "restricted"}


def check_collection(collection_dir) -> list[str]:
    d = pathlib.Path(collection_dir)
    violations: list[str] = []

    corpus = yaml.safe_load((d / "corpus.yaml").read_text(encoding="utf-8"))
    for p in corpus.get("papers", []):
        if p.get("license_tier") not in _VALID:
            violations.append(f"corpus entry {p.get('name')!r}: missing/invalid license_tier")

    si = json.loads((d / "skills_index.json").read_text(encoding="utf-8"))
    # Build slug→index_tier map for cross-check
    slug_to_index_tier = {}
    for e in si:
        if e.get("license_tier") not in _VALID:
            violations.append(f"skills_index {e.get('slug')!r}: missing/invalid license_tier")
        else:
            slug_to_index_tier[e.get("slug")] = e.get("license_tier")

    for md in (d / "skills").glob("*/SKILL.md"):
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        fm = yaml.safe_load(text.split("---\n", 2)[1]) or {}

        # Cross-check: frontmatter tier vs index tier
        slug = md.parent.name
        if slug in slug_to_index_tier:
            fm_tier = (fm.get("metadata") or {}).get("license_tier")
            index_tier = slug_to_index_tier[slug]
            if fm_tier not in _VALID:
                violations.append(f"{md}: metadata.license_tier missing/invalid")
            elif fm_tier != index_tier:
                violations.append(f"{md}: metadata.license_tier {fm_tier!r} != skills_index {index_tier!r}")

        tl = (fm.get("metadata") or {}).get("tool_license")
        if not tl:
            continue
        if tl.get("tier") not in _VALID:
            violations.append(f"{md}: tool_license.tier invalid")
        elif tl.get("requires_ack") != ack_required(tl["tier"]):
            violations.append(f"{md}: requires_ack inconsistent with tier {tl['tier']}")
    return violations


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: check_license_tiers <collection_dir> [...]", file=sys.stderr)
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
