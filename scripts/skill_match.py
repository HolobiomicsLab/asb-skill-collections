"""skill_match — match a (possibly ungrounded) candidate skill against the
existing collection's skills and tools.

This module has two halves:

* a **serverless lexical core** (this task) — pure-Python TF-IDF cosine ranking
  over an in-memory ``skills_index``/``tools_index``, plus a near-duplicate flag.
  It depends on nothing external, so a contributor without Perspicacité still
  gets useful ``related_skills`` / ``tools_used`` suggestions;
* a **Perspicacité KB backend + dispatch** layered on top (``kb_name``,
  ``build_skills_kb``, ``kb_match``, ``match_skills``), with the lexical core as
  the graceful fallback. The HTTP transport is injected (same shape as
  ``perspicacite_kb_bind._http``); nothing here touches the network on its own.

The lexical functions never raise on sparse/odd entries and never touch the
network. Each skill is reduced to a single searchable *document* by
:func:`skill_doc` (name + description + tools + EDAM topics + techniques); the
query text is scored against those documents with TF-IDF cosine similarity.
"""
from __future__ import annotations

import json
import math
import os
import re
from collections import Counter
from pathlib import Path

# Tokenizer: lowercase alphanumeric runs, but keep intra-token '-', '/', '_', '.'
# so identifiers like ``LC-MS``, ``MS/MS``, ``topic_3172`` survive as units while
# also yielding their sub-parts (we additionally split on those for recall).
_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9./_-]*")
_SPLIT_RE = re.compile(r"[\s./_-]+")


def _tokenize(text: str) -> list[str]:
    """Tokenize to lowercase terms, emitting both the joined identifier and its
    sub-parts (so ``LC-MS`` matches ``lc-ms`` *and* ``lc``/``ms``)."""
    if not text:
        return []
    low = text.lower()
    toks: list[str] = []
    for m in _TOKEN_RE.findall(low):
        toks.append(m)
        parts = [p for p in _SPLIT_RE.split(m) if p]
        if len(parts) > 1:
            toks.extend(parts)
    return toks


def skill_doc(entry: dict) -> str:
    """Join an index entry's searchable fields into one text document.

    Folds ``name`` + ``description`` + ``tools`` + ``edam_topics`` +
    ``techniques`` (and ``slug`` for good measure). Tolerant of missing keys.
    """
    parts: list[str] = []
    for key in ("slug", "name", "description"):
        val = entry.get(key)
        if isinstance(val, str) and val:
            parts.append(val)
    for key in ("tools", "tools_used", "edam_topics", "techniques"):
        val = entry.get(key)
        if isinstance(val, (list, tuple)):
            parts.extend(str(v) for v in val if v)
        elif isinstance(val, str) and val:
            parts.append(val)
    return " ".join(parts)


def _tf_idf_vectors(docs: list[list[str]]):
    """Return (idf, [tf-idf Counter per doc]) for a corpus of token lists."""
    n = len(docs)
    df: Counter = Counter()
    for toks in docs:
        for term in set(toks):
            df[term] += 1
    idf = {t: math.log((1 + n) / (1 + d)) + 1.0 for t, d in df.items()}
    vecs: list[dict] = []
    for toks in docs:
        tf = Counter(toks)
        total = sum(tf.values()) or 1
        vecs.append({t: (c / total) * idf.get(t, 0.0) for t, c in tf.items()})
    return idf, vecs


