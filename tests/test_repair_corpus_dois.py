"""A DOI is repaired only when a registry says the repair is the real work.

The dangerous version of this script is the one that strips characters because
they look like cruft. `10.1177/14690667231164766` ends in a long digit run and is
perfectly real; `10.1093/bioinformatics/btac355/6593484` ends in one and is a URL
fragment. Nothing in the string separates them — only the registry does.

So the patterns here propose, and the network disposes. These tests pin both
directions: a genuine artefact is repaired, and everything else is left alone.
"""

from __future__ import annotations

import pathlib
import sys

import pytest
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scripts import repair_corpus_dois as r  # noqa: E402

BADGE = "10.5281/zenodo.1043226.svg"
BADGE_REAL = "10.5281/zenodo.1043226"
OUP = "10.1093/bioinformatics/btac355/6593484"
OUP_REAL = "10.1093/bioinformatics/btac355"


def _registry(known: set[str]):
    """Stub fetch: only an *exact* DOI in `known` resolves.

    Substring matching would be wrong here in a way that hides the bug under
    test: `10.5281/zenodo.1043226` is a prefix of `10.5281/zenodo.1043226.svg`,
    so a loose stub would report the artefact itself as resolving.
    """
    def _fetch(url: str):
        return {"ok": True} if any(url.endswith(k) for k in known) else None
    return _fetch


def _corpus(tmp_path, dois):
    path = tmp_path / "corpus.yaml"
    path.write_text(yaml.safe_dump({"papers": [{"name": d, "doi": d} for d in dois]}),
                    encoding="utf-8")
    return str(path)


# --------------------------------------------------------------------------- #
# Candidate generation — shape only, no authority                              #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("doi,expected", [
    (BADGE, BADGE_REAL),
    ("10.5281/zenodo.99.PNG", "10.5281/zenodo.99"),
    (OUP, OUP_REAL),
    ("10.1093/bib/bbad229/7199559", "10.1093/bib/bbad229"),
])
def test_a_known_artefact_shape_proposes_the_stripped_form(doi, expected):
    assert expected in r.repair_candidates(doi)


@pytest.mark.parametrize("doi", [
    "10.1177/14690667231164766",      # a real DOI that is all digits after the slash
    "10.1002/9780470508183",          # a real book DOI, likewise
    "10.1101/060012",                 # a real bioRxiv DOI
    "10.1186/s13321-025-01051-y",     # ordinary Springer
    "10.1093/bioinformatics/btac355",  # already canonical, two segments
])
def test_a_healthy_doi_proposes_nothing(doi):
    """The pre-filter must not drag real DOIs into a network round trip."""
    assert r.repair_candidates(doi) == []


# --------------------------------------------------------------------------- #
# Classification — the registry decides                                        #
# --------------------------------------------------------------------------- #

def test_an_artefact_whose_stripped_form_resolves_is_repairable():
    out = r.classify(BADGE, _registry({BADGE_REAL}))
    assert out["status"] == r.STATUS_REPAIRABLE
    assert out["repaired"] == BADGE_REAL


def test_a_doi_that_resolves_is_left_alone_however_odd_it_looks():
    """The other side. Stripping a suffix off a working DOI invents a new work."""
    out = r.classify(OUP, _registry({OUP}))
    assert out["status"] == r.STATUS_OK
    assert out["repaired"] is None


def test_a_doi_where_nothing_resolves_is_reported_not_guessed():
    out = r.classify(BADGE, _registry(set()))
    assert out["status"] == r.STATUS_DEAD
    assert out["repaired"] is None


def test_a_repair_is_refused_when_two_candidates_both_resolve(monkeypatch):
    """Choosing between two real works is worse than leaving the entry broken.

    The two shipped rules rewrite mutually exclusive suffixes, so no real DOI
    reaches this branch today. It is tested through the candidate generator
    because the guard is what keeps a third rule from turning a coin toss into
    a silent corpus edit.
    """
    doi = "10.1234/broken"
    monkeypatch.setattr(r, "repair_candidates", lambda _: ["10.1234/one", "10.1234/two"])
    out = r.classify(doi, _registry({"10.1234/one", "10.1234/two"}))
    assert out["status"] == r.STATUS_AMBIGUOUS
    assert out["repaired"] is None
    assert out["candidates"] == ["10.1234/one", "10.1234/two"]


