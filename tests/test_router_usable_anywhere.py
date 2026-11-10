"""A generated router's commands run from any working directory with `python3`.

Hosts hand the agent the directory of the advertised SKILL.md, not the plugin
root (Claude Code: "Base directory for this skill: <root>/skills/_router";
Codex: the SKILL.md path), and a stock macOS has `python3` but no `python`.
The routers released on 2026-11-09 wrote `python bin/search_skills.py`, which
fails on both counts. These tests render the routers for two unit shapes and
run the exact commands they print, with only `${CLAUDE_SKILL_DIR}` substituted
the way Claude Code substitutes it, from an unrelated working directory.
"""

from __future__ import annotations

import json
import re
import shlex
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from scripts import router_shape


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "router_collection"
PYTHON3 = shutil.which("python3")
TOOL_RECORD = {
    "name": "FixtureTool",
    "slug": "fixturetool",
    "license_tier": "open",
    "repo_url": "https://example.org/fixturetool",
}


def _commands(text: str) -> list[str]:
    """Every command line of the router's bash blocks, comments dropped."""
    commands = []
    for block in re.findall(r"```bash\n(.*?)```", text, re.S):
        joined = block.replace("\\\n", " ")
        commands += [
            line.strip()
            for line in joined.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    return commands


def _copy_fixture(tmp_path: Path) -> Path:
    unit = tmp_path / "installed" / "fixture"
    shutil.copytree(FIXTURE, unit)
    (unit / "skills" / "_router" / "SKILL.md").unlink()
    return unit


def _technique_free_unit(tmp_path: Path) -> Path:
    """The shape of the 2026-11-09 releases: no techniques, no binder, tools."""
    unit = _copy_fixture(tmp_path)
    (unit / "bin" / "perspicacite_kb_bind.py").unlink()
    index = unit / "skills_index.json"
    rows = json.loads(index.read_text(encoding="utf-8"))
    for row in rows:
        row["techniques"] = []
    index.write_text(json.dumps(rows), encoding="utf-8")
    (unit / "tools").mkdir()
    (unit / "tools" / "fixturetool.yaml").write_text(
        yaml.safe_dump(TOOL_RECORD), encoding="utf-8"
    )
    (unit / "tools_index.json").write_text(json.dumps([TOOL_RECORD]), encoding="utf-8")
    return unit


@pytest.fixture(params=["fixture", "technique-free"])
def unit(request, tmp_path: Path) -> Path:
    built = _copy_fixture(tmp_path) if request.param == "fixture" else _technique_free_unit(tmp_path)
    router_shape.write_routers(built, rewrite=True)
    return built


def _router(unit: Path) -> str:
    return (unit / "skills" / "_router" / "SKILL.md").read_text(encoding="utf-8")


def _workflow_router(unit: Path) -> str:
    return (unit / "workflows" / "_workflow_router" / "SKILL.md").read_text(encoding="utf-8")


def _run(command: str, skill_dir: Path, cwd: Path) -> subprocess.CompletedProcess:
    argv = shlex.split(command.replace(router_shape.SKILL_DIR, str(skill_dir)))
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=120)


def test_no_command_uses_bare_python_or_a_cwd_relative_path(unit: Path) -> None:
    for text in (_router(unit), _workflow_router(unit)):
        commands = _commands(text)
        assert commands
        for command in commands:
            argv = shlex.split(command)
            assert argv[0] == "python3", command
            assert argv[1].startswith(f"{router_shape.SKILL_DIR}/../../bin/"), command
        assert not re.search(r"(?<![\w-])python (?!or)", text), "bare `python ` command"
        assert "--collection ." not in text
        assert "python bin/" not in text and "python3 bin/" not in text


def test_router_points_to_the_workflow_and_tool_searches(unit: Path) -> None:
    text = _router(unit)
    assert "--target workflows" in text
    if (unit / "tools_index.json").is_file() and list(unit.glob("tools/*.yaml")):
        assert "--target tools" in text
    else:
        assert "--target tools" not in text


def test_technique_filter_is_offered_only_when_the_index_has_tags(unit: Path) -> None:
    rows = json.loads((unit / "skills_index.json").read_text(encoding="utf-8"))
    tagged = any(row.get("techniques") for row in rows)
    assert ("--technique" in _router(unit)) is tagged


def test_every_tier_is_defined_with_one_meaning(unit: Path) -> None:
    text = _router(unit)
    tiers = text[text.index("## Licence tiers"):]
    for tier in ("`open`", "`noncommercial`", "`restricted`", "`unknown`"):
        assert tier in tiers
    assert "a licence was established and it constrains reuse" in tiers
    assert "no clear licence detected" not in tiers


def _description(text: str) -> str:
    return yaml.safe_load(text.split("---\n", 2)[1])["description"]


def test_description_opens_with_a_plain_domain_trigger(unit: Path) -> None:
    description = _description(_router(unit))
    first = description.split(". ")[0]
    assert first.startswith("Use for any fixture how-to question")
    assert first.endswith("before answering from memory")
    # Codex cut a description near 169 characters: the trigger must fit.
    assert len(first) + 1 <= 160
    assert "skill from" not in first
    assert "\u2014" not in _router(unit) and "\u2014" not in _workflow_router(unit)


