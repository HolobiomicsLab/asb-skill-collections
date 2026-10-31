"""The receipt, CITATION.cff and plugin-manifest jobs of validate.yml.

Three checks the release depends on ran nowhere in CI:

* `collections/metabolomics/v2/gate_report.json` failed its own
  `release_gate.py --verify` on main, and each later edit of a path it binds
  made it staler without turning anything red. The `receipt` job re-verifies
  it, read only, on pull requests that touch one of those paths.
* Every collection-level CITATION.cff failed CFF 1.2.0 validation (in
  metabolomics v2, references without authors or title). The `citation` job
  validates every tracked CITATION.cff outside the legacy v1 trees.
* `.claude-plugin/marketplace.json` failed `claude plugin validate --strict`,
  while gate 10 only checked that it carried `schema_version`, one of the keys
  that validator rejects. Gate 10 is now that validator, in its own job.

Each check is a job of its own, so a red one does not skip the gates of the
`validate` job. The static tests pin the jobs' text. The behavioural tests run
the receipt job's path filter and the citation job's file selection in a
throwaway git repository, with a stand-in for cffconvert.
"""
import os
import pathlib
import re
import shutil
import subprocess
import sys

import pytest

yaml = pytest.importorskip("yaml")

ROOT = pathlib.Path(__file__).parent.parent
VALIDATE = ROOT / ".github" / "workflows" / "validate.yml"

needs_git = pytest.mark.skipif(
    shutil.which("git") is None or shutil.which("bash") is None,
    reason="the behavioural tests run git and bash",
)


def _jobs() -> dict:
    return yaml.safe_load(VALIDATE.read_text())["jobs"]


def _step(job: dict, name_part: str) -> dict:
    found = [s for s in job["steps"] if name_part in s.get("name", "")]
    assert len(found) == 1, f"expected one step named like {name_part!r}, found {len(found)}"
    return found[0]


def _runs(job: dict) -> str:
    return "\n".join(s.get("run", "") for s in job["steps"])


def _git(repo: pathlib.Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid",
         "-c", "commit.gpgsign=false", *args],
        cwd=repo, check=True, capture_output=True, env=_clean_env(repo),
    )


def _clean_env(home: pathlib.Path, **extra: str) -> dict:
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin", "HOME": str(home),
           "GIT_CONFIG_NOSYSTEM": "1"}
    env.update(extra)
    return env


def _run_step(script: str, repo: pathlib.Path, **extra: str) -> subprocess.CompletedProcess:
    """Run a step body the way GitHub runs an unspecified shell: `bash -e <file>`."""
    body = repo.parent / "step.sh"
    body.write_text(script)
    return subprocess.run(["bash", "-e", str(body)], cwd=repo, capture_output=True,
                          text=True, env=_clean_env(repo.parent, **extra))


# -- receipt: the metabolomics v2 gate receipt re-verifies -----------------------

def test_receipt_job_verifies_the_v2_receipt_read_only():
    runs = _runs(_jobs()["receipt"])
    assert "python scripts/release_gate.py collections/metabolomics/v2 --verify" in runs
    assert "--report" not in runs, "the receipt is checked where it ships, never written elsewhere"
    assert "--strict" not in runs, "--strict rewrites the receipt; CI only re-verifies it"


def test_receipt_job_runs_on_pull_requests():
    assert "pull_request" in _jobs()["receipt"]["if"]


def test_receipt_checkout_reaches_the_base_parent():
    checkout = _step(_jobs()["receipt"], "Checkout")
    assert checkout["with"]["fetch-depth"] >= 2, (
        "the path filter diffs the merge commit against its first parent, "
        "which a depth-1 checkout does not have"
    )


def test_every_receipt_step_after_the_filter_waits_for_it():
    steps = _jobs()["receipt"]["steps"]
    names = [s.get("name", "") for s in steps]
    after = steps[[s.get("id") for s in steps].index("scope") + 1:]
    assert after, f"no step follows the path filter: {names}"
    for s in after:
        assert s.get("if") == "steps.scope.outputs.touched == 'true'", s.get("name")


