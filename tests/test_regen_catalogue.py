"""Catalogue generation is driven by the domain-release manifest."""

import json
import pathlib
import re

import pytest
import yaml

from scripts.regen_catalogue import build_catalogue, is_minted_doi, main, write_catalogue

REPO = pathlib.Path(__file__).resolve().parent.parent


def _release(version, *, status=None, doi=None, leaf_dir="leaves", tag=None):
    release = {
        "version": version,
        "path": f"collections/demo/v{version}",
        "released": f"2026-02-0{version}",
        "version_doi": doi,
        "leaf_dir": leaf_dir,
        "skills": version * 7,
        "tools": version * 3,
        "workflows": 0,
        "papers": 0,
    }
    if status:
        release["status"] = status
    if tag:
        release["tag"] = tag
    return release


def _template(slug, version, *, doi=None):
    entry = {
        "slug": slug,
        "version": str(version),
        "title": f"{slug.title()} Collection v{version}",
        "domain_topics": ["http://edamontology.org/topic_3172"],
        "lead_curators": [{"name": "Curator"}],
    }
    if doi is not None:
        entry["doi"] = doi
    return entry


@pytest.fixture
def tmp_repo(tmp_path):
    manifest = {
        "domains": {
            "zebra": {"releases": [_release(1, tag="zebra-v1.0.1")]},
            "alpha": {
                "releases": [
                    _release(2, doi="10.5281/zenodo.22", tag="alpha-v2.0.1"),
                    _release(1, status="legacy", doi="TODO-zenodo", leaf_dir="skills"),
                ]
            },
        }
    }
    (tmp_path / "collections.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    templates = [
        _template("alpha", 1, doi="TODO-zenodo"),
        _template("alpha", 2, doi="10.5281/zenodo.22"),
        _template("zebra", 1),
    ]
    (tmp_path / "catalogue.jsonld").write_text(
        json.dumps({"collections": templates}), encoding="utf-8"
    )
    return tmp_path


def test_catalogue_has_registry_context(tmp_repo):
    catalogue = build_catalogue(tmp_repo)
    assert catalogue["@type"] == "asb:SkillCollectionRegistry"
    assert catalogue["@context"]["status"] == "asb:status"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", catalogue["generated_at"])


def test_manifest_entries_have_required_fields_in_alphabetical_order(tmp_repo):
    entries = build_catalogue(tmp_repo)["collections"]
    assert [(entry["slug"], entry["version"]) for entry in entries] == [
        ("alpha", "1"), ("alpha", "2"), ("zebra", "1")
    ]
    required = {
        "@id", "title", "version", "slug", "skills_count", "tools_count",
        "papers_count", "workflows_count", "leaf_dir", "domain_topics",
        "lead_curators", "released_at", "status",
    }
    for entry in entries:
        assert required <= entry.keys()
        assert entry["title"] == f"{entry['slug'].title()} Collection v{entry['version']}"


def test_status_leaf_directory_and_release_timestamps_come_from_manifest(tmp_repo):
    entries = build_catalogue(tmp_repo)["collections"]
    legacy, published, _ = entries
    assert legacy["status"] == "legacy"
    assert published["status"] == "released"
    assert "tag" not in legacy
    assert "release_label" not in legacy
    assert published["tag"] == "alpha-v2.0.1"
    assert published["release_label"] == "2.0.1"
    assert legacy["leaf_dir"] == "skills"
    assert published["leaf_dir"] == "leaves"
    assert legacy["released_at"] == "2026-02-01T00:00:00Z"
    assert published["released_at"] == "2026-02-02T00:00:00Z"


def test_minted_doi_is_kept_and_placeholder_doi_is_omitted(tmp_repo):
    legacy, published, _ = build_catalogue(tmp_repo)["collections"]
    assert "doi" not in legacy
    assert published["doi"] == "10.5281/zenodo.22"


@pytest.mark.parametrize(
    ("doi", "minted"),
    [
        ("10.5281/zenodo.20794027", True),
        ("https://doi.org/10.5281/zenodo.1", False),
        ("TODO-zenodo", False),
        ("", False),
        (None, False),
    ],
)
def test_is_minted_doi(doi, minted):
    assert is_minted_doi(doi) is minted


def test_catalogue_write_to_file(tmp_repo):
    output = tmp_repo / "nested" / "catalogue.jsonld"
    write_catalogue(build_catalogue(tmp_repo), output)
    assert json.loads(output.read_text(encoding="utf-8"))["collections"]
    cli_output = tmp_repo / "cli" / "catalogue.jsonld"
    assert main(["--repo-root", str(tmp_repo), "--output", str(cli_output)]) == 0
    assert json.loads(cli_output.read_text(encoding="utf-8"))["collections"]


def test_tag_that_disagrees_with_major_is_refused(tmp_repo, capsys):
    manifest = yaml.safe_load((tmp_repo / "collections.yaml").read_text(encoding="utf-8"))
    manifest["domains"]["alpha"]["releases"][0]["tag"] = "alpha-v3.0.0"
    (tmp_repo / "collections.yaml").write_text(
        yaml.safe_dump(manifest), encoding="utf-8"
    )

    assert main(["--repo-root", str(tmp_repo)]) == 1
    assert "alpha/v2: tag 'alpha-v3.0.0'" in capsys.readouterr().err


def test_committed_catalogue_matches_manifest_regeneration():
    regenerated = build_catalogue(REPO)
    committed = json.loads((REPO / "catalogue.jsonld").read_text(encoding="utf-8"))
    regenerated.pop("generated_at")
    committed.pop("generated_at")
    assert committed == regenerated


def test_committed_catalogue_carries_each_registry_release_identity_and_counts():
    manifest = yaml.safe_load((REPO / "collections.yaml").read_text(encoding="utf-8"))
    catalogue = json.loads((REPO / "catalogue.jsonld").read_text(encoding="utf-8"))
    entries = {(entry["slug"], entry["version"]): entry for entry in catalogue["collections"]}
    releases = [
        (slug, release)
        for slug, domain in manifest["domains"].items()
        for release in domain["releases"]
    ]
    assert len(releases) == len(entries) == 14
    for slug, release in releases:
        entry = entries[(slug, str(release["version"]))]
        assert entry["status"] == release.get("status", "released")
        assert {
            "skills_count": entry["skills_count"],
            "tools_count": entry["tools_count"],
            "papers_count": entry["papers_count"],
            "workflows_count": entry["workflows_count"],
        } == {
            "skills_count": release["skills"],
            "tools_count": release["tools"],
            "papers_count": release["papers"],
            "workflows_count": release["workflows"],
        }
        if release.get("tag"):
            assert entry["tag"] == release["tag"]
            assert entry["release_label"] == release["tag"].removeprefix(f"{slug}-v")
        else:
            assert "tag" not in entry
            assert "release_label" not in entry
