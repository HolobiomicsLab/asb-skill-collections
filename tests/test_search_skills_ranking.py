"""Keyword fallback favours requested method roles over incidental plumbing."""

from __future__ import annotations

import pytest

from asb_skill_collections import asb_skill_index as index


@pytest.fixture
def ranking_rows() -> list[dict]:
    """Return a dozen role and plumbing leaves with realistic field overlap."""
    rows = [
        {
            "slug": "formula-candidate-ranking",
            "name": "Molecular formula candidate ranking",
            "description": "Rank molecular formula candidates from MS/MS evidence.",
            "tools": ["SIRIUS"],
        },
        {
            "slug": "zodiac-parameter-configuration",
            "name": "Parameter configuration",
            "description": "Parse a configuration file and toggle parameters for a request.",
            "tools": ["ZODIAC"],
        },
        {
            "slug": "gnps-submission-export",
            "name": "GNPS submission file export",
            "description": "Export an MGF file and build a GNPS submission request.",
            "tools": ["GNPS"],
        },
    ]
    rows.extend(
        {
            "slug": f"decoy-{number}",
            "name": f"Unrelated method {number}",
            "description": "Measure a distinct analytical outcome.",
            "tools": [f"Tool{number}"],
        }
        for number in range(1, 10)
    )
    assert len(rows) == 12
    return rows


def test_role_fields_outweigh_tool_only_plumbing(ranking_rows):
    hits = index.keyword_search(
        ranking_rows,
        "ZODIAC candidate ranking",
        k=5,
    )

    assert hits[0]["slug"] == "formula-candidate-ranking"


def test_requested_plumbing_is_not_deboosted(ranking_rows):
    hits = index.keyword_search(
        ranking_rows,
        "export an MGF submission file for GNPS",
        k=5,
    )

    assert hits[0]["slug"] == "gnps-submission-export"


def test_plumbing_penalty_de_ranks_instead_of_removing_a_match():
    row = {
        "slug": "retention-request-export",
        "name": "Retention request export",
        "description": "Export retention results and handle the request.",
        "tools": [],
    }

    hits = index.keyword_search([row], "retention", k=1)

    assert [hit["slug"] for hit in hits] == [row["slug"]]
    assert hits[0]["score"] == index.MATCHED_SCORE_FLOOR
    assert hits[0]["matched_fields"] == {
        "name": ["retention"],
        "description": ["retention"],
    }


def test_plumbing_leaf_ranks_below_role_leaf_with_the_same_matched_terms():
    rows = [
        {
            "slug": "spectral-library-file-export",
            "name": "Spectral library file export",
            "description": "Export spectral library files and handle the request.",
            "tools": [],
        },
        {
            "slug": "spectral-library-matching",
            "name": "Spectral library matching",
            "description": "Match experimental spectra against a spectral library.",
            "tools": [],
        },
    ]

    hits = index.keyword_search(rows, "spectral library", k=2)

    assert [hit["slug"] for hit in hits] == [
        "spectral-library-matching",
        "spectral-library-file-export",
    ]
    assert hits[1]["score"] == 4.0
    assert hits[1]["score"] < hits[0]["score"]
