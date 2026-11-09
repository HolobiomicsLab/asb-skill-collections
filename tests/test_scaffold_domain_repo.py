"""Scaffold complete released and candidate domain repository surfaces."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys

import yaml

from scripts import scaffold_domain_repo


REPO = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
SHA = "c" * 40
ALLOWED_GITHUB_URLS = re.compile(
    r"https://github\.com/HolobiomicsLab(?:"
    r"/asb-skill-collections(?:\.git)?|/asb-skills-fixture(?:\.git)?|)"
    r"(?:[/#?][^\s)\"']*)?"
)


def write_manifest(tmp_path: Path) -> Path:
    document = {
        "domains": {
            "fixture": {
                "concept_doi": "10.5281/zenodo.1234",
                "releases": [
                    {
                        "version": 2, "path": "collections/fixture/v2", "released": "2026-11-09",
                        "skills": 20, "tools": 4, "version_doi": "10.5281/zenodo.5678",
                    },
                    {
                        "version": 1, "path": "collections/fixture/v1", "released": "2026-10-15",
                        "skills": 15, "tools": 3, "version_doi": "10.5281/zenodo.4567",
                    },
                    {
                        "version": 1, "path": "collections/fixture/v1-legacy", "released": "2026-10-01",
                        "skills": 10, "tools": 2, "version_doi": None, "status": "legacy",
                    },
                ],
            }
        }
    }
    path = tmp_path / "collections.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return path


def run_scaffold(tmp_path: Path, stage: str = "released", out_name: str = "domain") -> Path:
    out = tmp_path / out_name
    arguments = [
        "--domain", "fixture", "--title", "fixture science", "--out", str(out),
        "--tooling-sha", SHA, "--stage", stage, "--manifest", str(write_manifest(tmp_path)),
    ]
    if stage == "candidate":
        arguments.extend(["--collection-path", "collections/fixture/v1"])
    paths = scaffold_domain_repo.scaffold(scaffold_domain_repo.Options(**vars(scaffold_domain_repo.parser().parse_args(arguments))))
    assert paths
    return out


def assert_complete_surface(out: Path) -> None:
    for path in out.rglob("*"):
        if path.is_file():
            assert not re.search(r"<[A-Z][A-Z0-9_]+>", path.read_text(encoding="utf-8")), path
            for url in re.findall(r"https://github\.com/[^\s)\"']+", path.read_text(encoding="utf-8")):
                assert ALLOWED_GITHUB_URLS.fullmatch(url), (path, url)
    marketplace = json.loads((out / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    assert marketplace["owner"]["name"] == "Holobiomics Lab"
    for workflow in (out / ".github/workflows").glob("*.yml"):
        assert yaml.safe_load(workflow.read_text(encoding="utf-8"))
    assert yaml.safe_load((out / "CITATION.cff").read_text(encoding="utf-8"))["cff-version"] == "1.2.0"
    assert json.loads((out / ".zenodo.json").read_text(encoding="utf-8"))["license"] == "CC-BY-4.0"


def test_released_scaffold_uses_registry_releases(tmp_path: Path) -> None:
    out = run_scaffold(tmp_path)
    assert_complete_surface(out)
    readme = (out / "README.md").read_text(encoding="utf-8")
    assert "ASB Skills: fixture science" in readme
    assert "collections/fixture/v2" in readme
    assert "collections/fixture/v1-legacy" not in readme
    assert "asbb install --repo <checkout> --skills <slug-a>,<slug-b> --collection fixture/v2" in readme
    marketplace = json.loads((out / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    assert [plugin["name"] for plugin in marketplace["plugins"]] == ["fixture", "fixture-v1"]
    assert marketplace["plugins"][0]["source"] == "./collections/fixture/v2"
    assert (out / "LICENSE").read_bytes() == (REPO / "LICENSE").read_bytes()
    assert (out / "collections/fixture/proposals/.gitkeep").is_file()


def test_candidate_scaffold_needs_no_registry_entry(tmp_path: Path) -> None:
    manifest = tmp_path / "collections.yaml"
    manifest.write_text("domains: {}\n", encoding="utf-8")
    out = tmp_path / "candidate"
    options = scaffold_domain_repo.parser().parse_args([
        "--domain", "fixture", "--title", "fixture science", "--out", str(out),
        "--tooling-sha", SHA, "--stage", "candidate", "--manifest", str(manifest),
        "--collection-path", "collections/fixture/v1",
    ])
    scaffold_domain_repo.scaffold(scaffold_domain_repo.Options(**vars(options)))
    assert_complete_surface(out)
    assert "candidate/<cut-id>" in (out / "README.md").read_text(encoding="utf-8")
    assert json.loads((out / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))["plugins"] == []
    gates = (out / ".github/workflows/gates.yml").read_text(encoding="utf-8")
    assert gates.count("- domain: fixture") == 1
    assert "# candidate stage:" in gates
    issue = (out / ".github/ISSUE_TEMPLATE/propose-paper.md").read_text(encoding="utf-8")
    assert "metabolomics (default)" not in issue
    assert 'labels: ["propose", "paper-intake", "needs-triage"]' in issue


def test_released_scaffold_rejects_a_legacy_only_domain(tmp_path: Path) -> None:
    manifest = tmp_path / "collections.yaml"
    manifest.write_text(
        "domains:\n  fixture:\n    releases:\n      - status: legacy\n        path: collections/fixture/v1\n",
        encoding="utf-8",
    )
    result = subprocess.run([
        PYTHON, str(REPO / "scripts/scaffold_domain_repo.py"), "--domain", "fixture", "--title", "Fixture",
        "--out", str(tmp_path / "out"), "--tooling-sha", SHA, "--stage", "released", "--manifest", str(manifest),
    ], capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert "no non-legacy release" in result.stderr


def test_nonempty_directory_force_and_dry_run(tmp_path: Path) -> None:
    out = run_scaffold(tmp_path)
    with pytest_raises("use --force"):
        run_scaffold(tmp_path)
    assert (out / "README.md").is_file()


def pytest_raises(message: str):
    import pytest
    return pytest.raises(ValueError, match=message)


def test_force_replaces_scaffold_files_and_dry_run_writes_nothing(tmp_path: Path) -> None:
    out = run_scaffold(tmp_path)
    (out / "README.md").write_text("stale\n", encoding="utf-8")
    arguments = [
        "--domain", "fixture", "--title", "fixture science", "--out", str(out), "--tooling-sha", SHA,
        "--manifest", str(write_manifest(tmp_path)), "--force",
    ]
    scaffold_domain_repo.scaffold(scaffold_domain_repo.Options(**vars(scaffold_domain_repo.parser().parse_args(arguments))))
    assert "stale" not in (out / "README.md").read_text(encoding="utf-8")
    dry = tmp_path / "dry"
    arguments[-1] = "--dry-run"
    arguments[arguments.index(str(out))] = str(dry)
    assert scaffold_domain_repo.main(arguments) == 0
    assert not dry.exists()
    assert not list(tmp_path.rglob("*.pyc"))


def test_policy_rejects_a_private_pipeline_url() -> None:
    """Publication drafts cannot reintroduce the private pipeline URL."""
    import pytest
    pipeline_url = "https://github.com/HolobiomicsLab/" + "AgenticScienceBuilder"
    with pytest.raises(ValueError, match="disallowed GitHub URL"):
        scaffold_domain_repo.validate_urls(
            {"CITATION.cff": pipeline_url}, "fixture"
        )


def test_policy_accepts_punctuation_after_an_allowed_url() -> None:
    """Prose punctuation is not part of an allowlisted URL."""
    scaffold_domain_repo.validate_urls(
        {"CITATION.cff": "https://github.com/HolobiomicsLab/asb-skills-fixture; registry"}, "fixture"
    )


def test_publication_drafts_drop_private_pipeline_links(tmp_path: Path) -> None:
    """Draft metadata retains its facts while removing a prohibited URL."""
    drafts = tmp_path / "rendered"
    target = drafts / "fixture"
    target.mkdir(parents=True)
    pipeline_url = "https://github.com/HolobiomicsLab/" + "AgenticScienceBuilder"
    (target / "CITATION.cff").write_text(yaml.safe_dump({
        "cff-version": "1.2.0", "message": "Cite this collection", "title": "Fixture",
        "authors": [{"name": "Holobiomics Lab"}], "license": "CC-BY-4.0",
        "abstract": f"generating pipeline - {pipeline_url}",
        "references": [{"repository-code": pipeline_url}],
    }, sort_keys=False), encoding="utf-8")
    (target / ".zenodo.json").write_text(json.dumps({
        "license": "CC-BY-4.0",
        "description": f"generating pipeline - {pipeline_url}",
        "related_identifiers": [{"identifier": pipeline_url}],
    }), encoding="utf-8")
    options = scaffold_domain_repo.Options(
        domain="fixture", title="fixture", out=tmp_path / "out", tooling_sha=SHA,
        stage="candidate", collection_path="collections/fixture/v1", publication_drafts=drafts,
    )
    files = scaffold_domain_repo.output_files(options)
    assert pipeline_url not in files["CITATION.cff"]
    assert pipeline_url not in files[".zenodo.json"]
