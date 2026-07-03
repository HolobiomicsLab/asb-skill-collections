"""Tests for scripts/skill_map.py — the embedding-space coverage + island map.

Covers the coverage-relative island logic (two-sided: a covered cluster is NOT
an island), the two disciplines (None != 0, no domain literals), centrality, and
the graceful degradation when a cache or workflows dir is absent.
"""
import os
import pathlib
import re
import sys
import tempfile

import numpy as np
import pytest

SCRIPTS = pathlib.Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import skill_map as sm  # noqa: E402


# --------------------------------------------------------------------------- #
# synthetic embedding fixture: three well-separated clusters of 6 leaves       #
# --------------------------------------------------------------------------- #
def _fixture():
    rng = np.random.default_rng(1)
    dim = 32
    centres = np.eye(3, dim)
    slugs, rows, index = [], [], []
    for cl in range(3):
        for k in range(6):
            slug = f"c{cl}_{k}"
            slugs.append(slug)
            rows.append(centres[cl] + 0.01 * rng.standard_normal(dim))
            index.append({"slug": slug, "tools": [f"tool{cl}"], "techniques": [f"tech{cl}"],
                          "dois": ["10.1/x"], "description": f"cluster {cl} leaf {k}"})
    X, aligned = sm.align_to_index(np.asarray(rows, dtype=np.float32), slugs,
                                   [r["slug"] for r in index])
    return index, X, aligned


# --------------------------------------------------------------------------- #
# alignment + graph primitives                                                 #
# --------------------------------------------------------------------------- #
def test_align_keeps_only_index_slugs_and_normalises():
    emb = np.array([[3.0, 4.0], [1.0, 0.0]], dtype=np.float32)
    X, slugs = sm.align_to_index(emb, ["keep", "drop"], ["keep"])
    assert slugs == ["keep"]
    assert np.isclose(np.linalg.norm(X[0]), 1.0)


def test_knn_graph_excludes_self_and_sorts():
    _, X, _ = _fixture()
    idx, sim = sm.knn_graph(X, 5)
    assert idx.shape == (18, 5)
    assert all(i not in idx[i] for i in range(18))           # never own neighbour
    assert np.all(sim[:, :-1] >= sim[:, 1:] - 1e-6)          # nearest-first


