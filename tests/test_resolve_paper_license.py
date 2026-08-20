"""The paper-licence resolver must fire on unestablished entries and only those.

Two ways to get this wrong, both silent. Under-fire: skip an entry whose reuse
rights were never asked about, leaving a genuinely CC-BY paper labelled
`restricted` and its skills under caps they do not need. Over-fire: overwrite an
entry whose repository already answered, or promote `access.type` on a licence
that grants nothing — which would hand the release gate an OA exemption the
source never gave.

Nothing here touches the network; the registry is stubbed.
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts import derive_license_tiers as dlt  # noqa: E402
from scripts import resolve_paper_license as rpl  # noqa: E402
from scripts.preprint_license import PreprintLicense  # noqa: E402

CC_BY = "https://creativecommons.org/licenses/by/4.0/"


def _entry(doi: str, **overrides) -> dict:
    entry = {"name": doi, "doi": doi, "repo_url": "", "status": "included",
             "access": {"type": "link-only", "is_oa": None, "license": None},
             "license_tier": "restricted", "license_detection": "none"}
    entry.update(overrides)
    return entry


def _corpus(tmp_path: pathlib.Path, entries: list[dict]) -> str:
    path = tmp_path / "corpus.yaml"
    path.write_text(yaml.safe_dump({"papers": entries}, sort_keys=False), encoding="utf-8")
    return str(path)


def _registry(answers: dict[str, PreprintLicense]):
    """Stub resolver: DOI -> outcome, defaulting to an unresolved lookup."""
    def _resolve(doi, fetch=None, preprints_only=True):
        return answers.get(doi, PreprintLicense(doi, "unresolved"))
    return _resolve


def _resolved(doi: str, spdx: str, reuse: str, registry: str = "crossref") -> PreprintLicense:
    return PreprintLicense(doi, "resolved", doi, registry, CC_BY, spdx, reuse, "open")


# --------------------------------------------------------------------------- #
# Which entries the resolver looks at                                          #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("detection", sorted(d for d in rpl.UNESTABLISHED_DETECTIONS if d is not None))
def test_an_entry_whose_repository_could_not_answer_is_examined(detection):
    assert rpl.needs_paper_license(_entry("10.1/a", license_detection=detection))


def test_an_entry_with_no_detection_field_at_all_is_examined():
    entry = _entry("10.1/a")
    entry.pop("license_detection")
    assert rpl.needs_paper_license(entry)


@pytest.mark.parametrize("detection", ["github-api", "license-file", "crossref-paper"])
def test_an_entry_whose_licence_is_already_established_is_left_alone(detection):
    assert not rpl.needs_paper_license(_entry("10.1/a", license_detection=detection))


def test_a_locked_entry_is_never_touched():
    assert not rpl.needs_paper_license(
        _entry("10.1/a", license_locked=True, license_detection="none"))


@pytest.mark.parametrize("detection", ["none", "file-present-unclassified"])
def test_an_entry_with_a_repository_stays_a_repository_question(detection):
    """Its license_tier describes the tool; the paper's licence is a different axis."""
    assert not rpl.needs_paper_license(
        _entry("10.1/a", repo_url="https://github.com/o/r", license_detection=detection))


def test_the_unestablished_vocabulary_covers_what_the_repo_route_can_report():
    """Drift guard: derive_license_tiers' own no-licence outcomes must be in the set."""
    no_repo_file = dlt.detect_license("o", "r", None, _fetch_api=lambda *a: None,
                                      _contents=lambda *a: [], _fetch_file=lambda *a: "")
    unclassifiable = dlt.detect_license("o", "r", None, _fetch_api=lambda *a: None,
                                        _contents=lambda *a: ["LICENSE"],
                                        _fetch_file=lambda *a: "some bespoke terms")
    for _, source in (no_repo_file, unclassifiable):
        assert source in rpl.UNESTABLISHED_DETECTIONS, (
            f"derive_license_tiers can report '{source}', which this script would skip")


