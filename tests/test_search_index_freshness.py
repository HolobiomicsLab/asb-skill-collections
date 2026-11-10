"""The docs-site index is reproducible from explicit domain checkouts, and the
committed one matches the registry."""

import importlib.util
import json
import pathlib
import shutil

import pytest
import yaml

from scripts.check_collections_manifest import checkout_counts, compute_tree_digest

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
                        "commit": "0" * 40,
                        "tree_digest": compute_tree_digest(checkout, "collections/fixture/v1"),
                        **checkout_counts(collection),
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
        "--output-dir", str(output),
    ]


def test_two_builds_are_byte_identical_and_have_no_build_time(fixture_checkout, tmp_path):
    gen = _generator()
    manifest, checkout = fixture_checkout
    first, second = tmp_path / "first", tmp_path / "second"
    assert gen.main(_arguments(manifest, checkout, first)) == 0
    assert gen.main(_arguments(manifest, checkout, second)) == 0
    for name in ("fixture.json", "manifest.json"):
        assert (first / name).read_bytes() == (second / name).read_bytes()
    payload = json.loads((first / "fixture.json").read_text(encoding="utf-8"))
    assert "generated_at" not in payload
    assert payload["collections"] == ["fixture/v1"]
    assert payload["skills"] and payload["workflows"]


def test_output_dir_leaves_the_committed_index_untouched(fixture_checkout, tmp_path):
    gen = _generator()
    manifest, checkout = fixture_checkout
    committed = gen.INDEX_DIR / "manifest.json"
    before = committed.read_bytes() if committed.is_file() else None
    output = tmp_path / "elsewhere" / "search_index"
    assert gen.main(_arguments(manifest, checkout, output)) == 0
    assert (output / "manifest.json").is_file()
    assert (committed.read_bytes() if committed.is_file() else None) == before


def test_build_without_a_checkout_and_no_index_is_refused(fixture_checkout, tmp_path):
    gen = _generator()
    manifest, _ = fixture_checkout
    output = tmp_path / "index"
    assert gen.main(["--manifest", str(manifest), "--output-dir", str(output)]) == 1
    assert not output.exists()


def test_committed_index_matches_the_registry():
    """What CI runs: every registry domain has a current, unaltered file."""
    gen = _generator()
    assert gen.check_index(REPO / "collections.yaml", gen.INDEX_DIR) == []
    assert not (REPO / "docs-site" / "search_index.json").exists(), "the monolithic index was replaced"
