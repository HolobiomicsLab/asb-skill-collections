"""The PII hard-fail patterns must not over-fire on other sciences' number formats.

The gate is general (every science's skills pass through it), so its precision must be
measured on a cross-domain negative corpus — not just metabolomics. This is the lesson
that a space-tolerant SSN pattern taught: it passed 0-FP on the 43k-span metabolomics
corpus, then false-positived on a bare 3-2-4 digit run (`123 45 6789`) — an electrode
id, a weather-station id, a coordinate. A 3-2-4 spaced number is ambiguous between an
SSN and a scientific id, so the SSN pattern stays dash-only and the space form is an
accepted gap (test_pii_evasion_hardening::test_ambiguous_spaced_ssn_is_deliberately_not_forced).

Negatives span ≥4 sciences that are NOT the gate's home domain (per generalize-or-stop):
electrophysiology, climate, astronomy, genomics, plus non-PII clinical prose.
"""
import pathlib
import re
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts.release_gate import PII_CONFIG  # noqa: E402

HARD = {k: re.compile(v, re.IGNORECASE) for k, v in PII_CONFIG["hard_fail_patterns"].items()}

# (science, sentence) — legitimate prose that must NOT trip any HARD_FAIL pattern.
CROSS_DOMAIN_NEGATIVES = [
    ("electrophysiology", "Electrode 123 45 6789 recorded the spike train across trials."),
    ("climate", "Weather station 123 45 6789 logged the temperature anomaly."),
    ("astronomy", "The quasar at RA 12 34 56.7 and Dec +45 12 30 was catalogued."),
    ("astronomy", "Source 2MASS J12345678 fell in the survey footprint."),
    ("genomics", "Variant rs4820193 on chromosome 7 associates with the trait."),
    ("genomics", "The interval chr7 12 34 5678 showed a called peak."),
    ("clinical-nonPII", "The patient cohort showed elevated inflammatory markers."),
    ("proteomics", "Peptide precursor 415.22 eluted at 12.34 minutes."),
    ("materials", "Sample 12 34 5678 was annealed at 900 K for two hours."),
]


@pytest.mark.parametrize("science,text", CROSS_DOMAIN_NEGATIVES)
def test_no_hard_fail_pattern_fires_on_cross_domain_prose(science, text):
    hits = [name for name, pat in HARD.items() if pat.search(text)]
    assert not hits, f"[{science}] false-positive PII patterns {hits} on: {text!r}"


def test_covers_at_least_four_distinct_nonhome_sciences():
    sciences = {s for s, _ in CROSS_DOMAIN_NEGATIVES if s != "metabolomics"}
    assert len(sciences) >= 4, f"need >=4 non-home sciences, got {sorted(sciences)}"


def test_named_patient_still_catches_real_names_not_common_prose():
    """named_patient_dx must catch 'Patient Jane Roe' but NOT 'patient cohort showed'
    (the IGNORECASE-capitalisation over-firing this test surfaced)."""
    pat = HARD["named_patient_dx"]
    assert pat.search("The vignette described Patient Jane Roe as a case."), "must catch a real named patient"
    for prose in ("patient cohort showed elevated markers",
                  "patient samples were collected at baseline",
                  "patient data indicated a trend"):
        assert not pat.search(prose), f"over-fires on common clinical prose: {prose!r}"


def test_the_ssn_pattern_is_dash_only():
    """Pin the decision: space-tolerant SSN over-fires cross-domain; keep it dashed."""
    ssn = PII_CONFIG["hard_fail_patterns"]["ssn"]
    assert ssn == r"\b\d{3}-\d{2}-\d{4}\b", (
        "SSN must stay dash-only — a space/other-separator form over-fires on scientific "
        "3-2-4 numeric ids (see this test's electrode/station negatives)"
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