def _bound_pattern() -> str:
    match = re.search(r"bound='([^']+)'", _step(_jobs()["receipt"], "binds")["run"])
    assert match, "the path filter must keep its pattern in a `bound='...'` variable"
    return match.group(1)


def test_the_filter_covers_every_file_the_receipt_hashes(monkeypatch):
    """The receipt's policy digests pii_config and the gate's own sources.

    A PR that edits one of them invalidates the receipt as surely as a
    collection edit does, so the filter must name each one. Read from the gate
    itself, so a source added to the digest later fails here until the
    filter names it too.
    """
    sys.path.insert(0, str(ROOT))
    from scripts import release_gate, release_receipt

    hashed: list[str] = []
    real = release_receipt.file_record

    def recording(path, label):
        hashed.append(pathlib.Path(path).resolve().relative_to(ROOT.resolve()).as_posix())
        return real(path, label)

    monkeypatch.setattr(release_receipt, "file_record", recording)
    release_gate._policy_snapshot()
    pattern = re.compile(_bound_pattern())
    assert hashed, "the policy snapshot hashed no source file"
    for path in [*hashed, "scripts/pii_config.py", "collections/metabolomics/v2/gate_report.json"]:
        assert pattern.search(path), f"{path} is bound by the receipt but not in the filter"


