import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import check_proposals as c


VALID_DESC = (
    "Use when you have a raw LC-MS feature table and need to filter blank "
    "contamination before downstream statistical analysis of metabolites."
)


def _good_fm(slug="my-new-skill", tools_used=None, **overrides):
    fm = {
        "name": slug,
        "description": VALID_DESC,
        "license": "CC-BY-4.0",
        "metadata": {
            "edam_operation": "http://edamontology.org/operation_3215",
            "edam_topics": ["http://edamontology.org/topic_0091"],
            "license_tier": "open",
            "provenance_tier": "community",
            "tools_used": ["mzmine"] if tools_used is None else tools_used,
        },
        "status": "hold",
        "related_skills": ["lc-ms-feature-extraction"],
    }
    fm.update(overrides)
    return fm


def _write_skill(col, fm, body="# Skill\n\nbody\n"):
    slug = fm["name"]
    d = col / "proposals" / "skills" / slug
    d.mkdir(parents=True, exist_ok=True)
    text = "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n" + body
    (d / "SKILL.md").write_text(text)


def _collection(tmp_path, tool_slugs=("mzmine",)):
    col = tmp_path / "v2"
    col.mkdir(parents=True)
    tools = [{"slug": s, "license_tier": "open", "used_by_skills": []} for s in tool_slugs]
    (col / "tools_index.json").write_text(json.dumps(tools))
    return col


# --- no proposals dir => clean -----------------------------------------------

def test_no_proposals_dir_returns_empty(tmp_path):
    col = _collection(tmp_path)
    assert c.check_collection(str(col)) == []


def test_empty_proposals_skills_dir_returns_empty(tmp_path):
    col = _collection(tmp_path)
    (col / "proposals" / "skills").mkdir(parents=True)
    assert c.check_collection(str(col)) == []


# --- clean staged skill passes -----------------------------------------------

def test_clean_staged_skill_passes(tmp_path):
    col = _collection(tmp_path)
    _write_skill(col, _good_fm())
    assert c.check_collection(str(col)) == []


# --- bad provenance tier -----------------------------------------------------

def test_non_community_provenance_tier_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["metadata"]["provenance_tier"] = "literature"
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("provenance_tier" in x and "community" in x for x in v)


# --- missing related_skills key ----------------------------------------------

def test_missing_related_skills_key_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    del fm["related_skills"]
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("related_skills" in x for x in v)


# --- status not hold ---------------------------------------------------------

def test_status_not_hold_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["status"] = "accepted"
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("status" in x and "hold" in x for x in v)


# --- dangling tools_used -----------------------------------------------------

def test_dangling_tools_used_fails(tmp_path):
    col = _collection(tmp_path, tool_slugs=("mzmine",))
    fm = _good_fm(tools_used=["mzmine", "ghost-tool"])
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("ghost-tool" in x for x in v)


# --- marketing description (frontmatter_violations) --------------------------

def test_marketing_description_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["description"] = (
        "Use when you want the best approach to filter blank contamination "
        "from your LC-MS feature table before statistical analysis."
    )
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("marketing" in x.lower() or "best" in x for x in v)


def test_bad_edam_iri_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["metadata"]["edam_operation"] = "https://edamontology.org/operation_3215"
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("edam" in x.lower() for x in v)


def test_non_mapping_frontmatter_reports_clean_violation(tmp_path):
    # A hand-authored proposal whose frontmatter parses to a list/scalar must yield
    # a clean violation, not an uncaught AttributeError traceback.
    col = _collection(tmp_path)
    d = col / "proposals" / "skills" / "broken"
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text("---\n- just\n- a\n- list\n---\n# Skill\n")
    v = c.check_collection(str(col))
    assert any("not a mapping" in x for x in v)


# --- main(argv) exit codes ---------------------------------------------------

def test_main_exits_zero_when_no_proposals(tmp_path):
    col = _collection(tmp_path)
    assert c.main([str(col)]) == 0


def test_main_exits_zero_on_clean_staged(tmp_path):
    col = _collection(tmp_path)
    _write_skill(col, _good_fm())
    assert c.main([str(col)]) == 0


def test_main_exits_one_on_violation(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["status"] = "accepted"
    _write_skill(col, fm)
    assert c.main([str(col)]) == 1
