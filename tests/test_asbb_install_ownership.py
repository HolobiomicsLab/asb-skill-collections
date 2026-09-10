"""Independent owners and source assets must not broaden a placement's scope."""

import shutil

import pytest

from asb_skill_collections.asbb import manifest
from asb_skill_collections.asbb.installer import install, uninstall
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import InstallOpts, generic_dest_target
from asb_skill_collections.asbb_cli import main
from tests.test_asbb_install import make_repo
from tests.test_asbb_installed_unit import make_unit


@pytest.mark.parametrize("operation", ["install", "uninstall", "sync"])
def test_other_owner_prevents_overwrite_or_cleanup_even_with_force(tmp_path, operation):
    repo = make_repo(tmp_path / "repo", skills=("owned-skill",))
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path, copy=True,
                       force=True, dest_override=tmp_path / "dest")
    dest = opts.dest_override
    dest.mkdir()
    (dest / "owned-skill").mkdir()
    sentinel = dest / "owned-skill" / "personal.txt"
    sentinel.write_text("belongs to another installation")
    manifest.record(opts.home, "another-owner", "dest", dest, ["owned-skill"], "copy")
    if operation != "install":
        manifest.record(opts.home, "demo-pack", "dest", dest, ["owned-skill"], "copy")
    if operation == "sync":
        (repo / "packs/demo/pack/skills/owned-skill").rename(
            repo / "packs/demo/pack/skills/new-skill"
        )
    before = manifest.manifest_path(opts.home).read_bytes()
    with pytest.raises((ValueError, FileExistsError)):
        if operation == "uninstall":
            uninstall("demo-pack", generic_dest_target(), opts)
        else:
            install(resolve_pack(repo, "demo-pack"), generic_dest_target(), opts)
    assert sentinel.read_text() == "belongs to another installation"
    assert manifest.manifest_path(opts.home).read_bytes() == before
    assert not (dest / "new-skill").exists()


@pytest.mark.parametrize("operation", ["uninstall", "sync"])
def test_changed_destination_is_refused(tmp_path, operation):
    repo = make_repo(tmp_path / "repo")
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path, copy=True,
                       dest_override=tmp_path / "original")
    target = generic_dest_target()
    pack = resolve_pack(repo, "demo-pack")
    install(pack, target, opts)
    original = opts.dest_override
    opts.dest_override = tmp_path / "another-root"
    with pytest.raises(ValueError):
        if operation == "uninstall":
            uninstall("demo-pack", target, opts)
        else:
            install(pack, target, opts)
    assert (original / "alpha-skill" / "SKILL.md").is_file()
    assert not opts.dest_override.exists()


def test_replaced_destination_root_symlink_is_refused(tmp_path):
    repo = make_repo(tmp_path / "repo")
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path, copy=True,
                       dest_override=tmp_path / "dest")
    target = generic_dest_target()
    install(resolve_pack(repo, "demo-pack"), target, opts)
    moved = tmp_path / "moved"
    opts.dest_override.rename(moved)
    opts.dest_override.symlink_to(moved, target_is_directory=True)
    with pytest.raises(ValueError):
        uninstall("demo-pack", target, opts)
    assert (moved / "alpha-skill" / "SKILL.md").is_file()


def test_copy_refuses_external_source_asset_before_writes(tmp_path):
    repo = tmp_path / "repo"
    source = make_unit(repo)
    private = tmp_path / "private.txt"
    private.write_text("private outside the source unit")
    (source / "bin" / "external.txt").symlink_to(private)
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path, copy=True,
                       dest_override=tmp_path / "dest")
    with pytest.raises(ValueError):
        install(resolve_pack(repo, "example-unit"), generic_dest_target(), opts)
    assert not opts.dest_override.exists()
    assert not opts.home.exists()


def test_cli_user_root_and_uninstall_dry_run(tmp_path, monkeypatch):
    repo = make_repo(tmp_path / "repo")
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    home = tmp_path / "home"
    args = ["demo-pack", "--runtime", "claude", "--user", "--home", str(home)]
    assert main(["install", *args, "--repo", str(repo), "--copy"]) == 0
    before = manifest.manifest_path(home).read_bytes()
    assert main(["uninstall", *args, "--dry-run"]) == 0
    assert manifest.manifest_path(home).read_bytes() == before
    assert main(["uninstall", *args]) == 0
    assert not (home / ".claude/skills/alpha-skill").exists()


def test_legacy_copy_record_upgrades_to_complete_unit(tmp_path):
    repo = tmp_path / "repo"
    source = make_unit(repo)
    dest = tmp_path / "dest"
    shutil.copytree(source / "skills" / "entry-point", dest / "entry-point")
    home = tmp_path / "home"
    manifest.record(home, "example-unit", "dest", dest, ["entry-point"], "copy")
    opts = InstallOpts(home=home, project=tmp_path, copy=True, dest_override=dest)
    install(resolve_pack(repo, "example-unit"), generic_dest_target(), opts)
    assert (dest / ".asbb-units/example-unit/bin/search_skills.py").is_file()
    assert manifest.get(home, "example-unit", "dest")["source"]["version"] == "3.2.1"