def test_knn_graph_no_self_leak_with_antipodal_pair():
    # A genuine cosine of exactly -1 must not collide with the diagonal sentinel.
    X = np.array([[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    idx, _ = sm.knn_graph(X, 2)
    assert 1 not in idx[1]                                   # self excluded
    assert 0 in idx[1]                                       # true antipodal neighbour kept


def test_mutual_knn_components_separates_clusters():
    _, X, _ = _fixture()
    idx, sim = sm.knn_graph(X, 5)
    comps = sm.mutual_knn_components(idx, sim, 0.5)
    assert len([c for c in comps if len(c) >= 5]) == 3       # three clusters recovered


# --------------------------------------------------------------------------- #
# coverage-relative islands — two-sided                                        #
# --------------------------------------------------------------------------- #
def test_covered_cluster_is_not_an_island():
    index, X, aligned = _fixture()
    by_slug = {r["slug"]: r for r in index}
    covered = sm.covered_indices(aligned, [("w0", {f"c0_{k}" for k in range(6)})])
    islands = sm.find_islands(X, aligned, by_slug, covered,
                              island_sim=0.5, link_sim=0.5, knn=5)
    techs = {t for isl in islands for t in isl["top_techniques"]}
    assert techs == {"tech1", "tech2"}                       # only uncovered clusters


def test_no_coverage_makes_islands_not_zero():
    index, X, aligned = _fixture()
    by_slug = {r["slug"]: r for r in index}
    assert sm.coverage_distance(X, set()) is None
    assert sm.find_islands(X, aligned, by_slug, set(),
                           island_sim=0.5, link_sim=0.5, knn=5) is None


def test_full_coverage_is_known_empty_not_unknown():
    index, X, aligned = _fixture()
    by_slug = {r["slug"]: r for r in index}
    covered = sm.covered_indices(aligned, [("w", set(aligned))])
    islands = sm.find_islands(X, aligned, by_slug, covered,
                              island_sim=0.5, link_sim=0.5, knn=5)
    assert islands == []                                     # known-covered, not None


# --------------------------------------------------------------------------- #
# centrality                                                                   #
# --------------------------------------------------------------------------- #
def test_hub_in_degree_counts_incoming():
    idx = np.array([[1, 2], [0, 2], [0, 1]])
    deg = sm.hub_in_degree(idx)
    assert deg[0] == 2 and deg[1] == 2 and deg[2] == 2


def test_core_closeness_ranks_central_leaf_first():
    X = np.array([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]], dtype=np.float32)
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    close = sm.core_closeness(X)
    assert np.argmax(close) in (0, 1)                        # not the outlier


# --------------------------------------------------------------------------- #
# workflow parsing + coverage block                                            #
# --------------------------------------------------------------------------- #
def test_parse_workflow_coverage_reads_step_skills():
    with tempfile.TemporaryDirectory() as d:
        wf = os.path.join(d, "wf1")
        os.makedirs(wf)
        with open(os.path.join(wf, "workflow.yaml"), "w") as fh:
            fh.write("steps:\n- id: a\n  skills:\n  - x\n  - y\n- id: b\n  skills:\n  - z\n")
        sets = sm.parse_workflow_coverage(d)
    assert sets == [("wf1", {"x", "y", "z"})]


def test_malformed_workflow_yaml_is_skipped_not_crash():
    with tempfile.TemporaryDirectory() as d:
        for name, body in [("w1", "- just\n- a list\n"),          # top-level list
                           ("w2", "steps: notalist\n"),           # steps not a list
                           ("w3", "steps:\n- id: a\n  skills: x\n"),  # skills a string
                           ("w4", "steps:\n- id: b\n  skills:\n  - keep\n")]:
            os.makedirs(os.path.join(d, name))
            with open(os.path.join(d, name, "workflow.yaml"), "w") as fh:
                fh.write(body)
        sets = sm.parse_workflow_coverage(d)
    assert sets == [("w4", {"keep"})]                              # only the valid one


def test_string_typed_leaf_fields_are_not_char_counted():
    slugs = ["a", "b"]
    by_slug = {"a": {"tools": "abcdef"}, "b": {"tools": ["real-tool"]}}
    counts = sm._top_counts([0, 1], by_slug, slugs, "tools", 4)
    assert counts == ["real-tool"]                                 # string ignored, list counted


def test_coverage_block_not_applicable_without_workflows():
    assert sm._coverage_block(["a", "b"], set(), [])["status"] == "not_applicable"
    ok = sm._coverage_block(["a", "b"], {0}, [("w", {"a"})])
    assert ok["status"] == "ok" and ok["pct"] == 50.0


# --------------------------------------------------------------------------- #
# findings — None != 0 and no silent percolation                              #
# --------------------------------------------------------------------------- #
def test_alignment_gap_warns():
    f = sm.map_findings({"n_aligned": 9, "n_leaves_index": 10})
    assert f and f[0]["check"] == "alignment" and f[0]["severity"] == "warn"


def test_giant_island_is_flagged_percolation():
    body = {"n_aligned": 100, "n_leaves_index": 100,
            "islands": [{"size": 40, "exemplar": "x"}]}
    assert any(f["check"] == "percolation" for f in sm.map_findings(body))


def test_dangling_super_skill_references_warn():
    body = {"n_aligned": 10, "n_leaves_index": 10,
            "coverage": {"status": "ok", "covered": 0, "n_workflows": 2, "pct": 0.0}}
    assert any(f["check"] == "coverage" for f in sm.map_findings(body))


def test_non_list_index_is_fail_not_crash():
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "skills_index.json"), "w") as fh:
            fh.write('{"leaves": [{"slug": "a"}]}')          # dict, not a list
        rep = sm.run(d, os.path.join(d, "nope.npz"), os.path.join(d, "wf"),
                     15, 0.55, 0.72, 15, False)
    assert rep["overall_status"] == "fail"
    assert rep["findings"][0]["check"] == "index" and "n_aligned" not in rep


def test_missing_cache_report_is_loud_not_applicable():
    rep = sm.build_report("d", None, "not_applicable",
                          [sm.finding("cache", "warn", "x", "missing")])
    assert rep["overall_status"] == "not_applicable" and "n_aligned" not in rep


def test_norm_doi_strips_resolver_prefix():
    assert sm.norm_doi("https://doi.org/10.1/X") == "10.1/x"


# --------------------------------------------------------------------------- #
# safety invariant #4 — no domain/DOI/id literals in the Forge's own code      #
# --------------------------------------------------------------------------- #
def test_forge_code_has_no_domain_or_id_literals():
    banned = re.compile(r"10\.\d{4,}/\S|MTBLS\d|PXD\d{6}|MSV\d{9}|==\s*[\"']metabolomics[\"']")
    lines = (SCRIPTS / "skill_map.py").read_text().splitlines()
    offenders = [(i + 1, ln) for i, ln in enumerate(lines)
                 if not ln.lstrip().startswith("#") and banned.search(ln)]
    assert not offenders, f"skill_map.py: domain/id literal in code: {offenders}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
