#!/usr/bin/env python3
"""ASBB release gate — the runnable enforcement of CONTENT_POLICY.md §5/§6.

This is the checkpoint between the private Tier-2 intermediates and the public
Tier-3 artifacts (CONTENT_POLICY.md §5). It takes a single collection directory
(e.g. ``collections/metabolomics/v1``) plus the source-corpus metadata
(``corpus.yaml``), runs the v0-active content checks, and writes a structured
``gate_report.json`` with one ``pass|warn|fail`` verdict per check.

Checks implemented (mapped to the §5 checklist + §6 safety gates):

  1. ACCESS-TIER (OA)         — gate 2 / 15.  Every ``status:included`` paper's
                                ``access.type`` is in the OA allowed set
                                (reuses promote.py ``_OA_TIERS`` + the
                                verify-paper.yml normalization).  ``preprint`` is
                                a PROVENANCE value, NOT an OA tier, and is
                                rejected as an ``access.type``.  ``require_open_access``
                                is True for v0.
  2. STRIP-VERBATIM / SIMILARITY — gate 5 / 6.  Scans every public text field
                                (SKILL.md bodies, card text, evidence spans) for
                                verbatim source spans over the per-span cap
                                (substring/n-gram + a simple similarity ratio) and
                                applies the cumulative cap (reuses promote.py caps
                                + ``_EVIDENCE_VERBATIM_RE``).
  3. PII / DUAL-USE (two-tier) — §6.  HARD FAIL on high-confidence clinical /
                                personal identifiers + non-author emails inside
                                verbatim quote spans; WARN + route-to-human for
                                ambiguous matches.  Author / affiliation emails are
                                allowlisted.  Regex + keyword lists live in a
                                versioned config dict (mirrors
                                ``pii_patterns.json``).
  4. PROVENANCE              — gate 8.  Every skill carries a source DOI + a
                                license tag.

Enforcement modes (CONTENT_POLICY.md §7):
  * default (advisory, staged-collections PRs): WARNs and FAILs are reported but
    the process exits 0 — the curator reviews and may merge.
  * ``--strict`` (hard-block, promotion to collections/ + release tag): any FAIL
    causes exit code 1.  Hard gates (2,5,6,8,15) are never overridable (§8).

Dependencies: Python 3 stdlib + PyYAML.  numpy is optional and unused by the
default code path (a hook is provided for a future embedding-similarity pass).

Reuse: this script imports the canonical caps / tier sets / strip helper from
``agentic_science_builder.release.promote`` when that package is importable, and
falls back to vendored copies of the same constants (kept byte-for-byte in sync)
when it is not — so the gate runs both inside an ASB checkout and standalone in
CI on the asb-skill-collections repo.

Usage:
    python scripts/release_gate.py collections/metabolomics/v1 \
        [--corpus collections/metabolomics/v1/corpus.yaml] \
        [--strict] [--report gate_report.json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError:  # pragma: no cover - guidance for CI
    sys.stderr.write(
        "release_gate.py requires PyYAML.  Install it with `pip install pyyaml`.\n"
    )
    raise

# --------------------------------------------------------------------------- #
# Reuse the real promote.py logic.  We import the canonical constants /        #
# helpers from the AgenticScienceBuilder package when it is importable, and    #
# fall back to vendored copies (identical values) otherwise so the gate runs   #
# standalone in the asb-skill-collections CI where ASB is not installed.       #
# --------------------------------------------------------------------------- #
try:  # pragma: no cover - exercised only inside an ASB checkout
    from agentic_science_builder.release.promote import (  # type: ignore
        _CUMULATIVE_CAP,
        _EVIDENCE_VERBATIM_RE,
        _NON_OA_TIERS,
        _OA_TIERS,
        _PER_SPAN_CAP,
        _TEXT_FIELD_CAP,
    )

    _PROMOTE_SOURCE = "agentic_science_builder.release.promote"
except Exception:  # noqa: BLE001 - any import failure → vendored fallback
    # Vendored fallback — kept byte-for-byte in sync with promote.py.
    _OA_TIERS = {
        "open-access",
        "open_access",
        "oa",
        "gold-oa",
        "gold_oa",
        "green-oa",
        "diamond",
    }
    _NON_OA_TIERS = {"hybrid", "closed", "paywalled", "unknown"}
    _PER_SPAN_CAP = 150
    _CUMULATIVE_CAP = 1500
    _TEXT_FIELD_CAP = 300
    _EVIDENCE_VERBATIM_RE = re.compile(r'^(\s*-\s+\[[^\]]*\][^:]*?):\s*"[^"]*"\s*$')
    _PROMOTE_SOURCE = "vendored-fallback"


# --------------------------------------------------------------------------- #
# Versioned PII / dual-use config (mirrors                                     #
# src/agentic_science_builder/release/pii_patterns.json — CONTENT_POLICY.md    #
# §6.2).  Bump ``version`` whenever a pattern/keyword/allowlist changes; the   #
# gate report records the version used per CONTENT_POLICY.md §6.2.             #
# --------------------------------------------------------------------------- #
PII_CONFIG: dict[str, Any] = {
    "version": "2026-06-15.1",
    "source": "scripts/release_gate.py::PII_CONFIG (mirror of pii_patterns.json)",
    # Tier 1 — HARD FAIL when found inside a verbatim quote span.
    "hard_fail_patterns": {
        # Clinical / personal identifiers.
        "mrn": r"\bMRN[:\s#]*\d{5,12}\b",
        "medical_record": r"\bmedical\s+record\s+(?:no\.?|number|#)\s*[:#]?\s*\d{4,}\b",
        "nhs_number": r"\b\d{3}[\s-]?\d{3}[\s-]?\d{4}\b",  # NHS 10-digit format
        "hospital_id": r"\b(?:hospital|patient)\s+ID[:\s#]*\w*\d{3,}\b",
        "account_number": r"\baccount\s+(?:no\.?|number|#)\s*[:#]?\s*\d{6,}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        # Explicit named-patient health information.
        "named_patient_dx": (
            r"\bpatient\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b"  # "Patient John Doe"
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
        "placeholder_subject": r"\b(?:Subject|Patient|Participant)[_\s\-]?(?:[A-Z]\b|\d{1,3}\b)",
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


# --------------------------------------------------------------------------- #
# Similarity thresholds (CONTENT_POLICY.md §5.3).                              #
# --------------------------------------------------------------------------- #
_NGRAM_JACCARD_THRESHOLD = 0.30  # >0.30 3-gram Jaccard overlap → flag
_SIMILARITY_RATIO_THRESHOLD = 0.92  # SequenceMatcher ratio proxy for cosine
_GATE_REPORT_SCHEMA = "asbb-release-gate/1.0"


# --------------------------------------------------------------------------- #
# Result model.                                                               #
# --------------------------------------------------------------------------- #
PASS, WARN, FAIL = "pass", "warn", "fail"
_SEVERITY = {PASS: 0, WARN: 1, FAIL: 2}


@dataclass
class CheckResult:
    """One gate check's verdict + structured detail."""

    name: str
    status: str = PASS
    gates: list[int] = field(default_factory=list)  # CONTENT_POLICY.md gate ids
    hard_gate: bool = False  # never-overridable per §8.2
    summary: str = ""
    details: list[dict[str, Any]] = field(default_factory=list)

    def add(self, status: str, message: str, **extra: Any) -> None:
        """Record a finding and escalate this check's overall status."""
        entry = {"status": status, "message": message}
        entry.update(extra)
        self.details.append(entry)
        if _SEVERITY[status] > _SEVERITY[self.status]:
            self.status = status

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "gates": self.gates,
            "hard_gate": self.hard_gate,
            "summary": self.summary or self.name,
            "n_findings": len(self.details),
            "details": self.details,
        }


