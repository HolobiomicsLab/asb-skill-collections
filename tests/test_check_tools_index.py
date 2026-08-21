import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import check_tools_index as c


def resolved(slug, tier="open", **extra):
    """A tool whose tier rests on a lookup of the tool's own repository."""
    return {"slug": slug, "license_tier": tier, "license": "MIT",
            "license_detection": "github-api", "license_subject": "tool",
            "used_by_skills": [], **extra}


def unresolved(slug, **extra):
    """A tool nothing was established about: the catalogue's actual shape today."""
    return {"slug": slug, "license_tier": "unknown", "license": None,
            "license_detection": None, "license_subject": None,
            "used_by_skills": [], **extra}


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
            resolved("t1", used_by_skills=["s1"]),
            unresolved("t2"),
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
            resolved("t1"),
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
            resolved("t1", used_by_skills=["s_ghost"]),
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
        tools_index=[resolved("t1")],
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
        tools_index=[resolved("t1")],
        skills_index=[],
    )
    _write_tool_yaml(d, "t1", license_tier="open")
    assert c.check_collection(str(d)) == []


def test_tool_yaml_tier_mismatch_is_violation(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[resolved("t1")],
        skills_index=[],
    )
    _write_tool_yaml(d, "t1", license_tier="restricted")
    v = c.check_collection(str(d))
    assert any("t1" in x and "license_tier" in x and "tools/" in x for x in v)


def test_tool_yaml_missing_tier_is_violation(tmp_path):
    # YAML exists but never got enriched -> the cross-check flags it.
    d = _collection(
        tmp_path,
        tools_index=[resolved("t1")],
        skills_index=[],
    )
    _write_tool_yaml(d, "t1", name="T1")
    v = c.check_collection(str(d))
    assert any("t1" in x and "license_tier" in x and "tools/" in x for x in v)


def test_tool_without_yaml_is_skipped(tmp_path):
    # tools/<slug>.yaml absent -> no YAML cross-check violation for that tool.
    d = _collection(
        tmp_path,
        tools_index=[resolved("t1")],
        skills_index=[],
    )
    (d / "tools").mkdir(exist_ok=True)  # dir exists but no t1.yaml
    assert c.check_collection(str(d)) == []


def test_no_tools_dir_is_skipped(tmp_path):
    # No tools/ dir at all -> cross-check is a no-op (back-compat).
    d = _collection(
        tmp_path,
        tools_index=[resolved("t1")],
        skills_index=[],
    )
    assert c.check_collection(str(d)) == []


# --------------------------------------------------------------------------- #
# Licence provenance: a tool's tier must rest on evidence about the tool.      #
# --------------------------------------------------------------------------- #

def test_a_tier_resting_on_a_paper_detection_is_a_violation(tmp_path):
    """The #42 regression. A citing paper's licence is not the tool's."""
    for detection in ("crossref-paper", "biorxiv_api-paper"):
        d = _collection(
            tmp_path / detection,
            tools_index=[{"slug": "t1", "license_tier": "open", "license": "CC-BY-4.0",
                          "license_detection": detection, "license_subject": "paper",
                          "used_by_skills": []}],
            skills_index=[],
        )
        v = c.check_collection(str(d))
        assert any("not evidence about the tool" in x for x in v), detection


def test_a_resolved_tier_without_a_subject_is_a_violation(tmp_path):
    d = _collection(
        tmp_path,
        tools_index=[{"slug": "t1", "license_tier": "open", "license": "MIT",
                      "license_detection": "github-api", "used_by_skills": []}],
        skills_index=[],
    )
    assert any("license_subject" in x for x in c.check_collection(str(d)))


def test_an_unknown_tier_may_not_still_carry_a_licence(tmp_path):
    """`unknown` means nothing was established; a leftover value contradicts it."""
    d = _collection(
        tmp_path,
        tools_index=[{"slug": "t1", "license_tier": "unknown", "license": "MIT",
                      "license_detection": None, "license_subject": None,
                      "used_by_skills": []}],
        skills_index=[],
    )
    assert any("unknown but a licence is recorded" in x for x in c.check_collection(str(d)))


def test_the_retired_canonical_url_key_is_rejected(tmp_path):
    """It named a tool's home while holding a citing paper's repository."""
    d = _collection(
        tmp_path,
        tools_index=[unresolved("t1", canonical_url="https://github.com/some/paper")],
        skills_index=[],
    )
    assert any("canonical_url" in x and "retired" in x for x in c.check_collection(str(d)))


def test_the_tier_vocabulary_comes_from_governance_not_a_local_copy():
    """A hand-copied set here would have rejected `unknown` the day it was added."""
    import yaml as _yaml
    governance = pathlib.Path(__file__).parent.parent / "governance" / "license_tiers.yaml"
    assert c._VALID == set(_yaml.safe_load(governance.read_text())["tiers"])
