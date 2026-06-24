"""Join corpus license_tier onto skills_index.json + kb_bundle.json (by DOI),
and build the metadata.tool_license block for non-open SKILL.md frontmatters.
"""
from __future__ import annotations

import json
import pathlib

import yaml

from scripts.license_tier import ack_required

_ORDER = {"open": 0, "noncommercial": 1, "restricted": 2}


def corpus_tier_by_doi(corpus_path) -> dict:
    doc = yaml.safe_load(pathlib.Path(corpus_path).read_text(encoding="utf-8"))
    out = {}
    for p in doc.get("papers", []):
        doi, tier = p.get("doi"), p.get("license_tier")
        if doi and tier:
            out[doi] = {"tier": tier, "license": (p.get("access") or {}).get("license"),
                        "repo_url": p.get("repo_url")}
    return out


def skill_tier(dois, tiers) -> str:
    """Most-restrictive tier across a skill's DOIs; 'open' when none are known."""
    found = [tiers[d]["tier"] for d in (dois or []) if d in tiers]
    return max(found, key=lambda t: _ORDER[t]) if found else "open"


def propagate_indices(skills_index_path, kb_bundle_path, tiers) -> dict:
    si_path, kb_path = pathlib.Path(skills_index_path), pathlib.Path(kb_bundle_path)
    si = json.loads(si_path.read_text(encoding="utf-8"))
    kb = json.loads(kb_path.read_text(encoding="utf-8"))
    summary: dict[str, int] = {}
    for entry in si:
        t = skill_tier(entry.get("dois"), tiers)
        entry["license_tier"] = t
        summary[t] = summary.get(t, 0) + 1
    for rec in (kb.get("skills") or {}).values():
        rec["license_tier"] = skill_tier(rec.get("dois"), tiers)
    si_path.write_text(json.dumps(si, indent=2, ensure_ascii=False), encoding="utf-8")
    kb_path.write_text(json.dumps(kb, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


def tool_license_block(tier, license, repo_url) -> dict:
    return {"tier": tier, "requires_ack": ack_required(tier),
            "ref": license or "unknown", "url": repo_url or ""}