# --------------------------------------------------------------------------- #
# Helpers.                                                                     #
# --------------------------------------------------------------------------- #
def _normalize_access_type(raw: str) -> str:
    """Normalize an ``access.type`` token to a canonical OA tier.

    Mirrors the verify-paper.yml normalization step (CONTENT_POLICY.md §3 /
    §7.5): lowercase + strip, unify underscore → hyphen, and map the bare
    ``green`` → ``green-oa``.  This reconciles the policy OA set (which lists
    bare ``green``) with promote.py's ``_OA_TIERS`` (which lists only
    ``green-oa``): after normalization both resolve to ``green-oa``.
    """
    t = (raw or "").strip().lower()
    if not t:
        return t
    t = t.replace("_", "-")
    if t == "green":
        t = "green-oa"
    return t


# Canonical (post-normalization) view of the OA allowed set so membership is
# spelling-insensitive against promote.py's `_OA_TIERS`.
_NORMALIZED_OA_TIERS = {_normalize_access_type(t) for t in _OA_TIERS} | {"green-oa"}


def _read_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split a SKILL.md into (frontmatter_dict, body).  Fail-soft to ({}, text)."""
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\n(.*?)\n---\n?(.*)\Z", text, re.DOTALL)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
        if not isinstance(fm, dict):
            fm = {}
    except Exception:  # noqa: BLE001 - malformed frontmatter → empty dict
        fm = {}
    return fm, m.group(2)


def _ngram_set(text: str, n: int = 3) -> set[tuple[str, ...]]:
    tokens = re.findall(r"\w+", text.lower())
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)} if len(tokens) >= n else set()


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _similarity_ratio(a: str, b: str) -> float:
    """A cheap stdlib stand-in for the §5.3 embedding-cosine check.

    SequenceMatcher.ratio() is a character-level similarity in [0, 1].  It is
    NOT a semantic embedding cosine — CONTENT_POLICY.md §5.3 specifies
    ``text-embedding-3-small`` cosine ≥ 0.92 for the production gate — but it
    flags near-verbatim restatements without a network/model dependency.  A
    numpy/embedding upgrade can replace this function (see TODO).
    """
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _iter_skill_md(collection_dir: Path) -> Iterable[Path]:
    skills_dir = collection_dir / "skills"
    root = skills_dir if skills_dir.is_dir() else collection_dir
    yield from sorted(root.rglob("SKILL.md"))


def _collect_evidence_spans(fm: dict[str, Any], body: str) -> list[dict[str, Any]]:
    """Pull verbatim quote spans out of a skill's frontmatter + body.

    Spans come from two places:
      * structured ``evidence_spans`` / ``evidence`` lists in frontmatter
        (each ``{text|quote, doi, section}``), and
      * ``## Evidence`` body lines of the form ``- [section] paraphrase: "quote"``
        matched by promote.py's ``_EVIDENCE_VERBATIM_RE`` (the verbatim part is
        the double-quoted tail).
    """
    spans: list[dict[str, Any]] = []

    def _push(text: str, doi: str | None, section: str | None) -> None:
        text = (text or "").strip()
        if text:
            spans.append({"text": text, "doi": doi or "", "section": section or ""})

    for key in ("evidence_spans", "evidence"):
        for sp in fm.get(key) or []:
            if isinstance(sp, dict):
                _push(sp.get("text") or sp.get("quote") or "", sp.get("doi"), sp.get("section"))
            elif isinstance(sp, str):
                _push(sp, None, None)

    for line in body.splitlines():
        mv = _EVIDENCE_VERBATIM_RE.match(line)
        if mv:
            qm = re.search(r':\s*"([^"]*)"\s*$', line)
            if qm:
                _push(qm.group(1), None, None)
    return spans


def _skill_dois(fm: dict[str, Any]) -> list[str]:
    """All source DOIs a skill declares (provenance.source_papers + derived_from)."""
    dois: list[str] = []
    prov = fm.get("provenance") or {}
    for sp in prov.get("source_papers") or []:
        if isinstance(sp, dict) and sp.get("doi"):
            dois.append(str(sp["doi"]))
    for df in fm.get("derived_from") or []:
        doi = df.get("doi") if isinstance(df, dict) else df
        if doi:
            dois.append(str(doi))
    if fm.get("doi"):
        dois.append(str(fm["doi"]))
    # Stable-dedup.
    seen: set[str] = set()
    out: list[str] = []
    for d in dois:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def _skill_license(fm: dict[str, Any]) -> str | None:
    """A skill's license tag, checked in the common frontmatter locations."""
    for key in ("license", "license_spdx", "spdx", "rights"):
        v = fm.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    meta = fm.get("metadata") or {}
    for key in ("license", "license_spdx", "spdx"):
        v = meta.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


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


