"""Public collection landing pages stay aligned with the release registry."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from scripts import render_collection_landings as landings

REPO = Path(__file__).resolve().parents[1]
RELATIVE_LINK = re.compile(r"\[[^]]+\]\((?![a-z]+:)([^)#]+)(?:#[^)]+)?\)")


def release(version: int, *, legacy: bool = False, archived: bool = True) -> dict:
    """Build one compact manifest release row."""
    row = {
        "version": version,
        "path": f"collections/demo/v{version}",
        "tag": f"demo-v{version}.0.1" if archived else None,
        "version_doi": f"10.5281/zenodo.{version}" if archived else None,
        "released": "2026-01-02",
        "skills": version,
        "tools": version + 1,
        "workflows": version + 2,
        "papers": version + 3,
    }
    if legacy:
        row["status"] = "legacy"
    return row


def fixture_inputs() -> tuple[dict, dict]:
    """Return a two-major manifest with one exact marketplace match."""
    current = release(2)
    current["superseded"] = [{
        "tag": "demo-v2.0.0",
        "version_doi": "10.5281/zenodo.20",
        "released": "2026-01-01",
    }]
    manifest = {
        "schema": "asb-collections-manifest/1",
        "domains": {
            "demo": {
                "repository": "HolobiomicsLab/asb-skills-demo",
                "concept_doi": "10.5281/zenodo.99",
                "releases": [current, release(1, legacy=True, archived=False)],
            }
        },
    }
    marketplace = {
        "plugins": [
            {
                "name": "demo",
                "source": {"source": "git-subdir", "path": "collections/demo/v2"},
            },
            {"name": "demo-pack", "source": "./packs/demo/example"},
        ]
    }
    return manifest, marketplace


def write_inputs(root: Path, manifest: dict, marketplace: dict) -> None:
    """Write generator inputs under an isolated repository root."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "collections.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
    )
    path = root / ".claude-plugin" / "marketplace.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(marketplace), encoding="utf-8")


def real_inputs() -> tuple[dict, dict]:
    """Load the committed registry inputs."""
    return landings.load_inputs(
        REPO / "collections.yaml", REPO / ".claude-plugin" / "marketplace.json"
    )


def test_small_fixture_has_one_page_per_release_row() -> None:
    manifest, marketplace = fixture_inputs()

    pages = landings.expected_landings(manifest, marketplace)

    assert set(pages) == {
        Path("collections/demo/v1/README.md"),
        Path("collections/demo/v2/README.md"),
    }


def test_real_manifest_has_one_current_page_per_release_row() -> None:
    manifest, marketplace = real_inputs()
    pages = landings.expected_landings(manifest, marketplace)
    release_count = sum(len(domain["releases"]) for domain in manifest["domains"].values())

    assert len(pages) == release_count == 14
    assert all((REPO / path).read_text(encoding="utf-8") == text for path, text in pages.items())


def test_text_builder_and_generation_are_deterministic(tmp_path: Path) -> None:
    manifest, marketplace = fixture_inputs()
    domain = manifest["domains"]["demo"]
    first = landings.render_collection_landing("demo", domain, domain["releases"][0], marketplace)
    second = landings.render_collection_landing("demo", domain, domain["releases"][0], marketplace)
    assert first == second

    write_inputs(tmp_path, manifest, marketplace)
    assert landings.main(["--root", str(tmp_path)]) == 0
    snapshot = {
        path: (tmp_path / path).read_bytes()
        for path in landings.expected_landings(manifest, marketplace)
    }
    assert landings.main(["--root", str(tmp_path)]) == 0
    assert {path: (tmp_path / path).read_bytes() for path in snapshot} == snapshot


