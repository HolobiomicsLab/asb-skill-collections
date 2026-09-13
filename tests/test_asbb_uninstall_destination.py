"""An explicit --dest must name the installation that is being removed."""

import pytest

from asb_skill_collections.asbb.installer import install, uninstall
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import InstallOpts, generic_dest_target
from tests.test_asbb_install import make_repo


def _install(tmp_path, dest):
    repo = make_repo(tmp_path / "repo")
    opts = InstallOpts(
        home=tmp_path / "home", project=tmp_path, copy=True, dest_override=dest
    )
    install(resolve_pack(repo, "demo-pack"), generic_dest_target(), opts)
    return opts


def test_uninstall_refuses_a_destination_other_than_the_recorded_one(tmp_path):
    installed = tmp_path / "installed"
    opts = _install(tmp_path, installed)
    opts.dest_override = tmp_path / "elsewhere"
    with pytest.raises(ValueError, match="installed at"):
        uninstall("demo-pack", generic_dest_target(), opts)
    assert (installed / "alpha-skill" / "SKILL.md").is_file()
    assert not (tmp_path / "elsewhere").exists()


def test_uninstall_removes_the_recorded_destination(tmp_path):
    installed = tmp_path / "installed"
    opts = _install(tmp_path, installed)
    assert sorted(uninstall("demo-pack", generic_dest_target(), opts)) == [
        "alpha-skill",
        "beta-skill",
    ]
    assert not (installed / "alpha-skill").exists()
