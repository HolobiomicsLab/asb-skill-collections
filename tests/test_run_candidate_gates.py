"""Contract tests for the seven-check candidate gate runner."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from scripts import run_candidate_gates as gate_runner
from scripts import bootstrap_indexes as bootstrap


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs"
CREATORS = REPO / "scripts" / "release_creators.yaml"
EXPECTED_CHECKS = {
    "gate",
    "lint",
    "check_license_tiers",
    "check_provenance_tiers",
    "check_tools_index",
    "surface",
    "verify",
}
EXPECTED_LOGS = {f"{name}.txt" for name in EXPECTED_CHECKS}


def _prepared_candidate(tmp_path: Path) -> Path:
    """Collect the Task 3 fixture and bootstrap it through the first S5 half."""
    candidate = tmp_path / "candidate"
    corpus = candidate / "corpus.yaml"
    collector_receipts = tmp_path / "collector-receipts"
    args = [
        "--cut",
        str(FIXTURE / "corpus"),
        "--domain",
        "metabarcoding",
        "--version",
        "v1",
        "--out",
        str(candidate),
        "--license",
        "CC-BY-4.0",
        "--plugin-repo",
        "https://github.com/HolobiomicsLab/asb-skills-metabarcoding",
        "--creators",
        str(CREATORS),
        "--corpus",
        str(FIXTURE / "corpus.yaml"),
        "--receipts",
        str(collector_receipts),
    ]
    environment = dict(os.environ)
    for key in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"):
        environment.pop(key, None)
    environment.update(
        HF_HUB_OFFLINE="1",
        TRANSFORMERS_OFFLINE="1",
        ASB_EMBED_MODEL="bge-small-en-v1.5",
        PYTHONDONTWRITEBYTECODE="1",
    )
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "collect_from_cut.py"), *args],
        cwd=REPO,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert result.returncode == 0, result.stdout
    shutil.copy2(FIXTURE / "corpus.yaml", corpus)
    assert (
        bootstrap.main(
            [
                str(candidate),
                "--corpus",
                str(corpus),
                "--receipts",
                str(tmp_path / "bootstrap-receipts"),
            ]
        )
        == 0
    )
    return candidate


def _run(candidate: Path, receipts: Path, *, dry_run: bool = False) -> int:
    """Invoke the public gate runner interface."""
    args = [
        str(candidate),
        "--corpus",
        str(candidate / "corpus.yaml"),
        "--receipts",
        str(receipts),
    ]
    if dry_run:
        args.append("--dry-run")
    return gate_runner.main(args)


def _tree_bytes(root: Path) -> dict[str, bytes]:
    """Return a byte-exact snapshot for dry-run assertions."""
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _plant_personal_email(candidate: Path) -> None:
    """Add one gate-parsed evidence span containing a real personal address."""
    leaf = next(iter(sorted((candidate / "leaves").glob("*/SKILL.md"))))
    text = leaf.read_text(encoding="utf-8")
    leaf.write_text(
        text.rstrip()
        + '\n- [contact] data contact: "Email name@ulb.ac.be for the data."\n',
        encoding="utf-8",
    )


def test_runner_executes_seven_checks_and_verifies_receipt(tmp_path: Path) -> None:
    """Keep all seven zero exit codes and a verified strict gate receipt."""
    candidate = _prepared_candidate(tmp_path)
    receipts = tmp_path / "gate-receipts"

    assert _run(candidate, receipts) == 0
    report = json.loads((receipts / "gate_report.json").read_text(encoding="utf-8"))
    checks = json.loads((receipts / "checks.json").read_text(encoding="utf-8"))
    assert report["release_verified"] is True
    assert checks == {
        "stage": "S5",
        "exit_code": 0,
        "checks": {
            "gate": 0,
            "lint": 0,
            "check_license_tiers": 0,
            "check_provenance_tiers": 0,
            "check_tools_index": 0,
            "surface": 0,
            "verify": 0,
        },
    }
    assert EXPECTED_LOGS <= {path.name for path in receipts.glob("*.txt")}


def test_runner_preserves_real_email_finding(tmp_path: Path) -> None:
    """Run every check after a hard PII failure and retain the named finding."""
    candidate = _prepared_candidate(tmp_path)
    receipts = tmp_path / "gate-receipts"
    _plant_personal_email(candidate)

    assert _run(candidate, receipts) == 1
    checks = json.loads((receipts / "checks.json").read_text(encoding="utf-8"))
    assert set(checks["checks"]) == EXPECTED_CHECKS
    assert checks["checks"]["gate"] == 1
    assert checks["exit_code"] == 1
    assert EXPECTED_LOGS <= {path.name for path in receipts.glob("*.txt")}
    gate_log = (receipts / "gate.txt").read_text(encoding="utf-8")
    assert "name@ulb.ac.be" in gate_log
    assert "non-author personal email" in gate_log


def test_runner_preserves_surface_finding_and_runs_every_check(tmp_path: Path) -> None:
    """Retain a foreign DOI finding without short-circuiting later checks."""
    candidate = _prepared_candidate(tmp_path)
    receipts = tmp_path / "gate-receipts"
    readme = candidate / "README.md"
    readme.write_text(
        "Foreign release DOI: 10.5281/zenodo.20794027\n",
        encoding="utf-8",
    )

    assert _run(candidate, receipts) == 1
    checks = json.loads((receipts / "checks.json").read_text(encoding="utf-8"))
    assert checks["checks"]["surface"] == 1
    assert checks["exit_code"] == 1
    assert all(
        code == 0 for name, code in checks["checks"].items() if name != "surface"
    )
    assert set(checks["checks"]) == EXPECTED_CHECKS
    surface_log = (receipts / "surface.txt").read_text(encoding="utf-8")
    assert "README.md:" in surface_log
    assert "metabolomics-v2-doi" in surface_log


def test_runner_dry_run_prints_commands_and_writes_nothing(
    tmp_path: Path, capsys
) -> None:
    """Print the exact seven commands under the active interpreter without writes."""
    candidate = _prepared_candidate(tmp_path)
    receipts = tmp_path / "gate-receipts"
    before = _tree_bytes(candidate)

    assert _run(candidate, receipts, dry_run=True) == 0
    assert _tree_bytes(candidate) == before
    assert not receipts.exists()
    plan = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert plan["dry_run"] is True
    assert len(plan["commands"]) == 7
    assert all(command[0] == sys.executable for command in plan["commands"])
