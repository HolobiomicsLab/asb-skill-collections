"""Tests for generate_hf_dataset_card.py"""
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import generate_hf_dataset_card as gen


MINIMAL_COLLECTION_YAML = """
title: "Metabolomics Skills"
slug: metabolomics
version: 1
domain: metabolomics
description: "Curated metabolomics skills for scientific AI agents."
"""

MINIMAL_CITATION_CFF = """
cff-version: 1.2.0
title: "ASB Metabolomics v1"
doi: "10.5281/zenodo.12345"
authors:
  - family-names: Nothias
    given-names: Louis-Felix
    orcid: https://orcid.org/0000-0001-6191-3389
"""


class TestGenerateDatasetCard(unittest.TestCase):

    def test_minimal_collection_yaml_only(self):
        """generate_readme from collection.yaml only, no CITATION.cff"""
        result = gen.generate_readme(
            collection=gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML),
            citation=None,
        )
        assert "license: apache-2.0" in result
        assert "agentic-ai" in result
        assert "metabolomics" in result
        assert "ASB Metabolomics Skills Benchmark v1" in result
        assert "config_name: skills" in result
        assert "config_name: benchmark" in result
        assert "config_name: tools" in result
        assert "PLACEHOLDER" in result  # no doi without CITATION.cff

    def test_with_citation_cff(self):
        """DOI from CITATION.cff appears in frontmatter"""
        result = gen.generate_readme(
            collection=gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML),
            citation=gen.parse_citation_cff(MINIMAL_CITATION_CFF),
        )
        assert "10.5281/zenodo.12345" in result
        assert "PLACEHOLDER" not in result

    def test_tags_include_domain_and_asb(self):
        collection = gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML)
        result = gen.generate_readme(collection=collection, citation=None)
        assert "scientific-agents" in result
        assert "asb" in result

    def test_pretty_name_format(self):
        collection = gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML)
        result = gen.generate_readme(collection=collection, citation=None)
        assert 'pretty_name: "ASB Metabolomics Skills Benchmark v1"' in result

    def test_parse_collection_yaml_missing_required_key(self):
        """Missing required key raises ValueError"""
        with self.assertRaises(ValueError):
            gen.parse_collection_yaml("title: Test\n")  # missing slug, version, domain

    def test_configs_data_files(self):
        collection = gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML)
        result = gen.generate_readme(collection=collection, citation=None)
        assert 'data_files: "skills/**/SKILL.md"' in result
        assert 'data_files: "benchmark/tasks/**/task.md"' in result
        assert 'data_files: "tools/**/*.yaml"' in result

    def test_body_contains_description(self):
        collection = gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML)
        result = gen.generate_readme(collection=collection, citation=None)
        assert "Curated metabolomics skills" in result

    def test_generate_readme_returns_string(self):
        collection = gen.parse_collection_yaml(MINIMAL_COLLECTION_YAML)
        result = gen.generate_readme(collection=collection, citation=None)
        assert isinstance(result, str)
        assert result.startswith("---\n")


if __name__ == "__main__":
    unittest.main()
