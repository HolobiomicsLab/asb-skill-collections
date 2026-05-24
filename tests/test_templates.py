"""YAML parse + schema conformance tests for template files."""
import pathlib
import yaml

ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_DIR = ROOT / "templates"


def _load_yaml_template(name: str) -> dict:
    """Load a .yaml.template by stripping Jinja-style placeholders and parsing."""
    content = (TEMPLATES_DIR / name).read_text()
    # Replace Jinja-style {{ }} placeholders with dummy values for parse test
    content = (
        content
        .replace("{{COLLECTION_TITLE}}", "Test")
        .replace("{{VERSION}}", "1")
        .replace("{{VERSION_NEXT}}", "2")
        .replace("{{CURATOR_NAME}}", "Test Curator")
        .replace("{{ORCID}}", "0000-0000-0000-0000")
        .replace("{{COLLECTION_SLUG}}", "test")
        .replace("{{DATE}}", "2026-01-01")
        .replace("{{DOMAIN}}", "test domain")
    )
    return yaml.safe_load(content)


def test_curator_criteria_template_parseable():
    data = _load_yaml_template("curator-criteria.yaml.template")
    assert "domain_concepts" in data
    assert "primary" in data["domain_concepts"]
    assert "thresholds" in data
    assert "lead_curator" in data["thresholds"]


def test_curator_criteria_template_has_required_threshold_fields():
    data = _load_yaml_template("curator-criteria.yaml.template")
    lead = data["thresholds"]["lead_curator"]
    assert "min_reviews" in lead
    assert "min_external_reviews" in lead
    assert "min_pubs" in lead
    assert "min_h_index" in lead
    assert "identity_layers" in lead
    assert lead["min_reviews"] == 30
    assert lead["min_external_reviews"] == 20


def test_attestation_template_parseable():
    data = _load_yaml_template("attestation.yaml.template")
    assert "reviewer" in data
    assert "paper" in data
    assert "is_coauthor" in data
    assert "verified_claim_ids" in data
    assert isinstance(data["verified_claim_ids"], list)


def test_attestation_template_has_coi_fields():
    data = _load_yaml_template("attestation.yaml.template")
    assert "is_coauthor" in data
    assert "author_position" in data
    assert "is_corresponding" in data
    assert data["is_coauthor"] is False


def test_attestation_template_has_verified_claim_ids_slot():
    """Gold-tier claim verification slot must exist per section 10.4."""
    data = _load_yaml_template("attestation.yaml.template")
    assert "verified_claim_ids" in data
    assert data["verified_claim_ids"] == []