# --------------------------------------------------------------------------- #
# What it writes — across publishers, and on the clean case                    #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("doi", [
    "10.1021/acs.jproteome.0e00000",   # a society publisher
    "10.1186/s13321-000-00000-0",      # a fully-OA journal
    "10.1038/s41586-000-00000-0",      # a subscription megajournal, author-paid OA
    "10.5281/zenodo.0000000",          # a repository deposit
])
def test_a_full_reuse_licence_promotes_any_publisher_to_open_access(tmp_path, doi):
    path = _corpus(tmp_path, [_entry(doi)])
    rpl.run([path], apply=True, cache_path=tmp_path / "c.json",
            _resolve=_registry({doi: _resolved(doi, "CC-BY-4.0", "full")}))
    entry = yaml.safe_load(pathlib.Path(path).read_text())["papers"][0]
    assert entry["access"]["type"] == "open-access"
    assert entry["access"]["license"] == "CC-BY-4.0"
    assert entry["license_detection"] == "crossref-paper"
    assert entry["source_reuse"] == "full"


@pytest.mark.parametrize("spdx,reuse", [("CC-BY-NC-4.0", "limited"), ("arXiv-1.0", "none")])
def test_a_licence_short_of_full_reuse_is_recorded_but_never_promoted(tmp_path, spdx, reuse):
    doi = "10.1/nc"
    path = _corpus(tmp_path, [_entry(doi)])
    rpl.run([path], apply=True, cache_path=tmp_path / "c.json",
            _resolve=_registry({doi: _resolved(doi, spdx, reuse)}))
    entry = yaml.safe_load(pathlib.Path(path).read_text())["papers"][0]
    assert entry["access"]["type"] == "link-only", "no full-reuse grant, no promotion"
    assert entry["access"]["license"] == spdx, "the licence is still worth recording"


def test_an_unresolved_lookup_changes_nothing_and_is_reported(tmp_path):
    doi = "10.1/silent"
    path = _corpus(tmp_path, [_entry(doi)])
    before = pathlib.Path(path).read_text()
    findings = rpl.run([path], apply=True, cache_path=tmp_path / "c.json",
                       _resolve=_registry({}))
    assert pathlib.Path(path).read_text() == before
    assert [f["status"] for f in findings] == ["unresolved"]
    assert rpl.summarize(findings)["unresolved"] == 1


def test_an_established_entry_is_not_rewritten(tmp_path):
    doi = "10.1/settled"
    settled = _entry(doi, license_detection="github-api", license_tier="open")
    settled["access"]["license"] = "MIT"
    path = _corpus(tmp_path, [settled])
    findings = rpl.run([path], apply=True, cache_path=tmp_path / "c.json",
                       _resolve=_registry({doi: _resolved(doi, "CC-BY-4.0", "full")}))
    assert findings == []
    assert yaml.safe_load(pathlib.Path(path).read_text())["papers"][0]["access"]["license"] == "MIT"


def test_a_cached_outcome_is_re_evaluated_against_the_current_access_type(tmp_path):
    """The cache stores the registry's answer, not a verdict about one entry."""
    doi = "10.1/cached"
    cache = tmp_path / "c.json"
    cache.write_text(json.dumps({doi: {"doi": doi, "status": "resolved", "spdx": "CC-BY-4.0",
                                       "source_reuse": "full", "registry": "crossref",
                                       "promotes": True}}))
    already_open = _entry(doi)
    already_open["access"]["type"] = "open-access"
    path = _corpus(tmp_path, [already_open])
    findings = rpl.run([path], apply=True, cache_path=cache, _resolve=_registry({}))
    assert findings[0]["promotes"] is False, "already open-access: nothing to promote"


if __name__ == "__main__":
    import subprocess
    raise SystemExit(subprocess.run([sys.executable, "-m", "pytest", __file__, "-q"]).returncode)
