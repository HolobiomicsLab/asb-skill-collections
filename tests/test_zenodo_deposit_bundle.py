"""The Zenodo archive carries the license texts."""

import zipfile

import pytest

from scripts import zenodo_deposit
from tests.test_zenodo_deposit import make_repo

LICENSE_FILES = ("LICENSING.md", "LICENSE", "governance/LICENSE_TIERS.md")


@pytest.fixture
def repo(tmp_path):
    return make_repo(tmp_path / "repo")


def test_archive_members_include_the_license_texts(repo, tmp_path):
    built = zenodo_deposit.build_archive(repo, "dom", "v1", tmp_path / "o")
    with zipfile.ZipFile(built.path) as archive:
        names = set(archive.namelist())
        for relative in LICENSE_FILES:
            assert f"dom/v1/{relative}" in names
            assert archive.read(f"dom/v1/{relative}") == (repo / relative).read_bytes()


@pytest.mark.parametrize("relative", LICENSE_FILES)
def test_a_missing_license_text_stops_the_build(repo, tmp_path, relative):
    (repo / relative).unlink()
    with pytest.raises(zenodo_deposit.ZenodoError, match=relative):
        zenodo_deposit.build_archive(repo, "dom", "v1", tmp_path / "o")
    assert not (tmp_path / "o" / "dom-v1.zip").exists()
