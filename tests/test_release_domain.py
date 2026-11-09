"""Offline contract tests for the staged domain release orchestrator."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import asb_skill_collections
from scripts import release_domain, zenodo_deposit

REPO = Path(__file__).resolve().parent.parent
FIXTURE = REPO / "tests" / "fixtures" / "router_collection"
PYTHON = Path(sys.executable)
NOW = "2026-11-09T10:11:12Z"
DOI = "10.5281/zenodo.1234567"
CONCEPT_DOI = "10.5281/zenodo.1234566"


def run_git(repo: Path, *arguments: str) -> None:
    subprocess.run(["git", *arguments], cwd=repo, check=True, capture_output=True)


def commit_all(repo: Path, message: str = "fixture") -> str:
    run_git(repo, "add", "-A")
    run_git(repo, "commit", "-m", message)
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()


def make_tooling(root: Path) -> Path:
    tooling = root / "tooling"
    shutil.copytree(REPO / "scripts", tooling / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(
        Path(asb_skill_collections.__file__).parent, tooling / "asb_skill_collections",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    shutil.copy2(REPO / "AGENTS.md", tooling / "AGENTS.md")
    shutil.copytree(REPO / "governance", tooling / "governance")
    (tooling / "scripts" / "release_creators.yaml").write_text(
        "creators:\n- family: Doe\n  given: Jane\n  orcid: 0000-0000-0000-0000\n"
    )
    (tooling / "docs-site").mkdir()
    shutil.copy2(REPO / "docs-site" / "build_search_index.py", tooling / "docs-site" / "build_search_index.py")
    (tooling / "collections.yaml").write_text("schema: asb-collections-manifest/1\ndomains: {}\n")
    (tooling / "catalogue.jsonld").write_text('{"@context": {}, "collections": []}\n')
    return tooling


def make_domain(root: Path) -> Path:
    domain = root / "domain"
    collection = domain / "collections" / "fixture" / "v1"
    shutil.copytree(FIXTURE, collection)
    for leaf in (collection / "leaves").glob("*/SKILL.md"):
        document = yaml.safe_load(leaf.read_text().split("---", 2)[1])
        document["license"] = "CC-BY-4.0"
        document["evidence_spans"] = [{"doi": "10.9999/asb-fixture-1", "text": "Synthetic fixture evidence."}]
        leaf.write_text("---\n" + yaml.safe_dump(document, sort_keys=False) + "---\n# Fixture procedure\n")
    (domain / "LICENSE").write_text("Apache-2.0\n")
    (domain / "LICENSING.md").write_text("Collection content: CC-BY-4.0\n")
    (collection / ".zenodo.json").write_text(json.dumps({
        "title": "ASB Fixture Skill Collection v1",
        "upload_type": "dataset",
        "description": "A compact fixture collection.",
        "access_right": "open",
        "license": "cc-by-4.0",
        "version": "v1.0.0",
        "creators": [{"name": "Doe, Jane", "orcid": "0000-0000-0000-0000"}],
        "related_identifiers": [{
            "relation": "isVersionOf", "identifier": "10.5281/zenodo.55", "scheme": "doi",
        }],
    }))
    (collection / "CITATION.cff").write_text(
        "cff-version: 1.2.0\ntitle: ASB Fixture Skill Collection v1\n"
        "version: '1'\ntype: dataset\nn_skills: 10\nn_tools: 10\nn_workflows: 5\nn_papers: 1\nn_dois: 1\n"
        "authors:\n- family-names: Doe\n  given-names: Jane\n"
    )
    (collection / "USAGE.md").write_text(
        "# Usage\n\n## Citation\n\nCite both:\n\n"
        "1. **The collection**, using v1's `CITATION.cff` and its version DOI, `PENDING`.\n"
        "2. **Every source paper**, through its DOI.\n"
    )
    (domain / "CITATION.cff").write_text(
        "cff-version: 1.2.0\ntitle: ASB Fixture Skill Collection\ntype: dataset\n"
        "authors:\n- family-names: Doe\n  given-names: Jane\n"
    )
    (domain / "README.md").write_text(
        "# Fixture\n\n## Collections\n\n"
        "| Path | Title | Skills | Tools | Released | DOI |\n"
        "|---|---|---|---|---|---|\n"
        "| `collections/fixture/v1` | ASB Fixture Skill Collection v1 | 10 | 10 | PENDING | PENDING |\n"
    )
    receipts = domain / "receipts" / "fixture"
    receipts.mkdir(parents=True)
    (receipts / "source.json").write_text(json.dumps({
        "domain": "fixture", "version": "v1", "cut_id": "fixture", "receipts": ["source.json"],
    }))
    run_git(domain, "init", "-b", "main")
    run_git(domain, "config", "user.name", "Fixture")
    run_git(domain, "config", "user.email", "fixture@example.invalid")
    commit_all(domain)
    return domain


@pytest.fixture
def release_fixture(tmp_path: Path) -> argparse.Namespace:
    domain = make_domain(tmp_path)
    tooling = make_tooling(tmp_path)
    return argparse.Namespace(
        repo=domain,
        tooling=tooling,
        state=tmp_path / "release_state.json",
        argv=lambda stage, *extra: [
            stage, "--domain", "fixture", "--version", "v1", "--repo-root", str(domain),
            "--tooling-root", str(tooling), "--state", str(tmp_path / "release_state.json"),
            *extra,
        ],
    )


@pytest.fixture(autouse=True)
def fake_tokens(monkeypatch) -> None:
    monkeypatch.setenv("ZENODO_TOKEN", "fixture-production-token")
    monkeypatch.setenv("ZENODO_SANDBOX_TOKEN", "fixture-sandbox-token")


class FakeZenodo:
    """Scripted deposit responses with an observable request journal."""

    def __init__(self, *, pending: bool, failure: int | None = None,
                 first_release_pending: bool = False, record_failure: int | None = None,
                 pending_page: int = 1) -> None:
        self.pending = pending
        self.pending_page = pending_page
        self.failure = failure
        self.record_failure = record_failure
        self.first_release_pending = first_release_pending
        self.calls: list[tuple[str, str, object]] = []
        self.metadata: dict = {"dates": [{"type": "collected", "description": "undated"}]}

    def __call__(self, method: str, url: str, token: str, body: object = None):
        self.calls.append((method, url, body))
        if self.failure:
            return self.failure, {"message": "scripted refusal"}
        base = f"{zenodo_deposit.ZENODO_URL}/api/deposit/depositions"
        if method == "GET" and url == f"{base}?status=draft":
            candidates = [{
                "id": 88, "conceptrecid": "999", "state": "unsubmitted",
                "metadata": {"title": "Another title", "version": "v1.0.0"},
                "links": {"self": f"{base}/88"},
            }]
            if self.first_release_pending:
                candidates.append(self.first_release_draft())
            if self.pending and self.pending_page == 1:
                candidates.append(self.draft())
            return 200, candidates
        if method == "GET" and url.startswith(f"{base}?status=draft&page="):
            page = int(url.rsplit("=", 1)[-1])
            if self.pending and self.pending_page == page:
                return 200, [self.draft()]
            return 200, []
        if method == "POST" and url == base:
            return 201, self.first_release_draft()
        if method == "POST" and url.endswith("/actions/newversion"):
            return 201, {"links": {"latest_draft": f"{base}/77"}}
        if method == "GET" and url == f"{base}/77":
            return 200, self.first_release_draft() if self.first_release_pending else self.draft()
        if method == "DELETE" and "/files/" in url:
            return 204, None
        if method == "PUT" and "/bucket/" in url:
            return 201, {"key": url.rsplit("/", 1)[-1]}
        if method == "PUT" and url == f"{base}/77":
            self.metadata = body["metadata"]
            return 200, self.draft()
        if method == "GET" and url.startswith(f"{zenodo_deposit.ZENODO_URL}/api/records/"):
            if self.record_failure:
                return self.record_failure, {"message": "scripted refusal"}
            return 200, {
                "id": 1234567, "doi": DOI, "conceptdoi": CONCEPT_DOI,
                "conceptrecid": "1234566", "metadata": {"version": "v1.0.0"},
            }
        raise AssertionError(f"unexpected deposit request: {method} {url}")

    def draft(self) -> dict:
        base = f"{zenodo_deposit.ZENODO_URL}/api/deposit/depositions"
        return {
            "id": 77,
            "conceptrecid": "1234566",
            "state": "unsubmitted",
            "metadata": self.metadata,
            "files": [{"id": "old-file"}],
            "links": {"bucket": f"{base}/77/bucket", "html": f"{zenodo_deposit.ZENODO_URL}/deposit/77"},
        }

    def first_release_draft(self) -> dict:
        draft = self.draft()
        draft.update(
            conceptrecid="456",
            metadata={"title": "ASB Fixture Skill Collection v1", "version": "v1.0.0"},
        )
        return draft


def seed_state(namespace: argparse.Namespace, stages: dict, **values) -> None:
    namespace.state.write_text(json.dumps({
        "schema": "asb-release-state/1", "domain": "fixture", "version": "v1",
        "stages": stages, **values,
    }))


def invoke(namespace: argparse.Namespace, stage: str, *extra: str, fake=None) -> int:
    options = list(extra)
    if (stage in {"deposit-plan", "deposit-draft"} and "--record-id" not in options
            and "--first-release" not in options):
        options.extend(["--record-id", "55"])
    return release_domain.main(
        namespace.argv(stage, *options),
        now=lambda: NOW,
        request=fake,
        runner=release_domain.SubprocessRunner(),
    )


def test_resume_runs_in_order_and_skips_unchanged_stages(release_fixture, capsys) -> None:
    code = release_domain.main(
        release_fixture.argv("gate", "--resume", "--record-id", "55"), now=lambda: NOW,
        request=FakeZenodo(pending=True), runner=release_domain.SubprocessRunner(),
    )
    assert code == 2
    state = json.loads(release_fixture.state.read_text())
    assert [name for name, record in state["stages"].items()
            if record["status"] in {"done", "waiting"}] == ["gate", "deposit-plan", "deposit-draft"]
    assert state["stages"]["deposit-draft"]["status"] == "waiting"
    assert "OWNER: publish" in capsys.readouterr().out
    assert invoke(release_fixture, "gate") == 0
    assert "unchanged; no-op" in capsys.readouterr().out


def test_record_doi_is_byte_stable_and_updates_all_release_surfaces(release_fixture) -> None:
    before = (release_fixture.repo / "collections/fixture/v1/.zenodo.json").read_bytes()
    arguments = ("--doi", DOI, "--released", "2026-11-09")
    seed_state(release_fixture, {"deposit-draft": {"status": "waiting"}})
    assert invoke(release_fixture, "record-doi", *arguments) == 0
    paths = [
        release_fixture.repo / "collections/fixture/v1/CITATION.cff",
        release_fixture.repo / "CITATION.cff",
        release_fixture.repo / "README.md",
        release_fixture.repo / "collections/fixture/v1/USAGE.md",
    ]
    snapshot = {path: path.read_bytes() for path in paths}
    assert all(DOI.encode() in content for content in snapshot.values())
    assert (release_fixture.repo / "collections/fixture/v1/.zenodo.json").read_bytes() == before
    assert invoke(release_fixture, "record-doi", *arguments, "--force") == 0
    assert {path: path.read_bytes() for path in paths} == snapshot


def test_deposit_draft_reuses_pending_draft_and_never_creates_another(release_fixture) -> None:
    assert invoke(release_fixture, "deposit-plan", "--record-id", "55") == 0
    fake = FakeZenodo(pending=True)
    assert invoke(release_fixture, "deposit-draft", "--record-id", "55", fake=fake) == 2
    methods = [(method, url.rsplit("/", 2)[-2:]) for method, url, _ in fake.calls]
    assert not any(method == "POST" and url.endswith("/actions/newversion") for method, url, _ in fake.calls)
    assert any(method == "DELETE" for method, _ in methods)
    assert any(method == "PUT" and url.endswith("/77") for method, url, _ in fake.calls)
    assert not any("publish" in url for _, url, _ in fake.calls)
    assert fake.metadata.get("dates") is None


def test_new_version_lookup_uses_drafts_of_the_record_concept(release_fixture) -> None:
    assert invoke(release_fixture, "deposit-plan", "--record-id", "55") == 0
    fake = FakeZenodo(pending=True, pending_page=2)
    assert invoke(release_fixture, "deposit-draft", "--record-id", "55", fake=fake) == 2
    urls = [url for _, url, _ in fake.calls]
    assert not any(url.endswith("/versions") for url in urls)
    assert any(url.endswith("/api/records/55") for url in urls)
    assert not any(url.endswith("/actions/newversion") for url in urls)


def test_a_draft_of_another_concept_is_not_reused(release_fixture) -> None:
    assert invoke(release_fixture, "deposit-plan", "--record-id", "55") == 0
    fake = FakeZenodo(pending=False)
    assert invoke(release_fixture, "deposit-draft", "--record-id", "55", fake=fake) == 2
    assert any(method == "POST" and url.endswith("/actions/newversion") for method, url, _ in fake.calls)


def test_deposit_draft_creates_first_draft_and_propagates_refusals(release_fixture) -> None:
    assert invoke(release_fixture, "deposit-plan", "--record-id", "55") == 0
    assert invoke(release_fixture, "deposit-draft", "--record-id", "55", fake=FakeZenodo(pending=False)) == 2
    assert invoke(release_fixture, "deposit-plan", "--record-id", "55", "--force") == 0
    assert invoke(release_fixture, "deposit-draft", "--record-id", "55", fake=FakeZenodo(pending=False, failure=403)) == 1


def test_deposit_plan_first_release_records_no_record_and_refuses_a_lineage(release_fixture) -> None:
    assert invoke(release_fixture, "deposit-plan", "--first-release") == 0
    state = json.loads(release_fixture.state.read_text())
    outputs = state["stages"]["deposit-plan"]["outputs"]
    assert outputs["record_id"] is None
    assert outputs["first_release"] is True
    registry = release_fixture.tooling / "collections.yaml"
    registry.write_text(yaml.safe_dump({
        "schema": "asb-collections-manifest/1",
        "domains": {"fixture": {"concept_doi": CONCEPT_DOI, "releases": []}},
    }))
    assert invoke(release_fixture, "deposit-plan", "--first-release", "--force") == 1


def test_deposit_draft_first_release_creates_and_reports_owner_steps(release_fixture, capsys) -> None:
    assert invoke(release_fixture, "deposit-plan", "--first-release") == 0
    fake = FakeZenodo(pending=False)
    assert invoke(release_fixture, "deposit-draft", "--first-release", fake=fake) == 2
    assert any(method == "POST" and url.endswith("/api/deposit/depositions")
               for method, url, _ in fake.calls)
    assert not any("newversion" in url or "publish" in url for _, url, _ in fake.calls)
    state = json.loads(release_fixture.state.read_text())
    outputs = state["stages"]["deposit-draft"]["outputs"]
    assert outputs == {
        "draft_url": f"{zenodo_deposit.ZENODO_URL}/deposit/77", "draft_id": "77",
        "reused": False, "conceptrecid": "456", "first_release": True,
    }
    assert "publishing mints both the version DOI and the concept DOI" in capsys.readouterr().out


def test_deposit_draft_first_release_reuses_matching_title_and_version(release_fixture) -> None:
    assert invoke(release_fixture, "deposit-plan", "--first-release") == 0
    fake = FakeZenodo(pending=False, first_release_pending=True)
    assert invoke(release_fixture, "deposit-draft", "--first-release", fake=fake) == 2
    assert not any(method == "POST" for method, _, _ in fake.calls)
    assert any(method == "GET" and url.endswith("?status=draft") for method, url, _ in fake.calls)
    state = json.loads(release_fixture.state.read_text())
    assert state["stages"]["deposit-draft"]["outputs"]["reused"] is True


def test_deposit_draft_refuses_an_archive_digest_mismatch(release_fixture) -> None:
    assert invoke(release_fixture, "deposit-plan", "--record-id", "55") == 0
    (release_fixture.repo / "collections/fixture/v1/collection.yaml").write_text("changed: true\n")
    assert invoke(release_fixture, "deposit-draft", "--record-id", "55", fake=FakeZenodo(pending=True)) == 1


def test_manifest_row_passes_the_real_checker_and_regen(release_fixture) -> None:
    stages = {
        "record-doi": {"status": "done", "inputs": {"doi": DOI}},
        "receipt": {"status": "done"},
    }
    seed_state(release_fixture, stages, doi=DOI)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=release_fixture.repo, text=True).strip()
    assert invoke(release_fixture, "manifest", "--concept-doi", CONCEPT_DOI, "--regen", "--commit", commit) == 0


def test_manifest_records_concept_doi_for_a_null_first_release_lineage(release_fixture) -> None:
    registry = release_fixture.tooling / "collections.yaml"
    registry.write_text(yaml.safe_dump({
        "schema": "asb-collections-manifest/1",
        "domains": {"fixture": {
            "repository": "Example/fixture", "concept_doi": None, "releases": [],
        }},
    }))
    seed_state(release_fixture, {"deposit-draft": {"status": "waiting"}})
    assert invoke(release_fixture, "record-doi", "--doi", DOI) == 0
    assert invoke(release_fixture, "receipt") == 0
    commit = commit_all(release_fixture.repo, "first release DOI")
    assert invoke(release_fixture, "manifest", "--concept-doi", CONCEPT_DOI, "--commit", commit) == 0
    document = yaml.safe_load(registry.read_text())
    assert document["domains"]["fixture"]["concept_doi"] == CONCEPT_DOI


def test_record_doi_first_release_prints_and_stores_the_concept_doi(release_fixture, capsys) -> None:
    seed_state(release_fixture, {"deposit-draft": {
        "status": "waiting", "outputs": {"first_release": True},
    }})
    fake = FakeZenodo(pending=False)
    assert invoke(release_fixture, "record-doi", "--doi", DOI, fake=fake) == 0
    output = capsys.readouterr().out
    assert f"concept DOI {CONCEPT_DOI} (record 1234566)" in output
    assert f"next: manifest --concept-doi {CONCEPT_DOI}" in output
    assert ("GET", f"{zenodo_deposit.ZENODO_URL}/api/records/1234567", None) in fake.calls
    state = json.loads(release_fixture.state.read_text())
    outputs = state["stages"]["record-doi"]["outputs"]
    assert outputs["concept_doi"] == CONCEPT_DOI
    assert outputs["conceptrecid"] == "1234566"


def test_manifest_defaults_concept_doi_from_the_record_doi_stage(release_fixture) -> None:
    registry = release_fixture.tooling / "collections.yaml"
    registry.write_text(yaml.safe_dump({
        "schema": "asb-collections-manifest/1",
        "domains": {"fixture": {
            "repository": "Example/fixture", "concept_doi": None, "releases": [],
        }},
    }))
    seed_state(release_fixture, {"deposit-draft": {
        "status": "waiting", "outputs": {"first_release": True},
    }})
    assert invoke(release_fixture, "record-doi", "--doi", DOI, fake=FakeZenodo(pending=False)) == 0
    assert invoke(release_fixture, "receipt") == 0
    commit = commit_all(release_fixture.repo, "first release DOI")
    assert invoke(release_fixture, "manifest", "--commit", commit) == 0
    document = yaml.safe_load(registry.read_text())
    assert document["domains"]["fixture"]["concept_doi"] == CONCEPT_DOI


def test_manifest_explicit_concept_doi_wins_over_the_stage_log(release_fixture) -> None:
    registry = release_fixture.tooling / "collections.yaml"
    registry.write_text(yaml.safe_dump({
        "schema": "asb-collections-manifest/1",
        "domains": {"fixture": {
            "repository": "Example/fixture", "concept_doi": None, "releases": [],
        }},
    }))
    seed_state(release_fixture, {
        "record-doi": {"status": "done", "inputs": {"doi": DOI},
                       "outputs": {"concept_doi": CONCEPT_DOI}},
        "receipt": {"status": "done"},
    }, doi=DOI)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=release_fixture.repo, text=True).strip()
    explicit = "10.5281/zenodo.9999999"
    assert invoke(release_fixture, "manifest", "--concept-doi", explicit, "--commit", commit) == 0
    document = yaml.safe_load(registry.read_text())
    assert document["domains"]["fixture"]["concept_doi"] == explicit


def test_record_doi_non_first_release_does_not_read_a_record(release_fixture, capsys) -> None:
    seed_state(release_fixture, {"deposit-draft": {"status": "waiting", "outputs": {}}})
    fake = FakeZenodo(pending=False)
    assert invoke(release_fixture, "record-doi", "--doi", DOI, fake=fake) == 0
    assert not any("/api/records/" in url for _, url, _ in fake.calls)
    assert "concept DOI" not in capsys.readouterr().out
    state = json.loads(release_fixture.state.read_text())
    assert "concept_doi" not in state["stages"]["record-doi"]["outputs"]


def test_record_doi_first_release_fetch_failure_keeps_the_stage(release_fixture, capsys) -> None:
    seed_state(release_fixture, {"deposit-draft": {
        "status": "waiting", "outputs": {"first_release": True},
    }})
    assert invoke(release_fixture, "record-doi", "--doi", DOI,
                  fake=FakeZenodo(pending=False, record_failure=503)) == 0
    output = capsys.readouterr().out
    assert "manifest --concept-doi <concept DOI>" in output
    state = json.loads(release_fixture.state.read_text())
    assert state["stages"]["record-doi"]["status"] == "done"
    assert "concept_doi" not in state["stages"]["record-doi"]["outputs"]


def test_tag_prints_but_never_runs_git_tag_or_push(release_fixture, capsys) -> None:
    seed_state(release_fixture, {"record-doi": {"status": "done"}})
    (release_fixture.repo / "tag-fixture.txt").write_text("tag target\n")
    head = commit_all(release_fixture.repo)
    calls = []

    def runner(command, cwd):
        calls.append(command)
        return release_domain.CommandResult(0, f"{head} refs/tags/fixture-v1.0.0\n", "")

    code = release_domain.main(
        release_fixture.argv("tag", "--commit", head, "--verify"), now=lambda: NOW, runner=runner,
    )
    assert code == 0
    output = capsys.readouterr().out
    assert f"OWNER: git tag fixture-v1.0.0 {head}" in output
    assert "OWNER: git push origin fixture-v1.0.0" in output
    assert calls == [
        ["git", "ls-remote", "--tags", "origin", "refs/tags/fixture-v1.0.0"],
        ["git", "rev-parse", "HEAD"],
    ]


def test_status_prints_stage_records_and_next_action(release_fixture, capsys) -> None:
    assert invoke(release_fixture, "gate") == 0
    assert invoke(release_fixture, "status") == 0
    output = capsys.readouterr().out
    assert "asb-release-state/1" in output
    assert "gate" in output
    assert "next: land" in output


def test_fake_end_to_end_covers_all_stages_and_writes_trace(release_fixture) -> None:
    fake = FakeZenodo(pending=True)
    assert invoke(release_fixture, "gate") == 0
    assert invoke(release_fixture, "deposit-plan", "--record-id", "55") == 0
    assert invoke(release_fixture, "deposit-draft", "--record-id", "55", fake=fake) == 2
    assert invoke(release_fixture, "record-doi", "--doi", DOI) == 0
    stale = release_fixture.repo / "collections/fixture/v1/gate_report.json"
    assert invoke(release_fixture, "receipt") == 1
    stale.unlink()
    assert invoke(release_fixture, "receipt") == 0
    assert (release_fixture.repo / "receipts/fixture/gate_report.json").is_file()
    head = commit_all(release_fixture.repo, "record DOI and receipt")
    assert invoke(release_fixture, "manifest", "--concept-doi", CONCEPT_DOI, "--commit", head) == 0
    assert invoke(release_fixture, "tag", "--commit", head) == 2
    assert invoke(release_fixture, "status") == 0
    state = json.loads(release_fixture.state.read_text())
    assert state["schema"] == "asb-release-state/1"
    assert all(record["repo_commit"] for record in state["stages"].values())
    assert (release_fixture.repo / "receipts/fixture/release_log.md").is_file()


def test_real_metabolomics_plan_offline_when_checkout_exists(tmp_path) -> None:
    checkout = Path("/Users/nothiasl/git/asb-skills-metabolomics")
    if not checkout.is_dir():
        pytest.skip("released domain checkout is absent")
    code = release_domain.main([
        "deposit-plan", "--domain", "metabolomics", "--version", "v3",
        "--repo-root", str(checkout), "--tooling-root", str(REPO),
        "--state", str(tmp_path / "state.json"), "--record-id", "20794027",
        "--publication-date", "2026-11-09", "--receipts", str(tmp_path / "receipts"),
    ], now=lambda: NOW)
    assert code == 0


def test_record_doi_invokes_the_hub_emitter_when_available(release_fixture, tmp_path) -> None:
    source = Path(os.environ.get("ASB_HUB_ROOT", "/Users/nothiasl/git/agenticsciencebuilder_dev"))
    emitter = source / "docs/asbb/release-manifest"
    if not emitter.is_dir():
        pytest.skip("hub release emitter is absent; set ASB_HUB_ROOT")
    hub = tmp_path / "hub"
    shutil.copytree(emitter, hub / "docs/asbb/release-manifest")
    source_record = release_fixture.repo / "receipts/fixture/source.json"
    record = json.loads(source_record.read_text())
    record["tooling_commit"] = "a" * 40
    source_record.write_text(json.dumps(record))
    seed_state(release_fixture, {"deposit-draft": {"status": "waiting"}})
    assert invoke(
        release_fixture, "record-doi", "--doi", DOI, "--hub-root", str(hub),
        "--receipts", str(release_fixture.repo / "receipts/fixture"),
    ) == 0
    manifest = yaml.safe_load((hub / "releases/fixture/RELEASE.yaml").read_text())
    assert manifest["domain"] == "fixture"
    assert manifest["version"] == "v1"
    assert manifest["record_state"] == "draft"


def test_land_dry_runs_then_executes_and_records_branch(release_fixture, tmp_path) -> None:
    candidate = tmp_path / "candidate"
    receipts = tmp_path / "receipts"
    source_collection = release_fixture.repo / "collections/fixture/v1"
    shutil.copytree(source_collection, candidate)
    descriptor = yaml.safe_load((candidate / "collection.yaml").read_text())
    descriptor.update(cut_id="0123456789ab", title="ASB Fixture Skill Collection v1")
    (candidate / "collection.yaml").write_text(yaml.safe_dump(descriptor, sort_keys=False))
    digest = hashlib.sha256()
    for path in sorted(candidate.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(candidate).as_posix().encode())
            digest.update(b"\0")
            digest.update(hashlib.sha256(path.read_bytes()).digest())
    shutil.copytree(release_fixture.repo / "receipts/fixture", receipts)
    (receipts / "gate_report.json").write_text('{"release_verified": true}\n')
    (receipts / "source.json").write_text(json.dumps({
        "status": "complete", "domain": "fixture", "version": "v1", "cut_id": "0123456789ab",
        "asb_commit": "a" * 40, "tooling_commit": "b" * 40, "corpus_commit": "c" * 40,
        "output_tree_sha256": digest.hexdigest(), "receipts": ["gate_report.json", "source.json"],
    }))
    domain = tmp_path / "landing-domain"
    domain.mkdir()
    (domain / ".zenodo.json").write_text("{}\n")
    run_git(domain, "init", "-b", "main")
    run_git(domain, "config", "user.name", "Fixture")
    run_git(domain, "config", "user.email", "fixture@example.invalid")
    commit_all(domain)
    state_path = tmp_path / "land-state.json"
    base = [
        "--domain", "fixture", "--version", "v1", "--repo-root", str(domain),
        "--tooling-root", str(release_fixture.tooling), "--state", str(state_path),
        "--candidate", str(candidate), "--receipts", str(receipts),
        "--title", "ASB Fixture Skill Collection v1",
    ]
    seed = {"schema": "asb-release-state/1", "domain": "fixture", "version": "v1",
            "stages": {"gate": {"status": "done"}}}
    state_path.write_text(json.dumps(seed))
    assert release_domain.main(["land", *base], now=lambda: NOW) == 2
    assert release_domain.main(["land", *base, "--execute"], now=lambda: NOW) == 2
    state = json.loads(state_path.read_text())
    assert state["stages"]["land"]["outputs"]["branch"] == "candidate/0123456789ab"
    assert state["stages"]["land"]["outputs"]["commit"]
    assert (domain / "receipts/0123456789ab/release_log.md").is_file()


PATCH_DOI = "10.5281/zenodo.1234999"
SURFACES = (
    "collections/fixture/v1/CITATION.cff", "CITATION.cff", "README.md",
    "collections/fixture/v1/USAGE.md",
)


def snapshot(repo: Path) -> dict:
    return {relative: (repo / relative).read_bytes() if (repo / relative).exists() else None
            for relative in SURFACES}


def test_record_doi_skips_an_absent_usage_file(release_fixture) -> None:
    (release_fixture.repo / "collections/fixture/v1/USAGE.md").unlink()
    seed_state(release_fixture, {"deposit-draft": {"status": "waiting"}})
    assert invoke(release_fixture, "record-doi", "--doi", DOI, "--released", "2026-11-09") == 0
    state = json.loads(release_fixture.state.read_text())
    outputs = state["stages"]["record-doi"]["outputs"]
    assert outputs["skipped_files"] == [str(release_fixture.repo / "collections/fixture/v1/USAGE.md")]
    assert len(outputs["changed_files"]) == 3
    for relative in SURFACES[:3]:
        assert DOI in (release_fixture.repo / relative).read_text()
    assert not (release_fixture.repo / "collections/fixture/v1/USAGE.md").exists()


def test_record_doi_refuses_a_readme_without_the_row_and_writes_nothing(release_fixture, capsys) -> None:
    readme = release_fixture.repo / "README.md"
    readme.write_text("# Fixture\n\nNo release table yet.\n")
    before = snapshot(release_fixture.repo)
    seed_state(release_fixture, {"deposit-draft": {"status": "waiting"}})
    assert invoke(release_fixture, "record-doi", "--doi", DOI) == 1
    assert snapshot(release_fixture.repo) == before
    error = capsys.readouterr().err
    assert "README has no release-table row for collections/fixture/v1" in error
    assert "| Path | Title | Skills | Tools | Released | DOI |" in error
    state = json.loads(release_fixture.state.read_text())
    assert "doi" not in state


def first_release(namespace: argparse.Namespace) -> str:
    """Record DOI, receipt, commit and register the fixture's v1.0.0 release."""
    seed_state(namespace, {"deposit-draft": {"status": "waiting"}})
    assert invoke(namespace, "record-doi", "--doi", DOI, "--released", "2026-11-01") == 0
    assert invoke(namespace, "receipt") == 0
    commit = commit_all(namespace.repo, "first release DOI")
    assert invoke(namespace, "manifest", "--concept-doi", CONCEPT_DOI, "--commit", commit) == 0
    return commit