def _build_email_allowlist(collection_meta: dict[str, Any]) -> tuple[set[str], re.Pattern]:
    """Author/affiliation email allowlist (exact set + institutional-role regex)."""
    exact = {e.lower() for e in PII_CONFIG["email_allowlist_exact"]}
    email_re = re.compile(PII_CONFIG["email_regex"])

    def _harvest(node: Any) -> None:
        if isinstance(node, str):
            for m in email_re.findall(node):
                if _is_notation_not_email(m):
                    continue
                exact.add(m.lower())
        elif isinstance(node, dict):
            for v in node.values():
                _harvest(v)
        elif isinstance(node, list):
            for v in node:
                _harvest(v)

    # Author / corresponding-author / curator / contact emails are allowlisted.
    for key in ("corresponding_author", "authors", "curators", "contact", "maintainers"):
        _harvest(collection_meta.get(key))
    role_re = re.compile(PII_CONFIG["email_allowlist_role_regex"], re.IGNORECASE)
    return exact, role_re


def _access_tier_from_corpus(corpus: dict[str, Any]) -> dict[str, str]:
    """Map DOI → normalized access tier from a corpus.yaml dict."""
    out: dict[str, str] = {}
    for p in corpus.get("papers") or []:
        doi = (p or {}).get("doi") or ""
        tier = _normalize_access_type(((p or {}).get("access") or {}).get("type") or "")
        if doi:
            out[doi] = tier
    return out


