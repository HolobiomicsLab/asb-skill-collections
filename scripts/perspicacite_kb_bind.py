#!/usr/bin/env python3
"""perspicacite_kb_bind — auto-bind an ASB skill to its Perspicacité grounding KB.

This is the *use-time* glue between an installed ASB skill and the evidence it
was built from.  When an agent (or a person) activates one or more skills from
this collection, this tool:

  1. **identifies** the grounding for each skill from ``kb_bundle.json`` —
     the source-paper DOI(s), the linked software tools, and the canonical
     per-paper KB slug (``asb-paper-<doi>``, the SAME slug the build used);
  2. **auto-generates** that KB in a running Perspicacité instance if it does
     not already exist — create the KB, ingest the DOI (paper full text +
     supplementary information are appended automatically by Perspicacité);
  3. **queries** it on demand (RAG over the bound KB) so the skill's claims,
     parameters, and evidence spans can be checked against the source.

Tiers (``--tier``) — the grounding depth a caller wants to leverage:

    paper   the paper full text + SI (default; KB mode 'paper')
    si      restrict retrieval to supplementary information / tables
    repo    the tool's source repository (no KB; returns the repo URL(s) so the
            agent can read code / README directly)

This script is stdlib-only and talks to Perspicacité over HTTP
(``PERSPICACITE_BASE``, default http://127.0.0.1:8000).  It mirrors the
build-time grounding path so use-time KBs are byte-for-byte the same target the
collection was assembled against.

Examples
--------
    # Prepare the KB(s) for one skill (create + ingest if missing):
    python scripts/perspicacite_kb_bind.py prepare \
        --collection collections/metabolomics/v2\
        --skill metabolomic-data-preprocessing-optimization

    # Ask a grounded question against a skill's KB:
    python scripts/perspicacite_kb_bind.py query \
        --collection collections/metabolomics/v2 \
        --skill metabolomic-data-preprocessing-optimization \
        --question "What normalization methods does the tool evaluate?"

    # Resolve grounding for a skill without touching Perspicacité (offline):
    python scripts/perspicacite_kb_bind.py resolve \
        --collection collections/metabolomics/v2 --skill <slug>
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = os.environ.get("PERSPICACITE_BASE", "http://127.0.0.1:8000").rstrip("/")


def kb_slug(doi: str) -> str:
    return ("asb-paper-" + re.sub(r"[^a-zA-Z0-9]+", "-", doi).strip("-")).lower()


def _http(method: str, path: str, body=None, timeout: int = 1200):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        BASE + path, data=data, method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def load_bundle(collection: Path) -> dict:
    p = collection / "kb_bundle.json"
    if not p.is_file():
        sys.exit(f"error: kb_bundle.json not found under {collection}")
    return json.loads(p.read_text(encoding="utf-8"))


def resolve_skill(bundle: dict, skill: str) -> dict:
    skills = bundle.get("skills") or {}
    if skill not in skills:
        # tolerant: accept the directory name or a close match
        matches = [s for s in skills if s == skill or skill in s]
        if len(matches) == 1:
            skill = matches[0]
        elif not matches:
            sys.exit(f"error: skill '{skill}' not in kb_bundle.json")
        else:
            sys.exit(f"error: '{skill}' is ambiguous: {matches[:5]}")
    rec = dict(skills[skill])
    rec["slug"] = skill
    rec["kb_slugs"] = rec.get("kb_slugs") or [kb_slug(d) for d in rec.get("dois", [])]
    return rec


def kb_exists(slug: str) -> bool:
    try:
        _http("GET", f"/api/kb/{slug}/stats", timeout=30)
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        return False
    except Exception:
        return False


def kb_chunks(slug: str):
    try:
        return _http("GET", f"/api/kb/{slug}/stats", timeout=30).get("chunk_count")
    except Exception:
        return None


def prepare_kb(slug: str, doi: str, desc: str) -> dict:
    """Create the KB if missing and ingest the DOI (paper + SI auto-appended)."""
    status = {"kb": slug, "doi": doi, "created": False, "ingested": False, "chunks": None}
    if kb_exists(slug) and (kb_chunks(slug) or 0) > 0:
        status["chunks"] = kb_chunks(slug)
        status["note"] = "already present"
        return status
    try:
        _http("POST", "/api/kb", {"name": slug, "description": desc}, timeout=60)
        status["created"] = True
    except urllib.error.HTTPError as e:
        if e.code not in (400, 409):
            status["error"] = f"create {e.code}"
            return status
    except Exception as e:
        # connection refused / DNS / timeout — Perspicacité unreachable. Degrade
        # gracefully (the kb backend is optional; callers fall back to `local`).
        status["error"] = f"perspicacite unreachable: {str(e)[:160]}"
        return status
    try:
        resp = _http("POST", f"/api/kb/{slug}/dois", {"dois": [doi]}, timeout=1200)
        status["ingested"] = True
        status["added_full_text"] = resp.get("added_with_full_text")
        status["added_metadata_only"] = resp.get("added_metadata_only")
        status["chunks"] = kb_chunks(slug)
    except Exception as e:
        status["error"] = f"ingest: {str(e)[:160]}"
    return status


def cmd_resolve(args) -> int:
    bundle = load_bundle(Path(args.collection))
    rec = resolve_skill(bundle, args.skill)
    print(json.dumps({
        "skill": rec["slug"], "tier": args.tier,
        "dois": rec.get("dois", []), "tools": rec.get("tools", []),
        "kb_slugs": rec["kb_slugs"], "kb_mode": bundle.get("perspicacite_kb_mode", "paper"),
        "perspicacite_base": BASE,
    }, indent=2))
    return 0


def cmd_prepare(args) -> int:
    bundle = load_bundle(Path(args.collection))
    rec = resolve_skill(bundle, args.skill)
    if args.tier == "repo":
        print(json.dumps({"skill": rec["slug"], "tier": "repo",
                          "tools": rec.get("tools", []),
                          "note": "repo tier: read the tool source directly; no KB built."}, indent=2))
        return 0
    if not rec.get("dois"):
        print(json.dumps({"skill": rec["slug"], "note": "no source DOI — nothing to ground."}))
        return 0
    out = []
    for doi, slug in zip(rec["dois"], rec["kb_slugs"]):
        out.append(prepare_kb(slug, doi, f"ASB grounding KB for skill {rec['slug']} ({doi})"))
    print(json.dumps({"skill": rec["slug"], "tier": args.tier, "kbs": out}, indent=2))
    return 0 if all(not k.get("error") for k in out) else 1


def cmd_query(args) -> int:
    bundle = load_bundle(Path(args.collection))
    rec = resolve_skill(bundle, args.skill)
    if not rec.get("dois"):
        sys.exit(f"error: skill '{rec['slug']}' has no source DOI to query.")
    # ensure KBs exist first (generate-on-use)
    if not args.no_prepare:
        for doi, slug in zip(rec["dois"], rec["kb_slugs"]):
            prepare_kb(slug, doi, f"ASB grounding KB for skill {rec['slug']} ({doi})")
    targets = rec["kb_slugs"]
    mode = bundle.get("perspicacite_kb_mode", "paper")
    # Grounded RAG goes through /api/chat scoped to the bound KB(s).  The 'si'
    # tier hints retrieval toward supplementary material via the query context.
    payload = {
        "query": args.question,
        "kb_names": targets,
        "mode": mode,
        "stream": False,
    }
    if args.tier == "si":
        payload["context"] = ("Prefer evidence from the supplementary information / "
                              "supplementary tables and figures of the source paper.")
    try:
        resp = _http("POST", "/api/chat", payload, timeout=600)
    except Exception as e:
        sys.exit(f"error: query failed against KB(s) {targets}: {str(e)[:200]}")
    if isinstance(resp, dict):
        ans = resp.get("answer") or resp.get("response") or resp.get("content")
        if ans:
            print(ans if isinstance(ans, str) else json.dumps(ans, indent=2)[:6000])
            cites = resp.get("citations") or resp.get("sources")
            if cites:
                print("\n--- sources ---")
                print(json.dumps(cites, indent=2)[:2000])
            return 0
    print(json.dumps(resp, indent=2)[:6000] if isinstance(resp, (dict, list)) else str(resp)[:6000])
    return 0


def unpaywall_oa_url(doi, email, _http=urllib.request.urlopen):
    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    try:
        with _http(urllib.request.Request(url), timeout=30) as r:
            data = json.loads(r.read())
    except Exception:
        return None
    loc = data.get("best_oa_location") or {}
    return loc.get("url_for_pdf") or loc.get("url") or None


def clone_repo(url, dest, _run=subprocess.run):
    dest = Path(dest)
    if dest.exists():
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        p = _run(["git", "clone", "--depth", "1", "--", url, str(dest)],
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return getattr(p, "returncode", 1) == 0
    except Exception:
        return False


def link_only(rec) -> bool:
    """Non-open tiers must never embed source content into shipped bundles."""
    return (rec.get("license_tier") or "open") in ("noncommercial", "restricted")


def build_local_manifest(rec, dest, paper, email, _clone=clone_repo, _oa=None):
    if _oa is None:
        _oa = unpaywall_oa_url
    tier = rec.get("license_tier") or "open"
    if link_only(rec):
        manifest = {
            "skill": rec["slug"], "mode": "link-only", "license_tier": tier,
            "note": "non-open tier: referenced, not embedded; bundling is the consumer's responsibility.",
            "repos": [{"url": u, "embedded": False} for u in (rec.get("repo_urls") or [])],
            "paper": None,
        }
        if paper and rec.get("dois"):
            manifest["paper"] = {"doi": rec["dois"][0], "embedded": False}
        return manifest
    base = Path(dest) / rec["slug"]
    manifest = {"skill": rec["slug"], "mode": "embed", "license_tier": tier, "repos": [], "paper": None}
    for i, url in enumerate(rec.get("repo_urls") or []):
        d = base / "repo" / str(i)
        manifest["repos"].append({"url": url, "dest": str(d), "cloned": _clone(url, d)})
    if paper and rec.get("dois"):
        doi = rec["dois"][0]
        manifest["paper"] = {"doi": doi, "oa_url": _oa(doi, email), "path": None}
    return manifest


def cmd_local(args) -> int:
    bundle = load_bundle(Path(args.collection))
    rec = resolve_skill(bundle, args.skill)
    print(json.dumps(build_local_manifest(rec, args.dest, args.paper, args.email), indent=2))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("resolve", "prepare", "query", "local"):
        sp = sub.add_parser(name)
        sp.add_argument("--collection", required=True,
                        help="Path to the collection/pack dir (contains kb_bundle.json).")
        sp.add_argument("--skill", required=True, help="Skill slug.")
        sp.add_argument("--tier", choices=("paper", "si", "repo"), default="paper",
                        help="Grounding tier (default: paper = full text + SI).")
        if name == "query":
            sp.add_argument("--question", required=True)
            sp.add_argument("--no-prepare", action="store_true",
                            help="Do not auto-create/ingest the KB before querying.")
        if name == "local":
            sp.add_argument("--dest", default=".grounding")
            sp.add_argument("--paper", action="store_true",
                            help="Also fetch the OA paper via Unpaywall.")
            sp.add_argument("--email", default=os.environ.get("UNPAYWALL_EMAIL", "research@holobiomics.org"))
    args = ap.parse_args(argv)
    return {"resolve": cmd_resolve, "prepare": cmd_prepare, "query": cmd_query, "local": cmd_local}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
