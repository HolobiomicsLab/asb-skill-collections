"""Preflight must separate source trees and unrelated historical placements."""

import pytest

from asb_skill_collections.asbb import manifest
from asb_skill_collections.asbb.installer import install
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import InstallOpts, generic_dest_target
from tests.test_asbb_install import make_repo


def test_unrelated_legacy_symlink_does_not_block_install(tmp_path):
    repo = make_repo(tmp_path / "repo")
    home = tmp_path / "home"
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    legacy_source = tmp_path / "legacy-source"
    legacy_source.mkdir()
    link = legacy / "legacy-entry"
    link.symlink_to(legacy_source, target_is_directory=True)
    manifest.record(home, "legacy", "dest", legacy, ["legacy-entry"], "symlink")
    opts = InstallOpts(home=home, project=tmp_path, copy=True,
                       dest_override=tmp_path / "new-destination")
    install(resolve_pack(repo, "demo-pack"), generic_dest_target(), opts)
    assert link.is_symlink() and link.resolve() == legacy_source
    assert (opts.dest_override / "alpha-skill" / "SKILL.md").exists()


@pytest.mark.parametrize("destination", ["same", "ancestor", "descendant"])
def test_overlapping_source_and_destination_is_refused(tmp_path, destination):
    repo = make_repo(tmp_path / "repo", skills=("alpha-skill",))
    pack = resolve_pack(repo, "demo-pack")
    source = pack.skills_dir.parent
    dest = {"same": source, "ancestor": source.parent,
            "descendant": source / "nested-destination"}[destination]
    original = (pack.skills_dir / "alpha-skill" / "SKILL.md").read_bytes()
    opts = InstallOpts(home=tmp_path / "home", project=tmp_path,
                       copy=True, dest_override=dest)
    with pytest.raises(ValueError):
        install(pack, generic_dest_target(), opts)
    assert (pack.skills_dir / "alpha-skill" / "SKILL.md").read_bytes() == original
    assert not (dest / ".asbb-units").exists()
    assert not manifest.manifest_path(opts.home).exists()
