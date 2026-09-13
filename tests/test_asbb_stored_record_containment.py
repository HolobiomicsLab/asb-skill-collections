"""A stored placement is untrusted input: it can never reach outside its root."""

import pytest

from asb_skill_collections.asbb import manifest
from asb_skill_collections.asbb.installer import install, uninstall
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import InstallOpts, generic_dest_target
from tests.test_asbb_install import make_repo

ESCAPES = {
    "parent": "../neighbour/personal.txt",
    "symlink-parent": "escape/personal.txt",
    "symlink-entry": "escape",
    "root": ".",
    "empty": "",
    "malformed": None,
}


@pytest.mark.parametrize("operation", ["uninstall", "reinstall"])
@pytest.mark.parametrize("escape", [*ESCAPES, "absolute"])
def test_a_stored_entry_outside_its_root_is_never_followed(
    tmp_path, capsys, operation, escape
):
    repo = make_repo(tmp_path / "repo", skills=("new-skill",))
    home, dest = tmp_path / "home", tmp_path / "dest"
    dest.mkdir()
    neighbour = tmp_path / "neighbour"
    neighbour.mkdir()
    victim = neighbour / "personal.txt"
    victim.write_text("keep neighbour")
    unmanaged = dest / "old-skill"
    unmanaged.write_text("keep until the record is validated")
    if escape == "symlink-parent":
        (dest / "escape").symlink_to(neighbour, target_is_directory=True)
    if escape == "symlink-entry":
        (dest / "escape").symlink_to(victim)
    entry = str(victim) if escape == "absolute" else ESCAPES[escape]
    manifest.save(
        home,
        {
            "demo-pack": {
                "dest": {
                    "dest_root": str(dest.resolve()),
                    "entries": ["old-skill", entry],
                    "mode": "copy",
                }
            }
        },
    )
    opts = InstallOpts(home=home, project=tmp_path, copy=True, dest_override=dest)
    if operation == "uninstall":
        uninstall("demo-pack", generic_dest_target(), opts)
    else:
        install(resolve_pack(repo, "demo-pack"), generic_dest_target(), opts)
    assert victim.read_text() == "keep neighbour"
    assert unmanaged.read_text() == "keep until the record is validated"
    assert "asbb: skipped" in capsys.readouterr().err
    if escape in ("symlink-parent", "symlink-entry"):
        assert (dest / "escape").is_symlink()


def test_a_stored_root_that_became_a_symlink_is_not_followed(tmp_path):
    repo = make_repo(tmp_path / "repo")
    opts = InstallOpts(
        home=tmp_path / "home", project=tmp_path, copy=True,
        dest_override=tmp_path / "dest",
    )
    target = generic_dest_target()
    install(resolve_pack(repo, "demo-pack"), target, opts)
    moved = tmp_path / "moved"
    opts.dest_override.rename(moved)
    opts.dest_override.symlink_to(moved, target_is_directory=True)
    with pytest.raises(ValueError, match="installed at"):
        uninstall("demo-pack", target, opts)
    assert (moved / "alpha-skill" / "SKILL.md").is_file()
