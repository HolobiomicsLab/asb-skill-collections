#!/usr/bin/env python3
# Generated report helper: edit scripts/skill_feedback.py (between its SHARED
# REPORT LOGIC markers) or scripts/pii_config.py, then run
# `python scripts/router_shape.py --sync-report-helper`. The CLI below the
# vendored blocks is maintained here. asb_skill_collections/report_issue.py is
# a byte-identical copy that `asbb report` runs.
"""Draft a report for the public ASB registry, redacted, without posting it.

Four routes, the same words wherever a skill is met:

  skill    this skill is wrong or could be better
  missing  a skill is missing: request it, or propose yours
  paper    a paper is not referenced: propose it
  fault    something technical failed: report it

The helper prints the title, labels, body, fingerprint and a prefilled
`issues/new` address on https://github.com/HolobiomicsLab/asb-skill-collections.
It never calls the network and never posts. Show the user the exact text and
file it only on an explicit yes. Redaction removes paths, credentials, email
addresses and clinical identifiers; it cannot recognise a sensitive sample
name, so the user is the last check. Standard library only.
"""
from __future__ import annotations

# BEGIN VENDORED PII CONFIG

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
    "version": "2026-10-29.1",
    "source": "scripts/pii_config.py::PII_CONFIG",
    # Tier 1 — HARD FAIL when found inside a verbatim quote span.
    "hard_fail_patterns": {
        # Clinical / personal identifiers.
        # `mrn` tolerates optional separators (`M.R.N 4820193`, `M R N …`) because the
        # abbreviation + a 5-12 digit run is specific — 0 false positives across ≥4
        # sciences (see test_pii_evasion_hardening / test_pii_crossdomain).
        "mrn": r"\bM[.\s]?R[.\s]?N\b[:\s#.]*\d{5,12}\b",
        "medical_record": r"\bmedical\s+record\s+(?:no\.?|number|#)\s*[:#]?\s*\d{4,}\b",
        # `nhs_number` is LABEL-BOUND like its clinical siblings. The bare 10-digit
        # form (`\d{3}[\s-]?\d{3}[\s-]?\d{4}`) fired on a Bloom-filter bit budget
        # (`-b 1000000000`, PAC README) and on two adjacent benchmark-table cells
        # (`223327 7644`, XTandem Parser) — measured 2026-09-20 on the transcriptomics
        # and proteomics candidates. A real NHS number in a quote arrives with its
        # label ("NHS number 943 476 5919", "NHS no. 9434765919", "NHS# …").
        "nhs_number": (
            r"\bNHS\s*(?:no\.?|number|num\.?|#|id)?\s*[:#]?\s*"
            r"\d{3}[\s-]?\d{3}[\s-]?\d{4}\b"
        ),
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
    # Exact-value allowlist for Tier-1 patterns, keyed by pattern label. A matched
    # string equal (case-insensitively) to a key is NOT a finding. Every entry is a
    # documented example value or an owner-read span, never a class of values —
    # the same shape as ``email_allowlist_exact``. Measured 2026-09-20, decided by
    # the owner 2026-10-29 (HUMAN_REVIEW_GATE.md, "Task 8 candidate gates").
    "hard_fail_allowlist_exact": {
        "ssn": {
            # The canonical placeholder SSNs (SSA "Woolworth" card 078-05-1120 and
            # the textbook 123-45-6789); the agentic-ai candidate quotes the latter
            # from a privacy-benchmark paper's own example record
            # (10.1109/access.2026.3704541).
            "123-45-6789": "documented example value (textbook placeholder)",
            "078-05-1120": "documented example value (SSA Woolworth card)",
        },
        "hospital_id": {
            # De-identified sample label of a cited public dataset, quoted in a
            # CC-BY paper (10.1093/bioinformatics/btad419, transcriptomics
            # candidate b5a519a80508). Owner decision 2026-10-29: keep the leaf.
            "patient id 11352": (
                "de-identified public-dataset sample label quoted in a CC-BY paper "
                "(DOI in the comment above); owner-read 2026-10-29"
            ),
        },
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
    # Placeholder LOCAL PARTS: a usage line such as ``-m your@mail-adress.com``
    # (Watchdog WMS README, measured 2026-09-20 on the epigenomics candidate) is a
    # template the reader fills in, not a person's address. The domain check above
    # cannot catch it (the domain is plausible), so the local part is checked
    # against the bounded set of documented template names. Compared whole and
    # case-insensitively. Generic words that real fixtures and real people use as
    # local parts (``name``, ``user``, ``email``, ``you``) are deliberately NOT in
    # the set (test_pii_context_exceptions treats ``name@lab.example.org`` as a
    # real address); ``user1`` or ``jane.doe`` stay e-mails as well.
    "email_placeholder_localparts": [
        "your", "yourname", "your.name", "your.email", "youremail", "username",
        "someone", "firstname.lastname", "first.last", "john.doe",
    ],
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


def _is_placeholder_email(local: str) -> bool:
    """True when the local part is one of the documented template names."""
    return local.lower() in {
        t.lower() for t in PII_CONFIG["email_placeholder_localparts"]
    }


def _hard_fail_allowlisted(label: str, matched: str) -> bool:
    """True when ``matched`` is an exact, documented allowlist value for ``label``.

    The allowlist holds example values and owner-read spans only
    (``hard_fail_allowlist_exact``); comparison is whole-string and
    case-insensitive, with surrounding whitespace ignored, so a different number
    or a longer identifier never inherits the exemption.
    """
    allowed = PII_CONFIG["hard_fail_allowlist_exact"].get(label, {})
    return matched.strip().lower() in {k.lower() for k in allowed}


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
    if _is_placeholder_email(local):
        return True
    if _is_git_ssh_clone(em, local, match):
        return True
    return _is_r_slot_access(local, domain)
# END VENDORED PII CONFIG
# BEGIN VENDORED REPORT LOGIC
# Everything between these markers is copied verbatim, with scripts/pii_config.py,
# into scripts/templates/report_issue.py, the standard-library helper a collection
# ships in bin/. Keep it standard library only. Regenerate the copies with
# `python scripts/router_shape.py --sync-report-helper`.
import hashlib
import re
import urllib.parse

# The public registry. The domain repositories are private, so every route lands
# here and a maintainer carries the report into the domain repository.
REGISTRY = "HolobiomicsLab/asb-skill-collections"
ISSUES_URL = f"https://github.com/{REGISTRY}/issues"

# The four routes, named in the same words wherever a skill is met.
ROUTES: dict[str, str] = {
    "skill": "this skill is wrong or could be better",
    "missing": "a skill is missing: request it, or propose yours",
    "paper": "a paper is not referenced: propose it",
    "fault": "something technical failed: report it",
}

# The issue template of each route, in the order of the issue chooser.
ROUTE_TEMPLATES: dict[str, str] = {
    "skill": "1-skill-feedback.md",
    "missing": "2-request-skill.md",
    "paper": "3-propose-paper.md",
    "fault": "4-technical-fault.md",
}

# What kind of friction this is. The kind decides where the report goes and what
# a maintainer can do with it, so it is a closed vocabulary, not free text. A
# technical fault of the framework is not a skill kind: it is route `fault`.
KINDS: dict[str, str] = {
    "defect": "an existing skill is wrong, stale, or does not work as written",
    "drift": "the underlying tool changed and the skill no longer matches it",
    "enhancement": "the skill works but could be better: a missing step, a better default, a clearer text",
    "efficiency": "the skill works but costs far more than it needs to",
    "gap": "no skill covers the task; a new one is warranted",
    "composition": "the leaves exist but nothing composes them; a workflow is warranted",
}

# The kinds of each skill route. `gap` and `composition` ask for new work.
ROUTE_KINDS: dict[str, tuple[str, ...]] = {
    "skill": ("defect", "drift", "enhancement", "efficiency"),
    "missing": ("gap", "composition"),
}
PROPOSE_KINDS = frozenset(ROUTE_KINDS["missing"])

# Kinds used before the vocabulary was unified (the site form and
# make_improvement_report.py), read as their current kind.
LEGACY_KINDS: dict[str, str] = {
    "correction": "defect",
    "bug": "defect",
    "tool-update": "drift",
    "new-skill": "gap",
    "other": "enhancement",
}

# The part of the framework a technical fault concerns (route `fault`).
FAULT_COMPONENTS: dict[str, str] = {
    "install": "installing a collection or the package",
    "plugin": "the plugin or its marketplace entry",
    "search": "the search script or the router",
    "cli": "the asbb command line",
    "mcp": "the MCP server",
    "site": "the web site",
    "gates": "the release gates and checks",
    "other": "anything else",
}

PAPER_TYPES = ("paper", "tool", "data resource")

# A prefilled address longer than this is not handed out: browsers and GitHub
# truncate long addresses, and a cut body is worse than a pasted one.
MAX_ADDRESS_LENGTH = 6000

# Redaction beyond the release gate's clinical set. These are the categories that
# leak from a *session transcript* rather than from published prose: the gate
# never sees a home directory or a bearer token, so its patterns do not cover
# them. Ordered longest-match-first where two could overlap.
OUTBOUND_PATTERNS: dict[str, str] = {
    "url_userinfo": r"\b[a-z][a-z0-9+.\-]*://[^/\s:@]+:[^/\s@]+@",
    "authorization_header": (
        # An HTTP auth header is two tokens: the scheme and the credential. A
        # single \S+ consumes only the scheme, so "Authorization: Bearer <tok>"
        # used to publish <tok> under a "redacted" label. Consume the scheme and
        # the credential that follows it, and keep the one-token form for the
        # assignment-shaped keys where a second token is ordinary prose.
        r"(?<![A-Za-z0-9])(?:authorization\s*[:=]\s*"
        r"(?:(?:bearer|basic|digest|token|apikey|api-key)\s+)?\S+"
        r"|(?:api[_-]?key|access[_-]?key|secret[_-]?key|"
        r"token|secret|password|passwd|pwd|key)\s*[:=]\s*\S+)"
    ),
    "credential": (
        r"\b(?:(?:sk|pk)-[A-Za-z0-9_\-]{10,}|"
        r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_\-]{10,}|"
        r"github_pat_[A-Za-z0-9_\-]{10,}|xox[baprs]-[A-Za-z0-9_\-]{10,}|"
        r"AKIA[0-9A-Z]{12,})\b"
    ),
    "posix_home": r"(?<![A-Za-z0-9_])/(?:Users|home)/[^\s\"'`]+",
    "windows_home": r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]+Users[\\/]+[^\s\"'`]+",
    "posix_path": r"(?<![A-Za-z0-9_:/])/(?!/)[^\s\"'`]+",
    "windows_path": r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]+[^\s\"'`]+",
}

REDACTED = "<redacted:{name}>"
REDACTED_PATH = REDACTED.format(name="absolute_path")
FINGERPRINT_LENGTH = 12

# Generic English function words, dropped before fingerprinting so that two
# people describing one problem in different words still collide. Deliberately
# domain-neutral: a metabolomics term dropped here would silently merge two
# unrelated reports, which is the worse error.
STOPWORDS = frozenset(
    "a an and are as at be but by for from has have how in into is it its no not "
    "of on or that the then there these this to was were when which with".split()
)


def _pii_patterns() -> dict[str, str]:
    """The release gate's clinical/personal set — one canonical source, not a copy."""
    patterns = dict(PII_CONFIG["hard_fail_patterns"])
    patterns["email"] = PII_CONFIG["email_regex"]
    return patterns


def _redact_pattern(text: str, name: str, pattern: str) -> tuple[str, int]:
    """Apply one pattern while preserving canonical non-email notation."""
    replacement_count = 0

    def replacement(match: re.Match) -> str:
        nonlocal replacement_count
        if name == "email" and _is_notation_not_email(match.group(0)):
            return match.group(0)
        replacement_count += 1
        return REDACTED.format(name=name)

    return re.sub(pattern, replacement, text, flags=re.IGNORECASE), replacement_count


def redact(text: str) -> tuple[str, list[str]]:
    """Return (redacted_text, categories_removed).

    Categories are reported so the calling skill can tell the user *what* was
    removed. Silence would leave them unable to judge whether the remainder is
    safe, which is the whole decision they are being asked to make.
    """
    removed: list[str] = []
    out = text or ""
    for name, pattern in {**OUTBOUND_PATTERNS, **_pii_patterns()}.items():
        out, n = _redact_pattern(out, name, pattern)
        if n:
            removed.append(name)
    return out, sorted(removed)


def _slash_path(value: str) -> str:
    """Return a lexical path form without reading the filesystem."""
    return (value or "").strip().replace("\\", "/")


def _is_absolute_path(value: str) -> bool:
    """Whether a string is an absolute or home-relative filesystem path."""
    path = _slash_path(value)
    return path.startswith(("/", "~/")) or bool(re.match(r"^[A-Za-z]:/", path))


def _collection_suffix(value: str) -> str | None:
    """Return the non-machine-specific suffix following a collections directory."""
    path = _slash_path(value)
    if path.startswith("collections/"):
        return path.removeprefix("collections/")
    marker = "/collections/"
    return path.split(marker, 1)[1] if marker in path else None


def _target_candidate(target: str, collection: str) -> str:
    """Keep an identifying collection suffix; replace unrelated absolute paths."""
    target_path = _slash_path(target)
    suffix = _collection_suffix(target_path)
    if suffix is not None:
        return suffix
    if not _is_absolute_path(target_path):
        return REDACTED_PATH if ".." in target_path.split("/") else target_path
    collection_path = _slash_path(collection).rstrip("/")
    if collection_path and target_path.startswith(collection_path + "/"):
        relative = target_path[len(collection_path) + 1 :]
        collection_id = _collection_suffix(collection_path)
        return "/".join(part for part in (collection_id, relative) if part)
    return REDACTED_PATH


def _collection_candidate(collection: str) -> str:
    """Keep a collection/version identifier without retaining its absolute prefix."""
    suffix = _collection_suffix(collection)
    if suffix is not None:
        return suffix
    return (
        REDACTED_PATH if _is_absolute_path(collection) else (collection or "").strip()
    )


def _path_redactions(raw: str, candidate: str) -> list[str]:
    """Describe machine-specific path material removed during normalisation."""
    if _slash_path(raw) == candidate:
        return []
    return ["absolute_path" if candidate == REDACTED_PATH else "path_prefix"]


def _has_separator_evasive_pii(value: str) -> str | None:
    """Find canonical PII shapes hidden behind identifier punctuation."""
    identifier_words = re.sub(r"[-_.]+", " ", value)
    for name, pattern in _pii_patterns().items():
        if re.search(pattern, identifier_words, flags=re.IGNORECASE):
            return name
    return None


def _redact_identifier(value: str) -> tuple[str, list[str]]:
    """Redact an identifier, including PII split by slug punctuation."""
    clean, removed = redact(value)
    evasive_category = _has_separator_evasive_pii(value)
    if evasive_category and evasive_category not in removed:
        return REDACTED.format(name=evasive_category), sorted(
            [*removed, evasive_category]
        )
    return clean, removed


def _redact_report_fields(values: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    """Apply the single outbound redaction boundary to every supplied field."""
    clean: dict[str, str] = {}
    removed: set[str] = set()
    for name, value in values.items():
        clean[name], categories = (
            _redact_identifier(value)
            if name in {"target", "collection"}
            else redact(value)
        )
        removed.update(categories)
    return clean, sorted(removed)


def _one_line(value: str) -> str:
    """Collapse a redacted value for a title or metadata line."""
    return " ".join((value or "").split())


def _fingerprint_redacted(kind: str, target: str, symptom: str) -> str:
    """Hash canonical text after reporter-specific material has been redacted."""
    symptom = re.sub(r"<redacted:[^>]+>", " ", symptom)
    target = re.sub(r"<redacted:[^>]+>", " ", target)
    words = re.sub(r"[^a-z0-9 ]+", " ", symptom.lower()).split()
    content = sorted(
        {word for word in words if len(word) > 2 and word not in STOPWORDS}
    )
    payload = "␟".join((kind, _one_line(target).lower(), " ".join(content)))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:FINGERPRINT_LENGTH]


def fingerprint(kind: str, target: str, symptom: str, collection: str = "") -> str:
    """A stable id for "this same friction", so reports can be merged.

    Keyed on the *kind*, the skill or capability it concerns, and the set of
    content words in the symptom — not on the reporter, the timestamp, or the
    surrounding prose, none of which two people hitting one problem would share.

    This catches close restatements, not arbitrary paraphrase: "the flag is
    wrong in the example" and "The example's flag is WRONG!" collide, but two
    genuinely different descriptions of one bug will not. The fingerprint is
    therefore a cheap merge, not a substitute for searching open issues — the
    calling skill must do both.
    """
    target_candidate = _target_candidate(target, collection)
    clean, _ = _redact_report_fields({"target": target_candidate, "symptom": symptom})
    return _fingerprint_redacted(kind, clean["target"], clean["symptom"])


def normalise_kind(kind: str) -> str:
    """Read a kind of the earlier vocabularies as its current kind."""
    value = (kind or "").strip().lower()
    return LEGACY_KINDS.get(value, value)


def labels_for(kind: str, drafted: bool = False) -> list[str]:
    """Labels a maintainer can filter on. `needs-triage` is always present.

    `propose` marks a report that asks for new work; `auto-report` marks one a
    form or a script drafted.
    """
    labels = ["usage-feedback", "needs-triage"]
    if normalise_kind(kind) in PROPOSE_KINDS:
        labels.append("propose")
    if drafted:
        labels.append("auto-report")
    return labels


def route_labels(route: str, kind: str = "", drafted: bool = True) -> list[str]:
    """The labels of one route, the same in the templates, scripts and site."""
    if route in ROUTE_KINDS:
        return labels_for(kind or ROUTE_KINDS[route][0], drafted)
    labels = {
        "paper": ["propose", "paper-intake", "needs-triage"],
        "fault": ["bug", "needs-triage"],
    }.get(route)
    if labels is None:
        raise ValueError(f"unknown route {route!r}; expected one of {sorted(ROUTES)}")
    return labels + (["auto-report"] if drafted else [])


def _route_of(kind: str) -> str:
    return "missing" if kind in PROPOSE_KINDS else "skill"


def _payload(route: str, title: str, labels: list[str], body: list[str],
             fid: str, stripped: list[str]) -> dict:
    """The one mapping a caller shows the user and then files unchanged."""
    payload = {
        "title": title,
        "labels": labels,
        "body": "\n".join(body).rstrip() + "\n",
    }
    return {
        **payload,
        "payload": payload,
        "preview": payload,
        "route": route,
        "template": ROUTE_TEMPLATES[route],
        "fingerprint": fid,
        "redacted": stripped,
    }


def _origin_lines(fields: dict, collection: str, release: str) -> list[str]:
    line = []
    if collection:
        line.append(f"**Collection:** `{_one_line(fields['collection'])}`")
    if release:
        line.append(f"**Release:** `{_one_line(fields['release'])}`")
    return ["  ·  ".join(line)] if line else []


def render_issue(
    kind: str,
    target: str,
    symptom: str,
    expected: str = "",
    context: str = "",
    collection: str = "",
    release: str = "",
) -> dict:
    """Render a skill report (routes `skill` and `missing`), everything redacted.

    Raises ValueError on an unknown `kind`: a report that cannot be routed is
    worse than no report, and silently relabelling it would hide the mistake.
    Kinds of the earlier vocabularies are read as their current kind.
    """
    kind = normalise_kind(kind)
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}; expected one of {sorted(KINDS)}")
    if not (target or "").strip() or not (symptom or "").strip():
        raise ValueError("a report needs both a target and a symptom")

    candidates = {
        "target": _target_candidate(target, collection),
        "symptom": symptom,
        "expected": expected,
        "context": context,
        "collection": _collection_candidate(collection),
        "release": release,
    }
    fields, stripped = _redact_report_fields(candidates)
    stripped = sorted(
        {
            *stripped,
            *_path_redactions(target, candidates["target"]),
            *_path_redactions(collection, candidates["collection"]),
        }
    )
    fid = _fingerprint_redacted(kind, fields["target"], fields["symptom"])
    route = _route_of(kind)
    happened, expectation = (
        ("What was tried", "What a skill should do")
        if route == "missing"
        else ("What happened", "What the skill led me to expect")
    )

    body = [
        f"**Route:** {ROUTES[route]}",
        f"**Kind:** `{kind}` ({KINDS[kind]})",
        f"**Target:** `{_one_line(fields['target'])}`",
        *_origin_lines(fields, collection, release),
        f"**Fingerprint:** `{fid}`  <!-- corroborate this issue rather than opening a new one -->",
        "",
        f"### {happened}",
        fields["symptom"].strip(),
    ]
    if fields["expected"].strip():
        body += ["", f"### {expectation}", fields["expected"].strip()]
    if fields["context"].strip():
        body += ["", "### Context", fields["context"].strip()]
    if stripped:
        body += ["", f"*Redacted before posting: {', '.join(stripped)}.*"]

    title = f"{kind}: {_one_line(fields['target'])}: {_one_line(fields['symptom'])[:80]}"
    return _payload(route, title, labels_for(kind, drafted=True), body, fid, stripped)


