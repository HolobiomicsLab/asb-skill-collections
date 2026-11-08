"""Router commands run from an installed plugin root, not a source checkout."""

from __future__ import annotations

import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parent.parent
V2 = REPO / "tests" / "fixtures" / "router_collection"
ROUTER = V2 / "skills" / "_router" / "SKILL.md"
BINDER = REPO / "scripts" / "perspicacite_kb_bind.py"
ROOT = "<collection root>"


def router_commands() -> list[str]:
    """Extract Python commands from the router's bash blocks."""
    text = ROUTER.read_text(encoding="utf-8")
    commands = []
    for block in re.findall(r"```bash\n(.*?)```", text, re.S):
        joined = block.replace("\\\n", " ")
        commands += [
            line.strip()
            for line in joined.splitlines()
            if line.strip().startswith("python ")
        ]
    return commands


@pytest.fixture(scope="module")
def installed(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Copy the installed-unit inputs outside the source checkout."""
    root = tmp_path_factory.mktemp("plugins") / "fixture"
    for name in ("bin", ".claude-plugin"):
        shutil.copytree(V2 / name, root / name)
    for name in ("skills_index.json", "kb_bundle.json", "workflows/workflows_index.json"):
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(V2 / name, root / name)
    return root


def _run(command: str, root: Path, cwd: Path) -> subprocess.CompletedProcess:
    argv = shlex.split(command.replace(ROOT, str(root)))
    assert argv[0] == "python"
    return subprocess.run(
        [sys.executable, *argv[1:]],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_router_names_three_commands_under_the_collection_root() -> None:
    commands = router_commands()
    assert len(commands) == 3, commands
    for command in commands:
        assert command.startswith(f'python "{ROOT}/bin/'), command
        assert "scripts/" not in command and "collections/" not in command, command
        script = shlex.split(command)[1].replace(f"{ROOT}/", "")
        assert (V2 / script).is_file(), script


def test_both_search_commands_run_from_an_installed_plugin_root(
    installed: Path, tmp_path: Path
) -> None:
    searches = [command for command in router_commands() if "search_skills.py" in command]
    assert len(searches) == 2
    for command in searches:
        command = command.replace("<the user's task>", "molecular networking")
        result = _run(command, installed, tmp_path)
        assert result.returncode == 0, result.stdout + result.stderr
        assert str(installed) in result.stdout


def test_the_grounding_command_resolves_from_an_installed_plugin_root(
    installed: Path, tmp_path: Path
) -> None:
    [command] = [item for item in router_commands() if "perspicacite_kb_bind.py" in item]
    slug = next(iter(json.loads((installed / "kb_bundle.json").read_text())["skills"]))
    offline = re.sub(r' --question "[^"]*"', "", command).replace(" query ", " resolve ")
    offline = offline.replace("<slug>", slug)
    result = _run(offline, installed, tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert slug in result.stdout


def test_binder_docstring_names_the_installed_path() -> None:
    doc = BINDER.read_text(encoding="utf-8").split('"""', 2)[1]
    assert "python scripts/perspicacite_kb_bind.py" not in doc
    assert "collections/fixture/v1" not in doc
    assert f'python "{ROOT}/bin/perspicacite_kb_bind.py"' in doc


def test_fixture_binder_is_the_current_source() -> None:
    assert (V2 / "bin" / "perspicacite_kb_bind.py").read_bytes() == BINDER.read_bytes()