# --------------------------------------------------------------------------- #
# Check 1 — ACCESS-TIER (OA).  Gates 2 / 15 (hard).                            #
# --------------------------------------------------------------------------- #
def check_access_tier(corpus: dict[str, Any], require_open_access: bool = True) -> CheckResult:
    res = CheckResult(
        name="access_tier_oa",
        gates=[2, 15],
        hard_gate=True,
        summary="Every included paper's access.type is in the OA allowed set (v0 OA-only).",
    )
    papers = corpus.get("papers") or []
    checked = 0
    for i, paper in enumerate(papers):
        if not isinstance(paper, dict):
            continue
        if paper.get("status") != "included":
            continue
        checked += 1
        doi = paper.get("doi") or f"[paper {i}]"
        raw = ((paper.get("access") or {}).get("type") or "").strip().lower()
        norm = _normalize_access_type(raw)
        if not norm or norm == "unknown":
            res.add(
                FAIL,
                f"{doi}: status=included but access.type is empty or 'unknown'.",
                doi=doi,
                access_type=raw,
            )
        elif norm == "preprint":
            res.add(
                FAIL,
                f"{doi}: access.type='preprint' is a PROVENANCE value, not an OA tier. "
                "Set a real OA tier (open-access / gold-oa / green-oa / diamond) and record "
                "'preprint' on the separate provenance axis (CONTENT_POLICY.md §3).",
                doi=doi,
                access_type=raw,
            )
        elif require_open_access and norm not in _NORMALIZED_OA_TIERS:
            res.add(
                FAIL,
                f"{doi}: access.type='{raw}' (normalized '{norm}') is not open-access. "
                f"v0 (require_open_access=true) permits only {sorted(_OA_TIERS)} "
                "(hyphen/underscore variants accepted; 'green'→'green-oa').",
                doi=doi,
                access_type=raw,
            )
    res.summary = f"{res.summary}  ({checked} included papers checked)"
    if checked == 0 and not res.details:
        res.add(WARN, "No papers with status=included found in corpus to validate.")
    return res


