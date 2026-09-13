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
  5. LAYOUT / PACKAGING      — gate 10.  Every promoted skill directory holds
                                ``SKILL.md`` and at most a pointer-form
                                ``skill_kb.json``; the sidecar stays inside a
                                per-skill and a collection-level byte budget
                                (both FAIL loudly, neither truncates); and
                                every ``collection.yaml`` reconciles its counts
                                and advertised members with the leaf/tool files
                                and any indexes the collection ships.

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
    python scripts/release_gate.py collections --catalogue-membership
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

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p
    import sys as _sys

    _sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from asb_skill_collections import layout
from scripts import unit_closure

try:
    import yaml
except ImportError:  # pragma: no cover - guidance for CI
    sys.stderr.write(
        "release_gate.py requires PyYAML.  Install it with `pip install pyyaml`.\n"
    )
    raise

from scripts.validate_workflows import validate_port_types

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


from scripts.pii_config import PII_CONFIG, _is_notation_not_email


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

# repo-oa: the paper-ACCESS axis only (CONTENT_POLICY.md §3) — "a public git
# repository cloned at build".  It asserts nothing about reuse rights; what a
# consumer may do with the tool rides on the separate `license_tier` axis (§4).
# Skills grounded on a repo-oa entry ground on the cloned REPOSITORY (code /
# README / docs), never on paper text — the repository-only grounding rule (§3).
# Because it is an access tier, admission REQUIRES evidence that a clone was
# possible: a non-empty `repo_url` (enforced under --strict below).
# `access.verified_via` is a constant stamp, not evidence — it reads
# `git_clone_succeeded_at_build` on entries that have no repo_url at all.
_REPO_OA_TIERS = {"repo-oa", "repo-permissive", "repo-copyleft"}

# link-only: the DOI resolves and is citable, but nothing was cloned and no
# reuse right is claimed (CONTENT_POLICY.md §3).  It is the honest tier for a
# source with no public repository -- a paywalled book, a journal placeholder,
# an archived deposit we did not bind to source.  Because it asserts no clone,
# it must NOT carry `access.verified_via`; the inverse of the repo-oa evidence
# rule is enforced below.  Skills grounded solely on link-only entries carry a
# weaker `grounding_tier`, they are not silently presented as repo-grounded.
_LINK_ONLY_TIERS = {"link-only"}
_NORMALIZED_OA_TIERS = _NORMALIZED_OA_TIERS | _REPO_OA_TIERS | _LINK_ONLY_TIERS

# ADMISSION and REUSE are different questions, and `link-only` answers them
# differently: a citable DOI is admissible (above), but the tier means no reuse
# right was established, so it takes the strict verbatim caps rather than the OA
# exemption.  `repo-oa` keeps the exemption because its spans come from a cloned,
# openly licensed repository (the repository-only grounding rule), not paper text.
# Where a link-only paper does declare an open licence, the fix is to record it —
# `scripts/resolve_paper_license.py` promotes such an entry to `open-access` on the
# registry's evidence — never to widen the exemption here.
# Kept separate from promote.py's `_NON_OA_TIERS`, which is vendored byte-for-byte.
_CAPPED_VERBATIM_TIERS = _NON_OA_TIERS | _LINK_ONLY_TIERS


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
    return (
        {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}
        if len(tokens) >= n
        else set()
    )


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
    # Covers both layouts (leaves/ + skills/, or skills/ alone) and skips
    # infrastructure skills in `_`-prefixed dirs, consistent with
    # collect_metabolomics_collection.py's `_`-skip: they are routing/entry
    # scaffolds, not paper-derived skills, so the provenance / verbatim gates
    # do not apply to them.
    return layout.iter_skill_md(collection_dir)


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
                _push(
                    sp.get("text") or sp.get("quote") or "",
                    sp.get("doi"),
                    sp.get("section"),
                )
            elif isinstance(sp, str):
                _push(sp, None, None)

    for line in body.splitlines():
        mv = _EVIDENCE_VERBATIM_RE.match(line)
        if mv:
            qm = re.search(r':\s*"([^"]*)"\s*$', line)
            if qm:
                _push(qm.group(1), None, None)
    return spans


