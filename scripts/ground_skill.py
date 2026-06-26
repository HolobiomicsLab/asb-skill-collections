#!/usr/bin/env python3
"""ground_skill — executable, best-effort literature grounding for a skill claim.

The *propose-skill* flow (``commands/propose-skill.md`` step 4) lets a contributor
propose a candidate source DOI for a community skill. This module turns that into
an executable check: it ensures the canonical per-paper KB
(``asb-paper-<doi-slug>`` — the SAME slug the build + binder use, see
:func:`scripts.perspicacite_kb_bind.kb_slug`) exists in a running Perspicacité
instance, then asks — over ``/api/chat`` scoped to that KB — whether the paper
**supports the skill's claims**, and parses a structured verdict + evidence quote.

Design contract (mirrors the binder's generate-on-use + graceful-degrade rails):

* :func:`verify_doi_support` **never raises**. Any error — unreachable server,
  malformed reply, missing answer — degrades to
  ``{supported: False, confidence: "low", evidence: ""}`` (plus the ``doi``).
* The HTTP client is **injected** (``http``), a callable matching
  ``perspicacite_kb_bind._http(method, path, body=None, timeout=...)``. Tests pass
  a mock; the CLI uses the real ``_http``. No live network in importable code.
* No git/gh side effects. No ``Date.now``.

A *supportive* verdict at ``high``/``medium`` confidence is the signal the command
uses to attach ``derived_from`` + ``metadata.literature_upgrade_candidate: true``.

Examples
--------
    python -m scripts.ground_skill --doi 10.1021/acs.jnatprod.7b00737 \
        --skill-md path/to/SKILL.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys

from scripts.perspicacite_kb_bind import _http as _real_http
from scripts.perspicacite_kb_bind import kb_slug

UNSUPPORTED = {"supported": False, "confidence": "low", "evidence": ""}

VALID_CONFIDENCE = ("high", "medium", "low")

_PROMPT = (
    "You are grounding a candidate skill against a single source paper. Using ONLY "
    "the retrieved passages from this paper, decide whether the paper SUPPORTS the "
    "claims/methods of the skill below.\n\n"
    "Reply in EXACTLY this structured form:\n"
    "VERDICT: SUPPORTED or NOT_SUPPORTED\n"
    "CONFIDENCE: high, medium, or low\n"
    'EVIDENCE: a short verbatim quote from the paper (or "" if none)\n\n'
    "Skill:\n{skill}\n"
)


def _ensure_kb(slug: str, doi: str, http) -> None:
    """Best-effort create+ingest the per-DOI KB via the injected ``http``.

    Mirrors :func:`scripts.perspicacite_kb_bind.prepare_kb` but uses the injected
    client so it stays network-free under test. Swallows every error — grounding is
    best-effort and the chat call degrades on its own if the KB is absent.
    """
    try:
        stats = http("GET", f"/api/kb/{slug}/stats", timeout=30)
        if isinstance(stats, dict) and (stats.get("chunk_count") or 0) > 0:
            return  # already present
    except Exception:
        pass  # 404 / unreachable — fall through to (re)create
    try:
        http("POST", "/api/kb",
             {"name": slug, "description": f"ASB grounding KB ({doi})"}, timeout=60)
    except Exception:
        pass  # 400/409 already-exists, or unreachable
    try:
        http("POST", f"/api/kb/{slug}/dois", {"dois": [doi]}, timeout=1200)
    except Exception:
        pass


def _answer_text(resp) -> str:
    """Pull the assistant answer out of a /api/chat response (binder's shape)."""
    if isinstance(resp, dict):
        ans = resp.get("answer") or resp.get("response") or resp.get("content")
        if isinstance(ans, str):
            return ans
        if ans is not None:
            return json.dumps(ans)
    if isinstance(resp, str):
        return resp
    return ""


def _parse_verdict(text: str) -> dict:
    """Parse the structured VERDICT/CONFIDENCE/EVIDENCE reply.

    Tolerant: missing/garbled fields degrade to unsupported+low rather than raise.
    """
    if not text:
        return dict(UNSUPPORTED)
    m_verdict = re.search(r"VERDICT\s*:\s*(SUPPORTED|NOT[_\s-]?SUPPORTED)", text, re.I)
    if not m_verdict:
        return dict(UNSUPPORTED)
    supported = m_verdict.group(1).upper().replace(" ", "_").replace("-", "_") == "SUPPORTED"

    conf = "low"
    m_conf = re.search(r"CONFIDENCE\s*:\s*(high|medium|low)", text, re.I)
    if m_conf:
        conf = m_conf.group(1).lower()
    elif supported:
        conf = "medium"  # supported but unspecified confidence -> conservative medium

    evidence = ""
    m_ev = re.search(r"EVIDENCE\s*:\s*(.+)", text, re.I | re.S)
    if m_ev:
        evidence = m_ev.group(1).strip().strip('"').strip()

    if not supported:
        # never advertise high confidence for a negative verdict downstream
        conf = "low" if conf == "high" else conf

    return {"supported": supported, "confidence": conf, "evidence": evidence}


def verify_doi_support(skill_text: str, doi: str, *, http=None, prepare: bool = True) -> dict:
    """Ask whether ``doi``'s paper supports ``skill_text``'s claims. Never raises.

    Parameters
    ----------
    skill_text : str
        The skill's claims/body (e.g. its SKILL.md text) to ground.
    doi : str
        Candidate source DOI; its KB is ``asb-paper-<doi-slug>``.
    http : callable, optional
        ``http(method, path, body=None, timeout=...)`` (the binder's ``_http``
        shape). Defaults to the real Perspicacité client.
    prepare : bool
        When True, best-effort create+ingest the KB before querying.

    Returns
    -------
    dict
        ``{doi, supported: bool, confidence: "high"|"medium"|"low", evidence: str}``.
        On any failure: ``{doi, supported: False, confidence: "low", evidence: ""}``.
    """
    if http is None:
        http = _real_http
    result = dict(UNSUPPORTED)
    result["doi"] = doi
    try:
        slug = kb_slug(doi)
        if prepare:
            _ensure_kb(slug, doi, http)
        payload = {
            "query": _PROMPT.format(skill=skill_text or ""),
            "kb_names": [slug],
            "mode": "paper",
            "stream": False,
        }
        resp = http("POST", "/api/chat", payload, timeout=600)
        parsed = _parse_verdict(_answer_text(resp))
        parsed["doi"] = doi
        return parsed
    except Exception:
        # Unreachable / unexpected — best-effort grounding degrades, never raises.
        return result


def main(argv=None, *, http=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--doi", required=True, help="candidate source DOI to ground against")
    ap.add_argument("--skill-md", required=True,
                    help="path to the SKILL.md whose claims to verify")
    a = ap.parse_args(argv)

    try:
        from pathlib import Path
        skill_text = Path(a.skill_md).read_text(encoding="utf-8")
    except Exception as e:  # missing/unreadable file is a real CLI error
        print(json.dumps({"error": f"cannot read --skill-md: {str(e)[:160]}"}, indent=2))
        return 1

    out = verify_doi_support(skill_text, a.doi, http=http)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
