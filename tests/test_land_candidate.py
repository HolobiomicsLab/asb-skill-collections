"""Contract tests for landing an assembled candidate on a private repo branch."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "land_candidate.py"
ASSEMBLER = REPO / "scripts" / "assemble_candidate.py"
FIXTURE = REPO / "tests" / "fixtures" / "cut_three_outputs"
DOMAIN = "metabarcoding"
VERSION = "v1"
TITLE = "ASB Metabarcoding Skill Collection v1"
CUT_ID = "c631e4625159"
ASB_COMMIT = "0123456789abcdef0123456789abcdef01234567"
TOOLING_COMMIT = "1123456789abcdef0123456789abcdef01234567"
CORPUS_COMMIT = "2123456789abcdef0123456789abcdef01234567"
BRANCH = f"candidate/{CUT_ID}"
COLLECTION_PATH = f"collections/{DOMAIN}/{VERSION}"
RECEIPTS_PATH = f"receipts/{CUT_ID}"
MARKETPLACE_PATH = ".claude-plugin/marketplace.json"
SUBJECT = f"feat(candidate): {DOMAIN} {VERSION} candidate {CUT_ID}"
OWNER = {
    "name": "Holobiomics Lab",
    "url": "https://github.com/HolobiomicsLab",
    "orcid_org": "https://orcid.org/0000-0001-6711-6719",
}


def _clean_environment() -> dict[str, str]:
    """Return the mandated offline, credential-free test environment."""
    environment = dict(os.environ)
    for key in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY"):
        environment.pop(key, None)
    environment.update(
        HF_HUB_OFFLINE="1",
        TRANSFORMERS_OFFLINE="1",
        ASB_EMBED_MODEL="bge-small-en-v1.5",
        PYTHONDONTWRITEBYTECODE="1",
    )
    return environment


def _run_process(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run one fixture command and retain both output streams."""
    return subprocess.run(
        command,
        cwd=cwd,
        env=_clean_environment(),
        text=True,
        capture_output=True,
        check=False,
    )


