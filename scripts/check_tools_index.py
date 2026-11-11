"""CI gate: the enriched tool catalog is internally consistent. Verifies that
every tool ``license_tier`` is valid, that no tool's licence was inherited from a
paper, that a resolved licence names where it was read, that the catalogue agrees
with the resolution it was derived from, that no retired key has returned, every
skill ``tools_used`` slug resolves to a real tool, and every tool ``used_by_skills``
slug resolves to a real skill. Exit 1 on violations. Each collection's line also
reports how many tools carry a resolved licence, so a collection that ends all
`unknown` is visible. Mirrors scripts/check_license_tiers.py and
scripts/check_provenance_tiers.py. Offline: no gate makes a network call.
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
from scripts.recorded_path import recorded_path

# The tier vocabulary has one home: governance/license_tiers.yaml. A hand-copied set
# here silently rejects any tier added there -- which is how `unknown` would have
# been rejected the moment it was introduced.
_VALID = set(load_map()["tiers"])

# Held a citing paper's repository under a name claiming it was the tool's. See #42.
_RETIRED_TOOL_KEYS = ("canonical_url",)
USAGE = "usage: check_tools_index.py <collection_dir> [<collection_dir> ...]"

# Detections written by scripts/resolve_tool_licenses.py from a registry or the
# reviewed map. A tier resting on one of them must name where it was read.
RESOLVER_DETECTIONS = frozenset({"bioconductor-package", "bioconda-package", "cran-package",
                                 "pypi-package", "biotools-entry", "reviewed-map",
                                 "repository-licence-file"})


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
    if detection in RESOLVER_DETECTIONS and not tool.get("license_evidence"):
        out.append(
            f"tools_index {slug!r}: tier {tier!r} from {detection!r} names no "
            f"license_evidence (the registry page or reviewed statement it was read from)"
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
        # Without the evidence file nothing can back a resolved tier. A catalogue
        # that claims one anyway has drifted from (or never had) its resolution.
        claimed = [t.get("slug") for t in tools
                   if t.get("license_tier") not in (TIER_UNKNOWN, None)
                   and t.get("license_detection") != DETECTION_VENDOR_PRODUCT]
        return [f"tools_index {slug!r}: tiered but tool_licenses.json is absent"
                for slug in claimed]
    resolved = json.loads(path.read_text(encoding="utf-8"))
    by_slug = {t.get("slug"): t for t in tools}
    out = []
    for slug, evidence in resolved.items():
        tool = by_slug.get(slug)
        if tool is None:
            out.append(f"tool_licenses {slug!r}: no such tool in tools_index")
            continue
        if evidence.get("license_tier") == TIER_UNKNOWN:
            # A reviewed entry that only records what the name denotes.
            if tool.get("license_tier") != TIER_UNKNOWN and \
                    tool.get("license_detection") != DETECTION_VENDOR_PRODUCT:
                out.append(f"tools_index {slug!r}: tiered, but its resolution is unknown")
            continue
        if tool.get("license") != evidence.get("license"):
            out.append(
                f"tools_index {slug!r}: licence {tool.get('license')!r} does not match "
                f"the resolved {evidence.get('license')!r}; re-run enrich_tools_index"
            )
        if evidence.get("license_tier") and tool.get("license_tier") != evidence["license_tier"]:
            out.append(
                f"tools_index {slug!r}: tier {tool.get('license_tier')!r} does not match "
                f"the resolved {evidence['license_tier']!r}; re-run enrich_tools_index"
            )
        if evidence.get("license_evidence") and \
                tool.get("license_evidence") != evidence["license_evidence"]:
            out.append(
                f"tools_index {slug!r}: license_evidence {tool.get('license_evidence')!r} "
                f"does not match the resolved {evidence['license_evidence']!r}"
            )
    # A vendor product is tiered from the entry-kind vocabulary, not from a licence
    # lookup, so it is legitimately absent from the resolution.
    unbacked = [t.get("slug") for t in tools
                if t.get("license_tier") != TIER_UNKNOWN and t.get("slug") not in resolved
                and t.get("license_detection") != DETECTION_VENDOR_PRODUCT]
    for slug in unbacked:
        out.append(f"tools_index {slug!r}: tiered but absent from tool_licenses.json")
    return out


def licence_counts(collection_dir) -> dict:
    """``{tools, resolved, vendor_product, unknown, tool_licenses}`` for the gate's line."""
    d = pathlib.Path(collection_dir)
    tools = json.loads((d / "tools_index.json").read_text(encoding="utf-8"))
    vendor = sum(1 for t in tools if t.get("license_detection") == DETECTION_VENDOR_PRODUCT)
    unknown = sum(1 for t in tools if t.get("license_tier") in (TIER_UNKNOWN, None))
    return {"tools": len(tools), "resolved": len(tools) - vendor - unknown,
            "vendor_product": vendor, "unknown": unknown,
            "tool_licenses": (d / "tool_licenses.json").is_file()}


def _counts_line(collection_dir) -> str:
    try:
        c = licence_counts(collection_dir)
    except (OSError, ValueError):
        return ""
    note = "" if c["tool_licenses"] else ", no tool_licenses.json: licence resolution not run"
    return (f" (tool licences: {c['resolved']} resolved, {c['vendor_product']} vendor products, "
            f"{c['unknown']} unknown of {c['tools']}{note})")


def check_collection(collection_dir) -> list[str]:
    d = pathlib.Path(collection_dir)
    violations: list[str] = []

    tools = json.loads((d / "tools_index.json").read_text(encoding="utf-8"))
    skills = json.loads((d / "skills_index.json").read_text(encoding="utf-8"))

    tool_slugs = {t.get("slug") for t in tools}
    skill_slugs = {s.get("slug") for s in skills}
    tier_by_slug = {t.get("slug"): t.get("license_tier") for t in tools}
    row_by_slug = {t.get("slug"): t for t in tools}

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
            # The same fields in both places, once the yaml carries them.
            for key in ("license", "license_evidence"):
                if key in rec and rec.get(key) != row_by_slug[slug].get(key):
                    violations.append(
                        f"tools/{slug}.yaml: {key} {rec.get(key)!r} != "
                        f"tools_index {row_by_slug[slug].get(key)!r}"
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
    if argv in (["-h"], ["--help"]):
        print(USAGE)
        print("Check tool and skill indexes for licence and reference consistency.")
        return 0
    if not argv:
        print(USAGE, file=sys.stderr)
        return 2
    failed = False
    for col in argv:
        v = check_collection(col)
        if v:
            failed = True
            print(f"FAIL {recorded_path(col)}{_counts_line(col)}:")
            for x in v:
                print(f"  - {x}")
        else:
            print(f"OK   {recorded_path(col)}{_counts_line(col)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