def test_patch_release_keeps_earlier_dois_and_traces_the_superseded_row(release_fixture, capsys) -> None:
    collection = release_fixture.repo / "collections/fixture/v1"
    (collection / "USAGE.md").write_text(
        "# Usage\n\n## Citation\n\nCite both:\n\n"
        "1. **The collection**, using v1's `CITATION.cff` and the version DOI of its\n"
        "   Zenodo record, `PENDING`.\n"
        "2. **Every source paper**, through its DOI.\n"
    )
    commit_all(release_fixture.repo, "usage placeholder")
    first = first_release(release_fixture)
    registry = release_fixture.tooling / "collections.yaml"
    first_row = yaml.safe_load(registry.read_text())["domains"]["fixture"]["releases"][0]
    assert first_row["tag"] == "fixture-v1.0.0"
    usage = (collection / "USAGE.md").read_text()
    (collection / "USAGE.md").write_text(usage.replace(
        f"`{DOI}`.\n", f"`{DOI}`; the lineage's concept DOI (all\n   versions) is `{CONCEPT_DOI}`.\n"))
    metadata = json.loads((collection / ".zenodo.json").read_text())
    metadata["version"] = "v1.0.1"
    (collection / ".zenodo.json").write_text(json.dumps(metadata))
    commit_all(release_fixture.repo, "patch release metadata")

    arguments = ("--doi", PATCH_DOI, "--released", "2026-11-09")
    assert invoke(release_fixture, "record-doi", *arguments) == 0
    cff = yaml.safe_load((collection / "CITATION.cff").read_text())
    assert cff["doi"] == PATCH_DOI
    assert [(item["value"], item["description"]) for item in cff["identifiers"]] == [
        (PATCH_DOI, "Zenodo version DOI of v1.0.1 (2026-11-09)"),
        (DOI, "Zenodo version DOI of v1 (2026-11-01)"),
    ]
    root = yaml.safe_load((release_fixture.repo / "CITATION.cff").read_text())
    assert [(item["value"], item["description"]) for item in root["identifiers"]] == [
        (DOI, "Zenodo version DOI of v1 (2026-11-01)"),
        (PATCH_DOI, "Zenodo version DOI of v1.0.1 (2026-11-09)"),
    ]
    usage = (collection / "USAGE.md").read_text()
    assert f"Zenodo record, `{PATCH_DOI}`; the lineage's concept DOI (all\n   versions) is `{CONCEPT_DOI}`." in usage
    assert f"`{DOI}`" not in usage
    readme = (release_fixture.repo / "README.md").read_text()
    assert f"| 2026-11-09 | [{PATCH_DOI}](https://doi.org/{PATCH_DOI}) |" in readme
    surfaces = snapshot(release_fixture.repo)
    assert invoke(release_fixture, "record-doi", *arguments, "--force") == 0
    assert snapshot(release_fixture.repo) == surfaces

    assert invoke(release_fixture, "receipt") == 0
    patch = commit_all(release_fixture.repo, "patch release DOI")
    assert invoke(release_fixture, "manifest", "--commit", patch, "--regen") == 0
    row = yaml.safe_load(registry.read_text())["domains"]["fixture"]["releases"][0]
    assert (row["tag"], row["commit"], row["version_doi"]) == ("fixture-v1.0.1", patch, PATCH_DOI)
    assert row["superseded"] == [{
        "tag": "fixture-v1.0.0", "commit": first, "tree_digest": first_row["tree_digest"],
        "version_doi": DOI, "released": first_row["released"],
    }]
    registered = registry.read_bytes()
    assert invoke(release_fixture, "manifest", "--commit", patch, "--regen", "--force") == 0
    assert registry.read_bytes() == registered
    capsys.readouterr()
    assert invoke(release_fixture, "tag", "--commit", patch) == 2
    assert f"OWNER: git tag fixture-v1.0.1 {patch}" in capsys.readouterr().out


