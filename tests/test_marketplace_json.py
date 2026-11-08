"""Marketplace entries use either local units or pinned remote subdirectories."""

from __future__ import annotations

import json
import pathlib
import re

import pytest


ROOT = pathlib.Path(__file__).parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "marketplace_fixture.json"
SHA = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def _source_is_valid(source, root: pathlib.Path) -> bool:
    if isinstance(source, str):
        return (root / source.lstrip("./") / ".claude-plugin" / "plugin.json").is_file()
    if not isinstance(source, dict) or source.get("source") != "git-subdir":
        return False
    path = source.get("path")
    return (
        isinstance(source.get("url"), str)
        and REPOSITORY.fullmatch(source["url"]) is not None
        and isinstance(path, str)
        and bool(path)
        and not path.startswith("/")
        and ".." not in pathlib.PurePosixPath(path).parts
        and source.get("ref") == "main"
        and isinstance(source.get("sha"), str)
        and SHA.fullmatch(source["sha"]) is not None
    )


@pytest.mark.parametrize("manifest", (FIXTURE,))
def test_every_marketplace_plugin_has_a_resolvable_source(manifest):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["plugins"]
    for plugin in data["plugins"]:
        source = plugin.get("source") or plugin.get("path")
        assert _source_is_valid(source, ROOT), plugin["name"]


def test_marketplace_json_carries_no_field_the_strict_validator_rejects():
    data = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    assert set(data) <= {"name", "description", "owner", "metadata", "plugins"}


def test_remote_source_does_not_need_a_local_checkout():
    remote = json.loads(FIXTURE.read_text())["plugins"][1]["source"]
    assert not (ROOT / remote["path"]).exists()
    assert _source_is_valid(remote, ROOT)


def test_repository_marketplace_entries_validate_in_a_temporary_checkout(tmp_path):
    source = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    for plugin in source["plugins"]:
        if isinstance(plugin.get("source"), str):
            unit = tmp_path / plugin["source"].lstrip("./")
            (unit / ".claude-plugin").mkdir(parents=True)
            (unit / ".claude-plugin" / "plugin.json").write_text("{}")
    for plugin in source["plugins"]:
        assert _source_is_valid(plugin.get("source") or plugin.get("path"), tmp_path)


@pytest.mark.parametrize(
    "change",
    (
        {"url": "not-a-repository"},
        {"path": "../outside"},
        {"path": "/absolute"},
        {"sha": "ABCDEF0123456789abcdef0123456789abcdef01"},
        {"sha": "0123"},
    ),
)
def test_invalid_remote_sources_are_refused(change):
    remote = dict(json.loads(FIXTURE.read_text())["plugins"][1]["source"])
    remote.update(change)
    assert not _source_is_valid(remote, ROOT)
