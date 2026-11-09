"""The intake adapter applies one receipt through injected git and gh calls."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import intake_github


class FakeRunner:
    """Record every command and answer the small subset the adapter needs."""

    def __init__(self, fail_push: bool = False, existing_prs: int = 0) -> None:
        self.calls: list[tuple[list[str], str]] = []
        self.fail_push = fail_push
        self.comments: list[str] = []
        self.existing_prs = existing_prs
        self.wave = ""

    def __call__(self, argv, cwd):
        command = list(argv)
        self.calls.append((command, cwd))
        if command[:2] == ["gh", "pr"] and command[2] == "list":
            rows = [{"number": 7}] if self.existing_prs else []
            return 0, json.dumps(rows), ""
        if command[:2] == ["gh", "issue"] and command[2] == "view":
            body = "".join(self.comments)
            return 0, json.dumps({"comments": [{"body": body}] if body else []}), ""
        if command[:2] == ["gh", "issue"] and command[2] == "comment":
            self.comments.append(command[command.index("--body") + 1])
            return 0, "", ""
        if "push" in command and self.fail_push:
            return 128, "", "fatal: could not read Username"
        return 0, "", ""


def staged_receipt(repo: Path, *, outcome: str = "staged", comment: str = "Staged for review.",
                   title: str = "A useful paper", issue: int = 42, digest_seed: str = "a") -> dict:
    """Write a wave file and return a receipt shaped like the core's output."""
    wave = repo / "collections" / "metabolomics" / "proposals" / "wave-2026-11-community.yaml"
    wave.parent.mkdir(parents=True, exist_ok=True)
    wave.write_text(f"papers:\n  - doi: 10.1/{digest_seed}\n", encoding="utf-8")
    return {
        "schema": "asb-intake-receipt/1",
        "outcome": outcome,
        "kind": "paper",
        "issue": {"number": issue},
        "domain": "metabolomics",
        "date": "2026-11-09",
        "doi": "10.1/xyz",
        "title": title,
        "repository": "example/repo",
        "access": "open",
        "code_license": "MIT",
        "warnings": [],
        "duplicate_of": "10.1/old" if outcome == "duplicate" else None,
        "row": {"doi": "10.1/xyz"},
        "wave_file": str(wave),
        "inputs_sha256": {"issue": "0" * 64},
        "comment_markdown": comment,
        "labels_add": ["intake-staged"],
        "labels_remove": ["intake-blocked"],
        "receipt_copy": True,
        "seed": digest_seed,
    }


def adapter(runner: FakeRunner, repo: Path, dry_run: bool = False) -> intake_github.Adapter:
    """Build an adapter with a fixed bot identity."""
    config = intake_github.Config(bot_name="asb-intake", bot_email="intake@example.invalid")
    return intake_github.Adapter(runner, repo, "metabolomics", config, dry_run=dry_run)


def commands(runner: FakeRunner) -> list[list[str]]:
    """Return the recorded argv lists."""
    return [command for command, _ in runner.calls]


def add_arguments(runner: FakeRunner) -> list[str]:
    """Return the argument list of the single git add call."""
    adds = [command for command in commands(runner) if command[:2] == ["git", "add"]]
    assert len(adds) == 1
    return adds[0][adds[0].index("--") + 1:]


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """Return an empty checkout root."""
    return tmp_path


def test_staged_writes_the_branch_and_only_the_two_files(repo: Path) -> None:
    """A staged receipt commits the wave row and its receipt copy."""
    runner = FakeRunner()
    receipt = staged_receipt(repo)
    adapter(runner, repo).apply(receipt)
    argv = commands(runner)
    assert argv[0] == ["git", "fetch", "origin", "main"]
    assert argv[1] == ["git", "checkout", "-B", "bot/intake-paper-42", "origin/main"]
    assert add_arguments(runner) == [
        "collections/metabolomics/proposals/wave-2026-11-community.yaml",
        "collections/metabolomics/proposals/receipts/intake-42.json",
    ]
    copy = repo / "collections/metabolomics/proposals/receipts/intake-42.json"
    assert json.loads(copy.read_text(encoding="utf-8"))["issue"] == {"number": 42}
    commits = [command for command in argv if command[0] == "git" and "commit" in command]
    assert len(commits) == 1
    assert "Intake: issue #42 staged for curator review" in commits[0]
    assert any(command[:3] == ["git", "push", "--force"] for command in argv)
    assert any(command[:3] == ["gh", "pr", "create"] for command in argv)
    pushes = [command for command in argv if command[:2] == ["git", "push"]]
    assert len(pushes) == 1 and pushes[0][-1] == "bot/intake-paper-42"


def test_staged_rerun_posts_no_second_comment(repo: Path) -> None:
    """The marker from the first comment suppresses the same receipt digest."""
    runner = FakeRunner()
    receipt = staged_receipt(repo)
    adapter(runner, repo).apply(receipt)
    first_comments = len(runner.comments)
    adapter(runner, repo).apply(receipt)
    assert first_comments == 1
    assert len(runner.comments) == 1
    assert "gh" in commands(runner)[-1][0]