# --------------------------------------------------------------------------- #
# Check 2 — STRIP-VERBATIM / SIMILARITY.  Gates 5 / 6 (hard).                  #
# --------------------------------------------------------------------------- #
def check_strip_verbatim(
    collection_dir: Path, access_by_doi: dict[str, str]
) -> CheckResult:
    res = CheckResult(
        name="strip_verbatim_similarity",
        gates=[5, 6],
        hard_gate=True,
        summary=(
            "OA papers exempt from caps (unlimited verbatim w/ attribution; "
            f">{_TEXT_FIELD_CAP}-char spans → advisory WARN).  Non-OA: per-span text cap "
            f"{_TEXT_FIELD_CAP} chars, cumulative cap {_CUMULATIVE_CAP} chars/DOI.  "
            "Near-verbatim similarity flagged for all."
        ),
    )
    cumulative_by_doi: dict[str, int] = {}
    total_spans = 0

    def _is_non_oa(doi: str) -> bool:
        # Treat unknown / non-OA tiers (and any DOI absent from the corpus) as
        # the strict-cap regime; OA papers permit fuller verbatim with attribution.
        return access_by_doi.get(doi, "unknown") in _NON_OA_TIERS or doi not in access_by_doi

    for sk_md in _iter_skill_md(collection_dir):
        try:
            text = sk_md.read_text(encoding="utf-8")
        except OSError as exc:
            res.add(WARN, f"{sk_md}: unreadable ({exc}).", file=str(sk_md))
            continue
        fm, body = _read_frontmatter(text)
        rel = str(sk_md.relative_to(collection_dir))
        skill_dois = _skill_dois(fm) or [""]
        spans = _collect_evidence_spans(fm, body)
        for span in spans:
            total_spans += 1
            span_text = span["text"]
            span_len = len(span_text)
            doi = span["doi"] or skill_dois[0]

            if not _is_non_oa(doi):
                # OPEN_ACCESS_POLICY.md §4: OA papers (any _OA_TIERS literal) pass
                # through UNCHANGED — unlimited verbatim with attribution.  No
                # per-span or cumulative cap is enforced.  §3 guidance suggests
                # snippets ≤300 chars; exceeding it is an advisory WARN (curator
                # review), never a release-blocking FAIL.
                if span_len > _TEXT_FIELD_CAP:
                    res.add(
                        WARN,
                        f"{rel}: OA verbatim span ({span_len} chars) exceeds the "
                        f"{_TEXT_FIELD_CAP}-char snippet guidance for DOI '{doi}' "
                        "(OA = unlimited with attribution; advisory only).",
                        file=rel,
                        doi=doi,
                        span_len=span_len,
                        cap=_TEXT_FIELD_CAP,
                        span_preview=span_text[:80],
                    )
            else:
                # Non-OA (hybrid / closed / paywalled / unknown): hard caps.
                # Per-span text-field cap is 300 (OPEN_ACCESS_POLICY.md §4 table;
                # the 150-char _PER_SPAN_CAP applies to claim source_excerpts,
                # stripped by promote.py Pass 2 — not to evidence-span text).
                if span_len > _TEXT_FIELD_CAP:
                    res.add(
                        FAIL,
                        f"{rel}: non-OA verbatim span ({span_len} chars) exceeds per-span "
                        f"cap ({_TEXT_FIELD_CAP}) for DOI '{doi}'.",
                        file=rel,
                        doi=doi,
                        span_len=span_len,
                        cap=_TEXT_FIELD_CAP,
                        span_preview=span_text[:80],
                    )

                # Cumulative cap (per DOI) — non-OA only.
                running = cumulative_by_doi.get(doi, 0) + span_len
                cumulative_by_doi[doi] = running
                if running > _CUMULATIVE_CAP:
                    res.add(
                        FAIL,
                        f"{rel}: cumulative verbatim for non-OA DOI '{doi}' reached {running} "
                        f"chars (cap {_CUMULATIVE_CAP}).",
                        file=rel,
                        doi=doi,
                        cumulative=running,
                        cap=_CUMULATIVE_CAP,
                    )

            # Similarity vs the source paragraph (CONTENT_POLICY.md §5.3).  We
            # do not have the Tier-1 source paragraph at gate time, so we compare
            # the span against the surrounding skill body as a same-corpus proxy:
            # a span that is near-identical to a long body window is a verbatim
            # paste that escaped paraphrasing.  This is intentionally a WARN
            # (curator review) unless the per-span cap above already FAILed.
            if span_len >= 60:
                window = body
                ratio = _similarity_ratio(span_text, window) if window else 0.0
                jac = _jaccard(_ngram_set(span_text), _ngram_set(window))
                if jac > _NGRAM_JACCARD_THRESHOLD and ratio >= _SIMILARITY_RATIO_THRESHOLD:
                    res.add(
                        FAIL,
                        f"{rel}: span is near-verbatim (jaccard={jac:.2f}, ratio={ratio:.2f}) — "
                        "both §5.3 thresholds exceeded; rewrite required.",
                        file=rel,
                        doi=doi,
                        jaccard=round(jac, 3),
                        ratio=round(ratio, 3),
                    )
                elif jac > _NGRAM_JACCARD_THRESHOLD or ratio >= _SIMILARITY_RATIO_THRESHOLD:
                    res.add(
                        WARN,
                        f"{rel}: span similarity above one §5.3 threshold "
                        f"(jaccard={jac:.2f}, ratio={ratio:.2f}) — curator review.",
                        file=rel,
                        doi=doi,
                        jaccard=round(jac, 3),
                        ratio=round(ratio, 3),
                    )

    res.summary = f"{res.summary}  ({total_spans} verbatim spans scanned)"
    return res


