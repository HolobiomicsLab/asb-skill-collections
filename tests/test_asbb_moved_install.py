"""An installation moved on disk stays locatable, and stays removable.

Every installed entry used to carry exactly one statement of where its assets
are: an absolute path, written at install time. Moving the destination — the one
thing a user does to a directory of skills — falsified it, and the entry's own
documented first step then named a directory that no longer existed. The
management side dead-ended in the same place: the record still named the old
root, so ``uninstall --dest <new>`` refused, ``install --dest <new>`` refused as
unowned, and the only accepted command was an uninstall aimed at a path that was
gone, which emptied the manifest and left the copy orphaned on disk.

These tests pin both halves: the entry locates its unit from its own directory,
and the ownership check recognises a moved unit as the same unit.
"""

import re
import shlex
import shutil
import subprocess
from pathlib import Path

import pytest

from asb_skill_collections.asbb import manifest
from asb_skill_collections.asbb.installer import install, uninstall
from asb_skill_collections.asbb.targets import TARGETS, generic_dest_target
from asb_skill_collections.asbb.units import (
    RECEIPT_FILE,
    RELATIVE_MARKER,
    UNITS_DIR,
    unit_from_entry,
)
from tests.test_asbb_installed_unit import (
    entry_path,
    installed_root,
    make_pack,
    opts_for,
)


def move_destination(target, opts, entry):
    """Rename the whole install root and return the new root and entry path."""
    dest = target.dest(opts)
    moved = dest.with_name(dest.name + "-moved")
    dest.rename(moved)
    return moved, moved / entry.relative_to(dest)


@pytest.mark.parametrize("runtime", ["agents", "cursor", "dest"])
@pytest.mark.parametrize("copy", [False, True])
def test_entry_locates_its_unit_after_the_install_root_moves(tmp_path, runtime, copy):
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path, copy=copy, dest_override=tmp_path / "home" / "custom")
    target = generic_dest_target() if runtime == "dest" else TARGETS[runtime]
    install(pack, target, opts)
    entry = entry_path(target, opts)
    unit = installed_root(entry)

    # The relative marker is derived from where the entry actually lands: skill
    # entries are directories beside `.asbb-units`, rules entries are files in
    # the destination itself, and a fixed `../` would miss one of the two.
    hop = "../" if target.kind == "skill" else ""
    assert RELATIVE_MARKER.search(entry.read_text())[1] == (
        f'"{hop}{UNITS_DIR}/{unit.name}"'
    )

    moved_root, moved_entry = move_destination(target, opts, entry)
    # Without this the test would pass on the absolute marker alone.
    assert not unit.exists()

    found = unit_from_entry(moved_entry)
    assert found is not None, "a moved entry must still locate its own asset root"
    assert found.is_relative_to(moved_root)
    assert (found / RECEIPT_FILE).is_file()
    assert (found / "skills_index.json").is_file()
    assert (found / "leaves/signal/SKILL.md").is_file()


