"""Offline EDAM vocabulary generation and resolution."""

import json
from pathlib import Path

from scripts.edam_vocabulary import EDAM_IRI, load, refresh, resolve


FIXTURE = Path(__file__).parent / "fixtures" / "edam_remap" / "EDAM.csv"


def test_refresh_and_load_all_class_statuses(tmp_path):
    output = tmp_path / "vocabulary.json"
    table = refresh(FIXTURE, output, "2026-11-09")
    assert table["release"] == "1.25"
    assert table["release_inferred"] is True
    assert table["release_inference"] == "maximum numeric Created in value"
    assert table["source_file"] == "EDAM.csv"
    assert len(table["source_sha256"]) == 64
    assert table["generated_at"] == "2026-11-09"
    assert table["license"] == "CC-BY-SA-4.0"
    assert len(table["terms"]) == 12
    assert load(output) == table
    assert {term["branch"] for term in table["terms"].values()} == {"topic", "operation", "data"}
    assert json.loads(output.read_text())["terms"]["topic_0001"]["replaced_by"] == "topic_0002"


def test_resolver_statuses_and_labels():
    vocabulary = load(FIXTURE.with_name("edam_vocabulary.json"))
    cases = {
        "valid": (f"{EDAM_IRI}topic_0002", "Live topic", None),
        "obsolete": (f"{EDAM_IRI}topic_0001", "Old topic", "topic_0002"),
        "wrong_branch": (f"{EDAM_IRI}topic_0100", None, None),
        "ghost": (f"{EDAM_IRI}topic_9999", None, None),
        "malformed": ("https://edamontology.org/topic_0002", None, None),
    }
    for status, (iri, label, replacement) in cases.items():
        result = resolve(iri, vocabulary)
        assert result.status == status
        assert result.label == label
        assert result.replaced_by == replacement
    assert resolve(f"{EDAM_IRI}operation_0003", vocabulary).replaced_by is None
    assert resolve(f"{EDAM_IRI}topic_0003", vocabulary).replaced_by is None
    assert resolve(None, vocabulary).status == "malformed"
    assert resolve(f"{EDAM_IRI}topic_1", vocabulary).status == "ghost"
    assert resolve(f"{EDAM_IRI}unknown_0001", vocabulary).status == "malformed"