# --------------------------------------------------------------------------- #
# Check 3 — PII / DUAL-USE (two-tier).  §6 (hard on Tier-1).                   #
# --------------------------------------------------------------------------- #
def check_pii_dual_use(
    collection_dir: Path, collection_meta: dict[str, Any]
) -> CheckResult:
    res = CheckResult(
        name="pii_dual_use",
        gates=[6],  # §6 content-safety gate (no numeric §5 row; tracked as gate 6 content-safety)
        hard_gate=True,
        summary=(
            "Two-tier PII / dual-use scan of verbatim quote spans "
            f"(pii_config={PII_CONFIG['version']})."
        ),
    )

    hard_patterns = {k: re.compile(v, re.IGNORECASE) for k, v in PII_CONFIG["hard_fail_patterns"].items()}
    warn_patterns = {k: re.compile(v, re.IGNORECASE) for k, v in PII_CONFIG["warn_patterns"].items()}
    email_re = re.compile(PII_CONFIG["email_regex"])
    instruction_re = re.compile(PII_CONFIG["dual_use_instruction_regex"], re.IGNORECASE)
    allow_exact, allow_role_re = _build_email_allowlist(collection_meta)

    n_spans = 0
    for sk_md in _iter_skill_md(collection_dir):
        try:
            text = sk_md.read_text(encoding="utf-8")
        except OSError:
            continue
        fm, body = _read_frontmatter(text)
        rel = str(sk_md.relative_to(collection_dir))
        for span in _collect_evidence_spans(fm, body):
            n_spans += 1
            span_text = span["text"]
            low = span_text.lower()

            # --- Tier 1: clinical / personal identifiers → HARD FAIL ----------
            for label, pat in hard_patterns.items():
                m = pat.search(span_text)
                if m:
                    res.add(
                        FAIL,
                        f"{rel}: clinical/personal identifier '{label}' in verbatim span.",
                        file=rel,
                        pattern=label,
                        match=m.group(0)[:60],
                    )

            # --- Emails: FAIL unless allowlisted ------------------------------
            for em in email_re.findall(span_text):
                eml = em.lower()
                # Skip scientific domain-notation false positives (e.g. Spec2Vec
                # 'peak@xxx.xx' / 'loss@xxx.xx' word tokens) — not real emails.
                if _is_notation_not_email(em):
                    continue
                if eml in allow_exact:
                    continue
                if allow_role_re.search(em):
                    res.add(
                        WARN,
                        f"{rel}: institutional-role email '{em}' in span "
                        "(not in allowlist; confirm + add).",
                        file=rel,
                        email=em,
                    )
                    continue
                res.add(
                    FAIL,
                    f"{rel}: non-author personal email '{em}' in verbatim span.",
                    file=rel,
                    email=em,
                )

            # --- Dual-use: active instruction → FAIL; keyword → WARN ----------
            if instruction_re.search(span_text):
                res.add(
                    FAIL,
                    f"{rel}: active dual-use instruction detected in span (DURC).",
                    file=rel,
                    span_preview=span_text[:80],
                )
            else:
                for kw in PII_CONFIG["dual_use_keywords"]:
                    if kw in low:
                        defensive = any(
                            ctx in low for ctx in PII_CONFIG["dual_use_defensive_context"]
                        )
                        res.add(
                            WARN,
                            f"{rel}: dual-use keyword '{kw}' in span "
                            f"({'defensive/neutral context' if defensive else 'review context'}) "
                            "— route to human.",
                            file=rel,
                            keyword=kw,
                            defensive=defensive,
                        )
                        break

            # --- Tier 2: suspected low-confidence PII → WARN ------------------
            for label, pat in warn_patterns.items():
                if pat.search(span_text):
                    res.add(
                        WARN,
                        f"{rel}: suspected low-confidence PII '{label}' in span — route to human.",
                        file=rel,
                        pattern=label,
                    )

    res.summary = f"{res.summary}  ({n_spans} spans scanned)"
    return res