def test_description_names_what_is_searched_without_workflow_slugs() -> None:
    contract = {"search_workflows": True, "search_tools": True, "tools_count": 1200,
                "workflows_count": 2, "workflow_names": ["a-b", "c-d"]}
    text = router_shape.router_description("Agentic AI", 668, contract)
    assert text.startswith("Use for any agentic AI how-to question")
    assert "668 evidence-grounded agentic AI skills" in text
    assert "2 end-to-end workflows and 1,200 tool records" in text
    assert "a b" not in text and "Workflows:" not in text


def test_claude_code_substitution_leaves_no_variable_and_names_no_variable(unit: Path) -> None:
    """Claude Code replaces every `${CLAUDE_SKILL_DIR}`; the result must read whole."""
    skill_dir = unit / "skills" / "_router"
    substituted = _router(unit).replace(router_shape.SKILL_DIR, str(skill_dir))
    assert "${" not in substituted.replace("${...}", "")
    assert f'python3 "{skill_dir}/../../bin/search_skills.py"' in substituted


def test_hosts_without_substitution_are_told_what_to_replace(unit: Path) -> None:
    text = _router(unit)
    assert router_shape.SKILL_DIR == "${CLAUDE_SKILL_DIR}"
    section = text[text.index("## 1. Search"):text.index("```bash")]
    assert router_shape.SKILL_DIR not in section
    assert "`<collection root>/skills/_router`" in section
    assert "do not `cd`" in section


def test_router_asks_for_doi_and_tier_in_the_answer(unit: Path) -> None:
    text = _router(unit)
    apply = text[text.index("## 2. Apply"):text.index("## 3.")]
    assert router_shape.CITE_IN_ANSWER in apply


@pytest.mark.skipif(PYTHON3 is None, reason="no python3 on PATH")
def test_every_router_command_runs_from_an_unrelated_cwd(unit: Path, tmp_path: Path) -> None:
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    queries = {
        "<the user's task>": "align retention time across samples",
        "<the user's goal>": "untargeted annotation",
        "<a tool name or task>": "FixtureTool",
    }
    routers = {
        unit / "skills" / "_router": _router(unit),
        unit / "workflows" / "_workflow_router": _workflow_router(unit),
    }
    ran = 0
    for skill_dir, text in routers.items():
        for command in _commands(text):
            if "search_skills.py" not in command:
                continue
            for placeholder, query in queries.items():
                command = command.replace(placeholder, query)
            result = _run(command, skill_dir, elsewhere)
            assert result.returncode == 0, command + "\n" + result.stdout + result.stderr
            paths = [
                line.split("read:", 1)[1].strip()
                for line in result.stdout.splitlines()
                if line.strip().startswith("read:")
            ]
            assert paths, result.stdout
            assert all(Path(path).is_absolute() and Path(path).is_file() for path in paths)
            ran += 1
    assert ran >= 3


@pytest.mark.skipif(PYTHON3 is None, reason="no python3 on PATH")
def test_the_binder_command_resolves_from_an_unrelated_cwd(tmp_path: Path) -> None:
    unit = _copy_fixture(tmp_path)
    router_shape.write_routers(unit, rewrite=True)
    [command] = [c for c in _commands(_router(unit)) if "perspicacite_kb_bind.py" in c]
    slug = next(iter(json.loads((unit / "kb_bundle.json").read_text())["skills"]))
    offline = re.sub(r' --question "[^"]*"', "", command).replace(" query ", " resolve ")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    result = _run(offline.replace("<slug>", slug), unit / "skills" / "_router", elsewhere)
    assert result.returncode == 0, result.stdout + result.stderr
    assert slug in result.stdout


def test_section_refresh_replaces_the_released_search_and_tier_text(tmp_path: Path) -> None:
    unit = _technique_free_unit(tmp_path)
    released = (
        "---\nname: fixture-router\ndescription: keep\n---\n\n# Fixture router\n\n"
        "## 1. Search\n\n```bash\npython bin/search_skills.py --query \"<the user's task>\" -k 10\n```\n\n"
        "Narrow with `--tool <name>`, `--technique <tag>` or `--edam <iri-substring>`.\n\n"
        "## Licence tiers\n\n`restricted` \u2014 no clear licence detected.\n"
    )
    router = unit / "skills" / "_router" / "SKILL.md"
    router.write_text(released, encoding="utf-8")

    router_shape.write_router(unit, 10)
    text = router.read_text(encoding="utf-8")

    assert text.startswith("---\nname: fixture-router\ndescription: keep\n---\n")
    assert "python bin/" not in text and "--technique" not in text
    assert router_shape.TIERS_SECTION in text and "`unknown`" in text


def test_workflow_router_is_kept_unless_rewritten(tmp_path: Path) -> None:
    unit = _copy_fixture(tmp_path)
    router = unit / "workflows" / "_workflow_router" / "SKILL.md"
    router.parent.mkdir()
    router.write_text("hand-written\n", encoding="utf-8")
    assert router_shape.write_workflow_router(unit) is False
    assert router.read_text(encoding="utf-8") == "hand-written\n"
    assert router_shape.write_workflow_router(unit, rewrite=True) is True
    text = router.read_text(encoding="utf-8")
    rows = json.loads((unit / "workflows" / "workflows_index.json").read_text())
    for row in rows:
        assert f"| `{row['slug']}` |" in text
