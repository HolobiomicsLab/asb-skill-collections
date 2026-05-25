"""Unit tests for regen_career_stats.py."""
import json
import pathlib
import shutil
import pytest
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture()
def tmp_repo(tmp_path):
    """A minimal fake repo with contributors.jsonld and one review."""
    shutil.copy(FIXTURES / "mini_contributors.jsonld", tmp_path / "contributors.jsonld")
    # Create a collection with a reviews dir
    reviews_dir = tmp_path / "collections" / "metabolomics" / "v1" / "reviews"
    reviews_dir.mkdir(parents=True)
    shutil.copy(FIXTURES / "mini_review.yaml", reviews_dir / "10.1234_test-paper.yaml")
    (tmp_path / "leaderboard").mkdir(exist_ok=True)
    (tmp_path / "leaderboard" / "by-domain").mkdir(exist_ok=True)
    return tmp_path


def test_career_jsonld_is_created(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    career_path = tmp_repo / "leaderboard" / "career.jsonld"
    assert career_path.exists()


def test_career_jsonld_has_contributors(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    data = json.loads((tmp_repo / "leaderboard" / "career.jsonld").read_text())
    assert "contributors" in data
    assert len(data["contributors"]) == 2


def test_career_stats_has_required_fields(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    data = json.loads((tmp_repo / "leaderboard" / "career.jsonld").read_text())
    alice = next(c for c in data["contributors"] if c["github"] == "alice")
    # Required aggregated fields
    assert "total_reviews" in alice
    assert "lead_curator_of" in alice
    assert "curator_of" in alice
    assert "domain_contributor_of" in alice
    assert "reviewer_of" in alice
    assert "self_authored_percentage" in alice


def test_self_authored_percentage(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    data = json.loads((tmp_repo / "leaderboard" / "career.jsonld").read_text())
    alice = next(c for c in data["contributors"] if c["github"] == "alice")
    # Alice: 12 total, 2 self_authored => 2/12 = ~16.67%
    assert abs(alice["self_authored_percentage"] - (2 / 12 * 100)) < 0.01


def test_annual_jsonld_is_created(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    # At least the current year file should exist
    from datetime import datetime
    year = datetime.now().year
    annual_path = tmp_repo / "leaderboard" / f"annual-{year}.jsonld"
    assert annual_path.exists()


def test_by_domain_jsonld_is_created(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    domain_path = tmp_repo / "leaderboard" / "by-domain" / "metabolomics.jsonld"
    assert domain_path.exists()


def test_by_domain_lists_reviewers(tmp_repo):
    from scripts.regen_career_stats import regen_career_stats
    regen_career_stats(tmp_repo)
    data = json.loads(
        (tmp_repo / "leaderboard" / "by-domain" / "metabolomics.jsonld").read_text()
    )
    assert "contributors" in data
    assert len(data["contributors"]) >= 1
