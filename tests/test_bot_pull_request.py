"""scripts/bot_pull_request.sh: regenerated files reach main through a pull request.

release.yml, career-stats-regen.yml and tier-update.yml pushed their commits
straight to main, which a branch rule requiring a pull request and the validate
check would refuse. They now call this script, which commits the given paths on
top of HEAD without moving it, points a bot/ branch at that commit and opens a
pull request into main through gh. The commit is built in a separate index, so
a change staged by an earlier step does not ride along.

Each test runs the script in a throwaway clone whose origin is a local bare
repository, with a stand-in for gh that records its arguments.
"""
import os
import pathlib
import shutil
import subprocess

import pytest

ROOT = pathlib.Path(__file__).parent.parent
SCRIPT = ROOT / "scripts" / "bot_pull_request.sh"

pytestmark = pytest.mark.skipif(
    shutil.which("git") is None or shutil.which("bash") is None,
    reason="the script runs git and bash",
)

GH_STUB = """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$GH_LOG"
if [ "$1 $2" = "pr list" ]; then
  echo "${GH_OPEN:-0}"
fi
"""


def _git(cwd: pathlib.Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
        cwd=cwd, check=True, capture_output=True, text=True,
    ).stdout.strip()


@pytest.fixture
def clone(tmp_path):
    origin = tmp_path / "origin.git"
    work = tmp_path / "work"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(work)], check=True)
    (work / "catalogue.jsonld").write_text("{}\n")
    (work / "other.txt").write_text("other\n")
    _git(work, "add", ".")
    _git(work, "commit", "-q", "-m", "base")
    _git(work, "remote", "add", "origin", str(origin))
    _git(work, "push", "-q", "origin", "main")
    _git(work, "config", "user.name", "bot")
    _git(work, "config", "user.email", "bot@example.invalid")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    gh = bin_dir / "gh"
    gh.write_text(GH_STUB)
    gh.chmod(0o755)
    return work, origin, tmp_path / "gh.log"


def _run(work, log, *args, open_prs="0"):
    env = {**os.environ, "PATH": f"{log.parent / 'bin'}{os.pathsep}{os.environ['PATH']}",
           "GH_LOG": str(log), "GH_OPEN": open_prs, "GH_TOKEN": "unused",
           "GITHUB_WORKFLOW": "Release"}
    return subprocess.run(["bash", str(SCRIPT), *args], cwd=work, env=env,
                          capture_output=True, text=True)


def _remote_head(origin: pathlib.Path, ref: str) -> str:
    found = subprocess.run(["git", "--git-dir", str(origin), "rev-parse", "--verify", "-q", ref],
                           capture_output=True, text=True)
    return found.stdout.strip()


def _gh_calls(log: pathlib.Path) -> list[str]:
    return log.read_text().splitlines() if log.exists() else []


def test_changes_go_to_a_bot_branch_and_a_pull_request_into_main(clone):
    work, origin, log = clone
    main_before = _remote_head(origin, "refs/heads/main")
    head_before = _git(work, "rev-parse", "HEAD")
    (work / "catalogue.jsonld").write_text('{"v": 2}\n')
    (work / "other.txt").write_text("unrelated edit\n")

    result = _run(work, log, "bot/catalogue-dom-v1", "chore: regen", "catalogue.jsonld")

    assert result.returncode == 0, result.stderr
    assert _remote_head(origin, "refs/heads/main") == main_before
    pushed = _remote_head(origin, "refs/heads/bot/catalogue-dom-v1")
    assert _git(work, "rev-parse", f"{pushed}^") == head_before
    changed = _git(work, "diff", "--name-only", head_before, pushed).splitlines()
    assert changed == ["catalogue.jsonld"]
    assert _git(work, "rev-parse", "HEAD") == head_before
    assert (work / "catalogue.jsonld").read_text() == '{"v": 2}\n'
    assert _git(work, "diff", "--cached", "--name-only") == ""
    calls = _gh_calls(log)
    assert calls[0].startswith("pr list --head bot/catalogue-dom-v1 --base main")
    assert calls[1].startswith("pr create --base main --head bot/catalogue-dom-v1 --title chore: regen")
    assert "Release workflow" in calls[1]


