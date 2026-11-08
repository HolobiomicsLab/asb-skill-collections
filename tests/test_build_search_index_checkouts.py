"""Search-index builds consume domain checkouts and manifest provenance."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import yaml

GENERATOR = Path(__file__).resolve().parent.parent / "docs-site" / "build_search_index.py"


def _generator():
    spec = importlib.util.spec_from_file_location("build_search_index_checkouts", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fixture(tmp_path: Path) -> tuple[Path, Path]:
    manifest = tmp_path / "collections.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "domains": {
                    "demo": {
                        "releases": [
                            {
                                "version": 2,
                                "path": "collections/demo/v2",
                                "commit": "b" * 40,
                            },
                            {
                                "version": 1,
                                "path": "collections/demo/v1",
                                "commit": "a" * 40,
                                "status": "legacy",
                                "leaf_dir": "skills",
                            },
                        ]
                    },
                    "missing": {"releases": []},
                }
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    checkout = tmp_path / "domain"
    for version, leaf_dir in ((2, "leaves"), (1, "skills")):
        collection = checkout / "collections" / "demo" / f"v{version}"
        skill = collection / leaf_dir / "alpha"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: alpha\ndescription: Test alpha.\n---\n## Summary\nAlpha.\n",
            encoding="utf-8",
        )
        (collection / "tools").mkdir()
        (collection / "tools" / "tool.yaml").write_text(
            "slug: tool\nname: Tool\n", encoding="utf-8"
        )
        (collection / "workflows" / "flow").mkdir(parents=True)
        (collection / "workflows" / "flow" / "SKILL.md").write_text(
            "---\nname: flow\ndescription: Test flow.\n---\n## Summary\nFlow.\n",
            encoding="utf-8",
        )
        (collection / "corpus.yaml").write_text(
            yaml.safe_dump(
                {
                    "collection": "demo",
                    "collection_version": version,
                    "papers": [{"doi": f"10.1/{version}", "title": "Paper"}],
                }
            ),
            encoding="utf-8",
        )
    staged = checkout / "staged-collections" / "demo" / "v9" / "skills" / "draft"
    staged.mkdir(parents=True)
    (staged / "SKILL.md").write_text(
        "---\nname: draft\ndescription: Draft skill.\n---\n## Summary\nDraft.\n",
        encoding="utf-8",
    )
    return manifest, checkout


def test_checkout_index_records_status_commit_and_manifest(tmp_path: Path, capsys) -> None:
    generator = _generator()
    manifest, checkout = _fixture(tmp_path)
    payload = generator.build_index(manifest, {"demo": checkout})
    assert payload["manifest_sha256"] == hashlib.sha256(manifest.read_bytes()).hexdigest()
    assert payload["collections"] == ["demo/v1", "demo/v2", "demo/v9"]
    assert payload["collection_status"] == {
        "demo/v1": "staged",
        "demo/v2": "released",
        "demo/v9": "staged",
    }
    assert payload["collection_commits"] == {"demo/v1": "a" * 40, "demo/v2": "b" * 40}
    assert payload["skills"][0]["md_path"].startswith("collections/demo/")
    assert "no checkout for missing" in capsys.readouterr().err
    assert generator.serialize(payload) == generator.serialize(
        generator.build_index(manifest, {"demo": checkout})
    )


def test_build_without_checkout_is_refused(tmp_path: Path, capsys) -> None:
    generator = _generator()
    manifest, _ = _fixture(tmp_path)
    assert generator.main(["--manifest", str(manifest)]) == 2
    assert "at least one --checkout" in capsys.readouterr().err


def test_check_manifest_mode(tmp_path: Path, capsys) -> None:
    generator = _generator()
    manifest, _ = _fixture(tmp_path)
    index = tmp_path / "index.json"
    index.write_text(
        json.dumps({"manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest()}),
        encoding="utf-8",
    )
    assert generator.main(["--manifest", str(manifest), "--check-manifest", str(index)]) == 0
    manifest.write_text(manifest.read_text(encoding="utf-8") + "# changed\n", encoding="utf-8")
    assert generator.main(["--manifest", str(manifest), "--check-manifest", str(index)]) == 1
    assert "manifest_sha256" in capsys.readouterr().err
