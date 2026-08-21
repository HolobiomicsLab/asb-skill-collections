"""Join corpus license_tier onto skills_index.json + kb_bundle.json (by DOI),
and build the metadata.tool_license block for non-open SKILL.md frontmatters.
"""
from __future__ import annotations

import json
import pathlib

import yaml

from asb_skill_collections import layout
from scripts.license_tier import ack_required

_ORDER = {"open": 0, "noncommercial": 1, "restricted": 2}


def detect_indent(text: str, default: int = 2) -> int:
    """Infer the leading-space indent width from the first indented line."""
    for line in text.splitlines():
        stripped = line.lstrip(" ")
        if stripped and stripped != line:
            return len(line) - len(stripped)
    return default


def corpus_tier_by_doi(corpus_path) -> dict:
    doc = yaml.safe_load(pathlib.Path(corpus_path).read_text(encoding="utf-8"))
    out = {}
    for p in doc.get("papers", []):
        doi, tier = p.get("doi"), p.get("license_tier")
        if doi and tier:
            out[doi] = {"tier": tier, "license": (p.get("access") or {}).get("license"),
                        "repo_url": p.get("repo_url")}
    return out


# What a skill's tier is when nothing establishes it. `open` would be the most
# permissive answer to a question nobody answered, and `asb-metabolomics` tells
# agents to default discovery to open-tier skills -- so an unestablished tier
# advertised as open is how a noncommercial tool gets presented as free to use.
UNESTABLISHED_TIER = "restricted"


def declared_tiers(collection_dir) -> dict[str, str]:
    """Each skill's own `metadata.tool_license.tier`, keyed by slug.

    A skill grounded on a repository rather than a paper has no corpus DOI, so
    the DOI join can say nothing about it -- but the skill itself often knows,
    because the tool's licence was read when the skill was written.
    """
    out: dict[str, str] = {}
    for md in layout.iter_skill_md(collection_dir):
        try:
            text = md.read_text(encoding="utf-8")
            fm = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        except (OSError, IndexError, yaml.YAMLError):
            continue
        tier = ((fm.get("metadata") or {}).get("tool_license") or {}).get("tier")
        if tier in _ORDER:
            out[md.parent.name] = tier
    return out


def skill_tier(dois, tiers, declared=None) -> str:
    """Most-restrictive tier across a skill's DOIs.

    With no DOI-derived tier, fall back to the skill's own declared
    `tool_license.tier`, and failing that to :data:`UNESTABLISHED_TIER`. Never
    to `open`: "we did not establish this" and "this is freely usable" are
    different answers, and only one of them is safe to guess.
    """
    found = [tiers[d]["tier"] for d in (dois or []) if d in tiers]
    if found:
        return max(found, key=lambda t: _ORDER[t])
    return declared if declared in _ORDER else UNESTABLISHED_TIER


def propagate_indices(skills_index_path, kb_bundle_path, tiers, declared=None) -> dict:
    si_path, kb_path = pathlib.Path(skills_index_path), pathlib.Path(kb_bundle_path)
    si_raw = si_path.read_text(encoding="utf-8")
    kb_raw = kb_path.read_text(encoding="utf-8")
    si = json.loads(si_raw)
    kb = json.loads(kb_raw)
    si_indent = detect_indent(si_raw)
    kb_indent = detect_indent(kb_raw)
    summary: dict[str, int] = {}
    declared = declared or {}
    for entry in si:
        t = skill_tier(entry.get("dois"), tiers, declared.get(entry.get("slug")))
        entry["license_tier"] = t
        summary[t] = summary.get(t, 0) + 1
    for slug, rec in (kb.get("skills") or {}).items():
        rec["license_tier"] = skill_tier(rec.get("dois"), tiers, declared.get(slug))
    si_path.write_text(json.dumps(si, indent=si_indent, ensure_ascii=False), encoding="utf-8")
    kb_path.write_text(json.dumps(kb, indent=kb_indent, ensure_ascii=False), encoding="utf-8")
    return summary


def tool_license_block(tier, license, repo_url) -> dict:
    return {"tier": tier, "requires_ack": ack_required(tier),
            "ref": license or "unknown", "url": repo_url or ""}
