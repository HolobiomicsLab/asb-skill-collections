"""The metabolomics v2 router's commands run from an installed plugin root.

The router told agents to run ``python scripts/perspicacite_kb_bind.py ...
--collection collections/metabolomics/v2``: a path of this repository, not of
the installed plugin, which ships the binder as ``bin/perspicacite_kb_bind.py``
and is itself the collection root. The router's three commands now name every
path under a ``<collection root>`` placeholder, and the binder's docstring does
the same. Each command is run here from a copy of the plugin, with the
placeholder filled in and a working directory outside it.
"""

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
V2 = REPO / "collections" / "metabolomics" / "v2"
ROUTER = V2 / "skills" / "_router" / "SKILL.md"
BINDER = REPO / "scripts" / "perspicacite_kb_bind.py"
ROOT = "<collection root>"


def router_commands() -> list[str]:
    """Every ``python ...`` command in the router's bash blocks, continuations joined."""
    text = ROUTER.read_text(encoding="utf-8")
    commands = []
    for block in re.findall(r"```bash\n(.*?)```", text, re.S):
        joined = block.replace("\\\n", " ")
        commands += [line.strip() for line in joined.splitlines() if line.strip().startswith("python ")]
    return commands


@pytest.fixture(scope="module")
def installed(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The files the three commands read, at a path unrelated to this repository."""
    root = tmp_path_factory.mktemp("plugins") / "metabolomics"
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
        [sys.executable, *argv[1:]], cwd=cwd, capture_output=True, text=True, timeout=120
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
    searches = [c for c in router_commands() if "search_skills.py" in c]
    assert len(searches) == 2

    for command in searches:
        command = command.replace("<the user's task>", "molecular networking")
        result = _run(command, installed, tmp_path)
        assert result.returncode == 0, result.stdout + result.stderr
        assert str(installed) in result.stdout


def test_the_grounding_command_resolves_from_an_installed_plugin_root(
    installed: Path, tmp_path: Path
) -> None:
    [command] = [c for c in router_commands() if "perspicacite_kb_bind.py" in c]
    slug = next(iter(json.loads((installed / "kb_bundle.json").read_text("utf-8"))["skills"]))
    # `query` needs a Perspicacité server; `resolve` takes the same path and
    # --collection arguments and answers offline.
    offline = re.sub(r' --question "[^"]*"', "", command).replace(" query ", " resolve ")
    offline = offline.replace("<slug>", slug)

    result = _run(offline, installed, tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr
    assert slug in result.stdout


def test_binder_docstring_names_the_installed_path() -> None:
    doc = BINDER.read_text(encoding="utf-8").split('"""', 2)[1]

    assert "python scripts/perspicacite_kb_bind.py" not in doc
    assert "collections/metabolomics/v2" not in doc
    assert f'python "{ROOT}/bin/perspicacite_kb_bind.py"' in doc


def test_every_shipped_binder_is_the_current_source() -> None:
    copies = [V2 / "bin" / "perspicacite_kb_bind.py"]
    copies += sorted(REPO.glob("packs/*/*/bin/perspicacite_kb_bind.py"))
    assert len(copies) > 1

    stale = [str(c.relative_to(REPO)) for c in copies if c.read_bytes() != BINDER.read_bytes()]
    assert not stale, stale
