"""Advertised collection totals must follow their on-disk units."""

from __future__ import annotations

import pathlib
import subprocess
import sys
import yaml

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


def _manifest_repository(tmp_path: pathlib.Path, skills: int = 30) -> pathlib.Path:
    collection = tmp_path / "collections" / "alpha" / "v2"
    (collection / "leaves" / "one").mkdir(parents=True)
    (collection / "leaves" / "two").mkdir()
    (collection / "tools").mkdir()
    (collection / "workflows" / "one").mkdir(parents=True)
    for path in collection.glob("leaves/*/"):
        (path / "SKILL.md").write_text("---\n---\n", encoding="utf-8")
    (collection / "tools" / "one.yaml").write_text("name: one\n", encoding="utf-8")
    (collection / "workflows" / "one" / "workflow.yaml").write_text(
        "name: one\n", encoding="utf-8"
    )
    (collection / "corpus.yaml").write_text(
        "papers: [{status: included}, {status: included}]\n", encoding="utf-8"
    )
    (collection / "collection.yaml").write_text(
        "slug: alpha\nversion: 2\n", encoding="utf-8"
    )
    marketplace = tmp_path / ".claude-plugin"
    marketplace.mkdir()
    (marketplace / "marketplace.json").write_text(
        '{"plugins":[{"name":"alpha","source":"./collections/alpha/v2"}]}',
        encoding="utf-8",
    )
    (tmp_path / "collections.yaml").write_text(
        yaml.safe_dump(
            {
                "domains": {
                    "alpha": {
                        "repository": "ExampleOrg/asb-skills-alpha",
                        "releases": [
                            {
                                "version": 2,
                                "path": "collections/alpha/v2",
                                "tag": None,
                                "version_doi": "10.5281/zenodo.123455",
                                "skills": 999,
                                "tools": 999,
                                "workflows": 999,
                                "papers": 999,
                            },
                            {
                                "version": 3,
                                "path": "collections/alpha/v3",
                                "tag": "alpha-v3.0.0",
                                "version_doi": "10.5281/zenodo.123456",
                                "skills": skills,
                                "tools": 4,
                                "workflows": 5,
                                "papers": 6,
                            }
                        ],
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text(
        f"""<a href=\"https://doi.org/10.5281/zenodo.123456\"><img src=\"https://img.shields.io/badge/skills-{skills}-blue\"></a>

# Domain release

The local v2 census has 2 skills.
The external v3 census has {skills} skills.
The badge release has {skills} skills.
""",
        encoding="utf-8",
    )
    return tmp_path


def test_manifest_release_claims_use_their_named_censuses(tmp_path):
    repo = _manifest_repository(tmp_path)

    claims, failures = guard.audit_repository(repo)

    assert failures == []
    root_claims = {
        claim.line: claim for claim in claims if claim.site == pathlib.Path("README.md")
    }
    assert root_claims[5].unit == pathlib.Path("collections/alpha/v2")
    assert root_claims[6].unit == pathlib.Path("collections/alpha/v3")
    assert root_claims[7].unit == pathlib.Path("collections/alpha/v3")


def test_wrong_manifest_release_count_is_a_finding(tmp_path):
    repo = _manifest_repository(tmp_path)
    readme = repo / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace(
            "The external v3 census has 30 skills.",
            "The external v3 census has 31 skills.",
        ),
        encoding="utf-8",
    )

    _, failures = guard.audit_repository(repo)

    assert len(failures) == 1
    assert failures[0].claim.unit == pathlib.Path("collections/alpha/v3")
    assert failures[0].claim.actual == 30


def test_badge_links_select_manifest_units_regardless_of_markup_order(tmp_path):
    repo = _manifest_repository(tmp_path)
    readme = repo / "README.md"
    readme.write_text(
        '[![30 skills](https://img.shields.io/badge/skills-30-blue)]'
        '(https://doi.org/10.5281/zenodo.123456)\n\n30 skills.\n',
        encoding="utf-8",
    )

    claims, failures = guard.audit_repository(repo)

    assert failures == []
    assert {
        claim.unit for claim in claims if claim.site == pathlib.Path("README.md")
    } == {pathlib.Path("collections/alpha/v3")}


def test_claims_follow_the_release_named_in_their_own_sentence(tmp_path):
    """One line naming two releases binds each count to its sentence's release."""
    repo = _manifest_repository(tmp_path)
    (repo / "README.md").write_text(
        '<a href="https://doi.org/10.5281/zenodo.123456">'
        '<img src="https://img.shields.io/badge/skills-30-blue"></a>\n'
        "\n# Domain release\n\n"
        "Collection v2 (2 skills, 1 tool) is the earlier collection; "
        "it is on main today. The marketplace lists v3 only, with 30 skills.\n",
        encoding="utf-8",
    )

    claims, failures = guard.audit_repository(repo)

    assert failures == []
    line_claims = {
        (claim.kind, claim.advertised): claim.unit
        for claim in claims
        if claim.site == pathlib.Path("README.md") and claim.line == 5
    }
    assert line_claims == {
        ("skills", 2): pathlib.Path("collections/alpha/v2"),
        ("tools", 1): pathlib.Path("collections/alpha/v2"),
        ("skills", 30): pathlib.Path("collections/alpha/v3"),
    }


def test_sentence_naming_an_unlisted_sibling_collection_is_censused_there(tmp_path):
    """A legacy tree beside the candidate is checked on disk, not against v2."""
    repo = _manifest_repository(tmp_path)
    legacy = repo / "collections" / "alpha" / "v1"
    (legacy / "skills" / "only").mkdir(parents=True)
    (legacy / "skills" / "only" / "SKILL.md").write_text("---\n---\n", encoding="utf-8")
    (legacy / "tools").mkdir()
    for name in ("a", "b", "c"):
        (legacy / "tools" / f"{name}.yaml").write_text(f"name: {name}\n", encoding="utf-8")
    (legacy / "collection.yaml").write_text("slug: alpha\nversion: 1\n", encoding="utf-8")
    (repo / "README.md").write_text(
        "# Domain release\n\n"
        "Collection v1 (1 skill, 3 tools) is the earlier flat-layout collection; "
        "it stays on main. The marketplace lists v2 only, with 2 skills.\n",
        encoding="utf-8",
    )

    claims, failures = guard.audit_repository(repo)

    assert failures == []
    line_claims = {
        (claim.kind, claim.advertised): claim.unit
        for claim in claims
        if claim.site == pathlib.Path("README.md") and claim.line == 3
    }
    assert line_claims == {
        ("skills", 1): pathlib.Path("collections/alpha/v1"),
        ("tools", 3): pathlib.Path("collections/alpha/v1"),
        ("skills", 2): pathlib.Path("collections/alpha/v2"),
    }
