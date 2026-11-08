"""The docs-site index is reproducible from explicit domain checkouts."""

import hashlib
import importlib.util
import json
import pathlib
import shutil

import pytest
import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
GENERATOR = REPO / "docs-site" / "build_search_index.py"
FIXTURE = REPO / "tests" / "fixtures" / "router_collection"


def _generator():
    spec = importlib.util.spec_from_file_location("build_search_index", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def fixture_checkout(tmp_path):
    checkout = tmp_path / "domain"
    collection = checkout / "collections" / "fixture" / "v1"
    collection.parent.mkdir(parents=True)
    shutil.copytree(FIXTURE, collection)
    manifest = tmp_path / "collections.yaml"
    manifest.write_text(
        yaml.safe_dump({
            "domains": {
                "fixture": {
                    "releases": [{
                        "version": 1,
                        "path": "collections/fixture/v1",
                        "commit": "fixture-commit",
                    }]
                }
            }
        }),
        encoding="utf-8",
    )
    return manifest, checkout


def _arguments(manifest, checkout, output):
    return [
        "--manifest", str(manifest),
        "--checkout", f"fixture={checkout}",
        "--output", str(output),
    ]


def test_two_builds_are_byte_identical_and_have_no_build_time(fixture_checkout, tmp_path):
    gen = _generator()
    manifest, checkout = fixture_checkout
    first, second = tmp_path / "first.json", tmp_path / "second.json"
    assert gen.main(_arguments(manifest, checkout, first)) == 0
    assert gen.main(_arguments(manifest, checkout, second)) == 0
    assert first.read_bytes() == second.read_bytes()
    payload = json.loads(first.read_text(encoding="utf-8"))
    assert "generated_at" not in payload
    assert payload["collections"] == ["fixture/v1"]


def test_output_leaves_the_committed_index_untouched(fixture_checkout, tmp_path):
    gen = _generator()
    manifest, checkout = fixture_checkout
    committed = tmp_path / "committed.json"
    committed.write_text("sentinel", encoding="utf-8")
    output = tmp_path / "elsewhere" / "search_index.json"
    assert gen.main(_arguments(manifest, checkout, output)) == 0
    assert output.is_file()
    assert committed.read_text(encoding="utf-8") == "sentinel"


def test_check_manifest_accepts_matching_digest(fixture_checkout, tmp_path):
    gen = _generator()
    manifest, _ = fixture_checkout
    index = tmp_path / "index.json"
    digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
    index.write_text(json.dumps({"manifest_sha256": digest}), encoding="utf-8")
    assert gen.main(["--manifest", str(manifest), "--check-manifest", str(index)]) == 0


def test_check_manifest_rejects_a_different_digest(fixture_checkout, tmp_path):
    gen = _generator()
    manifest, _ = fixture_checkout
    index = tmp_path / "index.json"
    index.write_text(json.dumps({"manifest_sha256": "stale"}), encoding="utf-8")
    assert gen.main(["--manifest", str(manifest), "--check-manifest", str(index)]) == 1


def test_build_without_a_checkout_is_refused(fixture_checkout, tmp_path):
    gen = _generator()
    manifest, _ = fixture_checkout
    output = tmp_path / "index.json"
    assert gen.main(["--manifest", str(manifest), "--output", str(output)]) == 2
    assert not output.exists()
