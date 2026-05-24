"""Unit tests for vet_curator.py with mocked OpenAlex + ORCID API responses."""
import pathlib
import tempfile
import unittest.mock as mock

import yaml

from scripts.vet_curator import (
    check_l1_github_in_orcid,
    check_l2_orcid_on_publications,
    vet_curator,
)


# -- fixtures ----------------------------------------------------------------

MOCK_ORCID_PERSON_WITH_GITHUB = {
    "researcher-urls": {
        "researcher-url": [
            {
                "url": {"value": "https://github.com/testuser"},
                "url-name": "GitHub",
            }
        ]
    }
}

MOCK_ORCID_PERSON_WITHOUT_GITHUB = {
    "researcher-urls": {
        "researcher-url": [
            {
                "url": {"value": "https://twitter.com/testuser"},
                "url-name": "Twitter",
            }
        ]
    }
}

MOCK_WORK_WITH_ORCID = {
    "id": "https://openalex.org/W1111",
    "authorships": [
        {
            "author": {
                "orcid": "https://orcid.org/0000-0001-2345-6789",
                "display_name": "Test Candidate",
            },
            "is_corresponding": False,
        }
    ],
}

MOCK_WORK_WITHOUT_ORCID = {
    "id": "https://openalex.org/W2222",
    "authorships": [
        {
            "author": {
                "orcid": "https://orcid.org/0000-0009-9999-9999",
                "display_name": "Other Person",
            },
            "is_corresponding": False,
        }
    ],
}


# -- L1 tests ----------------------------------------------------------------


def test_l1_pass_when_github_in_orcid():
    with mock.patch(
        "scripts.vet_curator._get_json", return_value=MOCK_ORCID_PERSON_WITH_GITHUB
    ):
        assert check_l1_github_in_orcid("testuser", "0000-0001-2345-6789") is True


def test_l1_fail_when_github_not_in_orcid():
    with mock.patch(
        "scripts.vet_curator._get_json",
        return_value=MOCK_ORCID_PERSON_WITHOUT_GITHUB,
    ):
        assert check_l1_github_in_orcid("testuser", "0000-0001-2345-6789") is False


def test_l1_fail_when_api_unreachable():
    with mock.patch("scripts.vet_curator._get_json", return_value=None):
        assert check_l1_github_in_orcid("testuser", "0000-0001-2345-6789") is False


# -- L2 tests ----------------------------------------------------------------


def test_l2_found_when_orcid_matches():
    with mock.patch(
        "scripts.vet_curator._get_json", return_value=MOCK_WORK_WITH_ORCID
    ):
        results = check_l2_orcid_on_publications(
            "0000-0001-2345-6789", ["10.1234/paper-1"]
        )
    assert results[0]["found"] is True


def test_l2_not_found_when_orcid_mismatch():
    with mock.patch(
        "scripts.vet_curator._get_json", return_value=MOCK_WORK_WITHOUT_ORCID
    ):
        results = check_l2_orcid_on_publications(
            "0000-0001-2345-6789", ["10.1234/paper-1"]
        )
    assert results[0]["found"] is False


def test_l2_handles_api_failure():
    with mock.patch("scripts.vet_curator._get_json", return_value=None):
        results = check_l2_orcid_on_publications(
            "0000-0001-2345-6789", ["10.1234/unreachable"]
        )
    assert results[0]["found"] is False
    assert "API failure" in results[0]["error"]


# -- end-to-end vet_curator tests --------------------------------------------


def _write_candidate(tmpdir: str, data: dict) -> pathlib.Path:
    p = pathlib.Path(tmpdir) / "testuser.yaml"
    p.write_text(yaml.dump(data))
    return p


def test_vet_curator_full_pass():
    """Candidate with L1+L2 pass should get reviewer, domain_contributor, curator tiers."""
    candidate_data = {
        "github": "testuser",
        "orcid": "0000-0001-2345-6789",
        "intended_collections": ["metabolomics"],
        "proof_publications": [
            {"doi": "10.1234/paper-1"},
            {"doi": "10.1234/paper-2"},
        ],
    }

    def side_effect(url):
        if "orcid.org" in url:
            return MOCK_ORCID_PERSON_WITH_GITHUB
        return MOCK_WORK_WITH_ORCID

    with tempfile.TemporaryDirectory() as tmpdir:
        candidate_path = _write_candidate(tmpdir, candidate_data)
        with mock.patch("scripts.vet_curator._get_json", side_effect=side_effect):
            result = vet_curator(candidate_path)

    assert result.l1_pass is True
    assert result.l2_pass is True
    assert "reviewer" in result.eligible_tiers
    assert "curator" in result.eligible_tiers
    assert result.errors == []


def test_vet_curator_l1_fail():
    """Candidate without GitHub URL in ORCID should have empty eligible_tiers."""
    candidate_data = {
        "github": "testuser",
        "orcid": "0000-0001-2345-6789",
        "intended_collections": ["metabolomics"],
        "proof_publications": [
            {"doi": "10.1234/paper-1"},
            {"doi": "10.1234/paper-2"},
        ],
    }

    def side_effect(url):
        if "orcid.org" in url:
            return MOCK_ORCID_PERSON_WITHOUT_GITHUB
        return MOCK_WORK_WITH_ORCID

    with tempfile.TemporaryDirectory() as tmpdir:
        candidate_path = _write_candidate(tmpdir, candidate_data)
        with mock.patch("scripts.vet_curator._get_json", side_effect=side_effect):
            result = vet_curator(candidate_path)

    assert result.l1_pass is False
    assert "reviewer" not in result.eligible_tiers
    assert len(result.errors) > 0
