"""Keyword fallback favours requested method roles over incidental plumbing."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from asb_skill_collections import asb_skill_index as index


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "collections" / "metabolomics" / "v2" / "bin" / "search_skills.py"


@pytest.fixture
def ranking_rows() -> list[dict]:
    """Return a dozen role and plumbing leaves with realistic field overlap."""
    rows = [
        {
            "slug": "formula-candidate-ranking",
            "name": "Molecular formula candidate ranking",
            "description": "Rank molecular formula candidates from MS/MS evidence.",
            "tools": ["SIRIUS"],
        },
        {
            "slug": "zodiac-parameter-configuration",
            "name": "Parameter configuration",
            "description": "Parse a configuration file and toggle parameters for a request.",
            "tools": ["ZODIAC"],
        },
        {
            "slug": "gnps-submission-export",
            "name": "GNPS submission file export",
            "description": "Export an MGF file and build a GNPS submission request.",
            "tools": ["GNPS"],
        },
    ]
    rows.extend(
        {
            "slug": f"decoy-{number}",
            "name": f"Unrelated method {number}",
            "description": "Measure a distinct analytical outcome.",
            "tools": [f"Tool{number}"],
        }
        for number in range(1, 10)
    )
    assert len(rows) == 12
    return rows


def test_role_fields_outweigh_tool_only_plumbing(ranking_rows):
    hits = index.keyword_search(
        ranking_rows,
        "ZODIAC candidate ranking",
        k=5,
    )

    assert hits[0]["slug"] == "formula-candidate-ranking"


def test_requested_plumbing_is_not_deboosted(ranking_rows):
    hits = index.keyword_search(
        ranking_rows,
        "export an MGF submission file for GNPS",
        k=5,
    )

    assert hits[0]["slug"] == "gnps-submission-export"


@pytest.fixture
def script_module():
    """Load the released wrapper without invoking a subprocess."""
    spec = importlib.util.spec_from_file_location("ranking_search_script", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_keyword_cli_names_the_semantic_fallback_once(script_module, capsys):
    assert script_module.main([
        "--collection", str(SCRIPT.parent.parent),
        "--query", "molecular formula ranking", "-k", "1", "--json",
    ]) == 0

    lines = capsys.readouterr().err.splitlines()
    assert lines == [
        "keyword ranking is the offline fallback; prefer semantic ranking with "
        "bin/semantic_search.py --mode auto"
    ]


def test_quiet_suppresses_keyword_fallback_notice(script_module, capsys):
    assert script_module.main([
        "--collection", str(SCRIPT.parent.parent),
        "--query", "molecular formula ranking", "-k", "1", "--json", "--quiet",
    ]) == 0

    assert capsys.readouterr().err == ""
