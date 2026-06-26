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


def _synthetic_fm(
    slug="my-meta-skill",
    tools_used=None,
    synthesized_from=("lc-ms-feature-extraction", "spectral-similarity-scoring"),
    skill_kind="super",
    orchestrates=("lc-ms-feature-extraction", "spectral-similarity-scoring"),
    **overrides,
):
    """A synthetic-provenance (optionally super) staged proposal frontmatter.

    Synthetic proposals are valid via ``metadata.synthesized_from`` rather than
    the community ``related_skills`` key.
    """
    meta = {
        "edam_operation": "http://edamontology.org/operation_3215",
        "edam_topics": ["http://edamontology.org/topic_0091"],
        "license_tier": "open",
        "provenance_tier": "synthetic",
        "tools_used": ["mzmine"] if tools_used is None else tools_used,
    }
    if synthesized_from is not None:
        meta["synthesized_from"] = list(synthesized_from)
    if skill_kind is not None:
        meta["skill_kind"] = skill_kind
    if orchestrates is not None:
        meta["orchestrates"] = list(orchestrates)
    fm = {
        "name": slug,
        "description": VALID_DESC,
        "license": "CC-BY-4.0",
        "metadata": meta,
        "status": "hold",
    }
    fm.update(overrides)
    return fm


def _literature_fm(
    slug="my-review-meta-skill",
    tools_used=None,
    dois=("10.1021/acs.analchem.0c01234",),
    synthesized_from=("lc-ms-feature-extraction", "spectral-similarity-scoring"),
    skill_kind="super",
    orchestrates=("lc-ms-feature-extraction", "spectral-similarity-scoring"),
    **overrides,
):
    """A review-grounded (literature-provenance) staged super-skill frontmatter.

    Literature proposals are valid via >=1 source ``metadata.dois`` (the review
    DOI), while keeping the super orchestration invariants.
    """
    meta = {
        "edam_operation": "http://edamontology.org/operation_3215",
        "edam_topics": ["http://edamontology.org/topic_0091"],
        "license_tier": "open",
        "provenance_tier": "literature",
        "tools_used": ["mzmine"] if tools_used is None else tools_used,
    }
    if dois is not None:
        meta["dois"] = list(dois)
    if synthesized_from is not None:
        meta["synthesized_from"] = list(synthesized_from)
    if skill_kind is not None:
        meta["skill_kind"] = skill_kind
    if orchestrates is not None:
        meta["orchestrates"] = list(orchestrates)
    fm = {
        "name": slug,
        "description": VALID_DESC,
        "license": "CC-BY-4.0",
        "metadata": meta,
        "status": "hold",
    }
    if dois is not None:
        fm["derived_from"] = [{"doi": d} for d in dois]
    fm.update(overrides)
    return fm


def _write_skill(col, fm, body="# Skill\n\nbody\n"):
    slug = fm["name"]
    d = col / "proposals" / "skills" / slug
    d.mkdir(parents=True, exist_ok=True)
    text = "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n" + body
    (d / "SKILL.md").write_text(text)


def _collection(
    tmp_path,
    tool_slugs=("mzmine",),
    skill_slugs=("lc-ms-feature-extraction", "spectral-similarity-scoring"),
):
    col = tmp_path / "v2"
    col.mkdir(parents=True)
    tools = [{"slug": s, "license_tier": "open", "used_by_skills": []} for s in tool_slugs]
    (col / "tools_index.json").write_text(json.dumps(tools))
    skills = [{"slug": s} for s in skill_slugs]
    (col / "skills_index.json").write_text(json.dumps(skills))
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

def test_unknown_provenance_tier_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["metadata"]["provenance_tier"] = "made-up"
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("provenance_tier" in x and "made-up" in x for x in v)


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


# --- synthetic provenance + super invariants ---------------------------------

def test_clean_synthetic_super_skill_passes(tmp_path):
    # A synthetic super-skill is valid via synthesized_from + a resolvable
    # orchestrates list — no community related_skills key required.
    col = _collection(tmp_path)
    _write_skill(col, _synthetic_fm())
    assert c.check_collection(str(col)) == []


def test_synthetic_without_synthesized_from_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _synthetic_fm(synthesized_from=None)
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("synthesized_from" in x for x in v)


def test_synthetic_with_empty_synthesized_from_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _synthetic_fm()
    fm["metadata"]["synthesized_from"] = []
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("synthesized_from" in x for x in v)


def test_super_with_empty_orchestrates_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _synthetic_fm(orchestrates=None)
    fm["metadata"]["orchestrates"] = []
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("orchestrates" in x for x in v)


