"""
Schema-contract tests for the canonical review-attestation template.

There is ONE canonical schema for a review attestation, defined by
``templates/attestation.yaml.template``:

    reviewer.orcid   -- nested under `reviewer`   (required)
    paper.doi        -- nested under `paper`       (required)
    is_coauthor      -- TOP-LEVEL key              (required)
    co_reviewer      -- TOP-LEVEL key              (optional; absent unless COI)

The template must expose the canonical field paths even though the content
workflows that consume them now live in the domain repositories.
"""
import pathlib

import yaml

ROOT = pathlib.Path(__file__).parent.parent
TEMPLATE = ROOT / "templates" / "attestation.yaml.template"


def load_attestation_template() -> dict:
    """Parse the blank attestation template (it has no Jinja placeholders)."""
    return yaml.safe_load(TEMPLATE.read_text())


# -- Canonical field paths of a filled-in attestation -------------------------
# Each accessor MUST evaluate without KeyError/TypeError against the template.
REQUIRED_READS = [
    ("reviewer.orcid", lambda d: d["reviewer"]["orcid"], "reviewer identity"),
    ("paper.doi", lambda d: d["paper"]["doi"], "paper identity"),
    ("is_coauthor (top-level)", lambda d: d["is_coauthor"], "conflict declaration"),
]

# Optional reads: accessed via `.get` on the top-level dict, so they resolve
# to None in the blank template (the "no COI declared" case).
OPTIONAL_READS = [
    ("co_reviewer (top-level)", lambda d: d.get("co_reviewer"), "conflict declaration"),
]


def test_every_required_workflow_field_resolves():
    data = load_attestation_template()
    for label, read, where in REQUIRED_READS:
        try:
            read(data)
        except (KeyError, TypeError) as exc:
            raise AssertionError(
                f"attestation template is missing a field read by CI "
                f"({where}): {label} -- {exc!r}"
            ) from exc


def test_optional_workflow_reads_use_correct_access_pattern():
    data = load_attestation_template()
    for label, read, _where in OPTIONAL_READS:
        # Must not raise; commented-out in the blank template -> None.
        assert read(data) is None, (
            f"{label} should be absent (None) in the blank template"
        )


def test_is_coauthor_is_top_level_not_nested_under_reviewer():
    """Guards the historical drift: d['reviewer']['is_coauthor']."""
    data = load_attestation_template()
    assert "is_coauthor" in data, "is_coauthor must be a TOP-LEVEL key"
    assert "is_coauthor" not in data["reviewer"], (
        "is_coauthor must NOT be nested under `reviewer` (canonical schema)"
    )


def test_paper_doi_is_nested_not_top_level():
    """Guards the historical drift: d['paper_doi']."""
    data = load_attestation_template()
    assert "paper_doi" not in data, (
        "use nested paper.doi, not a top-level paper_doi key"
    )
    assert "doi" in data["paper"], "paper.doi must exist (nested under `paper`)"


# -- Workflow side: forbid the known-bad accessors from creeping back --------
# Substrings that must NOT appear in either workflow file.
FORBIDDEN_ACCESSORS = [
    "d['paper_doi']",                       # paper.doi is nested, not top-level
    "d['reviewer']['is_coauthor']",         # is_coauthor is top-level
    "d['reviewer'].get('is_coauthor'",      # is_coauthor is top-level
]
