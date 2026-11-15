"""A managed install writes an entry whose commands run as printed, on every host.

Measured on 2026-11-16 in OpenCode and Mistral Vibe: the entry of a managed
install told the reader to `cd` into the unit while the router it prefixed said
"do not `cd`", and its commands still carried `${CLAUDE_SKILL_DIR}`, which only
Claude Code fills in. In a copied entry the variable, even filled in, points at
the host's skills directory, not at the unit. The installer knows where the unit
is, so it writes that path into the commands.
"""

from __future__ import annotations

import json
import shlex
import shutil
import subprocess
from pathlib import Path

import pytest

from asb_skill_collections import asbb_cli
from asb_skill_collections.asbb.installer import install, uninstall
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import TARGETS, InstallOpts, generic_dest_target
from scripts import router_shape
from tests.test_asbb_installed_unit import make_pack
from tests.test_router_usable_anywhere import FIXTURE, PYTHON3, _commands


def _router_pack(repo: Path, slug: str = "fixture"):
    """A marketplace pack whose router has the released shape (`${CLAUDE_SKILL_DIR}` commands)."""
    source = repo / "packs" / slug
    shutil.copytree(FIXTURE, source, ignore=shutil.ignore_patterns("__pycache__"))
    router_shape.write_routers(source, rewrite=True)
    marketplace = repo / ".claude-plugin" / "marketplace.json"
    marketplace.parent.mkdir(parents=True, exist_ok=True)
    marketplace.write_text(
        json.dumps({"plugins": [{"name": slug, "version": "1", "source": f"packs/{slug}"}]})
    )
    return resolve_pack(repo, slug)


def _opts(tmp_path: Path, **kwargs) -> InstallOpts:
    home = tmp_path / "home"
    project = home / "project"
    project.mkdir(parents=True, exist_ok=True)
    return InstallOpts(home=home, project=project, **kwargs)


def _entry(target, opts: InstallOpts, name: str) -> Path:
    return target.dest(opts) / name / "SKILL.md"


@pytest.mark.skipif(PYTHON3 is None, reason="no python3 on PATH")
@pytest.mark.parametrize("runtime", ["agents", "opencode", "vibe", "dest"])
@pytest.mark.parametrize("copy", [False, True])
def test_bound_router_commands_run_as_printed(tmp_path: Path, runtime: str, copy: bool) -> None:
    pack = _router_pack(tmp_path / "checkout")
    opts = _opts(tmp_path, copy=copy, dest_override=tmp_path / "home" / "custom")
    target = generic_dest_target() if runtime == "dest" else TARGETS[runtime]
    [name] = install(pack, target, opts)
    text = _entry(target, opts, name).read_text(encoding="utf-8")
    assert router_shape.SKILL_DIR not in text
    assert "cd -- " not in text
    assert "do not `cd`" in text
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    queries = {"<the user's task>": "align retention time across samples",
               "<the user's goal>": "untargeted annotation"}
    ran = 0
    for command in _commands(text):
        if "search_skills.py" not in command or "<a tool name or task>" in command:
            continue
        for placeholder, query in queries.items():
            command = command.replace(placeholder, query)
        result = subprocess.run(shlex.split(command), cwd=elsewhere, capture_output=True,
                                text=True, timeout=120)
        assert result.returncode == 0, command + "\n" + result.stdout + result.stderr
        paths = [line.split("read:", 1)[1].strip() for line in result.stdout.splitlines()
                 if line.strip().startswith("read:")]
        assert paths and all(Path(path).is_file() for path in paths), result.stdout
        ran += 1
    assert ran >= 1
    uninstall(pack.slug, target, opts)
    assert not _entry(target, opts, name).exists()


def test_entry_of_a_root_relative_router_keeps_the_cd_instruction(tmp_path: Path) -> None:
    """A router that prints `python bin/…` needs the working directory; say so, as before."""
    pack = make_pack(tmp_path / "checkout")
    target = TARGETS["agents"]
    opts = _opts(tmp_path)
    install(pack, target, opts)
    text = _entry(target, opts, "_router").read_text(encoding="utf-8")
    assert "cd -- " in text
    assert "python bin/search_skills.py" in text


