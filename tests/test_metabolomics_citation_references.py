"""The metabolomics collector writes only complete CITATION.cff references.

The v2 CITATION.cff listed 495 references as ``{type: article, doi: ...}``.
CFF 1.2.0 requires ``authors`` and ``title`` on every reference, so the file
failed validation and GitHub's "Cite this repository" and Zenodo misread it
without an error. The collector now writes a reference only with a title and
at least one author, taken from Crossref (DataCite for arXiv and Zenodo DOIs),
and reuses the complete references an earlier file already carries.
"""

from __future__ import annotations

import io
import json
import shutil
import subprocess
import urllib.error
from pathlib import Path

import pytest
import yaml

from scripts import collect_metabolomics_collection as collector

REPO = Path(__file__).resolve().parent.parent
V2_CITATION = REPO / "collections" / "metabolomics" / "v2" / "CITATION.cff"

CROSSREF_WORK = {
    "type": "journal-article",
    "title": ["Molecular networking with <i>GNPS</i>"],
    "author": [
        {"given": "Ada", "family": "Lovelace", "sequence": "first"},
        {"name": "The GNPS Consortium"},
        {"given": "", "family": ""},
    ],
    "issued": {"date-parts": [[2016, 8]]},
    "container-title": ["Nature Biotechnology"],
}
DATACITE_ATTRIBUTES = {
    "titles": [{"title": "A preprint on spectra"}],
    "creators": [
        {"name": "Hopper, Grace", "givenName": "Grace", "familyName": "Hopper",
         "nameType": "Personal"},
        {"name": "Holobiomics Lab", "nameType": "Organizational"},
    ],
    "publicationYear": 2025,
    "types": {"resourceTypeGeneral": "Preprint"},
}


def _complete(reference: dict) -> bool:
    return bool(reference.get("title")) and bool(reference.get("authors"))


def test_a_crossref_work_becomes_a_complete_reference() -> None:
    reference = collector.reference_from_crossref("10.1038/nbt.3597", CROSSREF_WORK)

    assert reference == {
        "type": "article",
        "title": "Molecular networking with GNPS",
        "authors": [
            {"family-names": "Lovelace", "given-names": "Ada"},
            {"name": "The GNPS Consortium"},
        ],
        "doi": "10.1038/nbt.3597",
        "year": 2016,
        "journal": "Nature Biotechnology",
    }


@pytest.mark.parametrize("missing", ["title", "author"])
def test_a_work_without_title_or_authors_gives_no_reference(missing: str) -> None:
    work = {key: value for key, value in CROSSREF_WORK.items() if key != missing}

    assert collector.reference_from_crossref("10.1/x", work) is None


def test_identical_author_entries_are_written_once() -> None:
    work = dict(CROSSREF_WORK, author=[{"given": "Liang", "family": "Wang"}] * 2)

    reference = collector.reference_from_crossref("10.1/x", work)

    assert reference["authors"] == [{"family-names": "Wang", "given-names": "Liang"}]


def test_a_datacite_record_becomes_a_complete_reference() -> None:
    reference = collector.reference_from_datacite("10.48550/arxiv.1", DATACITE_ATTRIBUTES)

    assert reference == {
        "type": "article",
        "title": "A preprint on spectra",
        "authors": [
            {"family-names": "Hopper", "given-names": "Grace"},
            {"name": "Holobiomics Lab"},
        ],
        "doi": "10.48550/arxiv.1",
        "year": 2025,
    }


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _opener(routes: dict[str, dict | None]):
    """A urlopen stand-in: a URL prefix maps to a JSON body, or None for a 404."""
    seen = []

    def urlopen(request, timeout=None):
        seen.append(request.full_url)
        assert request.get_header("User-agent", "").startswith("asb-skill-collections")
        for prefix, body in routes.items():
            if request.full_url.startswith(prefix):
                if body is None:
                    raise urllib.error.HTTPError(request.full_url, 404, "Not Found", {}, None)
                return _Response(json.dumps(body).encode())
        raise AssertionError(f"unexpected request {request.full_url}")

    urlopen.seen = seen
    return urlopen


def test_a_doi_crossref_does_not_hold_is_looked_up_in_datacite() -> None:
    opener = _opener({
        collector.CROSSREF_WORKS: None,
        collector.DATACITE_DOIS: {"data": {"attributes": DATACITE_ATTRIBUTES}},
    })

    reference = collector.fetch_citation_reference("10.5281/zenodo.1", opener)

    assert reference is not None and _complete(reference)
    assert [url.split("/")[2] for url in opener.seen] == ["api.crossref.org", "api.datacite.org"]
    assert opener.seen[0].endswith("10.5281%2Fzenodo.1")


def test_a_doi_neither_registry_holds_gives_no_reference() -> None:
    opener = _opener({collector.CROSSREF_WORKS: None, collector.DATACITE_DOIS: None})

    assert collector.fetch_citation_reference("10.9999/gone", opener) is None


def test_the_writer_never_emits_a_reference_without_title_and_authors() -> None:
    dois = ["10.1038/nbt.3597", "10.1/no-record"]
    references = {"10.1038/nbt.3597": collector.reference_from_crossref(dois[0], CROSSREF_WORK)}

    payload = yaml.safe_load(
        collector.render_citation_cff(dois, "2026-10-31T00:00:00Z", references)
    )

    assert [r["doi"] for r in payload["references"]] == ["10.1038/nbt.3597"]
    assert all(_complete(r) and r.get("type") for r in payload["references"])


def test_with_no_complete_reference_the_writer_omits_the_key() -> None:
    payload = yaml.safe_load(collector.render_citation_cff(["10.1/x"], "2026-10-31T00:00:00Z"))

    assert "references" not in payload


def test_complete_references_of_an_earlier_file_are_reused(tmp_path: Path) -> None:
    complete = collector.reference_from_crossref("10.1038/nbt.3597", CROSSREF_WORK)
    citation = tmp_path / "CITATION.cff"
    citation.write_text(
        yaml.safe_dump({"references": [complete, {"type": "article", "doi": "10.1/bare"}]}),
        encoding="utf-8",
    )

    reused = collector.existing_citation_references(citation)

    assert reused == {"10.1038/nbt.3597": complete}


def test_every_v2_reference_has_type_title_and_authors() -> None:
    payload = yaml.safe_load(V2_CITATION.read_text(encoding="utf-8"))

    incomplete = [r.get("doi") for r in payload.get("references") or [] if not (
        r.get("type") and _complete(r)
    )]
    assert not incomplete, incomplete


@pytest.mark.skipif(shutil.which("cffconvert") is None, reason="cffconvert not on PATH")
@pytest.mark.parametrize("source", ["generated", "v2"])
def test_cffconvert_validates(source: str, tmp_path: Path, monkeypatch) -> None:
    # The module's own DOI is the v1 placeholder "TODO-zenodo", left to the
    # legacy-v1 decision; the references are what this test is about.
    monkeypatch.setattr(collector, "COLLECTION_DOI", "10.5281/zenodo.20794027")
    if source == "v2":
        path = V2_CITATION
    else:
        path = tmp_path / "CITATION.cff"
        references = {"10.1038/nbt.3597": collector.reference_from_crossref(
            "10.1038/nbt.3597", CROSSREF_WORK
        )}
        path.write_text(
            collector.render_citation_cff(["10.1038/nbt.3597"], "2026-10-31T00:00:00Z", references),
            encoding="utf-8",
        )

    result = subprocess.run(
        ["cffconvert", "--validate", "-i", str(path)], capture_output=True, text=True, check=False
    )

    assert result.returncode == 0, result.stdout + result.stderr
