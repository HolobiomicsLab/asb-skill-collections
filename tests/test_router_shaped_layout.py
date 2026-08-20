"""A router-shaped collection must stay cheap to install.

A plugin host advertises every skill under a plugin's ``skills/`` directory by
injecting its name and description into the session prompt. These tests pin the
property that makes the metabolomics collection installable at all: the corpus
lives in ``leaves/`` and only a couple of entry points are advertised.
"""

from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

import pytest

from scripts import layout

REPO = pathlib.Path(__file__).resolve().parent.parent
V2 = REPO / "collections" / "metabolomics" / "v2"

# A session that spends more than this on one plugin's frontmatter has no room
# left to work; the pre-fix collection cost ~450k.
ADVERTISED_TOKEN_BUDGET = 5_000


def _marketplace_units() -> list[pathlib.Path]:
    """Every plugin directory the marketplace offers for installation."""
    manifest = json.loads(
        (REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )
    return [REPO / p["source"].lstrip("./") for p in manifest["plugins"]]


@pytest.mark.parametrize(
    "unit", _marketplace_units(), ids=lambda p: p.name
)
def test_every_offered_plugin_is_cheap_to_install(unit):
    """No plugin may charge a user's session for a corpus it ships as data."""
    advertised = sorted((unit / layout.ADVERTISED_DIRNAME).glob("*/SKILL.md"))
    total = sum(len(_frontmatter(p)) for p in advertised)
    assert total // 4 < ADVERTISED_TOKEN_BUDGET, (
        f"{unit.name} advertises {len(advertised)} skills costing ~{total // 4} "
        f"tokens at session start, over the {ADVERTISED_TOKEN_BUDGET} budget"
    )


@pytest.mark.parametrize(
    "unit", _marketplace_units(), ids=lambda p: p.name
)
def test_every_offered_plugin_can_retrieve_its_corpus(unit):
    """A router-shaped unit must ship the index and script its router promises."""
    if not layout.is_router_shaped(unit):
        pytest.skip("legacy layout: the corpus is advertised, not retrieved")
    assert (unit / "bin" / "search_skills.py").is_file()
    indexed = {e["slug"] for e in json.loads((unit / "skills_index.json").read_text())}
    on_disk = {d.name for d in (unit / "leaves").iterdir() if d.is_dir()}
    missing = on_disk - indexed
    assert not missing, f"{unit.name}: {len(missing)} leaves unreachable by search"


def _frontmatter(path: pathlib.Path) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    return match.group(1) if match else ""


def _advertised_skill_md() -> list[pathlib.Path]:
    return sorted((V2 / layout.ADVERTISED_DIRNAME).glob("*/SKILL.md"))


def test_collection_is_router_shaped():
    assert layout.is_router_shaped(V2)
    assert layout.leaf_dir(V2) == V2 / "leaves"


def test_corpus_lives_in_leaves_not_skills():
    leaves = list((V2 / "leaves").glob("*/SKILL.md"))
    assert len(leaves) > 1000, "the leaf corpus should hold the bulk of the skills"
    assert len(_advertised_skill_md()) <= 5, (
        "only entry points may sit under skills/ — everything a host advertises "
        "is charged to the user's context at session start"
    )


def test_router_is_advertised():
    slugs = {p.parent.name for p in _advertised_skill_md()}
    assert "_router" in slugs


def test_advertised_frontmatter_fits_the_budget():
    total = sum(len(_frontmatter(p)) for p in _advertised_skill_md())
    assert total // 4 < ADVERTISED_TOKEN_BUDGET, (
        f"advertised frontmatter is ~{total // 4} tokens, over the "
        f"{ADVERTISED_TOKEN_BUDGET} budget"
    )


def test_validation_still_covers_every_skill():
    """Moving leaves must not drop them from gate/index coverage."""
    found = layout.slugs(V2)
    indexed = {e["slug"] for e in json.loads((V2 / "skills_index.json").read_text())}
    assert indexed <= found, f"indexed but unreachable: {sorted(indexed - found)[:5]}"
    assert len(found) >= len(indexed)


def test_resolver_handles_legacy_layout(tmp_path):
    """Collections that still keep everything in skills/ are unaffected."""
    legacy = tmp_path / "legacy"
    (legacy / "skills" / "alpha").mkdir(parents=True)
    (legacy / "skills" / "alpha" / "SKILL.md").write_text("---\nname: alpha\n---\n")
    assert not layout.is_router_shaped(legacy)
    assert layout.leaf_dir(legacy) == legacy / "skills"
    assert layout.slugs(legacy) == {"alpha"}


@pytest.mark.parametrize(
    "args, expect_slug",
    [
        (["--tool", "SIRIUS", "-k", "1"], None),
        (["--query", "align retention time across samples", "-k", "1"], None),
        (["--technique", "LC-MS", "-k", "1"], None),
    ],
)
def test_search_script_returns_a_readable_path(args, expect_slug):
    """Retrieval must work offline and point at a file that exists."""
    out = subprocess.run(
        [sys.executable, str(V2 / "bin" / "search_skills.py"), *args],
        capture_output=True, text=True, cwd=V2, check=True,
    ).stdout
    read_lines = [ln for ln in out.splitlines() if ln.strip().startswith("read:")]
    assert read_lines, out
    target = V2 / read_lines[0].split("read:")[1].strip()
    assert target.is_file(), f"search pointed at a missing file: {target}"


def test_search_script_selftest_passes():
    subprocess.run(
        [sys.executable, str(V2 / "bin" / "search_skills.py"), "--selftest"],
        check=True, capture_output=True,
    )
