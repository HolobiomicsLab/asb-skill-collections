import json, pathlib, sys

import yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import check_provenance_tiers as c


def _collection(tmp_path, si_entries, skills=None):
    d = tmp_path / "v"
    (d / "skills").mkdir(parents=True)
    (d / "skills_index.json").write_text(json.dumps(si_entries))
    for slug, fm in (skills or {}).items():
        (d / "skills" / slug).mkdir()
        (d / "skills" / slug / "SKILL.md").write_text(f"---\n{fm}---\nbody\n")
    return d


def test_clean_collection_passes(tmp_path):
    d = _collection(
        tmp_path,
        [{"slug": "s1", "provenance_tier": "literature", "dois": ["10.1/a"]}],
        skills={"s1": "name: s1\nmetadata:\n  provenance_tier: literature\n"},
    )
    assert c.check_collection(str(d)) == []


def test_bad_tier_is_violation(tmp_path):
    d = _collection(
        tmp_path,
        [{"slug": "s1", "provenance_tier": "bogus", "dois": ["10.1/a"]}],
        skills={"s1": "name: s1\nmetadata:\n  provenance_tier: bogus\n"},
    )
    v = c.check_collection(str(d))
    assert any("s1" in x and "provenance_tier" in x for x in v)


def test_literature_without_doi_is_violation(tmp_path):
    d = _collection(
        tmp_path,
        [{"slug": "s1", "provenance_tier": "literature", "dois": []}],
        skills={"s1": "name: s1\nmetadata:\n  provenance_tier: literature\n"},
    )
    v = c.check_collection(str(d))
    assert any("s1" in x and "doi" in x for x in v)


def test_skill_md_mismatch_is_violation(tmp_path):
    d = _collection(
        tmp_path,
        [{"slug": "s1", "provenance_tier": "literature", "dois": ["10.1/a"]}],
        skills={"s1": "name: s1\nmetadata:\n  provenance_tier: synthetic\n"},
    )
    v = c.check_collection(str(d))
    assert any("s1" in x and ("mismatch" in x or "!=" in x) for x in v)


def test_skill_md_missing_tier_is_violation(tmp_path):
    d = _collection(
        tmp_path,
        [{"slug": "s1", "provenance_tier": "literature", "dois": ["10.1/a"]}],
        skills={"s1": "name: s1\nmetadata:\n  license_tier: open\n"},
    )
    v = c.check_collection(str(d))
    assert any("s1" in x and "provenance_tier" in x for x in v)


# --- layout + the repository tier --------------------------------------------

import pytest  # noqa: E402


def _layout_collection(tmp_path, corpus_dir, *, slug="tool-only", tier="repository",
                repo="https://github.com/a/b", fm_tier=None):
    col = tmp_path / "c"
    (col / corpus_dir / slug).mkdir(parents=True)
    meta = {"provenance_tier": fm_tier if fm_tier is not None else tier}
    if repo:
        meta["repo_url"] = repo
    (col / corpus_dir / slug / "SKILL.md").write_text(
        "---\n" + yaml.safe_dump({"name": slug, "metadata": meta}) + "---\nbody\n",
        encoding="utf-8")
    (col / "skills_index.json").write_text(
        json.dumps([{"slug": slug, "dois": [], "provenance_tier": tier}]), encoding="utf-8")
    return col


@pytest.mark.parametrize("corpus_dir", ["skills", "leaves"])
def test_a_repository_tier_skill_passes_in_either_layout(tmp_path, corpus_dir):
    assert c.check_collection(_layout_collection(tmp_path, corpus_dir)) == []


@pytest.mark.parametrize("corpus_dir", ["skills", "leaves"])
def test_a_frontmatter_mismatch_is_caught_in_either_layout(tmp_path, corpus_dir):
    """The cross-check used to glob a hardcoded `skills/`. On a router-shaped
    collection that reaches the two advertised entry points and reports a clean
    pass over every other skill."""
    col = _layout_collection(tmp_path, corpus_dir, tier="repository", fm_tier="literature")
    problems = c.check_collection(col)
    assert any("provenance_tier" in p for p in problems), problems


def test_a_repository_tier_without_a_repo_url_is_rejected(tmp_path):
    col = _layout_collection(tmp_path, "leaves", repo=None)
    assert any("repository requires repo_url" in p for p in c.check_collection(col))
