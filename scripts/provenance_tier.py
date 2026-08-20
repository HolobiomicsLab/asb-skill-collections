"""Provenance-tier kernel for ASB skills.

A skill's *provenance* records where its content came from, orthogonally to the
consumer `license_tier` (see scripts/license_tier.py). Three tiers:

- ``literature``  — synthesized from one or more source papers (requires >=1 doi).
- ``repository``  — taken from an open source repository that has no paper behind it
  (requires ``repo_url``). Distinct from ``community``: the content came from the
  tool's own code and documentation, not from a contributor's expertise.
- ``synthetic``   — derived from other skills (requires ``synthesized_from``).
- ``community``   — contributed/curated outside the literature pipeline (requires
  a ``related_skills`` key to be present, even if empty).

Pure logic: no data-file I/O. See governance/PROVENANCE_TIERS.md.
"""
from __future__ import annotations

VALID: set[str] = {"literature", "repository", "synthetic", "community"}
DEFAULT = "literature"
REPOSITORY = "repository"


def validate_entry(
    tier,
    *,
    dois=None,
    synthesized_from=None,
    related_skills=None,
    repo_url=None,
) -> list[str]:
    """Return human-readable violation strings (empty list = valid).

    - ``tier`` not in :data:`VALID` → one ``invalid provenance_tier`` violation
      (and no further checks).
    - ``literature`` with no ``dois`` → requires >=1 doi.
    - ``repository`` with no ``repo_url`` → requires repo_url.
    - ``synthetic`` with no ``synthesized_from`` → requires synthesized_from.
    - ``community`` with ``related_skills is None`` → requires the key present.
      An empty list is allowed (``None`` means the key is absent).
    """
    if tier not in VALID:
        return [f"invalid provenance_tier {tier!r}"]
    if tier == "literature" and not dois:
        return ["literature requires >=1 doi"]
    if tier == "repository" and not str(repo_url or "").strip():
        return ["repository requires repo_url"]
    if tier == "synthetic" and not synthesized_from:
        return ["synthetic requires synthesized_from"]
    if tier == "community" and related_skills is None:
        return ["community requires related_skills key"]
    return []
