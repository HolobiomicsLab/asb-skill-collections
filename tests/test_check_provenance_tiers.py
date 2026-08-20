import json, pathlib, sys
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
