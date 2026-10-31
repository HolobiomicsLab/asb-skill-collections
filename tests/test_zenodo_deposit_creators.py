"""The Zenodo template's creators must start with scripts/release_creators.yaml.

The metabolomics v2 template listed four creators, while the release creators
list, the source the collector and the README follow, names two. `plan` and
`draft` now convert that list to Zenodo creators and refuse a template whose
leading creators differ in content or order, before any request. Entries after
the list are accepted only as persons with an ORCID iD, the co-authors that
scripts/select_release_coauthors.py --apply appends.
"""
import json

import pytest

from scripts import select_release_coauthors, zenodo_deposit
from tests.test_zenodo_deposit import DATE, ZENODO_JSON, FakeZenodo, make_repo


@pytest.fixture
def repo(tmp_path):
    return make_repo(tmp_path / "repo")


def _write_template_creators(repo, creators):
    path = repo / "collections/dom/v1/.zenodo.json"
    path.write_text(json.dumps({**ZENODO_JSON, "creators": creators}))


def _plan(repo):
    return zenodo_deposit.main(["plan", "dom", "v1", "--repo-root", str(repo),
                                "--publication-date", DATE])


def test_matching_creators_pass_the_plan(repo, capsys):
    assert _plan(repo) == 0
    assert "refused" not in capsys.readouterr().out


@pytest.mark.parametrize("creators", [
    [{"name": "Doe, Jane", "orcid": "0000-0000-0000-0000"}, {"name": "Example Network"}],
    [{"name": "Doe, Jane"}],
    [{"name": "Doe, Jane", "orcid": "0000-0000-0000-0001"}],
    [],
], ids=["extra-entity", "missing-orcid", "other-orcid", "none"])
def test_mismatched_creators_make_plan_refuse(repo, capsys, creators):
    _write_template_creators(repo, creators)
    assert _plan(repo) == 1
    out = capsys.readouterr().out
    assert "refused: creators differ from scripts/release_creators.yaml" in out


def test_creator_order_counts(repo, capsys):
    (repo / "scripts" / "release_creators.yaml").write_text(
        "creators:\n- family: Doe\n  given: Jane\n  orcid: 0000-0000-0000-0000\n"
        "- name: Example Lab\n")
    _write_template_creators(repo, [{"name": "Example Lab"},
                                    {"name": "Doe, Jane", "orcid": "0000-0000-0000-0000"}])
    assert _plan(repo) == 1
    _write_template_creators(repo, [{"name": "Doe, Jane", "orcid": "0000-0000-0000-0000"},
                                    {"name": "Example Lab"}])
    assert _plan(repo) == 0


def test_draft_refuses_mismatched_creators_before_any_request(repo, monkeypatch, capsys):
    _write_template_creators(repo, [{"name": "Somebody Else"}])
    monkeypatch.setenv("ZENODO_TOKEN", "tok-test-only")
    fake = FakeZenodo(zenodo_deposit.ZENODO_URL)
    monkeypatch.setattr(zenodo_deposit, "_request", fake)
    code = zenodo_deposit.main(["draft", "dom", "v1", "--repo-root", str(repo),
                                "--out-dir", str(repo / "out"), "--publication-date", DATE])
    assert code == 1
    assert fake.calls == []
    assert "release_creators.yaml" in capsys.readouterr().err


def test_a_missing_creators_list_stops_the_plan(repo, capsys):
    (repo / "scripts" / "release_creators.yaml").unlink()
    assert _plan(repo) == 1
    assert "release_creators.yaml not found" in capsys.readouterr().err


def test_person_and_entity_entries_convert_to_zenodo_creators(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "release_creators.yaml").write_text(
        "creators:\n"
        "- family: Doe\n  given: Jane\n  orcid: https://orcid.org/0000-0000-0000-0000\n"
        "  affiliation: Example Institute\n"
        "- name: Example framework\n")
    assert zenodo_deposit.expected_creators(tmp_path) == [
        {"name": "Doe, Jane", "orcid": "0000-0000-0000-0000",
         "affiliation": "Example Institute"},
        {"name": "Example framework"},
    ]


def test_a_person_entry_without_given_name_is_an_error(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "release_creators.yaml").write_text("creators:\n- family: Doe\n")
    with pytest.raises(zenodo_deposit.ZenodoError, match="family and given"):
        zenodo_deposit.expected_creators(tmp_path)


def test_the_repository_creators_list_converts():
    root = zenodo_deposit.Path(__file__).resolve().parent.parent
    creators = zenodo_deposit.expected_creators(root)
    assert creators and all(creator.get("name") for creator in creators)


def test_coauthors_appended_by_select_release_coauthors_pass_the_plan(repo, capsys):
    template = repo / "collections/dom/v1/.zenodo.json"
    added = select_release_coauthors._apply_zenodo(
        template, [{"name": "Ada Example", "orcid": "0000-0002-1825-0097"}])
    assert added == 1
    assert json.loads(template.read_text())["creators"][-1] == {
        "name": "Example, Ada", "orcid": "0000-0002-1825-0097"}
    assert _plan(repo) == 0
    assert "refused" not in capsys.readouterr().out


@pytest.mark.parametrize("creators", [
    [{"name": "Example, Ada", "orcid": "0000-0002-1825-0097"},
     {"name": "Doe, Jane", "orcid": "0000-0000-0000-0000"}],
    [{"name": "Doe, Jane", "orcid": "0000-0000-0000-0000"},
     {"name": "Example, Ada", "orcid": "0000-0000-0000-0000"}],
    [{"name": "Doe, Jane", "orcid": "0000-0000-0000-0000"},
     {"name": "Example, Ada", "orcid": "https://orcid.org/0000-0002-1825-0097"}],
    [{"name": "Doe, Jane", "orcid": "0000-0000-0000-0000"},
     {"name": "Example, Ada", "orcid": "0000-0002-1825-0097", "type": "Other"}],
], ids=["coauthor-first", "duplicate-orcid", "orcid-url", "extra-key"])
def test_entries_after_the_list_must_be_distinct_orcid_persons(repo, capsys, creators):
    _write_template_creators(repo, creators)
    assert _plan(repo) == 1
    assert "refused: creators differ" in capsys.readouterr().out
