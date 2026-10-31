"""Regression coverage for the explicit unknown licence tier."""

from scripts import propagate_license_tiers as propagation


def test_noncommercial_governs_unknown_and_noncommercial_dois():
    tiers = {
        "10.1/unknown": {"tier": "unknown"},
        "10.1/noncommercial": {"tier": "noncommercial"},
    }

    assert (
        propagation.skill_tier(
            ["10.1/unknown", "10.1/noncommercial"], tiers
        )
        == "noncommercial"
    )


def test_unknown_is_preserved_when_it_is_the_only_known_tier():
    tiers = {"10.1/unknown": {"tier": "unknown"}}

    assert propagation.skill_tier(["10.1/unknown"], tiers) == "unknown"
