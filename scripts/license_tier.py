"""Consumer license-tier classification for ASB skills.

A skill's prose is the collection's own work (CC-BY-4.0). This module classifies
the *underlying tool/source* license into a consumer-facing tier so users know what
they may do with the tool. See governance/LICENSE_TIERS.md.
"""
from __future__ import annotations

import pathlib
import yaml

_DEFAULT_MAP = pathlib.Path(__file__).resolve().parent.parent / "governance" / "license_tiers.yaml"

# What a detector reports when it could not establish a licence. Shared, because
# two scripts write the same fields from different evidence -- a repository and a
# DOI registry -- and each must be able to tell "unasked" from "answered". A
# failed lookup must never overwrite a successful one.
UNESTABLISHED_DETECTIONS = frozenset({None, "", "none", "file-present-unclassified"})

# --------------------------------------------------------------------------- #
# Which licence a recorded value is about.                                     #
#                                                                              #
# `access.license` is written by two resolvers with different evidence: one    #
# reads a code repository, the other a DOI registry. The value alone does not  #
# say which -- `MIT` could be the tool's licence and `CC-BY-4.0` the paper's,  #
# and a corpus can hold both. Without the distinction a repository lookup can  #
# substitute a tool licence for a paper one and no guard fires, because a      #
# value is still present. See governance/LICENSE_TIERS.md and issue #35.       #
# --------------------------------------------------------------------------- #

SUBJECT_TOOL = "tool"
SUBJECT_PAPER = "paper"

# Detections that read a code repository, and so describe the *tool*.
TOOL_DETECTIONS = frozenset({"github-api", "license-file", "r-description", "readme-llm"})
# `verified_via` markers that identify the subject when the detection cannot:
# a clone reads the repository, Unpaywall reads the publication.
TOOL_VERIFICATIONS = frozenset({"git_clone_succeeded_at_build"})
PAPER_VERIFICATION_PREFIX = "unpaywall"


def licence_subject(entry: dict) -> str | None:
    """Whether a corpus entry's recorded licence is the tool's or the paper's.

    Derived, never guessed: from `license_detection` where it says, and from
    `access.verified_via` where it does not. Returns None when the entry records
    no licence, or when nothing in it identifies the subject -- an explicit
    "unknown" rather than a default, so a new detection source shows up as
    unlabelled instead of being silently filed under one axis.
    """
    access = entry.get("access") or {}
    if entry.get("license_subject") in (SUBJECT_TOOL, SUBJECT_PAPER):
        return entry["license_subject"]
    if not access.get("license"):
        return None
    detection = entry.get("license_detection")
    if detection in TOOL_DETECTIONS:
        return SUBJECT_TOOL
    if str(detection or "").endswith("-paper"):
        return SUBJECT_PAPER
    verified = str(access.get("verified_via") or "")
    if verified in TOOL_VERIFICATIONS:
        return SUBJECT_TOOL
    if verified.startswith(PAPER_VERIFICATION_PREFIX):
        return SUBJECT_PAPER
    return None


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
