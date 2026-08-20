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


# ---------------------------------------------------------------------------
# Per-tool YAML <-> tools_index license_tier cross-check
# ---------------------------------------------------------------------------

def _write_tool_yaml(d, slug, **fields):
    (d / "tools").mkdir(exist_ok=True)
    lines = [f"slug: {slug}"]
    for k, v in fields.items():
        lines.append(f"{k}: {v}")
    (d / "tools" / f"{slug}.yaml").write_text("\n".join(lines) + "\n")


def test_tool_yaml_tier_match_passes(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[{"slug": "t1", "license_tier": "open", "used_by_skills": []}],
        skills_index=[],
    )
    _write_tool_yaml(d, "t1", license_tier="open")
    assert c.check_collection(str(d)) == []


def test_tool_yaml_tier_mismatch_is_violation(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[{"slug": "t1", "license_tier": "open", "used_by_skills": []}],
        skills_index=[],
    )
    _write_tool_yaml(d, "t1", license_tier="restricted")
    v = c.check_collection(str(d))
    assert any("t1" in x and "license_tier" in x and "tools/" in x for x in v)


def test_tool_yaml_missing_tier_is_violation(tmp_path):
    # YAML exists but never got enriched -> the cross-check flags it.
    d = _collection(
        tmp_path,
        tools_index=[{"slug": "t1", "license_tier": "open", "used_by_skills": []}],
        skills_index=[],
    )
    _write_tool_yaml(d, "t1", name="T1")
    v = c.check_collection(str(d))
    assert any("t1" in x and "license_tier" in x and "tools/" in x for x in v)


def test_tool_without_yaml_is_skipped(tmp_path):
    # tools/<slug>.yaml absent -> no YAML cross-check violation for that tool.
    d = _collection(
        tmp_path,
        tools_index=[{"slug": "t1", "license_tier": "open", "used_by_skills": []}],
        skills_index=[],
    )
    (d / "tools").mkdir(exist_ok=True)  # dir exists but no t1.yaml
    assert c.check_collection(str(d)) == []


def test_no_tools_dir_is_skipped(tmp_path):
    # No tools/ dir at all -> cross-check is a no-op (back-compat).
    d = _collection(
        tmp_path,
        tools_index=[{"slug": "t1", "license_tier": "open", "used_by_skills": []}],
        skills_index=[],
    )
    assert c.check_collection(str(d)) == []