def _git(
    repo: Path, *arguments: str, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run git only against a test-owned temporary repository."""
    result = _run_process(["git", "-C", str(repo), *arguments], repo.parent)
    if check and result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return result


def _tree_bytes(root: Path) -> dict[str, bytes]:
    """Return all regular files below a tree in stable relative-path order."""
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


def _tree_digest(root: Path) -> str:
    """Match the collector digest for a test-local candidate mutation."""
    digest = hashlib.sha256()
    for relative, content in sorted(_tree_bytes(root).items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(content).digest())
    return digest.hexdigest()


@pytest.fixture(scope="module")
def assembled(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, Path]:
    """Run the Task 6 driver once and expose its complete candidate and receipts."""
    root = tmp_path_factory.mktemp("assembled-candidate")
    candidate = root / "candidate"
    receipts = root / "receipts"
    command = [
        sys.executable,
        str(ASSEMBLER),
        "--cut",
        str(FIXTURE / "corpus"),
        "--builds",
        str(FIXTURE / "builds"),
        "--tiered",
        str(FIXTURE / "metabarcoding_tiered.json"),
        "--domain",
        DOMAIN,
        "--version",
        VERSION,
        "--out",
        str(candidate),
        "--receipts",
        str(receipts),
        "--asb-commit",
        ASB_COMMIT,
        "--tooling-commit",
        TOOLING_COMMIT,
        "--corpus-commit",
        CORPUS_COMMIT,
        "--verified-on",
        "2026-09-18",
    ]
    result = _run_process(command, REPO)
    assert result.returncode == 0, result.stdout + result.stderr
    source = json.loads((receipts / "source.json").read_text(encoding="utf-8"))
    assert source["status"] == "complete"
    assert source["cut_id"] == CUT_ID
    assert json.loads((receipts / "gate_report.json").read_text())["release_verified"]
    return candidate, receipts


def _copy_inputs(assembled: tuple[Path, Path], tmp_path: Path) -> tuple[Path, Path]:
    """Copy the immutable assembled fixture for a mutating refusal test."""
    candidate = tmp_path / "candidate"
    receipts = tmp_path / "receipts-input"
    shutil.copytree(assembled[0], candidate)
    shutil.copytree(assembled[1], receipts)
    return candidate, receipts


def _create_repo(
    tmp_path: Path,
    *,
    configure_identity: bool = True,
    existing_target: bool = False,
) -> tuple[Path, str, bytes]:
    """Create a clean domain-repository fixture with one commit on main."""
    repo = tmp_path / "domain-repo"
    repo.mkdir()
    result = _run_process(["git", "init", "-b", "main", str(repo)], tmp_path)
    assert result.returncode == 0, result.stderr
    if configure_identity:
        _git(repo, "config", "user.name", "Landing Fixture")
        _git(repo, "config", "user.email", "landing@example.org")
    (repo / "README.md").write_text("# Fixture domain repository\n", encoding="utf-8")
    (repo / "LICENSE").write_text("CC-BY-4.0 fixture\n", encoding="utf-8")
    zenodo = b'{"metadata":{"title":"fixture deposit"}}\n'
    (repo / ".zenodo.json").write_bytes(zenodo)
    if existing_target:
        target = repo / COLLECTION_PATH
        target.mkdir(parents=True)
        (target / "occupied.txt").write_text("occupied\n", encoding="utf-8")
    _git(repo, "add", "--", ".")
    commit = ["git", "-C", str(repo)]
    if not configure_identity:
        commit.extend(
            ["-c", "user.name=Initial Fixture", "-c", "user.email=initial@example.org"]
        )
    commit.extend(["commit", "-m", "chore: initial domain repository"])
    result = _run_process(commit, tmp_path)
    assert result.returncode == 0, result.stderr
    return repo, _git(repo, "rev-parse", "HEAD").stdout.strip(), zenodo


def _land(
    candidate: Path,
    receipts: Path,
    repo: Path,
    *,
    dry_run: bool = False,
    author: tuple[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Invoke the S8 path interface from outside the target repository."""
    command = [
        sys.executable,
        str(SCRIPT),
        "--candidate",
        str(candidate),
        "--receipts",
        str(receipts),
        "--repo",
        str(repo),
        "--domain",
        DOMAIN,
        "--version",
        VERSION,
        "--title",
        TITLE,
    ]
    if author:
        command.extend(("--author-name", author[0], "--author-email", author[1]))
    if dry_run:
        command.append("--dry-run")
    return _run_process(command, repo.parent)


def _json_output(result: subprocess.CompletedProcess[str]) -> dict:
    """Decode the command's final non-empty stdout line."""
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert lines, result.stderr
    return json.loads(lines[-1])


def _branches(repo: Path) -> list[str]:
    """List local branch names without changing the test repository."""
    output = _git(repo, "branch", "--format=%(refname:short)").stdout
    return sorted(output.splitlines())


def test_dry_run_prints_plan_and_does_not_write_git_or_files(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Read preconditions and refs while leaving main and its worktree untouched."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    repo, initial, zenodo = _create_repo(tmp_path)
    before = _tree_bytes(repo)

    result = _land(candidate, receipts, repo, dry_run=True)

    assert result.returncode == 0, result.stdout + result.stderr
    assert _json_output(result) == {
        "branch": BRANCH,
        "dry_run": True,
        "message": SUBJECT,
        "paths": {
            "collection": COLLECTION_PATH,
            "marketplace": MARKETPLACE_PATH,
            "receipts": RECEIPTS_PATH,
            "zenodo": f"{COLLECTION_PATH}/.zenodo.json",
        },
    }
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == initial
    assert _git(repo, "branch", "--show-current").stdout.strip() == "main"
    assert _branches(repo) == ["main"]
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert _tree_bytes(repo) == before
    assert (repo / ".zenodo.json").read_bytes() == zenodo


def test_real_run_lands_exact_candidate_receipts_marketplace_and_commit(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Create one candidate branch while preserving the initial main commit."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    repo, initial, zenodo = _create_repo(tmp_path)
    descriptor = yaml.safe_load((candidate / "collection.yaml").read_text())

    result = _land(candidate, receipts, repo)

    assert result.returncode == 0, result.stdout + result.stderr
    report = _json_output(result)
    assert set(report) == {"branch", "commit", "files"}
    assert report["branch"] == BRANCH
    assert report["commit"] == _git(repo, "rev-parse", "HEAD").stdout.strip()
    assert (
        report["files"] == len(_tree_bytes(candidate)) + len(_tree_bytes(receipts)) + 2
    )
    assert _git(repo, "branch", "--show-current").stdout.strip() == BRANCH
    assert _git(repo, "rev-parse", "main").stdout.strip() == initial
    assert _git(repo, "rev-parse", "HEAD^").stdout.strip() == initial
    assert _git(repo, "status", "--porcelain").stdout == ""

    landed = repo / COLLECTION_PATH
    landed_tree = _tree_bytes(landed)
    assert landed_tree.pop(".zenodo.json") == zenodo
    assert landed_tree == _tree_bytes(candidate)
    assert _tree_bytes(repo / RECEIPTS_PATH) == _tree_bytes(receipts)
    assert not (repo / ".zenodo.json").exists()

    marketplace = json.loads((repo / MARKETPLACE_PATH).read_text(encoding="utf-8"))
    plugin_description = (
        f"{TITLE}, candidate from cut {CUT_ID}: {descriptor['skills_count']} "
        f"evidence-grounded skills over {descriptor['tools_count']} tools, each "
        "derived from a peer-reviewed method paper, generated by the "
        "AgenticScienceBuilder pipeline. Not a release; see "
        f"receipts/{CUT_ID}/."
    )
    repository_url = f"https://github.com/HolobiomicsLab/asb-skills-{DOMAIN}"
    assert marketplace == {
        "schema_version": "1.0",
        "name": f"asb-skills-{DOMAIN}",
        "description": (
            f"ASB {DOMAIN} skill collections: evidence-grounded scientific-agent "
            "skills and tool records from the AgenticScienceBuilder pipeline. "
            "Registry, tooling and governance: "
            "https://github.com/HolobiomicsLab/asb-skill-collections."
        ),
        "owner": OWNER,
        "publisher": OWNER,
        "release": False,
        "plugins": [
            {
                "name": DOMAIN,
                "source": f"./{COLLECTION_PATH}",
                "description": plugin_description,
                "version": "0.1.0",
                "author": {
                    "name": "Holobiomics Lab",
                    "url": "https://github.com/HolobiomicsLab",
                },
                "license": "CC-BY-4.0",
                "keywords": [DOMAIN],
                "homepage": repository_url,
                "repository": repository_url,
            }
        ],
    }

    message = _git(repo, "log", "-1", "--format=%B").stdout.strip()
    assert message == "\n".join(
        [
            SUBJECT,
            "",
            f"asb_commit: {ASB_COMMIT}",
            f"tooling_commit: {TOOLING_COMMIT}",
            f"corpus_commit: {CORPUS_COMMIT}",
            f"cut_id: {CUT_ID}",
            f"receipts: {RECEIPTS_PATH}/",
        ]
    )
    assert _git(repo, "log", "-1", "--format=%an <%ae>").stdout.strip() == (
        "Landing Fixture <landing@example.org>"
    )
    assert (repo / COLLECTION_PATH / "corpus.yaml").is_file()
    assert (repo / RECEIPTS_PATH / "source.json").is_file()
    assert (repo / MARKETPLACE_PATH).is_file()


def test_existing_candidate_branch_is_conflict_and_second_run_exits_two(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Classify an already landed cut as conflict after returning to main."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    repo, initial, _ = _create_repo(tmp_path)
    first = _land(candidate, receipts, repo)
    assert first.returncode == 0, first.stdout + first.stderr
    landed_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "checkout", "main")

    second = _land(candidate, receipts, repo)

    assert second.returncode == 2
    assert "already exists" in (second.stderr + second.stdout).lower()
    assert _git(repo, "branch", "--show-current").stdout.strip() == "main"
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == initial
    assert _git(repo, "rev-parse", BRANCH).stdout.strip() == landed_commit
    assert _git(repo, "status", "--porcelain").stdout == ""


@pytest.mark.parametrize(
    ("receipt", "field", "value", "reason"),
    [
        ("gate_report.json", "release_verified", False, "release_verified"),
        ("source.json", "status", "incomplete", "status"),
    ],
)
def test_incomplete_receipts_are_refused_before_branch_creation(
    assembled: tuple[Path, Path],
    tmp_path: Path,
    receipt: str,
    field: str,
    value: object,
    reason: str,
) -> None:
    """Require completed assembly and a verified release gate."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    payload_path = receipts / receipt
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    payload[field] = value
    payload_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    repo, initial, _ = _create_repo(tmp_path)

    result = _land(candidate, receipts, repo)

    assert result.returncode == 1
    assert reason in (result.stderr + result.stdout)
    assert _branches(repo) == ["main"]
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == initial
    assert _git(repo, "status", "--porcelain").stdout == ""


@pytest.mark.parametrize("repo_state", ["dirty", "wrong-branch", "nonrepo"])
def test_invalid_repository_state_is_refused_without_candidate_branch(
    assembled: tuple[Path, Path], tmp_path: Path, repo_state: str
) -> None:
    """Require a clean git worktree whose checked-out branch is main."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    if repo_state == "nonrepo":
        repo = tmp_path / "domain-repo"
        repo.mkdir()
        initial = None
    else:
        repo, initial, _ = _create_repo(tmp_path)
        if repo_state == "dirty":
            (repo / "README.md").write_text("dirty\n", encoding="utf-8")
        else:
            _git(repo, "checkout", "-b", "work")

    result = _land(candidate, receipts, repo)

    assert result.returncode == 1
    assert (
        "repository" in (result.stderr + result.stdout).lower()
        or repo_state.split("-")[0] in (result.stderr + result.stdout).lower()
    )
    if initial is not None:
        assert BRANCH not in _branches(repo)
        assert _git(repo, "rev-parse", "main").stdout.strip() == initial


def test_existing_collection_target_is_refused_before_branch_creation(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Never overlay a collection version already present on main."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    repo, initial, _ = _create_repo(tmp_path, existing_target=True)

    result = _land(candidate, receipts, repo)

    assert result.returncode == 1
    assert "exists" in (result.stderr + result.stdout).lower()
    assert _branches(repo) == ["main"]
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == initial
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_candidate_symlink_is_refused_before_branch_creation(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Reject non-regular candidate entries instead of dereferencing them."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    (candidate / "unsafe-link").symlink_to(candidate / "collection.yaml")
    repo, initial, _ = _create_repo(tmp_path)

    result = _land(candidate, receipts, repo)

    assert result.returncode == 1
    assert "symlink" in (result.stderr + result.stdout).lower()
    assert _branches(repo) == ["main"]
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == initial


def test_candidate_owned_zenodo_is_kept_without_moving_repository_metadata(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Keep the root deposit file when the candidate already supplies its own."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    candidate_zenodo = b'{"metadata":{"title":"candidate deposit"}}\n'
    (candidate / ".zenodo.json").write_bytes(candidate_zenodo)
    source_path = receipts / "source.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source["output_tree_sha256"] = _tree_digest(candidate)
    source_path.write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
    repo, _, repository_zenodo = _create_repo(tmp_path)

    result = _land(candidate, receipts, repo)

    assert result.returncode == 0, result.stdout + result.stderr
    assert (repo / COLLECTION_PATH / ".zenodo.json").read_bytes() == candidate_zenodo
    assert (repo / ".zenodo.json").read_bytes() == repository_zenodo
    assert _json_output(result)["files"] == (
        len(_tree_bytes(candidate)) + len(_tree_bytes(receipts)) + 1
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_missing_identity_requires_both_cli_author_fields_and_does_not_configure_repo(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Apply an explicit fallback identity to the commit command only."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    repo, initial, _ = _create_repo(tmp_path, configure_identity=False)

    refused = _land(candidate, receipts, repo)
    assert refused.returncode == 1
    assert "no git identity" in (refused.stderr + refused.stdout).lower()
    assert _branches(repo) == ["main"]
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == initial

    landed = _land(
        candidate,
        receipts,
        repo,
        author=("Candidate Builder", "builder@example.org"),
    )
    assert landed.returncode == 0, landed.stdout + landed.stderr
    assert _git(repo, "log", "-1", "--format=%an <%ae>").stdout.strip() == (
        "Candidate Builder <builder@example.org>"
    )
    assert (
        _git(repo, "config", "--local", "--get", "user.name", check=False).returncode
        == 1
    )
    assert (
        _git(repo, "config", "--local", "--get", "user.email", check=False).returncode
        == 1
    )


V2_VERSION = "v2"
V2_TITLE = "ASB Metabarcoding Skill Collection v2"
V2_COLLECTION_PATH = f"collections/{DOMAIN}/{V2_VERSION}"
V2_SUBJECT = f"feat(candidate): {DOMAIN} {V2_VERSION} candidate {CUT_ID}"
REFERENCE_MARKETPLACE = REPO / "tests" / "fixtures" / "marketplace_transcriptomics.json"
RELEASE_RECEIPTS_PATH = "receipts/split-2026-09-17"


def _copy_v2_inputs(assembled: tuple[Path, Path], tmp_path: Path) -> tuple[Path, Path]:
    """Derive valid v2 inputs by changing only landing-validated candidate facts."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    descriptor_path = candidate / "collection.yaml"
    descriptor = yaml.safe_load(descriptor_path.read_text(encoding="utf-8"))
    descriptor.update(version=2, title=V2_TITLE)
    descriptor_path.write_text(
        yaml.safe_dump(descriptor, sort_keys=False), encoding="utf-8"
    )

    source_path = receipts / "source.json"
    source = json.loads(source_path.read_text(encoding="utf-8"))
    source.update(version=V2_VERSION, output_tree_sha256=_tree_digest(candidate))
    source_path.write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
    return candidate, receipts


def _released_marketplace_payload(*, name: str | None = None) -> dict:
    """Adapt the real transcriptomics marketplace fixture to the test domain."""
    payload = json.loads(REFERENCE_MARKETPLACE.read_text(encoding="utf-8"))
    domain_title = DOMAIN.replace("-", " ").title()
    payload["name"] = name or f"asb-skills-{DOMAIN}"
    payload["description"] = payload["description"].replace("transcriptomics", DOMAIN)
    plugin = payload["plugins"][0]
    plugin["name"] = DOMAIN
    plugin["source"] = f"./{COLLECTION_PATH}"
    plugin["description"] = plugin["description"].replace(
        "Transcriptomics", domain_title
    )
    plugin["keywords"] = [DOMAIN]
    repository = f"https://github.com/HolobiomicsLab/asb-skills-{DOMAIN}"
    plugin.update(homepage=repository, repository=repository)
    return payload


def _create_released_repo(
    tmp_path: Path, *, marketplace_name: str | None = None
) -> tuple[Path, str, bytes, bytes]:
    """Create main with a tracked released v1 and its real marketplace shape."""
    repo, _, zenodo = _create_repo(tmp_path)
    marketplace_path = repo / MARKETPLACE_PATH
    marketplace_path.parent.mkdir(parents=True)
    marketplace_path.write_text(
        json.dumps(
            _released_marketplace_payload(name=marketplace_name),
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    collection = repo / COLLECTION_PATH / "collection.yaml"
    collection.parent.mkdir(parents=True)
    collection.write_text(
        yaml.safe_dump(
            {
                "slug": DOMAIN,
                "version": 1,
                "title": TITLE,
                "status": "released",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    source = repo / RELEASE_RECEIPTS_PATH / "source.json"
    source.parent.mkdir(parents=True)
    source.write_text(
        json.dumps(
            {
                "status": "complete",
                "cut_id": "split-2026-09-17",
                "domain": DOMAIN,
                "version": VERSION,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    _git(repo, "add", "--", MARKETPLACE_PATH, COLLECTION_PATH, RELEASE_RECEIPTS_PATH)
    _git(repo, "commit", "-m", "feat: release fixture v1")
    return (
        repo,
        _git(repo, "rev-parse", "HEAD").stdout.strip(),
        zenodo,
        marketplace_path.read_bytes(),
    )


def _v2_arguments(candidate: Path, receipts: Path, repo: Path) -> list[str]:
    """Build the v2 CLI arguments shared by subprocess and in-process tests."""
    return [
        "--candidate",
        str(candidate),
        "--receipts",
        str(receipts),
        "--repo",
        str(repo),
        "--domain",
        DOMAIN,
        "--version",
        V2_VERSION,
        "--title",
        V2_TITLE,
    ]


def _land_v2(
    candidate: Path, receipts: Path, repo: Path, *, dry_run: bool = False
) -> subprocess.CompletedProcess[str]:
    """Invoke the landing command for a candidate derived as v2."""
    command = [sys.executable, str(SCRIPT), *_v2_arguments(candidate, receipts, repo)]
    if dry_run:
        command.append("--dry-run")
    return _run_process(command, repo.parent)


def _load_landing_module(monkeypatch: pytest.MonkeyPatch) -> object:
    """Load the landing script as an isolated module for failure injection."""
    importlib_util = __import__("importlib.util", fromlist=["module_from_spec"])
    module_name = "land_candidate_rollback_test"
    spec = importlib_util.spec_from_file_location(module_name, SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib_util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, module_name, module)
    spec.loader.exec_module(module)
    return module


def test_v2_lands_by_appending_to_tracked_released_marketplace(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Append a v2 candidate without changing the released v1 entry or main."""
    candidate, receipts = _copy_v2_inputs(assembled, tmp_path)
    repo, initial, zenodo, original_bytes = _create_released_repo(tmp_path)
    original = json.loads(original_bytes)

    result = _land_v2(candidate, receipts, repo)

    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(repo, "branch", "--show-current").stdout.strip() == BRANCH
    assert _git(repo, "rev-parse", "main").stdout.strip() == initial
    assert _git(repo, "status", "--porcelain").stdout == ""
    landed = _tree_bytes(repo / V2_COLLECTION_PATH)
    assert landed.pop(".zenodo.json") == zenodo
    assert landed == _tree_bytes(candidate)
    assert not (repo / ".zenodo.json").exists()

    marketplace = json.loads((repo / MARKETPLACE_PATH).read_bytes())
    assert list(marketplace) == list(original)
    assert "release" not in marketplace
    assert marketplace["plugins"][0] == original["plugins"][0]
    assert list(marketplace["plugins"][0]) == list(original["plugins"][0])
    assert len(marketplace["plugins"]) == 2
    assert marketplace["plugins"][1]["source"] == f"./{V2_COLLECTION_PATH}"
    assert marketplace["plugins"][1]["release"] is False


def test_released_v1_marketplace_duplicate_exits_two_before_branch_creation(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Classify the existing v1 marketplace entry as the first conflict."""
    candidate, receipts = _copy_inputs(assembled, tmp_path)
    repo, initial, _, _ = _create_released_repo(tmp_path)

    result = _land(candidate, receipts, repo)

    assert result.returncode == 2
    assert f"marketplace already lists ./{COLLECTION_PATH}" in (
        result.stderr + result.stdout
    )
    assert _branches(repo) == ["main"]
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == initial
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_wrong_existing_marketplace_name_is_refused_before_branch_creation(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Reject a tracked marketplace owned by a different domain repository."""
    candidate, receipts = _copy_v2_inputs(assembled, tmp_path)
    repo, initial, _, _ = _create_released_repo(
        tmp_path, marketplace_name="asb-skills-wrong-domain"
    )

    result = _land_v2(candidate, receipts, repo)

    assert result.returncode == 1
    assert "name" in (result.stderr + result.stdout)
    assert _branches(repo) == ["main"]
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == initial
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_tracked_marketplace_is_restored_when_commit_fails(
    assembled: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Restore tracked main content and remove the candidate branch on rollback."""
    candidate, receipts = _copy_v2_inputs(assembled, tmp_path)
    repo, initial, zenodo, marketplace_bytes = _create_released_repo(tmp_path)
    module = _load_landing_module(monkeypatch)
    commit_calls = 0

    def fail_commit(_plan: object) -> None:
        nonlocal commit_calls
        commit_calls += 1
        raise module.LandingError("forced commit failure")

    monkeypatch.setattr(module, "_commit", fail_commit)
    exit_code = module.main(_v2_arguments(candidate, receipts, repo))
    captured = capsys.readouterr()

    assert exit_code == 1
    assert commit_calls == 1
    assert "landing failed: forced commit failure" in captured.err
    assert _git(repo, "branch", "--show-current").stdout.strip() == "main"
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == initial
    assert _branches(repo) == ["main"]
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert (repo / MARKETPLACE_PATH).read_bytes() == marketplace_bytes
    assert (repo / ".zenodo.json").read_bytes() == zenodo
    assert not (repo / V2_COLLECTION_PATH).exists()


def test_merge_dry_run_reports_marketplace_mode_without_writes(
    assembled: tuple[Path, Path], tmp_path: Path
) -> None:
    """Expose merge mode in the plan while leaving the released repo untouched."""
    candidate, receipts = _copy_v2_inputs(assembled, tmp_path)
    repo, initial, zenodo, _ = _create_released_repo(tmp_path)
    before = _tree_bytes(repo)

    result = _land_v2(candidate, receipts, repo, dry_run=True)

    assert result.returncode == 0, result.stdout + result.stderr
    assert _json_output(result) == {
        "branch": BRANCH,
        "dry_run": True,
        "marketplace": {"path": MARKETPLACE_PATH, "mode": "merge"},
        "message": V2_SUBJECT,
        "paths": {
            "collection": V2_COLLECTION_PATH,
            "marketplace": MARKETPLACE_PATH,
            "receipts": RECEIPTS_PATH,
            "zenodo": f"{V2_COLLECTION_PATH}/.zenodo.json",
        },
    }
    assert _git(repo, "rev-parse", "HEAD").stdout.strip() == initial
    assert _git(repo, "branch", "--show-current").stdout.strip() == "main"
    assert _branches(repo) == ["main"]
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert _tree_bytes(repo) == before
    assert (repo / ".zenodo.json").read_bytes() == zenodo
