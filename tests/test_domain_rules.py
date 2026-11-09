"""Per-domain rule resolution and explicit override contracts."""

import pytest

from scripts.domain_rules import DomainRulesError, collection_domain, domain_rules_path, resolve_rules_path


def test_domain_found_from_collection_slug(tmp_path):
    collection = tmp_path / "collection"
    collection.mkdir()
    (collection / "collection.yaml").write_text("slug: metabolomics\n", encoding="utf-8")

    assert collection_domain(collection) == "metabolomics"
    assert domain_rules_path(collection, "technique_rules.yaml").name == "technique_rules.yaml"
    assert resolve_rules_path(collection, "technique_rules.yaml").is_file()


def test_domain_without_rules_names_expected_path(tmp_path):
    collection = tmp_path / "collection"
    collection.mkdir()
    (collection / "collection.yaml").write_text("domain: astronomy\n", encoding="utf-8")

    with pytest.raises(DomainRulesError, match="scripts/rules/astronomy/technique_rules.yaml"):
        resolve_rules_path(collection, "technique_rules.yaml")


def test_explicit_rules_override_domain(tmp_path):
    collection = tmp_path / "collection"
    collection.mkdir()
    (collection / "collection.yaml").write_text("slug: astronomy\n", encoding="utf-8")
    explicit = tmp_path / "custom.yaml"
    explicit.write_text("rules_version: test\n", encoding="utf-8")

    assert resolve_rules_path(collection, "technique_rules.yaml", explicit) == explicit
