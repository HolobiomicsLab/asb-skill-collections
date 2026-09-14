"""A skill with no papers keeps its own repository in a derived unit bundle.

`resolve_repo_urls` exists to stop a skill being handed another paper's repository
(issue #42). Derived from DOIs alone it also erases the repository of a skill that
has no DOIs — whose `repo_urls` is its own source, not somebody else's. The
collection carries one such skill today (`masster`, `provenance_tier: repository`),
and the pack derived from it shipped an empty grounding map for it.
"""
import json
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

FIX = pathlib.Path(__file__).parent / "fixtures" / "mini_grounding"


def _corpus():
    return yaml.safe_load((FIX / "corpus.yaml").read_text())["papers"]


def test_paperless_skill_keeps_its_declared_repository():
    from scripts.build_grounding_bundle import resolve_repo_urls

    assert resolve_repo_urls([], _corpus(), ["zamboni-lab/masster-dist"]) == [
        "https://github.com/zamboni-lab/masster-dist",
    ]


def test_paperless_skill_with_nothing_declared_stays_empty():
    from scripts.build_grounding_bundle import resolve_repo_urls

    assert resolve_repo_urls([], _corpus(), None) == []
    assert resolve_repo_urls([], _corpus(), [""]) == []


def test_a_papered_skill_is_still_re_derived_not_trusted():
    """The declared list is used only where there is nothing to derive from."""
    from scripts.build_grounding_bundle import resolve_repo_urls

    urls = resolve_repo_urls(
        ["10.1021/acs.jnatprod.7b00737"],
        _corpus(),
        ["https://github.com/someone/else"],
    )
    assert urls == ["https://github.com/DorresteinLaboratory/Bioactive_Molecular_Networks"]


def test_filter_and_enrich_keeps_a_paperless_records_repository():
    from scripts.build_grounding_bundle import filter_and_enrich_bundle

    full = json.loads((FIX / "kb_bundle.json").read_text())
    full["skills"]["toolonly-skill"] = {
        "dois": [],
        "tools": ["Masster"],
        "kb_slugs": [],
        "provenance_tier": "repository",
        "repo_urls": ["https://github.com/zamboni-lab/masster-dist"],
    }
    out = filter_and_enrich_bundle(full, {"toolonly-skill", "norepo-skill"}, _corpus())
    assert out["skills"]["toolonly-skill"]["repo_urls"] == [
        "https://github.com/zamboni-lab/masster-dist",
    ]
    # a skill whose paper simply has no repository still resolves to nothing
    assert out["skills"]["norepo-skill"]["repo_urls"] == []
