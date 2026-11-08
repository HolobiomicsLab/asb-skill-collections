"""The release gate admits its declared repository and link-only access tiers."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import release_gate


def test_repo_oa_tiers_are_admitted():
    assert release_gate._REPO_OA_TIERS <= release_gate._NORMALIZED_OA_TIERS


def test_link_only_tiers_are_admitted():
    assert release_gate._LINK_ONLY_TIERS <= release_gate._NORMALIZED_OA_TIERS


def test_normalized_admission_covers_the_declared_tiers():
    declared = {
        release_gate._normalize_access_type(tier)
        for tier in release_gate._REPO_OA_TIERS | release_gate._LINK_ONLY_TIERS
    }
    assert declared <= release_gate._NORMALIZED_OA_TIERS


def test_repo_and_link_only_tiers_stay_distinct():
    assert release_gate._REPO_OA_TIERS.isdisjoint(release_gate._LINK_ONLY_TIERS)
    assert release_gate._LINK_ONLY_TIERS <= release_gate._CAPPED_VERBATIM_TIERS
    assert release_gate._REPO_OA_TIERS.isdisjoint(release_gate._CAPPED_VERBATIM_TIERS)
