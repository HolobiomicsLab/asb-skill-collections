"""Catalogue generation is driven by releases, not master-tree discovery."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.regen_catalogue import build_catalogue, main


def _manifest(root: Path, skills: int = 7) -> None:
    (root / "collections.yaml").write_text(
        yaml.safe_dump(
            {
                "domains": {
                    "demo": {
                        "releases": [
                            {
                                "version": 2,
                                "path": "collections/demo/v2",
                                "released": "2026-02-03T04:05:06Z",
                                "version_doi": "10.5281/zenodo.22",
                                "skills": skills,
                                "tools": 3,
                                "workflows": 0,
                                "papers": 0,
                            },
                            {
                                "version": 1,
                                "path": "collections/demo/v1",
                                "released": "2025-01-01",
                                "version_doi": None,
                                "status": "legacy",
                                "leaf_dir": "skills",
                                "skills": 2,
                                "tools": 1,
                                "workflows": 0,
                                "papers": 0,
                            },
                        ]
                    }
                }
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def _catalogue(root: Path) -> None:
    (root / "catalogue.jsonld").write_text(
        json.dumps(
            {
                "collections": [
                    {
                        "slug": "demo",
                        "version": str(version),
                        "title": title,
                        "domain_topics": ["http://edamontology.org/topic_3172"],
                        "lead_curators": [{"name": "Curator"}],
                    }
                    for version, title in ((1, "Demo v1"), (2, "Demo v2"))
                ]
            }
        ),
        encoding="utf-8",
    )


def test_manifest_releases_have_current_schema_and_statuses(tmp_path: Path) -> None:
    _manifest(tmp_path)
    _catalogue(tmp_path)
    output = tmp_path / "catalogue-output.jsonld"
    assert main(["--repo-root", str(tmp_path), "--output", str(output)]) == 0
    entries = build_catalogue(tmp_path)["collections"]
    assert [entry["version"] for entry in entries] == ["1", "2"]
    assert entries[0]["status"] == "staged"
    assert entries[0]["leaf_dir"] == "skills"
    assert "doi" not in entries[0]
    assert entries[1]["status"] == "released"
    assert entries[1]["leaf_dir"] == "leaves"
    assert entries[1]["doi"] == "10.5281/zenodo.22"
    assert entries[1]["released_at"] == "2026-02-03T04:05:06Z"
    assert entries[0]["released_at"] == "2025-01-01T00:00:00Z"
    for entry in entries:
        assert {
            "@id",
            "title",
            "version",
            "slug",
            "skills_count",
            "tools_count",
            "leaf_dir",
            "domain_topics",
            "released_at",
            "lead_curators",
            "status",
        } <= entry.keys()


def test_checkout_count_mismatch_is_refused(tmp_path: Path, capsys) -> None:
    _manifest(tmp_path)
    _catalogue(tmp_path)
    checkout = tmp_path / "domain"
    collection = checkout / "collections" / "demo" / "v2"
    (collection / "workflows").mkdir(parents=True)
    (collection / "skills_index.json").write_text("[{}]", encoding="utf-8")
    (collection / "tools_index.json").write_text("[{}, {}, {}]", encoding="utf-8")
    (collection / "workflows" / "workflows_index.json").write_text("[]", encoding="utf-8")
    (collection / "corpus.yaml").write_text("papers: []", encoding="utf-8")
    output = tmp_path / "refused.jsonld"
    result = main(
        [
            "--repo-root",
            str(tmp_path),
            "--checkout",
            f"demo={checkout}",
            "--output",
            str(output),
        ]
    )
    assert result == 1
    assert "demo/v2: checkout skills expected 7 got 1" in capsys.readouterr().err
    assert not output.exists()
