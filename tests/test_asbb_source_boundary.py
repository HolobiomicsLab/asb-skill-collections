"""Malformed marketplace inputs must fail before reading or copying outsiders."""

import json
from dataclasses import replace

import pytest

from asb_skill_collections.asbb.installer import install
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import InstallOpts, generic_dest_target, get_target
from asb_skill_collections.asbb_cli import main
from tests.test_asbb_install import make_repo


@pytest.mark.parametrize("escape", ["parent", "absolute", "symlink"])
def test_marketplace_source_cannot_leave_checkout(tmp_path, escape):
    repo = make_repo(tmp_path / "repo")
    private = tmp_path / "private-unit"
    (private / "skills" / "secret").mkdir(parents=True)
    (private / "skills" / "secret" / "SKILL.md").write_text("private procedure")
    (repo / "external").symlink_to(private, target_is_directory=True)
    source = {"parent": "../private-unit", "absolute": str(private),
              "symlink": "external"}[escape]
    (repo / ".claude-plugin" / "marketplace.json").write_text(json.dumps({
        "plugins": [{"name": "demo-pack", "source": source}]
    }))
    with pytest.raises(ValueError):
        resolve_pack(repo, "demo-pack")
    assert main(["install", "demo-pack", "--repo", str(repo),
                 "--dest", str(tmp_path / "dest"), "--home", str(tmp_path / "home")]) == 1
    assert not (tmp_path / "dest").exists()


def test_source_metadata_symlink_cannot_read_outside_unit(tmp_path):
    # resolve_pack reads only .claude-plugin/plugin.json, so a pack file aliased
    # to an outsider is refused where it would first be read: taking the source
    # inventory, before the destination or the receipt exist.
    repo = make_repo(tmp_path / "repo")
    metadata = tmp_path / "private.yaml"
    metadata.write_text('version: "private-marker"\n')
    (repo / "packs/demo/pack/collection.yaml").symlink_to(metadata)
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path, copy=True,
                       dest_override=tmp_path / "dest")
    with pytest.raises(ValueError):
        install(resolve_pack(repo, "demo-pack"), generic_dest_target(), opts)
    assert not (tmp_path / "dest").exists()
    assert not (tmp_path / "home").exists()


def test_descriptor_symlink_is_refused_when_the_pack_is_resolved(tmp_path):
    repo = make_repo(tmp_path / "repo")
    outside = tmp_path / "private.json"
    outside.write_text('{"version": "private-marker"}')
    (repo / "packs/demo/pack/.claude-plugin").mkdir(parents=True)
    (repo / "packs/demo/pack/.claude-plugin/plugin.json").symlink_to(outside)
    with pytest.raises(ValueError):
        resolve_pack(repo, "demo-pack")


@pytest.mark.parametrize("overlap", ["unit-parent", "duplicate", "ancestor"])
def test_overlapping_planned_entries_are_refused(tmp_path, overlap):
    skills = (".asbb-units",) if overlap == "unit-parent" else ("alpha", "beta")
    repo = make_repo(tmp_path / "repo", skills=skills)
    dest = tmp_path / "dest"
    target = generic_dest_target()
    if overlap == "duplicate":
        target = replace(get_target("cline"), dest=lambda o: dest,
                         filename=lambda name: "same.md")
    if overlap == "ancestor":
        target = replace(get_target("cline"), dest=lambda o: dest,
                         filename=lambda name: "rules" if name == "alpha" else "rules/beta.md")
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path, copy=True,
                       dest_override=dest)
    with pytest.raises(ValueError):
        install(resolve_pack(repo, "demo-pack"), target, opts)
    assert not dest.exists()
    assert not opts.home.exists()
