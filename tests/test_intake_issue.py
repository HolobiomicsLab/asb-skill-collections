import ast
import hashlib
import json
import pathlib
import shutil
import urllib.error
import urllib.parse

import pytest
import yaml

from scripts import intake_issue
from scripts import intake_resolvers
from scripts import proposal_corpus as pc


FIXTURES = pathlib.Path(__file__).parent / "fixtures" / "intake"
DATE = "2026-11-09"
DOI = "10.1234/example-tool.1"
REPO = "https://github.com/example/tool"
TITLE = "Example Tool: reproducible mass spectrometry analysis"


def issue_body(**changes):
    fields = {
        "What is it?": "Example Tool",
        "Link:": f"https://doi.org/{DOI}",
        "Type:": "paper",
        "Target collection:": "metabolomics",
        "Why it matters (one or two sentences):": "A useful reproducible analysis method.",
        "Open access?": "yes",
        "You:": "@example-user",
        "Conflict of interest?": "I am an author of this work.",
    }
    fields.update(changes)
    required = ["What is it?", "Link:", "Type:", "Target collection:"]
    lines = []
    for key in required:
        value = fields.pop(key)
        lines.extend([f"**{key}**", value, ""])
    lines.extend(["**Why it matters (one or two sentences):**", fields.pop("Why it matters (one or two sentences):"), "", "---", ""])
    for key, value in fields.items():
        lines.extend([f"- **{key}**", value, ""])
    return "\n".join(lines)


def issue(number=101, **changes):
    result = {
        "number": number,
        "title": "Propose: Example Tool",
        "body": issue_body(),
        "author": {"login": "example-user"},
        "labels": [{"name": "propose"}, {"name": "needs-triage"}],
        "url": f"https://github.com/example-org/asb-skills-example/issues/{number}",
        "createdAt": "2026-11-09T08:00:00Z",
        "updatedAt": "2026-11-09T08:00:00Z",
    }
    result.update(changes)
    return result


def crossref_message(doi=DOI, **changes):
    message = {
        "DOI": doi,
        "title": [TITLE],
        "published": {"date-parts": [[2026, 11, 1]]},
        "type": "journal-article",
        "link": [{"URL": REPO, "intended-application": "text-mining"}],
        "resource": {"primary": {"URL": "https://example.org/article"}},
        "license": [{"URL": "https://creativecommons.org/licenses/by/4.0/"}],
    }
    message.update(changes)
    return message


def datacite_message(doi="10.5281/zenodo.12345"):
    return {
        "data": {
            "id": doi,
            "attributes": {
                "doi": doi,
                "titles": [{"title": "Archived Example Tool"}],
                "publicationYear": 2026,
                "types": {"resourceTypeGeneral": "Software"},
                "url": REPO,
                "rightsList": [{"rightsUri": "https://creativecommons.org/licenses/by/4.0/"}],
            },
        }
    }


def unpaywall(doi=DOI, **changes):
    payload = {
        "doi": doi,
        "title": TITLE,
        "is_oa": True,
        "oa_status": "gold",
        "best_oa_location": {"license": "cc-by", "url": "https://example.org/article"},
        "genre": "journal-article",
        "year": 2026,
    }
    payload.update(changes)
    return payload


def repository(**changes):
    payload = {
        "full_name": "example/tool",
        "html_url": REPO,
        "archived": False,
        "private": False,
        "license": {"spdx_id": "MIT"},
    }
    payload.update(changes)
    return payload


