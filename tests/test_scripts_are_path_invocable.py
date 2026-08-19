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

# A script that carries the sys.path bootstrap is *claiming* it can be run by
# path. Testing only the CI-invoked ones let `skill_index.py` ship with the
# bootstrap placed below its first sibling import, where it does nothing: no
# workflow ran it, so nothing noticed.
BOOTSTRAP = 'if __package__ in (None, ""):'


def _path_invocable_scripts() -> list[str]:
    """Every script CI runs by path, plus every script that claims it can be."""
    found: set[str] = set()
    for workflow in sorted(WORKFLOWS.glob("*.yml")):
        found.update(m.group(1) for m in INVOCATION.finditer(workflow.read_text(encoding="utf-8")))
    for script in sorted((REPO / "scripts").glob("*.py")):
        if BOOTSTRAP in script.read_text(encoding="utf-8"):
            found.add(script.relative_to(REPO).as_posix())
    return sorted(rel for rel in found if (REPO / rel).is_file())


def _clean_env() -> dict[str, str]:
    """The runner's environment: no PYTHONPATH to paper over a bad import."""
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    return env


@pytest.mark.parametrize("rel", _path_invocable_scripts())
def test_a_path_invocable_script_imports_cleanly_by_path(rel):
    """`--help` is enough: the failure is at import time, before any argument."""
    proc = subprocess.run(
        [sys.executable, rel, "--help"],
        cwd=REPO, env=_clean_env(), capture_output=True, text=True,
    )
    assert "ModuleNotFoundError" not in proc.stderr, (
        f"{rel} cannot be run the way CI runs it:\n{proc.stderr.strip()[-400:]}"
    )


SIBLING_IMPORT = re.compile(r"^\s*(?:from|import)\s+(?:scripts|asb_skill_collections)\b", re.M)


def _runnable_scripts_importing_a_sibling() -> list[str]:
    """Scripts with a `__main__` block that reach for a sibling package."""
    out = []
    for script in sorted((REPO / "scripts").glob("*.py")):
        text = script.read_text(encoding="utf-8")
        if '__name__ == "__main__"' in text and SIBLING_IMPORT.search(text):
            out.append(script.relative_to(REPO).as_posix())
    return out


@pytest.mark.parametrize("rel", _runnable_scripts_importing_a_sibling())
def test_the_bootstrap_comes_before_the_first_sibling_import(rel):
    """A bootstrap below the import it enables is dead code.

    Cheaper and sharper than the subprocess probe: it names the line, and it
    still bites in an environment where an editable install would resolve the
    import anyway.
    """
    text = (REPO / rel).read_text(encoding="utf-8")
    assert BOOTSTRAP in text, f"{rel} imports a sibling but cannot be run by path"
    assert SIBLING_IMPORT.search(text).start() > text.index(BOOTSTRAP), (
        f"{rel} bootstraps sys.path *after* its first sibling import, so the "
        f"bootstrap never runs in time"
    )


def test_the_release_gate_runs_by_path_without_pythonpath():
    """The gate is the one CI blocks on; prove it end to end, not just --help."""
    proc = subprocess.run(
        [sys.executable, "scripts/release_gate.py", "collections/epigenomics/v1", "--strict"],
        cwd=REPO, env=_clean_env(), capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr.strip()[-600:] or proc.stdout.strip()[-600:]