@needs_git
@pytest.mark.parametrize("changed, touched", [
    ("collections/metabolomics/v2/skills/a/SKILL.md", "true"),
    ("collections/epigenomics/v1/ABOUT.md", "true"),
    ("scripts/pii_config.py", "true"),
    ("scripts/release_gate.py", "true"),
    ("scripts/release_receipt.py", "true"),
    ("asb_skill_collections/layout.py", "true"),
    ("docs/STATUS.md", "false"),
    ("scripts/pii_config.py.orig", "false"),
    ("tests/collections/fixture.yaml", "false"),
])
def test_the_path_filter_decides_from_the_diff(tmp_path, changed, touched):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "README.md").write_text("base\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    target = repo / changed
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("change\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "change")
    output = tmp_path / "github_output"
    result = _run_step(_step(_jobs()["receipt"], "binds")["run"], repo,
                       GITHUB_OUTPUT=str(output))
    assert result.returncode == 0, result.stderr
    assert output.read_text().strip() == f"touched={touched}"


@needs_git
def test_the_path_filter_fails_rather_than_skip_without_the_base(tmp_path):
    """A shallow checkout must turn the job red, not read as 'nothing changed'."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "collections").mkdir()
    (repo / "collections" / "x.yaml").write_text("x\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "only")
    output = tmp_path / "github_output"
    result = _run_step(_step(_jobs()["receipt"], "binds")["run"], repo,
                       GITHUB_OUTPUT=str(output))
    assert result.returncode != 0
    assert not output.exists() or "touched=false" not in output.read_text()


# -- citation: every non-legacy CITATION.cff is valid CFF 1.2.0 ----------------

def test_cffconvert_is_pinned_in_its_own_environment():
    install = _step(_jobs()["citation"], "Install cffconvert")["run"]
    assert 'python -m venv "$RUNNER_TEMP/cffconvert"' in install, (
        "cffconvert 2.0.0 requires jsonschema<4; it must not share the job's environment"
    )
    assert '"cffconvert==2.0.0"' in install


def test_the_legacy_exemption_names_only_v1_trees():
    script = _step(_jobs()["citation"], "Validate every")["run"]
    case = re.search(r"case \"\$f\" in\s*\n\s*([^)]+)\)", script)
    assert case, "the legacy exemption must be one `case` pattern"
    patterns = [p.strip() for p in case.group(1).split("|")]
    assert patterns, "no legacy pattern"
    for p in patterns:
        assert re.fullmatch(r"collections/[a-z0-9-]+/v1/\*", p), (
            f"{p}: only the legacy v1 trees may skip validation"
        )


STUB_CFFCONVERT = """\
#!{python}
import os, sys
with open(os.environ["STUB_LOG"], "a") as fh:
    fh.write(sys.argv[-1] + "\\n")
if os.environ.get("STUB_FAIL_ON") and sys.argv[-1] == os.environ["STUB_FAIL_ON"]:
    print("stand-in refusal")
    sys.exit(1)
print("Citation metadata are valid according to schema version 1.2.0.")
"""


def _citation_repo(tmp_path: pathlib.Path, files: list[str]) -> pathlib.Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "README.md").write_text("x\n")
    for rel in files:
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("cff-version: 1.2.0\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "tree")
    stub = tmp_path / "runner" / "cffconvert" / "bin" / "cffconvert"
    stub.parent.mkdir(parents=True)
    stub.write_text(STUB_CFFCONVERT.format(python=sys.executable))
    stub.chmod(0o755)
    return repo


def _run_citation(tmp_path, repo, **extra):
    log = tmp_path / "calls.log"
    result = _run_step(_step(_jobs()["citation"], "Validate every")["run"], repo,
                       RUNNER_TEMP=str(tmp_path / "runner"), STUB_LOG=str(log), **extra)
    calls = log.read_text().splitlines() if log.exists() else []
    return result, calls


TREE = [
    "CITATION.cff",
    "collections/metabolomics/v2/CITATION.cff",
    "collections/metabolomics/v1/CITATION.cff",
    "collections/epigenomics/v1/CITATION.cff",
    "collections/transcriptomics/v1/CITATION.cff",
]


@needs_git
def test_every_tracked_non_legacy_file_is_validated(tmp_path):
    repo = _citation_repo(tmp_path, TREE)
    untracked = repo / "collections" / "scratch" / "v9" / "CITATION.cff"
    untracked.parent.mkdir(parents=True)
    untracked.write_text("cff-version: 1.2.0\n")
    result, calls = _run_citation(tmp_path, repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert sorted(calls) == ["CITATION.cff", "collections/metabolomics/v2/CITATION.cff"]
    assert result.stdout.count("SKIP:") == 3
    assert "2 of 2 CITATION.cff files are valid CFF 1.2.0" in result.stdout


@needs_git
def test_one_invalid_file_fails_the_step_and_the_rest_are_still_checked(tmp_path):
    repo = _citation_repo(tmp_path, TREE)
    result, calls = _run_citation(tmp_path, repo, STUB_FAIL_ON="CITATION.cff")
    assert result.returncode == 1
    assert "::error file=CITATION.cff::" in result.stdout
    assert len(calls) == 2, "a refusal must not stop the other files being checked"


@needs_git
def test_a_tree_with_only_legacy_files_fails_rather_than_pass_over_nothing(tmp_path):
    repo = _citation_repo(tmp_path, TREE[2:])
    result, calls = _run_citation(tmp_path, repo)
    assert result.returncode == 1
    assert calls == []
    assert "checked nothing" in result.stdout


# -- gate 10: plugin manifests pass Claude Code's own validator ---------------

def test_gate10_is_the_strict_plugin_validator():
    job = _jobs()["plugin-manifest"]
    assert _step(job, "Validate the marketplace")["run"].strip() == "claude plugin validate --strict ."


def test_the_validator_is_a_pinned_release_on_a_node_it_supports():
    job = _jobs()["plugin-manifest"]
    install = _step(job, "Install Claude Code")["run"]
    assert re.search(r'"@anthropic-ai/claude-code@\d+\.\d+\.\d+"', install), (
        "pin an exact release, so a new validator cannot turn the gate red on its own"
    )
    node = _step(job, "Node.js")["with"]["node-version"]
    assert int(str(node).split(".")[0]) >= 22, "Claude Code 2.1 requires Node.js 22 or later"


def test_the_validate_job_no_longer_requires_schema_version():
    assert "schema_version" not in _runs(_jobs()["validate"]), (
        "gate 10 required a key that `claude plugin validate --strict` rejects"
    )


def test_no_release_check_hides_behind_continue_on_error():
    jobs = _jobs()
    for name in ("receipt", "citation", "plugin-manifest"):
        assert "continue-on-error" not in jobs[name], name
        for s in jobs[name]["steps"]:
            assert "continue-on-error" not in s, f"{name}: {s.get('name')}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