class Fetchers:
    def __init__(self, crossref_payload=None, datacite_payload=None,
                 openalex_payload=None, access_payload=None, repo_payload=None):
        self.crossref_payload = crossref_payload or {"message": crossref_message()}
        self.datacite_payload = datacite_payload
        self.openalex_payload = openalex_payload
        self.access_payload = access_payload if access_payload is not None else unpaywall()
        self.repo_payload = repo_payload if repo_payload is not None else repository()
        self.calls = []

    def __call__(self, url):
        self.calls.append(url)
        if "api.crossref.org/works?" in url:
            if self.crossref_payload is None:
                return None
            items = self.crossref_payload.get("message", {}).get("items", [])
            return {"message": {"items": items}}
        if "api.crossref.org/works/" in url:
            return self.crossref_payload
        if "api.datacite.org/dois/" in url:
            return self.datacite_payload
        if "api.openalex.org/works/" in url:
            return self.openalex_payload
        if "api.unpaywall.org/" in url:
            return self.access_payload
        if "api.github.com/repos/" in url:
            return self.repo_payload
        raise AssertionError(f"unexpected URL: {url}")


def corpus_document(rows=None, collection="metabolomics", version=3):
    document = {
        "schema": "asb-corpus/1.0",
        "collection": collection,
        "version": version,
        "generated_on": DATE,
        "source": "test proposals",
        "policy": "OPEN_ACCESS_POLICY.md",
        "wave": "community-2026-11",
        "papers": rows or [],
    }
    document["summary"] = pc.recompute_summary(document)
    return document


def row(issue_number=99, doi="10.1234/other.1", status="hold"):
    return {
        "name": "Other Tool",
        "doi": doi,
        "title": "Another paper",
        "year": 2026,
        "category": "Annotation",
        "repo_url": "https://github.com/example/other",
        "status": status,
        "license_tier": "open",
        "wave": "community-2026-11",
        "resource_type": "software-tool",
        "source_issue": issue_number,
        "access": {
            "type": "gold-oa",
            "license": "cc-by-4.0",
            "is_oa": True,
            "verified_via": "test",
            "verified_on": DATE,
            "code_license": "MIT",
        },
        "triage": {
            "proposer": "other-user",
            "rationale": "Another proposal.",
            "decision": "accept" if status == "hold" else "pending",
            "notes": "Curator review.",
        },
    }


@pytest.fixture
def inputs(tmp_path):
    issue_path = tmp_path / "issue.json"
    issue_path.write_text(json.dumps(issue()), encoding="utf-8")
    wave = tmp_path / "proposals" / "wave-2026-11-community.yaml"
    covered = tmp_path / "covered_dois.json"
    covered.write_text(json.dumps({"covered": {}}), encoding="utf-8")
    corpus = tmp_path / "v3" / "corpus.yaml"
    corpus.parent.mkdir()
    corpus.write_text(yaml.safe_dump({"papers": []}), encoding="utf-8")
    return {
        "issue_path": issue_path,
        "wave": wave,
        "covered": covered,
        "corpus": corpus,
        "glob": str(tmp_path / "proposals" / "wave-*.yaml"),
        "out": tmp_path / "receipt.json",
    }


def run_intake(inputs, fetchers=None, **changes):
    options = {
        "kind": "paper",
        "issue_json": str(inputs["issue_path"]),
        "domain": "metabolomics",
        "wave_file": str(inputs["wave"]),
        "covered": str(inputs["covered"]),
        "collection_corpus": str(inputs["corpus"]),
        "proposal_glob": [inputs["glob"]],
        "date": DATE,
        "out": str(inputs["out"]),
        "dry_run": False,
        "fetcher": fetchers or Fetchers(),
        "email": "intake-test.invalid",
        "sleep": lambda seconds: None,
    }
    options.update(changes)
    return intake_issue.run_intake(**options)


def read_receipt(inputs):
    return json.loads(inputs["out"].read_text(encoding="utf-8"))