def test_a_change_staged_by_an_earlier_step_stays_out_of_the_bot_commit(clone):
    work, origin, log = clone
    head_before = _git(work, "rev-parse", "HEAD")
    (work / "other.txt").write_text("staged elsewhere\n")
    _git(work, "add", "other.txt")
    (work / "catalogue.jsonld").write_text('{"v": 2}\n')

    result = _run(work, log, "bot/catalogue-dom-v1", "chore: regen", "catalogue.jsonld")

    assert result.returncode == 0, result.stderr
    pushed = _remote_head(origin, "refs/heads/bot/catalogue-dom-v1")
    changed = _git(work, "diff", "--name-only", head_before, pushed).splitlines()
    assert changed == ["catalogue.jsonld"]
    assert _git(work, "diff", "--cached", "--name-only") == "other.txt"


def test_only_a_staged_change_elsewhere_proposes_nothing(clone):
    work, origin, log = clone
    (work / "other.txt").write_text("staged elsewhere\n")
    _git(work, "add", "other.txt")

    result = _run(work, log, "bot/catalogue-dom-v1", "chore: regen", "catalogue.jsonld")

    assert result.returncode == 0, result.stderr
    assert "No changes to propose" in result.stdout
    assert _remote_head(origin, "refs/heads/bot/catalogue-dom-v1") == ""
    assert _gh_calls(log) == []


def test_an_open_pull_request_gets_the_new_commit_and_no_second_one(clone):
    work, origin, log = clone
    (work / "catalogue.jsonld").write_text('{"v": 2}\n')
    assert _run(work, log, "bot/stats", "first", "catalogue.jsonld").returncode == 0
    (work / "catalogue.jsonld").write_text('{"v": 3}\n')

    result = _run(work, log, "bot/stats", "second", "catalogue.jsonld", open_prs="1")

    assert result.returncode == 0, result.stderr
    pushed = _remote_head(origin, "refs/heads/bot/stats")
    assert _git(work, "show", f"{pushed}:catalogue.jsonld") == '{"v": 3}'
    assert sum(call.startswith("pr create") for call in _gh_calls(log)) == 1


def test_no_change_pushes_nothing_and_opens_nothing(clone):
    work, origin, log = clone
    result = _run(work, log, "bot/stats", "chore", "catalogue.jsonld")
    assert result.returncode == 0, result.stderr
    assert "No changes" in result.stdout
    assert _remote_head(origin, "refs/heads/bot/stats") == ""
    assert _gh_calls(log) == []


def test_missing_paths_are_skipped(clone):
    work, origin, log = clone
    (work / "catalogue.jsonld").write_text('{"v": 2}\n')
    result = _run(work, log, "bot/doi", "chore", "CITATION.cff", "catalogue.jsonld")
    assert result.returncode == 0, result.stderr
    assert _remote_head(origin, "refs/heads/bot/doi") != ""


@pytest.mark.parametrize("branch", ["main", "HEAD:main", "feature/x", "bot/"])
def test_a_branch_outside_bot_is_refused(clone, branch):
    work, origin, log = clone
    main_before = _remote_head(origin, "refs/heads/main")
    (work / "catalogue.jsonld").write_text('{"v": 2}\n')
    result = _run(work, log, branch, "chore", "catalogue.jsonld")
    assert result.returncode == 2
    assert _remote_head(origin, "refs/heads/main") == main_before
    assert _gh_calls(log) == []


def test_a_bot_branch_moved_since_it_was_read_is_not_overwritten(clone, monkeypatch):
    work, origin, log = clone
    (work / "catalogue.jsonld").write_text('{"v": 2}\n')
    assert _run(work, log, "bot/stats", "first", "catalogue.jsonld").returncode == 0
    first = _remote_head(origin, "refs/heads/bot/stats")
    # A git wrapper that moves the bot branch on the remote right after the
    # script reads it, as a concurrent run would.
    real_git = shutil.which("git")
    wrapper = log.parent / "bin" / "git"
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        f'out="$("{real_git}" "$@")"; status=$?\n'
        'printf "%s" "$out"; [ -n "$out" ] && echo\n'
        'if [ "$1" = "ls-remote" ]; then\n'
        f'  "{real_git}" --git-dir "{origin}" update-ref refs/heads/bot/stats "$("{real_git}" --git-dir "{origin}" rev-parse refs/heads/main)"\n'
        "fi\n"
        "exit $status\n"
    )
    wrapper.chmod(0o755)
    (work / "catalogue.jsonld").write_text('{"v": 3}\n')
    result = _run(work, log, "bot/stats", "second", "catalogue.jsonld", open_prs="1")
    assert result.returncode != 0
    assert _remote_head(origin, "refs/heads/bot/stats") != first
    assert _remote_head(origin, "refs/heads/bot/stats") == _remote_head(origin, "refs/heads/main")
