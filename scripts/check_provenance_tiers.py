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
# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))


from asb_skill_collections import layout
from scripts.provenance_tier import validate_entry


def _repo_urls(collection_dir) -> dict[str, str]:
    """Each skill's declared ``metadata.repo_url``, keyed by slug."""
    out: dict[str, str] = {}
    for md in layout.iter_skill_md(collection_dir):
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        fm = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        url = (fm.get("metadata") or {}).get("repo_url")
        if str(url or "").strip():
            out[md.parent.name] = url
    return out


def check_collection(collection_dir) -> list[str]:
    d = pathlib.Path(collection_dir)
    violations: list[str] = []

    si = json.loads((d / "skills_index.json").read_text(encoding="utf-8"))
    # A `repository`-tier entry keeps its repo_url in the SKILL.md, not the
    # index, so the invariant needs both sides.
    repos = _repo_urls(d)
    # Build slug→index_tier map for cross-check against SKILL.md frontmatter.
    slug_to_index_tier: dict[str, str] = {}
    for e in si:
        slug = e.get("slug")
        tier = e.get("provenance_tier")
        problems = validate_entry(
            tier,
            dois=e.get("dois"),
            synthesized_from=e.get("synthesized_from"),
            related_skills=e.get("related_skills"),
            repo_url=repos.get(slug),
        )
        for msg in problems:
            violations.append(f"skills_index {slug!r}: {msg}")
        if not problems:
            slug_to_index_tier[slug] = tier

    # A router-shaped collection keeps its corpus in `leaves/`; globbing a
    # hardcoded `skills/` there cross-checks the two entry points and reports a
    # clean pass over the other 5,857 skills.
    for md in layout.iter_skill_md(d):
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
