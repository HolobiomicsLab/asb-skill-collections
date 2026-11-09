"""Offline contract tests for the Crossref retraction monitor."""

from __future__ import annotations

import io
import json
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

from scripts import check_retractions as retractions


REFERENCE_DATE = datetime(2026, 11, 8, tzinfo=timezone.utc)


def write_corpus(root: Path, domain: str, version: str, papers: list[dict]) -> Path:
    """Write one minimal corpus and return its path."""
    path = root / domain / version / "corpus.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump({"papers": papers}), encoding="utf-8")
    return path


def paper(doi: str | None, title: str = "Paper", status: str = "included") -> dict:
    """Build a corpus paper row."""
    return {"name": title.lower(), "doi": doi, "title": title, "status": status}


def response(message: dict) -> dict:
    """Wrap a Crossref message in its response envelope."""
    return {"message": message}


def run_scan(tmp_path: Path, fetch, papers: list[dict] | None = None) -> dict:
    """Scan one released fixture with an injected Crossref client."""
    collections = tmp_path / "collections"
    staged = tmp_path / "staged-collections"
    staged.mkdir()
    write_corpus(collections, "metabolomics", "v3", papers or [paper("10.1/clean")])
    return retractions.check_collections(
        collections, staged, fetch_json=fetch, sleep=lambda _: None
    )


def test_not_retracted_is_clean(tmp_path: Path):
    report = run_scan(tmp_path, lambda _: response({"title": ["Paper"]}))
    collection = report["collections"][0]
    assert collection["checked"] == ["10.1/clean"]
    assert collection["retracted"] == []
    assert collection["errors"] == []
    assert report["exit_code"] == 0


def test_update_to_retraction_includes_notice_and_date(tmp_path: Path):
    payload = response(
        {
            "title": ["Retracted paper"],
            "update-to": [
                {
                    "type": "retraction",
                    "DOI": "10.1/notice",
                    "updated": {"date-parts": [[2026, 10, 30]]},
                }
            ],
        }
    )
    report = run_scan(
        tmp_path, lambda _: payload, [paper("10.1/retracted", "Original title")]
    )
    hit = report["collections"][0]["retracted"][0]
    assert hit == {
        "doi": "10.1/retracted",
        "title": "Original title",
        "retraction_doi": "10.1/notice",
        "retraction_date": "2026-10-30",
        "source": "update-to",
    }
    assert report["exit_code"] == 1


def test_relation_retraction_is_detected(tmp_path: Path):
    payload = response(
        {"relation": {"is-retracted-by": [{"id-type": "doi", "id": "10.1/notice"}]}}
    )
    report = run_scan(tmp_path, lambda _: payload, [paper("10.1/relation")])
    hit = report["collections"][0]["retracted"][0]
    assert hit["retraction_doi"] == "10.1/notice"
    assert hit["retraction_date"] is None
    assert hit["source"] == "relation.is-retracted-by"
    assert report["exit_code"] == 1


def test_http_404_is_an_error_not_a_clean_result(tmp_path: Path):
    def fetch(url: str):
        raise urllib.error.HTTPError(url, 404, "Not Found", {}, io.BytesIO(b""))

    report = run_scan(tmp_path, fetch)
    error = report["collections"][0]["errors"][0]
    assert error["kind"] == "http"
    assert error["status"] == 404
    assert report["collections"][0]["checked"] == []
    assert report["exit_code"] == 2


def test_rate_limit_is_retried_with_retry_after(tmp_path: Path):
    calls = []

    def fetch(url: str):
        calls.append(url)
        if len(calls) == 1:
            raise urllib.error.HTTPError(
                url, 429, "Rate limited", {"Retry-After": "7"}, io.BytesIO(b"")
            )
        return response({})

    report = run_scan(tmp_path, fetch)
    assert len(calls) == 2
    assert report["exit_code"] == 0


def test_retry_delay_honours_retry_after_and_sleep_is_injectable(tmp_path: Path):
    calls = []
    sleeps = []

    def fetch(url: str):
        calls.append(url)
        if len(calls) == 1:
            raise urllib.error.HTTPError(
                url, 429, "Rate limited", {"Retry-After": "7"}, io.BytesIO(b"")
            )
        return response({})

    collections = tmp_path / "collections"
    staged = tmp_path / "staged-collections"
    staged.mkdir()
    write_corpus(collections, "metabolomics", "v3", [paper("10.1/rate-limit")])
    report = retractions.check_collections(
        collections, staged, fetch_json=fetch, sleep=sleeps.append
    )
    assert sleeps == [7.0]
    assert report["exit_code"] == 0


def test_timeout_exhausts_bounded_retries_and_blocks_completion(tmp_path: Path):
    calls = []

    def fetch(_: str):
        calls.append(True)
        raise TimeoutError("timed out")

    report = run_scan(tmp_path, fetch)
    assert len(calls) == retractions.MAX_ATTEMPTS
    error = report["collections"][0]["errors"][0]
    assert error["kind"] == "timeout"
    assert error["status"] is None
    assert report["exit_code"] == 2


def test_status_filter_missing_doi_and_both_roots(tmp_path: Path):
    collections = tmp_path / "collections"
    staged = tmp_path / "staged-collections"
    write_corpus(
        collections,
        "metabolomics",
        "v3",
        [
            paper("10.1/included"),
            paper("10.1/excluded", status="hold"),
            paper(None, "No DOI"),
        ],
    )
    write_corpus(
        staged, "metabolomics", "v4", [paper("10.1/accepted", status="accepted")]
    )
    report = retractions.check_collections(
        collections, staged, fetch_json=lambda _: response({}), sleep=lambda _: None
    )
    assert [(row["collection"], row["version"]) for row in report["collections"]] == [
        ("metabolomics", "v3"),
        ("metabolomics", "v4"),
    ]
    assert report["collections"][0]["checked"] == ["10.1/included"]
    assert report["collections"][0]["skipped"][0]["reason"] == "no_doi"
    assert report["collections"][1]["checked"] == ["10.1/accepted"]


