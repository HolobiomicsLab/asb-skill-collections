"""Tests for the skill-matching engine.

Task 1 — serverless lexical core: skill_doc, lexical_match, match_tools,
near_duplicates (operate on in-memory index structures, no network).

Task 2 — Perspicacité KB backend + dispatch: kb_name, build_skills_kb, kb_match,
match_skills. The HTTP client is *injected* (mocked) — no live calls; the
dispatch falls back to the lexical core when the server raises or returns empty.
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


# === Task 2: Perspicacité KB backend + dispatch ===========================
#
# The injected ``http`` mirrors ``perspicacite_kb_bind._http`` —
# a callable ``http(method, path, body=None, timeout=...)`` returning parsed
# JSON (or raising on transport/HTTP error). Tests record calls, never hit the
# network, and exercise the graceful fallback to the lexical core.


class RecordingHttp:
    """A mock ``_http``-shaped client returning canned responses by (method, path).

    ``routes`` maps ``(method, path_prefix)`` to either a value (returned) or a
    callable ``(method, path, body) -> value``. A value that is an ``Exception``
    instance (or subclass) is *raised*. Unmatched routes return ``{}``.
    """

    def __init__(self, routes=None):
        self.routes = routes or {}
        self.calls = []

    def __call__(self, method, path, body=None, timeout=0):
        self.calls.append((method, path, body))
        # most-specific (longest prefix) route wins, so a precise
        # ``/api/kb/<kb>/documents`` route can shadow a broad ``/api/kb`` one
        best = None
        for (m, prefix), resp in self.routes.items():
            if m == method and (path == prefix or path.startswith(prefix + "/")):
                if best is None or len(prefix) > len(best[0]):
                    best = (prefix, resp)
        if best is None:
            return {}
        resp = best[1]
        if callable(resp):
            resp = resp(method, path, body)
        if isinstance(resp, Exception) or (
            isinstance(resp, type) and issubclass(resp, Exception)
        ):
            raise resp if isinstance(resp, Exception) else resp()
        return resp


@pytest.fixture
def collection_dir(tmp_path):
    """A throwaway collection dir with a tiny ``skills_index.json`` for the
    lexical-fallback path. Basename is fixed so ``kb_name`` is predictable."""
    coll = tmp_path / "metabolomics" / "v2"
    coll.mkdir(parents=True)
    (coll / "skills_index.json").write_text(json.dumps(SKILLS_INDEX), encoding="utf-8")
    return coll


# --- kb_name ----------------------------------------------------------------

def test_kb_name_uses_collection_basename(collection_dir):
    assert sm.kb_name(collection_dir) == "asb-skills-v2"


def test_kb_name_strips_trailing_slash():
    # normpath handles a trailing separator so the basename is still 'v2'
    assert sm.kb_name("collections/metabolomics/v2/") == "asb-skills-v2"


# --- build_skills_kb --------------------------------------------------------

def test_build_skills_kb_creates_and_ingests_one_doc_per_skill(collection_dir):
    http = RecordingHttp()
    out = sm.build_skills_kb(collection_dir, http=http)
    assert out["kb"] == "asb-skills-v2"
    assert out["ingested"] == len(SKILLS_INDEX)
    # the KB was created
    assert ("POST", "/api/kb", {"name": "asb-skills-v2", "description": sm.SKILLS_KB_DESC}) in [
        (m, p, b) for (m, p, b) in http.calls
    ] or any(m == "POST" and p == "/api/kb" for (m, p, b) in http.calls)
    # one ingest call per skill, each carrying the slug in metadata
    ingest_calls = [b for (m, p, b) in http.calls if "documents" in p or "/docs" in p]
    assert len(ingest_calls) == len(SKILLS_INDEX)
    ingested_slugs = {b["metadata"]["slug"] for b in ingest_calls}
    assert ingested_slugs == {e["slug"] for e in SKILLS_INDEX}
    # the doc text folds in the searchable fields
    rt_doc = next(b for b in ingest_calls if b["metadata"]["slug"] == "retention-time-alignment")
    assert "chromatographic" in rt_doc["text"]
    assert "xcms" in rt_doc["text"]


def test_build_skills_kb_tolerates_existing_kb(collection_dir):
    import urllib.error

    def create(method, path, body):
        raise urllib.error.HTTPError(path, 409, "exists", {}, None)

    http = RecordingHttp({
        ("POST", "/api/kb"): create,                          # create → 409
        ("POST", "/api/kb/asb-skills-v2/documents"): {},       # ingest → ok
    })
    # 409 on create (KB already exists) must not abort ingest
    out = sm.build_skills_kb(collection_dir, http=http)
    assert out["ingested"] == len(SKILLS_INDEX)


# --- kb_match ---------------------------------------------------------------

def test_kb_match_maps_hits_to_slug_score_backend(collection_dir):
    canned = {
        "results": [
            {"metadata": {"slug": "retention-time-alignment"}, "score": 0.91},
            {"metadata": {"slug": "retention-time-drift-correction"}, "score": 0.74},
        ]
    }
    http = RecordingHttp({("POST", "/api/kb/asb-skills-v2"): canned})
    hits = sm.kb_match("align retention time", collection_dir, k=5, http=http)
    assert hits == [
        {"slug": "retention-time-alignment", "score": 0.91, "backend": "kb"},
        {"slug": "retention-time-drift-correction", "score": 0.74, "backend": "kb"},
    ]
    # query was scoped to the skills KB
    assert any(p.startswith("/api/kb/asb-skills-v2") for (m, p, b) in http.calls)


def test_kb_match_respects_k(collection_dir):
    canned = {"results": [{"metadata": {"slug": f"s{i}"}, "score": 1.0 - i * 0.1} for i in range(5)]}
    http = RecordingHttp({("POST", "/api/kb"): canned})
    hits = sm.kb_match("anything", collection_dir, k=2, http=http)
    assert len(hits) == 2


def test_kb_match_empty_when_no_hits(collection_dir):
    http = RecordingHttp({("POST", "/api/kb"): {"results": []}})
    assert sm.kb_match("anything", collection_dir, k=5, http=http) == []


# --- match_skills dispatch --------------------------------------------------

def test_match_skills_uses_kb_when_http_returns_hits(collection_dir):
    canned = {
        "results": [
            {"metadata": {"slug": "spectral-library-matching"}, "score": 0.88},
        ]
    }
    http = RecordingHttp({("POST", "/api/kb"): canned})
    hits = sm.match_skills("spectral library cosine", collection_dir, http=http)
    assert hits
    assert hits[0]["backend"] == "kb"
    assert hits[0]["slug"] == "spectral-library-matching"


def test_match_skills_falls_back_to_lexical_when_http_raises(collection_dir):
    import urllib.error

    def boom(method, path, body):
        raise urllib.error.URLError("Connection refused")

    http = RecordingHttp({("POST", "/api/kb"): boom})
    hits = sm.match_skills(
        "align retention time across LC-MS chromatographic runs",
        collection_dir,
        http=http,
    )
    assert hits, "lexical fallback must still return matches"
    assert all(h["backend"] == "lexical" for h in hits)
    assert hits[0]["slug"] == "retention-time-alignment"


def test_match_skills_falls_back_to_lexical_when_kb_empty(collection_dir):
    http = RecordingHttp({("POST", "/api/kb"): {"results": []}})
    hits = sm.match_skills(
        "spectral library cosine annotation", collection_dir, http=http
    )
    # empty KB result is treated as "no signal" → lexical takes over
    assert hits
    assert all(h["backend"] == "lexical" for h in hits)
    assert hits[0]["slug"] == "spectral-library-matching"


def test_match_skills_lexical_when_no_http(collection_dir):
    hits = sm.match_skills(
        "align retention time chromatographic", collection_dir, http=None
    )
    assert hits
    assert all(h["backend"] == "lexical" for h in hits)


def test_match_skills_never_raises_on_broken_collection(tmp_path):
    # no skills_index.json, no server → must return [] rather than raise
    empty = tmp_path / "empty"
    empty.mkdir()
    assert sm.match_skills("anything", empty, http=None) == []
