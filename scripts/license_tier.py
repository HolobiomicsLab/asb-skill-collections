"""Consumer license-tier classification for ASB skills.

A skill's prose is the collection's own work (CC-BY-4.0). This module classifies
the *underlying tool/source* license into a consumer-facing tier so users know what
they may do with the tool. See governance/LICENSE_TIERS.md.
"""
from __future__ import annotations

import pathlib
import yaml

_DEFAULT_MAP = pathlib.Path(__file__).resolve().parent.parent / "governance" / "license_tiers.yaml"


def load_map(path: pathlib.Path | None = None) -> dict:
    return yaml.safe_load((path or _DEFAULT_MAP).read_text(encoding="utf-8"))


def tier_for_license(name: str, _map: dict | None = None) -> str:
    """Map an SPDX id or license name to open|noncommercial|restricted."""
    m = _map or load_map()
    if not name or not name.strip():
        return "restricted"
    key = name.strip()
    for spdx_id, tier in (m.get("spdx") or {}).items():
        if spdx_id.lower() == key.lower():
            return tier
    low = key.lower()
    for kw in (m.get("fallback") or {}).get("noncommercial_keywords", []):
        if kw.lower() in low:
            return "noncommercial"
    return (m.get("fallback") or {}).get("default", "restricted")


def ack_required(tier: str) -> bool:
    """Non-open tiers require a runtime use acknowledgment."""
    return tier != "open"
