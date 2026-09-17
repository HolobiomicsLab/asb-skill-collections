"""Advertised collection totals must follow their on-disk units."""

from __future__ import annotations

import pathlib
import subprocess
import sys

from scripts import check_advertised_counts as guard

REPO = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = REPO / "tests" / "fixtures" / "advertised_counts"


def test_matching_advertisements_pass_across_collection_surfaces():
    """The guard discovers a foreign-domain fixture without site allowlists."""
    claims, failures = guard.audit_repository(FIXTURES / "matching")

    assert failures == []
    assert {claim.kind for claim in claims} == {
        "entries",
        "papers",
        "skills",
        "tools",
        "workflows",
    }
    assert any(claim.site.name == "marketplace.json" for claim in claims)
    assert any(claim.site.name == "SKILL.md" for claim in claims)
    assert any(claim.site.name == "README.md" for claim in claims)
    assert any("techniques=radio" in claim.census_source for claim in claims)
    assert any("edam_topics=" in claim.census_source for claim in claims)


def test_stale_twin_exits_nonzero_and_lists_every_stale_site():
    """Independent stale metadata and prose sites are all named to the caller."""
    fixture = FIXTURES / "stale"
    result = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "check_advertised_counts.py"),
            "--repo-root",
            str(fixture),
        ],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "FAIL: 9 stale advertised count site(s)" in result.stdout
    expected_sites = {
        ".claude-plugin/marketplace.json:6",
        ".claude-plugin/marketplace.json:11",
        "collections/astronomy/v1/ABOUT.md:5",
        "collections/astronomy/v1/.claude-plugin/plugin.json:3",
        "collections/astronomy/v1/collection.yaml:8",
        "collections/astronomy/v1/corpus.yaml:3",
        "collections/astronomy/v1/corpus.yaml:4",
        "packs/astronomy/README.md:5",
    }
    assert all(site in result.stdout for site in expected_sites)