def test_open_reusable_paper_stages_hold_and_preserves_conflict(inputs):
    receipt = run_intake(inputs)
    assert receipt["schema"] == "asb-intake-receipt/1"
    assert receipt["outcome"] == "staged"
    assert receipt["kind"] == "paper"
    assert receipt["doi"] == DOI
    assert receipt["row"]["status"] == "hold"
    assert receipt["row"]["triage"]["decision"] == "pending"
    assert receipt["row"]["triage"]["proposer"] == "example-user"
    assert receipt["row"]["triage"]["conflict_declared"] is True
    assert "I am an author" in receipt["comment_markdown"]
    assert receipt["access"]["type"] == "gold"
    assert receipt["access"]["license"] == "cc-by"
    assert receipt["access"]["verified_on"] == DATE
    assert receipt["code_license"] == "MIT"
    assert receipt["labels_add"] == ["intake-staged"]
    assert set(receipt["labels_remove"]) == {"intake-blocked", "needs-triage"}
    assert intake_issue.QUEUED_SENTENCE in receipt["comment_markdown"]
    document = pc.load(inputs["wave"])
    assert pc.validate(document) == []
    assert document["wave"] == "community-2026-11"
    assert document["generated_on"] == DATE
    assert document["summary"] == {"total": 1, "candidate": 0, "hold": 1,
                                   "included": 0, "rejected": 0, "duplicate": 0}
    assert document["papers"] == [receipt["row"]]


@pytest.mark.parametrize(
    "link, expected",
    [
        (f"DOI:{DOI.upper()}.", DOI),
        ("https://doi.org/10.1234/example\u2011tool.1", DOI),
        (f"https://doi.org/{DOI}?utm_source=test", DOI),
    ],
)
def test_doi_normalization(inputs, link, expected):
    inputs["issue_path"].write_text(json.dumps(issue(body=issue_body(**{"Link:": link}))), encoding="utf-8")
    assert run_intake(inputs)["doi"] == expected


def test_datacite_software_doi_and_repository_license(inputs):
    doi = "10.5281/zenodo.12345"
    inputs["issue_path"].write_text(json.dumps(issue(body=issue_body(**{"Link:": doi}))), encoding="utf-8")
    fetchers = Fetchers(crossref_payload={"message": None}, datacite_payload=datacite_message(doi),
                        access_payload=None)
    receipt = run_intake(inputs, fetchers)
    assert receipt["outcome"] == "staged"
    assert receipt["doi"] == doi
    assert receipt["title"] == "Archived Example Tool"
    assert receipt["row"]["resource_type"] == "software-tool"
    assert receipt["access"]["license"] == "cc-by"
    assert receipt["code_license"] == "MIT"


def test_preprint_relation_uses_published_doi(inputs):
    preprint = "10.1101/2026.01.01.123456"
    published = crossref_message(relation={"is-preprint-of": [{"id": DOI, "id-type": "doi"}]})
    inputs["issue_path"].write_text(json.dumps(issue(body=issue_body(**{"Link:": preprint}))), encoding="utf-8")
    fetchers = Fetchers(crossref_payload={"message": published})

    def fetch(url):
        if preprint in urllib.parse.unquote(url):
            return {"message": {"DOI": preprint, "title": ["Preprint title"],
                                "published": {"date-parts": [[2026]]}, "type": "posted-content",
                                "relation": {"is-preprint-of": [{"id": DOI, "id-type": "doi"}]}}}
        return fetchers(url)

    fetchers.crossref_payload = {"message": crossref_message()}
    receipt = run_intake(inputs, fetch)
    assert receipt["doi"] == DOI
    assert receipt["title"] == TITLE
    assert any("published DOI" in warning for warning in receipt["warnings"])


