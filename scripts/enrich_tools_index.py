"""Enrich the tool catalog with consumer license fields + bidirectional
skill<->tool links.

Skill<->tool links are made by DOI intersection against the corpus. Licence fields
are NOT: a tool's licence must come from the tool, never from a paper that cites it
(issue #42, governance/LICENSE_TIERS.md).

Idempotent, key-order / indent preserving post-processor over committed artifacts
(the propagate_license_tiers.py / stamp_skill_license.py pattern). Reuses
detect_indent from propagate_license_tiers; does not fork the collector.

Writes back, in collection_dir:
- tools_index.json : + entry_kind, license_tier, license, license_detection,
                     license_subject, license_evidence, repo_url,
                     source_paper_repos, used_by_skills (- canonical_url)
- skills_index.json: + tools_used
- kb_bundle.json   : + tools_used on each skill record

`--licence-only` writes the licence fields, `entry_kind`, `repo_url`,
`source_paper_repos` and `license_evidence` into tools_index.json and nothing
else: `used_by_skills` is left as it is, and skills_index.json and kb_bundle.json
are not written. A licence release must not change what a search returns, and
the DOI-intersection links computed here differ from the name links the
collection was built with (on proteomics v1 they double the link count).
"""
from __future__ import annotations

import json
import pathlib

import yaml
# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))


from scripts.classify_tool_entries import KIND_VENDOR, classify_all
from scripts.license_tier import (DETECTION_VENDOR_PRODUCT, SUBJECT_TOOL, TIER_UNKNOWN,
                                  TOOL_DETECTIONS, UNESTABLISHED_DETECTIONS, load_map,
                                  tool_tier_from_evidence)
from scripts.propagate_license_tiers import detect_indent


def load_tool_evidence(collection_dir) -> dict:
    """``{slug: {license, license_detection}}`` resolved from each tool itself.

    Read from ``tool_licenses.json`` when a resolver has produced one; absent, every
    tool is unknown. Deliberately not derived from the corpus: see tool_license().
    """
    path = pathlib.Path(collection_dir) / "tool_licenses.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def tool_license(tool_evidence) -> tuple:
    """(tier, license, detection, subject, repo_url) from evidence about the tool.

    ``tool_evidence`` is a ``{license, license_detection, repo_url}`` mapping
    resolved from the tool's own repository or package metadata by
    ``resolve_tool_licenses.py``, or None when no such lookup has been done. No
    lookup, or a lookup whose detection is not a tool detection, yields the
    ``unknown`` tier with no licence and no repository recorded.

    ``repo_url`` is recorded so the claim can be disputed. Every licence in the
    catalogue was previously unauditable because no entry named the repository it
    came from, which is how a wrong one went unnoticed.

    This deliberately has no access to the corpus. Tiers used to be inherited from
    the papers that cite a tool, aggregated most-restrictively, which recorded CAMERA
    (GPL) as Apache-2.0 because a paper using CAMERA is Apache-2.0, and scikit-learn
    (BSD) as noncommercial because one preprint citing it is CC-BY-NC-ND. A citing
    paper's licence is evidence about the paper. See issue #42 and LICENSE_TIERS.md.
    """
    ev = tool_evidence or {}
    lic = ev.get("license")
    det = ev.get("license_detection")
    tier = _evidence_tier(ev)
    if tier == TIER_UNKNOWN:
        return (TIER_UNKNOWN, None, None, None, None)
    return (tier, lic, det, SUBJECT_TOOL, ev.get("repo_url") or None)


def _evidence_tier(ev) -> str:
    """The tier the resolver recorded, or one derived from the licence string.

    The resolver records the tier because some licences it reads have no single
    SPDX id: `GPL` as an R package declares it (every GPL version is open, and
    inventing a version is the error this avoids) or `GPL-2.0-only OR
    GPL-3.0-only`. Deriving those again from the string would fall back to
    `restricted`. A recorded tier counts only with a tool detection.
    """
    det = ev.get("license_detection")
    recorded = ev.get("license_tier")
    if recorded is not None:
        if det in UNESTABLISHED_DETECTIONS or det not in TOOL_DETECTIONS:
            return TIER_UNKNOWN
        if recorded not in set(load_map()["tiers"]):
            return TIER_UNKNOWN
        if recorded != TIER_UNKNOWN and not ev.get("license") and det != "reviewed-map":
            return TIER_UNKNOWN
        return recorded
    return tool_tier_from_evidence(ev.get("license"), det)


def source_paper_repos(tool_slug, tools_dir) -> list:
    """Repositories of the papers that cite this tool, from tools/<slug>.yaml.

    These are *not* the tool's own repository, and the distinction is the point.
    `tools_index.json` previously published one of them per tool under the key
    `canonical_url`, which named CAMERA's home as `LinShuhaiLAB/LipidIN` and Agilent
    MassHunter's as `PNNL-Comp-Mass-Spec/PNNL-PreProcessor`. Every one of those 700
    values was already a member of this list, so nothing is lost by naming it.
    """
    path = pathlib.Path(tools_dir) / f"{tool_slug}.yaml"
    if not path.is_file():
        return []
    rec = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return sorted({str(r) for r in (rec.get("source_repos") or []) if r})


