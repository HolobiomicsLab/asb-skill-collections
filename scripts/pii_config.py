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
    "version": "2026-09-19.2",
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
    # Bounded last-label set used to keep R slot syntax distinct from email
    # domains.  Only the final label is checked, so multi-label public endings
    # such as ``ac.uk`` and ``edu.au`` remain email-like.  Any two-letter last
    # label is email-like as well (every country-code top-level domain has two
    # letters), so this list only needs the generic top-level domains.
    "email_public_suffix_last_labels": [
        "ai", "app", "au", "bio", "biz", "ca", "ch", "cn", "com", "de", "dev",
        "edu", "email", "es", "eu", "fr", "gov", "health", "info", "int", "io",
        "it", "jp", "mil", "net", "nl", "online", "org", "pro", "science", "se",
        "site", "tech", "uk", "xyz",
    ],
    # Reserved DNS suffixes are deliberately email-like in examples and tests;
    # they must still be redacted rather than mistaken for R slot notation.
    "email_reserved_suffix_last_labels": [
        "example", "invalid", "localhost", "test",
    ],
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


def _is_git_ssh_clone(
    email: str, local: str, match: re.Match[str] | None
) -> bool:
    return bool(
        local == "git"
        and match is not None
        and match.group(0) == email
        and match.string[match.end():match.end() + 1] == ":"
    )


def _is_r_slot_access(local: str, domain: str) -> bool:
    if "." not in domain:
        return False
    if not local or not (local[-1].isalnum() or local[-1] in "._"):
        return False
    last_label = domain.rsplit(".", 1)[-1].lower()
    if len(last_label) == 2 and last_label.isalpha():
        return False
    email_like_labels = set(PII_CONFIG["email_public_suffix_last_labels"])
    email_like_labels.update(PII_CONFIG["email_reserved_suffix_last_labels"])
    return last_label not in email_like_labels


def _is_notation_not_email(
    em: str, match: re.Match[str] | None = None
) -> bool:
    """True when an email-shaped token belongs to a documented notation class.

    Guards against domain-notation false positives such as Spec2Vec / MS2DeepScore
    ``peak@<m/z>`` / ``loss@<m/z>`` word tokens (the 2-decimal m/z placeholder
    ``xxx.xx`` parses as a ``domain.tld``).  Two context classes are also benign:
    ``git_ssh_clone`` requires the exact ``git`` local part and a colon immediately
    after the match; ``r_slot_access`` requires an identifier character immediately
    before ``@`` and a domain last label that is neither two letters (a country
    code) nor in the bounded generic public-suffix set.

    ``match`` is optional for backward compatibility.  Context-aware callers pass
    the exact ``re.finditer`` match so its full source string and end offset are
    available; without it, the SSH-only exception fails closed.
    """
    local, _, domain = em.partition("@")
    if local.lower() in {t.lower() for t in PII_CONFIG["email_notation_localparts"]}:
        return True
    if re.fullmatch(PII_CONFIG["email_placeholder_domain_regex"], domain):
        return True
    if _is_git_ssh_clone(em, local, match):
        return True
    return _is_r_slot_access(local, domain)
