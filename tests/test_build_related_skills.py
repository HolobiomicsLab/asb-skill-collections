"""Tests for the embedding similarity graph (Task B4).

A FAKE deterministic embedder is used everywhere — NO sentence-transformers
model, NO network. The fake maps each skill's text to a fixed vector keyed by a
sentinel token in the text, so cosine neighbours are known up front.
"""
from __future__ import annotations

import importlib
import json

import pytest

from scripts import build_related_skills as brs
from scripts import check_related_skills as crs


# --------------------------------------------------------------------------- #
# Fake embedder: deterministic vectors picked by a token in the text.
# --------------------------------------------------------------------------- #
# Four 2-D unit-ish vectors. a/b are close (small angle); c is orthogonal to a;
# d is anti-parallel to a (cosine < 0).
_VECTORS = {
    "AAA": [1.0, 0.0],
    "BBB": [0.96, 0.28],   # ~16 deg from AAA  -> cosine ~0.96
    "CCC": [0.0, 1.0],     # orthogonal to AAA -> cosine 0.0
    "DDD": [-1.0, 0.0],    # opposite AAA      -> cosine -1.0
}


def _fake_embed(texts):
    out = []
    for t in texts:
        for token, vec in _VECTORS.items():
            if token in t:
                out.append(list(vec))
                break
        else:  # pragma: no cover - guard, tests always tag their text
            out.append([0.0, 0.0])
    return out


def _index(*pairs):
    """Build a minimal skills_index list. Each pair = (slug, tag-token)."""
    return [
        {"slug": slug, "name": slug, "description": f"desc {tag}", "tools": []}
        for slug, tag in pairs
    ]


# --------------------------------------------------------------------------- #
# related_map — pure cosine top-N.
# --------------------------------------------------------------------------- #
def test_related_map_orders_by_cosine_and_excludes_self_and_below_threshold():
    vectors = {
        "a": _VECTORS["AAA"],
        "b": _VECTORS["BBB"],
        "c": _VECTORS["CCC"],
        "d": _VECTORS["DDD"],
    }
    rel = brs.related_map(vectors, top_n=8, threshold=0.3)
    # a is close to b only (c=0.0 below threshold, d negative)
    assert rel["a"] == ["b"]
    assert rel["b"] == ["a"]
    # c orthogonal to everything -> no neighbours above 0.3
    assert rel["c"] == []
    # never include self
    for slug, neighbours in rel.items():
        assert slug not in neighbours


def test_related_map_respects_top_n():
    # three mutually-close vectors plus one far one
    vectors = {
        "a": [1.0, 0.0],
        "b": [0.99, 0.10],
        "c": [0.98, 0.15],
        "z": [0.0, 1.0],
    }
    rel = brs.related_map(vectors, top_n=1, threshold=0.3)
    assert len(rel["a"]) == 1
    # the single nearest neighbour of a is b (higher cosine than c)
    assert rel["a"] == ["b"]


def test_related_map_slug_tie_break():
    # b and c are at the SAME cosine to a -> tie broken by slug ascending.
    vectors = {
        "a": [1.0, 0.0],
        "c": [0.8, 0.6],
        "b": [0.8, -0.6],
    }
    rel = brs.related_map(vectors, top_n=8, threshold=0.3)
    assert rel["a"] == ["b", "c"]


def test_related_map_empty():
    assert brs.related_map({}, top_n=8, threshold=0.3) == {}


# --------------------------------------------------------------------------- #
# embed_skills — text via skill_match.skill_doc, vectors via injected embedder.
# --------------------------------------------------------------------------- #
def test_embed_skills_uses_injected_embedder():
    idx = _index(("a", "AAA"), ("b", "BBB"))
    vecs = brs.embed_skills(idx, embedder=_fake_embed)
    assert set(vecs) == {"a", "b"}
    assert vecs["a"] == _VECTORS["AAA"]
    assert vecs["b"] == _VECTORS["BBB"]