# --------------------------------------------------------------------------- #
# Check 4 — PROVENANCE.  Gate 8 (hard).                                        #
# --------------------------------------------------------------------------- #
def check_provenance(collection_dir: Path) -> CheckResult:
    res = CheckResult(
        name="provenance_doi_license",
        gates=[8],
        hard_gate=True,
        summary="Every skill carries a source DOI + a license SPDX tag.",
    )
    n_skills = 0
    for sk_md in _iter_skill_md(collection_dir):
        n_skills += 1
        rel = str(sk_md.relative_to(collection_dir))
        try:
            fm, _ = _read_frontmatter(sk_md.read_text(encoding="utf-8"))
        except OSError as exc:
            res.add(FAIL, f"{rel}: unreadable ({exc}).", file=rel)
            continue
        dois = _skill_dois(fm)
        if not dois:
            res.add(
                FAIL,
                f"{rel}: no source DOI (provenance.source_papers / derived_from / doi).",
                file=rel,
            )
        lic = _skill_license(fm)
        if not lic:
            res.add(FAIL, f"{rel}: no license tag (license / license_spdx / metadata.license).", file=rel)
    res.summary = f"{res.summary}  ({n_skills} skills checked)"
    if n_skills == 0:
        res.add(WARN, "No SKILL.md files found in collection.")
    return res


# --------------------------------------------------------------------------- #
# Corpus / collection loaders.                                                #
# --------------------------------------------------------------------------- #
def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return data if isinstance(data, dict) else {}
    except (OSError, yaml.YAMLError):
        return {}


def _resolve_corpus(collection_dir: Path, explicit: Path | None) -> tuple[dict[str, Any], Path | None]:
    if explicit:
        return _load_yaml(explicit), explicit
    for cand in (collection_dir / "corpus.yaml", collection_dir.parent / "corpus.yaml"):
        if cand.is_file():
            return _load_yaml(cand), cand
    return {}, None


