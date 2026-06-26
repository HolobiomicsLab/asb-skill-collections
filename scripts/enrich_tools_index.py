"""Enrich the tool catalog with consumer license fields + bidirectional
skill<->tool links, by DOI intersection against the corpus.

Idempotent, key-order / indent preserving post-processor over committed
artifacts (the propagate_license_tiers.py / stamp_skill_license.py pattern).
Reuses _ORDER, corpus license mapping, and detect_indent from
propagate_license_tiers; does not fork the collector or touch tools/<slug>.yaml.

Writes back, in collection_dir:
- tools_index.json : + license_tier, license, license_detection, used_by_skills
- skills_index.json: + tools_used
- kb_bundle.json   : + tools_used on each skill record
"""
from __future__ import annotations

import json
import pathlib

import yaml

from scripts.propagate_license_tiers import _ORDER, detect_indent


def corpus_by_doi(corpus_path) -> dict:
    """doi -> full paper dict, as shaped in corpus.yaml (papers list)."""
    doc = yaml.safe_load(pathlib.Path(corpus_path).read_text(encoding="utf-8"))
    out = {}
    for p in doc.get("papers", []):
        doi = p.get("doi")
        if doi:
            out[doi] = p
    return out


def tool_license(tool_dois, corpus_papers) -> tuple:
    """Most-restrictive (tier, license, detection) across a tool's matched corpus
    DOIs. Conservative default ("restricted", None, None) when nothing matches.

    license comes from access.license; detection from top-level license_detection
    (mirrors corpus_tier_by_doi / check_license_tiers conventions).
    """
    best = None  # (rank, tier, license, detection)
    for d in tool_dois or []:
        p = corpus_papers.get(d)
        if not p:
            continue
        tier = p.get("license_tier")
        if tier not in _ORDER:
            continue
        rank = _ORDER[tier]
        if best is None or rank > best[0]:
            lic = (p.get("access") or {}).get("license")
            det = p.get("license_detection")
            best = (rank, tier, lic, det)
    if best is None:
        return ("restricted", None, None)
    return (best[1], best[2], best[3])


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


def enrich(collection_dir) -> dict:
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

    papers = corpus_by_doi(d / "corpus.yaml")
    tools_used, used_by = link_maps(skills, tools)

    tool_tiers: dict[str, int] = {}
    for t in tools:
        tier, lic, det = tool_license(t.get("dois"), papers)
        t["license_tier"] = tier
        t["license"] = lic
        t["license_detection"] = det
        t["used_by_skills"] = used_by.get(t["slug"], [])
        tool_tiers[tier] = tool_tiers.get(tier, 0) + 1

    skills_linked = 0
    for s in skills:
        used = tools_used.get(s["slug"], [])
        s["tools_used"] = used
        if used:
            skills_linked += 1

    for slug, rec in (kb.get("skills") or {}).items():
        rec["tools_used"] = tools_used.get(slug, [])

    ti_path.write_text(json.dumps(tools, indent=detect_indent(ti_raw), ensure_ascii=False), encoding="utf-8")
    si_path.write_text(json.dumps(skills, indent=detect_indent(si_raw), ensure_ascii=False), encoding="utf-8")
    kb_path.write_text(json.dumps(kb, indent=detect_indent(kb_raw), ensure_ascii=False), encoding="utf-8")

    return {"tools": len(tools), "skills_linked": skills_linked, "tool_tiers": tool_tiers}


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--collection", required=True,
                    help="collection dir with tools_index.json + skills_index.json + kb_bundle.json + corpus.yaml")
    a = ap.parse_args(argv)
    res = enrich(a.collection)
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
