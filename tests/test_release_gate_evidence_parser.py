"""Regression tests for the release gate's body evidence parser."""

import json
import re
import shutil
from pathlib import Path

import pytest

from scripts import release_gate


REPO_ROOT = Path(__file__).parent.parent
MINI_COLLECTION = REPO_ROOT / "tests" / "fixtures" / "mini_collection"
SAMPLE_PATH = REPO_ROOT / "tests" / "fixtures" / "unrecognized_quote_samples.json"
SAMPLES = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))["samples"]
ORIGINAL_EVIDENCE_RE = re.compile(
    r'^(\s*-\s+\[[^\]]*\][^:]*?):\s*"[^"]*"\s*$'
)


def _texts(body):
    return [span["text"] for span in release_gate._collect_evidence_spans({}, body)]


def _old_parser_spans(body):
    spans = []
    for line in body.splitlines():
        if not ORIGINAL_EVIDENCE_RE.match(line):
            continue
        quote = re.search(r':\s*"([^"]*)"\s*$', line)
        if quote and quote.group(1).strip():
            spans.append({"text": quote.group(1).strip(), "doi": "", "section": ""})
    return spans


def _span_bytes(spans):
    return json.dumps(
        spans, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")


def _write_parser_collection(root, body):
    leaf = root / "leaves" / "parser-fixture" / "SKILL.md"
    leaf.parent.mkdir(parents=True)
    leaf.write_text(
        "---\n"
        "name: parser-fixture\n"
        "license: CC-BY-4.0\n"
        "derived_from:\n"
        "  - doi: 10.0000/parser-fixture\n"
        "---\n"
        + body,
        encoding="utf-8",
    )


def test_colons_are_allowed_in_evidence_labels():
    body = '- [methods] phase: normalization: "Quoted: result."'

    assert _texts(body) == ["Quoted: result."]


def test_one_line_span_uses_the_last_quote_as_its_closer():
    body = '- [methods] command example: "call("input.txt", mode="fast")"   '

    assert _texts(body) == ['call("input.txt", mode="fast")']


def test_multiline_span_closes_at_first_following_line_ending_in_quote():
    body = (
        '- [methods] command example: "first line\n'
        'second "inner" line\n'
        'third line"   \n'
        '- [results] later item: "kept separately"'
    )

    spans, stats = release_gate._collect_evidence_spans_with_stats({}, body)

    assert [span["text"] for span in spans] == [
        'first line\nsecond "inner" line\nthird line',
        "kept separately",
    ]
    assert stats == {
        "one_line": 1,
        "multiline": 1,
        "embedded_quote": 1,
        "unterminated": 0,
    }


def test_new_item_and_eof_abandon_unterminated_spans():
    body = (
        '- [methods] abandoned by item: "first line\n'
        "continuation\n"
        '- [readme] complete: "recognized"\n'
        '- [results] abandoned by eof: "last line\n'
        "continuation"
    )

    spans, stats = release_gate._collect_evidence_spans_with_stats({}, body)

    assert [span["text"] for span in spans] == ["recognized"]
    assert stats == {
        "one_line": 1,
        "multiline": 0,
        "embedded_quote": 0,
        "unterminated": 2,
    }


@pytest.mark.parametrize(
    "sample",
    SAMPLES,
    ids=[f"{index:02d}-{sample['sample_kind']}" for index, sample in enumerate(SAMPLES, 1)],
)
def test_all_supplied_unrecognized_blocks_are_parsed(sample):
    assert len(SAMPLES) == 12

    spans, stats = release_gate._collect_evidence_spans_with_stats(
        {}, sample["raw_block"]
    )

    assert [span["text"] for span in spans] == [sample["text"]]
    assert stats["multiline"] == ("multiline" in sample["sample_kind"])
    assert stats["one_line"] == ("multiline" not in sample["sample_kind"])
    assert stats["embedded_quote"] == (
        "embedded-quote" in sample["sample_kind"]
    )
    assert stats["unterminated"] == 0


def test_classic_mini_collection_spans_are_byte_identical_to_old_parser(tmp_path):
    copied_fixture = tmp_path / "mini_collection"
    shutil.copytree(MINI_COLLECTION, copied_fixture)
    classic_body = (
        '## Evidence\n'
        '- [methods] classic prose: "First classic span."\n'
        '  - [readme] indented classic prose: "Second classic span."   \n'
    )
    _write_parser_collection(copied_fixture, classic_body)
    body = (copied_fixture / "leaves/parser-fixture/SKILL.md").read_text(
        encoding="utf-8"
    ).split("---\n", 2)[2]

    expected = _old_parser_spans(body)
    actual = release_gate._collect_evidence_spans({}, body)

    assert len(expected) == 2
    assert _span_bytes(actual) == _span_bytes(expected)


def test_gate_checks_report_body_parser_statistics(tmp_path):
    body = (
        '- [methods] classic: "one line"\n'
        '- [readme] multiline: "first\nsecond "inner" line"\n'
        '- [results] incomplete: "never closes\n'
    )
    _write_parser_collection(tmp_path, body)
    expected = {
        "parser_one_line": 1,
        "parser_multiline": 1,
        "parser_embedded_quote": 1,
        "parser_unterminated": 1,
    }

    checks = (
        release_gate.check_strip_verbatim(
            tmp_path, {"10.0000/parser-fixture": "gold-oa"}
        ),
        release_gate.check_pii_dual_use(tmp_path, {}),
    )

    for check in checks:
        assert {key: check.coverage[key] for key in expected} == expected


def test_report_data_and_text_identify_the_gate_owned_parser(tmp_path, capsys):
    report = release_gate.run_gate(tmp_path, None, False)

    assert "gate-owned" in release_gate._EVIDENCE_PARSER_SOURCE
    assert report["evidence_parser_source"] == release_gate._EVIDENCE_PARSER_SOURCE
    assert (
        report["policy"]["evidence_parser_source"]
        == release_gate._EVIDENCE_PARSER_SOURCE
    )

    release_gate._print_human_summary(report)
    assert release_gate._EVIDENCE_PARSER_SOURCE in capsys.readouterr().out