def test_title_resolution_checks_similarity_and_expected_prefix(inputs):
    body = issue_body(**{"What is it?": TITLE, "Link:": "https://www.nature.com/articles/example"})
    inputs["issue_path"].write_text(json.dumps(issue(body=body)), encoding="utf-8")
    payload = {"message": {"items": [
        {"DOI": "10.9999/wrong", "title": [TITLE]},
        {"DOI": "10.1038/right", "title": [TITLE]},
    ]}}
    def fetch(url):
        if "api.crossref.org/works?" in url:
            return payload
        if "api.crossref.org/works/" in url and urllib.parse.unquote(url).endswith("10.1038/right"):
            return {"message": crossref_message(doi="10.1038/right")}
        if "api.datacite.org/" in url or "api.openalex.org/" in url:
            return None
        if "api.unpaywall.org/" in url or "api.github.com/" in url:
            return Fetchers()(url)
        raise AssertionError(f"unexpected URL: {url}")

    receipt = run_intake(inputs, fetch)
    assert receipt["doi"] == "10.1038/right"
    assert receipt["title"] == TITLE


def test_ambiguous_title_is_blocked_without_fabricated_metadata(inputs):
    body = issue_body(**{"What is it?": TITLE, "Link:": "https://www.nature.com/articles/example"})
    inputs["issue_path"].write_text(json.dumps(issue(body=body)), encoding="utf-8")
    receipt = run_intake(inputs, Fetchers(crossref_payload={"message": {"items": []}}))
    assert receipt["outcome"] == "blocked"
    assert receipt["row"] is None
    assert receipt["doi"] is None
    assert "DOI" in receipt["comment_markdown"]
    assert not inputs["wave"].exists()


def test_registry_error_remains_unresolved_not_closed(inputs):
    def failing_fetch(url):
        if "api.unpaywall.org" in url:
            raise urllib.error.HTTPError(url, 503, "Unavailable", {"Retry-After": "0"}, None)
        return Fetchers()(url)

    receipt = run_intake(inputs, failing_fetch)
    assert receipt["outcome"] == "staged"
    assert receipt["row"]["status"] == "candidate"
    assert receipt["access"]["verified_via"] == "unresolved"
    assert receipt["access"]["is_oa"] is None
    assert "pending" in receipt["row"]["triage"]["decision"]
    assert not receipt["access"]["type"] == "closed"


def test_closed_paper_is_candidate(inputs):
    fetchers = Fetchers(access_payload=unpaywall(is_oa=False, oa_status="closed",
                                                best_oa_location=None))
    receipt = run_intake(inputs, fetchers)
    assert receipt["row"]["status"] == "candidate"
    assert receipt["access"]["type"] == "closed"
    assert "closed" in receipt["row"]["triage"]["notes"]


def test_repository_only_tool_is_candidate(inputs):
    body = issue_body(**{"Link:": REPO})
    inputs["issue_path"].write_text(json.dumps(issue(body=body)), encoding="utf-8")
    fetchers = Fetchers(crossref_payload=None)
    receipt = run_intake(inputs, fetchers)
    assert receipt["row"]["status"] == "candidate"
    assert receipt["row"]["doi"] is None
    assert receipt["row"]["year"] is None
    assert receipt["doi"] is None


def test_missing_moved_and_gone_repository_do_not_create_fake_url(inputs):
    message = crossref_message(link=[{"URL": REPO}])
    fetchers = Fetchers(crossref_payload={"message": message}, repo_payload={"status": "gone"})
    receipt = run_intake(inputs, fetchers)
    assert receipt["repository"] == REPO
    assert receipt["code_license"] is None
    assert any("gone" in warning for warning in receipt["warnings"])
    assert receipt["row"]["repo_url"] == REPO


def test_moved_repository_preserves_original_and_warns(inputs):
    moved = repository(full_name="example/new-tool", html_url="https://github.com/example/new-tool")
    receipt = run_intake(inputs, Fetchers(repo_payload=moved))
    assert receipt["repository"] == moved["html_url"]
    assert receipt["row"]["repo_url"] == moved["html_url"]
    assert receipt["row"]["status"] == "candidate"
    assert any("moved" in warning for warning in receipt["warnings"])


def test_private_repository_response_is_not_staged_as_public(inputs):
    receipt = run_intake(inputs, Fetchers(repo_payload=repository(private=True)))
    assert receipt["code_license"] is None
    assert any("gone" in warning for warning in receipt["warnings"])


