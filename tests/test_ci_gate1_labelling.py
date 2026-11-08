"""The description lint keeps its published rules on real fixture trees."""

import yaml

from scripts import lint_skill_descriptions


def _write_skill(root, slug, description):
    directory = root / "collections" / "fixture" / "v1" / "skills" / slug
    directory.mkdir(parents=True)
    (directory / "SKILL.md").write_text(
        f"---\n{yaml.safe_dump({'description': description})}---\n", encoding="utf-8"
    )


def test_valid_description_passes(tmp_path):
    _write_skill(tmp_path, "valid", "Use when checking descriptions against their length budget.")
    assert lint_skill_descriptions.lint([tmp_path]) == []


def test_short_description_fails(tmp_path):
    _write_skill(tmp_path, "short", "Use when short.")
    failures = lint_skill_descriptions.lint([tmp_path])
    assert len(failures) == 1
    assert "description too short" in failures[0]


def test_long_description_fails(tmp_path):
    _write_skill(tmp_path, "long", "Use when " + "x" * 300)
    failures = lint_skill_descriptions.lint([tmp_path])
    assert len(failures) == 1
    assert "description too long" in failures[0]


def test_unapproved_opening_fails(tmp_path):
    _write_skill(tmp_path, "opening", "This description is long enough but does not say when to use it.")
    failures = lint_skill_descriptions.lint([tmp_path])
    assert len(failures) == 1
    assert "description must start" in failures[0]


def test_marketing_term_fails(tmp_path):
    _write_skill(tmp_path, "marketing", "Use when choosing the revolutionary approach for this fixture.")
    failures = lint_skill_descriptions.lint([tmp_path])
    assert len(failures) == 1
    assert "marketing term" in failures[0]


def test_missing_frontmatter_is_left_to_the_structure_gate(tmp_path):
    _write_skill(tmp_path, "valid", "Use when checking descriptions against their length budget.")
    path = tmp_path / "collections" / "fixture" / "v1" / "skills" / "valid" / "SKILL.md"
    path.write_text("No frontmatter\n", encoding="utf-8")
    assert lint_skill_descriptions.lint([tmp_path]) == []
