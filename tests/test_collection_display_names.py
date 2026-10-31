"""One display name per domain, carried by every metadata file of a collection.

The collector title-cased the domain slug, so agentic-ai became "ASB Agentic Ai"
and multi-omics "ASB Multi Omics" in collection.yaml and plugin.json, while
README, CITATION and .zenodo.json spelled the domain otherwise. The display
name now comes from one map in the collector, and the collection title built
from it is the one collection.yaml, plugin.json and CITATION.cff carry
(land_candidate.py copies it into .zenodo.json and the marketplace entry).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts import collect_from_cut as collector


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs"
CREATORS = REPO / "scripts" / "release_creators.yaml"


@pytest.mark.parametrize(
    ("domain", "expected"),
    [
        ("agentic-ai", "ASB Agentic AI"),
        ("multi-omics", "ASB Multi-Omics"),
        ("astronomy", "ASB Astronomy"),
        ("metabarcoding", "ASB Metabarcoding"),
    ],
)
def test_display_name(domain: str, expected: str) -> None:
    assert f"ASB {collector.display_name(domain)}" == expected
    assert collector.collection_title(domain, "v1") == f"{expected} Skill Collection v1"


@pytest.mark.parametrize("domain", ["agentic-ai", "multi-omics", "astronomy"])
def test_one_title_across_collection_plugin_and_citation(
    tmp_path: Path, domain: str
) -> None:
    candidate = tmp_path / "candidate"
    code = collector.main(
        [
            "--cut",
            str(FIXTURE / "corpus"),
            "--domain",
            domain,
            "--version",
            "v1",
            "--out",
            str(candidate),
            "--license",
            "CC-BY-4.0",
            "--plugin-repo",
            f"https://github.com/HolobiomicsLab/asb-skills-{domain}",
            "--creators",
            str(CREATORS),
            "--corpus",
            str(FIXTURE / "corpus.yaml"),
            "--receipts",
            str(tmp_path / "receipts"),
        ]
    )
    assert code == 0
    title = collector.collection_title(domain, "v1")
    prefix = f"ASB {collector.display_name(domain)}: "

    descriptor = yaml.safe_load((candidate / "collection.yaml").read_text("utf-8"))
    plugin = json.loads((candidate / ".claude-plugin" / "plugin.json").read_text("utf-8"))
    citation = yaml.safe_load((candidate / "CITATION.cff").read_text("utf-8"))

    assert descriptor["title"] == title
    assert citation["title"] == title
    assert descriptor["description"].startswith(prefix)
    assert plugin["description"].startswith(prefix)
    assert citation["abstract"].startswith(prefix)
