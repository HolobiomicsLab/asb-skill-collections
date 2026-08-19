#!/usr/bin/env python3
"""Build / align the leaf (or workflow) embedding cache for a collection.

The collection router (`bin/semantic_search.py`) ranks skills with
`text-embedding-3-large` when an embedding cache is present. That cache is a
`.npz` with two arrays:

    emb   float32 [N, D]   L2-normalised row embeddings (cosine == dot product)
    slug  str     [N]      the skill/workflow slug for each row

This script produces that cache for ANY collection in one of two modes:

  ALIGN (default, cheap, no API):  given a SOURCE `.npz` that already holds
      embeddings (e.g. the full set produced at collection-build time), filter +
      reorder it to exactly the slugs in the collection's current index. Stale
      slugs (purged leaves) are dropped; the result is byte-for-byte reproducible
      and needs no API key. This is what you run before a release after a purge.

  EMBED (`--embed`, needs OPENAI_API_KEY):  embed the index rows directly via the
      OpenAI embeddings API. Used to bootstrap a NEW collection that has no source
      cache yet, or to fill in slugs missing from the source. Costs API credits.

By design this is collection-agnostic: it reads slugs and text from the
collection's own `skills_index.json` / `workflows_index.json` — no domain, DOI,
or slug literals live here (see the generalize-or-stop guardrail).

Usage
-----
  # Align a full source cache to the current (possibly purged) index:
  python scripts/build_leaf_embedding_cache.py \
      --collection collections/<slug>/v<N> --source path/to/full_embeddings.npz

  # Bootstrap from scratch for a new collection (needs OPENAI_API_KEY):
  python scripts/build_leaf_embedding_cache.py \
      --collection collections/<slug>/v<N> --embed

Output defaults to `<collection>/.cache/leafemb_<collection.name>.npz`, the path
`bin/semantic_search.py` looks for. Ship the file as a Zenodo / GitHub Release
asset (it is gitignored — too large and binary for version control).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

EMB_MODEL = "text-embedding-3-large"
EMB_URL = "https://api.openai.com/v1/embeddings"
EMB_BATCH = 256


def _index_path(collection: Path, target: str) -> Path:
    return collection / ("workflows_index.json" if target == "workflows" else "skills_index.json")


def _default_output(collection: Path) -> Path:
    return collection / ".cache" / f"leafemb_{collection.name}.npz"


def _row_text(r: dict) -> str:
    """Text fed to the embedder. Mirrors the fields semantic_search ranks on so a
    freshly embedded cache stays comparable to an aligned one."""
    parts = [r.get("name", ""), r.get("description", "")]
    tools = r.get("tools") or []
    techniques = r.get("techniques") or []
    if tools:
        parts.append("Tools: " + ", ".join(tools))
    if techniques:
        parts.append("Techniques: " + ", ".join(techniques))
    return "\n".join(p for p in parts if p).strip()


def _normalise(emb):
    import numpy as np

    emb = np.asarray(emb, dtype="float32")
    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return (emb / norms).astype("float32")


def _embed_texts(texts: list[str], key: str):
    """Embed a list of texts via the OpenAI embeddings API, batched."""
    import numpy as np

    out: list[list[float]] = []
    for start in range(0, len(texts), EMB_BATCH):
        batch = texts[start : start + EMB_BATCH]
        body = json.dumps({"model": EMB_MODEL, "input": batch}).encode()
        req = urllib.request.Request(
            EMB_URL,
            data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    data = json.load(r)["data"]
                out.extend(d["embedding"] for d in data)
                break
            except (urllib.error.URLError, KeyError) as exc:
                if attempt == 4:
                    raise
                wait = 2 ** attempt
                print(f"  embed batch retry {attempt + 1} after {wait}s ({exc})", file=sys.stderr)
                time.sleep(wait)
        print(f"  embedded {min(start + EMB_BATCH, len(texts))}/{len(texts)}", file=sys.stderr)
    return np.asarray(out, dtype="float32")


def build_cache(
    collection: Path,
    target: str,
    source: Path | None,
    output: Path | None,
    embed_missing: bool,
) -> dict:
    import numpy as np

    rows = json.loads(_index_path(collection, target).read_text())
    index_slugs = [r["slug"] for r in rows if r.get("slug")]
    if not index_slugs:
        raise SystemExit(f"no slugs in index for {collection} (target={target})")
    by_slug = {r["slug"]: r for r in rows if r.get("slug")}

    src_vec: dict[str, "np.ndarray"] = {}
    if source is not None:
        z = np.load(source, allow_pickle=True)
        src_emb, src_slugs = z["emb"], [str(s) for s in z["slug"]]
        for s, v in zip(src_slugs, src_emb):
            src_vec[s] = v
        print(f"source cache: {len(src_slugs)} embeddings, dim={src_emb.shape[1]}")

    aligned: list["np.ndarray"] = []
    aligned_slugs: list[str] = []
    missing: list[str] = []
    for slug in index_slugs:
        if slug in src_vec:
            aligned.append(src_vec[slug])
            aligned_slugs.append(slug)
        else:
            missing.append(slug)

    key = os.environ.get("OPENAI_API_KEY")
    if missing and embed_missing:
        if not key:
            raise SystemExit("--embed requested but OPENAI_API_KEY is not set")
        print(f"embedding {len(missing)} slug(s) not present in source ...")
        texts = [_row_text(by_slug[s]) for s in missing]
        new_emb = _embed_texts(texts, key)
        for slug, vec in zip(missing, new_emb):
            aligned.append(vec)
            aligned_slugs.append(slug)
        missing = []

    if not aligned:
        raise SystemExit(
            "no embeddings produced — provide --source and/or --embed (with OPENAI_API_KEY)"
        )

    emb = _normalise(np.vstack(aligned))
    slug_arr = np.array(aligned_slugs, dtype=object)

    out_path = output or _default_output(collection)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out_path, emb=emb, slug=slug_arr)

    dropped = len(src_vec) - len([s for s in src_vec if s in by_slug]) if source else 0
    return {
        "output": str(out_path),
        "index_slugs": len(index_slugs),
        "embedded": len(aligned_slugs),
        "missing": missing,
        "dropped_stale_from_source": dropped,
        "dim": int(emb.shape[1]),
        "bytes": out_path.stat().st_size,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--collection", required=True, help="collection dir, e.g. collections/<slug>/v<N>")
    ap.add_argument("--target", choices=["skills", "workflows"], default="skills")
    ap.add_argument("--source", default=None, help="full source .npz (emb+slug) to align from")
    ap.add_argument("--output", default=None, help="output .npz (default: <collection>/.cache/leafemb_<name>.npz)")
    ap.add_argument("--embed", action="store_true",
                    help="embed slugs missing from source via OpenAI (needs OPENAI_API_KEY)")
    a = ap.parse_args()

    collection = Path(a.collection)
    if not collection.exists():
        raise SystemExit(f"collection not found: {collection}")

    report = build_cache(
        collection=collection,
        target=a.target,
        source=Path(a.source) if a.source else None,
        output=Path(a.output) if a.output else None,
        embed_missing=a.embed,
    )
    print(json.dumps(report, indent=2))
    if report["missing"]:
        print(
            f"WARNING: {len(report['missing'])} slug(s) had no embedding "
            f"(not in source, --embed off). They will fall back to keyword retrieval.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