def test_release_label_must_share_the_major_version(release_fixture, capsys) -> None:
    collection = release_fixture.repo / "collections/fixture/v1"
    metadata = json.loads((collection / ".zenodo.json").read_text())
    metadata["version"] = "v2.0.1"
    (collection / ".zenodo.json").write_text(json.dumps(metadata))
    before = snapshot(release_fixture.repo)
    seed_state(release_fixture, {"deposit-draft": {"status": "waiting"}})
    assert invoke(release_fixture, "record-doi", "--doi", DOI) == 1
    assert snapshot(release_fixture.repo) == before
    assert "is not v<major>.<minor>.<patch> with major v1" in capsys.readouterr().err


def test_manifest_digest_is_read_from_git_objects_and_refuses_untracked_files(release_fixture, capsys) -> None:
    from scripts.check_collections_manifest import compute_tree_digest, git_tree_digest

    seed_state(release_fixture, {"deposit-draft": {"status": "waiting"}})
    assert invoke(release_fixture, "record-doi", "--doi", DOI) == 0
    assert invoke(release_fixture, "receipt") == 0
    commit = commit_all(release_fixture.repo, "first release DOI")
    registry = release_fixture.tooling / "collections.yaml"
    before = registry.read_bytes()
    stray = release_fixture.repo / "collections/fixture/v1/gate_report.json"
    stray.write_text('{"stale": true}\n')
    assert invoke(release_fixture, "manifest", "--concept-doi", CONCEPT_DOI, "--commit", commit) == 1
    assert "collections/fixture/v1/gate_report.json" in capsys.readouterr().err
    assert registry.read_bytes() == before
    stray.unlink()
    (release_fixture.repo / "collections/fixture/v1/corpus.yaml").write_text("papers: []\n")
    assert invoke(release_fixture, "manifest", "--concept-doi", CONCEPT_DOI, "--commit", commit) == 1
    assert "collections/fixture/v1/corpus.yaml" in capsys.readouterr().err
    run_git(release_fixture.repo, "checkout", "--", "collections/fixture/v1/corpus.yaml")
    assert invoke(release_fixture, "manifest", "--concept-doi", CONCEPT_DOI, "--commit", commit) == 0
    row = yaml.safe_load(registry.read_text())["domains"]["fixture"]["releases"][0]
    expected = git_tree_digest(release_fixture.repo, commit, "collections/fixture/v1")
    assert row["tree_digest"] == expected
    assert compute_tree_digest(release_fixture.repo, "collections/fixture/v1") == expected
    assert "superseded" not in row