# --------------------------------------------------------------------------- #
# build — writes related_skills into both indices, indent-preserving + idempotent.
# --------------------------------------------------------------------------- #
def _write_collection(tmp_path, pairs):
    col = tmp_path / "col"
    col.mkdir()
    idx = _index(*pairs)
    (col / "skills_index.json").write_text(
        json.dumps(idx, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    kb = {"collection": "x", "version": 2, "skills": {
        slug: {"dois": [], "tools": []} for slug, _ in pairs
    }}
    (col / "kb_bundle.json").write_text(
        json.dumps(kb, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return col


def test_build_writes_related_skills_into_both_indices(tmp_path):
    col = _write_collection(
        tmp_path, [("a", "AAA"), ("b", "BBB"), ("c", "CCC")]
    )
    res = brs.build(col, embedder=_fake_embed, top_n=8)
    assert res["count"] == 3

    si = json.loads((col / "skills_index.json").read_text())
    by_slug = {e["slug"]: e for e in si}
    assert by_slug["a"]["related_skills"] == ["b"]
    assert by_slug["b"]["related_skills"] == ["a"]
    assert by_slug["c"]["related_skills"] == []

    kb = json.loads((col / "kb_bundle.json").read_text())
    assert kb["skills"]["a"]["related_skills"] == ["b"]
    assert kb["skills"]["c"]["related_skills"] == []


def test_build_is_idempotent(tmp_path):
    col = _write_collection(tmp_path, [("a", "AAA"), ("b", "BBB")])
    brs.build(col, embedder=_fake_embed, top_n=8)
    first_si = (col / "skills_index.json").read_text()
    first_kb = (col / "kb_bundle.json").read_text()

    res2 = brs.build(col, embedder=_fake_embed, top_n=8)
    assert res2["written"] is False
    assert (col / "skills_index.json").read_text() == first_si
    assert (col / "kb_bundle.json").read_text() == first_kb


def test_build_preserves_four_space_indent(tmp_path):
    col = tmp_path / "col"
    col.mkdir()
    idx = _index(("a", "AAA"), ("b", "BBB"))
    (col / "skills_index.json").write_text(
        json.dumps(idx, indent=4, ensure_ascii=False), encoding="utf-8"
    )
    kb = {"skills": {"a": {"dois": []}, "b": {"dois": []}}}
    (col / "kb_bundle.json").write_text(
        json.dumps(kb, indent=4, ensure_ascii=False), encoding="utf-8"
    )
    brs.build(col, embedder=_fake_embed, top_n=8)
    text = (col / "skills_index.json").read_text()
    # a 4-space-indented file keeps 4-space indentation after the write.
    assert '\n        "slug"' in text or '\n    {' in text


# --------------------------------------------------------------------------- #
# default_embedder — lazy import; module must import WITHOUT the extra.
# --------------------------------------------------------------------------- #
def test_module_imports_without_sentence_transformers():
    # Re-importing the module must not require sentence-transformers.
    mod = importlib.reload(importlib.import_module("scripts.build_related_skills"))
    assert hasattr(mod, "default_embedder")
    assert hasattr(mod, "related_map")


def test_default_embedder_is_lazy(monkeypatch):
    # Calling default_embedder() without the extra installed raises a helpful
    # ImportError — but merely importing the module (done above) does not.
    import builtins

    real_import = builtins.__import__

    def _block(name, *args, **kwargs):
        if name == "sentence_transformers" or name.startswith("sentence_transformers."):
            raise ImportError("no sentence_transformers")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _block)
    with pytest.raises(ImportError):
        brs.default_embedder()


# --------------------------------------------------------------------------- #
# check_related_skills gate.
# --------------------------------------------------------------------------- #
def test_gate_passes_on_clean_collection(tmp_path):
    col = _write_collection(tmp_path, [("a", "AAA"), ("b", "BBB"), ("c", "CCC")])
    brs.build(col, embedder=_fake_embed, top_n=8)
    assert crs.check_collection(col) == []


def test_gate_passes_when_field_absent(tmp_path):
    # No related_skills written anywhere -> vacuously clean (real-data state).
    col = _write_collection(tmp_path, [("a", "AAA"), ("b", "BBB")])
    assert crs.check_collection(col) == []


def test_gate_flags_dangling_reference(tmp_path):
    col = _write_collection(tmp_path, [("a", "AAA"), ("b", "BBB")])
    si = json.loads((col / "skills_index.json").read_text())
    for e in si:
        if e["slug"] == "a":
            e["related_skills"] = ["does-not-exist"]
    (col / "skills_index.json").write_text(
        json.dumps(si, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    violations = crs.check_collection(col)
    assert violations
    assert any("does-not-exist" in v for v in violations)


def test_gate_main_exit_codes(tmp_path):
    clean = _write_collection(tmp_path, [("a", "AAA"), ("b", "BBB")])
    brs.build(clean, embedder=_fake_embed, top_n=8)
    assert crs.main([str(clean)]) == 0

    dirty = tmp_path / "dirty"
    dirty.mkdir()
    (dirty / "skills_index.json").write_text(
        json.dumps([{"slug": "a", "related_skills": ["ghost"]}], indent=2),
        encoding="utf-8",
    )
    (dirty / "kb_bundle.json").write_text(
        json.dumps({"skills": {}}, indent=2), encoding="utf-8"
    )
    assert crs.main([str(dirty)]) == 1
