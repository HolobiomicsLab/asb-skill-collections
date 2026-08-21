"""Every composite workflow in the repo validates -- released or staged.

`validate_workflows.py` is run by `release_gate.check_workflows` over
`collections/*/v*/workflows`, and the CI job that walks staged content globs
`staged-collections/*/v*`. A workflow staged at `staged-collections/<domain>/
workflows/<slug>/` matches neither, so a broken manifest there reaches a
promotion PR unchecked -- the silent-clean-pass this suite exists to prevent.

The discovery below keys on structure (a directory holding both `SKILL.md` and
`workflow.yaml`) rather than on a list of paths, so a workflow staged somewhere
new is covered the day it is written instead of the day someone remembers to add
its path here.
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import validate_workflows  # noqa: E402

# The released collection is the slug authority: a workflow's leaves must resolve
# there whether the workflow itself is released or still staged.
SKILLS_INDEX = ROOT / "collections" / "metabolomics" / "v2" / "skills_index.json"


def workflow_dirs() -> list[pathlib.Path]:
    """Every workflow directory in the repo, found by shape."""
    found = []
    for root in ("collections", "staged-collections"):
        base = ROOT / root
        if not base.is_dir():
            continue
        for skill_md in base.rglob("workflows/*/SKILL.md"):
            d = skill_md.parent
            if d.name.startswith("_") or d.name == "bin":
                continue
            if (d / "workflow.yaml").is_file():
                found.append(d)
    return sorted(found)


@pytest.fixture(scope="module")
def slugs() -> set:
    return {r["slug"] for r in json.loads(SKILLS_INDEX.read_text())}


def test_discovery_finds_both_trees():
    """Guards the guard: if discovery silently matched nothing, every test below
    would pass without validating anything."""
    dirs = workflow_dirs()
    roots = {p.relative_to(ROOT).parts[0] for p in dirs}
    assert len(dirs) >= 21, f"expected the released workflows at least, found {len(dirs)}"
    assert "collections" in roots
    assert "staged-collections" in roots, (
        "no staged workflow discovered -- if staging was emptied on purpose, "
        "relax this; otherwise discovery has drifted"
    )


@pytest.mark.parametrize("wf_dir", workflow_dirs(), ids=lambda p: p.name)
def test_workflow_manifest_is_valid(wf_dir, slugs):
    errors = validate_workflows.validate_one(str(wf_dir), slugs)
    assert not errors, "\n".join(errors)