def render_fault(
    component: str,
    ran: str,
    happened: str,
    expected: str = "",
    versions: str = "",
    collection: str = "",
    release: str = "",
) -> dict:
    """Render a technical fault of the framework (route `fault`), redacted."""
    component = (component or "").strip().lower()
    if component not in FAULT_COMPONENTS:
        raise ValueError(
            f"unknown component {component!r}; expected one of {sorted(FAULT_COMPONENTS)}"
        )
    if not (ran or "").strip() or not (happened or "").strip():
        raise ValueError("a fault report needs what was run and what happened")
    candidates = {
        "ran": ran,
        "happened": happened,
        "expected": expected,
        "versions": versions,
        "collection": _collection_candidate(collection),
        "release": release,
    }
    fields, stripped = _redact_report_fields(candidates)
    stripped = sorted({*stripped, *_path_redactions(collection, candidates["collection"])})
    fid = _fingerprint_redacted("fault", component, fields["happened"])
    body = [
        f"**Route:** {ROUTES['fault']}",
        f"**Component:** `{component}` ({FAULT_COMPONENTS[component]})",
        *_origin_lines(fields, collection, release),
        f"**Fingerprint:** `{fid}`  <!-- corroborate this issue rather than opening a new one -->",
        "",
        "### What was run",
        fields["ran"].strip(),
        "",
        "### What happened",
        fields["happened"].strip(),
    ]
    if fields["expected"].strip():
        body += ["", "### What was expected", fields["expected"].strip()]
    if fields["versions"].strip():
        body += ["", "### Versions", fields["versions"].strip()]
    if stripped:
        body += ["", f"*Redacted before posting: {', '.join(stripped)}.*"]
    title = f"fault: {component}: {_one_line(fields['happened'])[:80]}"
    return _payload("fault", title, route_labels("fault"), body, fid, stripped)


