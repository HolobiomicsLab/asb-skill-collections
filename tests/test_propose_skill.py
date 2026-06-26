import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import propose_skill as p


# --- fixtures ----------------------------------------------------------------

VALID_DESC = (
    "Use when you have a raw LC-MS feature table and need to filter blank "
    "contamination before downstream statistical analysis of metabolites."
)


def _frontmatter(slug="my-new-skill"):
    return {
        "name": slug,
        "description": VALID_DESC,
        "license": "CC-BY-4.0",
        "metadata": {
            "edam_operation": "http://edamontology.org/operation_3215",
            "edam_topics": ["http://edamontology.org/topic_0091"],
            "license_tier": "open",
            "provenance_tier": "community",
            "tools_used": ["mzmine"],
        },
        "status": "hold",
        "related_skills": ["lc-ms-feature-extraction"],
    }


def _ledger_meta(slug="my-new-skill"):
    return {
        "slug": slug,
        "contributor": "octocat",
        "related_skills": ["lc-ms-feature-extraction"],
        "tools_used": ["mzmine"],
        "license_tier": "open",
        "grounding": {"upgrade_candidate": False},
        "status": "hold",
    }


BODY = "# My New Skill\n\nApply the procedure here.\n"
DATE = "2026-06-26"


# --- stage_proposal: writes the tree -----------------------------------------

def test_stage_proposal_writes_skill_md_and_ledger(tmp_path):
    res = p.stage_proposal(
        str(tmp_path), _frontmatter(), BODY, _ledger_meta(), date=DATE
    )
    skill_md = tmp_path / "proposals" / "skills" / "my-new-skill" / "SKILL.md"
    ledger = tmp_path / "proposals" / "wave-skills-2026-06-26.yaml"
    assert skill_md.is_file()
    assert ledger.is_file()
    # returned paths point at what was written
    assert pathlib.Path(res["skill_md"]) == skill_md
    assert pathlib.Path(res["ledger"]) == ledger


def test_stage_proposal_skill_md_has_frontmatter_and_body(tmp_path):
    p.stage_proposal(str(tmp_path), _frontmatter(), BODY, _ledger_meta(), date=DATE)
    text = (tmp_path / "proposals" / "skills" / "my-new-skill" / "SKILL.md").read_text()
    assert text.startswith("---\n")
    fm = yaml.safe_load(text.split("---\n", 2)[1])
    assert fm["related_skills"] == ["lc-ms-feature-extraction"]
    assert fm["metadata"]["provenance_tier"] == "community"
    assert fm["status"] == "hold"
    # body is preserved after the closing fence
    assert "Apply the procedure here." in text.split("---\n", 2)[2]


def test_stage_proposal_ledger_schema_and_entry(tmp_path):
    p.stage_proposal(str(tmp_path), _frontmatter(), BODY, _ledger_meta(), date=DATE)
    ledger = yaml.safe_load(
        (tmp_path / "proposals" / "wave-skills-2026-06-26.yaml").read_text()
    )
    assert ledger["schema"] == "asb-skill-proposals/1.0"
    slugs = [e["slug"] for e in ledger["proposals"]]
    assert "my-new-skill" in slugs
    entry = next(e for e in ledger["proposals"] if e["slug"] == "my-new-skill")
    assert entry["status"] == "hold"
    assert entry["tools_used"] == ["mzmine"]
    # a submitted_on date is stamped from the passed date
    assert entry.get("submitted_on") == DATE


# --- idempotence -------------------------------------------------------------