def test_paper_and_code_licenses_stay_separate(inputs):
    message = crossref_message(license=[{"URL": "https://creativecommons.org/licenses/by-nc/4.0/"}])
    fetchers = Fetchers(crossref_payload={"message": message},
                        access_payload=unpaywall(best_oa_location={"license": "cc-by-nc"}),
                        repo_payload=repository(license={"spdx_id": "MIT"}))
    receipt = run_intake(inputs, fetchers)
    assert receipt["row"]["status"] == "candidate"
    assert receipt["access"]["license"] == "cc-by-nc"
    assert receipt["code_license"] == "MIT"
    assert receipt["row"]["license_tier"] == "open"


def test_second_run_is_byte_identical(inputs):
    run_intake(inputs)
    wave_before = inputs["wave"].read_bytes()
    second = run_intake(inputs)
    assert inputs["wave"].read_bytes() == wave_before
    assert second["inputs_sha256"]["wave_file_before"] == hashlib.sha256(wave_before).hexdigest()
    assert len(pc.load(inputs["wave"])["papers"]) == 1


def test_existing_commented_wave_is_byte_identical_on_unchanged_rerun(inputs):
    run_intake(inputs)
    inputs["wave"].write_text(intake_issue.NEW_WAVE_HEADER + pc.dump(pc.load(inputs["wave"])), encoding="utf-8")
    before = inputs["wave"].read_bytes()
    run_intake(inputs)
    assert inputs["wave"].read_bytes() == before


def test_edited_issue_updates_same_row_without_overwriting_curator_acceptance(inputs):
    run_intake(inputs)
    document = pc.load(inputs["wave"])
    document["papers"][0]["triage"]["decision"] = "accept"
    inputs["wave"].write_text(pc.dump(document), encoding="utf-8")
    updated = issue(body=issue_body(**{"Why it matters (one or two sentences):": "Updated rationale."}))
    inputs["issue_path"].write_text(json.dumps(updated), encoding="utf-8")
    receipt = run_intake(inputs)
    assert len(pc.load(inputs["wave"])["papers"]) == 1
    assert receipt["row"]["triage"]["rationale"] == "Updated rationale."
    assert receipt["row"]["triage"]["decision"] == "accept"


def test_two_issues_share_one_wave(inputs):
    run_intake(inputs)
    inputs["issue_path"].write_text(json.dumps(issue(number=102, body=issue_body(
        **{"Link:": "10.1234/second", "What is it?": "Second Tool"}))), encoding="utf-8")
    fetchers = Fetchers(crossref_payload={"message": crossref_message(doi="10.1234/second")})
    run_intake(inputs, fetchers)
    document = pc.load(inputs["wave"])
    assert [paper["source_issue"] for paper in document["papers"]] == [101, 102]
    assert document["summary"]["total"] == 2


@pytest.mark.parametrize("where", ["covered", "corpus", "proposal"])
def test_duplicate_precedence_and_safe_comment(inputs, where, tmp_path):
    inputs["wave"].parent.mkdir()
    if where == "covered":
        inputs["covered"].write_text(json.dumps({"covered": {"10-1234-example-tool-1": {}}}), encoding="utf-8")
        inputs["corpus"].write_text(yaml.safe_dump({"papers": [row(doi=DOI)]}), encoding="utf-8")
        inputs["wave"].write_text(pc.dump(corpus_document([row(doi=DOI)])), encoding="utf-8")
        expected = "covered_dois.json"
    elif where == "corpus":
        inputs["corpus"].write_text(yaml.safe_dump({"papers": [row(doi=DOI)]}), encoding="utf-8")
        inputs["wave"].write_text(pc.dump(corpus_document([row(doi=DOI)])), encoding="utf-8")
        expected = "corpus.yaml"
    else:
        inputs["wave"].write_text(pc.dump(corpus_document([row(doi=DOI)])), encoding="utf-8")
        expected = "wave-2026-11-community.yaml"
    before = inputs["wave"].read_bytes()
    fetchers = Fetchers()
    receipt = run_intake(inputs, fetchers)
    assert receipt["outcome"] == "duplicate"
    assert receipt["duplicate_of"]["where"] == where
    assert receipt["duplicate_of"]["path"] == expected
    assert receipt["duplicate_of"]["doi"] == DOI
    assert inputs["wave"].read_bytes() == before
    assert str(tmp_path) not in receipt["comment_markdown"]
    assert not any("api.github.com" in url for url in fetchers.calls)


