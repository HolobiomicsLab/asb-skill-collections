"""A recorded licence must say which thing it licenses.

`access.license` is written by two resolvers with different evidence: one reads
a code repository and can only speak about the tool, the other reads a DOI
registry and can only speak about the paper. The value itself does not
distinguish them — `MIT` can be a tool licence and `CC-BY-4.0` a paper licence,
and one corpus holds both.

Without the distinction, a repository lookup silently substitutes a tool licence
for a paper one: 61 entries in metabolomics/v1 changed meaning that way in a
single run, and no guard fired, because a value was still present. Substitution
is worse than erasure for exactly that reason.
"""

from __future__ import annotations

import glob
import pathlib
import sys

import pytest
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts.license_tier import (SUBJECT_PAPER, SUBJECT_TOOL,  # noqa: E402
                                  licence_subject)

ROOT = pathlib.Path(__file__).parent.parent


# --------------------------------------------------------------------------- #
# Derivation — from evidence already in the entry, never a default             #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("detection", ["github-api", "license-file", "r-description", "readme-llm"])
def test_a_licence_read_from_a_repository_is_about_the_tool(detection):
    assert licence_subject(
        {"access": {"license": "MIT"}, "license_detection": detection}) == SUBJECT_TOOL


@pytest.mark.parametrize("detection", ["crossref-paper", "datacite-paper", "biorxiv_api-paper"])
def test_a_licence_read_from_a_registry_is_about_the_paper(detection):
    assert licence_subject(
        {"access": {"license": "CC-BY-4.0"}, "license_detection": detection}) == SUBJECT_PAPER


def test_a_clone_verified_licence_is_about_the_tool():
    """Non-GitHub repos (GitLab, Bitbucket) carry no detection label; the
    licence was still read out of a checkout."""
    assert licence_subject({
        "access": {"license": "AGPL-3.0", "verified_via": "git_clone_succeeded_at_build"},
    }) == SUBJECT_TOOL


def test_an_unpaywall_verified_licence_is_about_the_paper():
    assert licence_subject({
        "access": {"license": "cc-by", "verified_via": "unpaywall_best_oa_location"},
    }) == SUBJECT_PAPER


def test_an_explicit_label_is_believed_over_the_derivation():
    """Once a resolver has declared the subject, that is the record."""
    assert licence_subject({
        "access": {"license": "MIT"}, "license_detection": "github-api",
        "license_subject": SUBJECT_PAPER}) == SUBJECT_PAPER


# --------------------------------------------------------------------------- #
# Refusal — the other side                                                     #
# --------------------------------------------------------------------------- #

def test_an_entry_with_no_licence_has_no_subject():
    assert licence_subject({"access": {"license": None}, "license_detection": "none"}) is None


def test_an_unrecognised_evidence_source_is_unlabelled_not_defaulted():
    """A new detection source must show up as unknown rather than be filed
    under whichever axis happens to be first in the code."""
    assert licence_subject({
        "access": {"license": "MIT", "verified_via": "some-future-method"},
        "license_detection": "some-future-source"}) is None


def test_a_nonsense_label_does_not_survive():
    assert licence_subject({
        "access": {"license": "MIT", "verified_via": "unpaywall_oa_locations"},
        "license_subject": "vibes"}) == SUBJECT_PAPER


# --------------------------------------------------------------------------- #
# The corpora themselves                                                       #
# --------------------------------------------------------------------------- #

def _corpus_files():
    return sorted(ROOT.glob("collections/*/v*/corpus.yaml"))


def test_every_recorded_licence_declares_its_subject():
    """No entry may carry a licence whose axis is unknown."""
    offenders = []
    for cf in _corpus_files():
        for paper in (yaml.safe_load(cf.read_text()) or {}).get("papers") or []:
            if (paper.get("access") or {}).get("license") and not licence_subject(paper):
                offenders.append(f"{cf.parent}: {paper.get('name')}")
    assert not offenders, f"licences with no identifiable subject: {offenders}"


def test_the_stored_label_agrees_with_the_evidence():
    """A stored label that contradicts the entry's own evidence would let a
    substitution hide behind the very field meant to prevent it."""
    offenders = []
    for cf in _corpus_files():
        for paper in (yaml.safe_load(cf.read_text()) or {}).get("papers") or []:
            stored = paper.get("license_subject")
            if not stored:
                continue
            derived = licence_subject({k: v for k, v in paper.items() if k != "license_subject"})
            if derived and derived != stored:
                offenders.append(f"{cf.parent}: {paper.get('name')} stored={stored} evidence={derived}")
    assert not offenders, offenders


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
