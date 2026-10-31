"""Metabolomics v2 and its packs never call their sources peer-reviewed.

78 of the 566 v2 corpus papers are bioRxiv, arXiv or ChemRxiv preprints or
Zenodo deposits, yet the plugin manifest, the marketplace entry, ABOUT.md,
USAGE.md, .zenodo.json, GROUNDING.md and the routers said every skill was
derived from a peer-reviewed method paper. They now say "a method paper
(journal article or preprint) and its code", as the generators do. The
plugin description also counts the three skills v2 advertises, not one.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from scripts import collect_metabolomics_collection as collector
from scripts import release_gate

REPO = Path(__file__).resolve().parent.parent
V2 = REPO / "collections" / "metabolomics" / "v2"
PEER_REVIEWED = re.compile(r"\bpeer[-\s]?reviewed\b", re.IGNORECASE)


def test_the_gate_finds_no_peer_review_claim_in_v2() -> None:
    corpus = yaml.safe_load((V2 / "corpus.yaml").read_text(encoding="utf-8"))

    result = release_gate.check_peer_review_claim(V2, corpus)

    assert result.coverage["not_peer_reviewed_dois"] > 0
    assert result.status == release_gate.PASS, result.details


def test_marketplace_and_pack_surfaces_make_no_peer_review_claim() -> None:
    marketplace = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text("utf-8"))
    surfaces = {f"marketplace:{p['name']}": p.get("description", "") for p in marketplace["plugins"]}
    for pack in sorted((REPO / "packs" / "metabolomics").glob("*/")):
        for name in ("skills/_router/SKILL.md", "GROUNDING.md", ".claude-plugin/plugin.json"):
            path = pack / name
            if path.is_file():
                surfaces[str(path.relative_to(REPO))] = path.read_text(encoding="utf-8")

    claims = sorted(where for where, text in surfaces.items() if PEER_REVIEWED.search(text))
    assert not claims, claims


def test_the_collector_default_description_makes_no_peer_review_claim() -> None:
    assert not PEER_REVIEWED.search(collector.COLLECTION_DESCRIPTION)


def test_the_v2_plugin_description_counts_the_three_advertised_skills() -> None:
    description = json.loads((V2 / ".claude-plugin" / "plugin.json").read_text("utf-8"))["description"]
    advertised = sorted(p.parent.name for p in (V2 / "skills").glob("*/SKILL.md"))

    assert advertised == ["_router", "asb-contribute", "asb-metabolomics"]
    assert "three skills are advertised" in description
    assert "one router skill is advertised" not in description
