"""Zenodo deposit tooling: deterministic archive, offline plan, draft-only upload.

Nothing here reaches the network. The tool sends every request through one
function, `zenodo_deposit._request`; the tests replace it with a recorder, and
one test runs the real function against a local HTTP server.
"""

import hashlib
import http.server
import json
import os
import threading
import zipfile
from pathlib import Path

import pytest

from scripts import zenodo_deposit

TOKEN = "tok-prod-0123456789"
SANDBOX_TOKEN = "tok-sandbox-9876543210"
RECORD = "555"
DRAFT_ID = 777
DATE = "2026-11-01"

ZENODO_JSON = {
    "title": "Synthetic collection v1",
    "upload_type": "dataset",
    "description": "A synthetic collection.",
    "access_right": "open",
    "license": "cc-by-4.0",
    "version": "dom-v0.1.0",
    "creators": [{"name": "Doe, Jane", "orcid": "0000-0000-0000-0000"}],
    "keywords": ["synthetic"],
    "related_identifiers": [
        {"relation": "isVersionOf", "identifier": f"10.5281/zenodo.{RECORD}", "scheme": "doi"},
        {"relation": "isSupplementTo", "identifier": "https://example.org/repo", "scheme": "url"},
    ],
    "notes": "Synthetic.",
}


def make_repo(root: Path, zenodo_json=None) -> Path:
    """A repository root holding collections/dom/v1 and the files the archive bundles."""
    coll = root / "collections" / "dom" / "v1"
    (coll / "skills" / "b").mkdir(parents=True)
    (coll / "skills" / "a").mkdir(parents=True)
    (coll / "skills" / "b" / "SKILL.md").write_text("b\n")
    (coll / "skills" / "a" / "SKILL.md").write_text("a\n")
    (coll / "collection.yaml").write_text("name: dom\n")
    (coll / "bin").mkdir()
    (coll / "bin" / "tool.py").write_text("print(1)\n")
    (coll / "bin" / "__pycache__").mkdir()
    (coll / "bin" / "__pycache__" / "tool.cpython-312.pyc").write_bytes(b"\x00")
    (coll / ".cache").mkdir()
    (coll / ".cache" / "emb.npz").write_bytes(b"cache")
    (coll / ".DS_Store").write_bytes(b"junk")
    (coll / ".zenodo.json").write_text(json.dumps(zenodo_json or ZENODO_JSON))
    (root / "scripts").mkdir()
    (root / "scripts" / "perspicacite_kb_bind.py").write_text("bind\n")
    (root / "scripts" / "requirements.txt").write_text("reqs\n")
    (root / "AGENTS.md").write_text("agents\n")
    return root


@pytest.fixture
def repo(tmp_path):
    return make_repo(tmp_path / "repo")


@pytest.fixture(autouse=True)
def tokens(monkeypatch):
    monkeypatch.setenv("ZENODO_TOKEN", TOKEN)
    monkeypatch.setenv("ZENODO_SANDBOX_TOKEN", SANDBOX_TOKEN)


class FakeZenodo:
    """Records each request and answers like the deposit API, with overrides per call."""

    def __init__(self, base, fail=None):
        self.base = base
        self.calls = []
        self.fail = fail or {}

    def __call__(self, method, url, token, body=None):
        self.calls.append((method, url, token, body))
        key = (method, url.removeprefix(self.base))
        if key in self.fail:
            return self.fail[key], {"message": "refused"}
        dep = f"{self.base}/api/deposit/depositions"
        if method == "POST" and url == f"{dep}/{RECORD}/actions/newversion":
            return 201, {"id": int(RECORD), "links": {"latest_draft": f"{dep}/{DRAFT_ID}"}}
        if method == "GET" and url == f"{dep}/{DRAFT_ID}":
            return 200, {
                "id": DRAFT_ID,
                "files": [{"id": "old-1"}, {"id": "old-2"}],
                "links": {"bucket": f"{self.base}/api/files/bkt",
                          "html": f"{self.base}/deposit/{DRAFT_ID}"},
            }
        if method == "DELETE" and "/files/" in url:
            return 204, None
        if method == "PUT" and url.startswith(f"{self.base}/api/files/bkt/"):
            return 201, {"key": url.rsplit("/", 1)[1]}
        if method == "PUT" and url == f"{dep}/{DRAFT_ID}":
            return 200, {"id": DRAFT_ID}
        raise AssertionError(f"unexpected request {method} {url}")

    def steps(self):
        return [(m, u.removeprefix(self.base)) for m, u, _, _ in self.calls]


