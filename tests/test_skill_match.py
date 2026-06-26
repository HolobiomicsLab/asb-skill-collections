"""Tests for the skill-matching engine (serverless lexical core).

skill_doc, lexical_match, match_tools, near_duplicates operate on in-memory
index structures with no network; match_skills is the collection-level entry
point that ranks a query against ``skills_index.json`` lexically. (Skill
matching is lexical by design — Perspicacité is used for the separate
literature-grounding step, not skill↔skill matching.)
"""
import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import skill_match as sm


# --- tiny in-memory fixtures (shape mirrors skills_index.json / tools_index.json) ---

SKILLS_INDEX = [
    {
        "slug": "retention-time-alignment",
        "name": "retention-time-alignment",
        "description": (
            "Use when you need to align chromatographic retention time across "
            "LC-MS samples so the same feature lines up between runs."
        ),
        "edam_topics": ["http://edamontology.org/topic_3172"],
        "tools": ["xcms"],
        "techniques": ["LC-MS"],
        "tools_used": ["xcms"],
    },
    {
        "slug": "retention-time-drift-correction",
        "name": "retention-time-drift-correction",
        "description": (
            "Use when retention time drifts across a long LC-MS batch and you "
            "want to correct chromatographic alignment using anchor features."
        ),
        "edam_topics": ["http://edamontology.org/topic_3172"],
        "tools": ["xcms"],
        "techniques": ["LC-MS"],
        "tools_used": ["xcms"],
    },
    {
        "slug": "spectral-library-matching",
        "name": "spectral-library-matching",
        "description": (
            "Use when annotating MS/MS spectra by cosine similarity against a "
            "reference spectral library to assign compound identities."
        ),
        "edam_topics": ["http://edamontology.org/topic_3520"],
        "tools": ["matchms"],
        "techniques": ["MS/MS"],
        "tools_used": ["matchms"],
    },
]

TOOLS_INDEX = [
    {"slug": "xcms", "name": "xcms", "used_by_skills": ["retention-time-alignment"]},
    {"slug": "matchms", "name": "matchms", "used_by_skills": ["spectral-library-matching"]},
    {"slug": "mzmine", "name": "MZmine", "used_by_skills": []},
]


# --- skill_doc --------------------------------------------------------------

def test_skill_doc_joins_searchable_fields():
    doc = sm.skill_doc(SKILLS_INDEX[0])
    assert "retention-time-alignment" in doc
    assert "chromatographic" in doc
    # tools, edam topics, techniques are folded in
    assert "xcms" in doc
    assert "topic_3172" in doc
    assert "LC-MS" in doc


def test_skill_doc_tolerates_missing_fields():
    # a sparse entry must not raise and must include what's present
    doc = sm.skill_doc({"slug": "x", "name": "x"})
    assert "x" in doc
    assert isinstance(doc, str)


# --- lexical_match ----------------------------------------------------------

def test_lexical_match_ranks_obviously_related_first():
    text = (
        "I need to align retention time across my LC-MS runs so the same "
        "chromatographic feature matches between samples."
    )
    hits = sm.lexical_match(text, SKILLS_INDEX, k=3)
    assert hits, "expected at least one hit"
    assert hits[0]["slug"] == "retention-time-alignment"
    # the unrelated spectral-matching skill must not outrank the RT skills
    top_two = {h["slug"] for h in hits[:2]}
    assert "retention-time-drift-correction" in top_two


def test_lexical_match_shape_and_backend_tag():
    hits = sm.lexical_match("spectral library cosine annotation", SKILLS_INDEX, k=10)
    assert hits[0]["slug"] == "spectral-library-matching"
    h = hits[0]
    assert set(h) == {"slug", "score", "backend"}
    assert h["backend"] == "lexical"
    assert isinstance(h["score"], float)
    assert h["score"] > 0


def test_lexical_match_respects_k():
    hits = sm.lexical_match("retention time chromatographic LC-MS spectral", SKILLS_INDEX, k=1)
    assert len(hits) == 1


