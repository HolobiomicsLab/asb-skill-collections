"""Tests for scripts/tier_update.py.

Covers the existing review-attestation path (backward compatible) and the new
author-credit path: a contributor listed as a skill ``author`` is credited in
contributors.jsonld (a contributions counter is incremented + tier re-evaluated)
when their authored skill is merged. See Task 5 / governance/AUTHORSHIP.md.
"""
import json
import pathlib
import sys

import pytest
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import tier_update as tu


# --- fixtures ---------------------------------------------------------------

CRITERIA = {
    "thresholds": {
        "reviewer": {"min_reviews": 1},
        "domain_contributor": {"min_reviews": 5},
        "curator": {"min_reviews": 10},
        "lead_curator": {"min_reviews": 30, "min_external_reviews": 20},
    }
}


def _registry(orcid="0000-0002-1111-2222", **extra):
    contrib = {"orcid": f"https://orcid.org/{orcid}", "asb:tier": "none"}
    contrib.update(extra)
    return {"contributors": [contrib]}


def _write(tmp_path):
    contributors = tmp_path / "contributors.jsonld"
    criteria = tmp_path / "curator-criteria.yaml"
    criteria.write_text(yaml.safe_dump(CRITERIA))
    return contributors, criteria


def _load(path):
    return json.loads(pathlib.Path(path).read_text())["contributors"][0]


# --- existing review path (backward compatibility) --------------------------

def test_review_path_increments_reviews_and_promotes(tmp_path):
    contributors, criteria = _write(tmp_path)
    contributors.write_text(json.dumps(_registry()))

    tu.update_contributor(
        contributors, criteria,
        orcid="0000-0002-1111-2222", collection_slug="metabolomics",
        is_self_authored=False,
    )

    c = _load(contributors)
    assert c["asb:total_reviews"] == 1
    assert c["asb:external_reviews"] == 1
    assert c["asb:tier"] == "reviewer"


def test_review_path_missing_contributor_exits_1(tmp_path):
    contributors, criteria = _write(tmp_path)
    contributors.write_text(json.dumps(_registry(orcid="0000-0000-0000-0000")))

    with pytest.raises(SystemExit) as exc:
        tu.update_contributor(
            contributors, criteria,
            orcid="0000-0002-9999-9999", collection_slug="metabolomics",
            is_self_authored=False,
        )
    assert exc.value.code == 1


# --- new author-credit path -------------------------------------------------

def test_author_credit_increments_contributions_and_reevaluates(tmp_path):
    contributors, criteria = _write(tmp_path)
    contributors.write_text(json.dumps(_registry()))

    tu.credit_author(
        contributors, criteria,
        orcid="0000-0002-1111-2222", collection_slug="metabolomics",
    )

    c = _load(contributors)
    # A new, separate counter — does NOT touch review counters.
    assert c["asb:authored_skills"] == 1
    assert "asb:total_reviews" not in c
    # An authored, merged skill credits the contributor at >= reviewer tier.
    assert c["asb:tier"] == "reviewer"


def test_author_credit_accumulates(tmp_path):
    contributors, criteria = _write(tmp_path)
    contributors.write_text(json.dumps(_registry(**{"asb:authored_skills": 2})))

    tu.credit_author(
        contributors, criteria,
        orcid="0000-0002-1111-2222", collection_slug="metabolomics",
    )

    assert _load(contributors)["asb:authored_skills"] == 3


def test_author_credit_does_not_downgrade_existing_tier(tmp_path):
    contributors, criteria = _write(tmp_path)
    # An established curator (12 reviews) who also authors a skill keeps curator.
    contributors.write_text(
        json.dumps(
            _registry(
                **{
                    "asb:total_reviews": 12,
                    "asb:external_reviews": 12,
                    "asb:tier": "curator",
                }
            )
        )
    )

    tu.credit_author(
        contributors, criteria,
        orcid="0000-0002-1111-2222", collection_slug="metabolomics",
    )

    c = _load(contributors)
    assert c["asb:authored_skills"] == 1
    assert c["asb:total_reviews"] == 12  # untouched
    assert c["asb:tier"] == "curator"  # not downgraded to reviewer


def test_author_credit_missing_contributor_exits_1(tmp_path):
    contributors, criteria = _write(tmp_path)
    contributors.write_text(json.dumps(_registry(orcid="0000-0000-0000-0000")))

    with pytest.raises(SystemExit) as exc:
        tu.credit_author(
            contributors, criteria,
            orcid="0000-0002-9999-9999", collection_slug="metabolomics",
        )
    assert exc.value.code == 1


def test_evaluate_tier_authored_only_reaches_reviewer(tmp_path):
    # No reviews but >=1 authored skill -> reviewer (entry tier).
    assert tu.evaluate_tier(0, 0, CRITERIA, authored_skills=1) == "reviewer"
    # Zero of everything -> none.
    assert tu.evaluate_tier(0, 0, CRITERIA, authored_skills=0) == "none"


def test_cli_credit_author_flag(tmp_path):
    contributors, criteria = _write(tmp_path)
    contributors.write_text(json.dumps(_registry()))

    tu.main(
        [
            "--orcid", "0000-0002-1111-2222",
            "--collection", "metabolomics",
            "--credit-author",
            "--contributors", str(contributors),
            "--criteria", str(criteria),
        ]
    )

    assert _load(contributors)["asb:authored_skills"] == 1