def test_new_digest_updates_the_branch_and_posts_once(repo: Path) -> None:
    """An edited issue yields one new comment and one pull request update."""
    runner = FakeRunner(existing_prs=1)
    first = staged_receipt(repo, comment="Staged for review.", digest_seed="a")
    adapter(runner, repo).apply(first)
    second = staged_receipt(repo, comment="Updated for review.", digest_seed="b")
    adapter(runner, repo).apply(second)
    assert len(runner.comments) == 2
    edits = [command for command in commands(runner) if command[:3] == ["gh", "pr", "edit"]]
    assert len(edits) == 2
    branches = [command[3] for command in commands(runner) if command[:3] == ["git", "checkout", "-B"]]
    assert branches == ["bot/intake-paper-42", "bot/intake-paper-42"]


def test_blocked_posts_and_labels_without_a_branch(repo: Path) -> None:
    """A blocked receipt never touches git."""
    runner = FakeRunner()
    adapter(runner, repo).apply(staged_receipt(repo, outcome="blocked"))
    assert not any(command[0] == "git" for command in commands(runner))
    assert len(runner.comments) == 1
    edits = [command for command in commands(runner) if command[:3] == ["gh", "issue", "edit"]]
    assert len(edits) == 1
    assert "--add-label" in edits[0]
    assert "--remove-label" in edits[0]


def test_duplicate_posts_and_labels_without_a_branch(repo: Path) -> None:
    """A duplicate adds the duplicate label and creates no branch or pull request."""
    runner = FakeRunner()
    receipt = staged_receipt(repo, outcome="duplicate")
    receipt["labels_add"] = []
    adapter(runner, repo).apply(receipt)
    assert not any(command[0] == "git" for command in commands(runner))
    assert not any(command[:2] == ["gh", "pr"] for command in commands(runner))
    assert len(runner.comments) == 1
    edits = [command for command in commands(runner) if command[:3] == ["gh", "issue", "edit"]]
    assert edits[0][edits[0].index("--add-label") + 1] == "duplicate"


def test_dry_run_runs_nothing(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Dry-run prints every command and calls the runner zero times."""
    runner = FakeRunner()
    adapter(runner, repo, dry_run=True).apply(staged_receipt(repo))
    assert runner.calls == []
    printed = capsys.readouterr().out
    assert "bot/intake-paper-42" in printed
    assert not (repo / "collections/metabolomics/proposals/receipts/intake-42.json").exists()


def test_push_failure_leaves_the_local_branch_and_exits_one(
    repo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A refused push keeps the branch and surfaces a refusal."""
    runner = FakeRunner(fail_push=True)
    receipt = staged_receipt(repo)
    monkeypatch.setenv("ASB_INTAKE_BOT_NAME", "asb-intake")
    monkeypatch.setenv("ASB_INTAKE_BOT_EMAIL", "intake@example.invalid")
    path = repo / "receipt.json"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    code = intake_github.main(
        ["--receipt", str(path), "--repo", str(repo), "--domain", "metabolomics"],
        env={"ASB_INTAKE_BOT_NAME": "asb-intake", "ASB_INTAKE_BOT_EMAIL": "intake@example.invalid"},
        run=runner,
    )
    assert code == 1
    assert "push failed" in capsys.readouterr().err


def test_no_absolute_paths_in_body_or_comment(repo: Path) -> None:
    """A local path in the receipt is scrubbed before it reaches GitHub."""
    runner = FakeRunner()
    receipt = staged_receipt(repo)
    receipt["warnings"] = [f"read {repo}/collections/metabolomics/proposals/wave.yaml"]
    receipt["comment_markdown"] = f"See {repo}/receipt.json and /etc/passwd for details."
    adapter(runner, repo).apply(receipt)
    text = "\n".join(runner.comments)
    pr_create = [command for command in commands(runner) if command[:3] == ["gh", "pr", "create"]]
    assert pr_create
    body = pr_create[0][pr_create[0].index("--body") + 1]
    assert str(repo) not in text + body
    assert "/etc/passwd" not in text + body
    assert "ASB_INTAKE_BOT_NAME" not in body


def test_domain_mismatch_is_refused(repo: Path) -> None:
    """A receipt for another domain is not applied."""
    runner = FakeRunner()
    receipt = staged_receipt(repo)
    receipt["domain"] = "epigenomics"
    with pytest.raises(intake_github.Refused):
        adapter(runner, repo).apply(receipt)
    assert runner.calls == []


def test_staged_missing_wave_file_is_refused(repo: Path) -> None:
    """A receipt naming a wave file that does not exist writes no branch."""
    runner = FakeRunner()
    receipt = staged_receipt(repo)
    (repo / "collections/metabolomics/proposals/wave-2026-11-community.yaml").unlink()
    with pytest.raises(intake_github.Refused):
        adapter(runner, repo).apply(receipt)
    assert runner.calls == []


def test_wave_file_outside_the_checkout_is_refused(repo: Path) -> None:
    """An absolute path outside the checkout cannot be committed."""
    runner = FakeRunner()
    receipt = staged_receipt(repo)
    receipt["wave_file"] = "/tmp/elsewhere/wave.yaml"
    with pytest.raises(intake_github.Refused):
        adapter(runner, repo).apply(receipt)
    assert runner.calls == []
