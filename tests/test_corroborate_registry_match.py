"""Offline checks for registry-match corroboration signals."""
import json
from pathlib import Path
import subprocess
import sys

from scripts import corroborate_registry_match as c


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures" / "registry_match_corroboration"


def _record(
    slug: str,
    evidence: str,
    registry_text: str,
    registry: str = "bioconda",
    label: str = "accepted_match",
    registry_record: dict | None = None,
) -> dict:
    return {
        "tool_slug": slug,
        "tool_name": slug,
        "registry": registry,
        "registry_package": slug,
        "label": label,
        "texts": {"tool_evidence": evidence, "registry_description": registry_text},
        "identity_values": [slug],
        "registry_record": registry_record or {"summary": registry_text},
    }


SYNTHETIC_RECORDS = [
    _record("lipidr", "library(lipidr) quantifies lipid spectra", "Lipid spectra quantification", "bioconductor"),
    _record("peaks", "pip install peaks; Python mass peak detection", "Python mass peak detection", registry_record={"source_url": "https://pypi.io/peaks.tgz"}),
    _record("workflow", "conda install workflow; sequence pipeline runner", "Sequence pipeline runner"),
    _record("plotter", "plotter.Rmd creates chemical figures", "Chemical figure creation", "bioconductor"),
    _record("reader", "reader.py parses tandem spectra", "Python tandem spectrum parser", registry_record={"summary": "Python tandem spectrum parser"}),
    _record("overlap", "fragment isotope annotation", "isotope fragment annotation"),
    _record("empty", "", "A richly described registry package"),
    _record("bacteria", "mass spectrum molecular annotation", "bacterial genome read typing", label="wrong_match"),
    _record("methyl", "tandem spectra formula prediction", "DNA methylation trajectory analysis", "bioconductor", "wrong_match"),
    _record("pycollision", "library(pycollision) models metabolites", "Python genome assembler", label="wrong_match", registry_record={"source_url": "https://pypi.io/pycollision.tgz"}),
    _record("javacollision", "Java metabolite network reconstruction", "Differential metabolite statistics", "bioconductor", "wrong_match"),
    _record("thin", "thin", "bacterial abundance estimator", label="wrong_match"),
]


def test_ecosystem_detection_covers_commands_urls_and_extensions():
    text = "library(x); pip install y; conda install z; code.Rmd script.py model.jar task.rb"
    assert c.detect_ecosystems(text) == {"r", "python", "conda", "java", "ruby"}


def test_bioconductor_is_consistent_with_explicit_r_evidence():
    signal = c.ecosystem_signal("BiocManager::install('x')", "bioconductor", {})
    assert signal["verdict"] == "corroborated"
    assert signal["registry_ecosystems"] == ["r"]


def test_ecosystem_disagreement_is_a_contradiction():
    record = {"source_url": "https://pypi.io/packages/example.tar.gz"}
    signal = c.ecosystem_signal("library(example)", "bioconda", record)
    assert signal["evidence_ecosystems"] == ["r"]
    assert signal["registry_ecosystems"] == ["python"]
    assert signal["verdict"] == "contradicted"


def test_domain_signal_removes_the_exact_match_identity():
    signal = c.domain_signal(
        "Orbit aligns tandem mass spectra",
        "Orbit aligns bacterial genome reads",
        ["Orbit"],
        threshold=0.1,
    )
    assert "orbit" not in signal["overlap_tokens"]
    assert signal["overlap_tokens"] == ["aligns"]


def test_domain_agreement_and_disagreement_are_distinct():
    agreeing = c.domain_signal(
        "annotates tandem mass spectra fragments",
        "fragment annotation for tandem mass spectra",
        ["tool"],
        threshold=0.1,
    )
    disagreeing = c.domain_signal(
        "annotates tandem mass spectra fragments",
        "bacterial genome read taxonomic typing",
        ["tool"],
        threshold=0.1,
    )
    assert agreeing["verdict"] == "corroborated"
    assert disagreeing["verdict"] == "contradicted"


def test_missing_or_thin_text_is_insufficient():
    missing = c.domain_signal("", "bacterial genome read typing", ["tool"], 0.1)
    identity_only = c.domain_signal("Orbit", "Orbit package", ["Orbit"], 0.1)
    assert missing["verdict"] == "insufficient"
    assert identity_only["verdict"] == "insufficient"


def test_combined_verdict_preserves_conflict_as_insufficient():
    assert c.combined_verdict("contradicted", "corroborated") == "insufficient"
    assert c.combined_verdict("contradicted", "insufficient") == "contradicted"
    assert c.combined_verdict("insufficient", "corroborated") == "corroborated"
    assert c.combined_verdict("insufficient", "insufficient") == "insufficient"


def test_tuning_and_split_are_deterministic_on_twelve_records():
    first = c.analyse_records(SYNTHETIC_RECORDS, seed=17, held_out_fraction=0.30)
    second = c.analyse_records(SYNTHETIC_RECORDS, seed=17, held_out_fraction=0.30)
    assert first == second
    assert first["measurements"]["tuning"]["accepted_matches"] == 5
    assert first["measurements"]["held_out"]["accepted_matches"] == 2
    assert first["measurements"]["tuning"]["wrong_matches"] == 5
    assert first["measurements"]["held_out"]["wrong_matches"] == 5


def test_threshold_candidates_come_from_tuning_records_only():
    tuning, _ = c._split_positive_slugs(SYNTHETIC_RECORDS, 17, 0.30)
    selected = [
        record for record in SYNTHETIC_RECORDS
        if record["label"] == "wrong_match" or record["tool_slug"] in tuning
    ]
    result = c.analyse_records(SYNTHETIC_RECORDS, seed=17, held_out_fraction=0.30)
    assert result["method"]["threshold_candidates"] == c._threshold_candidates(selected)


def test_synthetic_fixture_exercises_all_three_combined_verdicts():
    result = c.analyse_records(SYNTHETIC_RECORDS, seed=17, held_out_fraction=0.30)
    assert {record["verdict"] for record in result["records"]} == {
        "corroborated",
        "contradicted",
        "insufficient",
    }


def test_cli_regenerates_committed_fixture_byte_for_byte(tmp_path):
    output = tmp_path / "result.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/corroborate_registry_match.py",
            "--collection", str(FIXTURES / "collection"),
            "--registry-config", str(FIXTURES / "registry_config.yaml"),
            "--bioconda", str(FIXTURES / "bioconda.json"),
            "--bioconductor", str(FIXTURES / "bioconductor.json"),
            "--seed", "17",
            "--bioconda-snapshot-date", "2026-11-07",
            "--bioconductor-snapshot-date", "2026-11-07",
            "--output", str(output),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert output.read_bytes() == (FIXTURES / "expected.json").read_bytes()


def test_committed_result_validates_and_discloses_unretained_inputs():
    result = json.loads(
        (ROOT / "docs/design/registry-match-corroboration-2026-11-07.json").read_text()
    )
    c.validate_result(result)
    assert len(result["records"]) == 94
    assert result["method"]["threshold"] == 0.021713
    assert len(result["method"]["threshold_candidates"]) == 38
    for registry in ("bioconda", "bioconductor"):
        assert result["inputs"][registry]["snapshot_date"] == "2026-11-07"
        assert result["inputs"][registry]["retained"] is False
        assert result["inputs"][registry]["file"] is None
        assert result["inputs"][registry]["sha256"] is None
