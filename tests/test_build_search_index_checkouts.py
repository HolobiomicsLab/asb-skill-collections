"""The per-domain search index: verified checkouts, incremental builds, check mode."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
from pathlib import Path

import pytest
import yaml

from scripts.check_collections_manifest import checkout_counts, compute_tree_digest

GENERATOR = Path(__file__).resolve().parent.parent / "docs-site" / "build_search_index.py"


def _generator():
    spec = importlib.util.spec_from_file_location("build_search_index_checkouts", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _collection(checkout: Path, slug: str, version: int, leaf_dir: str, skill: str) -> None:
    collection = checkout / "collections" / slug / f"v{version}"
    leaf = collection / leaf_dir / skill
    leaf.mkdir(parents=True)
    (leaf / "SKILL.md").write_text(
        f"---\nname: {skill}\ndescription: Test {skill}.\n---\n## Summary\n{skill} summary.\n",
        encoding="utf-8",
    )
    (collection / "tools").mkdir()
    (collection / "tools" / "tool.yaml").write_text(f"slug: tool\nname: Tool {slug}\n", encoding="utf-8")
    (collection / "workflows" / "flow").mkdir(parents=True)
    (collection / "workflows" / "flow" / "SKILL.md").write_text(
        "---\nname: flow\ndescription: Test flow.\n---\n## Summary\nFlow.\n", encoding="utf-8"
    )
    (collection / "corpus.yaml").write_text(
        yaml.safe_dump({
            "collection": slug,
            "collection_version": version,
            "papers": [{"doi": f"10.1/{slug}.{version}", "title": "Paper"}],
        }),
        encoding="utf-8",
    )


def _row(checkout: Path, slug: str, version: int, commit: str, **extra) -> dict:
    path = f"collections/{slug}/v{version}"
    return {
        "version": version,
        "path": path,
        "commit": commit,
        "tree_digest": compute_tree_digest(checkout, path),
        **checkout_counts(checkout / path),
        **extra,
    }


@pytest.fixture
def world(tmp_path: Path) -> dict:
    demo = tmp_path / "demo-domain"
    _collection(demo, "demo", 2, "leaves", "alpha")
    _collection(demo, "demo", 1, "skills", "beta")
    staged = demo / "staged-collections" / "demo" / "v9" / "skills" / "draft"
    staged.mkdir(parents=True)
    (staged / "SKILL.md").write_text("---\nname: draft\ndescription: Draft.\n---\n", encoding="utf-8")
    other = tmp_path / "other-domain"
    _collection(other, "other", 1, "leaves", "gamma")
    registry = {
        "schema": "asb-collections-manifest/1",
        "domains": {
            "demo": {"releases": [
                _row(demo, "demo", 2, "b" * 40),
                _row(demo, "demo", 1, "a" * 40, status="legacy", leaf_dir="skills"),
            ]},
            "other": {"releases": [_row(other, "other", 1, "c" * 40)]},
        },
    }
    manifest = tmp_path / "collections.yaml"
    manifest.write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
    return {"manifest": manifest, "demo": demo, "other": other, "index": tmp_path / "index"}


def _run(generator, world: dict, *arguments: str) -> int:
    return generator.main(["--manifest", str(world["manifest"]), "--output-dir", str(world["index"]), *arguments])


def _full(generator, world: dict, *arguments: str) -> int:
    return _run(generator, world, "--checkout", f"demo={world['demo']}",
                "--checkout", f"other={world['other']}", *arguments)


def _snapshot(directory: Path) -> dict[str, bytes]:
    return {path.name: path.read_bytes() for path in sorted(directory.iterdir())} if directory.exists() else {}


def _edit_registry(world: dict, edit) -> None:
    document = yaml.safe_load(world["manifest"].read_text(encoding="utf-8"))
    edit(document)
    world["manifest"].write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")


def test_per_domain_files_and_manifest(world) -> None:
    generator = _generator()
    assert _full(generator, world) == 0
    index = world["index"]
    assert sorted(path.name for path in index.iterdir()) == ["demo.json", "manifest.json", "other.json"]
    demo = json.loads((index / "demo.json").read_text(encoding="utf-8"))
    assert demo["domain"] == "demo"
    assert demo["collections"] == ["demo/v1", "demo/v2"]  # the staged tree is not indexed
    assert demo["collection_status"] == {"demo/v1": "staged", "demo/v2": "released"}
    assert demo["collection_commits"] == {"demo/v1": "a" * 40, "demo/v2": "b" * 40}
    assert {skill["name"] for skill in demo["skills"]} == {"alpha", "beta"}
    assert demo["skills"][0]["md_path"].startswith("collections/demo/")
    manifest = json.loads((index / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == generator.MANIFEST_SCHEMA_VERSION
    assert manifest["default_domains"] == []  # metabolomics is not in this registry
    entry = manifest["domains"]["demo"]
    data = (index / "demo.json").read_bytes()
    assert entry["file"] == "demo.json"
    assert entry["sha256"] == hashlib.sha256(data).hexdigest()
    assert entry["bytes"] == len(data)
    assert entry["counts"] == {"papers": 2, "skills": 2, "tools": 2, "workflows": 2}
    assert entry["collections"] == [
        {"label": "demo/v1", "status": "staged", "commit": "a" * 40},
        {"label": "demo/v2", "status": "released", "commit": "b" * 40},
    ]
    registry = yaml.safe_load(world["manifest"].read_text(encoding="utf-8"))
    assert entry["registry_digest"] == generator.registry_digest("demo", registry["domains"]["demo"], False)
    assert manifest["domains"]["other"]["counts"]["skills"] == 1


def test_registry_digest_covers_only_the_fields_that_shape_the_index(world) -> None:
    generator = _generator()
    domain = yaml.safe_load(world["manifest"].read_text(encoding="utf-8"))["domains"]["demo"]
    digest = generator.registry_digest("demo", domain, False)
    domain["releases"][0]["version_doi"] = "10.5281/zenodo.1"
    domain["releases"][0]["skills"] = 999
    domain["repository"] = "Example/demo"
    assert generator.registry_digest("demo", domain, False) == digest
    domain["releases"][0]["tree_digest"] = "sha256:" + "0" * 64
    assert generator.registry_digest("demo", domain, False) != digest
    assert generator.registry_digest("demo", domain, True) != generator.registry_digest("demo", domain, False)


def test_two_builds_are_byte_identical(world, tmp_path) -> None:
    generator = _generator()
    assert _full(generator, world) == 0
    first = _snapshot(world["index"])
    shutil.rmtree(world["index"])
    assert _full(generator, world) == 0
    assert _snapshot(world["index"]) == first
    assert "generated_at" not in json.loads(first["demo.json"])


def test_domain_without_checkout_keeps_its_file(world, capsys) -> None:
    generator = _generator()
    assert _full(generator, world) == 0
    before = _snapshot(world["index"])
    other_file = world["index"] / "other.json"
    mtime = other_file.stat().st_mtime_ns
    capsys.readouterr()
    assert _run(generator, world, "--checkout", f"demo={world['demo']}") == 0
    assert "kept other" in capsys.readouterr().out
    assert _snapshot(world["index"]) == before
    assert other_file.stat().st_mtime_ns == mtime
    # A registry change in another domain leaves this one valid.
    _edit_registry(world, lambda d: d["domains"]["demo"]["releases"][0].update(version_doi="10.5281/zenodo.9"))
    assert _run(generator, world) == 0
    assert _snapshot(world["index"]) == before


def test_missing_domain_without_checkout_is_refused(world, capsys) -> None:
    generator = _generator()
    assert _run(generator, world, "--checkout", f"demo={world['demo']}") == 1
    err = capsys.readouterr().err
    assert "other: no index file recorded" in err
    assert "--checkout other=" in err
    assert not world["index"].exists()


def test_stale_domain_without_checkout_is_refused(world, capsys) -> None:
    generator = _generator()
    assert _full(generator, world) == 0
    before = _snapshot(world["index"])
    _edit_registry(world, lambda d: d["domains"]["other"]["releases"][0].update(commit="d" * 40))
    capsys.readouterr()
    assert _run(generator, world, "--checkout", f"demo={world['demo']}") == 1
    assert "other: index is stale" in capsys.readouterr().err
    assert _snapshot(world["index"]) == before


def test_tampered_file_without_checkout_is_refused(world, capsys) -> None:
    generator = _generator()
    assert _full(generator, world) == 0
    (world["index"] / "other.json").write_text("{}", encoding="utf-8")
    capsys.readouterr()
    assert _run(generator, world) == 1
    assert "does not match its recorded sha256" in capsys.readouterr().err


def test_checkout_that_differs_from_the_registry_is_refused(world, capsys) -> None:
    generator = _generator()
    assert _full(generator, world) == 0
    before = _snapshot(world["index"])
    leaf = world["demo"] / "collections/demo/v2/leaves/alpha/SKILL.md"
    leaf.write_text(leaf.read_text(encoding="utf-8") + "edited\n", encoding="utf-8")
    capsys.readouterr()
    assert _full(generator, world) == 1
    err = capsys.readouterr().err
    assert "demo/v2: tree_digest expected" in err
    assert "not the registered release" in err
    assert _snapshot(world["index"]) == before


def test_wrong_checkout_for_a_domain_is_refused(world, capsys) -> None:
    generator = _generator()
    assert _run(generator, world, "--checkout", f"demo={world['other']}",
                "--checkout", f"other={world['other']}") == 1
    assert "demo/v2: checkout validation failed" in capsys.readouterr().err
    assert not world["index"].exists()


def test_release_without_digest_is_verified_against_git_or_refused(world, capsys) -> None:
    generator = _generator()
    _edit_registry(world, lambda d: d["domains"]["other"]["releases"][0].pop("tree_digest"))
    assert _full(generator, world) == 1  # not a git repository: cannot verify
    assert "other/v1: cannot verify the checkout" in capsys.readouterr().err
    _edit_registry(world, lambda d: d["domains"]["other"]["releases"][0].pop("commit"))
    assert _full(generator, world) == 1
    assert "neither tree_digest nor commit" in capsys.readouterr().err


def test_unknown_checkout_domain_is_refused(world, capsys) -> None:
    generator = _generator()
    assert _full(generator, world, "--checkout", f"ghost={world['other']}") == 1
    assert "ghost: --checkout names a domain that is not in" in capsys.readouterr().err


def test_domain_leaving_the_registry_loses_its_file(world) -> None:
    generator = _generator()
    assert _full(generator, world) == 0
    _edit_registry(world, lambda d: d["domains"].pop("other"))
    assert _run(generator, world) == 0
    assert sorted(path.name for path in world["index"].iterdir()) == ["demo.json", "manifest.json"]


def test_default_domain_is_recorded_and_persists(world, capsys) -> None:
    generator = _generator()
    assert _full(generator, world, "--default-domain", "other", "--default-domain", "demo") == 0
    manifest_path = world["index"] / "manifest.json"
    assert json.loads(manifest_path.read_text())["default_domains"] == ["demo", "other"]
    assert _run(generator, world, "--checkout", f"demo={world['demo']}") == 0
    assert json.loads(manifest_path.read_text())["default_domains"] == ["demo", "other"]
    assert _run(generator, world, "--default-domain", "other") == 0
    assert json.loads(manifest_path.read_text())["default_domains"] == ["other"]
    before = _snapshot(world["index"])
    capsys.readouterr()
    assert _run(generator, world, "--default-domain", "ghost") == 1
    assert "--default-domain ghost: not a registry domain" in capsys.readouterr().err
    assert _snapshot(world["index"]) == before


def test_initial_default_domain_is_metabolomics_when_registered(tmp_path) -> None:
    generator = _generator()
    checkout = tmp_path / "domain"
    _collection(checkout, "metabolomics", 3, "leaves", "alpha")
    manifest = tmp_path / "collections.yaml"
    manifest.write_text(yaml.safe_dump({"domains": {"metabolomics": {
        "releases": [_row(checkout, "metabolomics", 3, "e" * 40)]}}}), encoding="utf-8")
    index = tmp_path / "index"
    assert generator.main(["--manifest", str(manifest), "--output-dir", str(index),
                           "--checkout", f"metabolomics={checkout}"]) == 0
    assert json.loads((index / "manifest.json").read_text())["default_domains"] == ["metabolomics"]


def test_check_mode_passes_on_a_fresh_index(world, capsys) -> None:
    generator = _generator()
    assert _full(generator, world) == 0
    assert _run(generator, world, "--check-manifest", str(world["index"])) == 0
    assert _run(generator, world, "--check-manifest", str(world["index"] / "manifest.json")) == 0
    assert "OK: search index" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("damage", "message"),
    [
        (lambda w: _edit_registry(w, lambda d: d["domains"].update(new={"releases": []})),
         "new: registry domain has no index entry"),
        (lambda w: _edit_registry(w, lambda d: d["domains"].pop("other")),
         "other: index entry for a domain that is not in the registry"),
        (lambda w: _edit_registry(w, lambda d: d["domains"]["demo"]["releases"][0].update(commit="f" * 40)),
         "demo: registry_digest is stale"),
        (lambda w: (w["index"] / "demo.json").unlink(), "demo: index file 'demo.json' is missing"),
        (lambda w: (w["index"] / "demo.json").write_text("{}", encoding="utf-8"), "demo: demo.json has 2 bytes"),
        (lambda w: (w["index"] / "demo.json").write_bytes(
            (w["index"] / "demo.json").read_bytes().replace(b"alpha", b"alphb")),
         "demo: demo.json sha256 differs"),
        (lambda w: (w["index"] / "stray.json").write_text("{}", encoding="utf-8"),
         "stray.json: file not recorded in the manifest"),
        (lambda w: (w["index"] / "manifest.json").unlink(), "manifest.json: missing"),
    ],
)
def test_check_mode_reports_each_failure(world, capsys, damage, message) -> None:
    generator = _generator()
    assert _full(generator, world) == 0
    damage(world)
    capsys.readouterr()
    assert _run(generator, world, "--check-manifest", str(world["index"])) == 1
    assert message in capsys.readouterr().err


def test_check_mode_rejects_an_unindexed_default_domain(world, capsys) -> None:
    generator = _generator()
    assert _full(generator, world) == 0
    path = world["index"] / "manifest.json"
    manifest = json.loads(path.read_text())
    manifest["default_domains"] = ["ghost"]
    path.write_text(json.dumps(manifest), encoding="utf-8")
    assert _run(generator, world, "--check-manifest", str(world["index"])) == 1
    assert "default_domains" in capsys.readouterr().err
