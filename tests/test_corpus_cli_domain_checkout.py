"""Corpus maintenance commands require an explicit domain checkout input."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent


def test_missing_domain_manifest_is_refused(tmp_path: Path) -> None:
    from scripts.regen_catalogue import main

    assert main(["--repo-root", str(tmp_path)]) == 1


@pytest.mark.parametrize(
    "script", ["preprint_license.py", "repair_corpus_dois.py", "resolve_paper_license.py"]
)
def test_corpus_argument_is_required_and_names_domain_checkout(script: str) -> None:
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / script), "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "--corpus" in result.stdout
    assert "domain checkout" in result.stdout
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / script)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "required" in result.stderr