def link_maps(skills_index, tools_index) -> tuple:
    """Bidirectional skill<->tool maps via DOI intersection.

    Returns (tools_used_by_skill_slug, used_by_skills_by_tool_slug); each value
    is a sorted list of slugs. Mutual inverses by construction.
    """
    tools_used: dict[str, list] = {}
    used_by: dict[str, list] = {t["slug"]: [] for t in tools_index}
    tool_dois = [(t["slug"], set(t.get("dois") or [])) for t in tools_index]
    for s in skills_index:
        s_dois = set(s.get("dois") or [])
        matched = sorted(slug for slug, t_dois in tool_dois if s_dois & t_dois)
        tools_used[s["slug"]] = matched
        for tslug in matched:
            used_by[tslug].append(s["slug"])
    for tslug in used_by:
        used_by[tslug] = sorted(used_by[tslug])
    return tools_used, used_by


def enrich(collection_dir, licence_only: bool = False) -> dict:
    d = pathlib.Path(collection_dir)
    ti_path = d / "tools_index.json"
    si_path = d / "skills_index.json"
    kb_path = d / "kb_bundle.json"

    ti_raw = ti_path.read_text(encoding="utf-8")
    si_raw = si_path.read_text(encoding="utf-8")
    kb_raw = kb_path.read_text(encoding="utf-8")
    tools = json.loads(ti_raw)
    skills = json.loads(si_raw)
    kb = json.loads(kb_raw)

    if not licence_only:
        tools_used, used_by = link_maps(skills, tools)
    kinds = classify_all(tools)
    # Tool-level licence evidence, keyed by slug. Empty until a resolver that reads
    # each tool's own repository is wired in (issue #43); every tool is `unknown`
    # until then, which is what the catalogue actually knows.
    tool_evidence = load_tool_evidence(d)

    tool_tiers: dict[str, int] = {}
    for t in tools:
        evidence = tool_evidence.get(t["slug"]) or {}
        tier, lic, det, subject, repo = tool_license(evidence)
        # A reviewer's entry_kind outranks the vocabulary classifier.
        kind = evidence.get("entry_kind") or kinds[t["slug"]]["kind"]
        if tier == TIER_UNKNOWN and kind == KIND_VENDOR:
            tier, det, subject = "restricted", DETECTION_VENDOR_PRODUCT, SUBJECT_TOOL
        t["entry_kind"] = kind
        t["license_tier"] = tier
        t["license"] = lic
        t["license_detection"] = det
        t["license_subject"] = subject
        # Where the licence was read: a registry page or a reviewed statement.
        t["license_evidence"] = (evidence.get("license_evidence") or None) \
            if subject == SUBJECT_TOOL and det != DETECTION_VENDOR_PRODUCT else None
        # The tool's own repository when resolved, else nothing: the repositories
        # of citing papers stay in source_paper_repos (decision K1).
        t["repo_url"] = repo
        t["source_paper_repos"] = source_paper_repos(t["slug"], d / "tools")
        # Named a tool's canonical home while holding a citing paper's repository.
        t.pop("canonical_url", None)
        if not licence_only:
            t["used_by_skills"] = used_by.get(t["slug"], [])
        tool_tiers[tier] = tool_tiers.get(tier, 0) + 1

    if licence_only:
        skills_linked = sum(1 for s in skills if s.get("tools_used"))
    else:
        skills_linked = 0
        for s in skills:
            used = tools_used.get(s["slug"], [])
            s["tools_used"] = used
            if used:
                skills_linked += 1
        for slug, rec in (kb.get("skills") or {}).items():
            rec["tools_used"] = tools_used.get(slug, [])

    ti_path.write_text(json.dumps(tools, indent=detect_indent(ti_raw), ensure_ascii=False), encoding="utf-8")
    if not licence_only:
        si_path.write_text(json.dumps(skills, indent=detect_indent(si_raw), ensure_ascii=False), encoding="utf-8")
        kb_path.write_text(json.dumps(kb, indent=detect_indent(kb_raw), ensure_ascii=False), encoding="utf-8")

    entry_kinds: dict[str, int] = {}
    for record in kinds.values():
        entry_kinds[record["kind"]] = entry_kinds.get(record["kind"], 0) + 1
    unresolved_software = sum(
        1 for t in tools
        if t["license_tier"] == TIER_UNKNOWN and t["entry_kind"] != KIND_VENDOR
        and kinds[t["slug"]]["kind"] == "software")
    return {"tools": len(tools), "skills_linked": skills_linked, "tool_tiers": tool_tiers,
            "entry_kinds": dict(sorted(entry_kinds.items())),
            "unresolved_software": unresolved_software}


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--collection", required=True,
                    help="collection dir with tools_index.json + skills_index.json + kb_bundle.json + tools/")
    ap.add_argument("--licence-only", action="store_true",
                    help="write licence fields, entry_kind, repo_url, source_paper_repos and "
                         "license_evidence only; leave the skill-tool links untouched")
    a = ap.parse_args(argv)
    res = enrich(a.collection, licence_only=a.licence_only)
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