def paper_body(fields: dict) -> str:
    """The body of a paper proposal, in the fields `scripts/intake_issue.py` reads.

    The site form (`docs-site/propose.js`) writes the same lines. Optional
    fields are left out when empty.
    """
    lines = [
        f"**What is it?** {_one_line(fields.get('what', ''))}",
        "",
        f"**Link:** {_one_line(fields.get('link', ''))}",
        "",
        f"**Type:** {_one_line(fields.get('type', ''))}",
        "",
        f"**Target collection:** {_one_line(fields.get('collection', ''))}",
        "",
        "**Why it matters (one or two sentences):**",
        (fields.get("why") or "").strip(),
    ]
    for label, key in (("Target version:", "version"), ("Open access?", "open_access"),
                       ("You:", "you"), ("Conflict of interest?", "coi")):
        value = _one_line(fields.get(key, ""))
        if value:
            lines += ["", f"**{label}** {value}"]
    return "\n".join(lines).rstrip() + "\n"


def render_paper(
    what: str,
    link: str,
    paper_type: str,
    collection: str,
    why: str,
    version: str = "",
    open_access: str = "",
    you: str = "",
    coi: str = "",
) -> dict:
    """Render a paper proposal (route `paper`) that the intake parser reads.

    `collection` is the domain of the target collection (`metabolomics`), or a
    collection label (`metabolomics/v3`) whose domain is kept.
    """
    paper_type = (paper_type or "").strip().lower()
    if paper_type not in PAPER_TYPES:
        raise ValueError(f"unknown type {paper_type!r}; expected one of {list(PAPER_TYPES)}")
    domain = _collection_candidate(collection).split("/", 1)[0].strip()
    if not all((value or "").strip() for value in (what, link, domain, why)):
        raise ValueError("a paper proposal needs what it is, a link, a target collection and why it matters")
    candidates = {"what": what, "link": link, "type": paper_type, "collection": domain,
                  "why": why, "version": version, "open_access": open_access,
                  "you": you, "coi": coi}
    fields, stripped = _redact_report_fields(candidates)
    body = paper_body(fields)
    if stripped:
        body += f"\n*Redacted before posting: {', '.join(stripped)}.*\n"
    fid = _fingerprint_redacted("paper", fields["collection"], fields["link"])
    title = f"Propose: {_one_line(fields['what'])[:100]}"
    return _payload("paper", title, route_labels("paper"), body.rstrip("\n").splitlines(),
                    fid, stripped)


