"""Workflow discovery and validation operate on collection fixtures."""

from __future__ import annotations

import json
import pathlib
import sys

import pytest


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import validate_workflows  # noqa: E402


COLLECTION = ROOT / "tests" / "fixtures" / "router_collection"


def workflow_dirs(root: pathlib.Path = COLLECTION) -> list[pathlib.Path]:
    """Discover workflows by their two-file shape, not a released path list."""
    return sorted(
        path.parent
        for path in root.rglob("workflows/*/SKILL.md")
        if not path.parent.name.startswith("_")
        and (path.parent / "workflow.yaml").is_file()
    )


@pytest.fixture(scope="module")
def slugs() -> set[str]:
    rows = json.loads((COLLECTION / "skills_index.json").read_text())
    return {row["slug"] for row in rows}


def test_discovery_finds_the_fixture_workflows():
    assert len(workflow_dirs()) == 5


@pytest.mark.parametrize("workflow", workflow_dirs(), ids=lambda path: path.name)
def test_workflow_manifest_is_valid(workflow, slugs):
    errors = validate_workflows.validate_one(str(workflow), slugs)
    assert not errors, "\n".join(errors)