def _cosine(a: dict, b: dict) -> float:
    if not a or not b:
        return 0.0
    # iterate the smaller vector
    if len(a) > len(b):
        a, b = b, a
    dot = sum(w * b.get(t, 0.0) for t, w in a.items())
    if dot == 0.0:
        return 0.0
    na = math.sqrt(sum(w * w for w in a.values()))
    nb = math.sqrt(sum(w * w for w in b.values()))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def lexical_match(text: str, skills_index: list[dict], *, k: int = 10) -> list[dict]:
    """Rank ``skills_index`` against ``text`` by TF-IDF cosine similarity.

    Returns up to ``k`` hits ``{slug, score, backend:"lexical"}`` sorted by
    descending score; entries with zero overlap are dropped. Never raises.
    """
    entries = [e for e in (skills_index or []) if e.get("slug")]
    if not entries:
        return []
    doc_tokens = [_tokenize(skill_doc(e)) for e in entries]
    # the query joins the corpus so IDF reflects both query and documents
    query_tokens = _tokenize(text)
    idf, doc_vecs = _tf_idf_vectors(doc_tokens + [query_tokens])
    q_vec = doc_vecs[-1]
    doc_vecs = doc_vecs[:-1]
    scored = []
    for entry, vec in zip(entries, doc_vecs):
        s = _cosine(q_vec, vec)
        if s > 0.0:
            scored.append({"slug": entry["slug"], "score": float(s), "backend": "lexical"})
    scored.sort(key=lambda h: (-h["score"], h["slug"]))
    return scored[:k]


def match_tools(
    matched_slugs: list[str],
    skills_index: list[dict],
    tools_index: list[dict],
    text: str | None = None,
) -> list[dict]:
    """Suggest tool slugs for a candidate skill.

    Union of (a) the ``tools_used`` of every matched skill and (b) lexical
    tool-name hits when ``text`` is supplied (a tool whose slug or name appears
    as a token in ``text``). Returns deduped ``{slug, score}`` ordered by score
    then slug; score 1.0 for a direct text/name hit, 0.5 for a union-only hit.
    """
    by_slug = {e["slug"]: e for e in (skills_index or []) if e.get("slug")}
    tools = [t for t in (tools_index or []) if t.get("slug")]
    scores: dict[str, float] = {}

    # (a) union of matched skills' tools_used
    for slug in matched_slugs or []:
        entry = by_slug.get(slug)
        if not entry:
            continue
        for tool_slug in entry.get("tools_used") or []:
            if tool_slug:
                scores[tool_slug] = max(scores.get(tool_slug, 0.0), 0.5)

    # (b) lexical tool-name hits in the supplied text
    if text:
        text_tokens = set(_tokenize(text))
        for t in tools:
            names = {t["slug"]} | set(_tokenize(t.get("name") or ""))
            names |= set(_tokenize(t["slug"]))
            if text_tokens & names:
                scores[t["slug"]] = 1.0

    res = [{"slug": s, "score": float(sc)} for s, sc in scores.items()]
    res.sort(key=lambda r: (-r["score"], r["slug"]))
    return res


def near_duplicates(candidates: list[dict], *, threshold: float = 0.0) -> list[str]:
    """Slugs of candidates whose score is strictly greater than ``threshold``.

    The caller sets the threshold to decide what counts as "too close, annotate
    or merge instead of adding a new skill". The default (``0.0``) is a no-op
    that flags nothing — near-duplicate detection is opt-in by passing a
    positive threshold. Order is preserved from ``candidates``.
    """
    if threshold <= 0.0:
        return []
    out: list[str] = []
    for c in candidates or []:
        slug = c.get("slug")
        score = c.get("score")
        if slug is None or score is None:
            continue
        if float(score) > threshold:
            out.append(slug)
    return out


# ===========================================================================
# Perspicacité KB backend + dispatch (Task 2)
#
# Layered on top of the lexical core: query an ``asb-skills-<collection>`` KB in
# a running Perspicacité instance for semantic matches, falling back to the
# serverless lexical core whenever the server is unreachable or returns nothing.
#
# The ``http`` parameter is the *injected* transport — same shape as
# ``perspicacite_kb_bind._http``: ``http(method, path, body=None, timeout=...)``
# returning parsed JSON (or raising on transport/HTTP error). Production callers
# pass ``perspicacite_kb_bind._http``; tests pass a recording mock. Nothing here
# touches the network on its own.
# ===========================================================================

SKILLS_KB_DESC = "ASB skills index for community-contribution matching."


def kb_name(collection_dir) -> str:
    """The Perspicacité KB slug for a collection: ``asb-skills-<basename>``.

    The basename is the final path component (``collections/metabolomics/v2`` →
    ``v2`` → ``asb-skills-v2``); a trailing separator is tolerated.
    """
    base = os.path.basename(os.path.normpath(str(collection_dir)))
    return f"asb-skills-{base}"


