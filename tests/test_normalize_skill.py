import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from scripts import normalize_skill as n


# --- slugify -----------------------------------------------------------------

def test_slugify_lowercases_and_hyphenates():
    assert n.slugify("My New Skill") == "my-new-skill"


def test_slugify_strips_punctuation_and_collapses():
    assert n.slugify("LC-MS  Feature  Extraction!!") == "lc-ms-feature-extraction"


def test_slugify_trims_leading_trailing_separators():
    assert n.slugify("  --Adduct (M+H)+--  ") == "adduct-m-h"


# --- valid_edam --------------------------------------------------------------

def test_valid_edam_accepts_canonical_iri():
    assert n.valid_edam("http://edamontology.org/operation_3215") is True


def test_valid_edam_rejects_https_and_other_hosts():
    assert n.valid_edam("https://edamontology.org/operation_3215") is False
    assert n.valid_edam("http://example.org/operation_3215") is False
    assert n.valid_edam("operation_3215") is False
    assert n.valid_edam("") is False
    assert n.valid_edam(None) is False


# --- check_description -------------------------------------------------------

VALID_DESC = (
    "Use when you have a raw LC-MS feature table and need to filter blank "
    "contamination before downstream statistical analysis of metabolites."
)


def test_check_description_valid_returns_empty():
    assert n.check_description(VALID_DESC) == []


def test_check_description_each_allowed_prefix_ok():
    for prefix in ("Use when", "Reference for", "Explains", "Decision support for"):
        desc = prefix + " a representative situation that is long enough to clear the fifty character minimum bound."
        assert n.check_description(desc) == [], prefix


def test_check_description_bad_prefix_flagged():
    desc = "Helps you filter blank contamination from an LC-MS feature table prior to statistical analysis here."
    violations = n.check_description(desc)
    assert any("prefix" in v.lower() for v in violations)


def test_check_description_too_short_flagged():
    desc = "Use when filtering."  # < 50 chars
    violations = n.check_description(desc)
    assert any("50" in v or "short" in v.lower() for v in violations)


def test_check_description_too_long_flagged():
    desc = "Use when " + ("x" * 320)  # > 300 chars
    violations = n.check_description(desc)
    assert any("300" in v or "long" in v.lower() for v in violations)


def test_check_description_marketing_terms_flagged():
    for term in ("best", "state-of-the-art", "revolutionary", "leading", "superior"):
        desc = f"Use when you want the {term} approach to filter blank contamination from your LC-MS feature table."
        violations = n.check_description(desc)
        assert any("marketing" in v.lower() for v in violations), term


def test_check_description_marketing_substring_flagged_for_ci_parity():
    # CI Gate 5 uses substring matching (`term in desc.lower()`); the normalizer
    # must flag the SAME cases so a skill it pre-clears isn't later rejected by
    # CI. "bestowing" contains "best"; "misleading" contains "leading".
    for word, term in (("bestowing", "best"), ("misleading", "leading")):
        desc = (
            f"Use when {word} labels on an LC-MS feature table before downstream "
            "statistical analysis of the resulting metabolite features."
        )
        violations = n.check_description(desc)
        assert any("marketing" in v.lower() for v in violations), word
        assert any(term in v for v in violations), term


# --- parse_skill_md ----------------------------------------------------------

def test_parse_skill_md_splits_frontmatter_and_body():
    text = "---\nname: foo\ndescription: bar\n---\n# Title\n\nbody text\n"
    fm, body = n.parse_skill_md(text)
    assert fm == {"name": "foo", "description": "bar"}
    assert "body text" in body


def test_parse_skill_md_no_frontmatter_returns_none():
    fm, body = n.parse_skill_md("# Just a title\n\nbody\n")
    assert fm is None
    assert body is None


# --- frontmatter_violations --------------------------------------------------

def _good_fm():
    return {
        "name": "blank-contamination-filtering",
        "description": VALID_DESC,
        "metadata": {
            "edam_operation": "http://edamontology.org/operation_3215",
            "edam_topics": ["http://edamontology.org/topic_0091"],
            "license_tier": "open",
        },
    }


def test_frontmatter_violations_clean_is_empty():
    assert n.frontmatter_violations(_good_fm()) == []


