"""Legacy manifest releases retain integrity checks without publication metadata."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

from scripts.check_collections_manifest import compute_tree_digest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "check_collections_manifest.py"


def _release(version: int, status: str | None = None) -> dict:
    release = {
        "version": version,
        "path": f"collections/demo/v{version}",
        "tag": f"demo-v{version}.0.0",
        "commit": "a" * 40,
        "source_commit": None,
        "tree_digest": "sha256:" + "0" * 64,
        "version_doi": f"10.5281/zenodo.{version}",
        "released": "2026-01-01",
        "skills": 1,
        "tools": 1,
        "workflows": 1,
        "papers": 1,
    }
    if status:
        release["status"] = status
        release.update(tag=None, version_doi=None)
    return release


def _write_fixture(tmp_path: Path, published_nulls: bool = False) -> tuple[Path, Path]:
    published = _release(2)
    if published_nulls:
        published.update(tag=None, version_doi=None)
    manifest = tmp_path / "collections.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "schema": "asb-collections-manifest/1",
                "domains": {
                    "demo": {
                        "repository": "example/demo",
                        "concept_doi": "10.5281/zenodo.99",
                        "releases": [published, _release(1, "legacy")],
                    }
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    entries = []
    for version in (2, 1):
        entries.append(
            {
                "slug": "demo",
                "version": str(version),
                "skills_count": 1,
                "tools_count": 1,
                "workflows_count": 1,
                "papers_count": 1,
            }
        )
        if version == 2 and not published_nulls:
            entries[-1]["doi"] = "10.5281/zenodo.2"
    catalogue = tmp_path / "catalogue.jsonld"
    catalogue.write_text(json.dumps({"collections": entries}), encoding="utf-8")
    return manifest, catalogue


def _run(manifest: Path, catalogue: Path, checkout: Path | None = None):
    command = [sys.executable, str(SCRIPT), "--manifest", str(manifest)]
    if checkout:
        command.extend(["--checkout", f"demo={checkout}"])
    return subprocess.run(command, capture_output=True, text=True, check=False)


def test_legacy_accepts_null_publication_metadata(tmp_path: Path) -> None:
    result = _run(*_write_fixture(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr


def test_published_release_rejects_null_publication_metadata(tmp_path: Path) -> None:
    result = _run(*_write_fixture(tmp_path, published_nulls=True))
    assert result.returncode == 1
    assert "demo/v2: invalid version_doi None" in result.stdout


def test_unknown_release_status_is_rejected(tmp_path: Path) -> None:
    manifest, catalogue = _write_fixture(tmp_path)
    document = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    document["domains"]["demo"]["releases"][1]["status"] = "archived"
    manifest.write_text(yaml.safe_dump(document), encoding="utf-8")
    result = _run(manifest, catalogue)
    assert result.returncode == 1
    assert "demo/v1: invalid status 'archived'" in result.stdout


def test_legacy_catalogue_may_omit_doi_but_not_conflict(tmp_path: Path) -> None:
    manifest, catalogue = _write_fixture(tmp_path)
    document = json.loads(catalogue.read_text(encoding="utf-8"))
    document["collections"][1]["doi"] = "10.5281/zenodo.999"
    catalogue.write_text(json.dumps(document), encoding="utf-8")
    result = _run(manifest, catalogue)
    assert result.returncode == 1
    assert "demo/v1: catalogue doi" in result.stdout


def test_legacy_checkout_verifies_tree_digest(tmp_path: Path) -> None:
    manifest, catalogue = _write_fixture(tmp_path)
    checkout = tmp_path / "domain"
    for version in (2, 1):
        collection = checkout / "collections" / "demo" / f"v{version}"
        (collection / "workflows").mkdir(parents=True)
        (collection / "skills_index.json").write_text("[]", encoding="utf-8")
        (collection / "tools_index.json").write_text("[]", encoding="utf-8")
        (collection / "workflows" / "workflows_index.json").write_text("[]", encoding="utf-8")
        (collection / "corpus.yaml").write_text("papers: []", encoding="utf-8")
    document = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    for release in document["domains"]["demo"]["releases"]:
        release.update(skills=0, tools=0, workflows=0, papers=0)
        release["tree_digest"] = compute_tree_digest(checkout, release["path"])
    manifest.write_text(yaml.safe_dump(document), encoding="utf-8")
    entries = json.loads(catalogue.read_text(encoding="utf-8"))
    for entry in entries["collections"]:
        entry.update(
            skills_count=0,
            tools_count=0,
            workflows_count=0,
            papers_count=0,
        )
    catalogue.write_text(json.dumps(entries), encoding="utf-8")
    assert _run(manifest, catalogue, checkout).returncode == 0
    (checkout / "collections" / "demo" / "v1" / "new.txt").write_text("changed", encoding="utf-8")
    result = _run(manifest, catalogue, checkout)
    assert result.returncode == 1
    assert "demo/v1: tree_digest expected" in result.stdout
