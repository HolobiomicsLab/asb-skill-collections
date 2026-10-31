"""The four candidate gates of 2026-09-20 stopped on false positives; pin the fix.

Measured on the class-A candidates (HUMAN_REVIEW_GATE.md, "Task 8 candidate gates"):
transcriptomics (9 leaves), proteomics (2) stopped on `nhs_number` matching bare
ten-digit runs; epigenomics (6) on a template e-mail with a placeholder local part;
agentic-ai (2) on the textbook SSN example; one transcriptomics leaf on a real,
de-identified public-dataset sample label. Owner decision 2026-10-29: option (a),
label-bound `nhs_number`, placeholder local-part rule, exact allowlists; the sample
label is kept by an owner-read exact allowlist entry.

Two-sided, per the generalize-or-stop rule: the real spans must pass, the real
identifiers they resemble must still be caught, and the allowlist must not widen.
"""
import pathlib
import re
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts.pii_config import (  # noqa: E402
    PII_CONFIG,
    _hard_fail_allowlisted,
    _is_notation_not_email,
)

HARD = {k: re.compile(v, re.IGNORECASE) for k, v in PII_CONFIG["hard_fail_patterns"].items()}
NHS = HARD["nhs_number"]
SSN = HARD["ssn"]
HOSPITAL = HARD["hospital_id"]
EMAIL = re.compile(PII_CONFIG["email_regex"])

# --- the measured spans, verbatim shape ------------------------------------------
MEASURED_MUST_PASS = [
    # transcriptomics, PAC README: a Bloom-filter bit budget, not an NHS number.
    (NHS, "run with -b 1000000000 to set the Bloom filter size in bits"),
    # proteomics, XTandem Parser benchmark table: two adjacent cells.
    (NHS, "Number of quality spectra 223327 7644 Parsing time (s)"),
]


@pytest.mark.parametrize("pat,text", MEASURED_MUST_PASS)
def test_bare_digit_runs_no_longer_match_nhs(pat, text):
    assert not pat.search(text), f"nhs_number still fires on a bare digit run: {text!r}"


@pytest.mark.parametrize(
    "text",
    [
        "the record shows NHS number 943 476 5919 for the index case",
        "NHS no. 9434765919 was quoted",
        "NHS# 943-476-5919",
        "nhs number: 943 476 5919",
    ],
)
def test_labelled_nhs_numbers_are_still_caught(text):
    assert NHS.search(text), f"missed a labelled NHS number in: {text!r}"


def test_template_email_with_placeholder_local_part_is_not_an_email():
    # epigenomics, Watchdog WMS README usage line.
    span = "configureExamples.sh [-m your@mail-adress.com]"
    m = EMAIL.search(span)
    assert m and _is_notation_not_email(m.group(0), match=m)


@pytest.mark.parametrize(
    "email",
    ["jane.smith@univ-cotedazur.fr", "yourname2@mail-adress.com", "user1@lab.org", "j.doe@cnrs.fr"],
)
def test_real_looking_emails_are_still_emails(email):
    m = EMAIL.search(f"contact {email} for the data")
    assert m and not _is_notation_not_email(m.group(0), match=m), email


def test_textbook_ssn_example_is_allowlisted_but_other_ssns_are_not():
    # agentic-ai: the paper's own example record.
    m = SSN.search("record = {'ssn': '123-45-6789'}")
    assert m and _hard_fail_allowlisted("ssn", m.group(0))
    m2 = SSN.search("the field held 987-65-4320 for one subject")
    assert m2 and not _hard_fail_allowlisted("ssn", m2.group(0))


def test_owner_read_sample_label_is_allowlisted_exactly():
    # transcriptomics, 10.1093/bioinformatics/btad419: de-identified sample label.
    m = HOSPITAL.search("sample 4 (patient id 11352.p1) in [4]")
    assert m and _hard_fail_allowlisted("hospital_id", m.group(0))
    # A different or longer identifier never inherits the exemption.
    for other in ("patient id 11353", "patient id 113520", "hospital id 11352"):
        m2 = HOSPITAL.search(f"see {other} in the cohort")
        assert m2 and not _hard_fail_allowlisted("hospital_id", m2.group(0)), other


def test_allowlist_holds_only_documented_exact_values():
    allow = PII_CONFIG["hard_fail_allowlist_exact"]
    assert set(allow) <= set(PII_CONFIG["hard_fail_patterns"])
    for label, entries in allow.items():
        for value, reason in entries.items():
            assert HARD[label].fullmatch(value), (label, value)
            assert reason.strip(), (label, value)
    assert _hard_fail_allowlisted("ssn", "123-45-6789")
    assert not _hard_fail_allowlisted("mrn", "123-45-6789")


def test_version_bumped_for_this_change():
    assert PII_CONFIG["version"] >= "2026-10-29.1"


def test_both_config_copies_are_identical():
    a = (REPO_ROOT / "scripts" / "pii_config.py").read_text()
    b = (REPO_ROOT / "collections" / "metabolomics" / "v2" / "scripts" / "pii_config.py").read_text()
    assert a == b
