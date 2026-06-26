import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import check_tools_index as c


def _collection(tmp_path, tools_index, skills_index):
    d = tmp_path / "v"
    d.mkdir(parents=True)
    (d / "tools_index.json").write_text(json.dumps(tools_index))
    (d / "skills_index.json").write_text(json.dumps(skills_index))
    return d


def test_clean_collection_passes(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[
            {"slug": "t1", "license_tier": "open", "used_by_skills": ["s1"]},
            {"slug": "t2", "license_tier": "restricted", "used_by_skills": []},
        ],
        skills_index=[
            {"slug": "s1", "tools_used": ["t1"]},
            {"slug": "s2", "tools_used": []},
        ],
    )
    assert c.check_collection(str(d)) == []


def test_bad_tool_tier_is_violation(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[
            {"slug": "t1", "license_tier": "bogus", "used_by_skills": []},
        ],
        skills_index=[
            {"slug": "s1", "tools_used": []},
        ],
    )
    v = c.check_collection(str(d))
    assert any("t1" in x and "license_tier" in x for x in v)


def test_missing_tool_tier_is_violation(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[
            {"slug": "t1", "used_by_skills": []},
        ],
        skills_index=[],
    )
    v = c.check_collection(str(d))
    assert any("t1" in x and "license_tier" in x for x in v)


def test_dangling_tools_used_ref_is_violation(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[
            {"slug": "t1", "license_tier": "open", "used_by_skills": []},
        ],
        skills_index=[
            {"slug": "s1", "tools_used": ["t_ghost"]},
        ],
    )
    v = c.check_collection(str(d))
    assert any("s1" in x and "t_ghost" in x for x in v)


def test_dangling_used_by_skills_ref_is_violation(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[
            {"slug": "t1", "license_tier": "open", "used_by_skills": ["s_ghost"]},
        ],
        skills_index=[
            {"slug": "s1", "tools_used": []},
        ],
    )
    v = c.check_collection(str(d))
    assert any("t1" in x and "s_ghost" in x for x in v)


def test_main_exits_nonzero_on_violation(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[{"slug": "t1", "license_tier": "bogus", "used_by_skills": []}],
        skills_index=[],
    )
    assert c.main([str(d)]) == 1


def test_main_exits_zero_on_clean(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[{"slug": "t1", "license_tier": "open", "used_by_skills": []}],
        skills_index=[{"slug": "s1", "tools_used": []}],
    )
    assert c.main([str(d)]) == 0
