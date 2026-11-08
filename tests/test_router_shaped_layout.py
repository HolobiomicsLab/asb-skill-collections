"""A router-shaped collection stays cheap to install and searchable offline."""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

import pytest

from asb_skill_collections import layout


REPO = pathlib.Path(__file__).resolve().parent.parent
V2 = REPO / "tests" / "fixtures" / "router_collection"
ADVERTISED_TOKEN_BUDGET = 5_000


def _frontmatter(path: pathlib.Path) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    return match.group(1) if match else ""


def _advertised_skill_md() -> list[pathlib.Path]:
    return sorted((V2 / layout.ADVERTISED_DIRNAME).glob("*/SKILL.md"))


def _marketplace_units() -> list[pathlib.Path]:
    manifest = json.loads(
        (REPO / "tests/fixtures/marketplace_fixture.json").read_text(encoding="utf-8")
    )
    return [
        REPO / plugin["source"].lstrip("./")
        for plugin in manifest["plugins"]
        if isinstance(plugin["source"], str)
    ]


@pytest.mark.parametrize("unit", _marketplace_units(), ids=lambda path: path.name)
def test_every_offered_plugin_is_cheap_to_install(unit):
    advertised = sorted((unit / layout.ADVERTISED_DIRNAME).glob("*/SKILL.md"))
    total = sum(len(_frontmatter(path)) for path in advertised)
    assert total // 4 < ADVERTISED_TOKEN_BUDGET


@pytest.mark.parametrize("unit", _marketplace_units(), ids=lambda path: path.name)
def test_every_offered_plugin_can_retrieve_its_corpus(unit):
    if not layout.is_router_shaped(unit):
        pytest.skip("legacy layout: the corpus is advertised, not retrieved")
    assert (unit / "bin" / "search_skills.py").is_file()
    indexed = {row["slug"] for row in json.loads((unit / "skills_index.json").read_text())}
    on_disk = {path.name for path in (unit / "leaves").iterdir() if path.is_dir()}
    assert on_disk <= indexed


def test_collection_is_router_shaped():
    assert layout.is_router_shaped(V2)
    assert layout.leaf_dir(V2) == V2 / "leaves"


def test_corpus_lives_in_leaves_not_skills():
    assert len(list((V2 / "leaves").glob("*/SKILL.md"))) == 10
    assert len(_advertised_skill_md()) == 1


def test_router_is_advertised():
    assert {path.parent.name for path in _advertised_skill_md()} == {"_router"}


def test_advertised_frontmatter_fits_the_budget():
    total = sum(len(_frontmatter(path)) for path in _advertised_skill_md())
    assert total // 4 < ADVERTISED_TOKEN_BUDGET


def test_validation_still_covers_every_skill():
    found = layout.slugs(V2)
    indexed = {row["slug"] for row in json.loads((V2 / "skills_index.json").read_text())}
    assert indexed <= found


def test_resolver_handles_legacy_layout(tmp_path):
    legacy = tmp_path / "legacy"
    (legacy / "skills" / "alpha").mkdir(parents=True)
    (legacy / "skills" / "alpha" / "SKILL.md").write_text("---\nname: alpha\n---\n")
    assert not layout.is_router_shaped(legacy)
    assert layout.leaf_dir(legacy) == legacy / "skills"
    assert layout.slugs(legacy) == {"alpha"}


@pytest.mark.parametrize(
    "args",
    (
        ["--tool", "FormulaFixture", "-k", "1"],
        ["--query", "align retention time across samples", "-k", "1"],
        ["--technique", "LC-MS", "-k", "1"],
    ),
)
def test_search_script_returns_a_readable_path(args):
    out = subprocess.run(
        [sys.executable, str(V2 / "bin" / "search_skills.py"), *args],
        capture_output=True,
        text=True,
        cwd=V2,
        check=True,
    ).stdout
    read_lines = [line for line in out.splitlines() if line.strip().startswith("read:")]
    assert read_lines, out
    target = V2 / read_lines[0].split("read:")[1].strip()
    assert target.is_file()


def test_search_script_selftest_passes():
    subprocess.run(
        [sys.executable, str(V2 / "bin" / "search_skills.py"), "--selftest"],
        check=True,
        capture_output=True,
    )
