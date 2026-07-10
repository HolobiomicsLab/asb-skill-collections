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
    """Load the SPDX-to-tier governance map (governance/license_tiers.yaml)."""
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

    # Normalize by stripping -only / -or-later suffixes to match legacy SPDX ids
    def _norm(s):
        s = s.lower()
        for suf in ("-or-later", "-only"):
            if s.endswith(suf):
                s = s[: -len(suf)]
        return s

    nk = _norm(key)
    for spdx_id, tier in (m.get("spdx") or {}).items():
        if _norm(spdx_id) == nk:
            return tier

    low = key.lower()
    for kw in (m.get("fallback") or {}).get("noncommercial_keywords", []):
        if kw.lower() in low:
            return "noncommercial"
    return (m.get("fallback") or {}).get("default", "restricted")


def ack_required(tier: str) -> bool:
    """Only the noncommercial tier triggers a blocking runtime use acknowledgment.
    'restricted' is labeled + link-only with a soft note, but does not block."""
    return tier == "noncommercial"


def source_reuse_for_license(spdx: str, _map: dict | None = None) -> str | None:
    """What may we do with a SOURCE's text under this licence?

    Returns 'full', 'limited', 'none', or None when the licence is not in the
    canonical table. None means UNKNOWN and must block admission -- it is never
    the same as 'none', which is a known refusal. See governance/license_tiers.yaml.
    """
    if not spdx or not spdx.strip():
        return None
    table = (_map or load_map()).get("source_reuse") or {}
    key = spdx.strip().lower()
    for known, reuse in table.items():
        if known.lower() == key:
            return reuse
    return None


def permits_full_reuse(spdx: str, _map: dict | None = None) -> bool:
    """True only for licences that grant redistribution and derivation.

    An unknown licence is not full reuse, but callers must still distinguish the
    two: use source_reuse_for_license() when the difference matters.
    """
    return source_reuse_for_license(spdx, _map) == "full"
