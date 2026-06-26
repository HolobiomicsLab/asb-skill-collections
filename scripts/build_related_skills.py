"""Embedding similarity graph — precompute ``related_skills`` per skill (Task B4).

A complement to the lexical ``skill_match`` core: instead of TF-IDF cosine, this
builds a *semantic* similarity graph from sentence-transformer embeddings of each
skill's :func:`skill_match.skill_doc` text, and writes the resulting top-N
neighbour lists into ``skills_index.json`` + ``kb_bundle.json``.

Two backends, one injectable interface (``embedder_for``):

* **local** — pinned MiniLM (``sentence-transformers``, ``[embed]`` extra):
  lightweight, offline, no key.
* **openai** — ``text-embedding-3-large`` (``openai``, ``[embed-openai]`` extra):
  the advanced backend, the *same* model Perspicacité uses (3072-dim); needs
  ``OPENAI_API_KEY``. The CLI defaults to this when a key is present, else local.

Design constraints (see the operationalize-pipelines plan):

* **Optional dependencies, lazy import.** Both backend builders import their
  package *inside* the function, so this module imports fine without either extra,
  and the pure graph/IO helpers (:func:`related_map`, :func:`embed_skills`,
  :func:`build`) work with any injected embedder.
* **No live model/network in tests.** Every entry point takes an injected
  ``embedder`` (a ``callable(list[str]) -> list[list[float]]``); only the CLI
  reaches for :func:`default_embedder`.
* **Idempotent, indent-preserving writes.** Reuses
  ``propagate_license_tiers.detect_indent`` and writes a file only when its
  serialization changes.
* **No git/gh side effects, no ``Date.now``.**

The real 5,865-skill precompute (``pip install '.[embed]'`` then
``python -m scripts.build_related_skills --collection collections/metabolomics/v2``)
is a maintainer operation. Until it is run, ``related_skills`` is absent and the
``check_related_skills`` gate passes vacuously — which is correct.
"""
from __future__ import annotations

import json
import math
import pathlib

from scripts.propagate_license_tiers import detect_indent
from scripts.skill_match import skill_doc

# Pinned model: small, fast, widely cached. Behind the [embed] extra.
_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Defaults for the similarity graph.
DEFAULT_TOP_N = 8
DEFAULT_THRESHOLD = 0.3


