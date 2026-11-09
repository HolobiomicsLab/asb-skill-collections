"""Deterministic EDAM remap tiers, byte preservation, and receipts."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from asb_skill_collections.layout import leaf_dir
from scripts.edam_vocabulary import EDAM_IRI
from scripts.remap_edam import plan_remap


REPO = Path(__file__).resolve().parents[1]
FIXTURE = REPO / "tests" / "fixtures" / "edam_remap"
VOCABULARY = FIXTURE / "edam_vocabulary.json"
REAL = Path(os.environ.get("ASB_METABOLOMICS_CHECKOUT", "")) / "collections" / "metabolomics" / "v3"
REAL_VOCABULARY = REPO / "scripts" / "data" / "edam_vocabulary.json"


def make_collection(tmp_path):
    collection = tmp_path / "collection"
    rows = []
    definitions = [
        ("obsolete-replaced", ["topic_0001"], "operation_0001", [], "Metabolite workflow"),
        ("obsolete-cross", ["topic_0003"], "operation_0003", [], "Metabolite workflow"),
        ("wrong-branch", ["topic_0100"], "operation_0100", [], "Metabolite workflow"),
        ("ghost", ["topic_9999"], "operation_9999", [], "Metabolite workflow"),
        ("malformed", ["topic_bad"], "operation_bad", [], "Metabolite workflow"),
        ("generic-topic-drop", ["topic_0121", "topic_3172"], "operation_3646", ["Python"], "Metabolite quantification"),
        ("proteomics-tool", ["topic_0121"], "operation_0282", ["MaxQuant"], "Spectral analysis"),
        ("proteomics-text", ["topic_0121"], "operation_0002", ["Python"], "Peptide identification"),
        ("foreign-operation", ["topic_3520"], "operation_3218", ["Python"], "NMR workflow"),
        ("valid-unchanged", ["topic_3520", "topic_3172"], "operation_0002", ["Python"], "Mass spectrometry"),
    ]
    for slug, topics, operation, tools, description in definitions:
        topic_iris = [f"{EDAM_IRI}{topic}" for topic in topics]
        operation_iri = f"{EDAM_IRI}{operation}"
        metadata = {"edam_operation": operation_iri, "edam_topics": list(topic_iris)}
        frontmatter = {
            "name": slug,
            "description": description,
            "tools": tools,
            "edam_operation": operation_iri,
            "edam_topics": topic_iris,
            "metadata": metadata,
        }
        leaf = collection / "leaves" / slug / "SKILL.md"
        leaf.parent.mkdir(parents=True)
        text = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n\nBody for " + description + ".\n"
        leaf.write_text(text)
        rows.append({
            "slug": slug, "name": slug, "description": description, "tools": tools,
            "edam_operation": operation_iri, "edam_topics": topic_iris, "dois": [f"10.0000/{slug}"],
        })
    collection.mkdir(exist_ok=True)
    (collection / "skills_index.json").write_text(json.dumps(rows, indent=1) + "\n")
    (collection / "collection.yaml").write_text(
        "name: fixture\nedam_topics:\n" + "".join(f"- {iri}\n" for row in rows for iri in row["edam_topics"])
        + "other: preserved\n"
    )
    (collection / "tools_index.json").write_text(json.dumps([
        {"slug": "empty", "edam_topics": []},
        {"slug": "tool", "edam_topics": [f"{EDAM_IRI}topic_0001", f"{EDAM_IRI}topic_9999"], "other": "keep"},
    ], indent=1) + "\n")
    return collection


def run_cli(collection, receipt, tier="T2", *extra):
    return subprocess.run(
        [sys.executable, "scripts/remap_edam.py", "--collection", str(collection),
         "--vocabulary", str(VOCABULARY), "--tier", tier, "--receipt", str(receipt),
         "--date", "2026-11-09", *extra],
        cwd=REPO, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True, capture_output=True, check=True,
    )


def test_tiers_and_never_touch_topic_3520(tmp_path):
    collection = make_collection(tmp_path)
    expectations = {
        "T1": (3, {"R1_topic_removed": 3, "R1_operation_removed": 2}),
        "T2": (5, {"R2_topic_replaced": 1, "R2_topic_removed": 1,
                    "R2_operation_replaced": 1, "R2_operation_removed": 1}),
        "T3": (6, {"R3_topic_0121_removed": 1}),
        "T3b": (7, {"R5_operation_removed": 2}),
        "T4": (8, {"R5_operation_removed": 3}),
    }
    for tier, (touched, counters) in expectations.items():
        result = plan_remap(collection, VOCABULARY, tier)
        assert result["totals"]["leaves_touched"] == touched
        for rule, count in counters.items():
            assert result["rule_counts"][rule] == count
        assert result["rule_counts"]["R4_topic_3520_removed"] == 0
        if tier == "T3":
            assert result["rule_counts"]["R3_topic_0121_removed"] == 1
        if tier == "T1":
            assert result["totals"]["topic_fields_empty_after"] == 3
            assert result["totals"]["operation_fields_empty_after"] == 2


def test_body_proteomics_signal_and_valid_identifiers_survive(tmp_path):
    collection = make_collection(tmp_path)
    leaf = collection / "leaves" / "generic-topic-drop" / "SKILL.md"
    leaf.write_text(leaf.read_text().replace("Body for Metabolite quantification.", "Body identifies tryptic peptides."))
    result = plan_remap(collection, VOCABULARY, "T3")
    assert "R3_topic_0121_removed" not in result["rule_counts"]
    unchanged = next(row for row in result["rows"] if row["slug"] == "valid-unchanged")
    assert unchanged["edam_topics"] == [f"{EDAM_IRI}topic_3520", f"{EDAM_IRI}topic_3172"]
    assert unchanged["edam_operation"] == f"{EDAM_IRI}operation_0002"


def test_legacy_skills_layout_is_supported(tmp_path):
    collection = make_collection(tmp_path)
    shutil.move(str(collection / "leaves"), str(collection / "skills"))
    result = plan_remap(collection, VOCABULARY, "T2")
    assert result["totals"]["leaves_touched"] == 5
    assert leaf_dir(collection).name == "skills"


def test_write_revert_idempotence_byte_preservation_and_receipt(tmp_path):
    collection = make_collection(tmp_path)
    original = {path: path.read_bytes() for path in collection.rglob("*") if path.is_file()}
    receipt_path = tmp_path / "receipt.json"
    dry = run_cli(collection, receipt_path)
    assert '"leaves_touched": 5' in dry.stdout
    assert {path: path.read_bytes() for path in collection.rglob("*") if path.is_file()} == original
    dry_receipt = json.loads(receipt_path.read_text())
    assert dry_receipt["schema"] == "asb-edam-remap/1"
    assert dry_receipt["write"] is False
    assert dry_receipt["changes"]
    assert set(dry_receipt["input_sha256"]) == {"skills_index.json", "collection.yaml", "leaves"}
    assert all(set(change) == {"slug", "field", "before", "after", "rules"} for change in dry_receipt["changes"])
    assert dry_receipt["top_five"]["topics"]

    run_cli(collection, receipt_path, "T2", "--write")
    written = {path: path.read_bytes() for path in collection.rglob("*") if path.is_file()}
    rows = {row["slug"]: row for row in json.loads((collection / "skills_index.json").read_text())}
    assert rows["obsolete-replaced"]["edam_topics"] == [f"{EDAM_IRI}topic_0002"]
    assert rows["obsolete-cross"]["edam_topics"] == []
    assert rows["ghost"]["edam_operation"] is None
    assert json.loads((collection / "tools_index.json").read_text())[1]["edam_topics"] == [f"{EDAM_IRI}topic_0002"]
    manifest = yaml.safe_load((collection / "collection.yaml").read_text())
    assert f"{EDAM_IRI}topic_0002" in manifest["edam_topics"]
    assert (collection / "collection.yaml").read_text().endswith("other: preserved\n")
    run_cli(collection, receipt_path, "T2", "--write")
    assert {path: path.read_bytes() for path in collection.rglob("*") if path.is_file()} == written

    subprocess.run(
        [sys.executable, "scripts/remap_edam.py", "revert", "--receipt", str(receipt_path),
         "--collection", str(collection)], cwd=REPO,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, text=True, capture_output=True, check=True,
    )
    assert {path: path.read_bytes() for path in collection.rglob("*") if path.is_file()} == original


def test_revert_requires_write_receipt(tmp_path):
    collection = make_collection(tmp_path)
    receipt = tmp_path / "receipt.json"
    run_cli(collection, receipt)
    result = subprocess.run(
        [sys.executable, "scripts/remap_edam.py", "revert", "--receipt", str(receipt),
         "--collection", str(collection)], cwd=REPO, text=True, capture_output=True,
    )
    assert result.returncode != 0
    assert "write receipt" in result.stderr


@pytest.mark.skipif(not os.environ.get("ASB_METABOLOMICS_CHECKOUT"), reason="set ASB_METABOLOMICS_CHECKOUT")
def test_real_collection_audit_acceptance():
    t1 = plan_remap(REAL, REAL_VOCABULARY, "T1")
    t2 = plan_remap(REAL, REAL_VOCABULARY, "T2")
    assert t1["totals"]["leaves_touched"] == 693
    assert t2["totals"] == {
        "leaves": 11830, "leaves_touched": 921, "papers_touched": 360,
        "topic_fields_empty_before": 903, "topic_fields_empty_after": 1042,
        "operation_fields_empty_before": 2646, "operation_fields_empty_after": 3057,
    }
