"""The pre-publication scan reads every ref the remote serves, pull refs included.

A repository made public publishes ``refs/pull/<n>/head`` as well as its
branches. The release gap audit of 2026-10-30 found trim receipts quoting the
spans the gate had removed, local paths and an unparsable router on refs that
no scan of the checked-out branch had read. The scan lists the remote's refs,
fetches the commits missing locally without writing a ref, and reports those
three defects without repeating the span text.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import scan_remote_refs as scan


REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "scan_remote_refs.py"
QUOTE = "A sentence long enough to be a quotation from a paper whose licence forbids it."
CLEAN_RECEIPT = {
    "status": "applied",
    "kept": [{"kind": "leaf", "leaf": "a-leaf", "doi": "10.1/x", "characters": 40,
              "sha256": "0" * 64}],
    "dropped": [],
}
LEAKY_RECEIPT = {
    "status": "applied",
    "kept": [],
    "dropped": [{"kind": "leaf", "leaf": "a-leaf", "doi": "10.1/x",
                 "dropped_text": QUOTE}],
}
GOOD_ROUTER = '---\nname: router\ndescription: "Use when: routing a task"\n---\n\nBody.\n'
BAD_ROUTER = "---\nname: router\ndescription: Use when: routing a task\n---\n\nBody.\n"


def _git(cwd: Path, *arguments: str) -> str:
    environment = {
        **os.environ,
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.org",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.org",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
    }
    result = subprocess.run(
        ["git", *arguments], cwd=cwd, env=environment, capture_output=True, text=True, check=True
    )
    return result.stdout


def _write_tree(root: Path, receipt: dict, router: str, gate_line: str) -> None:
    receipts = root / "receipts" / "abc123def456"
    receipts.mkdir(parents=True, exist_ok=True)
    (receipts / "evidence_trim_receipt.json").write_text(json.dumps(receipt), "utf-8")
    (receipts / "gate.txt").write_text(gate_line + "\n", "utf-8")
    router_dir = root / "collections" / "d" / "v1" / "skills" / "_router"
    router_dir.mkdir(parents=True, exist_ok=True)
    (router_dir / "SKILL.md").write_text(router, "utf-8")
    leaf = root / "collections" / "d" / "v1" / "leaves" / "a-leaf"
    leaf.mkdir(parents=True, exist_ok=True)
    (leaf / "SKILL.md").write_text("---\nname: a-leaf\n---\n\nRun `cd /home/user/data`.\n", "utf-8")


def _commit(seed: Path, message: str) -> str:
    _git(seed, "add", "-A")
    _git(seed, "commit", "-q", "-m", message)
    return _git(seed, "rev-parse", "HEAD").strip()


@pytest.fixture
def remote(tmp_path: Path) -> Path:
    """A bare remote with a clean main, a leaky branch and a leaky pull ref."""
    bare = tmp_path / "remote.git"
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(bare))
    seed = tmp_path / "seed"
    _git(tmp_path, "init", "-q", "-b", "main", str(seed))
    _write_tree(seed, CLEAN_RECEIPT, GOOD_ROUTER, "OK collections/d/v1")
    _commit(seed, "clean")
    _git(seed, "push", "-q", str(bare), "main")
    _git(seed, "checkout", "-q", "-b", "candidate/old")
    _write_tree(seed, LEAKY_RECEIPT, BAD_ROUTER, "OK /Users/someone/scratch/d/v1")
    _commit(seed, "leaky branch")
    _git(seed, "push", "-q", str(bare), "candidate/old")
    _git(seed, "checkout", "-q", "main")
    _git(seed, "checkout", "-q", "-b", "pr")
    _write_tree(seed, LEAKY_RECEIPT, GOOD_ROUTER, "OK collections/d/v1")
    pull = _commit(seed, "pull request head")
    _git(seed, "push", "-q", str(bare), f"{pull}:refs/pull/1/head")
    return bare


def _clone(remote: Path, tmp_path: Path) -> Path:
    local = tmp_path / "local"
    # --no-local copies only the objects the branches reach, as a network clone does.
    _git(tmp_path, "clone", "-q", "--no-local", str(remote), str(local))
    return local


def _refs(local: Path) -> str:
    return _git(local, "for-each-ref", "--format=%(refname) %(objectname)")


def _by_ref(report: dict) -> dict[str, dict]:
    (repository,) = report["repositories"]
    return {row["ref"]: row for row in repository["refs"]}


def test_pull_refs_are_fetched_and_scanned_without_writing_a_ref(remote: Path, tmp_path: Path) -> None:
    local = _clone(remote, tmp_path)
    pull_sha = _git(remote, "rev-parse", "refs/pull/1/head").strip()
    assert subprocess.run(
        ["git", "-C", str(local), "cat-file", "-e", f"{pull_sha}^{{commit}}"], capture_output=True
    ).returncode != 0, "the clone must start without the pull request commit"
    before = _refs(local)
    out = tmp_path / "scan.json"

    code = scan.main(["--repo", str(local), "--out", str(out)])

    report = json.loads(out.read_text("utf-8"))
    refs = _by_ref(report)
    assert code == 1
    assert report["exit_code"] == 1
    assert {"refs/heads/main", "refs/heads/candidate/old", "refs/pull/1/head"} <= set(refs)
    assert all(row["scanned"] for row in refs.values())
    assert refs["refs/heads/main"]["findings"] == 0
    pull = refs["refs/pull/1/head"]
    assert pull["findings"] == 1
    assert pull["trim_receipts"][0]["span_text_fields"][0]["characters"] == len(QUOTE)
    assert _refs(local) == before
    assert not (local / ".git" / "FETCH_HEAD").exists()


def test_branch_findings_cover_span_text_paths_and_router(remote: Path, tmp_path: Path) -> None:
    local = _clone(remote, tmp_path)
    out = tmp_path / "scan.json"

    scan.main(["--repo", str(local), "--out", str(out)])

    branch = _by_ref(json.loads(out.read_text("utf-8")))["refs/heads/candidate/old"]
    (receipt,) = branch["trim_receipts"]
    assert receipt["file"] == "receipts/abc123def456/evidence_trim_receipt.json"
    assert [row["pointer"] for row in receipt["span_text_fields"]] == ["/dropped/0/dropped_text"]
    assert receipt["span_text_characters"] == len(QUOTE)
    assert [hit["file"] for hit in branch["absolute_paths"]] == ["receipts/abc123def456/gate.txt"]
    assert [row["file"] for row in branch["router_frontmatter"]] == [
        "collections/d/v1/skills/_router/SKILL.md"
    ]
    assert "does not parse" in branch["router_frontmatter"][0]["error"]


def test_the_report_never_repeats_span_text(remote: Path, tmp_path: Path) -> None:
    local = _clone(remote, tmp_path)
    out = tmp_path / "scan.json"

    scan.main(["--repo", str(local), "--out", str(out)])

    assert QUOTE[:30] not in out.read_text("utf-8")


def test_paths_in_widens_the_path_scan_to_the_whole_tree(remote: Path, tmp_path: Path) -> None:
    local = _clone(remote, tmp_path)
    out = tmp_path / "scan.json"

    scan.main(["--repo", str(local), "--out", str(out), "--paths-in", "."])

    main = _by_ref(json.loads(out.read_text("utf-8")))["refs/heads/main"]
    assert [hit["file"] for hit in main["absolute_paths"]] == [
        "collections/d/v1/leaves/a-leaf/SKILL.md"
    ]


def test_a_long_string_in_a_trim_receipt_is_a_finding() -> None:
    receipt = {"dropped": [{"leaf": "a-leaf", "note": "x" * 201}]}

    described = scan.scan_trim_receipt(json.dumps(receipt), max_string=200)

    assert described["span_text_fields"] == []
    assert [row["pointer"] for row in described["long_strings"]] == ["/dropped/0/note"]
    assert described["longest_string"] == 201


def test_a_clean_remote_exits_zero(tmp_path: Path) -> None:
    bare = tmp_path / "remote.git"
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(bare))
    seed = tmp_path / "seed"
    _git(tmp_path, "init", "-q", "-b", "main", str(seed))
    _write_tree(seed, CLEAN_RECEIPT, GOOD_ROUTER, "OK collections/d/v1")
    _commit(seed, "clean")
    _git(seed, "push", "-q", str(bare), "main")
    local = _clone(bare, tmp_path)
    out = tmp_path / "scan.json"

    assert scan.main(["--repo", str(local), "--out", str(out)]) == 0
    assert json.loads(out.read_text("utf-8"))["summary"]["refs_with_findings"] == 0


def test_an_unscanned_ref_exits_two(remote: Path, tmp_path: Path) -> None:
    local = _clone(remote, tmp_path)
    out = tmp_path / "scan.json"

    code = scan.main(["--repo", str(local), "--out", str(out), "--no-fetch"])

    refs = _by_ref(json.loads(out.read_text("utf-8")))
    assert code == 2
    assert refs["refs/pull/1/head"]["scanned"] is False


def test_an_unreachable_remote_exits_two(tmp_path: Path) -> None:
    local = tmp_path / "local"
    _git(tmp_path, "init", "-q", "-b", "main", str(local))
    _git(local, "remote", "add", "origin", str(tmp_path / "missing.git"))
    out = tmp_path / "scan.json"

    assert scan.main(["--repo", str(local), "--out", str(out)]) == 2
    assert json.loads(out.read_text("utf-8"))["repositories"][0]["error"]


def test_the_script_runs_by_path(remote: Path, tmp_path: Path) -> None:
    local = _clone(remote, tmp_path)
    out = tmp_path / "scan.json"
    environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(local), "--out", str(out)],
        cwd=REPO, env=environment, capture_output=True, text=True,
    )

    assert result.returncode == 1, result.stderr
    assert "with findings (exit 1)" in result.stdout
