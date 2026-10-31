"""The Zenodo archive carries the license texts.

The archive built by scripts/zenodo_deposit.py held the collection and three
grounding files, but none of the texts its content is licensed under. It now
bundles LICENSING.md (which license covers which layer), LICENSE (the
Apache-2.0 text LICENSING.md points to) and governance/LICENSE_TIERS.md (the
per-skill license tiers), at the same relative paths as in the repository, and
refuses to build without them. The release workflow's Zenodo step bundles the
same three files.
"""
import pathlib
import zipfile

import pytest
import yaml

from scripts import zenodo_deposit
from tests.test_zenodo_deposit import make_repo

ROOT = pathlib.Path(__file__).parent.parent

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


def test_the_repository_archive_lists_the_license_texts():
    names = {name for name, _ in zenodo_deposit._archive_members(ROOT, "metabolomics", "v2")}
    for relative in LICENSE_FILES:
        assert f"metabolomics/v2/{relative}" in names


def test_the_release_workflow_bundles_the_same_license_texts():
    workflow = yaml.safe_load((ROOT / ".github" / "workflows" / "release.yml").read_text())
    (step,) = [s for s in workflow["jobs"]["release"]["steps"] if s.get("id") == "zenodo"]
    for relative in LICENSE_FILES:
        assert f'("{relative}",' in step["run"], relative


def test_release_deposit_doc_lists_the_license_texts():
    text = (ROOT / "docs" / "RELEASE_DEPOSIT.md").read_text()
    for relative in LICENSE_FILES:
        assert f"`{relative}`" in text