def test_receipt_writes_under_the_cut_receipts_or_beside_the_collection(release_fixture) -> None:
    seed_state(release_fixture, {"deposit-draft": {"status": "waiting"}})
    assert invoke(release_fixture, "record-doi", "--doi", DOI) == 0
    assert invoke(release_fixture, "receipt") == 0
    report = release_fixture.repo / "receipts/fixture/gate_report.json"
    state = json.loads(release_fixture.state.read_text())
    assert state["stages"]["receipt"]["outputs"]["report"] == str(report)
    assert state["stages"]["receipt"]["digests"]["receipt"] == hashlib.sha256(report.read_bytes()).hexdigest()
    assert not (release_fixture.repo / "collections/fixture/v1/gate_report.json").exists()

    shutil.rmtree(release_fixture.repo / "receipts")
    state.pop("cut_id", None)
    release_fixture.state.write_text(json.dumps(state))
    assert invoke(release_fixture, "receipt", "--force") == 0
    fallback = release_fixture.repo / "collections/fixture/v1/gate_report.json"
    assert fallback.is_file()
    assert invoke(release_fixture, "receipt", "--force") == 0


def test_record_doi_selects_the_row_whose_path_cell_is_the_collection(release_fixture) -> None:
    readme = release_fixture.repo / "README.md"
    status = "| Plugin manifests | validated for `collections/fixture/v1` |\n"
    readme.write_text(readme.read_text().replace("## Collections", "| Item | State |\n|---|---|\n"
                                                 + status + "\n## Collections"))
    seed_state(release_fixture, {"deposit-draft": {"status": "waiting"}})
    assert invoke(release_fixture, "record-doi", "--doi", DOI, "--released", "2026-11-09") == 0
    text = readme.read_text()
    assert status in text
    assert (f"| `collections/fixture/v1` | ASB Fixture Skill Collection v1 | 10 | 10 | 2026-11-09 "
            f"| [{DOI}](https://doi.org/{DOI}) |") in text