def run_draft(repo, monkeypatch, capsys, *extra, fake=None, sandbox=False):
    base = zenodo_deposit.SANDBOX_URL if sandbox else zenodo_deposit.ZENODO_URL
    fake = fake or FakeZenodo(base)
    monkeypatch.setattr(zenodo_deposit, "_request", fake)
    argv = ["draft", "dom", "v1", "--repo-root", str(repo), "--out-dir", str(repo / "out"),
            "--publication-date", DATE, *extra]
    if sandbox:
        argv.append("--sandbox")
    code = zenodo_deposit.main(argv)
    out = capsys.readouterr()
    return code, out, fake


def entries(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        return zf.namelist()


def test_archive_is_deterministic_across_builds_and_mtimes(repo, tmp_path):
    first = zenodo_deposit.build_archive(repo, "dom", "v1", tmp_path / "o1")
    for path in repo.rglob("*"):
        os.utime(path, (1_900_000_000, 1_900_000_000))
    second = zenodo_deposit.build_archive(repo, "dom", "v1", tmp_path / "o2")
    assert first.sha256 == second.sha256
    assert first.size == second.size == first.path.stat().st_size
    assert first.sha256 == hashlib.sha256(first.path.read_bytes()).hexdigest()
    assert first.path.name == "dom-v1.zip"


def test_archive_changes_when_content_changes(repo, tmp_path):
    before = zenodo_deposit.build_archive(repo, "dom", "v1", tmp_path / "o1")
    (repo / "collections/dom/v1/skills/a/SKILL.md").write_text("changed\n")
    after = zenodo_deposit.build_archive(repo, "dom", "v1", tmp_path / "o2")
    assert before.sha256 != after.sha256


def test_archive_entries_are_sorted_filtered_and_stamped(repo, tmp_path):
    built = zenodo_deposit.build_archive(repo, "dom", "v1", tmp_path / "o")
    names = entries(built.path)
    assert names == sorted(names)
    assert "dom/v1/.zenodo.json" in names
    assert "dom/v1/skills/a/SKILL.md" in names
    assert not any("__pycache__" in n or ".cache" in n or ".DS_Store" in n for n in names)
    assert {"dom/v1/AGENTS.md", "dom/v1/scripts/perspicacite_kb_bind.py",
            "dom/v1/scripts/requirements.txt"} <= set(names)
    with zipfile.ZipFile(built.path) as zf:
        assert {i.date_time for i in zf.infolist()} == {zenodo_deposit.ZIP_EPOCH}


def test_archive_rejects_a_missing_collection(repo, tmp_path):
    with pytest.raises(zenodo_deposit.ZenodoError, match="collection directory"):
        zenodo_deposit.build_archive(repo, "dom", "v9", tmp_path / "o")


def test_archive_command_prints_sha256_and_size(repo, capsys):
    code = zenodo_deposit.main(["archive", "dom", "v1", "--repo-root", str(repo),
                                "--out-dir", str(repo / "out")])
    out = capsys.readouterr().out
    built = repo / "out" / "dom-v1.zip"
    assert code == 0
    assert hashlib.sha256(built.read_bytes()).hexdigest() in out
    assert str(built.stat().st_size) in out


def test_metadata_payload_wraps_dates_and_drops_the_lineage_relation(repo):
    payload, dropped = zenodo_deposit.metadata_payload(
        repo / "collections/dom/v1/.zenodo.json", DATE)
    meta = payload["metadata"]
    assert meta["publication_date"] == DATE
    assert [r["relation"] for r in meta["related_identifiers"]] == ["isSupplementTo"]
    assert dropped == ["isVersionOf"]
    assert meta["title"] == ZENODO_JSON["title"]


def test_an_explicit_publication_date_in_the_file_wins(repo):
    path = repo / "collections/dom/v1/.zenodo.json"
    path.write_text(json.dumps({**ZENODO_JSON, "publication_date": "2026-01-02"}))
    payload, _ = zenodo_deposit.metadata_payload(path, DATE)
    assert payload["metadata"]["publication_date"] == "2026-01-02"


def test_validate_metadata_names_each_rejected_key_and_relation():
    meta = {**ZENODO_JSON, "upload_type": "spreadsheet", "bogus": 1,
            "related_identifiers": [{"relation": "isVersionOf", "identifier": "x"},
                                    {"relation": "cites", "identifier": "10.1/x"}]}
    problems = zenodo_deposit.validate_metadata(meta)
    assert any("bogus" in p for p in problems)
    assert any("upload_type" in p and "spreadsheet" in p for p in problems)
    assert any("isVersionOf" in p for p in problems)
    assert not any("cites" in p for p in problems)


def test_validate_metadata_requires_the_mandatory_fields_and_a_license_when_open():
    problems = zenodo_deposit.validate_metadata({"access_right": "open"})
    for key in ("upload_type", "title", "creators", "description", "license"):
        assert any(key in p for p in problems)


def test_validate_metadata_accepts_the_template_once_lineage_is_dropped(repo):
    payload, _ = zenodo_deposit.metadata_payload(
        repo / "collections/dom/v1/.zenodo.json", DATE)
    assert zenodo_deposit.validate_metadata(payload["metadata"]) == []


def test_plan_prints_metadata_and_files_without_any_request(repo, monkeypatch, capsys):
    def forbidden(*args, **kwargs):
        raise AssertionError("plan must not use the network")

    monkeypatch.setattr(zenodo_deposit, "_request", forbidden)
    code = zenodo_deposit.main(["plan", "dom", "v1", "--repo-root", str(repo),
                                "--publication-date", DATE])
    out = capsys.readouterr().out
    assert code == 0
    assert "https://zenodo.org" in out
    assert f"new version of record {RECORD}" in out
    assert "Synthetic collection v1" in out and DATE in out
    assert "dom-v1.zip" in out and "sha256" in out
    assert "isVersionOf" in out and "not sent" in out
    assert TOKEN not in out


def test_plan_names_the_sandbox_host(repo, capsys):
    zenodo_deposit.main(["plan", "dom", "v1", "--repo-root", str(repo), "--sandbox",
                         "--publication-date", DATE])
    assert "https://sandbox.zenodo.org" in capsys.readouterr().out


def test_plan_reports_problems_and_fails(repo, capsys):
    bad = {**ZENODO_JSON, "bogus": 1}
    (repo / "collections/dom/v1/.zenodo.json").write_text(json.dumps(bad))
    code = zenodo_deposit.main(["plan", "dom", "v1", "--repo-root", str(repo),
                                "--publication-date", DATE])
    assert code == 1
    assert "bogus" in capsys.readouterr().out


def test_draft_call_sequence_and_payloads(repo, monkeypatch, capsys):
    code, out, fake = run_draft(repo, monkeypatch, capsys)
    base = zenodo_deposit.ZENODO_URL
    dep = "/api/deposit/depositions"
    assert code == 0
    assert fake.steps() == [
        ("POST", f"{dep}/{RECORD}/actions/newversion"),
        ("GET", f"{dep}/{DRAFT_ID}"),
        ("DELETE", f"{dep}/{DRAFT_ID}/files/old-1"),
        ("DELETE", f"{dep}/{DRAFT_ID}/files/old-2"),
        ("PUT", "/api/files/bkt/dom-v1.zip"),
        ("PUT", f"{dep}/{DRAFT_ID}"),
    ]
    upload = fake.calls[4][3]
    assert isinstance(upload, Path)
    assert hashlib.sha256(upload.read_bytes()).hexdigest() in out.out
    meta_body = fake.calls[5][3]
    assert set(meta_body) == {"metadata"}
    assert meta_body["metadata"]["publication_date"] == DATE
    assert f"{base}/deposit/{DRAFT_ID}" in out.out
    assert "not published" in out.out


def test_draft_never_calls_a_publish_action(repo, monkeypatch, capsys):
    _, _, fake = run_draft(repo, monkeypatch, capsys)
    assert not any("publish" in url for _, url, _, _ in fake.calls)
    source = Path(zenodo_deposit.__file__).read_text()
    assert "actions/publish" not in source
    assert "--publish" not in source


def test_token_is_sent_as_credential_and_never_printed(repo, monkeypatch, capsys):
    code, out, fake = run_draft(repo, monkeypatch, capsys)
    assert code == 0
    assert {token for _, _, token, _ in fake.calls} == {TOKEN}
    assert TOKEN not in out.out + out.err
    assert TOKEN not in json.dumps([c[3] for c in fake.calls if isinstance(c[3], dict)])


def test_sandbox_switches_host_and_token(repo, monkeypatch, capsys):
    code, out, fake = run_draft(repo, monkeypatch, capsys, sandbox=True)
    assert code == 0
    assert all(url.startswith("https://sandbox.zenodo.org/") for _, url, _, _ in fake.calls)
    assert {token for _, _, token, _ in fake.calls} == {SANDBOX_TOKEN}
    assert SANDBOX_TOKEN not in out.out + out.err
    assert "https://sandbox.zenodo.org/deposit/" in out.out


@pytest.mark.parametrize("sandbox,variable", [(False, "ZENODO_TOKEN"),
                                              (True, "ZENODO_SANDBOX_TOKEN")])
def test_missing_token_fails_before_any_request(repo, monkeypatch, capsys, sandbox, variable):
    monkeypatch.delenv(variable)
    code, out, fake = run_draft(repo, monkeypatch, capsys, sandbox=sandbox)
    assert code == 1
    assert variable in out.err
    assert fake.calls == []


def test_empty_token_counts_as_missing(repo, monkeypatch, capsys):
    monkeypatch.setenv("ZENODO_TOKEN", "  ")
    code, out, fake = run_draft(repo, monkeypatch, capsys)
    assert code == 1 and fake.calls == []


def test_non_2xx_on_newversion_stops_the_run(repo, monkeypatch, capsys):
    base = zenodo_deposit.ZENODO_URL
    fake = FakeZenodo(base, fail={("POST", f"/api/deposit/depositions/{RECORD}/actions/newversion"): 403})
    code, out, fake = run_draft(repo, monkeypatch, capsys, fake=fake)
    assert code == 1
    assert "403" in out.err and "newversion" in out.err
    assert len(fake.calls) == 1


def test_failed_file_delete_stops_before_upload(repo, monkeypatch, capsys):
    base = zenodo_deposit.ZENODO_URL
    fake = FakeZenodo(base, fail={("DELETE", f"/api/deposit/depositions/{DRAFT_ID}/files/old-2"): 500})
    code, out, fake = run_draft(repo, monkeypatch, capsys, fake=fake)
    assert code == 1
    assert not any(m == "PUT" for m, _ in fake.steps())


def test_failed_upload_leaves_the_metadata_unsent(repo, monkeypatch, capsys):
    base = zenodo_deposit.ZENODO_URL
    fake = FakeZenodo(base, fail={("PUT", "/api/files/bkt/dom-v1.zip"): 413})
    code, out, fake = run_draft(repo, monkeypatch, capsys, fake=fake)
    assert code == 1
    assert fake.steps()[-1] == ("PUT", "/api/files/bkt/dom-v1.zip")


def test_draft_refuses_metadata_the_api_would_reject(repo, monkeypatch, capsys):
    bad = {**ZENODO_JSON, "bogus": 1}
    (repo / "collections/dom/v1/.zenodo.json").write_text(json.dumps(bad))
    code, out, fake = run_draft(repo, monkeypatch, capsys)
    assert code == 1 and fake.calls == []
    assert "bogus" in out.err


def test_record_id_option_overrides_the_file(repo, monkeypatch, capsys):
    base = zenodo_deposit.ZENODO_URL
    refused = FakeZenodo(base, fail={("POST", "/api/deposit/depositions/999/actions/newversion"): 404})
    code, out, fake = run_draft(repo, monkeypatch, capsys, "--record-id", "999", fake=refused)
    assert code == 1
    assert fake.steps()[0] == ("POST", "/api/deposit/depositions/999/actions/newversion")


def test_draft_without_a_record_id_fails_before_any_request(repo, monkeypatch, capsys):
    no_lineage = {**ZENODO_JSON, "related_identifiers": []}
    (repo / "collections/dom/v1/.zenodo.json").write_text(json.dumps(no_lineage))
    code, out, fake = run_draft(repo, monkeypatch, capsys)
    assert code == 1 and fake.calls == []
    assert "--record-id" in out.err


def test_missing_zenodo_json_is_an_error(repo, monkeypatch, capsys):
    (repo / "collections/dom/v1/.zenodo.json").unlink()
    code, out, fake = run_draft(repo, monkeypatch, capsys)
    assert code == 1 and ".zenodo.json" in out.err


class Recorder(http.server.BaseHTTPRequestHandler):
    seen = []

    def _reply(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length)
        Recorder.seen.append((self.command, self.path, dict(self.headers), body))
        status = 403 if self.path == "/denied" else 200
        payload = json.dumps({"message": "denied"} if status == 403 else {"ok": True}).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    do_GET = do_POST = do_PUT = do_DELETE = _reply

    def log_message(self, *args):
        pass


@pytest.fixture
def server():
    Recorder.seen = []
    httpd = http.server.HTTPServer(("127.0.0.1", 0), Recorder)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()
    httpd.server_close()


def test_real_request_sends_bearer_json_and_file_bodies(server, tmp_path):
    status, body = zenodo_deposit._request("PUT", f"{server}/x", TOKEN, {"metadata": {"a": 1}})
    assert (status, body) == (200, {"ok": True})
    method, path, headers, sent = Recorder.seen[-1]
    assert headers["Authorization"] == f"Bearer {TOKEN}"
    assert headers["Content-Type"] == "application/json"
    assert json.loads(sent) == {"metadata": {"a": 1}}

    blob = tmp_path / "f.zip"
    blob.write_bytes(b"PK-bytes" * 1000)
    zenodo_deposit._request("PUT", f"{server}/bucket/f.zip", TOKEN, blob)
    _, _, headers, sent = Recorder.seen[-1]
    assert headers["Content-Type"] == "application/octet-stream"
    assert sent == blob.read_bytes()

    zenodo_deposit._request("DELETE", f"{server}/gone", TOKEN)
    assert Recorder.seen[-1][0] == "DELETE" and Recorder.seen[-1][3] == b""


def test_real_request_returns_error_statuses_instead_of_raising(server):
    status, body = zenodo_deposit._request("GET", f"{server}/denied", TOKEN)
    assert status == 403 and body == {"message": "denied"}
