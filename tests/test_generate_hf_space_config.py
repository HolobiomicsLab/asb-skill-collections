"""Tests for generate_hf_space_config.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import generate_hf_space_config as gen


MINIMAL_COLLECTION = {
    "title": "Metabolomics Skills",
    "slug": "metabolomics",
    "version": 1,
    "domain": "metabolomics",
    "description": "Curated metabolomics skills.",
}

LEADERBOARD_URL = (
    "https://raw.githubusercontent.com/HolobiomicsLab/"
    "asb-skill-collections/main/collections/metabolomics/v1/benchmark/leaderboard.jsonld"
)


class TestGenerateSpaceConfig(unittest.TestCase):

    def test_space_readme_has_yaml_frontmatter(self):
        readme = gen.generate_space_readme(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert readme.startswith("---\n")
        assert "sdk: gradio" in readme
        assert "title:" in readme

    def test_space_readme_sdk_version(self):
        readme = gen.generate_space_readme(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "sdk_version:" in readme

    def test_space_readme_has_leaderboard_env(self):
        readme = gen.generate_space_readme(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "LEADERBOARD_URL" in readme

    def test_app_py_fetches_leaderboard_url(self):
        app_py = gen.generate_app_py(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "LEADERBOARD_URL" in app_py
        assert "requests" in app_py
        assert "gradio" in app_py or "gr" in app_py

    def test_app_py_renders_sortable_table(self):
        app_py = gen.generate_app_py(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        # Must have a DataFrame or table component
        assert "DataFrame" in app_py or "dataframe" in app_py.lower()

    def test_app_py_has_result_type_filter(self):
        app_py = gen.generate_app_py(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "result_type" in app_py

    def test_app_py_has_submit_button(self):
        app_py = gen.generate_app_py(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "Submit" in app_py or "submit" in app_py.lower()

    def test_app_py_submit_opens_github_issue(self):
        app_py = gen.generate_app_py(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "github.com" in app_py
        assert "issues" in app_py.lower() or "new" in app_py.lower()

    def test_generate_space_config_returns_both(self):
        result = gen.generate_space_config(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "readme" in result
        assert "app_py" in result
        assert isinstance(result["readme"], str)
        assert isinstance(result["app_py"], str)

    def test_space_title_includes_collection_title(self):
        readme = gen.generate_space_readme(
            collection=MINIMAL_COLLECTION,
            leaderboard_url=LEADERBOARD_URL,
        )
        assert "Metabolomics" in readme


if __name__ == "__main__":
    unittest.main()
