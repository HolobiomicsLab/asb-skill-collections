"""The description lint enforces its rules directly on fixture trees."""

import pathlib
import re

import yaml

from scripts import lint_skill_descriptions


def _skill(root, slug, description):
    directory = root / "skills" / slug
    directory.mkdir(parents=True)
    (directory / "SKILL.md").write_text(
        f"---\n{yaml.safe_dump({'description': description})}---\n", encoding="utf-8"
    )


def test_lint_accepts_a_bounded_use_when_description(tmp_path):
    _skill(tmp_path, "valid", "Use when testing a skill description in a compact fixture tree.")
    assert lint_skill_descriptions.lint([tmp_path]) == []
    assert lint_skill_descriptions.main([str(tmp_path)]) == 0


def test_lint_rejects_an_invalid_description(tmp_path):
    _skill(tmp_path, "invalid", "Best tool.")
    failures = lint_skill_descriptions.lint([tmp_path])
    assert len(failures) == 3
    assert any("description must start" in failure for failure in failures)
    assert any("description too short" in failure for failure in failures)
    assert any("marketing term" in failure for failure in failures)
    assert lint_skill_descriptions.main([str(tmp_path)]) == 1


def test_no_workflow_installs_an_unpublished_name():
    workflows = pathlib.Path(__file__).parent.parent / ".github" / "workflows"
    install = re.compile(r"\b(pip3?|pipx|uv pip)\s+(install|run)\b")
    offenders = [
        f"{workflow.name}:{number}"
        for workflow in workflows.glob("*.y*ml")
        for number, line in enumerate(workflow.read_text(encoding="utf-8").splitlines(), 1)
        if install.search(line) and "indicium-adapters" in line
    ]
    assert not offenders
