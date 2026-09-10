"""Stored placements are untrusted input, including during reinstall cleanup."""

from dataclasses import replace

import pytest

from asb_skill_collections.asbb import manifest
from asb_skill_collections.asbb.installer import install, uninstall
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import InstallOpts, generic_dest_target
from asb_skill_collections.asbb_cli import main
from tests.test_asbb_install import make_repo


@pytest.mark.parametrize("operation", ["uninstall", "sync"])
@pytest.mark.parametrize("escape", ["parent", "absolute", "symlink-parent", "symlink-entry",
                                    "root", "empty", "malformed"])
def test_stored_escape_is_refused_before_any_mutation(tmp_path, operation, escape):
    repo = make_repo(tmp_path / "repo", skills=("new-skill",))
    home, dest = tmp_path / "home", tmp_path / "dest"
    dest.mkdir()
    neighbor = tmp_path / "neighbor"
    neighbor.mkdir()
    victim = neighbor / "personal.txt"
    victim.write_text("keep neighbor")
    ordinary = dest / "old-skill"
    ordinary.write_text("keep until record validated")
    if escape == "symlink-parent":
        (dest / "escape").symlink_to(neighbor, target_is_directory=True)
    if escape == "symlink-entry":
        (dest / "escape").symlink_to(victim)
    entries = {"parent": "../neighbor/personal.txt", "absolute": str(victim),
               "symlink-parent": "escape/personal.txt", "symlink-entry": "escape",
               "root": ".", "empty": "", "malformed": None}
    manifest.save(home, {"demo-pack": {"dest": {
        "dest_root": str(dest), "entries": ["old-skill", entries[escape]], "mode": "copy"
    }}})
    before = manifest.manifest_path(home).read_bytes()
    opts = InstallOpts(home=home, project=tmp_path, copy=True, dest_override=dest)
    with pytest.raises(ValueError):
        if operation == "uninstall":
            uninstall("demo-pack", generic_dest_target(), opts)
        else:
            install(resolve_pack(repo, "demo-pack"), generic_dest_target(), opts)
    assert victim.read_text() == "keep neighbor"
    assert ordinary.read_text() == "keep until record validated"
    assert not (dest / "new-skill").exists()
    assert manifest.manifest_path(home).read_bytes() == before


def test_install_refuses_destination_symlink_parent_even_with_force(tmp_path):
    repo = make_repo(tmp_path / "repo")
    dest, neighbor = tmp_path / "dest", tmp_path / "neighbor"
    dest.mkdir()
    neighbor.mkdir()
    (neighbor / "personal.txt").write_text("keep")
    (dest / "escape").symlink_to(neighbor, target_is_directory=True)
    from asb_skill_collections.asbb.targets import get_target
    target = replace(get_target("cline"), dest=lambda o: dest,
                     filename=lambda name: f"escape/{name}.md")
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path, force=True)
    with pytest.raises(ValueError):
        install(resolve_pack(repo, "demo-pack"), target, opts)
    assert list(neighbor.iterdir()) == [neighbor / "personal.txt"]


def test_tampered_managed_symlink_is_refused(tmp_path):
    repo = make_repo(tmp_path / "repo", skills=("alpha-skill",))
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path,
                       dest_override=tmp_path / "dest")
    target = generic_dest_target()
    install(resolve_pack(repo, "demo-pack"), target, opts)
    neighbor = tmp_path / "personal.txt"
    neighbor.write_text("keep")
    link = opts.dest_override / "alpha-skill"
    link.unlink()
    link.symlink_to(neighbor)
    with pytest.raises(ValueError):
        uninstall("demo-pack", target, opts)
    assert link.is_symlink() and neighbor.read_text() == "keep"


def test_uninstall_dry_run_keeps_files_and_manifest(tmp_path):
    repo = make_repo(tmp_path / "repo")
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path, copy=True,
                       dest_override=tmp_path / "dest")
    target = generic_dest_target()
    install(resolve_pack(repo, "demo-pack"), target, opts)
    before = manifest.manifest_path(opts.home).read_bytes()
    opts.dry_run = True
    assert uninstall("demo-pack", target, opts)
    assert (opts.dest_override / "alpha-skill" / "SKILL.md").exists()
    assert manifest.manifest_path(opts.home).read_bytes() == before


def test_cli_reports_unsafe_uninstall_without_traceback(tmp_path, capsys):
    dest = tmp_path / "dest"
    dest.mkdir()
    home = tmp_path / "home"
    victim = tmp_path / "personal.txt"
    victim.write_text("keep")
    manifest.record(home, "demo", "dest", dest, ["../personal.txt"], "copy")
    assert main(["uninstall", "demo", "--dest", str(dest), "--home", str(home)]) == 1
    assert "refusing" in capsys.readouterr().err
    assert victim.read_text() == "keep"
