"""The distribution names the same authors as CITATION.cff, in the same order."""

from __future__ import annotations

import pathlib
import tomllib

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


def _citation_names() -> list[str]:
    citation = yaml.safe_load((REPO_ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    return [
        author.get("name") or f"{author['given-names']} {author['family-names']}"
        for author in citation["authors"]
    ]


def test_pyproject_authors_are_the_citation_authors():
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    names = [author["name"] for author in pyproject["project"]["authors"]]

    assert names == _citation_names()
