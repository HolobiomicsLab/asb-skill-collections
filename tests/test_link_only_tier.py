"""The link-only access tier and the grounding labels derived from it.

`link-only` exists so a source with no public repository can be cited honestly
instead of carrying a `repo-oa` tier whose clone never happened. These tests
pin the two properties that keep it honest: it may not claim a clone, and the
skills resting on it must be labelled as weaker.
"""

from __future__ import annotations

import pathlib

import pytest
import yaml

from scripts import label_grounding_tier as lg
from scripts import release_gate

V2 = pathlib.Path(__file__).resolve().parent.parent / "collections" / "metabolomics" / "v2"


def _corpus(tmp_path, papers):
    path = tmp_path / "corpus.yaml"
    path.write_text(yaml.safe_dump({"papers": papers}), encoding="utf-8")
    return path


def test_link_only_is_an_admitted_tier():
    assert "link-only" in release_gate._NORMALIZED_OA_TIERS
    assert "link-only" not in release_gate._REPO_OA_TIERS, (
        "link-only must not inherit the repo-oa clone-evidence requirement"
    )


def test_link_only_entry_may_not_claim_a_clone(tmp_path):
    corpus = yaml.safe_load(
        _corpus(tmp_path, [{
            "doi": "10.1/x", "status": "included", "repo_url": "",
            "access": {"type": "link-only", "verified_via": "git_clone_succeeded_at_build"},
        }]).read_text()
    )
    res = release_gate.check_access_tier(corpus, require_open_access=True)
    assert any("claims no clone" in str(d) for d in res.details)


def test_clean_link_only_entry_passes(tmp_path):
    corpus = yaml.safe_load(
        _corpus(tmp_path, [{
            "doi": "10.1/x", "status": "included", "repo_url": "",
            "access": {"type": "link-only", "is_oa": None},
        }]).read_text()
    )
    res = release_gate.check_access_tier(corpus, require_open_access=True)
    assert not [d for d in res.details if str(d.get("level", "")).lower() == "fail"]


@pytest.mark.parametrize(
    "dois, weak, expected",
    [
        ([], set(), "ungrounded"),
        (["10.1/a"], {"10.1/a"}, "link-only"),
        (["10.1/a", "10.1/b"], {"10.1/a"}, "repo"),
        (["10.1/a", "10.1/b"], {"10.1/a", "10.1/b"}, "link-only"),
    ],
)
def test_tier_grades_by_weakest_evidence(dois, weak, expected):
    assert lg.tier_for(dois, weak) == expected


def test_no_source_never_defaults_to_the_strong_tier():
    """A skill citing nothing must not be presented as repository-grounded."""
    assert lg.tier_for([], {"10.1/a"}) == lg.UNGROUNDED
    assert lg.tier_for([], set()) != lg.REPO_GROUNDED


def test_released_corpus_has_no_orphan_repo_oa():
    raw = yaml.safe_load((V2 / "corpus.yaml").read_text(encoding="utf-8"))
    papers = raw["papers"] if isinstance(raw, dict) else raw
    orphans = [
        p for p in papers
        if (p.get("access") or {}).get("type") in release_gate._REPO_OA_TIERS
        and p.get("status") == "included"
        and not (p.get("repo_url") or "").strip()
    ]
    assert not orphans, f"{len(orphans)} repo-oa entries still claim an unverifiable clone"


def test_released_link_only_entries_carry_no_clone_stamp():
    raw = yaml.safe_load((V2 / "corpus.yaml").read_text(encoding="utf-8"))
    papers = raw["papers"] if isinstance(raw, dict) else raw
    stamped = [
        p["doi"] for p in papers
        if (p.get("access") or {}).get("type") == "link-only"
        and (p.get("access") or {}).get("verified_via")
    ]
    assert not stamped, f"link-only entries still claiming a clone: {stamped[:3]}"
