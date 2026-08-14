"""Corpus DOIs must be canonical — no URL cruft (`?ref=`, `#sec…`, `.svg`).

A DOI carrying a query string or fragment is the same work as its canonical form,
but a string-keyed index treats the two as different papers: skills split across
both, and neither half sees the other's grounding. This guard keeps new cruft out.

One entry is a **documented exception**, deferred to the `orphan-grounding` human
decision rather than fixed here: `10.1021/acs.analchem.1c03163?ref=` (NPFimg, a real
tool with a repo) normalises onto `10.1021/acs.analchem.1c03163`, which already exists
as an empty-`repo_url` placeholder — one of the 78 `orphan-grounding` entries. Merging
a real entry into an orphan changes the orphan set, which only a human may decide (see
`agenticsciencebuilder_dev/docs/asbb/HUMAN_REVIEW_GATE.md`). So it is allow-listed here,
not silently normalised.
"""

import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).parent.parent
CANONICAL_DOI = re.compile(r"^10\.\d{4,9}/[^\s?#]+$")

# Deferred to the orphan-grounding decision — NOT a licence to add more.
KNOWN_ORPHAN_ENTANGLED = {"10.1021/acs.analchem.1c03163?ref="}


def _corpus_files():
    return sorted(ROOT.glob("collections/*/v*/corpus.yaml"))


def test_corpus_files_exist():
    assert _corpus_files(), "no collections/*/v*/corpus.yaml found"


def test_corpus_dois_are_canonical():
    """Every corpus DOI is canonical, except the documented orphan-entangled one."""
    offenders = []
    for cf in _corpus_files():
        doc = yaml.safe_load(cf.read_text()) or {}
        for paper in doc.get("papers", []):
            doi = (paper.get("doi") or "").strip()
            if not doi or CANONICAL_DOI.match(doi):
                continue
            if doi in KNOWN_ORPHAN_ENTANGLED:
                continue
            offenders.append(f"{cf.relative_to(ROOT)}: {doi!r}")
    assert not offenders, "non-canonical DOIs (strip ?ref=/#frag/.svg): " + "; ".join(offenders)


def test_the_only_allowed_exception_still_needs_a_human():
    """The allow-list must not outlive its cause: if the entangled DOI is gone from
    the corpus, delete the exception so it cannot mask a future regression."""
    present = set()
    for cf in _corpus_files():
        doc = yaml.safe_load(cf.read_text()) or {}
        present |= {(p.get("doi") or "").strip() for p in doc.get("papers", [])}
    stale = KNOWN_ORPHAN_ENTANGLED - present
    assert not stale, f"remove resolved allow-list entries: {stale}"


if __name__ == "__main__":
    import sys

    import pytest

    sys.exit(pytest.main([__file__, "-q"]))
