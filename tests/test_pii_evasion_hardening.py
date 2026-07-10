"""The clinical-identifier patterns must resist trivial separator obfuscation.

The red-team recall harness (`test_pii_dual_use_gate.py`) found the gate missed
`M.R.N 4820193` (dotted) and `000 00 0000` (space-separated SSN): `\\bMRN\\b` and the
dash-only SSN pattern didn't tolerate separators. This tightens both — while keeping
them at **zero false positives** on the real 43k-span corpus, because each still
requires its discriminating digit run.

Two-sided, per the generalize-or-stop rule:
  * must-catch: the original forms AND their obfuscations;
  * must-not-catch: legitimate numeric prose that merely resembles an identifier;
  * a corpus-wide false-positive floor (0) as a regression guard against future
    loosening — if someone widens these regexes and starts matching real spans, this
    turns red.
"""
import pathlib
import re
import sys

import pytest

REPO_ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))
from scripts.release_gate import (  # noqa: E402
    PII_CONFIG,
    _collect_evidence_spans,
    _iter_skill_md,
    _read_frontmatter,
)

MRN = re.compile(PII_CONFIG["hard_fail_patterns"]["mrn"], re.IGNORECASE)
SSN = re.compile(PII_CONFIG["hard_fail_patterns"]["ssn"], re.IGNORECASE)

MUST_CATCH = [
    (MRN, "the record listed MRN: 4820193 here"),       # original
    (MRN, "the code M.R.N 4820193 was printed"),         # dotted evasion
    (MRN, "stamped M R N 4820193 on the vial"),          # spaced evasion
    (SSN, "identifier 000-00-0000 in one row"),          # original
    (SSN, "the field held 000 00 0000 without dashes"),  # spaced evasion
]

MUST_NOT_CATCH = [
    (SSN, "the measured m/z 415.2201 matched the formula"),
    (SSN, "software version 1.20.3040 was released"),
    (SSN, "grid offset 41 22 0100 in the map"),          # 2-2-4, not 3-2-4
    (MRN, "the mrn cohort was large that year"),          # word, no digit run
    (MRN, "gene M.R.N.1 carried the variant"),            # <5 digit run
]


@pytest.mark.parametrize("pat,text", MUST_CATCH)
def test_obfuscated_identifiers_are_caught(pat, text):
    assert pat.search(text), f"missed a HARD_FAIL identifier in: {text!r}"


@pytest.mark.parametrize("pat,text", MUST_NOT_CATCH)
def test_legitimate_numeric_prose_is_not_flagged(pat, text):
    assert not pat.search(text), f"false positive on benign prose: {text!r}"


def test_version_was_bumped_for_the_pattern_change():
    # A pattern change must bump the config version so gate_report.json records it.
    assert PII_CONFIG["version"] >= "2026-07-10.1"


def _corpus_spans():
    root = REPO_ROOT / "collections" / "metabolomics" / "v2"
    if not root.is_dir():
        return None
    spans = []
    for md in _iter_skill_md(root):
        fm, body = _read_frontmatter(md.read_text(encoding="utf-8", errors="ignore"))
        spans += [s["text"] for s in _collect_evidence_spans(fm, body)]
    return spans


def test_zero_false_positives_on_real_corpus():
    """Regression floor: neither tightened pattern may fire on any real span."""
    spans = _corpus_spans()
    if spans is None:
        pytest.skip("metabolomics/v2 corpus not present in this checkout")
    mrn_fp = [t for t in spans if MRN.search(t)]
    ssn_fp = [t for t in spans if SSN.search(t)]
    assert not mrn_fp, f"MRN pattern false-positived on {len(mrn_fp)} real spans, e.g. {mrn_fp[:2]}"
    assert not ssn_fp, f"SSN pattern false-positived on {len(ssn_fp)} real spans, e.g. {ssn_fp[:2]}"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
