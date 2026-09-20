"""Contract tests for the candidate release-surface check."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tests.test_run_candidate_gates import _prepared_candidate


REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "check_release_surface.py"
DOI = "10.5281/zenodo.20794027"
IRI = "https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2"
RETRACTED_PHRASES = {
    "gradable-by-solver": "is gradable by `asb solve-workflow`",
    "gradable-workflow": "a gradable `workflow.yaml`",
    "eval-ablation-set": "is the eval-ablation set",
    "staging-only": "STAGING ONLY",
    "promote-via-gate": "promote via `release_gate.py`",
    "staged-not-released": "are **staged** (not yet released)",
    "staged-set": "this staged set",
    "staging-heading": "— STAGING",
}


def _run(
    candidate: Path, *, rules: Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Invoke the release-surface check in the fixed offline environment."""
    environment = dict(os.environ)
    for key in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"):
        environment.pop(key, None)
    environment.update(
        HF_HUB_OFFLINE="1",
        TRANSFORMERS_OFFLINE="1",
        ASB_EMBED_MODEL="bge-small-en-v1.5",
        PYTHONDONTWRITEBYTECODE="1",
    )
    command = [sys.executable, str(SCRIPT), str(candidate)]
    if rules is not None:
        command.extend(["--rules", str(rules)])
    return subprocess.run(
        command,
        cwd=REPO,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _write_zenodo(candidate: Path, document: dict) -> None:
    """Write deterministic candidate deposit metadata."""
    (candidate / ".zenodo.json").write_text(
        json.dumps(document, indent=2) + "\n", encoding="utf-8"
    )


def test_prepared_candidate_has_no_surface_findings(tmp_path: Path) -> None:
    """Keep the prepared public fixture clean under the recorded rules."""
    result = _run(_prepared_candidate(tmp_path))

    assert result.returncode == 0, result.stderr
    assert re.fullmatch(
        r"surface: 0 findings in \d+ files scanned \(0 skipped undecodable\)\n",
        result.stdout,
    )


def test_v2_doi_in_workflow_is_a_finding(tmp_path: Path) -> None:
    """Reject a foreign release DOI wherever candidate prose carries it."""
    candidate = _prepared_candidate(tmp_path)
    skill = candidate / "workflows" / "example" / "SKILL.md"
    skill.parent.mkdir(parents=True, exist_ok=True)
    skill.write_text(
        f"# Example workflow\n\nRelease DOI: {DOI}\n",
        encoding="utf-8",
    )

    result = _run(candidate)

    assert result.returncode == 1, result.stderr
    assert (
        f"workflows/example/SKILL.md:3: metabolomics-v2-doi: {DOI}"
    ) in result.stdout


@pytest.mark.parametrize(
    ("domain", "version"), [("metabolomics", "v3"), ("astronomy", "v1")]
)
def test_identifier_rules_are_domain_neutral(
    tmp_path: Path, domain: str, version: str
) -> None:
    """Reject a foreign identifier independently of candidate domain."""
    candidate = _prepared_candidate(tmp_path)
    (candidate / "collection.yaml").write_text(
        f"domain: {domain}\nversion: {version}\n", encoding="utf-8"
    )
    (candidate / "README.md").write_text(f"{DOI}\n", encoding="utf-8")

    result = _run(candidate)

    assert result.returncode == 1, result.stderr
    assert "README.md:1: metabolomics-v2-doi" in result.stdout


@pytest.mark.parametrize(("rule_id", "phrase"), RETRACTED_PHRASES.items())
def test_each_retracted_phrase_is_a_finding(
    tmp_path: Path, rule_id: str, phrase: str
) -> None:
    """Report every recorded retraction under its own data-defined id."""
    candidate = _prepared_candidate(tmp_path)
    (candidate / "README.md").write_text(f"{phrase}\n", encoding="utf-8")

    result = _run(candidate)

    assert result.returncode == 1, result.stderr
    assert f"README.md:1: {rule_id}: {phrase}" in result.stdout


def test_phrase_matching_collapses_whitespace_and_case(tmp_path: Path) -> None:
    """Find a retracted sentence after wrapping and recasing it."""
    candidate = _prepared_candidate(tmp_path)
    (candidate / "README.md").write_text(
        "Context\nIS GRADABLE BY `ASB\nSOLVE-WORKFLOW`\n", encoding="utf-8"
    )

    result = _run(candidate)

    assert result.returncode == 1, result.stderr
    assert "README.md:2: gradable-by-solver:" in result.stdout


@pytest.mark.parametrize("relation", ["isNewVersionOf", "isPreviousVersionOf"])
def test_doi_is_allowed_as_zenodo_lineage_identifier(
    tmp_path: Path, relation: str
) -> None:
    """Permit the previous deposit DOI only in an approved lineage relation."""
    candidate = _prepared_candidate(tmp_path)
    _write_zenodo(
        candidate,
        {
            "title": "Candidate",
            "related_identifiers": [{"identifier": DOI, "relation": relation}],
        },
    )

    result = _run(candidate)

    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize(
    ("relative_path", "document"),
    [
        (
            ".zenodo.json",
            {
                "description": DOI,
                "related_identifiers": [
                    {"identifier": DOI, "relation": "isNewVersionOf"}
                ],
            },
        ),
        (
            ".zenodo.json",
            {
                "related_identifiers": [
                    {"identifier": DOI, "relation": "isSupplementTo"}
                ]
            },
        ),
        (
            ".zenodo.json",
            {"related_identifiers": [{"other_key": DOI, "relation": "isNewVersionOf"}]},
        ),
        ("collection.yaml", f"doi: {DOI}\n"),
    ],
)
def test_doi_outside_approved_lineage_value_is_a_finding(
    tmp_path: Path, relative_path: str, document: dict | str
) -> None:
    """Reject the DOI in prose, another relation, or another file."""
    candidate = _prepared_candidate(tmp_path)
    target = candidate / relative_path
    if isinstance(document, dict):
        target.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    else:
        target.write_text(document, encoding="utf-8")

    result = _run(candidate)

    assert result.returncode == 1, result.stderr
    assert f"{relative_path}:" in result.stdout
    assert "metabolomics-v2-doi" in result.stdout
    assert "surface: 1 findings" in result.stdout


def test_iri_has_no_zenodo_lineage_exception(tmp_path: Path) -> None:
    """Reject the foreign collection IRI even in an approved relation shape."""
    candidate = _prepared_candidate(tmp_path)
    _write_zenodo(
        candidate,
        {"related_identifiers": [{"identifier": IRI, "relation": "isNewVersionOf"}]},
    )

    result = _run(candidate)

    assert result.returncode == 1, result.stderr
    assert ".zenodo.json:4: metabolomics-v2-iri" in result.stdout


def test_invalid_utf8_is_counted_and_skipped(tmp_path: Path) -> None:
    """Skip an undecodable regular file without failing a clean candidate."""
    candidate = _prepared_candidate(tmp_path)
    (candidate / "opaque.bin").write_bytes(b"\xff\xfe\x00")

    result = _run(candidate)

    assert result.returncode == 0, result.stderr
    assert re.search(
        r"surface: 0 findings in \d+ files scanned \(1 skipped undecodable\)\n$",
        result.stdout,
    )


def test_second_run_is_byte_identical(tmp_path: Path) -> None:
    """Emit byte-identical output for an unchanged candidate."""
    candidate = _prepared_candidate(tmp_path)

    first = _run(candidate)
    second = _run(candidate)

    assert first.returncode == second.returncode == 0
    assert first.stdout.encode() == second.stdout.encode()
    assert first.stderr.encode() == second.stderr.encode()


def test_missing_candidate_and_invalid_rules_exit_two(tmp_path: Path) -> None:
    """Reserve exit two for invalid checker inputs."""
    missing = _run(tmp_path / "missing")
    assert missing.returncode == 2
    assert "ERROR:" in missing.stderr

    candidate = tmp_path / "candidate"
    candidate.mkdir()
    rules = tmp_path / "rules.yaml"
    rules.write_text("foreign_identifiers: [\n", encoding="utf-8")
    invalid_rules = _run(candidate, rules=rules)
    assert invalid_rules.returncode == 2
    assert "ERROR:" in invalid_rules.stderr
