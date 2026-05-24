"""Schema conformance tests for contributors.jsonld."""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent.parent


def test_contributors_jsonld_parseable():
    data = json.loads((ROOT / "contributors.jsonld").read_text())
    assert "@context" in data
    assert "contributors" in data
    assert isinstance(data["contributors"], list)


def test_contributors_jsonld_has_required_context_keys():
    data = json.loads((ROOT / "contributors.jsonld").read_text())
    ctx = data["@context"]
    assert "@vocab" in ctx
    assert "orcid" in ctx
    assert "asb:tier" in ctx
    assert "asb:total_reviews" in ctx
    assert "asb:external_reviews" in ctx
    assert "asb:self_authored_reviews" in ctx