def issue_address(report: dict, limit: int = MAX_ADDRESS_LENGTH) -> dict:
    """The prefilled `issues/new` address of a report, bounded in length.

    The route's template is named so that GitHub applies its labels even for a
    reporter who may not set labels. When the body would make the address too
    long, `address` is None: give the user `short_address` (title and template
    only) and the body to paste.
    """
    params = {"template": report["template"], "title": report["title"],
              "labels": ",".join(report["labels"])}
    short = f"{ISSUES_URL}/new?" + urllib.parse.urlencode(params)
    full = f"{ISSUES_URL}/new?" + urllib.parse.urlencode({**params, "body": report["body"]})
    return {"address": full if len(full) <= limit else None, "short_address": short,
            "limit": limit}


def corroboration(fid: str, symptom: str, context: str = "") -> str:
    """The comment that strengthens an existing issue instead of duplicating it."""
    fields, _ = _redact_report_fields(
        {"fingerprint": fid, "symptom": symptom, "context": context}
    )
    lines = [
        f"Hit this too (`{_one_line(fields['fingerprint'])}`).",
        "",
        fields["symptom"].strip(),
    ]
    if fields["context"].strip():
        lines += ["", fields["context"].strip()]
    return "\n".join(lines).rstrip() + "\n"
# END VENDORED REPORT LOGIC

