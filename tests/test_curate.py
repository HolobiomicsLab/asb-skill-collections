"""Tests for scripts/curate.py — the static curation auditor.

Covers the check logic, the two disciplines (None != 0, no domain literals), and
the robustness fixes for malformed inputs (a curation sweep must never crash).
"""
import pathlib
import re
import sys
import tempfile

import pytest

SCRIPTS = pathlib.Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))  # so curate's `import validate_workflows` resolves

import curate  # noqa: E402


# --------------------------------------------------------------------------- #
# check logic                                                                  #
# --------------------------------------------------------------------------- #
def test_leaf_grounding_distinguishes_absent_from_empty():
    idx = [{"slug": "a", "dois": ["10.1/x"]},   # grounded
           {"slug": "b"},                        # no field -> warn (unknown)
           {"slug": "c", "dois": []}]            # empty -> fail (ungrounded)
    r = curate.check_leaf_grounding(idx)
    sev = {f["target"]: f["severity"] for f in r["findings"]}
    assert sev == {"b": "warn", "c": "fail"}
    assert r["status"] == "fail"


def test_oversized_leaf_flags_over_cap():
    idx = [{"slug": "big", "tools": [f"t{i}" for i in range(26)]},
           {"slug": "ok", "tools": ["one"]}]
    r = curate.check_oversized_leaf(idx)
    assert r["n_findings"] == 1 and r["findings"][0]["target"] == "big"


def test_duplicate_leaf_is_two_sided():
    # a & b: identical description + shared tools/DOI -> flagged.
    # c: shares tools/DOI but a distinct description -> NOT flagged (over-fire guard).
    idx = [
        {"slug": "a", "tools": ["T"], "dois": ["10.1/x"], "description": "does a thing"},
        {"slug": "b", "tools": ["T"], "dois": ["10.1/x"], "description": "does a thing"},
        {"slug": "c", "tools": ["T"], "dois": ["10.1/x"], "description": "a wholly different task"},
    ]
    r = curate.check_duplicate_leaf(idx)
    assert r["n_findings"] == 1
    assert "a" in r["findings"][0]["target"] and "b" in r["findings"][0]["target"]


def test_duplicate_leaf_caps_oversized_bucket():
    idx = [{"slug": f"s{i}", "tools": ["T"], "dois": ["10.1/x"], "description": "same text"}
           for i in range(curate._MAX_DUP_BUCKET + 5)]
    r = curate.check_duplicate_leaf(idx)  # must not run the full O(n^2) pairwise
    assert r["n_findings"] == 1 and "manual review" in r["findings"][0]["detail"]


# --------------------------------------------------------------------------- #
# None != 0                                                                    #
# --------------------------------------------------------------------------- #
def test_doi_in_corpus_no_corpus_is_not_applicable():
    idx = [{"slug": "a", "dois": ["10.1/x"]}]
    assert curate.check_doi_in_corpus(idx, set())["status"] == "not_applicable"
    assert curate.check_doi_in_corpus(idx, {"10.1/x"})["status"] == "pass"


def test_norm_doi_strips_resolver_prefix():
    assert curate.norm_doi("https://doi.org/10.1/X") == "10.1/x"
    assert curate.norm_doi("doi:10.2/Y") == "10.2/y"


# --------------------------------------------------------------------------- #
# robustness — a malformed leaf/file must be flagged, never crash the sweep    #
# --------------------------------------------------------------------------- #
def test_non_dict_frontmatter_is_error_not_crash():
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as tf:
        tf.write("---\njust a scalar\n---\nbody\n")
        p = tf.name
    fm, err = curate.read_frontmatter(p)
    pathlib.Path(p).unlink()
    assert fm is None and err == "frontmatter is not a mapping"


def test_string_typed_fields_are_flagged_not_char_counted():
    idx = [{"slug": "m", "dois": "10.1/x", "tools": "abcdefghij"}]
    assert curate.check_leaf_grounding(idx)["status"] == "fail"       # dois not a list
    r = curate.check_oversized_leaf(idx)
    assert r["n_findings"] == 1 and "not a list" in r["findings"][0]["detail"]  # not "10 tools"
    curate.check_doi_in_corpus(idx, {"10.1/x"})                       # must not iterate chars
    curate.check_duplicate_leaf(idx)                                  # must not crash


def test_missing_slug_does_not_crash():
    idx = [{"dois": []}]  # ungrounded AND slug-less
    r = curate.check_leaf_grounding(idx)
    assert r["findings"][0]["target"] == "<missing-slug>"


# --------------------------------------------------------------------------- #
# report assembly                                                              #
# --------------------------------------------------------------------------- #
def test_overall_status_is_worst_and_na_collapses_to_pass():
    warn = curate.result("x", [curate.finding("x", "warn", "t", "d")], 1, 0)
    na = curate.result("y", [], 0, 1, status="not_applicable")
    rep = curate.build_report("d", [na, warn])
    assert rep["overall_status"] == "warn"
    assert curate.build_report("d", [na])["overall_status"] == "pass"
    assert curate.build_report("d", [])["overall_status"] == "pass"


# --------------------------------------------------------------------------- #
# safety invariant #4 — no domain/DOI/id literals in the Forge's own code      #
# --------------------------------------------------------------------------- #
def test_forge_code_has_no_domain_or_id_literals():
    banned = re.compile(r"10\.\d{4,}/\S|MTBLS\d|PXD\d{6}|MSV\d{9}|==\s*[\"']metabolomics[\"']")
    for name in ("curate.py",):
        lines = (SCRIPTS / name).read_text().splitlines()
        offenders = [(i + 1, ln) for i, ln in enumerate(lines)
                     if not ln.lstrip().startswith("#") and banned.search(ln)]
        assert not offenders, f"{name}: domain/id literal in code: {offenders}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
