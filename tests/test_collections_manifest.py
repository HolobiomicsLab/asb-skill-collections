"""The domain-release manifest agrees with catalogues and local checkouts."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "check_collections_manifest.py"
DOI = "10.5281/zenodo.1234567"


def write_fixture(root: Path) -> tuple[Path, Path, Path]:
    """Create a two-file domain release and an independently hashed manifest."""
    checkout = root / "checkout"
    collection = checkout / "collections" / "astronomy" / "v1"
    (collection / "workflows").mkdir(parents=True)
    (collection / "alpha.txt").write_text("alpha\n", encoding="utf-8")
    (collection / "beta.txt").write_text("beta\n", encoding="utf-8")
    (collection / "skills_index.json").write_text("[{}]\n", encoding="utf-8")
    (collection / "tools_index.json").write_text("[{}, {}]\n", encoding="utf-8")
    (collection / "workflows" / "workflows_index.json").write_text(
        "[{}, {}, {}]\n", encoding="utf-8"
    )
    (collection / "corpus.yaml").write_text(
        "papers:\n  - doi: one\n  - doi: two\n  - doi: three\n  - doi: four\n",
        encoding="utf-8",
    )
    lines = []
    for path in collection.rglob("*"):
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {path.relative_to(checkout).as_posix()}\n")
    tree_digest = "sha256:" + hashlib.sha256("".join(sorted(lines)).encode()).hexdigest()
    release = {
        "version": 1,
        "path": "collections/astronomy/v1",
        "tag": "astronomy-v1.0.0",
        "commit": "a" * 40,
        "source_commit": None,
        "tree_digest": tree_digest,
        "version_doi": DOI,
        "released": "2026-01-02",
        "skills": 1,
        "tools": 2,
        "workflows": 3,
        "papers": 4,
    }
    manifest = root / "collections.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "schema": "asb-collections-manifest/1",
                "domains": {
                    "astronomy": {
                        "repository": "Example/astronomy",
                        "concept_doi": "10.5281/zenodo.1234566",
                        "releases": [release],
                    }
                },
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    catalogue = root / "catalogue.jsonld"
    catalogue.write_text(
        json.dumps(
            {
                "collections": [
                    {
                        "slug": "astronomy",
                        "version": "1",
                        "doi": DOI,
                        "skills_count": 1,
                        "tools_count": 2,
                        "workflows_count": 3,
                        "papers_count": 4,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    return manifest, catalogue, checkout


def run_checker(manifest: Path, catalogue: Path, checkout: Path) -> subprocess.CompletedProcess:
    """Run the checker against an isolated domain fixture."""
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--manifest",
            str(manifest),
            "--catalogue",
            str(catalogue),
            "--checkout",
            f"astronomy={checkout}",
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )


def update_release(manifest: Path, key: str, value: object) -> None:
    """Change one release value in a fixture manifest."""
    document = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    document["domains"]["astronomy"]["releases"][0][key] = value
    manifest.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")


def test_matching_manifest_catalogue_and_checkout_pass(tmp_path: Path) -> None:
    """A valid domain-neutral fixture produces one release summary."""
    manifest, catalogue, checkout = write_fixture(tmp_path)

    result = run_checker(manifest, catalogue, checkout)

    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout == (
        "OK astronomy/v1: skills=1 tools=2 workflows=3 papers=4 tree=verified\n"
    )


def test_wrong_tree_digest_fails_with_expected_line(tmp_path: Path) -> None:
    """A manifest digest is recomputed rather than trusted."""
    manifest, catalogue, checkout = write_fixture(tmp_path)
    update_release(manifest, "tree_digest", "sha256:" + "0" * 64)

    result = run_checker(manifest, catalogue, checkout)

    assert result.returncode == 1
    assert "astronomy/v1: tree_digest expected sha256:" + "0" * 64 in result.stdout


@pytest.mark.parametrize(("key", "actual"), [("skills", 1), ("papers", 4)])
def test_wrong_checkout_count_fails_with_expected_line(
    tmp_path: Path, key: str, actual: int
) -> None:
    """Index and corpus totals independently constrain the manifest."""
    manifest, catalogue, checkout = write_fixture(tmp_path)
    update_release(manifest, key, 99)

    result = run_checker(manifest, catalogue, checkout)

    assert result.returncode == 1
    assert f"astronomy/v1: checkout {key} expected 99 got {actual}" in result.stdout


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("skills_count", 1),
        ("tools_count", 2),
        ("workflows_count", 3),
        ("papers_count", 4),
    ],
)
def test_catalogue_count_disagreement_fails_without_checkout(
    tmp_path: Path, field: str, expected: int
) -> None:
    """Catalogue validation also runs when no source checkout is supplied."""
    manifest, catalogue, checkout = write_fixture(tmp_path)
    document = json.loads(catalogue.read_text(encoding="utf-8"))
    document["collections"][0][field] = 99
    catalogue.write_text(json.dumps(document), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--manifest", str(manifest)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert f"astronomy/v1: catalogue {field} 99 != {expected}" in result.stdout
    assert checkout.is_dir()


def test_symlink_is_excluded_from_tree_digest(tmp_path: Path) -> None:
    """A symlink cannot inject content into a release digest."""
    manifest, catalogue, checkout = write_fixture(tmp_path)
    collection = checkout / "collections" / "astronomy" / "v1"
    (collection / "linked.txt").symlink_to(collection / "alpha.txt")

    result = run_checker(manifest, catalogue, checkout)

    assert result.returncode == 0, result.stdout + result.stderr


def test_escaping_release_path_is_rejected(tmp_path: Path) -> None:
    """A release path cannot read outside its assigned checkout."""
    manifest, catalogue, checkout = write_fixture(tmp_path)
    update_release(manifest, "path", "../outside")

    result = run_checker(manifest, catalogue, checkout)

    assert result.returncode == 1
    assert "astronomy/v1: invalid relative path '../outside'" in result.stdout
    assert "checkout validation failed" not in result.stdout


SUPERSEDED = {
    "tag": "astronomy-v1.0.0",
    "commit": "b" * 40,
    "tree_digest": "sha256:" + "1" * 64,
    "version_doi": "10.5281/zenodo.1234560",
    "released": "2026-01-01",
}


def test_superseded_trace_of_a_patch_release_passes(tmp_path: Path) -> None:
    """A row moved to a patch release keeps the replaced values under superseded."""
    manifest, catalogue, checkout = write_fixture(tmp_path)
    update_release(manifest, "tag", "astronomy-v1.0.1")
    update_release(manifest, "superseded", [SUPERSEDED])

    result = run_checker(manifest, catalogue, checkout)

    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ([], "superseded must be a non-empty list"),
        ([{**SUPERSEDED, "commit": "short"}], "superseded[0]: invalid commit 'short'"),
        ([{**SUPERSEDED, "released": "9 Nov"}], "superseded[0]: invalid released '9 Nov'"),
        ([{**SUPERSEDED, "extra": 1}], "superseded[0] keys must be"),
        ([{**SUPERSEDED, "tag": "astronomy-v1.0.1"}], "superseded repeats the current tag"),
    ],
)
def test_malformed_superseded_trace_fails(tmp_path: Path, value: object, message: str) -> None:
    """Shape and formats of the superseded entries are checked."""
    manifest, catalogue, checkout = write_fixture(tmp_path)
    update_release(manifest, "tag", "astronomy-v1.0.1")
    update_release(manifest, "superseded", value)

    result = run_checker(manifest, catalogue, checkout)

    assert result.returncode == 1
    assert message in result.stdout