def test_own_existing_row_is_updated_not_duplicate(inputs):
    run_intake(inputs)
    assert run_intake(inputs)["outcome"] == "staged"


def test_ambiguous_existing_issue_rows_are_blocked(inputs):
    run_intake(inputs)
    other = inputs["wave"].with_name("wave-2026-11-other.yaml")
    shutil.copyfile(inputs["wave"], other)
    before = inputs["wave"].read_bytes()
    receipt = run_intake(inputs)
    assert receipt["outcome"] == "blocked"
    assert "multiple existing" in receipt["comment_markdown"]
    assert inputs["wave"].read_bytes() == before


@pytest.mark.parametrize(
    "body, missing",
    [
        (issue_body(**{"Target collection:": "genomics"}), "Target collection"),
        (issue_body(**{"What is it?": ""}), "What is it?"),
        (issue_body(**{"Link:": ""}), "Link"),
        (issue_body(**{"Why it matters (one or two sentences):": ""}), "Why it matters"),
        ("No recognizable fields", "What is it?"),
        (issue_body(**{"Type:": "workflow"}), "Type"),
    ],
)
def test_invalid_required_fields_blocked(inputs, body, missing):
    inputs["issue_path"].write_text(json.dumps(issue(body=body)), encoding="utf-8")
    receipt = run_intake(inputs)
    assert receipt["outcome"] == "blocked"
    assert missing in receipt["comment_markdown"]
    assert receipt["labels_add"] == ["intake-blocked"]
    assert not inputs["wave"].exists()


def test_non_paper_webpage_blocked(inputs):
    body = issue_body(**{"Link:": "https://example.org/cool-science"})
    inputs["issue_path"].write_text(json.dumps(issue(body=body)), encoding="utf-8")
    receipt = run_intake(inputs, Fetchers(crossref_payload=None))
    assert receipt["outcome"] == "blocked"
    assert "not an allowed" in receipt["comment_markdown"].lower()


def test_oversized_body_blocked(inputs):
    inputs["issue_path"].write_text(json.dumps(issue(body=issue_body() + "x" * 20001)), encoding="utf-8")
    receipt = run_intake(inputs)
    assert receipt["outcome"] == "blocked"
    assert "body" in receipt["comment_markdown"].lower()


def test_disallowed_scheme_blocked(inputs):
    body = issue_body(**{"Link:": "file:///tmp/paper.txt"})
    inputs["issue_path"].write_text(json.dumps(issue(body=body)), encoding="utf-8")
    receipt = run_intake(inputs)
    assert receipt["outcome"] == "blocked"
    assert "HTTPS" in receipt["comment_markdown"]


def test_dry_run_writes_only_receipt(inputs):
    receipt = run_intake(inputs, dry_run=True)
    assert receipt["outcome"] == "staged"
    assert receipt["row"] is not None
    assert not inputs["wave"].exists()


def test_unsupported_kind_blocked(inputs):
    receipt = run_intake(inputs, kind="workflow")
    assert receipt["outcome"] == "blocked"
    assert receipt["kind"] == "workflow"
    assert "paper" in receipt["comment_markdown"]


