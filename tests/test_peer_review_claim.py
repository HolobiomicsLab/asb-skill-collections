"""A collection whose corpus holds preprints or deposits never says peer-reviewed.

Every plugin manifest said its skills were each derived from a peer-reviewed
method paper, while corpora hold bioRxiv, arXiv and ChemRxiv preprints and
Zenodo deposits. The generators now say "a method paper (journal article or
preprint) and its code", and the release gate fails the old claim over such a
corpus.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from scripts import land_candidate, release_gate, router_shape


PEER_REVIEWED = (
    "ASB Genomics: 3 evidence-grounded skills, each derived from a peer-reviewed "
    "method paper."
)
NEUTRAL = (
    "ASB Genomics: 3 evidence-grounded skills, each derived from a method paper "
    "(journal article or preprint) and its code."
)


def _collection(tmp_path: Path, dois: list[str], plugin_description: str) -> Path:
    unit = tmp_path / "collection"
    plugin = unit / ".claude-plugin" / "plugin.json"
    plugin.parent.mkdir(parents=True)
    plugin.write_text(
        json.dumps({"name": "genomics", "description": plugin_description}),
        encoding="utf-8",
    )
    papers = [
        {"doi": doi, "status": "included", "access": {"type": "gold-oa"}}
        for doi in dois
    ]
    (unit / "corpus.yaml").write_text(yaml.safe_dump({"papers": papers}), "utf-8")
    leaf = unit / "leaves" / "alpha" / "SKILL.md"
    leaf.parent.mkdir(parents=True)
    leaf.write_text(
        "---\nname: alpha\nlicense: CC-BY-4.0\nderived_from:\n"
        f"- doi: {dois[0]}\n---\n\n# Alpha\n\nThe method was peer-reviewed.\n",
        encoding="utf-8",
    )
    return unit


def _check(unit: Path) -> release_gate.CheckResult:
    corpus = yaml.safe_load((unit / "corpus.yaml").read_text(encoding="utf-8"))
    return release_gate.check_peer_review_claim(unit, corpus)


@pytest.mark.parametrize(
    "doi",
    [
        "10.1101/2023.01.01.522000",
        "10.48550/arXiv.2401.00001",
        "10.26434/chemrxiv-2023-abcde",
        "https://doi.org/10.5281/zenodo.1234567",
    ],
)
def test_peer_reviewed_manifest_over_a_preprint_corpus_fails(
    tmp_path: Path, doi: str
) -> None:
    unit = _collection(tmp_path, ["10.1038/s41587-020-00797-0", doi], PEER_REVIEWED)

    result = _check(unit)

    assert result.status == release_gate.FAIL
    [finding] = result.details
    assert finding["file"] == ".claude-plugin/plugin.json"
    assert result.coverage["not_peer_reviewed_dois"] == 1


def test_journal_only_corpus_may_say_peer_reviewed(tmp_path: Path) -> None:
    unit = _collection(tmp_path, ["10.1038/s41587-020-00797-0"], PEER_REVIEWED)

    result = _check(unit)

    assert result.status != release_gate.FAIL
    assert result.details == []


def test_neutral_wording_passes_over_a_preprint_corpus(tmp_path: Path) -> None:
    unit = _collection(tmp_path, ["10.1101/2023.01.01.522000"], NEUTRAL)

    result = _check(unit)

    assert result.status == release_gate.PASS
    assert result.counts["checked"] == 1


def test_top_level_documents_and_advertised_skills_are_claim_surfaces(
    tmp_path: Path,
) -> None:
    unit = _collection(tmp_path, ["10.1101/2023.01.01.522000"], NEUTRAL)
    (unit / "ABOUT.md").write_text("Skills from peer reviewed papers.\n", "utf-8")
    router = unit / "skills" / "_router" / "SKILL.md"
    router.parent.mkdir(parents=True)
    router.write_text(
        "---\nname: r\n---\n\nEach distilled from a\nPeer-Reviewed method paper.\n",
        encoding="utf-8",
    )

    result = _check(unit)

    failed = sorted(d["file"] for d in result.details if d["status"] == release_gate.FAIL)
    assert failed == ["ABOUT.md", "skills/_router/SKILL.md"]
    router_finding = [d for d in result.details if d["file"].endswith("SKILL.md")][0]
    assert router_finding["lines"] == [6]


def test_held_preprints_do_not_count(tmp_path: Path) -> None:
    unit = _collection(tmp_path, ["10.1038/s41587-020-00797-0"], PEER_REVIEWED)
    corpus = yaml.safe_load((unit / "corpus.yaml").read_text(encoding="utf-8"))
    corpus["papers"].append({"doi": "10.1101/2023.01.01.522000", "status": "hold"})

    result = release_gate.check_peer_review_claim(unit, corpus)

    assert result.status != release_gate.FAIL


def test_strict_gate_blocks_the_claim(tmp_path: Path) -> None:
    unit = _collection(tmp_path, ["10.1101/2023.01.01.522000"], PEER_REVIEWED)

    report = release_gate.run_gate(unit, None, True)
    checks = {check["name"]: check for check in report["checks"]}

    assert checks["peer_review_claim"]["status"] == release_gate.FAIL
    assert report["release_verified"] is False


def test_generated_router_and_marketplace_make_no_peer_review_claim(
    tmp_path: Path,
) -> None:
    unit = _collection(tmp_path, ["10.1101/2023.01.01.522000"], NEUTRAL)
    router_shape.write_router(unit, 1)
    router = (unit / "skills" / "_router" / "SKILL.md").read_text(encoding="utf-8")

    assert "method paper (journal article or preprint) and its code" in router
    assert _check(unit).status == release_gate.PASS
    assert "peer-reviewed" not in router_shape.ROUTER_TEMPLATE
    assert "peer-reviewed" not in Path(land_candidate.__file__).read_text("utf-8")
