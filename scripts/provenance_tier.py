"""Provenance-tier kernel for ASB skills.

A skill's *provenance* records where its content came from, orthogonally to the
consumer `license_tier` (see scripts/license_tier.py). Three tiers:

- ``literature``  — synthesized from one or more source papers (requires >=1 doi).
- ``synthetic``   — derived from other skills (requires ``synthesized_from``).
- ``community``   — contributed/curated outside the literature pipeline (requires
  a ``related_skills`` key to be present, even if empty).

Pure logic: no data-file I/O. See governance/PROVENANCE_TIERS.md.
"""
from __future__ import annotations

VALID: set[str] = {"literature", "synthetic", "community"}
DEFAULT = "literature"


def validate_entry(
    tier,
    *,
    dois=None,
    synthesized_from=None,
    related_skills=None,
) -> list[str]:
    """Return human-readable violation strings (empty list = valid).

    - ``tier`` not in :data:`VALID` → one ``invalid provenance_tier`` violation
      (and no further checks).
    - ``literature`` with no ``dois`` → requires >=1 doi.
    - ``synthetic`` with no ``synthesized_from`` → requires synthesized_from.
    - ``community`` with ``related_skills is None`` → requires the key present.
      An empty list is allowed (``None`` means the key is absent).
    """
    if tier not in VALID:
        return [f"invalid provenance_tier {tier!r}"]
    if tier == "literature" and not dois:
        return ["literature requires >=1 doi"]
    if tier == "synthetic" and not synthesized_from:
        return ["synthetic requires synthesized_from"]
    if tier == "community" and related_skills is None:
        return ["community requires related_skills key"]
    return []
