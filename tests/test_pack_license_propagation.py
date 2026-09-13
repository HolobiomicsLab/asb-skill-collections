"""Pack builds preserve the licence signal declared by each source leaf."""

import json
from pathlib import Path

import pytest
import yaml

from scripts.build_grounding_bundle import build_unit
from scripts.stamp_skill_license import BANNER_MARKER, license_banner, stamp_skill

LEAF = """---
name: sample-method
description: 'Keep this deliberately long description on its original line, including its chosen quotes, because packaging must preserve all content unrelated to the licence signal.'
metadata:  # retain this comment
  tools: [ExampleTool]
  tool_license:
    ref: 'unchanged'
derived_from: []
---

# Sample method

Keep this paragraph, its trailing spaces, and its final newline.  
"""


def _write_leaf(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _without_signal(text: str) -> str:
    return "".join(
        line
        for line in text.splitlines(keepends=True)
        if not line.startswith("  license_tier:") and BANNER_MARKER not in line
    )


@pytest.fixture
def build_paths(tmp_path):
    collection, pack = tmp_path / "collection", tmp_path / "pack"
    collection.mkdir()
    plugin = pack / ".claude-plugin" / "plugin.json"
    plugin.parent.mkdir(parents=True)
    plugin.write_text(json.dumps({"name": "example", "description": "Example."}))
    (collection / "kb_bundle.json").write_text(
        json.dumps({"skills": {"sample-method": {"license_tier": "restricted"}}})
    )
    binder = tmp_path / "binder.py"
    binder.write_text("# Binder fixture\n")
    return pack, collection, binder


@pytest.mark.parametrize("domain", ["astronomy", "climate", "genomics", "proteomics"])
@pytest.mark.parametrize("tier", ["open", "noncommercial", "restricted", "unknown"])
@pytest.mark.parametrize("corpus_dir", ["skills", "leaves"])
def test_build_carries_source_tier_and_only_its_signal(
    build_paths, domain, tier, corpus_dir
):
    pack, collection, binder = build_paths
    original = LEAF.replace("Sample method", domain)
    copied = _write_leaf(pack / corpus_dir / "sample-method" / "SKILL.md", original)
    source = _write_leaf(
        collection / corpus_dir / "sample-method" / "SKILL.md",
        LEAF.replace("  tools:", f"  license_tier: {tier}\n  tools:"),
    )
    source_before = source.read_bytes()

    written = build_unit(pack, collection, binder)

    text = copied.read_text()
    frontmatter = yaml.safe_load(text.split("---\n", 2)[1])
    assert frontmatter["metadata"]["license_tier"] == tier
    expected_banner = license_banner(tier)
    assert text.count(BANNER_MARKER) == int(expected_banner is not None)
    if expected_banner:
        assert expected_banner in text
        assert text.index("# " + domain) < text.index(expected_banner)
    assert _without_signal(text) == original
    assert source.read_bytes() == source_before
    assert str(copied.relative_to(pack)) in written

    first = {
        str(p.relative_to(pack)): p.read_bytes() for p in pack.rglob("*") if p.is_file()
    }
    assert str(copied.relative_to(pack)) not in build_unit(pack, collection, binder)
    assert {
        str(p.relative_to(pack)): p.read_bytes() for p in pack.rglob("*") if p.is_file()
    } == first


@pytest.mark.parametrize("source_exists", [False, True])
def test_build_does_not_invent_a_tier_from_the_bundle(build_paths, source_exists):
    pack, collection, binder = build_paths
    copied = _write_leaf(pack / "leaves" / "sample-method" / "SKILL.md", LEAF)
    if source_exists:
        _write_leaf(collection / "leaves" / "sample-method" / "SKILL.md", LEAF)
    build_unit(pack, collection, binder)
    assert copied.read_text() == LEAF


def test_build_replaces_an_existing_banner_without_changing_prose(build_paths):
    pack, collection, binder = build_paths
    prior = LEAF.replace(
        "# Sample method\n\n",
        "# Sample method\n\n" + license_banner("restricted") + "\n",
    )
    copied = _write_leaf(pack / "leaves" / "sample-method" / "SKILL.md", prior)
    _write_leaf(
        collection / "skills" / "sample-method" / "SKILL.md",
        LEAF.replace("  tools:", "  license_tier: noncommercial\n  tools:"),
    )
    build_unit(pack, collection, binder)
    first = copied.read_bytes()
    assert license_banner("noncommercial") in copied.read_text()
    assert copied.read_text().count(BANNER_MARKER) == 1
    assert _without_signal(copied.read_text()) == LEAF
    build_unit(pack, collection, binder)
    assert copied.read_bytes() == first


@pytest.mark.parametrize(
    "metadata",
    [
        "metadata:  # retain comment\n  tools: [ExampleTool]\n",
        "metadata: {tools: [ExampleTool]}  # retain comment\n",
        "metadata: {}\n",
        "metadata:\n",
        "metadata: null  # retain comment\n",
        "",
    ],
)
def test_stamper_handles_metadata_shapes_without_reflow(tmp_path, metadata):
    text = (
        "---\nname: 'keep these quotes'\n" + metadata + "---\n# Method\n\nUse it.  \n"
    )
    leaf = _write_leaf(tmp_path / "SKILL.md", text)
    stamp_skill(leaf, "restricted")
    stamped = leaf.read_text()
    assert "name: 'keep these quotes'\n" in stamped
    assert "Use it.  \n" in stamped
    if "# retain comment" in metadata:
        assert "# retain comment" in stamped
    assert (
        yaml.safe_load(stamped.split("---\n", 2)[1])["metadata"]["license_tier"]
        == "restricted"
    )
    assert not stamp_skill(leaf, "restricted")
    assert leaf.read_text() == stamped


def test_stamper_updates_only_the_existing_tier_value(tmp_path):
    original = LEAF.replace(
        "  tools:", "  license_tier: open  # preserve this comment\n  tools:"
    )
    leaf = _write_leaf(tmp_path / "SKILL.md", original)
    stamp_skill(leaf, "restricted")
    expected = original.replace("license_tier: open", "license_tier: restricted")
    expected = expected.replace(
        "# Sample method\n\n",
        "# Sample method\n\n" + license_banner("restricted") + "\n",
    )
    assert leaf.read_text() == expected
