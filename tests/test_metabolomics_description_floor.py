"""The metabolomics collector no longer writes "Use when when" or tool spans.

31 % of the released metabolomics v2 leaf descriptions read "Use when when
...": a "When to use" section that opens "When you have ..." was given a second
"Use when" prefix. The collector also filled every leaf's frontmatter
evidence_spans with the first spans of each tool the leaf names, so one tool
sentence grounded dozens of unrelated leaves (561 spans were each shared by
more than ten leaves). The collector now drops a leading "when", "use when" or
"if/when" before adding "Use when", copies no tool span into a leaf, and the
v2 leaves were re-derived with it.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts import collect_metabolomics_collection as collector
from scripts import lint_skill_descriptions as lint
from scripts import release_gate

REPO = Path(__file__).resolve().parent.parent
V2 = REPO / "collections" / "metabolomics" / "v2"


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("When you have a raw LC-MS file and need to pick peaks in it.",
         "Use when you have a raw LC-MS file and need to pick peaks in it."),
        ("when, after alignment, the feature table needs gap filling.",
         "Use when after alignment, the feature table needs gap filling."),
        ("Use when when you have spectra that need library matching.",
         "Use when you have spectra that need library matching."),
        ("Use when use when the workflow requires background thresholding.",
         "Use when the workflow requires background thresholding."),
        ("If/when the baseline drifts, you need to correct it before picking.",
         "Use when the baseline drifts, you need to correct it before picking."),
    ],
)
def test_a_when_opening_is_not_doubled(source: str, expected: str) -> None:
    description = collector._build_description("peak-picking", source, "", "metabolomics")

    assert description == expected
    assert not release_gate._DOUBLED_USE_WHEN_RE.match(description)
    assert lint.check_description(description) == []


def test_a_when_opening_in_the_fallback_is_not_doubled() -> None:
    description = collector._build_description(
        "peak-picking", "", "When you have a raw file, pick its peaks with the tool.", "metabolomics"
    )

    assert description == "Use when you have a raw file, pick its peaks with the tool."


@pytest.mark.parametrize(
    ("when_to_use", "fallback", "expected"),
    [
        ("you have spectra that need library matching.", "",
         "Use when you have spectra that need library matching."),
        ("Use when you need to align retention times across runs.", "",
         "Use when you need to align retention times across runs."),
        ("Whenever a run finishes, its features need to be exported.", "",
         "Use when whenever a run finishes, its features need to be exported."),
        ("", "Aligns retention times across runs of one study.",
         "Use when you need to aligns retention times across runs of one study."),
    ],
)
def test_other_openings_are_unchanged(when_to_use: str, fallback: str, expected: str) -> None:
    assert collector._build_description("x", when_to_use, fallback, "metabolomics") == expected


def _build(tmp_path: Path) -> Path:
    skill = tmp_path / "coll_alpha" / "skills" / "peak-picking"
    skill.mkdir(parents=True)
    (skill / "skill.md").write_text(
        "---\nname: peak-picking\ndescription: Picks peaks.\n---\n\n# Peak picking\n\n"
        "## When to use\n\nWhen you have a raw LC-MS file and need its peaks.\n\n"
        "## Procedure\n\nRun the picker.\n",
        encoding="utf-8",
    )
    (skill / "tools.json").write_text(
        json.dumps({"tools": [{"name": "XCMS", "evidence_spans": ["import xcms", "xcms::findPeaks"]}]}),
        encoding="utf-8",
    )
    return skill


def test_a_leaf_carries_no_span_copied_from_its_tools(tmp_path: Path) -> None:
    record = collector.extract_skill(_build(tmp_path), "coll_alpha", "10.1/a", "Alpha", "")
    record["_all_sources"] = [record]

    text = collector.render_skill_md(record, domain_label="metabolomics")
    frontmatter = yaml.safe_load(text.split("---\n", 2)[1])

    assert "evidence_spans" not in frontmatter
    assert "import xcms" not in text
    assert frontmatter["metadata"]["tools"] == ["XCMS"]
    assert frontmatter["description"] == "Use when you have a raw LC-MS file and need its peaks."


def test_the_v2_leaves_meet_the_text_floor() -> None:
    result = release_gate.check_leaf_text_floor(V2)

    assert result.status != release_gate.FAIL, result.details
    assert result.coverage["leaves"] >= len(list((V2 / "leaves").glob("*/SKILL.md")))


def test_the_v2_index_carries_the_leaf_descriptions() -> None:
    rows = {row["slug"]: row for row in json.loads((V2 / "skills_index.json").read_text("utf-8"))}
    for path in sorted((V2 / "leaves").glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = yaml.safe_load(text[4:text.index("\n---\n", 4) + 1])
        assert rows[path.parent.name]["description"] == frontmatter["description"], path