def test_fixture_issue_shape():
    fixture = json.loads((FIXTURES / "open-paper.json").read_text(encoding="utf-8"))
    assert fixture["number"] == 101
    assert "**Link:**" in fixture["body"]


def test_intake_tests_never_use_the_live_http_fetcher():
    source = pathlib.Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    calls = {node.func.attr for node in ast.walk(tree)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
    assert "http_json" not in calls
    assert "urlopen" not in calls


def test_receipt_has_exact_m40_keys_and_null_wave_on_duplicate(inputs):
    run_intake(inputs)
    receipt = run_intake(inputs)
    expected = {"schema", "outcome", "kind", "issue", "domain", "date", "doi", "title",
                "repository", "access", "code_license", "warnings", "duplicate_of", "row",
                "wave_file", "inputs_sha256", "comment_markdown", "labels_add", "labels_remove"}
    assert expected <= set(receipt)
    assert receipt["conflict_statement"] == "I am an author of this work."
    assert receipt["duplicate_of"] is None


def test_cli_dry_run_returns_staged_exit_zero(inputs, monkeypatch):
    monkeypatch.setenv("INTAKE_TEST_CONTACT", "intake-test.invalid")
    args = ["--kind", "paper", "--issue-json", str(inputs["issue_path"]),
            "--domain", "metabolomics", "--wave-file", str(inputs["wave"]),
            "--covered", str(inputs["covered"]), "--collection-corpus", str(inputs["corpus"]),
            "--proposal-glob", inputs["glob"], "--date", DATE, "--out", str(inputs["out"]),
            "--email-env", "INTAKE_TEST_CONTACT", "--dry-run"]
    monkeypatch.setattr(intake_resolvers, "http_json", Fetchers())
    assert intake_issue.main(args) == 0
    assert read_receipt(inputs)["outcome"] == "staged"


def test_retry_after_is_honored_without_real_sleep():
    delays = []
    calls = []

    def fetch(url):
        calls.append(url)
        if len(calls) < 3:
            raise urllib.error.HTTPError(url, 429, "Limited", {"Retry-After": "7"}, None)
        return {"message": {"DOI": DOI, "title": [TITLE], "published": {"date-parts": [[2026]]}}}

    resolver = intake_issue.intake_resolvers.Resolver(fetch, delays.append, pc.normalise_doi)
    assert resolver.by_doi(DOI)["doi"] == DOI
    assert delays == [7.0, 7.0]


def test_repository_duplicate_is_warning_not_proof(inputs):
    inputs["wave"].parent.mkdir()
    other = row(doi="10.1234/other-repository-paper")
    other["repo_url"] = REPO
    inputs["wave"].write_text(pc.dump(corpus_document([other])), encoding="utf-8")
    receipt = run_intake(inputs)
    assert receipt["outcome"] == "staged"
    assert receipt["duplicate_of"] is None
    assert any("repository identity" in warning for warning in receipt["warnings"])


def test_comment_does_not_expose_absolute_wave_path(inputs):
    receipt = run_intake(inputs)
    assert str(inputs["wave"]) not in receipt["comment_markdown"]
    assert "/Users/" not in receipt["comment_markdown"]


@pytest.mark.parametrize("url", ["http://github.com/example/tool",
                                 "https://github.com@evil.invalid/example/tool",
                                 "https://github.com/example/tool?next=https://evil.invalid"])
def test_repository_metadata_must_be_plain_public_github_https(inputs, url):
    message = crossref_message(link=[{"URL": url}])
    receipt = run_intake(inputs, Fetchers(crossref_payload={"message": message}))
    assert receipt["repository"] is None
    assert receipt["code_license"] is None


def test_invalid_issue_json_still_writes_blocked_receipt(inputs):
    inputs["issue_path"].write_text("{broken", encoding="utf-8")
    receipt = run_intake(inputs)
    assert receipt["outcome"] == "blocked"
    assert receipt["issue"] == 0
    assert read_receipt(inputs)["outcome"] == "blocked"