def test_manifest_keeps_the_registry_layout(release_fixture) -> None:
    registry = release_fixture.tooling / "collections.yaml"
    other = (
        "  other:\n"
        "    repository: Example/other\n"
        "    concept_doi: 10.5281/zenodo.1111110\n"
        "    releases:\n"
        "      - version: 1\n"
        "        path: collections/other/v1\n"
        "        tag: other-v1.0.0\n"
        "        commit: " + "a" * 40 + "\n"
        "        source_commit: null\n"
        "        tree_digest: sha256:" + "0" * 64 + "\n"
        "        version_doi: 10.5281/zenodo.1111111\n"
        "        released: 2026-01-02\n"
        "        skills: 1\n        tools: 1\n        workflows: 0\n        papers: 1\n"
    )
    header = "schema: asb-collections-manifest/1\n# tree_digest: defined over the committed tree.\ndomains:\n"
    registry.write_text(header + other)
    seed_state(release_fixture, {
        "record-doi": {"status": "done", "inputs": {"doi": DOI}}, "receipt": {"status": "done"},
    }, doi=DOI, released="2026-11-09")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=release_fixture.repo, text=True).strip()
    release_domain.update_manifest(release_domain.ReleaseContext(
        argparse.Namespace(tooling_root=release_fixture.tooling, domain="fixture", concept_doi=CONCEPT_DOI),
        None, None, lambda: NOW, json.loads(release_fixture.state.read_text()), [],
    ), {"version": 1, "path": "collections/fixture/v1", "tag": "fixture-v1.0.0", "commit": commit,
        "source_commit": None, "tree_digest": "sha256:" + "1" * 64, "version_doi": DOI,
        "released": "2026-11-09", "skills": 10, "tools": 10, "workflows": 5, "papers": 1})
    text = registry.read_text()
    assert text.startswith(header + other)
    assert "  fixture:\n    repository: HolobiomicsLab/asb-skills-fixture\n    concept_doi: " in text
    assert "        released: 2026-11-09\n" in text
