import copy
import json
import pathlib

import pytest
import yaml

from scripts import proposal_corpus as pc


FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "proposals"
WAVES = sorted(FIXTURES.glob("wave-*.yaml"))


def valid_row(**changes):
    row = {
        "name": "Example",
        "doi": "10.1234/example.1",
        "title": "An example paper",
        "year": 2026,
        "category": "Annotation",
        "repo_url": "https://github.com/example/tool",
        "status": "candidate",
        "license_tier": "open",
        "wave": "community-test",
        "resource_type": "software-tool",
        "source_issue": 42,
        "access": {
            "type": "gold-oa",
            "license": "cc-by-4.0",
            "is_oa": True,
            "verified_via": "test",
            "verified_on": "2026-11-08",
        },
        "triage": {
            "proposer": "literature-watch",
            "rationale": "Relevant test example.",
            "decision": "pending",
            "notes": "Awaiting curator review.",
        },
    }
    row.update(changes)
    return row


def valid_document(rows=None):
    rows = [valid_row()] if rows is None else rows
    document = {
        "schema": "asb-corpus/1.0",
        "collection": "metabolomics",
        "version": 3,
        "generated_on": "2026-11-08",
        "source": "test proposals",
        "policy": "OPEN_ACCESS_POLICY.md",
        "wave": "community-test",
        "papers": rows,
    }
    document["summary"] = pc.recompute_summary(document)
    return document


def test_both_live_wave_fixtures_validate():
    assert len(WAVES) == 2
    for path in WAVES:
        assert pc.validate(pc.load(path)) == []


def test_sparse_live_summary_remains_valid():
    document = pc.load(WAVES[0])
    assert set(document["summary"]) < {"total", *pc.STATUSES}
    assert pc.validate(document) == []


@pytest.mark.parametrize("value", ["not yaml", [1], None])
def test_non_mapping_document_is_content_violation(value):
    violations = pc.validate(value)
    assert len(violations) == 1
    assert violations[0].path == "$"


def test_invalid_yaml_load_is_content_violation(tmp_path):
    path = tmp_path / "broken.yaml"
    path.write_text("papers: [\n", encoding="utf-8")
    violations = pc.validate(pc.load(path))
    assert violations[0].path == "$"
    assert "invalid YAML" in violations[0].message


@pytest.mark.parametrize(
    ("change", "path"),
    [
        ({"schema": "other/1"}, "schema"),
        ({"unknown": True}, "$.unknown"),
        ({"collection": 3}, "$.collection"),
        ({"generated_on": "11-08-2026"}, "generated_on"),
        ({"papers": {}}, "papers"),
        ({"summary": []}, "summary"),
    ],
)
def test_document_violations(change, path):
    document = valid_document()
    document.update(change)
    assert path in {violation.path for violation in pc.validate(document)}


def test_missing_required_document_field():
    document = valid_document()
    del document["wave"]
    assert "$" in {violation.path for violation in pc.validate(document)}


@pytest.mark.parametrize(
    ("change", "path"),
    [
        ({"title": 2}, "papers[0].title"),
        ({"year": True}, "papers[0].year"),
        ({"source_issue": "42"}, "papers[0].source_issue"),
        ({"doi": "not a DOI"}, "papers[0].doi"),
        ({"status": "accepted"}, "papers[0].status"),
        ({"source_watch": "today"}, "papers[0].source_watch"),
        ({"source_queries": [42]}, "papers[0].source_queries[0]"),
        ({"priority": 1.5}, "papers[0].priority"),
        ({"extra": "field"}, "papers[0].extra"),
    ],
)
def test_row_violations(change, path):
    document = valid_document([valid_row(**change)])
    assert path in {violation.path for violation in pc.validate(document)}


def test_null_doi_is_valid_for_repository_resource():
    row = valid_row(doi=None)
    assert pc.validate(valid_document([row])) == []


@pytest.mark.parametrize(
    ("change", "path"),
    [
        ({"is_oa": "yes"}, "papers[0].access.is_oa"),
        ({"verified_on": "2026/11/08"}, "papers[0].access.verified_on"),
        ({"unknown": 1}, "papers[0].access.unknown"),
    ],
)
def test_access_violations(change, path):
    row = valid_row()
    row["access"].update(change)
    assert path in {violation.path for violation in pc.validate(valid_document([row]))}


