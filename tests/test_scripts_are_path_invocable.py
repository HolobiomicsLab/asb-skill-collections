"""Scripts documented as `python scripts/x.py` must run that way.

Running a script by path puts *its own directory* on ``sys.path``, not the
repository root — so ``from scripts import layout`` raises ModuleNotFoundError
even though the same import works under pytest, which does put the root there.
CI invokes the release gate exactly that way, and every local run that exported
PYTHONPATH hid the breakage.

One local caveat: a developer whose interpreter carries an editable install of
``scripts`` from another checkout will see the import succeed anyway, resolved
against that other tree. The end-to-end gate test below still fails, and a CI
runner has no such install, so the pair holds. Do not "fix" a red run here by
exporting PYTHONPATH.
"""

from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
WORKFLOWS = REPO / ".github" / "workflows"
INVOCATION = re.compile(r"python3?\s+(scripts/[a-z_0-9]+\.py)")


def _ci_invoked_scripts() -> list[str]:
    """Every `python scripts/x.py` a CI workflow actually runs."""
    found: set[str] = set()
    for workflow in sorted(WORKFLOWS.glob("*.yml")):
        text = workflow.read_text(encoding="utf-8")
        found.update(m.group(1) for m in INVOCATION.finditer(text))
    return sorted(rel for rel in found if (REPO / rel).is_file())


def _clean_env() -> dict[str, str]:
    """The runner's environment: no PYTHONPATH to paper over a bad import."""
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    return env


@pytest.mark.parametrize("rel", _ci_invoked_scripts())
def test_a_ci_invoked_script_imports_cleanly_by_path(rel):
    """`--help` is enough: the failure is at import time, before any argument."""
    proc = subprocess.run(
        [sys.executable, rel, "--help"],
        cwd=REPO, env=_clean_env(), capture_output=True, text=True,
    )
    assert "ModuleNotFoundError" not in proc.stderr, (
        f"{rel} cannot be run the way CI runs it:\n{proc.stderr.strip()[-400:]}"
    )


def test_the_release_gate_runs_by_path_without_pythonpath():
    """The gate is the one CI blocks on; prove it end to end, not just --help."""
    proc = subprocess.run(
        [sys.executable, "scripts/release_gate.py", "collections/epigenomics/v1", "--strict"],
        cwd=REPO, env=_clean_env(), capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr.strip()[-600:] or proc.stdout.strip()[-600:]
