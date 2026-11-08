"""Deterministic technique tagging, measured parity, and byte preservation."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from scripts.normalize_skill import parse_skill_md
from scripts.tag_techniques import (
    RULES_PATH,
    annotate,
    insert_json_field,
    load_rules,
    load_rows,
    match_row,
    replace_json_field,
    replace_yaml_list,
    strip_techniques,
)


REPO = Path(__file__).resolve().parents[1]
# A domain checkout and the investigation evidence are local, private inputs: the two
# tests that read them run only when these environment variables point at them.
COLLECTIONS = Path(os.environ.get("ASB_METABOLOMICS_CHECKOUT", "")) / "collections" / "metabolomics"
INVESTIGATION = Path(os.environ.get("ASB_INT045_EVIDENCE", ""))
PYTHON = Path(sys.executable)
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def run_cli(*arguments):
    return subprocess.run(
        [str(PYTHON), "scripts/tag_techniques.py", *map(str, arguments)],
        cwd=REPO,
        env=ENV,
        capture_output=True,
        text=True,
        check=True,
    )


def actual_techniques(leaf):
    frontmatter, _ = parse_skill_md(leaf.read_text())
    return frontmatter.get("metadata", {}).get("techniques", [])


@pytest.mark.parametrize(
    ("tag", "rule", "positive", "negative"),
    [
        ("LC-MS", "lc_ms", "Analyze UHPLC-MS/MS features.", "An LCMSMSx suffix is not a platform."),
        ("LC-MS", "liquid_chromatography", "Liquid chromatography separates compounds.", "Gas chromatography is separate."),
        ("LC-MS", "tandem_ms", "Interpret MS2 and MS/MS spectra.", "A mass spectrum alone is insufficient."),
        ("GC-MS", "gc_ms", "Process GCxGC-MS data.", "A GC-MSword suffix is not a platform."),
        ("GC-MS", "gas_chromatography", "Gas chromatographic separation is used.", "Liquid chromatography is separate."),
        ("CE-MS", "ce_ms", "Couple CESI-MS to the detector.", "A CEMSX suffix is not a platform."),
        ("CE-MS", "capillary_electrophoresis", "Capillary electrophoresis separates ions.", "Capillary columns alone are insufficient."),
        ("direct-infusion-MS", "di_ms_strict", "Acquire DIMS and FIA-MS spectra.", "DI-MS was excluded by the measured strict rule."),
        ("direct-infusion-MS", "flow_injection", "Use flow-injection analysis.", "A flowing stream alone is insufficient."),
        ("MS-imaging", "ms_imaging", "Analyze spatial metabolomics by MSI imaging.", "Molecular images alone are insufficient."),
        ("MS-imaging", "desi", "DESI spectra were acquired.", "The word design contains no platform name."),
        ("ion-mobility-MS", "ion_mobility", "Separate by ion-mobility.", "Mobile ions alone are insufficient."),
        ("ion-mobility-MS", "ims_ms", "Acquire TIMS-MS/MS spectra.", "A TIMSMSx suffix is not a platform."),
        ("NMR", "nmr", "Acquire NMR and nuclear magnetic resonance spectra.", "The NMRx suffix is not a platform."),
    ],
)
def test_golden_regexes(tag, rule, positive, negative):
    rules = load_rules(RULES_PATH)
    assert rule in annotate(positive, rules)[tag]
    assert rule not in annotate(negative, rules).get(tag, [])


def test_v2_held_out_metrics_match_investigation_exactly():
    collection = COLLECTIONS / "v2"
    evidence = INVESTIGATION / "techniques.json"
    if not collection.is_dir() or not evidence.is_file():
        pytest.skip("Released v2 collection or investigation measurements are unavailable")
    expected = json.loads(evidence.read_text())["held_out_metrics"]
    rows = load_rows(collection)
    rules = load_rules(RULES_PATH)
    for row in rows:
        row.matches = match_row(row, rules)
    for tag in rules.vocabulary:
        observed = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
        for row in rows:
            if int(hashlib.sha256(row.slug.encode()).hexdigest(), 16) % 2 == 0:
                continue
            predicted = tag in row.tags
            actual = tag in row.existing_tags
            key = "tp" if predicted and actual else "fp" if predicted else "fn" if actual else "tn"
            observed[key] += 1
        predicted = observed["tp"] + observed["fp"]
        actual = observed["tp"] + observed["fn"]
        observed["precision"] = round(observed["tp"] / predicted, 4) if predicted else None
        observed["recall"] = round(observed["tp"] / actual, 4) if actual else None
        assert observed == expected[tag]["test"]


def test_v3_dry_run_reproduces_projected_counts(tmp_path):
    collection = COLLECTIONS / "v3"
    if not collection.is_dir():
        pytest.skip("Released v3 collection is unavailable")
    report = tmp_path / "report.json"
    result = run_cli("--collection", collection, "--rules", RULES_PATH, "--report", report)
    counts = json.loads(result.stdout)["per_tag"]
    assert counts == {
        "LC-MS": 5716,
        "GC-MS": 469,
        "CE-MS": 65,
        "direct-infusion-MS": 33,
        "MS-imaging": 532,
        "ion-mobility-MS": 308,
        "NMR": 876,
    }
    receipt = json.loads(report.read_text())
    assert receipt["totals"] == {"tagged": 7163, "untagged": 4667, "leaves": 11830}
    assert receipt["leaves"][0]["matches"]
    assert not any(row.get("techniques") for row in json.loads((collection / "skills_index.json").read_text()))


def test_write_is_idempotent_and_changes_only_technique_fields(tmp_path):
    collection = tmp_path / "collection"
    shutil.copytree(REPO / "tests/fixtures/router_collection", collection)
    for leaf in collection.glob("leaves/*/SKILL.md"):
        text = leaf.read_text()
        metadata = {
            "tools": parse_skill_md(text)[0].get("tools", []),
            "techniques": parse_skill_md(text)[0].get("techniques", []),
        }
        frontmatter, body = parse_skill_md(text)
        frontmatter["metadata"] = metadata
        frontmatter["metadata"]["techniques"] = sorted(set(frontmatter["metadata"]["techniques"]))
        frontmatter.pop("tools", None)
        frontmatter.pop("techniques", None)
        text = "---\n" + yaml.safe_dump(frontmatter, sort_keys=False) + "---\n" + body
        leaf.write_text(text)
    index = collection / "skills_index.json"
    index_rows = json.loads(index.read_text())
    for row in index_rows:
        row.pop("techniques", None)
    index.write_text(json.dumps(index_rows, indent=1) + "\n")
    for row in index_rows:
        index.write_text(insert_json_field(index.read_text(), row["slug"], "techniques", []))
    baseline = {path: path.read_bytes() for path in collection.rglob("*") if path.is_file()}
    run_cli("--collection", collection, "--rules", RULES_PATH, "--write")
    once = {path: path.read_bytes() for path in collection.rglob("*") if path.is_file()}
    run_cli("--collection", collection, "--rules", RULES_PATH, "--write")
    assert once == {path: path.read_bytes() for path in collection.rglob("*") if path.is_file()}
    assert set(once) == set(baseline)
    index_by_slug = {row["slug"]: row for row in json.loads(index.read_text())}
    for path, after in once.items():
        before_text = baseline[path].decode()
        after_text = after.decode()
        if path.name == "SKILL.md" and path.parent.parent.name == "leaves":
            assert strip_techniques(before_text) == strip_techniques(after_text)
            tags = actual_techniques(path)
            assert tags == sorted(tags)
            assert set(index_by_slug[path.parent.name]["techniques"]).issubset(tags)
        elif path.name == "skills_index.json":
            before_rows = json.loads(before_text)
            after_rows = json.loads(after_text)
            for old, new in zip(before_rows, after_rows, strict=True):
                old = dict(old)
                old.pop("techniques")
                new_without_tags = dict(new)
                new_without_tags.pop("techniques")
                assert old == new_without_tags
        else:
            assert before_text == after_text
    assert once != baseline


def test_targeted_editors_preserve_inline_styles():
    leaf = "---\nmetadata: {license_tier: open, techniques: [NMR]}\n---\nbody\n"
    assert replace_yaml_list(leaf, ["LC-MS"], target="inline") == (
        "---\nmetadata: {license_tier: open, techniques: [LC-MS]}\n---\nbody\n"
    )
    index = '[{"slug":"a","techniques": ["NMR"],"name":"a"}]\n'
    assert replace_json_field(index, "a", "techniques", ["LC-MS"]) == (
        '[{"slug":"a","techniques": ["LC-MS"],"name":"a"}]\n'
    )


def test_only_subset_leaves_other_tags_unchanged(tmp_path):
    collection = tmp_path / "collection"
    shutil.copytree(REPO / "tests/fixtures/router_collection", collection)
    index = collection / "skills_index.json"
    before = index.read_bytes()
    result = run_cli(
        "--collection", collection, "--rules", RULES_PATH, "--only", "CE-MS,direct-infusion-MS"
    )
    counts = json.loads(result.stdout)["per_tag"]
    assert counts == {"CE-MS": 0, "direct-infusion-MS": 0}
    assert index.read_bytes() == before
    run_cli(
        "--collection", collection, "--rules", RULES_PATH,
        "--only", "CE-MS,direct-infusion-MS", "--write"
    )
    assert json.loads(index.read_text())[0]["techniques"] == ["LC-MS"]
    leaf = collection / "leaves/chromatographic-alignment/SKILL.md"
    assert actual_techniques(leaf) == []