# Wrapper imports follow the vendored blocks, including their future import.
import argparse  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

COLLECTION_ROOT = Path(__file__).resolve().parent.parent


def collection_identity(root: Path = COLLECTION_ROOT) -> dict[str, str]:
    """Collection label and release label of the unit this helper ships in.

    Read from `.claude-plugin/plugin.json` beside `bin/`; empty when the helper
    runs outside a collection (for example as `asbb report`).
    """
    try:
        meta = json.loads((root / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"collection": "", "release": ""}
    name = str(meta.get("name") or "").strip()
    version = str(meta.get("version") or "").strip()
    if not name:
        return {"collection": "", "release": ""}
    major = version.split(".", 1)[0]
    return {
        "collection": f"{name}/v{major}" if major.isdigit() else name,
        "release": f"{name}-v{version}" if version else "",
    }


def build_parser(prog: str | None = None) -> argparse.ArgumentParser:
    """One subcommand per route; `--help` on each lists its fields."""
    identity = collection_identity()
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Draft a redacted report for the public ASB registry. Nothing is posted.",
    )
    routes = parser.add_subparsers(dest="route", required=True, metavar="ROUTE")

    def route(name: str) -> argparse.ArgumentParser:
        sub = routes.add_parser(name, help=ROUTES[name], description=ROUTES[name])
        sub.add_argument("--collection", default=identity["collection"],
                         help="collection label, e.g. metabolomics/v3 (default: this collection)")
        sub.add_argument("--release", default=identity["release"],
                         help="release label, e.g. metabolomics-v3.0.2 (default: this collection)")
        sub.add_argument("--json", action="store_true", help="print the report as JSON")
        return sub

    skill = route("skill")
    skill.add_argument("--skill", required=True, help="the skill slug, as the search printed it")
    skill.add_argument("--kind", default="defect",
                       choices=[*ROUTE_KINDS["skill"], *sorted(k for k, v in LEGACY_KINDS.items()
                                                          if v in ROUTE_KINDS["skill"])])
    skill.add_argument("--symptom", required=True, help="what happened")
    skill.add_argument("--expected", default="", help="what the skill led you to expect")
    skill.add_argument("--context", default="", help="tool and version, OS; no paths or sample names")

    missing = route("missing")
    missing.add_argument("--task", required=True, help="the task no skill covers, in a few words")
    missing.add_argument("--kind", default="gap", choices=ROUTE_KINDS["missing"])
    missing.add_argument("--tried", required=True, help="the search run, or the skills composed by hand")
    missing.add_argument("--should", default="", help="what a skill should do; a method paper DOI if known")

    paper = route("paper")
    paper.add_argument("--what", required=True, help="paper title or tool name")
    paper.add_argument("--link", required=True, help="a DOI, repository or homepage")
    paper.add_argument("--type", default="paper", choices=PAPER_TYPES)
    paper.add_argument("--why", required=True, help="why it matters, one or two sentences")
    paper.add_argument("--version", default="", help="target version, e.g. next")
    paper.add_argument("--open-access", default="", help="yes, no or not sure")
    paper.add_argument("--you", default="", help="your handle or ORCID, if you want credit")
    paper.add_argument("--coi", default="", help="conflict of interest, if any")

    fault = route("fault")
    fault.add_argument("--component", required=True, choices=sorted(FAULT_COMPONENTS))
    fault.add_argument("--ran", required=True, help="the exact command, or the page and button")
    fault.add_argument("--happened", required=True, help="the error or output that matters")
    fault.add_argument("--expected", default="")
    fault.add_argument("--versions", default="", help="Python, OS, agent host and version")
    return parser


