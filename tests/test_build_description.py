"""Regression tests for collection-neutral skill descriptions."""

from __future__ import annotations

import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts import collect_metabolomics_collection as collector  # noqa: E402
from scripts import lint_skill_descriptions as lint  # noqa: E402


def _description_from(source: str, source_field: str = "when_to_use") -> str:
    """Build a description with ``source`` in one supported source field."""
    if source_field == "when_to_use":
        return collector._build_description("documented-method", source, "")
    return collector._build_description("documented-method", "", source)


@pytest.mark.parametrize("source_field", ["when_to_use", "fallback_desc"])
@pytest.mark.parametrize(
    ("source", "expected_opening"),
    [
        ("Use when X", "Use when X"),
        ("use when X", "Use when X"),
        ("USE WHEN X", "Use when X"),
        ("Use when use when X", "Use when X"),
        ("Apply this skill when X", "Use when X"),
        ("reference FOR X", "Reference for X"),
        ("EXPLAINS X", "Explains X"),
        ("decision SUPPORT for X", "Decision support for X"),
    ],
)
def test_source_opening_is_canonical_and_not_doubled(
    source_field: str, source: str, expected_opening: str
) -> None:
    description = _description_from(source, source_field)

    assert description.startswith(expected_opening)
    canonical_prefix = expected_opening.rsplit(" ", 1)[0]
    assert description.lower().count(canonical_prefix.lower()) == 1
    assert lint.check_description(description) == []


def test_empty_input_uses_the_supplied_domain_label() -> None:
    description = collector._build_description(
        "documented-method", "", "", domain_label="proteomics"
    )

    assert "in a proteomics workflow" in description
    assert "proteomics" in description
    assert "metabolomics" not in description
    assert lint.check_description(description) == []


def test_empty_input_without_a_label_is_domain_neutral() -> None:
    description = collector._build_description("documented-method", "", "")

    assert "in the workflow it documents" in description
    assert "proteomics" not in description
    assert "metabolomics" not in description
    assert lint.check_description(description) == []


@pytest.mark.parametrize(
    ("domain_label", "expected_context"),
    [
        ("proteomics", "in proteomics analysis"),
        (None, "in the analysis it documents"),
    ],
)
def test_short_source_padding_uses_the_requested_context(
    domain_label: str | None, expected_context: str
) -> None:
    description = collector._build_description(
        "documented-method", "Use when X", "", domain_label=domain_label
    )

    assert expected_context in description
    assert lint.check_description(description) == []


def test_generated_descriptions_contain_no_marketing_terms() -> None:
    for term in collector.MARKETING_TERMS:
        description = collector._build_description(
            "documented-method",
            f"Use when the {term} workflow needs documented review",
            "",
        )

        assert term.lower() not in description.lower(), term
        assert lint.check_description(description) == [], term


@pytest.mark.parametrize("source_length", [10, 60, 400])
def test_every_source_length_produces_a_lint_clean_bounded_description(
    source_length: int,
) -> None:
    source = ("perform documented analysis " * 20)[:source_length]
    assert len(source) == source_length

    description = collector._build_description(
        "documented-method", source, "", domain_label="proteomics"
    )

    assert lint.check_description(description) == []
    assert collector.MIN_LEN <= len(description) <= collector.MAX_LEN
    assert lint.MIN_LEN <= len(description) <= lint.MAX_LEN
