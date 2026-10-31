"""An advertised skill is installed under its frontmatter name.

Every pack and collection ships its router as ``skills/_router/``, whose
frontmatter name is the unit's own (``metabolomics-collection-router``,
``metabolomics-lc-ms-router``, ...). Skill-native hosts expect a skill's
directory to carry its name, and two units installed under ``_router`` would
collide on one path. The source directory stays ``_router``, which the Claude
plugin layout relies on; only the installed entry is renamed.
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from asb_skill_collections.asbb import installer, manifest  # noqa: E402
from asb_skill_collections.asbb.repo import resolve_pack  # noqa: E402
from asb_skill_collections.asbb.targets import TARGETS, InstallOpts  # noqa: E402
from asb_skill_collections.asbb_cli import main  # noqa: E402


def _pack(repo: pathlib.Path, slug: str, entries: dict[str, str]):
    """A pack advertising ``entries`` (directory name -> frontmatter name)."""
    marketplace = repo / ".claude-plugin" / "marketplace.json"
    marketplace.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(marketplace.read_text()) if marketplace.exists() else {"plugins": []}
    data["plugins"].append({"name": slug, "version": "1", "source": f"packs/{slug}"})
    marketplace.write_text(json.dumps(data))
    source = repo / "packs" / slug
    for directory, name in entries.items():
        skill = source / "skills" / directory / "SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text(f"---\nname: {name}\ndescription: Route {slug}.\n---\n\nRoute.\n")
    (source / "leaves" / "signal").mkdir(parents=True)
    (source / "leaves" / "signal" / "SKILL.md").write_text("# signal\n")
    return resolve_pack(repo, slug)


def _opts(tmp_path, **kwargs):
    home = tmp_path / "home"
    (home / "project").mkdir(parents=True, exist_ok=True)
    return InstallOpts(home=home, project=home / "project", **kwargs)


def test_the_router_is_installed_under_its_frontmatter_name(tmp_path):
    pack = _pack(tmp_path / "repo", "stellar", {"_router": "stellar-collection-router"})
    opts = _opts(tmp_path)
    target = TARGETS["agents"]

    assert installer.install(pack, target, opts) == ["stellar-collection-router"]

    dest = target.dest(opts)
    assert sorted(p.name for p in dest.iterdir() if not p.name.startswith(".")) == [
        "stellar-collection-router"]
    entry = dest / "stellar-collection-router" / "SKILL.md"
    assert "name: stellar-collection-router" in entry.read_text()
    assert "`skills/_router/SKILL.md`" in entry.read_text()
    assert (pack.skills_dir / "_router" / "SKILL.md").is_file()


def test_two_routers_share_one_destination(tmp_path):
    repo = tmp_path / "repo"
    first = _pack(repo, "stellar", {"_router": "stellar-router"})
    second = _pack(repo, "radio", {"_router": "radio-router"})
    opts = _opts(tmp_path)
    target = TARGETS["agents"]

    installer.install(first, target, opts)
    installer.install(second, target, opts)

    dest = target.dest(opts)
    assert (dest / "stellar-router" / "SKILL.md").is_file()
    assert (dest / "radio-router" / "SKILL.md").is_file()
    assert installer.uninstall("stellar", target, opts) == ["stellar-router"]
    assert (dest / "radio-router" / "SKILL.md").is_file()


def test_a_rules_entry_is_named_after_the_frontmatter_too(tmp_path):
    pack = _pack(tmp_path / "repo", "stellar", {"_router": "stellar-router"})
    opts = _opts(tmp_path)

    assert installer.install(pack, TARGETS["cursor"], opts) == ["stellar-router.mdc"]


@pytest.mark.parametrize("name", ("_router", "Not A Name", "../escape", ""),
                         ids=("underscore", "spaces", "traversal", "empty"))
def test_a_frontmatter_name_that_is_not_a_skill_name_keeps_the_directory(tmp_path, name):
    pack = _pack(tmp_path / "repo", "stellar", {"_router": name})

    assert installer.install(pack, TARGETS["agents"], _opts(tmp_path)) == ["_router"]


def test_a_reinstall_retires_the_entry_installed_under_the_directory_name(
    tmp_path, monkeypatch, capsys
):
    """An install made before this rename is replaced cleanly, with no orphan."""
    pack = _pack(tmp_path / "repo", "stellar", {"_router": "stellar-router"})
    opts = _opts(tmp_path)
    target = TARGETS["agents"]
    dest = target.dest(opts)
    with monkeypatch.context() as earlier:
        earlier.setattr(installer, "_entry_name", lambda fm, directory: directory)
        assert installer.install(pack, target, opts) == ["_router"]
    assert (dest / "_router").is_symlink()

    assert installer.install(pack, target, opts) == ["stellar-router"]

    assert "skipped" not in capsys.readouterr().err
    assert not (dest / "_router").exists() and not (dest / "_router").is_symlink()
    assert (dest / "stellar-router" / "SKILL.md").is_file()
    assert manifest.get(opts.home, "stellar", "agents")["entries"] == ["stellar-router"]
    assert installer.uninstall("stellar", target, opts) == ["stellar-router"]
    assert sorted(p.name for p in dest.iterdir()) == []


def test_the_shipped_collection_installs_its_router_under_its_name(tmp_path, capsys):
    rc = main(["install", "metabolomics", "--runtime", "agents", "--repo", str(REPO_ROOT),
               "--home", str(tmp_path), "--dry-run"])

    out = capsys.readouterr().out
    assert rc == 0
    dest = tmp_path.resolve() / ".agents" / "skills"
    assert f"would write {dest / 'metabolomics-collection-router'}" in out
    assert f"would write {dest / '_router'}" not in out
