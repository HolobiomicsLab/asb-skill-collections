"""CI gate: the enriched tool catalog is internally consistent. Verifies that
every tool ``license_tier`` is valid, that no tool's licence was inherited from a
paper, that no retired key has returned, every skill ``tools_used`` slug resolves to
a real tool, and every tool ``used_by_skills`` slug resolves to a real skill.
Exit 1 on violations. Mirrors scripts/check_license_tiers.py and
scripts/check_provenance_tiers.py.
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

from scripts.license_tier import (DETECTION_VENDOR_PRODUCT, SUBJECT_TOOL, TIER_UNKNOWN,
                                  TOOL_DETECTIONS, load_map)

# The tier vocabulary has one home: governance/license_tiers.yaml. A hand-copied set
# here silently rejects any tier added there -- which is how `unknown` would have
# been rejected the moment it was introduced.
_VALID = set(load_map()["tiers"])

# Held a citing paper's repository under a name claiming it was the tool's. See #42.
_RETIRED_TOOL_KEYS = ("canonical_url",)


def _licence_provenance_violations(slug, tool, tier) -> list[str]:
    """A resolved tool tier must rest on evidence about the tool itself.

    Two-sided: a resolved tier needs a tool detection and a `tool` subject, and an
    `unknown` tier must not still carry a licence. Without this, a paper's licence
    can be written onto the tool axis and nothing fires, because a value is present.
    """
    out = []
    detection = tool.get("license_detection")
    subject = tool.get("license_subject")
    if tier == TIER_UNKNOWN:
        if tool.get("license"):
            out.append(f"tools_index {slug!r}: tier is unknown but a licence is recorded")
        if subject is not None:
            out.append(f"tools_index {slug!r}: tier is unknown but license_subject is set")
        return out
    if detection not in TOOL_DETECTIONS:
        out.append(
            f"tools_index {slug!r}: tier {tier!r} rests on detection {detection!r}, "
            f"which is not evidence about the tool"
        )
    if subject != SUBJECT_TOOL:
        out.append(
            f"tools_index {slug!r}: tier {tier!r} but license_subject is {subject!r}"
        )
    return out


def _resolution_drift(collection_dir, tools) -> list[str]:
    """tools_index must agree with the resolution it was derived from.

    ``tool_licenses.json`` is the evidence; ``tools_index.json`` is derived from it
    by ``enrich_tools_index.py``. Editing one without re-running the other leaves a
    licence in the catalogue that no evidence supports, which is the whole failure
    class this gate exists for. Skipped when no resolution has been run.
    """
    path = pathlib.Path(collection_dir) / "tool_licenses.json"
    if not path.is_file():
        return []
    resolved = json.loads(path.read_text(encoding="utf-8"))
    by_slug = {t.get("slug"): t for t in tools}
    out = []
    for slug, evidence in resolved.items():
        tool = by_slug.get(slug)
        if tool is None:
            out.append(f"tool_licenses {slug!r}: no such tool in tools_index")
        elif tool.get("license") != evidence.get("license"):
            out.append(
                f"tools_index {slug!r}: licence {tool.get('license')!r} does not match "
                f"the resolved {evidence.get('license')!r}; re-run enrich_tools_index"
            )
    # A vendor product is tiered from the entry-kind vocabulary, not from a licence
    # lookup, so it is legitimately absent from the resolution.
    unbacked = [t.get("slug") for t in tools
                if t.get("license_tier") != TIER_UNKNOWN and t.get("slug") not in resolved
                and t.get("license_detection") != DETECTION_VENDOR_PRODUCT]
    for slug in unbacked:
        out.append(f"tools_index {slug!r}: tiered but absent from tool_licenses.json")
    return out


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
        tier = t.get("license_tier")
        if tier not in _VALID:
            violations.append(f"tools_index {slug!r}: missing/invalid license_tier")
        violations.extend(_licence_provenance_violations(slug, t, tier))
        for key in _RETIRED_TOOL_KEYS:
            if key in t:
                violations.append(
                    f"tools_index {slug!r}: retired key {key!r} is back; a citing "
                    f"paper's repository is not the tool's (see source_paper_repos)"
                )
        for ref in t.get("used_by_skills") or []:
            if ref not in skill_slugs:
                violations.append(
                    f"tools_index {slug!r}: used_by_skills {ref!r} not in skills_index"
                )

    violations.extend(_resolution_drift(d, tools))

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