def _load_skills_index(collection_dir) -> list[dict]:
    """Load ``skills_index.json`` for the lexical fallback. Never raises —
    a missing/garbled file yields an empty index (callers degrade to no hits)."""
    p = Path(str(collection_dir)) / "skills_index.json"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(data, dict):
        # tolerate a wrapped {"skills": [...]} shape
        data = data.get("skills") or data.get("entries") or []
    return data if isinstance(data, list) else []


def build_skills_kb(collection_dir, *, http) -> dict:
    """Idempotently create the skills KB and ingest one document per skill.

    Creates ``asb-skills-<collection>`` (tolerating an already-present KB:
    HTTP 400/409 on create is ignored), then POSTs one document per skill —
    text = :func:`skill_doc` (name + description + tools + EDAM + techniques),
    metadata ``{"slug": <slug>}`` — so retrieval maps a hit straight back to a
    skill. Returns ``{"kb": <slug>, "ingested": <count>}``.
    """
    name = kb_name(collection_dir)
    # create (idempotent: an existing KB returns 400/409, which we swallow)
    try:
        http("POST", "/api/kb", {"name": name, "description": SKILLS_KB_DESC}, timeout=60)
    except Exception as e:  # noqa: BLE001
        code = getattr(e, "code", None)
        if code is not None and code not in (400, 409):
            raise
    ingested = 0
    for entry in _load_skills_index(collection_dir):
        slug = entry.get("slug")
        if not slug:
            continue
        http(
            "POST",
            f"/api/kb/{name}/documents",
            {"text": skill_doc(entry), "metadata": {"slug": slug}},
            timeout=120,
        )
        ingested += 1
    return {"kb": name, "ingested": ingested}


def _hit_slug(hit: dict):
    """Pull the skill slug out of a KB hit (tolerant of response shapes)."""
    meta = hit.get("metadata") if isinstance(hit.get("metadata"), dict) else {}
    return meta.get("slug") or hit.get("slug") or hit.get("id")


def _hit_score(hit: dict) -> float:
    for key in ("score", "similarity", "relevance"):
        v = hit.get(key)
        if isinstance(v, (int, float)):
            return float(v)
    # a distance (lower = closer) folded to a similarity-like score
    d = hit.get("distance")
    if isinstance(d, (int, float)):
        return float(1.0 / (1.0 + d))
    return 0.0


def kb_match(text: str, collection_dir, *, k: int = 10, http) -> list[dict]:
    """Query the skills KB and map hits to ``{slug, score, backend:"kb"}``.

    Scopes the search to ``asb-skills-<collection>`` and returns up to ``k``
    hits, best first. Hits without a resolvable slug are dropped. Raises only if
    ``http`` raises (the caller — :func:`match_skills` — handles that)."""
    name = kb_name(collection_dir)
    resp = http("POST", f"/api/kb/{name}/search", {"query": text, "k": k}, timeout=120)
    hits = []
    if isinstance(resp, dict):
        hits = resp.get("results") or resp.get("hits") or resp.get("matches") or []
    elif isinstance(resp, list):
        hits = resp
    out: list[dict] = []
    for h in hits:
        if not isinstance(h, dict):
            continue
        slug = _hit_slug(h)
        if not slug:
            continue
        out.append({"slug": slug, "score": _hit_score(h), "backend": "kb"})
    return out[:k]


def match_skills(text: str, collection_dir, *, k: int = 10, http=None) -> list[dict]:
    """Match ``text`` against the collection's skills, KB-first with a lexical
    fallback.

    When ``http`` is provided, try the Perspicacité KB backend
    (:func:`kb_match`). On **any** exception (server unreachable, HTTP error,
    odd payload) *or* an empty result, fall back to the serverless lexical core
    (:func:`lexical_match` over ``skills_index.json``). Always returns a list and
    never raises — a contributor without a server still gets suggestions, and a
    broken collection yields ``[]``.
    """
    if http is not None:
        try:
            hits = kb_match(text, collection_dir, k=k, http=http)
            if hits:
                return hits
        except Exception:  # noqa: BLE001 — graceful degrade to lexical
            pass
    return lexical_match(text, _load_skills_index(collection_dir), k=k)
