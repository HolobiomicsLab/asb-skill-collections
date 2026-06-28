#!/usr/bin/env python3
"""semantic_search — Perspicacité-first retrieval over the ASB collection (P2).

The router's "find the right skill/workflow" step. Uses SEMANTIC retrieval
(text-embedding-3-large — the same model Perspicacité uses) when an embedding backend is
available, and falls back to a KEYWORD index search otherwise, so it always works offline.
This is the upgrade from pure keyword/EDAM matching (which the P0 pilot showed mis-ranks
leaves) to meaning-based ranking, while preserving the collection's portability.

Targets:
  --target skills    -> skills_index.json   (default)
  --target workflows -> workflows_index.json (composite workflow super-skills)

Semantic mode is used when ALL of: numpy importable, an embedding cache exists
(env ASB_LEAF_EMB_CACHE or <collection>/.cache/leafemb_<name>.npz), and OPENAI_API_KEY set.
Otherwise keyword mode. Force with --mode {auto,semantic,keyword}.

Usage:
  python semantic_search.py --query "annotate untargeted LC-MS/MS" --collection <dir> [--target skills|workflows] [--technique LC-MS] [--k 10]
"""
from __future__ import annotations
import argparse, json, os, sys, urllib.request, urllib.error
from pathlib import Path

EMB_MODEL = "text-embedding-3-large"
EMB_URL = "https://api.openai.com/v1/embeddings"
STOP = set("the a an of for and or to in on with from by use when need data your this that "
           "is are be using into across over per via".split())


def _index_path(collection: Path, target: str) -> Path:
    return collection / ("workflows_index.json" if target == "workflows" else "skills_index.json")


def _row_text(r: dict) -> str:
    return " ".join([r.get("name", ""), r.get("description", ""),
                     " ".join(r.get("tools", [])), " ".join(r.get("techniques", []))]).lower()


def _tech_ok(r: dict, technique: str | None) -> bool:
    if not technique:
        return True
    return technique.lower() in [t.lower() for t in r.get("techniques", [])]


def keyword_search(rows, query, technique, k):
    terms = [t for t in "".join(c.lower() if c.isalnum() else " " for c in query).split()
             if t not in STOP and len(t) > 2]
    scored = []
    for r in rows:
        if not _tech_ok(r, technique):
            continue
        text = _row_text(r)
        score = sum(text.count(t) for t in terms) + 3 * sum(t in r.get("name", "").lower() for t in terms)
        if score:
            scored.append((score, r))
    scored.sort(key=lambda x: -x[0])
    return [{"slug": r.get("slug"), "name": r.get("name"), "score": s,
             "techniques": r.get("techniques", []), "tools": r.get("tools", [])[:4]}
            for s, r in scored[:k]]


def _cache_for(collection: Path) -> Path | None:
    env = os.environ.get("ASB_LEAF_EMB_CACHE")
    if env and Path(env).exists():
        return Path(env)
    for c in [collection / ".cache" / f"leafemb_{collection.name}.npz",
              collection.parent.parent / ".cache" / f"leafemb_{collection.name}.npz"]:
        if c.exists():
            return c
    return None


def semantic_search(collection, rows, query, technique, k):
    import numpy as np
    cache = _cache_for(collection)
    key = os.environ.get("OPENAI_API_KEY")
    if not (cache and key):
        return None  # caller falls back
    z = np.load(cache, allow_pickle=True)
    emb, slugs = z["emb"], list(z["slug"])
    body = json.dumps({"model": EMB_MODEL, "input": query}).encode()
    req = urllib.request.Request(EMB_URL, data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            q = np.array(json.load(r)["data"][0]["embedding"], dtype="float32")
    except (urllib.error.URLError, KeyError):
        return None
    q /= (np.linalg.norm(q) + 1e-9)
    scores = emb @ q
    by_slug = {x["slug"]: x for x in rows if "slug" in x}
    order = np.argsort(-scores)
    out = []
    for i in order:
        slug = slugs[i]
        r = by_slug.get(slug)
        if r is None or not _tech_ok(r, technique):
            continue
        out.append({"slug": slug, "name": r.get("name"), "score": round(float(scores[i]), 4),
                    "techniques": r.get("techniques", []), "tools": r.get("tools", [])[:4]})
        if len(out) >= k:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--collection", required=True)
    ap.add_argument("--target", choices=["skills", "workflows"], default="skills")
    ap.add_argument("--technique", default=None)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--mode", choices=["auto", "semantic", "keyword"], default="auto")
    a = ap.parse_args()
    coll = Path(a.collection)
    rows = json.loads(_index_path(coll, a.target).read_text())
    mode = a.mode
    res = None
    if mode in ("auto", "semantic"):
        try:
            res = semantic_search(coll, rows, a.query, a.technique, a.k)
        except Exception:
            res = None
        if res is not None:
            mode = "semantic"
    if res is None:
        res = keyword_search(rows, a.query, a.technique, a.k)
        mode = "keyword"
    print(json.dumps({"mode": mode, "target": a.target, "results": res}, indent=2))


if __name__ == "__main__":
    main()
