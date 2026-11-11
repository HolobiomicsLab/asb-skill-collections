"""Ranking contract of the default selector (asb-keyword 1.0.0, rule router).

A skill asked for by its own name comes first, a named tool counts, and a
plumbing description is neither removed nor pushed below other matches.
Selector 1.1.0 broke the first and the last of these; see docs/selection.md.
"""

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


def test_a_skill_named_by_the_query_outranks_skills_that_only_describe_it():
    rows = [
        {
            "slug": "annotation-with-spectral-library-matching",
            "name": "Annotation review",
            "description": "Review annotations from spectral library matching results.",
            "tools": [],
        },
        {
            "slug": "spectral-library-matching",
            "name": "Spectral library matching",
            "description": "Compare experimental MS/MS spectra with reference records.",
            "tools": [],
        },
    ]

    hits = index.keyword_search(rows, "spectral library matching", k=2)

    assert [hit["slug"] for hit in hits] == [
        "spectral-library-matching",
        "annotation-with-spectral-library-matching",
    ]
    assert hits[0]["score"] == hits[1]["score"] == 3.0


def test_a_plumbing_description_does_not_bury_a_skill_named_by_the_query():
    rows = [
        {
            "slug": "retention-time-alignment",
            "name": "Retention time alignment",
            "description": "Load and handle retention time tables, then align runs.",
            "tools": [],
        },
        {
            "slug": "retention-time-drift-review",
            "name": "Drift review",
            "description": "Review retention time drift and alignment quality across runs.",
            "tools": [],
        },
    ]

    hits = index.keyword_search(rows, "retention time alignment", k=2)

    assert hits[0]["slug"] == "retention-time-alignment"
    assert hits[0]["score"] == 3.0


def test_an_exact_tool_name_in_the_query_adds_two_points(ranking_rows):
    hits = index.keyword_search(ranking_rows, "ZODIAC candidate ranking", k=5)

    assert [hit["slug"] for hit in hits] == [
        "zodiac-parameter-configuration",
        "formula-candidate-ranking",
    ]
    assert [hit["score"] for hit in hits] == [3.0, 2.0]


def test_requested_plumbing_ranks_first(ranking_rows):
    hits = index.keyword_search(
        ranking_rows,
        "export an MGF submission file for GNPS",
        k=5,
    )

    assert hits[0]["slug"] == "gnps-submission-export"


def test_equal_scores_prefer_the_name_the_query_covers_most():
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
    assert hits[0]["score"] == hits[1]["score"] == 2.0
