"""
Schema-contract tests binding the review-attestation template to the CI
workflows that parse it.

There is ONE canonical schema for a review attestation, defined by
``templates/attestation.yaml.template``:

    reviewer.orcid   -- nested under `reviewer`   (required)
    paper.doi        -- nested under `paper`       (required)
    is_coauthor      -- TOP-LEVEL key              (required)
    co_reviewer      -- TOP-LEVEL key              (optional; absent unless COI)

``.github/workflows/verify-coi.yml`` and ``.github/workflows/tier-update.yml``
read these fields with inline ``python -c`` snippets. Historically those
snippets drifted from the template -- reading ``d['paper_doi']`` and
``d['reviewer']['is_coauthor']`` -- which silently broke every COI/tier run
because the template never produced those paths.

These tests lock both sides together:

  * the template must expose every field the workflows read (so a filled-in
    attestation actually resolves), and
  * the workflow files must use the canonical accessors (so a future edit
    can't reintroduce the wrong path without a test failing).

If a test here fails, do NOT loosen it -- reconcile the template and the
workflows onto the canonical schema above.
"""
import pathlib

import yaml

ROOT = pathlib.Path(__file__).parent.parent
TEMPLATE = ROOT / "templates" / "attestation.yaml.template"
VERIFY_COI = ROOT / ".github" / "workflows" / "verify-coi.yml"
TIER_UPDATE = ROOT / ".github" / "workflows" / "tier-update.yml"


def load_attestation_template() -> dict:
    """Parse the blank attestation template (it has no Jinja placeholders)."""
    return yaml.safe_load(TEMPLATE.read_text())


# -- Field paths the workflows read from a filled-in attestation -------------
# Each accessor MUST evaluate without KeyError/TypeError against the template.
# Keep this list in lock-step with the `python -c` snippets in the workflows
# named under `where`.
REQUIRED_READS = [
    ("reviewer.orcid", lambda d: d["reviewer"]["orcid"],
     "verify-coi.yml, tier-update.yml"),
    ("paper.doi", lambda d: d["paper"]["doi"], "verify-coi.yml"),
    ("is_coauthor (top-level)", lambda d: d["is_coauthor"],
     "verify-coi.yml, tier-update.yml"),
]

# Optional reads: accessed via `.get` on the top-level dict, so they resolve
# to None in the blank template (the "no COI declared" case).
OPTIONAL_READS = [
    ("co_reviewer (top-level)", lambda d: d.get("co_reviewer"), "verify-coi.yml"),
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


def test_workflows_do_not_use_drifted_accessors():
    for wf in (VERIFY_COI, TIER_UPDATE):
        text = wf.read_text()
        for bad in FORBIDDEN_ACCESSORS:
            assert bad not in text, (
                f"{wf.name} uses non-canonical accessor {bad!r}; "
                f"reconcile with templates/attestation.yaml.template"
            )


def test_workflows_use_canonical_accessors():
    verify = VERIFY_COI.read_text()
    tier = TIER_UPDATE.read_text()
    assert "d['paper']['doi']" in verify, (
        "verify-coi.yml must read paper.doi as d['paper']['doi']"
    )
    assert "d.get('is_coauthor'" in verify, (
        "verify-coi.yml must read top-level is_coauthor as d.get('is_coauthor', ...)"
    )
    assert "d.get('is_coauthor')" in tier, (
        "tier-update.yml must read top-level is_coauthor as d.get('is_coauthor')"
    )
