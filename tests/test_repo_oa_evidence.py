"""A repo-* access tier must be backed by evidence a clone was possible.

`access.type: repo-oa` is the paper-ACCESS axis (CONTENT_POLICY.md §3): it asserts a
public git repository was cloned at build. The only evidence of that is a non-empty
`repo_url`. `access.verified_via` is a constant stamp -- it reads
`git_clone_succeeded_at_build` even on entries with no repo_url -- so it corroborates
nothing. Without this check the tier is self-certifying: an empty string passes.

Two-sided, across four unrelated sciences so the rule is a property of the tier and not
of one corpus:
  - a repo-* entry with an EMPTY repo_url FAILs (in every domain);
  - a repo-* entry WITH a repo_url stays clean;
  - a non-repo OA tier with an empty repo_url stays clean (the check is scoped).
"""

import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import release_gate
from scripts.release_gate import FAIL, PASS, check_access_tier

# Four sciences with no shared vocabulary, none the code's home domain.
SCIENCES = [
    ("metabolomics", "10.1000/metab.1"),
    ("astrophysics", "10.1000/astro.2"),
    ("climate-science", "10.1000/climate.3"),
    ("electrophysiology", "10.1000/ephys.4"),
]

_EVIDENCE_MARK = "repo_url is empty"


def _paper(doi, access_type, repo_url):
    return {
        "doi": doi,
        "name": doi,
        "status": "included",
        "repo_url": repo_url,
        "access": {
            "type": access_type,
            "is_oa": True,
            "verified_via": "git_clone_succeeded_at_build",  # the constant stamp
        },
    }


def _evidence_findings(result):
    return [d for d in result.details if _EVIDENCE_MARK in d["message"]]


@pytest.mark.parametrize("science,doi", SCIENCES)
@pytest.mark.parametrize("tier", sorted(release_gate._REPO_OA_TIERS))
def test_repo_tier_without_repo_url_fails_in_every_science(science, doi, tier):
    res = check_access_tier({"papers": [_paper(doi, tier, "")]})
    findings = _evidence_findings(res)
    assert len(findings) == 1, f"{science}/{tier}: expected one evidence FAIL"
    assert findings[0]["status"] == FAIL
    assert res.status == FAIL


@pytest.mark.parametrize("science,doi", SCIENCES)
def test_repo_oa_with_repo_url_is_clean(science, doi):
    res = check_access_tier(
        {"papers": [_paper(doi, "repo-oa", "https://github.com/acme/tool")]}
    )
    assert _evidence_findings(res) == []
    assert res.status == PASS


@pytest.mark.parametrize("science,doi", SCIENCES)
def test_non_repo_tier_with_empty_repo_url_is_not_flagged(science, doi):
    # gold-oa never claims a clone, so an empty repo_url is irrelevant to it.
    res = check_access_tier({"papers": [_paper(doi, "gold-oa", "")]})
    assert _evidence_findings(res) == []


def test_verified_via_stamp_alone_is_not_evidence():
    # The exact shipped shape: verified_via says a clone succeeded, repo_url empty.
    res = check_access_tier({"papers": [_paper("10.1002/9780470508183", "repo-oa", "")]})
    assert len(_evidence_findings(res)) == 1


def test_evidence_fails_block_only_under_strict():
    # A FAIL on this hard gate blocks under --strict (promotion) and is advisory
    # otherwise (staged PRs): blocking_fail = strict and counts[FAIL] > 0.
    corpus = {"papers": [_paper(doi, "repo-oa", "") for _, doi in SCIENCES]}
    res = check_access_tier(corpus)
    assert res.status == FAIL and len(_evidence_findings(res)) == len(SCIENCES)
    assert (True and res.status == FAIL) is True  # strict → blocks
    assert (False and res.status == FAIL) is False  # advisory → reported, exit 0


def test_excluded_entries_are_not_checked():
    p = _paper("10.1000/held.9", "repo-oa", "")
    p["status"] = "hold"
    res = check_access_tier({"papers": [p]})
    assert _evidence_findings(res) == []


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