@pytest.mark.parametrize(
    ("change", "path"),
    [
        ({"decision": ""}, "papers[0].triage.decision"),
        ({"conflict_declared": "false"}, "papers[0].triage.conflict_declared"),
        ({"curated_on": "today"}, "papers[0].triage.curated_on"),
        ({"unknown": 1}, "papers[0].triage.unknown"),
    ],
)
def test_triage_violations(change, path):
    row = valid_row()
    row["triage"].update(change)
    assert path in {violation.path for violation in pc.validate(valid_document([row]))}


def test_nested_blocks_are_required_mappings():
    row = valid_row(access=[], triage=None)
    paths = {violation.path for violation in pc.validate(valid_document([row]))}
    assert {"papers[0].access", "papers[0].triage"} <= paths


def test_summary_detects_stale_and_unknown_counts():
    stale = valid_document()
    stale["summary"]["total"] = 99
    unknown = valid_document()
    unknown["summary"]["accepted"] = 1
    wrong = valid_document()
    wrong["summary"]["candidate"] = "1"
    for document in (stale, unknown, wrong):
        assert any(v.path.startswith("summary") for v in pc.validate(document))


def test_invalid_status_never_prevents_other_content_violations():
    document = valid_document()
    document["papers"][0]["status"] = "accepted"
    document["papers"][0]["year"] = "unknown"
    paths = {violation.path for violation in pc.validate(document)}
    assert {"papers[0].status", "papers[0].year"} <= paths


def test_summary_recomputes_all_statuses_instead_of_incrementing():
    rows = [valid_row(status=status, doi=f"10.1234/example.{index}")
            for index, status in enumerate(pc.STATUSES)]
    document = valid_document(rows)
    document["summary"] = {"total": 1, "included": 1}
    assert pc.recompute_summary(document) == {
        "total": 5, "candidate": 1, "hold": 1, "included": 1,
        "rejected": 1, "duplicate": 1,
    }


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("https://doi.org/10.1038/S41592-022-01486-3", "10.1038/s41592-022-01486-3"),
        ("doi:10.1101/2021.02.25.432841v1", "10.1101/2021.02.25.432841"),
        ("10.21203/rs.3.rs-9283100/v1", "10.21203/rs.3.rs-9283100/v1"),
        ("10.1007/s11306-017-1242-7.", "10.1007/s11306-017-1242-7"),
        ("arXiv:1802.09347v2", "10.48550/arxiv.1802.09347"),
        ("not a doi", None),
        (None, None),
    ],
)
def test_corpus_doi_normalization(raw, expected):
    assert pc.normalise_doi(raw) == expected


def test_duplicate_precedence_covered_then_corpus_then_proposals():
    doi = "10.1234/shared.1"
    first = valid_document([valid_row(doi=doi)])
    second = valid_document([valid_row(doi=doi)])
    third = valid_document([valid_row(doi=doi)])
    covered = {"covered": {pc._doi_key(doi): {}}}
    corpus = [valid_row(doi=doi)]
    matches = pc.find_duplicates([first, second, third], covered, corpus)
    assert [match.source for match in matches if match.severity == "error"] == [
        "covered", "covered", "covered"
    ]
    matches = pc.find_duplicates([first, second, third], {"covered": {}}, corpus)
    assert [match.source for match in matches if match.severity == "error"] == [
        "corpus", "corpus", "corpus"
    ]
    matches = pc.find_duplicates([first, second, third], {"covered": {}}, [])
    assert [match.source for match in matches if match.severity == "error"] == [
        "proposal", "proposal"
    ]


def test_repository_duplicate_is_only_a_warning():
    first = valid_document([valid_row(doi="10.1234/one")])
    second = valid_document([valid_row(doi="10.1234/two")])
    matches = pc.find_duplicates([first, second], {}, [])
    assert [(match.source, match.severity) for match in matches] == [
        ("repository", "warning")
    ]