def render(args: argparse.Namespace) -> dict:
    """Render the chosen route with the shared report logic."""
    if args.route == "skill":
        return render_issue(args.kind, args.skill, args.symptom, args.expected,
                            args.context, args.collection, args.release)
    if args.route == "missing":
        return render_issue(args.kind, args.task, args.tried, args.should, "",
                            args.collection, args.release)
    if args.route == "paper":
        return render_paper(args.what, args.link, args.type, args.collection, args.why,
                            args.version, args.open_access, args.you, args.coi)
    return render_fault(args.component, args.ran, args.happened, args.expected,
                        args.versions, args.collection, args.release)


def text_report(report: dict, address: dict) -> str:
    """What the user is shown before deciding whether to post."""
    lines = [
        f"Route: {ROUTES[report['route']]}",
        f"Title: {report['title']}",
        f"Labels: {', '.join(report['labels'])}",
        f"Fingerprint: {report['fingerprint']} (search open issues for it first; "
        "if one matches, comment there instead)",
        "Redacted: " + (", ".join(report["redacted"]) or "nothing recognised"),
        "----- body -----",
        report["body"].rstrip("\n"),
        "----- end of body -----",
    ]
    if address["address"]:
        lines.append(f"Address: {address['address']}")
    else:
        lines += [f"The body is too long for an address (limit {address['limit']} characters).",
                  f"Address: {address['short_address']}",
                  "Open it and paste the body above."]
    lines += [
        f"With gh and the user's yes: gh issue create --repo {REGISTRY} "
        "--title <title> --body-file <file with the body> "
        + " ".join(f"--label {label}" for label in report["labels"]),
        "Show this text to the user and post only on an explicit yes. Redaction cannot "
        "recognise a sensitive sample name: the user is the last check.",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None, prog: str | None = None) -> int:
    """Print the report of one route; 2 on a report that cannot be routed."""
    args = build_parser(prog).parse_args(argv)
    try:
        report = render(args)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    address = issue_address(report)
    if args.json:
        print(json.dumps({**report["payload"], "route": report["route"],
                          "template": report["template"], "fingerprint": report["fingerprint"],
                          "redacted": report["redacted"], **address}, indent=2))
    else:
        print(text_report(report, address))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