def _skill_repo_url(fm: dict[str, Any]) -> str:
    """The repository a skill grounds on, if it declares one.

    Repository-only grounding (CONTENT_POLICY.md §3) makes a cloned repository
    a first-class provenance basis, not a lesser one: a skill describing a tool
    whose code is public is grounded on that code even when the tool has no
    method paper. Only a non-empty http(s) URL counts as evidence.
    """
    for source in (fm.get("metadata") or {}, fm):
        raw = str((source or {}).get("repo_url") or "").strip()
        if raw.startswith(("https://", "http://")):
            return raw
    return ""


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
    for key in (
        "corresponding_author",
        "authors",
        "curators",
        "contact",
        "maintainers",
    ):
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
def check_access_tier(
    corpus: dict[str, Any], require_open_access: bool = True
) -> CheckResult:
    res = CheckResult(
        name="access_tier_oa",
        gates=[2, 15],
        hard_gate=True,
        summary="Every included paper's access.type is in the OA allowed set (v0 OA-only).",
    )
    # A repo-* access tier claims a clone happened; only a non-empty repo_url is
    # evidence of that. FAIL surfaces the finding and blocks the strict (promotion)
    # path, while staged-collections PRs stay advisory (CONTENT_POLICY.md §3).
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
        stamp = ((paper.get("access") or {}).get("verified_via") or "").strip()
        if norm in _LINK_ONLY_TIERS and stamp:
            res.add(
                FAIL,
                f"{doi}: access.type='{raw}' claims no clone, but "
                f"access.verified_via='{stamp}' still asserts one. A link-only "
                "entry must carry no clone stamp (CONTENT_POLICY.md §3).",
                doi=doi,
                access_type=raw,
            )
        if norm in _REPO_OA_TIERS and not (paper.get("repo_url") or "").strip():
            res.add(
                FAIL,
                f"{doi}: access.type='{raw}' claims a repository was cloned at build, but "
                "repo_url is empty — no clone was possible, so the tier is unverified. "
                "access.verified_via is a constant stamp, not evidence (CONTENT_POLICY.md "
                "§3). Provide a repo_url or set status:needs-evidence.",
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
            f">{_TEXT_FIELD_CAP}-char spans → advisory WARN).  Non-OA and link-only "
            f"(no reuse right established): per-span text cap {_TEXT_FIELD_CAP} chars, "
            f"cumulative cap {_CUMULATIVE_CAP} chars/DOI.  "
            "Near-verbatim similarity flagged for all."
        ),
    )
    cumulative_by_doi: dict[str, int] = {}
    total_spans = 0

    def _is_non_oa(doi: str) -> bool:
        # Treat unknown / non-OA / link-only tiers (and any DOI absent from the
        # corpus) as the strict-cap regime; OA papers permit fuller verbatim with
        # attribution.  See _CAPPED_VERBATIM_TIERS for why link-only is in here.
        return (
            access_by_doi.get(doi, "unknown") in _CAPPED_VERBATIM_TIERS
            or doi not in access_by_doi
        )

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
                # OPEN_ACCESS_POLICY.md "Per-paper access tier rules" /
                # "Open-access": OA papers (any _OA_TIERS literal) pass
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
                # Per-span text-field cap is 300 (OPEN_ACCESS_POLICY.md
                # "Hybrid / quotation" rules and TL;DR table;
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
                if (
                    jac > _NGRAM_JACCARD_THRESHOLD
                    and ratio >= _SIMILARITY_RATIO_THRESHOLD
                ):
                    res.add(
                        FAIL,
                        f"{rel}: span is near-verbatim (jaccard={jac:.2f}, ratio={ratio:.2f}) — "
                        "both §5.3 thresholds exceeded; rewrite required.",
                        file=rel,
                        doi=doi,
                        jaccard=round(jac, 3),
                        ratio=round(ratio, 3),
                    )
                elif (
                    jac > _NGRAM_JACCARD_THRESHOLD
                    or ratio >= _SIMILARITY_RATIO_THRESHOLD
                ):
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
        gates=[
            6
        ],  # §6 content-safety gate (no numeric §5 row; tracked as gate 6 content-safety)
        hard_gate=True,
        summary=(
            "Two-tier PII / dual-use scan of verbatim quote spans "
            f"(pii_config={PII_CONFIG['version']})."
        ),
    )

    hard_patterns = {
        k: re.compile(v, re.IGNORECASE)
        for k, v in PII_CONFIG["hard_fail_patterns"].items()
    }
    warn_patterns = {
        k: re.compile(v, re.IGNORECASE) for k, v in PII_CONFIG["warn_patterns"].items()
    }
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
                            ctx in low
                            for ctx in PII_CONFIG["dual_use_defensive_context"]
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
        summary="Every skill carries provenance (source DOI or repository) + a license SPDX tag.",
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
        if not dois and not _skill_repo_url(fm):
            res.add(
                FAIL,
                f"{rel}: no provenance — needs a source DOI "
                "(provenance.source_papers / derived_from / doi) or, for a tool with "
                "no method paper, the repository it grounds on (metadata.repo_url).",
                file=rel,
            )
        lic = _skill_license(fm)
        if not lic:
            res.add(
                FAIL,
                f"{rel}: no license tag (license / license_spdx / metadata.license).",
                file=rel,
            )
    res.summary = f"{res.summary}  ({n_skills} skills checked)"
    if n_skills == 0:
        res.add(WARN, "No SKILL.md files found in collection.")
    return res