# --------------------------------------------------------------------------- #
# Writing                                                                      #
# --------------------------------------------------------------------------- #

def test_apply_rewrites_only_the_repairable_entry(tmp_path):
    healthy = "10.1177/14690667231164766"
    path = _corpus(tmp_path, [BADGE, healthy])
    r.run([path], apply=True, fetch=_registry({BADGE_REAL, healthy}))
    dois = [p["doi"] for p in yaml.safe_load(pathlib.Path(path).read_text())["papers"]]
    assert dois == [BADGE_REAL, healthy]


def test_audit_mode_writes_nothing(tmp_path):
    path = _corpus(tmp_path, [BADGE])
    before = pathlib.Path(path).read_text()
    findings = r.run([path], apply=False, fetch=_registry({BADGE_REAL}))
    assert pathlib.Path(path).read_text() == before
    assert findings[0]["status"] == r.STATUS_REPAIRABLE


def test_a_healthy_corpus_costs_no_network_calls(tmp_path):
    """The pre-filter is what makes this cheap enough to run in CI."""
    calls = []

    def _counting(url):
        calls.append(url)
        return None

    path = _corpus(tmp_path, ["10.1186/s13321-025-01051-y", "10.1101/060012"])
    assert r.run([path], apply=False, fetch=_counting) == []
    assert calls == []


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))


# --- propagation: the corpus is not the only place a DOI is keyed on ---------

def _collection(tmp_path, doi):
    col = tmp_path / "c"
    (col / "leaves" / "s").mkdir(parents=True)
    (col / "leaves" / "s" / "SKILL.md").write_text(
        f"---\nname: s\nderived_from:\n- doi: {doi}\n---\nbody\n", encoding="utf-8")
    (col / "skills_index.json").write_text(
        yaml.safe_dump([{"slug": "s", "dois": [doi]}]), encoding="utf-8")
    (col / "corpus.yaml").write_text(
        yaml.safe_dump({"papers": [{"name": doi, "title": doi, "doi": doi}]}), encoding="utf-8")
    return col


def test_a_repair_reaches_the_skills_and_indexes_too(tmp_path):
    """Repairing only corpus.yaml turns a visible break into an invisible one:
    every derived_from and index row would point at a DOI the corpus no longer
    has, and the join would silently find nothing."""
    col = _collection(tmp_path, BADGE)
    r.run([str(col / "corpus.yaml")], apply=True, fetch=_registry({BADGE_REAL}))
    assert BADGE not in (col / "leaves" / "s" / "SKILL.md").read_text()
    assert BADGE_REAL in (col / "leaves" / "s" / "SKILL.md").read_text()
    assert BADGE not in (col / "skills_index.json").read_text()


def test_the_placeholder_name_and_title_are_repaired_with_the_doi(tmp_path):
    """The harvester copies the DOI string into name/title when it has nothing
    better; leaving those keeps the artefact on display."""
    col = _collection(tmp_path, BADGE)
    r.run([str(col / "corpus.yaml")], apply=True, fetch=_registry({BADGE_REAL}))
    paper = yaml.safe_load((col / "corpus.yaml").read_text())["papers"][0]
    assert paper["doi"] == paper["name"] == paper["title"] == BADGE_REAL


def test_a_real_title_is_never_overwritten_by_the_doi(tmp_path):
    """The other side: only a name/title that *is* the DOI string is a placeholder."""
    col = _collection(tmp_path, BADGE)
    doc = yaml.safe_load((col / "corpus.yaml").read_text())
    doc["papers"][0]["title"] = "A real paper title"
    (col / "corpus.yaml").write_text(yaml.safe_dump(doc), encoding="utf-8")
    r.run([str(col / "corpus.yaml")], apply=True, fetch=_registry({BADGE_REAL}))
    assert yaml.safe_load((col / "corpus.yaml").read_text())["papers"][0]["title"] == "A real paper title"


def test_propagation_does_nothing_without_a_repair(tmp_path):
    col = _collection(tmp_path, BADGE)
    assert r.propagate_repairs(col, {}) == 0
