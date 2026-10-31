"""The class-A collector writes a collection CITATION.cff that is valid CFF 1.2.0.

Every collection-level CITATION.cff in the public tree failed CFF 1.2.0
validation, the metabolomics v2 one because its 495 references lack the
required authors and title. GitHub's "Cite this repository" and Zenodo misread
or ignore an invalid file without an error. The class-A collector writes no
``references`` (the source DOIs are in corpus.yaml), and this keeps it so.
The cffconvert check runs when cffconvert is on PATH.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from scripts import collect_from_cut as collector


REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs"
CREATORS = REPO / "scripts" / "release_creators.yaml"


@pytest.fixture(scope="module")
def citation(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("citation")
    code = collector.main(
        [
            "--cut",
            str(FIXTURE / "corpus"),
            "--domain",
            "agentic-ai",
            "--version",
            "v1",
            "--out",
            str(root / "candidate"),
            "--license",
            "CC-BY-4.0",
            "--plugin-repo",
            "https://github.com/HolobiomicsLab/asb-skills-agentic-ai",
            "--creators",
            str(CREATORS),
            "--corpus",
            str(FIXTURE / "corpus.yaml"),
            "--receipts",
            str(root / "receipts"),
        ]
    )
    assert code == 0
    return root / "candidate" / "CITATION.cff"


def test_generated_citation_has_the_required_cff_fields(citation: Path) -> None:
    payload = yaml.safe_load(citation.read_text(encoding="utf-8"))

    assert payload["cff-version"] == "1.2.0"
    assert payload["message"]
    assert payload["title"] == "ASB Agentic AI Skill Collection v1"
    assert payload["type"] in {"software", "dataset"}
    assert isinstance(payload["version"], str)
    assert "references" not in payload
    assert payload["authors"]
    for author in payload["authors"]:
        assert author.get("name") or (
            author.get("family-names") and author.get("given-names")
        ), author


@pytest.mark.skipif(shutil.which("cffconvert") is None, reason="cffconvert not on PATH")
def test_generated_citation_passes_cffconvert_validate(citation: Path) -> None:
    result = subprocess.run(
        ["cffconvert", "--validate", "-i", str(citation)],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