def default_embedder():
    """Return ``embed(texts) -> list[list[float]]`` backed by a pinned model.

    ``sentence-transformers`` is imported here, *not* at module import time, so
    this module loads without the ``[embed]`` extra. Calling this function
    without the extra installed raises ``ImportError`` with install guidance.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as e:  # pragma: no cover - exercised via monkeypatch
        raise ImportError(
            "default_embedder requires the optional 'embed' extra: "
            "pip install '.[embed]'  (sentence-transformers)"
        ) from e

    model = SentenceTransformer(_MODEL_NAME)

    def embed(texts):
        # convert_to_numpy=False keeps a plain list-of-lists return shape.
        vecs = model.encode(list(texts), convert_to_numpy=False)
        return [[float(x) for x in v] for v in vecs]

    return embed


_OPENAI_MODEL = "text-embedding-3-large"


def openai_embedder(model=_OPENAI_MODEL, *, batch_size=256):
    """Return ``embed(texts) -> list[list[float]]`` backed by the OpenAI
    embeddings API (``text-embedding-3-large`` by default — the *same* model
    Perspicacité uses, 3072-dim). Reads ``OPENAI_API_KEY`` from the environment.

    ``openai`` is imported here, *not* at module import time, so this module loads
    without it; calling without the package or a key raises with guidance.
    """
    try:
        from openai import OpenAI
    except ImportError as e:  # pragma: no cover - exercised via monkeypatch
        raise ImportError(
            "openai_embedder requires the optional 'embed-openai' extra: "
            "pip install '.[embed-openai]'  (openai)"
        ) from e
    import os

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("openai_embedder requires OPENAI_API_KEY in the environment")
    client = OpenAI()

    def embed(texts):
        texts = list(texts)
        out: list[list[float]] = []
        for i in range(0, len(texts), batch_size):
            resp = client.embeddings.create(model=model, input=texts[i : i + batch_size])
            out.extend([list(d.embedding) for d in resp.data])
        return out

    return embed


def embedder_for(backend, **kwargs):
    """Resolve a backend name to an embedder.

    ``local`` — pinned MiniLM (offline, no key, lightweight);
    ``openai`` — ``text-embedding-3-large`` (advanced, Perspicacité-aligned, needs
    ``OPENAI_API_KEY``).
    """
    if backend == "local":
        return default_embedder()
    if backend == "openai":
        return openai_embedder(**kwargs)
    raise ValueError(f"unknown embedder backend {backend!r} (use 'local' or 'openai')")


def default_backend():
    """Prefer the advanced OpenAI backend when a key is present, else lightweight local."""
    import os

    return "openai" if os.environ.get("OPENAI_API_KEY") else "local"


def embed_skills(skills_index, *, embedder):
    """Embed each skill's document text into a ``{slug: vector}`` map.

    Text per skill is :func:`skill_match.skill_doc` (name + description + tools +
    EDAM topics + techniques). ``embedder`` is a ``callable(list[str]) ->
    list[list[float]]`` (injected — never the live model in tests). Entries
    without a ``slug`` are skipped.
    """
    entries = [e for e in (skills_index or []) if e.get("slug")]
    if not entries:
        return {}
    docs = [skill_doc(e) for e in entries]
    vectors = embedder(docs)
    return {e["slug"]: list(v) for e, v in zip(entries, vectors)}


def _cosine(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    if dot == 0.0:
        return 0.0
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def related_map(vectors, *, top_n=DEFAULT_TOP_N, threshold=DEFAULT_THRESHOLD):
    """Cosine top-N neighbour graph from a ``{slug: vector}`` map. Pure.

    For each slug, returns the ``top_n`` other slugs with the highest cosine
    similarity that is strictly above ``threshold``, excluding self. Ties in
    similarity are broken by slug ascending (deterministic output). Returns
    ``{slug: [slug, ...]}``.
    """
    slugs = sorted(vectors)
    out: dict[str, list[str]] = {}
    for s in slugs:
        vs = vectors[s]
        scored = []
        for other in slugs:
            if other == s:
                continue
            sim = _cosine(vs, vectors[other])
            if sim > threshold:
                scored.append((sim, other))
        # highest similarity first; tie-break by slug ascending.
        scored.sort(key=lambda p: (-p[0], p[1]))
        out[s] = [slug for _, slug in scored[:top_n]]
    return out


def _load_json(path):
    raw = path.read_text(encoding="utf-8")
    return json.loads(raw), detect_indent(raw)


def _write_json_if_changed(path, obj, indent) -> bool:
    """Write ``obj`` only when the serialization differs. Returns True if written."""
    new = json.dumps(obj, indent=indent, ensure_ascii=False)
    if path.exists() and path.read_text(encoding="utf-8") == new:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def build(collection_dir, *, embedder=None, top_n=DEFAULT_TOP_N,
          threshold=DEFAULT_THRESHOLD) -> dict:
    """Compute + write the ``related_skills`` graph for a collection.

    Embeds every skill in ``skills_index.json`` (via ``embedder``, defaulting to
    :func:`default_embedder` when none is injected), builds the cosine top-N
    graph, and writes each neighbour list into both the ``skills_index.json``
    entry and the matching ``kb_bundle.json['skills'][slug]`` record. Writes are
    indent-preserving and idempotent (a file unchanged in content is not
    rewritten). Returns ``{"count": int, "written": bool}``.
    """
    if embedder is None:
        embedder = default_embedder()

    d = pathlib.Path(collection_dir)
    si_path = d / "skills_index.json"
    kb_path = d / "kb_bundle.json"

    si, si_indent = _load_json(si_path)
    kb, kb_indent = _load_json(kb_path)

    vectors = embed_skills(si, embedder=embedder)
    rel = related_map(vectors, top_n=top_n, threshold=threshold)

    for entry in si:
        slug = entry.get("slug")
        if slug in rel:
            entry["related_skills"] = rel[slug]

    kb_skills = kb.get("skills")
    if isinstance(kb_skills, dict):
        for slug, neighbours in rel.items():
            rec = kb_skills.get(slug)
            if isinstance(rec, dict):
                rec["related_skills"] = neighbours

    wrote_si = _write_json_if_changed(si_path, si, si_indent)
    wrote_kb = _write_json_if_changed(kb_path, kb, kb_indent)

    return {"count": len(rel), "written": bool(wrote_si or wrote_kb)}


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--collection", required=True,
        help="collection root (skills_index.json + kb_bundle.json)",
    )
    ap.add_argument(
        "--top-n", type=int, default=DEFAULT_TOP_N,
        help=f"neighbours per skill (default {DEFAULT_TOP_N})",
    )
    ap.add_argument(
        "--threshold", type=float, default=DEFAULT_THRESHOLD,
        help=f"minimum cosine similarity (default {DEFAULT_THRESHOLD})",
    )
    ap.add_argument(
        "--backend", choices=("local", "openai"), default=None,
        help="embedder: 'local' (MiniLM, offline) or 'openai' (text-embedding-3-large). "
             "Default: openai when OPENAI_API_KEY is set, else local.",
    )
    a = ap.parse_args(argv)

    # A live embedder (model / API) is constructed only here, never in build's
    # importable path or in tests.
    backend = a.backend or default_backend()
    res = build(a.collection, embedder=embedder_for(backend), top_n=a.top_n,
                threshold=a.threshold)
    print(json.dumps({"backend": backend, **res}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