@pytest.mark.parametrize("copy", [False, True])
def test_documented_first_step_reaches_the_unit_after_a_move(tmp_path, copy):
    """Run the entry's own `cd` block, verbatim, from the new location."""
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path, copy=copy)
    target = TARGETS["agents"]
    install(pack, target, opts)
    entry = entry_path(target, opts)
    _, moved_entry = move_destination(target, opts, entry)

    block = re.search(r"```sh\n(.*?)```", moved_entry.read_text(), re.DOTALL)[1]
    # The block's only parameter is ENTRY: the path the reader read the file
    # from. Everything else about the command has to survive the move unaided.
    script = re.sub(
        r"^ENTRY=.*$", f"ENTRY={shlex.quote(str(moved_entry))}", block, flags=re.M
    )
    landed = subprocess.run(
        ["sh", "-c", f"set -e\n{script}\npwd\n"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert Path(landed.stdout.strip()).resolve() == unit_from_entry(moved_entry)


def test_an_entry_with_only_the_legacy_absolute_marker_still_resolves(tmp_path):
    """Installations written before the relative marker must keep working."""
    pack = make_pack(tmp_path / "repo")
    opts = opts_for(tmp_path, copy=True)
    target = TARGETS["agents"]
    install(pack, target, opts)
    entry = entry_path(target, opts)
    unit = installed_root(entry)
    entry.write_text(RELATIVE_MARKER.sub("", entry.read_text()))
    assert unit_from_entry(entry) == unit


@pytest.mark.parametrize("copy", [False, True])
def test_moved_install_uninstalls_from_its_new_destination(tmp_path, copy):
    pack = make_pack(tmp_path / "repo")
    first = tmp_path / "home" / "first"
    opts = opts_for(tmp_path, copy=copy, dest_override=first)
    target = generic_dest_target()
    install(pack, target, opts)
    second = first.with_name("second")
    first.rename(second)
    opts.dest_override = second

    assert uninstall(pack.slug, target, opts) == ["_router"]
    assert manifest.load(opts.home) == {}
    assert list(second.iterdir()) == [], "the moved installation must leave no orphan"
    assert not first.exists()


def test_moved_install_reinstalls_at_its_new_destination(tmp_path):
    pack = make_pack(tmp_path / "repo")
    first = tmp_path / "home" / "first"
    opts = opts_for(tmp_path, copy=True, dest_override=first)
    target = generic_dest_target()
    install(pack, target, opts)
    second = first.with_name("second")
    first.rename(second)
    opts.dest_override = second

    install(pack, target, opts)  # no --force: the moved unit is recognised as ours
    rec = manifest.get(opts.home, pack.slug, target.id)
    assert rec["dest_root"] == str(second)
    assert rec["retained_units"] == [], "the root it moved from must not be retained"
    assert sorted(p.name for p in second.iterdir()) == [UNITS_DIR, "_router"]
    entry = second / "_router" / "SKILL.md"
    assert installed_root(entry).is_relative_to(second)
    assert uninstall(pack.slug, target, opts) == ["_router"]
    assert list(second.iterdir()) == []


def test_a_copy_of_the_installation_is_not_a_move(tmp_path):
    """The original still standing is what separates a copy from a move."""
    pack = make_pack(tmp_path / "repo")
    first = tmp_path / "home" / "first"
    opts = opts_for(tmp_path, copy=True, dest_override=first)
    target = generic_dest_target()
    install(pack, target, opts)
    second = first.with_name("second")
    shutil.copytree(first, second)
    opts.dest_override = second

    with pytest.raises(ValueError, match="installed at"):
        uninstall(pack.slug, target, opts)
    with pytest.raises(FileExistsError):
        install(pack, target, opts)
    assert (second / "_router" / "SKILL.md").is_file()
    assert (first / "_router" / "SKILL.md").is_file()
    assert manifest.get(opts.home, pack.slug, target.id)["dest_root"] == str(first)


def test_a_lookalike_unit_at_the_named_destination_is_not_the_moved_one(tmp_path):
    """Identity, not resemblance: a different revision cannot stand in."""
    repo = tmp_path / "repo"
    pack = make_pack(repo)
    first = tmp_path / "home" / "first"
    opts = opts_for(tmp_path, copy=True, dest_override=first)
    target = generic_dest_target()
    install(pack, target, opts)
    second = first.with_name("second")
    opts.dest_override = second
    install(make_pack(repo, version="2"), target, opts)
    shutil.rmtree(first)

    # The record now names `second`; restore a record naming the vanished
    # `first`, so the only thing standing between the two is the receipt.
    data = manifest.load(opts.home)
    data[pack.slug][target.id]["dest_root"] = str(first)
    manifest.save(opts.home, data)
    kept = sorted(p.name for p in second.iterdir())

    with pytest.raises(ValueError, match="installed at"):
        uninstall(pack.slug, target, opts)
    assert sorted(p.name for p in second.iterdir()) == kept