def test_super_with_absent_orchestrates_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _synthetic_fm(orchestrates=None)  # key absent entirely
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("orchestrates" in x for x in v)


def test_super_orchestrates_slug_not_in_index_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _synthetic_fm(
        synthesized_from=("lc-ms-feature-extraction", "ghost-skill"),
        orchestrates=("lc-ms-feature-extraction", "ghost-skill"),
    )
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("ghost-skill" in x for x in v)


def test_synthetic_skill_kind_skill_does_not_require_orchestrates(tmp_path):
    # Default/explicit non-super kind => orchestrates is irrelevant.
    col = _collection(tmp_path)
    fm = _synthetic_fm(skill_kind="skill", orchestrates=None)
    _write_skill(col, fm)
    assert c.check_collection(str(col)) == []


def test_synthetic_default_skill_kind_is_skill(tmp_path):
    # No skill_kind key => treated as 'skill', so no orchestrates needed.
    col = _collection(tmp_path)
    fm = _synthetic_fm(skill_kind=None, orchestrates=None)
    _write_skill(col, fm)
    assert c.check_collection(str(col)) == []


def test_invalid_skill_kind_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _synthetic_fm(skill_kind="orchestrator", orchestrates=None)
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("skill_kind" in x for x in v)


# --- literature provenance (review-grounded super-skills) --------------------

def test_clean_literature_super_skill_passes(tmp_path):
    # A review-grounded super-skill is valid via >=1 source DOI + a resolvable
    # orchestrates list — no community related_skills key required.
    col = _collection(tmp_path)
    _write_skill(col, _literature_fm())
    assert c.check_collection(str(col)) == []


def test_literature_without_doi_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _literature_fm(dois=None)
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("doi" in x.lower() for x in v)


def test_literature_with_empty_dois_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _literature_fm()
    fm["metadata"]["dois"] = []
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("doi" in x.lower() for x in v)


def test_literature_super_still_resolves_orchestrates(tmp_path):
    # The super invariants apply regardless of provenance: a literature super
    # with a dangling orchestrate slug must fail.
    col = _collection(tmp_path)
    fm = _literature_fm(
        synthesized_from=("lc-ms-feature-extraction", "ghost-skill"),
        orchestrates=("lc-ms-feature-extraction", "ghost-skill"),
    )
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("ghost-skill" in x for x in v)


def test_community_skill_with_super_kind_resolves_orchestrates(tmp_path):
    # skill_kind/orchestrates apply regardless of provenance; a community super
    # with a dangling orchestrate slug must fail.
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["metadata"]["skill_kind"] = "super"
    fm["metadata"]["orchestrates"] = ["lc-ms-feature-extraction", "ghost-skill"]
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("ghost-skill" in x for x in v)


# --- contributors (co-authorship attribution) --------------------------------

def test_no_contributors_key_passes(tmp_path):
    # contributors is optional — a staged skill without it is still valid.
    col = _collection(tmp_path)
    _write_skill(col, _good_fm())
    assert c.check_collection(str(col)) == []


def test_valid_contributors_block_passes(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["contributors"] = [
        {"name": "Ada Lovelace", "role": "author", "orcid": "0000-0002-1825-0097"},
        {"name": "Grace Hopper", "role": "reviewer"},
    ]
    _write_skill(col, fm)
    assert c.check_collection(str(col)) == []


def test_contributors_not_a_list_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["contributors"] = {"name": "Ada", "role": "author"}
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("contributor" in x.lower() for x in v)


def test_contributor_entry_not_mapping_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["contributors"] = ["Ada Lovelace"]
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("contributor" in x.lower() and "mapping" in x.lower() for x in v)


def test_contributor_missing_name_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["contributors"] = [{"role": "author"}]
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("contributor" in x.lower() and "name" in x.lower() for x in v)


def test_contributor_empty_name_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["contributors"] = [{"name": "  ", "role": "author"}]
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("contributor" in x.lower() and "name" in x.lower() for x in v)


def test_contributor_missing_role_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["contributors"] = [{"name": "Ada"}]
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("contributor" in x.lower() and "role" in x.lower() for x in v)


def test_contributor_bad_role_fails(tmp_path):
    col = _collection(tmp_path)
    fm = _good_fm()
    fm["contributors"] = [{"name": "Ada", "role": "maintainer"}]
    _write_skill(col, fm)
    v = c.check_collection(str(col))
    assert any("contributor" in x.lower() and "role" in x.lower() for x in v)


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
