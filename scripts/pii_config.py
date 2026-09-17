"""Shared PII patterns for the release gate and outbound feedback helper."""

from __future__ import annotations

import re
from typing import Any

# --------------------------------------------------------------------------- #
# Versioned PII / dual-use config — this module IS the library that           #
# CONTENT_POLICY.md §6.2 names.  No ``pii_patterns.json`` exists, here or in  #
# the framework; §6.2's pointer to one was corrected 2026-09-13.  Bump        #
# ``version`` whenever a pattern/keyword/allowlist changes: the gate report   #
# records the version used and folds this dict into ``receipt_sha256``.       #
# --------------------------------------------------------------------------- #
PII_CONFIG: dict[str, Any] = {
    "version": "2026-09-13.1",
    "source": "scripts/pii_config.py::PII_CONFIG",
    # Tier 1 — HARD FAIL when found inside a verbatim quote span.
    "hard_fail_patterns": {
        # Clinical / personal identifiers.
        # `mrn` tolerates optional separators (`M.R.N 4820193`, `M R N …`) because the
        # abbreviation + a 5-12 digit run is specific — 0 false positives across ≥4
        # sciences (see test_pii_evasion_hardening / test_pii_crossdomain).
        "mrn": r"\bM[.\s]?R[.\s]?N\b[:\s#.]*\d{5,12}\b",
        "medical_record": r"\bmedical\s+record\s+(?:no\.?|number|#)\s*[:#]?\s*\d{4,}\b",
        "nhs_number": r"\b\d{3}[\s-]?\d{3}[\s-]?\d{4}\b",  # NHS 10-digit format
        "hospital_id": r"\b(?:hospital|patient)\s+ID[:\s#]*\w*\d{3,}\b",
        "account_number": r"\baccount\s+(?:no\.?|number|#)\s*[:#]?\s*\d{6,}\b",
        # `ssn` stays DASH-ONLY on purpose. A space-separated 3-2-4 run (`000 00 0000`)
        # is irreducibly ambiguous with scientific numeric IDs (electrode / station /
        # coordinate values), so tolerating spaces over-fires cross-domain — a
        # documented, accepted detection gap, NOT a regex to force. The dashed form is
        # a specific SSN convention. (test_pii_crossdomain pins this decision.)
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        # Explicit named-patient health information: "Patient John Doe".
        # The name parts are wrapped in (?-i:...) so they require REAL capitalisation
        # even though the gate compiles every pattern with IGNORECASE — otherwise
        # IGNORECASE makes [A-Z] match lowercase and this fires on ordinary clinical
        # prose ("patient cohort showed", "patient samples were"). See test_pii_crossdomain.
        "named_patient_dx": (
            r"\bpatient\s+(?-i:[A-Z][a-z]+\s+[A-Z][a-z]+)\b"
        ),
        "subject_id_phenotype": (
            r"\bsubject\s+(?:id\s+)?\d{3,}\s+(?:showed|presented|exhibited|had)\b"
        ),
    },
    # Email handling — a real email inside a quote is HARD FAIL unless the local
    # part / domain is on the author/affiliation allowlist (then it is allowed).
    "email_regex": r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
    # Domain-notation false positives — scientific token formats of the shape
    # ``<word>@<value>`` collide with the email regex (e.g. Spec2Vec / MS2DeepScore
    # encode peaks as ``peak@<m/z>`` and neutral losses as ``loss@<m/z>``; the
    # 2-decimal m/z placeholder ``xxx.xx`` then parses as a ``domain.tld``).  An
    # email match is treated as NOTATION (skipped, not PII) when EITHER:
    #   (a) its local-part is one of these mass-spec / cheminformatics tokens, OR
    #   (b) its domain is a placeholder made only of x/X and dots (never a real
    #       domain, e.g. ``xxx.xx``, ``xx``, ``x.x``).
    # Both conditions are individually sufficient (defense in depth) and neither
    # can mask a real personal/author email, whose local-part is a name and whose
    # domain resolves to a real TLD.
    "email_notation_localparts": [
        "peak", "loss", "frag", "fragment", "ion", "precursor", "product",
        "mz", "mass", "neutral", "adduct", "bin", "feature", "token", "word",
    ],
    "email_placeholder_domain_regex": r"^[xX]+(?:\.[xX]+)*$",
    # Author / corresponding-author / institutional-role emails are allowlisted
    # (CONTENT_POLICY.md §6 Tier-1 exception).  Populated per-run from the
    # collection frontmatter (corresponding_author / curators / contact) and
    # seeded with institutional role-address patterns.
    "email_allowlist_exact": [
        "louisfelix.nothias@gmail.com",
    ],
    # Role addresses at institutional domains → allowed (e.g. info@lab.ac.uk).
    "email_allowlist_role_regex": (
        r"\b(?:info|contact|admin|lab|group|office|corresponding)@"
        r"[A-Za-z0-9.\-]+\.(?:ac\.[a-z]{2}|edu|gov|org)\b"
    ),
    # Tier 1 — confirmed dual-use red-flag keywords (NIH/NSF DURC categories).
    # Presence alone is a WARN (defensive/neutral context is common in
    # literature); only the active-instruction patterns below escalate to FAIL.
    "dual_use_keywords": [
        "gain-of-function",
        "gain of function",
        "weaponize",
        "weaponization",
        "weaponizable",
        "pathogen enhancement",
        "enhance transmissibility",
        "enhanced transmissibility",
        "aerosolize",
        "select agent",
        "bioweapon",
        "organism enhancement",
    ],
    # Active-instruction dual-use → HARD FAIL (synthesis / how-to framing).
    "dual_use_instruction_regex": (
        r"\b(?:protocol|procedure|steps?|instructions?|method)\b[^.]{0,80}\b"
        r"(?:synthesi[sz]e|weaponi[sz]e|enhance\s+(?:virulence|transmissibility|lethality))\b"
    ),
    # Tier 2 — WARN-only suspected-PII signals (low confidence).
    "warn_patterns": {
        # The label letter is wrapped in (?-i:...) for the same reason as
        # ``named_patient_dx`` above: the gate compiles with IGNORECASE, so a bare
        # [A-Z] also matches lowercase and the trailing "s" of an ordinary plural
        # satisfies it ("number of participants", "patients were enrolled"). The
        # rule targets an enumerated individual (Subject 12, Patient_A), never a
        # headcount. Measured 2026-09-13 on collections/metabolomics/v2: 3 hits,
        # all three the same quoted phrase "weighting by number of participants".
        "placeholder_subject": r"\b(?:Subject|Patient|Participant)[_\s\-]?(?:(?-i:[A-Z])\b|\d{1,3}\b)",
        "initials_in_clinical": r"\bpatient\s+[A-Z]\.\s*[A-Z]\.",
    },
    # Words that put a dual-use keyword into a neutral / defensive frame → keep
    # the finding at WARN rather than escalating.
    "dual_use_defensive_context": [
        "risk factor",
        "mechanism",
        "transmission in",
        "infection",
        "surveillance",
        "detection",
        "diagnosis",
        "epidemiolog",
    ],
}


def _is_notation_not_email(em: str) -> bool:
    """True when an ``<x>@<y>`` token is scientific notation, not a real email.

    Guards against domain-notation false positives such as Spec2Vec / MS2DeepScore
    ``peak@<m/z>`` / ``loss@<m/z>`` word tokens (the 2-decimal m/z placeholder
    ``xxx.xx`` parses as a ``domain.tld``).  See ``PII_CONFIG`` notes.
    """
    local, _, domain = em.partition("@")
    if local.lower() in {t.lower() for t in PII_CONFIG["email_notation_localparts"]}:
        return True
    if re.fullmatch(PII_CONFIG["email_placeholder_domain_regex"], domain):
        return True
    return False