def test_lexical_match_scores_sorted_descending():
    hits = sm.lexical_match("retention time alignment chromatographic", SKILLS_INDEX, k=10)
    scores = [h["score"] for h in hits]
    assert scores == sorted(scores, reverse=True)


def test_lexical_match_no_overlap_returns_empty():
    hits = sm.lexical_match("zzqq totally unrelated tokens foobar", SKILLS_INDEX, k=10)
    assert hits == []


# --- match_tools ------------------------------------------------------------

def test_match_tools_unions_tools_used_of_matched_skills():
    res = sm.match_tools(
        ["retention-time-alignment", "spectral-library-matching"],
        SKILLS_INDEX,
        TOOLS_INDEX,
    )
    slugs = {r["slug"] for r in res}
    assert "xcms" in slugs
    assert "matchms" in slugs
    for r in res:
        assert set(r) == {"slug", "score"}


def test_match_tools_adds_lexical_tool_name_hits_from_text():
    # text mentions MZmine by name → its slug should surface even though no
    # matched skill uses it
    res = sm.match_tools(
        ["retention-time-alignment"],
        SKILLS_INDEX,
        TOOLS_INDEX,
        text="processed with MZmine and xcms",
    )
    slugs = {r["slug"] for r in res}
    assert "xcms" in slugs       # from the matched skill's tools_used
    assert "mzmine" in slugs     # from the lexical tool-name hit in text


def test_match_tools_dedupes_and_handles_empty():
    assert sm.match_tools([], SKILLS_INDEX, TOOLS_INDEX) == []
    # same tool reached via union + text should not duplicate
    res = sm.match_tools(
        ["retention-time-alignment"],
        SKILLS_INDEX,
        TOOLS_INDEX,
        text="xcms xcms xcms",
    )
    assert [r["slug"] for r in res].count("xcms") == 1


# --- near_duplicates --------------------------------------------------------

def test_near_duplicates_default_threshold_flags_nothing():
    candidates = [
        {"slug": "a", "score": 0.9},
        {"slug": "b", "score": 0.1},
    ]
    assert sm.near_duplicates(candidates) == []


def test_near_duplicates_threshold_selects_above():
    candidates = [
        {"slug": "retention-time-alignment", "score": 0.92},
        {"slug": "retention-time-drift-correction", "score": 0.61},
        {"slug": "spectral-library-matching", "score": 0.10},
    ]
    flagged = sm.near_duplicates(candidates, threshold=0.6)
    assert flagged == ["retention-time-alignment", "retention-time-drift-correction"]


def test_near_duplicates_threshold_is_strict_greater():
    candidates = [{"slug": "a", "score": 0.5}, {"slug": "b", "score": 0.51}]
    # exactly-at-threshold is excluded; only strictly-greater is flagged
    assert sm.near_duplicates(candidates, threshold=0.5) == ["b"]


# === match_skills — collection-level lexical matching =======================
#
# Skill-similarity matching is intentionally lexical (Perspicacité is a paper
# RAG system, used elsewhere for literature grounding — not skill↔skill
# matching). These tests exercise the collection-level entry point over a real
# ``skills_index.json``.


@pytest.fixture
def collection_dir(tmp_path):
    """A throwaway collection dir with a tiny ``skills_index.json``."""
    coll = tmp_path / "metabolomics" / "v2"
    coll.mkdir(parents=True)
    (coll / "skills_index.json").write_text(json.dumps(SKILLS_INDEX), encoding="utf-8")
    return coll


def test_match_skills_ranks_lexically_over_the_index(collection_dir):
    hits = sm.match_skills("align retention time chromatographic", collection_dir)
    assert hits
    assert all(h["backend"] == "lexical" for h in hits)
    assert hits[0]["slug"] == "retention-time-alignment"


def test_match_skills_respects_k(collection_dir):
    hits = sm.match_skills("spectral library cosine annotation", collection_dir, k=1)
    assert len(hits) <= 1


def test_match_skills_never_raises_on_broken_collection(tmp_path):
    # no skills_index.json, no server → must return [] rather than raise
    empty = tmp_path / "empty"
    empty.mkdir()
    assert sm.match_skills("anything", empty) == []