def test_frontmatter_violations_bad_description():
    fm = _good_fm()
    fm["description"] = "Helps with stuff and is reasonably long but lacks an allowed prefix entirely here today."
    assert n.frontmatter_violations(fm)


def test_frontmatter_violations_bad_edam_operation():
    fm = _good_fm()
    fm["metadata"]["edam_operation"] = "https://edamontology.org/operation_3215"
    assert any("edam" in v.lower() for v in n.frontmatter_violations(fm))


def test_frontmatter_violations_bad_edam_topic():
    fm = _good_fm()
    fm["metadata"]["edam_topics"] = ["http://example.org/topic_0091"]
    assert any("edam" in v.lower() for v in n.frontmatter_violations(fm))


def test_frontmatter_violations_string_edam_topics_single_message():
    # A bare string instead of a list must yield ONE clear violation, not one
    # per character (contributor-supplied frontmatter robustness).
    fm = _good_fm()
    fm["metadata"]["edam_topics"] = "http://edamontology.org/topic_0091"
    violations = n.frontmatter_violations(fm)
    topic_violations = [v for v in violations if "edam_topics" in v or "topic IRI" in v]
    assert topic_violations == ["edam_topics must be a list"]


def test_frontmatter_violations_bad_license_tier():
    fm = _good_fm()
    fm["metadata"]["license_tier"] = "proprietary"
    assert any("license_tier" in v.lower() for v in n.frontmatter_violations(fm))


# --- normalized_frontmatter --------------------------------------------------

def test_normalized_frontmatter_sets_community_fields():
    raw = {
        "name": "blank-contamination-filtering",
        "description": VALID_DESC,
        "metadata": {
            "edam_operation": "http://edamontology.org/operation_3215",
            "edam_topics": ["http://edamontology.org/topic_0091"],
        },
    }
    fm = n.normalized_frontmatter(
        raw,
        related_skills=["lc-ms-feature-extraction"],
        tools_used=["mzmine"],
        license_tier="open",
    )
    assert fm["related_skills"] == ["lc-ms-feature-extraction"]
    assert fm["metadata"]["provenance_tier"] == "community"
    assert fm["metadata"]["license_tier"] == "open"
    assert fm["metadata"]["tools_used"] == ["mzmine"]
    assert fm["status"] == "hold"
    # preserves provided EDAM/description, does not fabricate
    assert fm["description"] == VALID_DESC
    assert fm["metadata"]["edam_operation"] == "http://edamontology.org/operation_3215"


def test_normalized_frontmatter_round_trips_through_yaml():
    raw = {
        "name": "blank-contamination-filtering",
        "description": VALID_DESC,
        "metadata": {
            "edam_operation": "http://edamontology.org/operation_3215",
            "edam_topics": ["http://edamontology.org/topic_0091"],
        },
    }
    fm = n.normalized_frontmatter(
        raw, related_skills=[], tools_used=[], license_tier="restricted"
    )
    dumped = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
    reloaded = yaml.safe_load(dumped)
    assert reloaded == fm
    # a community frontmatter with related_skills key present must pass the gate
    assert n.frontmatter_violations(fm) == []


def test_normalized_frontmatter_derived_from_optional():
    raw = {"name": "x", "description": VALID_DESC, "metadata": {}}
    without = n.normalized_frontmatter(
        raw, related_skills=[], tools_used=[], license_tier="open"
    )
    assert "derived_from" not in without
    with_df = n.normalized_frontmatter(
        raw,
        related_skills=[],
        tools_used=[],
        license_tier="open",
        derived_from=[{"doi": "10.1/x", "title": "T"}],
    )
    assert with_df["derived_from"] == [{"doi": "10.1/x", "title": "T"}]


def test_normalized_frontmatter_does_not_mutate_input():
    raw = {"name": "x", "description": VALID_DESC, "metadata": {"license_tier": "open"}}
    snapshot = {"name": "x", "description": VALID_DESC, "metadata": {"license_tier": "open"}}
    n.normalized_frontmatter(raw, related_skills=["a"], tools_used=["b"], license_tier="restricted")
    assert raw == snapshot


# --- contributors (co-authorship attribution) --------------------------------