def test_stage_proposal_is_idempotent(tmp_path):
    first = p.stage_proposal(
        str(tmp_path), _frontmatter(), BODY, _ledger_meta(), date=DATE
    )
    md_text_1 = pathlib.Path(first["skill_md"]).read_text()
    ledger_text_1 = pathlib.Path(first["ledger"]).read_text()

    second = p.stage_proposal(
        str(tmp_path), _frontmatter(), BODY, _ledger_meta(), date=DATE
    )
    md_text_2 = pathlib.Path(second["skill_md"]).read_text()
    ledger_text_2 = pathlib.Path(second["ledger"]).read_text()

    assert md_text_1 == md_text_2
    assert ledger_text_1 == ledger_text_2
    # the ledger has exactly one entry for this slug (no duplicate append)
    ledger = yaml.safe_load(ledger_text_2)
    assert [e["slug"] for e in ledger["proposals"]].count("my-new-skill") == 1


def test_stage_proposal_appends_distinct_slugs_to_same_wave(tmp_path):
    p.stage_proposal(str(tmp_path), _frontmatter("skill-a"), BODY, _ledger_meta("skill-a"), date=DATE)
    p.stage_proposal(str(tmp_path), _frontmatter("skill-b"), BODY, _ledger_meta("skill-b"), date=DATE)
    ledger = yaml.safe_load(
        (tmp_path / "proposals" / "wave-skills-2026-06-26.yaml").read_text()
    )
    slugs = sorted(e["slug"] for e in ledger["proposals"])
    assert slugs == ["skill-a", "skill-b"]


def test_stage_proposal_updates_existing_entry_in_place(tmp_path):
    p.stage_proposal(str(tmp_path), _frontmatter(), BODY, _ledger_meta(), date=DATE)
    meta2 = _ledger_meta()
    meta2["contributor"] = "someone-else"
    p.stage_proposal(str(tmp_path), _frontmatter(), BODY, meta2, date=DATE)
    ledger = yaml.safe_load(
        (tmp_path / "proposals" / "wave-skills-2026-06-26.yaml").read_text()
    )
    entries = [e for e in ledger["proposals"] if e["slug"] == "my-new-skill"]
    assert len(entries) == 1
    assert entries[0]["contributor"] == "someone-else"


# --- dry run -----------------------------------------------------------------

def test_dry_run_writes_nothing(tmp_path):
    res = p.stage_proposal(
        str(tmp_path), _frontmatter(), BODY, _ledger_meta(), date=DATE, dry_run=True
    )
    assert not (tmp_path / "proposals").exists()
    # still reports the paths it WOULD have written
    assert "skill_md" in res and "ledger" in res
    assert res.get("dry_run") is True


# --- slug from frontmatter name ----------------------------------------------

def test_stage_proposal_slugifies_name_for_dir(tmp_path):
    fm = _frontmatter()
    fm["name"] = "My New Skill"
    res = p.stage_proposal(str(tmp_path), fm, BODY, _ledger_meta("my-new-skill"), date=DATE)
    assert (tmp_path / "proposals" / "skills" / "my-new-skill" / "SKILL.md").is_file()
    assert pathlib.Path(res["skill_md"]).parent.name == "my-new-skill"


# --- main(argv) --------------------------------------------------------------

def _write_input_skill(tmp_path):
    fm = _frontmatter()
    text = "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n" + BODY
    src = tmp_path / "input_SKILL.md"
    src.write_text(text)
    return src


def test_main_dry_run_writes_nothing(tmp_path, capsys):
    src = _write_input_skill(tmp_path)
    col = tmp_path / "col"
    col.mkdir()
    rc = p.main(
        ["--collection", str(col), "--skill-md", str(src), "--date", DATE, "--dry-run"]
    )
    assert rc == 0
    assert not (col / "proposals").exists()


def test_main_stages_files(tmp_path):
    src = _write_input_skill(tmp_path)
    col = tmp_path / "col"
    col.mkdir()
    rc = p.main(["--collection", str(col), "--skill-md", str(src), "--date", DATE])
    assert rc == 0
    assert (col / "proposals" / "skills" / "my-new-skill" / "SKILL.md").is_file()
    assert (col / "proposals" / "wave-skills-2026-06-26.yaml").is_file()
