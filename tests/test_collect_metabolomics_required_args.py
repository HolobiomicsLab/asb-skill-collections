"""The metabolomics collector needs its two inputs named; it has no local default.

``--builds-root`` and ``--corpus`` defaulted to one maintainer's checkout
paths, which published that machine's layout and made a run on any other
machine fail on a path nobody named. Both are required now, so a run without
them stops with a usage error before reading anything.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "collect_metabolomics_collection.py"


@pytest.mark.parametrize(
    "argv",
    [[], ["--corpus", "corpus.json"], ["--builds-root", "builds"]],
    ids=["neither", "no-builds-root", "no-corpus"],
)
def test_a_run_without_both_inputs_is_a_usage_error(argv: list[str], tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--dry-run", *argv],
        cwd=tmp_path, capture_output=True, text=True, timeout=60,
    )

    assert result.returncode == 2, result.stdout + result.stderr
    assert "the following arguments are required" in result.stderr
    missing = {"--builds-root", "--corpus"} - set(argv)
    for flag in missing:
        assert flag in result.stderr


def test_the_script_names_no_local_path() -> None:
    text = SCRIPT.read_text(encoding="utf-8")

    assert "/Users/" not in text
    assert "/home/" not in text
