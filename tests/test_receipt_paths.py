"""Receipts written by a candidate assembly carry no absolute path.

The receipts land in the public skills repositories beside each collection.
The writers recorded the scratch and home directories of the machine that ran
them (source.json view, join.txt, gate.txt, gate_report.json, the check_*.txt
logs, same_paper_pairs.json and collect_receipt.json builds_root), and a
by-hand scrub did not survive the next run. Each writer now records a path
relative to the git checkout that holds it, or else by its final component.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.recorded_path import recorded_child, recorded_path


REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "assemble_candidate.py"
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs"
ABSOLUTE = re.compile(r"(^|[\"'\s:=(])(/Users/|/home/|/private/|/tmp/|/var/folders/|[A-Za-z]:\\\\)")
COMMIT = "0123456789abcdef0123456789abcdef01234567"


def test_a_path_in_a_checkout_is_recorded_relative_to_it(tmp_path: Path) -> None:
    (tmp_path / "checkout" / ".git").mkdir(parents=True)
    target = tmp_path / "checkout" / "outputs" / "cut"
    target.mkdir(parents=True)

    assert recorded_path(target) == "outputs/cut"
    assert recorded_path(tmp_path / "checkout") == "."
    assert recorded_child(target, target / "leaves" / "a" / "SKILL.md") == (
        "outputs/cut/leaves/a/SKILL.md"
    )


def test_a_path_outside_any_checkout_is_recorded_by_its_name(tmp_path: Path) -> None:
    target = tmp_path / "scratch" / "candidate"
    target.mkdir(parents=True)

    assert recorded_path(target) == "candidate"
    assert recorded_child(target, target / "leaves" / "a" / "SKILL.md") == (
        "candidate/leaves/a/SKILL.md"
    )


@pytest.fixture(scope="module")
def assembled(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, Path]:
    """Assemble the fixture in a scratch directory that no checkout holds."""
    root = tmp_path_factory.mktemp("receipt-paths")
    fixture = root / "fixture"
    shutil.copytree(FIXTURE, fixture)
    receipts = root / "receipts"
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
        [
            sys.executable,
            str(SCRIPT),
            "--cut",
            str(fixture / "corpus"),
            "--builds",
            str(fixture / "builds"),
            "--tiered",
            str(fixture / "metabarcoding_tiered.json"),
            "--domain",
            "metabarcoding",
            "--version",
            "v1",
            "--out",
            str(root / "candidate"),
            "--receipts",
            str(receipts),
            "--asb-commit",
            COMMIT,
            "--tooling-commit",
            COMMIT,
            "--corpus-commit",
            COMMIT,
            "--verified-on",
            "2026-09-18",
        ],
        cwd=REPO,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert result.returncode == 0, result.stdout
    return root, receipts


def test_assembled_receipts_carry_no_absolute_path(assembled: tuple[Path, Path]) -> None:
    root, receipts = assembled
    files = sorted(path for path in receipts.rglob("*") if path.is_file())
    assert {path.name for path in files} >= {
        "check_license_tiers.txt",
        "check_provenance_tiers.txt",
        "check_tools_index.txt",
        "collect_receipt.json",
        "gate.txt",
        "gate_report.json",
        "join.txt",
        "same_paper_pairs.json",
        "source.json",
    }
    leaks = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        found = [
            marker
            for marker in (str(root), str(root.resolve()), str(REPO))
            if marker in text
        ]
        if found or ABSOLUTE.search(text):
            leaks[path.name] = found or ABSOLUTE.search(text).group(0)
    assert leaks == {}


def test_assembled_receipts_name_their_inputs(assembled: tuple[Path, Path]) -> None:
    _, receipts = assembled

    assert '"view": "corpus"' in (receipts / "source.json").read_text("utf-8")
    assert "collection : candidate" in (receipts / "gate.txt").read_text("utf-8")
    assert "report     : gate_report.json" in (receipts / "gate.txt").read_text("utf-8")
    assert (receipts / "check_license_tiers.txt").read_text("utf-8").startswith(
        "OK   candidate"
    )
