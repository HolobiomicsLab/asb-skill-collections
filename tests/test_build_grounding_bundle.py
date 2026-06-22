"""Unit tests for build_grounding_bundle.py."""
import json, pathlib, sys
import pytest, yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
FIX = pathlib.Path(__file__).parent / "fixtures" / "mini_grounding"


def _corpus():
    return yaml.safe_load((FIX / "corpus.yaml").read_text())["papers"]

def _tools():
    return json.loads((FIX / "tools_index.json").read_text())


def test_resolve_repo_urls_merges_corpus_and_tools_dedup():
    from scripts.build_grounding_bundle import resolve_repo_urls
    urls = resolve_repo_urls(["10.1021/acs.jnatprod.7b00737"], _corpus(), _tools())
    assert urls == [
        "https://github.com/DorresteinLaboratory/Bioactive_Molecular_Networks",
        "https://github.com/CCMS-UCSD/GNPS_Workflows",
    ]

def test_resolve_repo_urls_drops_empty():
    from scripts.build_grounding_bundle import resolve_repo_urls
    assert resolve_repo_urls(["10.1000/norepo"], _corpus(), _tools()) == []

def test_filter_and_enrich_bundle():
    from scripts.build_grounding_bundle import filter_and_enrich_bundle
    full = json.loads((FIX / "kb_bundle.json").read_text())
    out = filter_and_enrich_bundle(full, {"bioactivity-score-aggregation", "norepo-skill"}, _corpus(), _tools())
    assert set(out["skills"]) == {"bioactivity-score-aggregation", "norepo-skill"}
    assert out["skills"]["bioactivity-score-aggregation"]["repo_urls"] == [
        "https://github.com/DorresteinLaboratory/Bioactive_Molecular_Networks",
        "https://github.com/CCMS-UCSD/GNPS_Workflows",
    ]
    assert out["skills"]["norepo-skill"]["repo_urls"] == []
    assert out["distinct_dois"] == ["10.1000/norepo", "10.1021/acs.jnatprod.7b00737"]
    assert out["kb_prefix"] == "asb-paper-"
