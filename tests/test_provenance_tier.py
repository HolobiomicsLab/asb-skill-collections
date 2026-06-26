import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import provenance_tier as p


def test_constants():
    assert p.VALID == {"literature", "synthetic", "community"}
    assert p.DEFAULT == "literature"


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