def test_normalized_frontmatter_omits_contributors_when_none():
    raw = {"name": "x", "description": VALID_DESC, "metadata": {}}
    fm = n.normalized_frontmatter(
        raw, related_skills=[], tools_used=[], license_tier="open"
    )
    assert "contributors" not in fm


def test_normalized_frontmatter_emits_well_formed_contributors_block():
    raw = {"name": "x", "description": VALID_DESC, "metadata": {}}
    contributors = [
        {
            "name": "Ada Lovelace",
            "role": "author",
            "orcid": "0000-0002-1825-0097",
            "github": "ada",
        },
        {"name": "Grace Hopper", "role": "reviewer"},
    ]
    fm = n.normalized_frontmatter(
        raw,
        related_skills=[],
        tools_used=[],
        license_tier="open",
        contributors=contributors,
    )
    assert fm["contributors"] == [
        {
            "name": "Ada Lovelace",
            "role": "author",
            "orcid": "0000-0002-1825-0097",
            "github": "ada",
        },
        {"name": "Grace Hopper", "role": "reviewer"},
    ]
    # optional keys are dropped when absent (no orcid/github key on Grace)
    assert "orcid" not in fm["contributors"][1]
    assert "github" not in fm["contributors"][1]


def test_normalized_frontmatter_contributors_block_does_not_mutate_input():
    raw = {"name": "x", "description": VALID_DESC, "metadata": {}}
    contributors = [{"name": "Ada", "role": "author", "extra": "drop-me"}]
    snapshot = [{"name": "Ada", "role": "author", "extra": "drop-me"}]
    fm = n.normalized_frontmatter(
        raw,
        related_skills=[],
        tools_used=[],
        license_tier="open",
        contributors=contributors,
    )
    # input is not mutated; the emitted entry keeps only the well-formed keys
    assert contributors == snapshot
    assert fm["contributors"] == [{"name": "Ada", "role": "author"}]


def test_normalized_frontmatter_contributors_round_trips_through_yaml():
    raw = {
        "name": "blank-contamination-filtering",
        "description": VALID_DESC,
        "metadata": {
            "edam_operation": "http://edamontology.org/operation_3215",
            "edam_topics": ["http://edamontology.org/topic_0091"],
        },
    }
    fm = n.normalized_frontmatter(
        raw,
        related_skills=[],
        tools_used=[],
        license_tier="open",
        contributors=[{"name": "Ada Lovelace", "role": "author"}],
    )
    reloaded = yaml.safe_load(yaml.safe_dump(fm, sort_keys=False, allow_unicode=True))
    assert reloaded == fm
    # emitting a contributors block must not break the existing gate
    assert n.frontmatter_violations(fm) == []


# --- contributor_violations --------------------------------------------------

def test_contributor_violations_valid_returns_empty():
    contributors = [
        {"name": "Ada Lovelace", "role": "author", "orcid": "0000-0002-1825-0097"},
        {"name": "Grace Hopper", "role": "reviewer"},
        {"name": "Curator C", "role": "curator", "github": "cc"},
    ]
    assert n.contributor_violations(contributors) == []


def test_contributor_violations_absent_is_clean():
    # contributors is optional — absence (None) yields no violations.
    assert n.contributor_violations(None) == []


def test_contributor_violations_not_a_list_flagged():
    assert n.contributor_violations({"name": "Ada", "role": "author"})


def test_contributor_violations_entry_not_mapping_flagged():
    v = n.contributor_violations(["Ada Lovelace"])
    assert any("mapping" in x.lower() for x in v)


def test_contributor_violations_missing_name_flagged():
    v = n.contributor_violations([{"role": "author"}])
    assert any("name" in x.lower() for x in v)


def test_contributor_violations_empty_name_flagged():
    v = n.contributor_violations([{"name": "   ", "role": "author"}])
    assert any("name" in x.lower() for x in v)


def test_contributor_violations_missing_role_flagged():
    v = n.contributor_violations([{"name": "Ada"}])
    assert any("role" in x.lower() for x in v)


def test_contributor_violations_bad_role_flagged():
    v = n.contributor_violations([{"name": "Ada", "role": "maintainer"}])
    assert any("role" in x.lower() for x in v)


def test_contributor_violations_each_allowed_role_ok():
    for role in ("author", "reviewer", "curator"):
        assert n.contributor_violations([{"name": "X", "role": role}]) == [], role
