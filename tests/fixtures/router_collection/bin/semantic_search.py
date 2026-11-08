#!/usr/bin/env python3
"""Keyword and optional embedding-backed retrieval for this collection."""
from pathlib import Path
import sys

COLLECTION_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from search_skills import *  # noqa: F401,F403,E402

# Wrapper imports follow the shared selector, including its future import.
import argparse  # noqa: E402
import urllib.error  # noqa: E402
import urllib.request  # noqa: E402

EMB_MODEL = "text-embedding-3-large"
EMB_URL = "https://api.openai.com/v1/embeddings"


def _index_path(collection: Path, target: str) -> Path:
    """Resolve indexes identically to the package and standalone router."""
    return index_path(collection, target)


def _tech_ok(row: dict, technique: str | None) -> bool:
    if not technique:
        return True
    return technique.lower() in [tag.lower() for tag in row.get("techniques", [])]


def _keep(row: dict, technique: str | None, max_tools: int) -> bool:
    """Apply the technique filter and the registry/meta-artifact guard."""
    if not _tech_ok(row, technique):
        return False
    if max_tools and len(row.get("tools", [])) > max_tools:
        return False
    return True


def _cache_for(collection: Path) -> Path | None:
    env = os.environ.get("ASB_LEAF_EMB_CACHE")
    if env and Path(env).exists():
        return Path(env)
    for candidate in [
        collection / ".cache" / f"leafemb_{collection.name}.npz",
        collection.parent.parent / ".cache" / f"leafemb_{collection.name}.npz",
    ]:
        if candidate.exists():
            return candidate
    return None


class SemanticUnavailable(RuntimeError):
    """Semantic ranking cannot run here; the message says why, in one line."""


def semantic_search(collection, rows, query, technique, k, max_tools):
    """Rank cached leaf vectors by the embedding of one query."""
    try:
        import numpy as np
    except ImportError:
        raise SemanticUnavailable("numpy is not installed") from None
    cache = _cache_for(collection)
    if cache is None:
        raise SemanticUnavailable(
            "no leaf embedding cache (set ASB_LEAF_EMB_CACHE or place "
            f".cache/leafemb_{collection.name}.npz under the collection)"
        )
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SemanticUnavailable("OPENAI_API_KEY is not set, so the query cannot be embedded")
    with np.load(cache, allow_pickle=True) as cache_data:
        embeddings, slugs = cache_data["emb"], list(cache_data["slug"])
    body = json.dumps({"model": EMB_MODEL, "input": query}).encode()
    request = urllib.request.Request(
        EMB_URL,
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            query_embedding = np.array(
                json.load(response)["data"][0]["embedding"], dtype="float32"
            )
    except (urllib.error.URLError, KeyError) as error:
        raise SemanticUnavailable(
            f"the query embedding request failed ({error.__class__.__name__})"
        ) from None
    query_embedding /= np.linalg.norm(query_embedding) + 1e-9
    scores = embeddings @ query_embedding
    by_slug = {row["slug"]: row for row in rows if "slug" in row}
    results = []
    for index in np.argsort(-scores):
        slug = str(slugs[index])
        row = by_slug.get(slug)
        if row is None or not _keep(row, technique, max_tools):
            continue
        results.append({
            "slug": slug,
            "name": row.get("name"),
            "score": round(float(scores[index]), 4),
            "techniques": row.get("techniques", []),
            "tools": row.get("tools", [])[:4],
        })
        if len(results) >= k:
            break
    return results


def main(argv: list[str] | None = None) -> int:
    """Run semantic retrieval, or the shared keyword selector with fallback."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--collection", type=Path, default=COLLECTION_ROOT)
    parser.add_argument("--target", choices=sorted(TARGETS), default="skills")
    parser.add_argument("--technique", default=None)
    parser.add_argument("-k", "--k", type=int, default=10)
    parser.add_argument("--mode", choices=["auto", "semantic", "keyword"], default="auto")
    parser.add_argument("--max-tools", type=int, default=25)
    parser.add_argument("--selector", choices=SELECTORS)
    args = parser.parse_args(argv)
    collection = args.collection.resolve()
    rows = json.loads(_index_path(collection, args.target).read_text())
    max_tools = args.max_tools if args.target == "skills" else 0
    results = None
    mode = args.mode
    if mode in ("auto", "semantic"):
        try:
            results = semantic_search(
                collection, rows, args.query, args.technique, args.k, max_tools
            )
            reason = "the semantic backend returned no result"
        except SemanticUnavailable as error:
            results, reason = None, str(error)
        except Exception as error:
            results, reason = None, f"the semantic backend failed ({error.__class__.__name__})"
        if results is not None:
            mode = "semantic"
        elif args.mode == "semantic":
            print(f"semantic_search.py: --mode semantic cannot run: {reason}.", file=sys.stderr)
            return 2
        else:
            print(
                f"semantic_search.py: semantic ranking unavailable ({reason}); "
                "falling back to the keyword selector.",
                file=sys.stderr,
            )
    if results is None:
        results = keyword_search(
            rows,
            args.query,
            args.technique,
            args.k,
            max_tools,
            collection=collection_id(collection),
            target=args.target,
            selector=args.selector,
            fallback="keyword" if args.mode == "keyword" else "keyword-after-semantic",
        )
        mode = "keyword"
    print(json.dumps({"mode": mode, "target": args.target, "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
