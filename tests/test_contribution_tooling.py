"""Tests for the contribution-loop tooling:

  * make_improvement_report.scrub      — PII/secret/path redaction (two-sided)
  * select_release_coauthors           — leaderboard -> proposed authors + --apply
  * regen_career_stats rank/external   — numeric rank + external_reviews fields
  * build_leaf_embedding_cache         — align path (drop stale / report missing)
"""
import json
import pathlib
import shutil
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


# --------------------------------------------------------------------------- #
# make_improvement_report.scrub                                                #
# --------------------------------------------------------------------------- #
def test_scrub_redacts_all_categories():
    from scripts.make_improvement_report import scrub

    dirty = (
        "see /Users/jane/data/run.mzML and C:\\Users\\bob\\x and /etc/passwd "
        "email jane@lab.org host 10.0.0.5 token=sk-abcdef0123456789abcd "
        "key=SUPERSECRETVALUE password: hunter2"
    )
    clean, counts = scrub(dirty)
    assert "jane@lab.org" not in clean
    assert "10.0.0.5" not in clean
    assert "/Users/jane" not in clean and "jane" not in clean  # username gone with path
    assert "C:\\Users\\bob" not in clean
    assert "/etc/passwd" not in clean
    assert "sk-abcdef0123456789abcd" not in clean
    assert "SUPERSECRETVALUE" not in clean
    assert "hunter2" not in clean
    assert counts.get("email") == 1
    assert counts.get("ip") == 1
    assert counts.get("path", 0) >= 3
    assert counts.get("secret", 0) >= 3


def test_scrub_leaves_clean_text_untouched():
    from scripts.make_improvement_report import scrub

    clean_in = (
        "The default ppm tolerance in step 3 is too tight for Orbitrap data; "
        "the source paper (DOI 10.1234/abc.def, EDAM operation_3215 via "
        "http://edamontology.org/operation_3215) recommends 10 ppm. A key insight "
        "is that resolution matters."
    )
    out, counts = scrub(clean_in)
    assert out == clean_in
    assert counts == {}


def test_scrub_underscore_prefixed_keys_and_token_shapes():
    """Regression: \\b before an underscore-glued key did NOT match, leaking
    ANTHROPIC_API_KEY / GITHUB_TOKEN etc. (adversarial-review MUST-FIX)."""
    from scripts.make_improvement_report import scrub

    dirty = (
        "export ANTHROPIC_API_KEY=sk-ant-abc123def456ghi789jkl "
        "GITHUB_TOKEN=ghp_0123456789abcdef0123 "
        "aws AKIAIOSFODNN7EXAMPLE my_secret_key: hunter2pass"
    )
    clean, counts = scrub(dirty)
    for leak in ["sk-ant-abc123def456ghi789jkl", "ghp_0123456789abcdef0123",
                 "AKIAIOSFODNN7EXAMPLE", "hunter2pass"]:
        assert leak not in clean, f"leaked: {leak}"
    assert counts.get("secret", 0) >= 4


def test_scrub_no_redos_on_long_blob():
    """A long no-delimiter blob (pasted diff/base64) must not hang the scrubber."""
    import time
    from scripts.make_improvement_report import scrub

    t0 = time.time()
    scrub("a" * 200_000)
    assert time.time() - t0 < 2.0


# --------------------------------------------------------------------------- #
# select_release_coauthors                                                     #
# --------------------------------------------------------------------------- #
@pytest.fixture()
def leaderboard_repo(tmp_path):
    """A repo whose leaderboard is built from the mini contributor fixture."""
    shutil.copy(FIXTURES / "mini_contributors.jsonld", tmp_path / "contributors.jsonld")
    (tmp_path / "leaderboard" / "by-domain").mkdir(parents=True)
    from scripts.regen_career_stats import regen_career_stats

    regen_career_stats(tmp_path)
    return tmp_path


def test_rank_and_external_in_career(leaderboard_repo):
    data = json.loads((leaderboard_repo / "leaderboard" / "career.jsonld").read_text())
    by_login = {c["github"]: c for c in data["contributors"]}
    assert by_login["alice"]["rank"] == 1  # 12 reviews
    assert by_login["bob"]["rank"] == 2    # 3 reviews
    assert by_login["alice"]["external_reviews"] == 10
    assert by_login["bob"]["external_reviews"] == 3


def test_select_coauthors_tier_gate(leaderboard_repo):
    from scripts.select_release_coauthors import select_coauthors

    # Default min_tier=domain_contributor -> bob (reviewer) excluded, alice kept.
    res = select_coauthors(leaderboard_repo, "metabolomics", "domain_contributor", 3, 0, 0)
    logins = [s["github"] for s in res["selected"]]
    assert logins == ["alice"]

    # Lowered to reviewer -> both, ranked by external_reviews desc.
    res2 = select_coauthors(leaderboard_repo, "metabolomics", "reviewer", 1, 0, 0)
    assert [s["github"] for s in res2["selected"]] == ["alice", "bob"]