def test_dry_run_does_not_fetch_and_preserves_pending_dois(tmp_path: Path):
    def fetch(_: str):
        raise AssertionError("dry-run must not fetch")

    collections = tmp_path / "collections"
    staged = tmp_path / "staged-collections"
    staged.mkdir()
    write_corpus(collections, "metabolomics", "v3", [paper("10.1/clean")])
    dry_report = retractions.check_collections(
        collections,
        staged,
        fetch_json=fetch,
        sleep=lambda _: None,
        dry_run=True,
    )
    assert dry_report["collections"][0]["pending"] == ["10.1/clean"]
    assert dry_report["exit_code"] == 0


def test_render_issue_has_stable_collection_marker():
    title, body = retractions.render_issue(
        "metabolomics",
        "v3",
        [
            {
                "doi": "10.1/retracted",
                "title": "Original title",
                "retraction_doi": "10.1/notice",
                "retraction_date": "2026-10-30",
            }
        ],
    )
    assert "metabolomics/v3" in title
    assert body.splitlines()[0] == "<!-- asb-retraction-watch: metabolomics/v3 -->"
    assert "10.1/notice" in body
    assert "2026-10-30" in body
    assert "reviewed release action" in body


def existing_issue(marker: bool, created_at: str, number: int = 42) -> dict:
    """Build an issue list row with the CLI's normalized date key."""
    body = (
        "<!-- asb-retraction-watch: metabolomics/v3 -->"
        if marker
        else "Same title, no marker"
    )
    return {
        "number": number,
        "title": "Retraction",
        "body": body,
        "created_at": created_at,
    }


def test_recent_matching_issue_gets_a_comment_command():
    commands = retractions.recommend_issue_commands(
        "metabolomics",
        "v3",
        [{"doi": "10.1/retracted", "title": "Paper"}],
        [existing_issue(True, "2026-10-20T00:00:00Z")],
        REFERENCE_DATE,
    )
    assert len(commands) == 1
    assert commands[0].startswith("gh issue comment 42 ")
    assert "issue create" not in commands[0]


@pytest.mark.parametrize(
    "issues",
    [
        [],
        [existing_issue(False, "2026-11-01T00:00:00Z")],
        [existing_issue(True, "2026-09-01T00:00:00Z")],
    ],
)
def test_missing_unmarked_or_old_issue_gets_a_create_command(issues):
    commands = retractions.recommend_issue_commands(
        "metabolomics",
        "v3",
        [{"doi": "10.1/retracted", "title": "Paper"}],
        issues,
        REFERENCE_DATE,
    )
    assert len(commands) == 1
    assert commands[0].startswith("gh issue create ")
    assert "--label retraction-watch" in commands[0]


def test_main_writes_machine_report_and_prints_recommended_command(
    tmp_path: Path, capsys
):
    collections = tmp_path / "collections"
    staged = tmp_path / "staged-collections"
    staged.mkdir()
    write_corpus(collections, "metabolomics", "v3", [])
    issues = tmp_path / "issues.json"
    issues.write_text(json.dumps([]), encoding="utf-8")
    report_path = tmp_path / "report.json"
    exit_code = retractions.main(
        [
            "--collections",
            str(collections),
            "--staged",
            str(staged),
            "--existing-issues",
            str(issues),
            "--report",
            str(report_path),
            "--dry-run",
            "--reference-date",
            "2026-11-08",
        ]
    )
    assert exit_code == 0
    assert json.loads(report_path.read_text(encoding="utf-8"))["exit_code"] == 0
    assert capsys.readouterr().out == ""


def test_main_returns_two_when_errors_accompany_a_retraction(
    tmp_path: Path, monkeypatch, capsys
):
    collections = tmp_path / "collections"
    staged = tmp_path / "staged-collections"
    staged.mkdir()
    write_corpus(
        collections,
        "metabolomics",
        "v3",
        [paper("10.1/retracted"), paper("10.1/error")],
    )

    def fetch(url: str):
        if "retracted" in url:
            return response(
                {"update-to": [{"type": "retraction", "DOI": "10.1/notice"}]}
            )
        raise urllib.error.HTTPError(url, 404, "Not Found", {}, io.BytesIO(b""))

    monkeypatch.setattr(
        retractions, "default_fetch_json", lambda url, user_agent: fetch(url)
    )
    exit_code = retractions.main(
        [
            "--collections",
            str(collections),
            "--staged",
            str(staged),
            "--reference-date",
            "2026-11-08",
        ]
    )
    assert exit_code == 2
    assert capsys.readouterr().out == ""


def test_workflow_yaml_parses_and_names_script():
    path = (
        Path(__file__).parent.parent
        / "scripts"
        / "templates"
        / "domain-retraction-watch.yml"
    )
    workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert workflow[True]["schedule"] == [{"cron": "0 6 1 * *"}]
    assert workflow["permissions"] == {"contents": "read", "issues": "write"}
    steps = workflow["jobs"]["retraction-watch"]["steps"]
    run_text = "\n".join(step.get("run", "") for step in steps)
    assert "check_retractions.py" in run_text
    assert "gh issue list" in run_text
    assert "<TOOLING_SHA>" in path.read_text(encoding="utf-8")
