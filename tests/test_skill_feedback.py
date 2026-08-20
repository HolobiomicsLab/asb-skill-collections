"""Usage reports must dedupe across reporters and must not leak the reporter.

Two failure modes, both quiet. Leak: a home path, a token or a clinical
identifier rides a session transcript into a public issue. Fragmentation: ten
people hit one problem and open ten issues, because nothing recognised them as
the same problem — which is the failure that makes crowd-sourced feedback worse
than no feedback at all.
"""

from __future__ import annotations

import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts import skill_feedback as sf  # noqa: E402


# --------------------------------------------------------------------------- #
# Redaction                                                                    #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("secret,category", [
    ("/Users/someone/lab/samples", "posix_home"),
    ("/home/someone/lab/samples", "posix_home"),
    ("sk-abcdefghijklmnop0123", "credential"),
    ("ghp_abcdefghijklmnop0123", "credential"),
    ("Authorization: Bearer abc123", "authorization_header"),
    ("https://user:hunter2@internal.example/api", "url_userinfo"),
])
def test_an_outbound_secret_never_reaches_the_body(secret, category):
    out, removed = sf.redact(f"it failed on {secret} during the run")
    assert secret not in out
    assert category in removed


def test_a_clinical_identifier_is_caught_by_the_gates_own_patterns():
    """One canonical pattern set: the release gate's, not a second copy here."""
    out, removed = sf.redact("crashed on MRN 4820193 in the export")
    assert "4820193" not in out
    assert "mrn" in removed


def test_ordinary_technical_detail_survives_redaction():
    """The other side. Over-redacting produces a report nobody can act on."""
    text = ("mzmine 4.4.3 batch export wrote 0 rows; the skill says --format mgf "
            "but the CLI wants --export-mgf. Ran on Ubuntu 24.04, Python 3.12.")
    out, removed = sf.redact(text)
    assert out == text
    assert removed == []


def test_the_reader_is_told_what_was_removed():
    issue = sf.render_issue("defect", "spectral-library-match",
                            symptom="failed reading /Users/me/data/run1.mzML")
    assert "posix_home" in issue["redacted"]
    assert "Redacted before posting: posix_home." in issue["body"]


# --------------------------------------------------------------------------- #
# Fingerprinting — the same friction must collide across reporters             #
# --------------------------------------------------------------------------- #

def test_two_reporters_describing_one_problem_collide():
    a = sf.fingerprint("defect", "sirius-denovo", "the flag is wrong in the example")
    b = sf.fingerprint("defect", "sirius-denovo", "The example's flag is WRONG!")
    assert a == b


def test_wording_order_does_not_change_the_fingerprint():
    assert (sf.fingerprint("defect", "x", "timeout on large files")
            == sf.fingerprint("defect", "x", "files large on timeout"))


@pytest.mark.parametrize("kind,target,symptom", [
    ("gap", "sirius-denovo", "the flag is wrong in the example"),
    ("defect", "other-skill", "the flag is wrong in the example"),
    ("defect", "sirius-denovo", "crashes on empty input"),
])
def test_a_different_problem_gets_a_different_fingerprint(kind, target, symptom):
    """The other side: collapsing distinct reports would hide real problems."""
    baseline = sf.fingerprint("defect", "sirius-denovo", "the flag is wrong in the example")
    assert sf.fingerprint(kind, target, symptom) != baseline


def test_the_fingerprint_is_in_the_body_so_a_reader_can_match_on_it():
    issue = sf.render_issue("defect", "x", symptom="y")
    assert issue["fingerprint"] in issue["body"]


# --------------------------------------------------------------------------- #
# Routing and refusal                                                          #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("kind", sorted(sf.KINDS))
def test_every_kind_renders_and_carries_triage_labels(kind):
    issue = sf.render_issue(kind, "some-target", symptom="something went wrong")
    assert "usage-feedback" in issue["labels"]
    assert "needs-triage" in issue["labels"]
    assert sf.KINDS[kind] in issue["body"]


@pytest.mark.parametrize("kind,expected", [("gap", "propose"), ("composition", "workflow")])
def test_a_report_that_asks_for_new_work_is_labelled_as_a_proposal(kind, expected):
    assert expected in sf.labels_for(kind)


def test_a_defect_is_not_labelled_a_proposal():
    assert "propose" not in sf.labels_for("defect")


def test_an_unroutable_kind_is_refused_rather_than_relabelled():
    with pytest.raises(ValueError, match="unknown kind"):
        sf.render_issue("vibes", "x", symptom="y")


@pytest.mark.parametrize("target,symptom", [("", "something"), ("x", ""), ("x", "   ")])
def test_a_report_missing_its_substance_is_refused(target, symptom):
    with pytest.raises(ValueError):
        sf.render_issue("defect", target, symptom=symptom)


def test_corroboration_carries_the_fingerprint_and_is_redacted():
    text = sf.corroboration("abc123def456", "same crash under /home/me/x")
    assert "abc123def456" in text
    assert "/home/me/x" not in text


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