def test_select_coauthors_collection_scope(leaderboard_repo):
    from scripts.select_release_coauthors import select_coauthors

    res = select_coauthors(leaderboard_repo, "proteomics", "reviewer", 1, 0, 0)
    assert res["selected"] == []  # nobody contributed to proteomics


def test_select_coauthors_empty(tmp_path):
    from scripts.select_release_coauthors import select_coauthors

    res = select_coauthors(tmp_path, None, "reviewer", 1, 0, 0)
    assert res["selected"] == []
    assert "no leaderboard" in res["note"]


def test_apply_citation_and_zenodo_dedup(leaderboard_repo, tmp_path):
    from scripts.select_release_coauthors import (
        _apply_citation,
        _apply_zenodo,
        select_coauthors,
    )

    cff = tmp_path / "CITATION.cff"
    cff.write_text(
        "cff-version: 1.2.0\n"
        "title: Test\n"
        "authors:\n"
        "- name: Core Org\n"
        "- family-names: Lead\n"
        "  given-names: Person\n"
        "  orcid: https://orcid.org/0000-0009-9999-9999\n"
        "keywords:\n"
        "- test\n"
    )
    zen = tmp_path / ".zenodo.json"
    zen.write_text(json.dumps({"creators": [{"name": "Core Org"}]}, indent=2) + "\n")

    res = select_coauthors(leaderboard_repo, "metabolomics", "domain_contributor", 3, 0, 0)
    assert _apply_citation(cff, res["selected"]) == 1   # alice added
    assert _apply_zenodo(zen, res["selected"]) == 1

    import yaml

    doc = yaml.safe_load(cff.read_text())
    orcids = {a.get("orcid", "").rsplit("/", 1)[-1] for a in doc["authors"]}
    assert "0000-0001-0000-0001" in orcids        # alice
    assert "0000-0009-9999-9999" in orcids        # core author preserved
    assert "keywords" in doc and doc["keywords"] == ["test"]  # rest of file intact

    # Idempotent: re-applying adds nobody (dedup by ORCID).
    assert _apply_citation(cff, res["selected"]) == 0
    assert _apply_zenodo(zen, res["selected"]) == 0


def test_apply_citation_indented_block_stays_valid(leaderboard_repo, tmp_path):
    """Regression: yaml.safe_dump emits column-0 items; appending to an INDENTED
    authors block must preserve indentation or the file becomes invalid YAML."""
    import yaml
    from scripts.select_release_coauthors import _apply_citation, select_coauthors

    cff = tmp_path / "CITATION_indented.cff"
    cff.write_text(
        "cff-version: 1.2.0\n"
        "title: Test\n"
        "authors:\n"
        "  - family-names: Lead\n"
        "    given-names: Person\n"
        "    orcid: https://orcid.org/0000-0009-9999-9999\n"
        "version: '2'\n"
    )
    res = select_coauthors(leaderboard_repo, "metabolomics", "domain_contributor", 3, 0, 0)
    assert _apply_citation(cff, res["selected"]) == 1
    doc = yaml.safe_load(cff.read_text())  # must still parse
    assert doc["version"] == "2"
    orcids = {a.get("orcid", "").rsplit("/", 1)[-1] for a in doc["authors"]}
    assert "0000-0001-0000-0001" in orcids and "0000-0009-9999-9999" in orcids


# --------------------------------------------------------------------------- #
# build_leaf_embedding_cache (align path)                                      #
# --------------------------------------------------------------------------- #
def test_build_cache_align_drops_stale_reports_missing(tmp_path):
    np = pytest.importorskip("numpy")
    from scripts.build_leaf_embedding_cache import build_cache

    coll = tmp_path / "collections" / "demo" / "v1"
    coll.mkdir(parents=True)
    # index wants s1, s2; source has s1, s3 (s2 missing, s3 stale).
    (coll / "skills_index.json").write_text(json.dumps([
        {"slug": "s1", "name": "one"}, {"slug": "s2", "name": "two"},
    ]))
    src = tmp_path / "src.npz"
    np.savez(src, emb=np.array([[3.0, 4.0], [1.0, 0.0]], dtype="float32"),
             slug=np.array(["s1", "s3"], dtype=object))

    report = build_cache(coll, "skills", src, None, embed_missing=False)
    assert report["embedded"] == 1
    assert report["missing"] == ["s2"]
    assert report["dropped_stale_from_source"] == 1

    z = np.load(report["output"], allow_pickle=True)
    assert list(z["slug"]) == ["s1"]
    # row was [3,4] -> normalized to unit length
    assert abs(float(np.linalg.norm(z["emb"][0])) - 1.0) < 1e-5