def check_workflows(collection_dir: Path) -> CheckResult:
    """Validate the composite workflow super-skill subtree (`workflows/<slug>/`).

    Each workflow's leaves must resolve in skills_index.json, the workflow.yaml DAG
    (after / inputs_from) must reference only earlier steps, every transferred port type
    must be declared by the producer's outputs and consumer's inputs, no leaf may appear
    in two stages, and tools must not leak script filenames. Declared workflow counts are
    compared with the on-disk layout. ``verification.final_outputs[].type`` is not
    compared with step outputs because those values are file kinds in a different
    vocabulary. Non-hard (advisory) — the leaf collection is the hard-gated artifact;
    workflows are an additive layer.
    """
    res = CheckResult(
        name="composite_workflows",
        gates=[],
        hard_gate=False,
        summary=(
            "Composite workflow super-skills resolve to real leaves with a valid typed DAG "
            "and matching layout count."
        ),
    )
    wf_root = collection_dir / "workflows"
    collection_meta = _load_yaml(collection_dir / "collection.yaml")
    has_declared_count = "workflows_count" in collection_meta
    workflow_dirs = [
        path
        for path in (sorted(wf_root.iterdir()) if wf_root.is_dir() else [])
        if path.is_dir() and not path.name.startswith("_") and path.name != "bin"
    ]
    n_workflows = len(workflow_dirs)
    if has_declared_count and collection_meta["workflows_count"] != n_workflows:
        res.add(
            WARN,
            "collection.yaml workflows_count mismatch: "
            f"declared {collection_meta['workflows_count']}, "
            f"on-disk workflow directories {n_workflows}",
            file="collection.yaml",
        )
    if not wf_root.is_dir():
        res.add(PASS, "No workflows/ subtree (n/a).")
        return res
    # Leaf slug resolution needs the leaf index. A staging subtree (workflows only) has no
    # skills_index.json — its leaves live in the released collection — so degrade to a loud
    # WARN and run the structural checks (DAG / collisions / tool leaks) rather than a false
    # FAIL. Full slug resolution: validate_workflows.py --collection <released>.
    idx: set | None = None
    idx_path = collection_dir / "skills_index.json"
    if idx_path.is_file():
        try:
            idx = {r["slug"] for r in json.loads(idx_path.read_text(encoding="utf-8"))}
        except ValueError as exc:
            res.add(FAIL, f"cannot parse skills_index.json: {exc}")
    else:
        res.add(WARN, "no skills_index.json in this subtree — leaf-slug resolution deferred "
                      "to validate_workflows.py --collection <released>; structural checks only.")
    for d in workflow_dirs:
        name = d.name
        sk_md, wf_y = d / "SKILL.md", d / "workflow.yaml"
        if not (sk_md.is_file() and wf_y.is_file()):
            res.add(FAIL, f"{name}: missing SKILL.md or workflow.yaml", file=name)
            continue
        try:
            fm, _ = _read_frontmatter(sk_md.read_text(encoding="utf-8"))
            wf = yaml.safe_load(wf_y.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as exc:
            res.add(FAIL, f"{name}: unreadable ({exc})", file=name)
            continue
        meta = fm.get("metadata", {}) or {}
        if meta.get("kind") != "composite-workflow":
            res.add(FAIL, f"{name}: metadata.kind != composite-workflow", file=name)
        steps = wf.get("steps") or []
        for message in validate_port_types(name, steps):
            res.add(FAIL, message, file=name)
        ids: set = set()
        seen: dict = {}
        for st in steps:
            sid = st.get("id")
            for s in st.get("skills") or []:
                if idx is not None and s not in idx:
                    res.add(FAIL, f"{name}/{sid}: unresolved skill {s}", file=name)
                if s in seen and seen[s] != sid:
                    res.add(
                        FAIL, f"{name}: collision {s} ({seen[s]} & {sid})", file=name
                    )
                seen[s] = sid
            for a in st.get("after") or []:
                if a not in ids:
                    res.add(FAIL, f"{name}/{sid}: dangling after -> {a}", file=name)
            for k in st.get("inputs_from") or {}:
                if k not in ids:
                    res.add(
                        FAIL, f"{name}/{sid}: dangling inputs_from -> {k}", file=name
                    )
            ids.add(sid)
        for t in meta.get("member_tools") or []:
            if str(t).endswith(".py"):
                res.add(WARN, f"{name}: script-filename as tool: {t}", file=name)
    res.summary = f"{res.summary}  ({n_workflows} workflows checked)"
    if n_workflows == 0:
        res.add(PASS, "workflows/ present but empty.")
    return res


# --------------------------------------------------------------------------- #
# Layout / packaging (gate 10).                                               #
# --------------------------------------------------------------------------- #
#: The only two files a promoted skill directory may hold.  ``SKILL.md`` is the
#: skill; ``skill_kb.json`` is the pointer-form knowledge-base sidecar written
#: by ``asb collection promote``.  Everything else — a ``docs/`` tree, a
#: ``README.md``, a stray ``tools.json`` — is a Tier-1/Tier-2 intermediate that
#: CONTENT_POLICY.md §5 keeps out of the public collection, so its presence is
#: a packaging failure rather than a matter of taste.
_KB_SIDECAR_FILENAME = "skill_kb.json"
_ALLOWED_SKILL_FILES = frozenset({"SKILL.md", _KB_SIDECAR_FILENAME})

#: Per-skill sidecar budget.  The promoter refuses to write a sidecar over this
#: size rather than truncating it, and the gate refuses to ship one: a
#: truncated pointer list is indistinguishable from a short one, which is
#: exactly the confusion the knowledge-base status enum exists to prevent.
_KB_SIDECAR_MAX_BYTES = 64 * 1024

#: Collection-level budget over every sidecar in the collection.  The largest
#: shipped collection holds 5,859 leaves; at the audited p99 sidecar size
#: (7,446 B) that totals roughly 43 MB, so 64 MiB leaves room to grow while
#: still refusing a collection whose sidecars have drifted an order of
#: magnitude past what was measured.
_COLLECTION_KB_MAX_BYTES = 64 * 1024 * 1024


def _index_slugs(
    index_path: Path, member_key: str = "skills"
) -> tuple[set[str], str | None]:
    """Slugs declared by an index, or an error string.

    Tolerates the two shapes the index has worn — a bare list of entries, and
    an object wrapping one under ``skills`` — and accepts plain strings as
    slugs.  An entry that declares no slug is drift, not a shape this reads
    around, so it is reported rather than skipped.
    """
    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return set(), f"unreadable ({exc})"
    if isinstance(data, dict):
        data = data.get(member_key, [])
    if not isinstance(data, list):
        return set(), "not a list of entries"
    slugs: set[str] = set()
    for i, entry in enumerate(data):
        if isinstance(entry, str):
            slugs.add(entry)
        elif isinstance(entry, dict) and isinstance(entry.get("slug"), str):
            slugs.add(entry["slug"])
        else:
            return slugs, f"entry {i} declares no slug"
    return slugs, None


def _catalogue_member_set(
    metadata: dict[str, Any], member_key: str, label: str, res: CheckResult
) -> set[str] | None:
    """Return one advertised member set, reporting malformed lists loudly."""
    members = metadata.get(member_key)
    if not isinstance(members, list) or not all(
        isinstance(item, str) for item in members
    ):
        res.add(FAIL, f"{label}: collection.yaml {member_key} is not a list of slugs.")
        return None
    if len(set(members)) != len(members):
        res.add(
            FAIL, f"{label}: collection.yaml {member_key} contains duplicate members."
        )
    return set(members)


def _disk_member_set(collection_dir: Path, member_key: str) -> tuple[set[str], str]:
    """Return the skill directories or tool YAMLs shipped by one collection."""
    if member_key == "skills":
        leaf_dir = layout.leaf_dir(collection_dir)
        members = set()
        if leaf_dir.is_dir():
            members = {
                path.name
                for path in leaf_dir.iterdir()
                if path.is_dir()
                and not path.name.startswith("_")
                and (path / "SKILL.md").is_file()
            }
        return members, f"{leaf_dir.name}/"
    tools_dir = collection_dir / "tools"
    members = (
        {path.stem for path in tools_dir.glob("*.yaml")}
        if tools_dir.is_dir()
        else set()
    )
    return members, "tools/"


def _report_member_difference(
    res: CheckResult,
    label: str,
    left: set[str],
    right: set[str],
    left_name: str,
    right_name: str,
) -> None:
    """Report both directions of one set comparison."""
    for missing_from_right in sorted(left - right):
        res.add(
            FAIL,
            f"{label}: {left_name} missing from {right_name}: {missing_from_right!r}.",
            slug=missing_from_right,
        )
    for missing_from_left in sorted(right - left):
        res.add(
            FAIL,
            f"{label}: {right_name} missing from {left_name}: {missing_from_left!r}.",
            slug=missing_from_left,
        )


def _check_advertised_count(
    metadata: dict[str, Any], member_key: str, label: str, res: CheckResult
) -> None:
    """Require the advertised count to equal its own member-list length."""
    count_key = f"{member_key}_count"
    if metadata.get(count_key) != len(metadata[member_key]):
        res.add(
            FAIL,
            f"{label}: {count_key} is {metadata.get(count_key)!r} but {member_key} "
            f"has {len(metadata[member_key])} members.",
        )


def _check_optional_index(
    collection_dir: Path,
    member_key: str,
    advertised: set[str],
    label: str,
    res: CheckResult,
) -> None:
    """Compare advertised members with an index when the collection ships one."""
    index_name = f"{member_key}_index.json"
    index_path = collection_dir / index_name
    if not index_path.is_file():
        return
    indexed, error = _index_slugs(index_path, member_key)
    if error:
        res.add(FAIL, f"{label}: {index_name}: {error}.", file=index_name)
        return
    _report_member_difference(
        res, label, advertised, indexed, f"collection.yaml {member_key}", index_name
    )


def _check_catalogue_members(
    collection_dir: Path,
    metadata: dict[str, Any],
    member_key: str,
    label: str,
    res: CheckResult,
) -> None:
    """Check count, disk members, and optional index for one member class."""
    advertised = _catalogue_member_set(metadata, member_key, label, res)
    if advertised is None:
        return
    _check_advertised_count(metadata, member_key, label, res)
    on_disk, disk_name = _disk_member_set(collection_dir, member_key)
    _report_member_difference(
        res, label, advertised, on_disk, f"collection.yaml {member_key}", disk_name
    )
    _check_optional_index(collection_dir, member_key, advertised, label, res)


def _check_collection_catalogue(
    collection_yaml: Path, root: Path, res: CheckResult
) -> None:
    """Check both advertised member classes in one collection manifest."""
    try:
        label = collection_yaml.relative_to(root).as_posix()
    except ValueError:
        label = collection_yaml.as_posix()
    metadata = _load_yaml(collection_yaml)
    _check_catalogue_members(collection_yaml.parent, metadata, "skills", label, res)
    _check_catalogue_members(collection_yaml.parent, metadata, "tools", label, res)


def check_catalogue_membership(collections_root: Path) -> CheckResult:
    """Reconcile every collection manifest found below ``collections_root``."""
    res = CheckResult(
        name="catalogue_membership",
        gates=[10],
        hard_gate=True,
        summary="Collection counts and advertised members match disk and published indexes.",
    )
    collection_yamls = sorted(Path(collections_root).rglob("collection.yaml"))
    if not collection_yamls:
        res.add(FAIL, f"No collection.yaml found under {collections_root}.")
        return res
    for collection_yaml in collection_yamls:
        _check_collection_catalogue(collection_yaml, Path(collections_root), res)
    if res.status == PASS:
        res.add(PASS, f"All {len(collection_yamls)} collection catalogues agree.")
    res.summary = f"{res.summary}  ({len(collection_yamls)} catalogues checked)"
    return res


def check_layout(
    collection_dir: Path,
    per_skill_max_bytes: int = _KB_SIDECAR_MAX_BYTES,
    collection_max_bytes: int = _COLLECTION_KB_MAX_BYTES,
) -> CheckResult:
    """Every shipped skill directory holds ``SKILL.md`` + at most a sidecar.

    Three things nothing checked before this gate existed:

    * **A forbidden-files list.**  The one-file-per-skill invariant was a
      convention.  A build that leaked a ``docs/`` tree into a promoted bundle
      would have shipped it.
    * **A byte budget.**  Both budgets FAIL loudly; neither truncates.  A
      truncated sidecar still parses, so truncation would ship a knowledge-base
      manifest that silently understates itself.
    * **``skills_index.json`` ↔ leaf-directory consistency** (gate 10).  An
      index entry with no skill on disk is a broken advertisement; a leaf the
      index never names is unreachable through the router.  The check is
      inert when the collection ships no index — most do not, and absence is
      not drift.
    """
    res = CheckResult(
        name="layout_packaging",
        gates=[10],
        hard_gate=True,
        summary=(
            "Each skill dir holds SKILL.md (+ optional skill_kb.json) within budget; "
            "skills_index.json matches the leaf directories."
        ),
    )
    n_skills = 0
    total_kb_bytes = 0
    for sk_md in _iter_skill_md(collection_dir):
        skill_dir = sk_md.parent
        if skill_dir == Path(collection_dir):
            # `iter_skill_md` falls back to the collection root when no skill
            # directory exists; the root is not a skill bundle, so the
            # file-set rule does not apply to it.
            continue
        n_skills += 1
        rel_dir = str(skill_dir.relative_to(collection_dir))
        for path in sorted(skill_dir.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(skill_dir).as_posix()
            if rel in _ALLOWED_SKILL_FILES:
                continue
            res.add(
                FAIL,
                f"{rel_dir}: unexpected file {rel!r} — a promoted skill directory "
                f"may hold only {sorted(_ALLOWED_SKILL_FILES)}.",
                file=f"{rel_dir}/{rel}",
            )
        sidecar = skill_dir / _KB_SIDECAR_FILENAME
        if sidecar.is_file():
            size = sidecar.stat().st_size
            total_kb_bytes += size
            if size > per_skill_max_bytes:
                res.add(
                    FAIL,
                    f"{rel_dir}: {_KB_SIDECAR_FILENAME} is {size} B, over the "
                    f"{per_skill_max_bytes} B per-skill budget — refuse and rebuild "
                    "it smaller; do not truncate.",
                    file=f"{rel_dir}/{_KB_SIDECAR_FILENAME}",
                    bytes=size,
                    budget=per_skill_max_bytes,
                )
    if total_kb_bytes > collection_max_bytes:
        res.add(
            FAIL,
            f"knowledge-base sidecars total {total_kb_bytes} B, over the "
            f"{collection_max_bytes} B collection budget.",
            bytes=total_kb_bytes,
            budget=collection_max_bytes,
        )

    unit_closure.record_index_closure(res, collection_dir)

    res.summary = f"{res.summary}  ({n_skills} skills checked)"
    if n_skills == 0:
        res.add(WARN, "No SKILL.md files found in collection.")
    return res


def check_unit_closure(collection_dir: Path) -> CheckResult:
    """Check pack index closure and helpers in the collection and its packs."""
    res = CheckResult(
        name="unit_closure",
        gates=[10],
        hard_gate=True,
        summary="Pack indexes match their leaves; declared helpers stay inside each unit.",
    )
    for finding in unit_closure.gate_findings(collection_dir):
        res.add(FAIL, **{**vars(finding), "unit": str(finding.unit)})
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


def _resolve_corpus(
    collection_dir: Path, explicit: Path | None
) -> tuple[dict[str, Any], Path | None]:
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
        check_workflows(collection_dir),
        check_layout(collection_dir),
        check_unit_closure(collection_dir),
    ]
    if (collection_dir / "collection.yaml").is_file():
        checks.append(check_catalogue_membership(collection_dir))

    counts = {PASS: 0, WARN: 0, FAIL: 0}
    for c in checks:
        counts[c.status] += 1
    overall = FAIL if counts[FAIL] else (WARN if counts[WARN] else PASS)

    mode = "strict" if strict else "advisory"
    # Hard gates (2,5,6,8,10,15) are never overridable (§8.2); in strict mode any
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
            "kb_sidecar_max_bytes": _KB_SIDECAR_MAX_BYTES,
            "collection_kb_max_bytes": _COLLECTION_KB_MAX_BYTES,
            "allowed_skill_files": sorted(_ALLOWED_SKILL_FILES),
        },
        "overall_status": overall,
        "blocking": blocking_fail,
        "exit_code": 1 if blocking_fail else 0,
        "summary_counts": counts,
        "hard_gate_ids": [2, 5, 6, 8, 10, 15],
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
        print(
            f"    {icon[c['status']]:>4}  {c['name']} (gates {c['gates']}){hard} — {c['n_findings']} finding(s)"
        )
        for d in c["details"]:
            print(f"            · [{icon[d['status']]}] {d['message']}")
    print(
        f"  overall    : {icon[report['overall_status']]}  (exit {report['exit_code']})"
    )
    if report["blocking"]:
        print(
            "  RESULT     : BLOCKED — strict mode + at least one FAIL on a hard gate."
        )
    elif report["overall_status"] == FAIL:
        print("  RESULT     : advisory — FAIL(s) reported, exit 0 (curator review).")


def _print_check_summary(result: CheckResult) -> None:
    """Print one repository-wide check with the release gate vocabulary."""
    print(f"{result.status.upper()}: {result.name} — {result.summary}")
    for detail in result.details:
        print(f"  [{detail['status'].upper()}] {detail['message']}")


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
        help="Collection directory, or a tree root with --catalogue-membership.",
    )
    parser.add_argument(
        "--catalogue-membership",
        action="store_true",
        help="Walk every collection.yaml below collection_dir and check advertised members.",
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

    if args.catalogue_membership:
        result = check_catalogue_membership(collection_dir)
        _print_check_summary(result)
        return 1 if result.status == FAIL else 0

    strict = bool(args.strict)  # --advisory and default both → strict=False
    report = run_gate(collection_dir, args.corpus, strict)

    report_path = args.report or (collection_dir / "gate_report.json")
    try:
        report_path.write_text(
            json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8"
        )
    except OSError as exc:
        sys.stderr.write(f"error: could not write report to {report_path}: {exc}\n")
        return 2

    if not args.quiet:
        _print_human_summary(report)
        print(f"  report     : {report_path}")

    return int(report["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
