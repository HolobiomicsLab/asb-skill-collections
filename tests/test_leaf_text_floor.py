"""The release gate fails two generator faults that once reached a release.

31 % of the metabolomics v2 leaf descriptions read "Use when when ...", and
leaf frontmatter evidence_spans were copied from tool mentions, so one sentence
grounded dozens of unrelated leaves. Both lints accepted these. The gate now
fails a description starting "Use when when" and a frontmatter evidence span
shared by more than ten leaves, and reports the share of leaves that carry no
span.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from scripts import release_gate


def _leaf(
    root: Path, slug: str, description: str, spans: list[str], body: str = "# Body\n"
) -> None:
    path = root / "leaves" / slug / "SKILL.md"
    path.parent.mkdir(parents=True)
    frontmatter = {
        "name": slug,
        "description": description,
        "license": "CC-BY-4.0",
        "derived_from": [{"doi": "10.1/x"}],
        "evidence_spans": [{"doi": "10.1/x", "text": text} for text in spans],
    }
    path.write_text(
        "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n\n" + body,
        encoding="utf-8",
    )


def _failures(result: release_gate.CheckResult) -> list[dict]:
    return [d for d in result.details if d["status"] == release_gate.FAIL]


def test_doubled_use_when_fails(tmp_path: Path) -> None:
    _leaf(tmp_path, "a", "Use when when you have raw LC-MS data.", ["Span a."])
    _leaf(tmp_path, "b", "use When  WHEN a table is ready.", ["Span b."])
    _leaf(tmp_path, "c", "Use when you have raw LC-MS data.", ["Span c."])
    _leaf(tmp_path, "d", "Use when whenever a run finishes.", ["Span d."])

    result = release_gate.check_leaf_text_floor(tmp_path)

    assert result.status == release_gate.FAIL
    [finding] = _failures(result)
    assert finding["count"] == 2
    assert finding["examples"] == ["leaves/a", "leaves/b"]
    assert result.counts["checked"] == 4
    assert result.counts["failed"] == 2


def test_a_span_shared_by_more_than_ten_leaves_fails(tmp_path: Path) -> None:
    shared = "import numpy as np"
    for index in range(11):
        _leaf(tmp_path, f"leaf-{index:02d}", "Use when a task fits.", [shared])

    result = release_gate.check_leaf_text_floor(tmp_path)

    [finding] = _failures(result)
    assert finding["count"] == 1
    [example] = finding["examples"]
    assert example["leaves"] == 11
    assert example["characters"] == len(shared)
    assert shared not in str(result.to_dict())
    assert result.counts["failed"] == 11


def test_a_span_shared_by_ten_leaves_passes(tmp_path: Path) -> None:
    for index in range(10):
        _leaf(tmp_path, f"leaf-{index:02d}", "Use when a task fits.", ["Shared   span."])

    result = release_gate.check_leaf_text_floor(tmp_path)

    assert result.status == release_gate.PASS
    assert result.counts["failed"] == 0


def test_whitespace_variants_count_as_one_span(tmp_path: Path) -> None:
    for index in range(11):
        text = "Shared span." if index % 2 else "Shared \n span."
        _leaf(tmp_path, f"leaf-{index:02d}", "Use when a task fits.", [text])

    assert release_gate.check_leaf_text_floor(tmp_path).status == release_gate.FAIL


BODY_EVIDENCE = (
    "# Body\n\n## Evidence\n\n"
    '- [methods] a claim: "A quote from the paper this leaf was built from."\n'
)


def test_share_of_leaves_without_spans_is_reported_not_failed(tmp_path: Path) -> None:
    _leaf(tmp_path, "a", "Use when a task fits.", ["Span a."])
    _leaf(tmp_path, "b", "Use when a task fits.", [], body=BODY_EVIDENCE)
    _leaf(tmp_path, "c", "Use when a task fits.", [])
    _leaf(tmp_path, "d", "Use when a task fits.", ["Span d."])

    result = release_gate.check_leaf_text_floor(tmp_path)

    assert result.status == release_gate.PASS
    assert result.coverage == {
        "leaves": 4,
        "leaves_without_evidence_spans": 2,
        "leaves_without_any_evidence": 1,
    }
    assert "2 of 4 leaves, 50.0 %, carry no frontmatter evidence span" in result.summary
    assert "1, 25.0 %, carry no evidence of either kind" in result.summary


def test_body_quotes_shared_by_leaves_of_one_paper_are_not_counted(
    tmp_path: Path,
) -> None:
    """Class-A leaves quote their own paper in the body; several leaves may share one."""
    for index in range(12):
        _leaf(tmp_path, f"leaf-{index:02d}", "Use when a task fits.", [], body=BODY_EVIDENCE)

    result = release_gate.check_leaf_text_floor(tmp_path)

    assert result.status == release_gate.PASS
    assert result.coverage["leaves_without_any_evidence"] == 0


def test_strict_gate_blocks_the_floor(tmp_path: Path) -> None:
    _leaf(tmp_path, "a", "Use when when you have raw data.", ["Span a."])
    (tmp_path / "corpus.yaml").write_text(
        yaml.safe_dump(
            {"papers": [{"doi": "10.1/x", "status": "included", "access": {"type": "gold-oa"}}]}
        ),
        encoding="utf-8",
    )

    report = release_gate.run_gate(tmp_path, None, True)
    checks = {check["name"]: check for check in report["checks"]}

    assert checks["leaf_text_floor"]["status"] == release_gate.FAIL
    assert report["release_verified"] is False
