"""CI gate: the enriched tool catalog is internally consistent. Verifies that
every tool ``license_tier`` is valid, every skill ``tools_used`` slug resolves to
a real tool, and every tool ``used_by_skills`` slug resolves to a real skill.
Exit 1 on violations. Mirrors scripts/check_license_tiers.py and
scripts/check_provenance_tiers.py.
"""
from __future__ import annotations

import json
import pathlib
import sys

import yaml

_VALID = {"open", "noncommercial", "restricted"}


def check_collection(collection_dir) -> list[str]:
    d = pathlib.Path(collection_dir)
    violations: list[str] = []

    tools = json.loads((d / "tools_index.json").read_text(encoding="utf-8"))
    skills = json.loads((d / "skills_index.json").read_text(encoding="utf-8"))

    tool_slugs = {t.get("slug") for t in tools}
    skill_slugs = {s.get("slug") for s in skills}
    tier_by_slug = {t.get("slug"): t.get("license_tier") for t in tools}

    # Every tool license_tier is valid; every used_by_skills slug resolves.
    for t in tools:
        slug = t.get("slug")
        if t.get("license_tier") not in _VALID:
            violations.append(f"tools_index {slug!r}: missing/invalid license_tier")
        for ref in t.get("used_by_skills") or []:
            if ref not in skill_slugs:
                violations.append(
                    f"tools_index {slug!r}: used_by_skills {ref!r} not in skills_index"
                )

    # Per-tool YAML license_tier must equal its tools_index license_tier.
    # Tools that have no tools/<slug>.yaml are skipped (not every tool has one).
    tools_dir = d / "tools"
    if tools_dir.is_dir():
        for yaml_path in sorted(tools_dir.glob("*.yaml")):
            slug = yaml_path.stem
            if slug not in tier_by_slug:
                continue
            rec = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
            yaml_tier = rec.get("license_tier")
            if yaml_tier != tier_by_slug[slug]:
                violations.append(
                    f"tools/{slug}.yaml: license_tier {yaml_tier!r} != "
                    f"tools_index {tier_by_slug[slug]!r}"
                )

    # Every skill tools_used slug resolves to a real tool.
    for s in skills:
        slug = s.get("slug")
        for ref in s.get("tools_used") or []:
            if ref not in tool_slugs:
                violations.append(
                    f"skills_index {slug!r}: tools_used {ref!r} not in tools_index"
                )

    return violations


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: check_tools_index <collection_dir> [...]", file=sys.stderr)
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