def test_covered_doi_precedes_repository_warning():
    row = valid_row()
    matches = pc.find_duplicates(
        [valid_document([row])], {"covered": {pc._doi_key(row["doi"]): {}}}, [row]
    )
    assert matches[0].source == "covered"
    assert matches[0].severity == "error"


def test_add_row_refuses_normalized_duplicate():
    document = valid_document()
    with pytest.raises(pc.ProposalError, match="duplicate DOI"):
        pc.add_row(document, valid_row(doi="HTTPS://DOI.ORG/10.1234/EXAMPLE.1."))


def test_add_row_sorts_by_normalized_doi_then_issue_and_updates_summary():
    document = valid_document([
        valid_row(doi="10.1234/a", source_issue=20),
        valid_row(doi="10.1234/a", source_issue=3),
    ])
    pc.add_row(document, valid_row(doi="10.1234/z", source_issue=1))
    pc.add_row(document, valid_row(doi=None))
    assert [(row["doi"], row["source_issue"]) for row in document["papers"]] == [
        ("10.1234/a", 3), ("10.1234/a", 20), ("10.1234/z", 1), (None, 42)
    ]
    assert document["summary"]["total"] == 4


def test_set_status_allows_candidate_hold_and_hold_included():
    document = valid_document()
    pc.set_status(document, "10.1234/EXAMPLE.1", "hold", "accept", "curator",
                  "2026-11-08", "Reviewed and queued.")
    pc.set_status(document, "10.1234/example.1", "included", "landed", "maintainer",
                  "2026-11-09", "Build landed in the collection.")
    row = document["papers"][0]
    assert row["status"] == "included"
    assert row["triage"]["curated_by"] == "maintainer"
    assert document["summary"]["included"] == 1


@pytest.mark.parametrize("terminal", ["rejected", "duplicate"])
def test_set_status_allows_terminal_dispositions_from_any_other_status(terminal):
    for current in pc.STATUSES:
        if current == terminal:
            continue
        document = valid_document([valid_row(status=current)])
        pc.set_status(document, "10.1234/example.1", terminal, terminal, "curator",
                      "2026-11-08", "Reason recorded.")
        assert document["papers"][0]["status"] == terminal


@pytest.mark.parametrize(
    ("current", "target"),
    [("candidate", "included"), ("hold", "candidate"), ("included", "hold"),
     ("rejected", "hold"), ("duplicate", "candidate"), ("hold", "hold")],
)
def test_set_status_refuses_disallowed_transitions(current, target):
    document = valid_document([valid_row(status=current)])
    with pytest.raises(pc.ProposalError, match="not allowed"):
        pc.set_status(document, "10.1234/example.1", target, "accept", "curator",
                      "2026-11-08", "Reason recorded.")


@pytest.mark.parametrize(
    ("doi", "decision", "by", "on", "notes"),
    [("10.1234/missing", "accept", "curator", "2026-11-08", "Reason"),
     ("bad", "accept", "curator", "2026-11-08", "Reason"),
     ("10.1234/example.1", "", "curator", "2026-11-08", "Reason"),
     ("10.1234/example.1", "accept", "", "2026-11-08", "Reason"),
     ("10.1234/example.1", "accept", "curator", "today", "Reason"),
     ("10.1234/example.1", "accept", "curator", "2026-11-08", "")],
)
def test_set_status_requires_identity_and_transition_evidence(doi, decision, by, on, notes):
    document = valid_document()
    with pytest.raises(pc.ProposalError):
        pc.set_status(document, doi, "hold", decision, by, on, notes)


def test_set_status_requires_exactly_one_match():
    document = valid_document([
        valid_row(), valid_row(doi="https://doi.org/10.1234/EXAMPLE.1")
    ])
    with pytest.raises(pc.ProposalError, match="exactly one"):
        pc.set_status(document, "10.1234/example.1", "hold", "accept", "curator",
                      "2026-11-08", "Reason recorded.")


