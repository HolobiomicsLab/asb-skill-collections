#!/usr/bin/env python3
"""build_grounding_bundle — emit self-contained grounding artifacts into a unit
(a per-technique pack or the full collection): filtered+enriched kb_bundle.json,
vendored perspicacite_kb_bind.py, /ground command, GROUNDING.md."""
from __future__ import annotations
import json
from pathlib import Path


def resolve_repo_urls(skill_dois, corpus_papers, tools_index):
    doi_set = {d for d in skill_dois}
    out = []
    by_doi = {p.get("doi"): p for p in corpus_papers}
    for d in skill_dois:
        url = (by_doi.get(d) or {}).get("repo_url")
        if url and url not in out:
            out.append(url)
    for t in tools_index:
        if doi_set.intersection(t.get("dois") or []):
            url = t.get("canonical_url")
            if url and url not in out:
                out.append(url)
    return out