def test_check_reports_missing_stale_and_unexpected_pages(tmp_path: Path, capsys) -> None:
    manifest, marketplace = fixture_inputs()
    write_inputs(tmp_path, manifest, marketplace)
    assert landings.main(["--root", str(tmp_path)]) == 0
    capsys.readouterr()
    assert landings.main(["--root", str(tmp_path), "--check"]) == 0

    missing = tmp_path / "collections/demo/v1/README.md"
    missing.unlink()
    assert landings.main(["--root", str(tmp_path), "--check"]) == 1
    assert "missing: collections/demo/v1/README.md" in capsys.readouterr().out
    assert not missing.exists()
    assert landings.main(["--root", str(tmp_path)]) == 0

    stale = tmp_path / "collections/demo/v2/README.md"
    current = stale.read_text(encoding="utf-8")
    edited = current.replace("| Skills |", "| Skilz |")
    assert edited != current
    stale.write_text(edited, encoding="utf-8")
    assert landings.main(["--root", str(tmp_path), "--check"]) == 1
    assert "stale: collections/demo/v2/README.md" in capsys.readouterr().out
    assert stale.read_text(encoding="utf-8") == edited
    assert landings.main(["--root", str(tmp_path)]) == 0
    assert stale.read_text(encoding="utf-8") == current

    unexpected = tmp_path / "collections/demo/v9/README.md"
    unexpected.parent.mkdir(parents=True)
    unexpected.write_text("unexpected\n", encoding="utf-8")
    assert landings.main(["--root", str(tmp_path), "--check"]) == 1
    assert "unexpected: collections/demo/v9/README.md" in capsys.readouterr().out
    assert unexpected.read_text(encoding="utf-8") == "unexpected\n"


def test_no_page_links_a_content_repository() -> None:
    manifest, marketplace = real_inputs()

    pages = landings.expected_landings(manifest, marketplace)

    assert all("github.com/HolobiomicsLab/asb-skills-" not in page for page in pages.values())


def test_legacy_page_is_explicit_and_points_to_the_current_major() -> None:
    manifest, marketplace = fixture_inputs()
    page = landings.expected_landings(manifest, marketplace)[
        Path("collections/demo/v1/README.md")
    ]

    assert page.startswith("# Demo skill collection v1\n\n**Legacy release.**")
    assert "[v2](../v2/README.md)" in page
    assert "No release tag was minted for this version." in page
    assert "None: this version has no public archive." in page
    assert "This version has no public archive. Use the current major, [v2](../v2/README.md)." in page
    assert "It has no Zenodo archive." in page
    assert "private" not in page
    assert "PENDING" not in page


def test_a_collection_readme_is_never_replaced_or_removed(tmp_path: Path, capsys) -> None:
    """In a content repository the same path holds the collection's own README."""
    manifest, marketplace = fixture_inputs()
    write_inputs(tmp_path, manifest, marketplace)
    own = tmp_path / "collections/demo/v2/README.md"
    own.parent.mkdir(parents=True)
    own.write_text("# The collection's own README\n", encoding="utf-8")

    assert landings.main(["--root", str(tmp_path)]) == 1
    assert "refusing to replace or remove" in capsys.readouterr().err
    assert own.read_text(encoding="utf-8") == "# The collection's own README\n"
    assert not (tmp_path / "collections/demo/v1/README.md").exists()

    own.unlink()
    assert landings.main(["--root", str(tmp_path)]) == 0
    (own.parent / "collection.yaml").write_text("id: demo\n", encoding="utf-8")
    assert landings.main(["--root", str(tmp_path)]) == 1

    (own.parent / "collection.yaml").unlink()
    stray = tmp_path / "collections/demo/v9/README.md"
    stray.parent.mkdir(parents=True)
    stray.write_text("hand-written\n", encoding="utf-8")
    assert landings.main(["--root", str(tmp_path)]) == 1
    assert stray.read_text(encoding="utf-8") == "hand-written\n"


def test_install_commands_say_that_the_marketplace_source_is_public() -> None:
    manifest, marketplace = real_inputs()
    page = landings.expected_landings(manifest, marketplace)[
        Path("collections/proteomics/v1/README.md")
    ]

    assert "/plugin install proteomics@asb-skill-collections" in page
    assert "installs from the public domain repository" in page
    assert "these commands need no read access" in page
    assert "private" not in page
    assert "read access to it" not in page


def test_install_commands_require_an_exact_marketplace_source_path() -> None:
    manifest, marketplace = fixture_inputs()
    pages = landings.expected_landings(manifest, marketplace)
    current = pages[Path("collections/demo/v2/README.md")]
    legacy = pages[Path("collections/demo/v1/README.md")]

    assert "/plugin install demo@asb-skill-collections" in current
    assert "codex plugin add demo@asb-skill-collections" in current
    assert "/plugin install" not in legacy
    assert "codex plugin add" not in legacy


def test_every_relative_link_in_every_real_page_resolves() -> None:
    manifest, marketplace = real_inputs()
    pages = landings.expected_landings(manifest, marketplace)

    failures = []
    for relative, page in pages.items():
        for target in RELATIVE_LINK.findall(page):
            resolved = (REPO / relative.parent / target).resolve()
            if not resolved.exists():
                failures.append(f"{relative.as_posix()}: {target}")
    assert failures == []