@pytest.mark.parametrize("path", WAVES, ids=lambda path: path.name)
def test_live_wave_dump_is_canonical_and_idempotent(path):
    original = path.read_bytes()
    once = pc.dump(pc.load(path))
    twice = pc.dump(yaml.safe_load(once))
    assert once.encode() == twice.encode()
    assert yaml.safe_load(once) == pc.load(path)
    if original != once.encode():
        assert "#" not in once.split("source:", 1)[0]


def test_dump_key_order_block_style_and_no_aliases():
    shared = ["query one"]
    row = valid_row(source_queries=shared, priority_reasons=shared)
    document = valid_document([row])
    rendered = pc.dump(document)
    assert list(yaml.safe_load(rendered)) == list(pc.DOCUMENT_KEYS)
    assert "&id" not in rendered and "*id" not in rendered
    assert "papers:\n- name:" in rendered


def test_validate_cli_and_exit_code(capsys):
    paths = [str(path) for path in WAVES]
    assert pc.main(["validate", *paths]) == 0
    captured = capsys.readouterr()
    assert captured.out.count("OK") == 2


def test_validate_cli_reports_content_and_exits_one(tmp_path, capsys):
    path = tmp_path / "invalid.yaml"
    path.write_text(pc.dump(valid_document([valid_row(status="bad")])), encoding="utf-8")
    assert pc.main(["validate", str(path)]) == 1
    assert "papers[0].status" in capsys.readouterr().out


def test_summary_cli_write_is_canonical(tmp_path, capsys):
    path = tmp_path / "wave.yaml"
    document = valid_document()
    document["summary"] = {"total": 0}
    path.write_text(pc.dump(document), encoding="utf-8")
    assert pc.main(["summary", str(path)]) == 0
    assert document["summary"]["total"] == 0
    assert pc.main(["summary", str(path), "--write"]) == 0
    assert pc.load(path)["summary"] == pc.recompute_summary(valid_document())
    for line in capsys.readouterr().out.splitlines():
        assert json.loads(line.split(": ", 1)[1])["total"] == 1


def test_duplicate_cli_errors_and_repository_warnings(tmp_path, capsys):
    proposal = tmp_path / "wave.yaml"
    covered = tmp_path / "covered.json"
    corpus = tmp_path / "corpus.yaml"
    proposal.write_text(pc.dump(valid_document()), encoding="utf-8")
    covered.write_text(json.dumps({"covered": {pc._doi_key("10.1234/example.1"): {}}}),
                       encoding="utf-8")
    corpus.write_text(pc.dump(valid_document([])), encoding="utf-8")
    assert pc.main(["check-duplicates", "--covered", str(covered), "--corpus",
                    str(corpus), str(proposal)]) == 1
    assert "ERROR" in capsys.readouterr().out
    covered.write_text(json.dumps({"covered": {}}), encoding="utf-8")
    corpus.write_text(pc.dump(valid_document([valid_row(doi="10.1234/other")])),
                      encoding="utf-8")
    assert pc.main(["check-duplicates", "--covered", str(covered), "--corpus",
                    str(corpus), str(proposal)]) == 0
    assert "WARNING" in capsys.readouterr().out


def test_no_clock_or_cross_repository_import():
    source = pathlib.Path(pc.__file__).read_text(encoding="utf-8")
    assert "datetime.now" not in source
    assert "date.today" not in source
    assert "doi_utils" not in source
    assert copy.deepcopy(valid_document()) == valid_document()


def test_watch_row_may_leave_issue_and_repository_null() -> None:
    row = valid_row(status="candidate", source_issue=None, repo_url=None,
                    source_watch="2026-11-09")
    assert pc.validate({**valid_document(), "papers": [row]}) == []


def test_null_source_issue_requires_source_watch() -> None:
    row = valid_row(status="candidate", source_issue=None)
    paths = [violation.path for violation in pc.validate({**valid_document(), "papers": [row]})]
    assert "papers[0].source_issue" in paths


def test_null_repo_url_is_refused_on_a_held_row() -> None:
    row = valid_row(status="hold", repo_url=None, source_issue=7)
    paths = [violation.path for violation in pc.validate({**valid_document(), "papers": [row]})]
    assert "papers[0].repo_url" in paths
