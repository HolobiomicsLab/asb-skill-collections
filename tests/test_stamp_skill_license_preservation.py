"""Licence stamping must not consume prose or damage YAML syntax."""

import pytest
import yaml

from scripts.stamp_skill_license import BANNER_MARKER, license_banner, stamp_skill


def _leaf(tmp_path, frontmatter, body="# Method\n\nUse it.\n"):
    path = tmp_path / "SKILL.md"
    path.write_text("---\n" + frontmatter + "---\n" + body)
    return path


@pytest.mark.parametrize("prefix", ["", "> "])
def test_marker_mentioned_in_prose_is_preserved(tmp_path, prefix):
    prose = prefix + "Keep this literal " + BANNER_MARKER + " example.\n"
    path = _leaf(tmp_path, "name: example\n", "# Method\n\n" + prose)
    stamp_skill(path, "restricted")
    first = path.read_bytes()
    assert prose in path.read_text()
    assert path.read_text().count(license_banner("restricted")) == 1
    assert not stamp_skill(path, "restricted")
    assert path.read_bytes() == first


@pytest.mark.parametrize(
    "frontmatter, expected",
    [
        (
            "default_tier: &tier open\nmetadata:\n  license_tier: *tier\n  tools: []\n",
            "default_tier: &tier open\nmetadata:\n  license_tier: restricted\n  tools: []\n",
        ),
        (
            "base: &meta\n  tools: []\nmetadata: *meta\n",
            "base: &meta\n  tools: []\nmetadata: {<<: *meta, license_tier: restricted}\n",
        ),
        (
            "name: x\nmetadata:\n  ? tools\n  : [Example]\n",
            "name: x\nmetadata:\n  license_tier: restricted\n  ? tools\n  : [Example]\n",
        ),
    ],
)
def test_yaml_value_is_changed_at_its_own_syntax_span(tmp_path, frontmatter, expected):
    path = _leaf(tmp_path, frontmatter)
    stamp_skill(path, "restricted")
    after = path.read_text().split("---\n", 2)[1]
    assert after == expected
    assert yaml.safe_load(after)["metadata"]["license_tier"] == "restricted"
    first = path.read_bytes()
    assert not stamp_skill(path, "restricted")
    assert path.read_bytes() == first


@pytest.mark.parametrize(
    "frontmatter",
    [
        "metadata:\n  license_tier: &tier open\n  sibling: *tier\n",
        "metadata: &meta\n  tools: []\nsibling: *meta\n",
    ],
)
def test_shared_anchor_requiring_unrelated_edits_fails_without_writing(
    tmp_path, frontmatter
):
    path = _leaf(tmp_path, frontmatter)
    before = path.read_bytes()
    with pytest.raises(ValueError, match="shared YAML anchor"):
        stamp_skill(path, "restricted")
    assert path.read_bytes() == before


def test_missing_metadata_in_a_flow_mapping_preserves_other_fields(tmp_path):
    path = _leaf(tmp_path, "{name: 'keep quotes', tools: []}\n")
    stamp_skill(path, "open")
    after = path.read_text().split("---\n", 2)[1]
    assert after == "{metadata: {license_tier: open}, name: 'keep quotes', tools: []}\n"
    assert yaml.safe_load(after)["metadata"]["license_tier"] == "open"


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
@pytest.mark.parametrize("gap", ["", "\n"])
def test_only_signal_lines_are_added_without_normalizing_line_endings(
    tmp_path, newline, gap
):
    original = (
        (
            "---\nname: example\nmetadata:\n  tools: []\n---\n# Method\n"
            + gap
            + "Keep spaces.  \n"
        )
        .replace("\n", newline)
        .encode()
    )
    path = tmp_path / "SKILL.md"
    path.write_bytes(original)
    stamp_skill(path, "restricted")
    first = path.read_bytes()
    stripped = b"".join(
        line
        for line in first.splitlines(keepends=True)
        if not line.startswith(b"  license_tier:")
        and BANNER_MARKER.encode() not in line
    )
    assert stripped == original
    assert not stamp_skill(path, "restricted")
    assert path.read_bytes() == first
