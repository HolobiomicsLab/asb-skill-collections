"""The evidence trim receipt identifies spans without republishing them.

A span the collector removes or shortens is removed because its paper's licence
does not allow the text to be republished. The trim receipt ships in the public
skills repositories next to the collection, so a receipt that quoted the
removed text (as ``text``, ``kept_text`` and ``dropped_text`` once did)
republished every quote the gate had just withheld. Each row now carries the
span's location, its lengths and the SHA-256 of its UTF-8 text, and nothing
else of the span.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

import yaml

from scripts import collect_from_cut as collector
from scripts import release_gate, skill_index


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs"
CREATORS = REPO / "scripts" / "release_creators.yaml"
TEXT_KEYS = {"text", "kept_text", "dropped_text", "quote"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
PREFIX = 40


def _strict_fixture(tmp_path: Path) -> Path:
    """Copy the cut fixture with every paper in the strict, capped regime."""
    fixture = tmp_path / "fixture"
    shutil.copytree(FIXTURE, fixture)
    corpus_path = fixture / "corpus.yaml"
    corpus = yaml.safe_load(corpus_path.read_text(encoding="utf-8"))
    for paper in corpus["papers"]:
        paper["access"] = {"type": "closed", "source_reuse": "none"}
    corpus_path.write_text(
        yaml.safe_dump(corpus, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    return fixture


def _collect(fixture: Path, tmp_path: Path) -> dict:
    receipts = tmp_path / "receipts"
    code = collector.main(
        [
            "--cut",
            str(fixture / "corpus"),
            "--domain",
            "metabarcoding",
            "--version",
            "v1",
            "--out",
            str(tmp_path / "candidate"),
            "--license",
            "CC-BY-4.0",
            "--plugin-repo",
            "https://github.com/HolobiomicsLab/asb-skills-metabarcoding",
            "--creators",
            str(CREATORS),
            "--corpus",
            str(fixture / "corpus.yaml"),
            "--receipts",
            str(receipts),
        ]
    )
    assert code == 0
    return json.loads((receipts / "evidence_trim_receipt.json").read_text("utf-8"))


def _source_spans(fixture: Path) -> list[str]:
    """Every evidence span the cut offers, leaves and tool records alike."""
    spans: list[str] = []
    for path in sorted((fixture / "corpus" / "skills").glob("*/skill.md")):
        frontmatter, body = skill_index.split_frontmatter(path.read_text("utf-8"))
        spans.extend(
            span["text"]
            for span in release_gate._collect_evidence_spans(frontmatter or {}, body)
        )
    for index in sorted((fixture / "builds").glob("*/tools/_index.json")):
        for record in json.loads(index.read_text("utf-8")).get("records", []):
            for span in record.get("evidence_spans") or []:
                text = span.get("text") or span.get("quote") if isinstance(span, dict) else span
                spans.append(str(text or ""))
    return [span.strip() for span in spans if len(span.strip()) >= PREFIX]


def test_trim_receipt_rows_carry_location_lengths_and_digest_only(tmp_path: Path) -> None:
    fixture = _strict_fixture(tmp_path)
    receipt = _collect(fixture, tmp_path)

    assert receipt["status"] == "applied"
    assert receipt["dropped"], "the strict fixture must remove or shorten spans"
    assert any(row["reason"] == "cumulative_budget_exhausted" for row in receipt["dropped"])
    for row in receipt["kept"] + receipt["dropped"]:
        assert not TEXT_KEYS & set(row), row
        assert row["doi"]
        assert SHA256.fullmatch(row["sha256"])
        assert isinstance(row["characters"], int) and row["characters"] > 0
        if row["kind"] == "leaf":
            assert row["leaf"]
        if row["source"] == "body":
            assert isinstance(row["body_line"], int)
    for row in receipt["dropped"]:
        assert row["kept_characters"] + row["dropped_characters"] == row["characters"]
        assert row["dropped_characters"] > 0


def test_trim_receipt_holds_no_span_text_dropped_or_kept(tmp_path: Path) -> None:
    fixture = _strict_fixture(tmp_path)
    receipt = _collect(fixture, tmp_path)
    serialized = json.dumps(receipt, ensure_ascii=False)
    spans = _source_spans(fixture)

    assert spans
    leaked = [span[:PREFIX] for span in spans if span[:PREFIX] in serialized]
    assert leaked == []


def test_dropped_digest_identifies_the_source_span(tmp_path: Path) -> None:
    """A reviewer holding the paper can still match a row to the text it removed."""
    fixture = _strict_fixture(tmp_path)
    receipt = _collect(fixture, tmp_path)
    digests = {
        hashlib.sha256(span.encode("utf-8")).hexdigest(): len(span)
        for span in _source_spans(fixture)
    }

    matched = [row for row in receipt["dropped"] if row["sha256"] in digests]
    assert matched
    assert all(digests[row["sha256"]] == row["characters"] for row in matched)