# --------------------------------------------------------------------------- #
# Driver.                                                                      #
# --------------------------------------------------------------------------- #
def run_gate(
    collection_dir: Path,
    corpus_path: Path | None,
    strict: bool,
) -> dict[str, Any]:
    corpus, resolved_corpus = _resolve_corpus(collection_dir, corpus_path)
    access_by_doi = _access_tier_from_corpus(corpus)

    collection_meta = _load_yaml(collection_dir / "collection.yaml")

    checks = [
        check_access_tier(corpus, require_open_access=True),
        check_strip_verbatim(collection_dir, access_by_doi),
        check_pii_dual_use(collection_dir, collection_meta),
        check_provenance(collection_dir),
    ]

    counts = {PASS: 0, WARN: 0, FAIL: 0}
    for c in checks:
        counts[c.status] += 1
    overall = FAIL if counts[FAIL] else (WARN if counts[WARN] else PASS)

    mode = "strict" if strict else "advisory"
    # Hard gates (2,5,6,8,15) are never overridable (§8.2); in strict mode any
    # FAIL on these blocks.  In advisory mode (staged PRs) everything is reported
    # but the process exits 0.
    blocking_fail = strict and counts[FAIL] > 0

    report: dict[str, Any] = {
        "schema": _GATE_REPORT_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "collection_dir": str(collection_dir),
        "corpus_path": str(resolved_corpus) if resolved_corpus else None,
        "mode": mode,
        "strict": strict,
        "promote_logic_source": _PROMOTE_SOURCE,
        "policy": {
            "oa_tiers": sorted(_NORMALIZED_OA_TIERS),
            "per_span_cap": _PER_SPAN_CAP,
            "cumulative_cap": _CUMULATIVE_CAP,
            "text_field_cap": _TEXT_FIELD_CAP,
            "ngram_jaccard_threshold": _NGRAM_JACCARD_THRESHOLD,
            "similarity_ratio_threshold": _SIMILARITY_RATIO_THRESHOLD,
            "pii_config_version": PII_CONFIG["version"],
            "require_open_access": True,
        },
        "overall_status": overall,
        "blocking": blocking_fail,
        "exit_code": 1 if blocking_fail else 0,
        "summary_counts": counts,
        "hard_gate_ids": [2, 5, 6, 8, 15],
        "checks": [c.to_dict() for c in checks],
    }
    return report


def _print_human_summary(report: dict[str, Any]) -> None:
    icon = {PASS: "PASS", WARN: "WARN", FAIL: "FAIL"}
    print(f"ASBB release gate — {report['mode']} mode")
    print(f"  collection : {report['collection_dir']}")
    print(f"  corpus     : {report['corpus_path']}")
    print(f"  reuse      : {report['promote_logic_source']}")
    print("  checks:")
    for c in report["checks"]:
        hard = " [hard-gate]" if c["hard_gate"] else ""
        print(f"    {icon[c['status']]:>4}  {c['name']} (gates {c['gates']}){hard} — {c['n_findings']} finding(s)")
        for d in c["details"]:
            print(f"            · [{icon[d['status']]}] {d['message']}")
    print(f"  overall    : {icon[report['overall_status']]}  (exit {report['exit_code']})")
    if report["blocking"]:
        print("  RESULT     : BLOCKED — strict mode + at least one FAIL on a hard gate.")
    elif report["overall_status"] == FAIL:
        print("  RESULT     : advisory — FAIL(s) reported, exit 0 (curator review).")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="release_gate.py",
        description=(
            "ASBB release gate — runs the CONTENT_POLICY.md §5/§6 content checks "
            "over a collection directory and writes gate_report.json."
        ),
    )
    parser.add_argument(
        "collection_dir",
        type=Path,
        help="Collection directory, e.g. collections/metabolomics/v1",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=None,
        help="Path to corpus.yaml (default: <collection_dir>/corpus.yaml or its parent).",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--strict",
        action="store_true",
        help="Hard-block: any FAIL exits 1 (promotion to collections/ + release tag).",
    )
    mode.add_argument(
        "--advisory",
        action="store_true",
        help="Advisory (default): report WARN/FAIL but exit 0 (staged-collections PRs).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Where to write gate_report.json (default: <collection_dir>/gate_report.json).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress the human-readable summary (still writes the JSON report).",
    )
    args = parser.parse_args(argv)

    collection_dir: Path = args.collection_dir
    if not collection_dir.is_dir():
        sys.stderr.write(f"error: collection_dir not found: {collection_dir}\n")
        return 2

    strict = bool(args.strict)  # --advisory and default both → strict=False
    report = run_gate(collection_dir, args.corpus, strict)

    report_path = args.report or (collection_dir / "gate_report.json")
    try:
        report_path.write_text(json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"error: could not write report to {report_path}: {exc}\n")
        return 2

    if not args.quiet:
        _print_human_summary(report)
        print(f"  report     : {report_path}")

    return int(report["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
