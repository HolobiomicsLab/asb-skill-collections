"""Unit tests for check_coi.py using mocked OpenAlex API responses."""
import unittest.mock as mock

from scripts.check_coi import check_coi


# -- fixtures ----------------------------------------------------------------

MOCK_WORK_WITH_COAUTHOR = {
    "id": "https://openalex.org/W1234567890",
    "doi": "https://doi.org/10.1234/test-paper",
    "authorships": [
        {
            "author": {
                "id": "https://openalex.org/A1111",
                "orcid": "https://orcid.org/0000-0001-1234-5678",
                "display_name": "Lead Author",
            },
            "author_position": "first",
            "is_corresponding": False,
        },
        {
            "author": {
                "id": "https://openalex.org/A2222",
                "orcid": "https://orcid.org/0000-0002-9876-5432",
                "display_name": "Co-author",
            },
            "author_position": "middle",
            "is_corresponding": True,
        },
    ],
}

MOCK_WORK_WITHOUT_ORCID_MATCH = {
    "id": "https://openalex.org/W9999",
    "doi": "https://doi.org/10.1234/other-paper",
    "authorships": [
        {
            "author": {
                "id": "https://openalex.org/A3333",
                "orcid": "https://orcid.org/0000-0003-0000-0000",
                "display_name": "Someone Else",
            },
            "author_position": "first",
            "is_corresponding": True,
        }
    ],
}


# -- tests -------------------------------------------------------------------


def test_check_coi_detects_coauthor():
    """Reviewer who is a coauthor should be flagged."""
    with mock.patch(
        "scripts.check_coi.fetch_work_by_doi", return_value=MOCK_WORK_WITH_COAUTHOR
    ):
        result = check_coi(
            orcid="0000-0002-9876-5432",
            doi="10.1234/test-paper",
        )
    assert result.is_coauthor is True
    assert result.author_position == 2
    assert result.is_corresponding is True
    assert result.error is None


def test_check_coi_detects_non_coauthor():
    """Reviewer who is not a coauthor should not be flagged."""
    with mock.patch(
        "scripts.check_coi.fetch_work_by_doi",
        return_value=MOCK_WORK_WITHOUT_ORCID_MATCH,
    ):
        result = check_coi(
            orcid="0000-0002-9876-5432",
            doi="10.1234/other-paper",
        )
    assert result.is_coauthor is False
    assert result.author_position is None
    assert result.is_corresponding is False


def test_check_coi_normalizes_orcid_url():
    """Full ORCID URL should be normalized to bare ID."""
    with mock.patch(
        "scripts.check_coi.fetch_work_by_doi", return_value=MOCK_WORK_WITH_COAUTHOR
    ):
        result = check_coi(
            orcid="https://orcid.org/0000-0002-9876-5432",
            doi="10.1234/test-paper",
        )
    assert result.is_coauthor is True
    assert result.orcid == "0000-0002-9876-5432"


def test_check_coi_handles_api_failure():
    """API failure should return error result, not raise."""
    with mock.patch("scripts.check_coi.fetch_work_by_doi", return_value=None):
        result = check_coi(
            orcid="0000-0002-9876-5432",
            doi="10.9999/nonexistent",
        )
    assert result.is_coauthor is False
    assert result.error is not None
    assert "Could not fetch" in result.error


def test_check_coi_detects_first_author():
    """First author should have author_position=1."""
    with mock.patch(
        "scripts.check_coi.fetch_work_by_doi", return_value=MOCK_WORK_WITH_COAUTHOR
    ):
        result = check_coi(
            orcid="0000-0001-1234-5678",
            doi="10.1234/test-paper",
        )
    assert result.is_coauthor is True
    assert result.author_position == 1
    assert result.is_corresponding is False
