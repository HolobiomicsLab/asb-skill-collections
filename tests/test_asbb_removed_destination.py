"""A destination the user deleted must leave the manifest, not haunt it.

Cleaning an entry validated ownership before looking at the entry, and
:func:`_owned_entry` establishes ownership by reading the unit receipt kept
*inside the destination*. So a destination the user removed by hand took the
proof of ownership with it, and every entry raised ``FileNotFoundError``. Two
consequences followed, and only the first was visible:

* the user saw one ``asbb: skipped <entry>: [Errno 2] No such file or
  directory: …/.asbb-units/<digest>/.asbb-unit.json`` per entry, naming a path
  they no longer had; and
* because a skipped entry stays in ``entries``, the snapshot was never dropped,
  so **every later install of that pack reprinted the same errors** — for as
  long as the manifest lived.

Observed on the real manifest before the fix: three skip lines on an install
into an unrelated destination, repeated on every subsequent install.

An entry that is already gone is already cleaned, so the check is now "is
anything there?" first. The assertions are two-sided on purpose: the record has
to be dropped *and* the safety it was protecting has to survive — a destination
that still holds an entry the installer cannot prove it owns must still be
refused, and a dangling symlink must still count as present.
"""

import json

import pytest

from asb_skill_collections.asbb import manifest
from asb_skill_collections.asbb.installer import install, uninstall
from asb_skill_collections.asbb.repo import resolve_pack
from asb_skill_collections.asbb.targets import InstallOpts, generic_dest_target
from tests.test_asbb_install import make_repo

SKILLS = ("alpha-skill", "beta-skill")


def _opts(home, project, dest):
    return InstallOpts(home=home, project=project, copy=True, dest_override=dest)


def _install(tmp_path, dest, *, home=None, repo=None):
    """Install the demo pack into `dest` and return (home, repo)."""
    home = home or tmp_path / "home"
    repo = repo or make_repo(tmp_path / "repo", skills=SKILLS)
    dest.mkdir(parents=True, exist_ok=True)
    install(
        resolve_pack(repo, "demo-pack"),
        generic_dest_target(),
        _opts(home, tmp_path, dest),
    )
    return home, repo


def _record(home, slug="demo-pack"):
    return manifest.load(home).get(slug, {}).get("dest")


def _roots(rec):
    return [rec["dest_root"], *(s["dest_root"] for s in rec.get("retained_units", ()))]


# --------------------------------------------------------------------------- #
# The defect: a removed destination retained forever, re-reported every time.  #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("how", ["whole-tree", "contents-only"])
def test_a_removed_destination_is_dropped_from_the_manifest(tmp_path, capsys, how):
    """Both shapes a user produces by hand, since they fail the same way.

    ``rm -rf dest`` takes the root as well; ``rm -rf dest/*`` leaves an empty
    directory behind. The receipt is gone either way, which is all the old code
    touched, so a fix keyed on the root's existence would repair only one.
    """
    import shutil

    first, second = tmp_path / "old-dest", tmp_path / "new-dest"
    home, repo = _install(tmp_path, first)
    assert (first / "alpha-skill").exists()

    shutil.rmtree(first)
    if how == "contents-only":
        first.mkdir()

    capsys.readouterr()
    _install(tmp_path, second, home=home, repo=repo)
    err = capsys.readouterr().err
    assert "asbb: skipped" not in err, err
    assert str(first) not in err, "a path the user deleted must not be reported"

    rec = _record(home)
    assert rec["dest_root"] == str(second.resolve())
    assert rec.get("retained_units", []) == [], (
        "the snapshot for a destination that no longer exists must not be kept"
    )


def test_the_stale_record_does_not_come_back_on_the_next_install(tmp_path, capsys):
    """The half that was invisible: the errors repeated on *every* later install."""
    import shutil

    first, second = tmp_path / "old-dest", tmp_path / "new-dest"
    home, repo = _install(tmp_path, first)
    shutil.rmtree(first)
    _install(tmp_path, second, home=home, repo=repo)

    capsys.readouterr()
    _install(tmp_path, second, home=home, repo=repo)
    assert capsys.readouterr().err == ""
    assert str(first) not in json.dumps(manifest.load(home))


def test_uninstalling_from_a_removed_destination_reports_the_entries_gone(tmp_path):
    """`uninstall` returns what is no longer installed, and clears the record."""
    import shutil

    dest = tmp_path / "dest"
    home, _ = _install(tmp_path, dest)
    shutil.rmtree(dest)

    removed = uninstall("demo-pack", generic_dest_target(), _opts(home, tmp_path, dest))
    assert sorted(removed) == sorted(SKILLS)
    assert _record(home) is None, "nothing is installed; nothing should be recorded"


# --------------------------------------------------------------------------- #
# The safety the ownership check exists for is unchanged.                      #
# --------------------------------------------------------------------------- #
def test_an_entry_still_on_disk_without_its_receipt_is_still_refused(tmp_path, capsys):
    """Only *absence* is cleaned. A file that is there still needs a receipt.

    Deleting the unit — the proof of ownership — while leaving the entry in
    place is what an unmanaged edit looks like from the installer's side. The
    entry is someone else's content now, so it must survive and be reported.
    """
    import shutil

    dest = tmp_path / "dest"
    home, _ = _install(tmp_path, dest)
    shutil.rmtree(dest / ".asbb-units")
    survivor = dest / "alpha-skill"
    assert survivor.exists()

    capsys.readouterr()
    removed = uninstall("demo-pack", generic_dest_target(), _opts(home, tmp_path, dest))
    assert removed == []
    assert survivor.exists(), "an entry we cannot prove we own is never deleted"
    err = capsys.readouterr().err
    assert "asbb: skipped" in err
    assert "alpha-skill" in err
    assert _record(home) is not None, "a refused entry keeps its record for review"


def test_a_dangling_symlink_counts_as_present_not_as_absent(tmp_path, capsys):
    """`exists()` follows links, so a broken link reads as absent to `exists()`.

    A symlink install whose unit was removed leaves exactly this: a name that
    is occupied by a link resolving to nothing. Treating it as absent would
    drop the record while the dead link stayed in the user's destination, which
    is the opposite of cleaning it.
    """
    import shutil

    dest = tmp_path / "dest"
    home = tmp_path / "home"
    repo = make_repo(tmp_path / "repo", skills=SKILLS)
    dest.mkdir()
    install(
        resolve_pack(repo, "demo-pack"),
        generic_dest_target(),
        InstallOpts(home=home, project=tmp_path, copy=False, dest_override=dest),
    )
    link = dest / "alpha-skill"
    assert link.is_symlink()
    shutil.rmtree(dest / ".asbb-units")
    assert not link.exists() and link.is_symlink(), "the fixture must be a dead link"

    capsys.readouterr()
    uninstall("demo-pack", generic_dest_target(), _opts(home, tmp_path, dest))
    err = capsys.readouterr().err
    assert "asbb: skipped" in err and "alpha-skill" in err
    assert link.is_symlink(), "the dead link is still there to be reported, not ignored"


def test_the_helper_reads_absence_not_unreachability():
    """Pinned directly: the three states the destination path can be in."""
    from asb_skill_collections.asbb.installer import _absent

    import pathlib
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        real = root / "real"
        real.write_text("x")
        dangling = root / "dangling"
        dangling.symlink_to(root / "nothing-here")
        assert _absent(root / "missing") is True
        assert _absent(real) is False
        assert _absent(dangling) is False


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
