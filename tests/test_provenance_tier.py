import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import provenance_tier as p


def test_constants():
    # `repository` joined the vocabulary on 2026-08-20: a skill taken from an
    # open source tool with no paper behind it fitted none of the other three,
    # so its origin went unrecorded and the gate reported it as invalid.
    assert p.VALID == {"literature", "repository", "synthetic", "community"}
    assert p.DEFAULT == "literature"
    assert p.REPOSITORY == "repository"


# --- one valid case per tier ------------------------------------------------

def test_literature_valid_with_doi():
    assert p.validate_entry("literature", dois=["10.1/a"]) == []


def test_synthetic_valid_with_synthesized_from():
    assert p.validate_entry("synthetic", synthesized_from=["s1", "s2"]) == []


def test_community_valid_with_related_skills_present():
    # an empty related_skills list is allowed (the key is present)
    assert p.validate_entry("community", related_skills=[]) == []
    assert p.validate_entry("community", related_skills=["s1"]) == []


# --- failure cases ----------------------------------------------------------

def test_unknown_tier():
    assert p.validate_entry("bogus", dois=["10.1/a"]) == [
        "invalid provenance_tier 'bogus'"
    ]


def test_literature_without_doi():
    assert p.validate_entry("literature") == ["literature requires >=1 doi"]
    assert p.validate_entry("literature", dois=[]) == ["literature requires >=1 doi"]
    assert p.validate_entry("literature", dois=None) == ["literature requires >=1 doi"]


def test_synthetic_without_synthesized_from():
    assert p.validate_entry("synthetic") == ["synthetic requires synthesized_from"]
    assert p.validate_entry("synthetic", synthesized_from=[]) == [
        "synthetic requires synthesized_from"
    ]
    assert p.validate_entry("synthetic", synthesized_from=None) == [
        "synthetic requires synthesized_from"
    ]


def test_community_without_related_skills_key():
    # None means the key is absent → violation
    assert p.validate_entry("community") == ["community requires related_skills key"]
    assert p.validate_entry("community", related_skills=None) == [
        "community requires related_skills key"
    ]


# --- repository: an origin the first three tiers could not express -----------

def test_repository_requires_a_repo_url():
    """Its evidence, exactly as `literature` requires a doi. Without one the
    tier is an unbacked claim about where the content came from."""
    assert p.validate_entry("repository") == ["repository requires repo_url"]
    assert p.validate_entry("repository", repo_url="   ") == ["repository requires repo_url"]


def test_repository_with_a_repo_url_is_valid():
    assert p.validate_entry("repository", repo_url="https://github.com/a/b") == []


def test_repository_does_not_need_a_doi():
    """The whole point: this is the tier for a tool with no paper behind it."""
    assert p.validate_entry("repository", dois=[], repo_url="https://github.com/a/b") == []


def test_a_repo_url_does_not_excuse_a_missing_doi_on_literature():
    """The other side. Adding a tier must not weaken the ones beside it."""
    assert p.validate_entry("literature", dois=[], repo_url="https://github.com/a/b") == [
        "literature requires >=1 doi"]