def test_unit_path_unsafe_in_double_quotes_is_not_written_into_commands(tmp_path: Path) -> None:
    pack = _router_pack(tmp_path / "checkout")
    opts = _opts(tmp_path, dest_override=tmp_path / "home" / "odd $dir")
    target = generic_dest_target()
    [name] = install(pack, target, opts)
    text = _entry(target, opts, name).read_text(encoding="utf-8")
    assert router_shape.SKILL_DIR in text
    assert "cd -- " in text


def test_opencode_and_vibe_destinations(tmp_path: Path) -> None:
    opts = _opts(tmp_path)
    assert TARGETS["opencode"].dest(opts) == opts.home / ".config" / "opencode" / "skills"
    assert TARGETS["vibe"].dest(opts) == opts.home / ".vibe" / "skills"
    moved = _opts(tmp_path, config_home=tmp_path / "xdg", vibe_home=tmp_path / "vibe")
    assert TARGETS["opencode"].dest(moved) == tmp_path / "xdg" / "opencode" / "skills"
    assert TARGETS["vibe"].dest(moved) == tmp_path / "vibe" / "skills"


def test_cli_reads_the_host_directories_from_the_environment(tmp_path: Path, monkeypatch, capsys) -> None:
    pack = _router_pack(tmp_path / "checkout")
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    monkeypatch.setenv("VIBE_HOME", str(tmp_path / "vibe"))
    for runtime, expected in (("opencode", tmp_path / "xdg" / "opencode" / "skills"),
                              ("vibe", tmp_path / "vibe" / "skills")):
        code = asbb_cli.main(["install", pack.slug, "--repo", str(tmp_path / "checkout"),
                              "--runtime", runtime, "--home", str(home), "--dry-run"])
        assert code == 0
        assert str(expected.resolve()) in capsys.readouterr().out
    monkeypatch.setenv("XDG_CONFIG_HOME", "relative/dir")
    monkeypatch.delenv("VIBE_HOME")
    code = asbb_cli.main(["install", pack.slug, "--repo", str(tmp_path / "checkout"),
                          "--runtime", "opencode", "--home", str(home), "--dry-run"])
    assert code == 0
    assert str((home / ".config" / "opencode" / "skills").resolve()) in capsys.readouterr().out


def test_entry_names_the_unit_first_and_the_installed_directory_for_a_move(tmp_path: Path) -> None:
    """A host that resolves a linked entry reads it inside the unit; the prose must hold there too."""
    pack = _router_pack(tmp_path / "checkout")
    target = TARGETS["agents"]
    opts = _opts(tmp_path)
    [name] = install(pack, target, opts)
    entry = _entry(target, opts, name)
    text = entry.read_text(encoding="utf-8")
    unit = json.loads(text.split("<!-- asbb-unit: ", 1)[1].split(" -->", 1)[0])
    start = text.index("## Installed pack location")
    preface = text[start:text.index("\n# ", start)]
    assert f"This pack's asset root is `{unit}`." in preface
    assert f"`{target.dest(opts).resolve() / name}`" in preface
    assert "resolved against the directory holding this file" not in preface
    physical = entry.resolve()
    assert Path(unit) in physical.parents and (Path(unit) / ".asbb-unit.json").is_file()


def test_cli_prints_what_opencode_still_needs(tmp_path: Path, monkeypatch, capsys) -> None:
    pack = _router_pack(tmp_path / "checkout")
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    argv = ["install", pack.slug, "--repo", str(tmp_path / "checkout"), "--home", str(home)]
    assert asbb_cli.main([*argv, "--runtime", "opencode"]) == 0
    out = capsys.readouterr().out
    units = home / ".config" / "opencode" / "skills" / ".asbb-units"
    assert f'"external_directory": {{"{units}/**": "allow"}}' in out
    assert asbb_cli.main([*argv, "--runtime", "agents"]) == 0
    assert "external_directory" not in capsys.readouterr().out
