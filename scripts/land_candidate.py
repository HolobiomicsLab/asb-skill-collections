#!/usr/bin/env python3
"""Land a verified domain candidate on an unpushed Git branch (S8)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


DOMAIN_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_PATTERN = re.compile(r"^v([1-9][0-9]*)$")
CUT_PATTERN = re.compile(r"^[0-9a-f]{12}$")
COMMIT_PATTERN = re.compile(r"^[0-9a-fA-F]{7,40}$")
OWNER = {
    "name": "Holobiomics Lab",
    "url": "https://github.com/HolobiomicsLab",
    "orcid_org": "https://orcid.org/0000-0001-6711-6719",
}
AUTHOR = {
    "name": "Holobiomics Lab",
    "url": "https://github.com/HolobiomicsLab",
}


class LandingError(RuntimeError):
    """An invalid input or repository state that exits with status one."""


class ConflictError(LandingError):
    """An existing candidate branch that exits with status two."""


@dataclass(frozen=True)
class CandidateInput:
    """Validated immutable candidate facts and regular-file inventories."""

    candidate: Path
    receipts: Path
    candidate_files: tuple[tuple[Path, Path], ...]
    receipt_files: tuple[tuple[Path, Path], ...]
    source: dict[str, Any]
    descriptor: dict[str, Any]


@dataclass(frozen=True)
class RepositoryInput:
    """Validated repository location and optional fallback commit identity."""

    root: Path
    fallback_identity: tuple[str, str] | None
    marketplace: dict[str, Any] | None


@dataclass(frozen=True)
class LandingPlan:
    """All validated facts needed to describe or execute one landing."""

    inputs: CandidateInput
    repository: RepositoryInput
    branch: str
    collection_path: str
    receipts_path: str
    marketplace_path: str
    message: str


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Land a verified release candidate on a local candidate branch."
    )
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--receipts", required=True, type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--author-name")
    parser.add_argument("--author-email")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def _read_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise LandingError(f"required regular file is missing: {label}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise LandingError(f"invalid JSON in {label}: {exc}") from exc
    if not isinstance(payload, dict):
        raise LandingError(f"{label} must contain a JSON object")
    return payload


def _read_yaml(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise LandingError(f"required regular file is missing: {label}")
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise LandingError(f"invalid YAML in {label}: {exc}") from exc
    if not isinstance(payload, dict):
        raise LandingError(f"{label} must contain a YAML mapping")
    return payload


def _regular_files(root: Path, label: str) -> tuple[tuple[Path, Path], ...]:
    if not root.is_dir() or root.is_symlink():
        raise LandingError(f"{label} must be a regular directory: {root}")
    files: list[tuple[Path, Path]] = []
    for path in sorted(
        root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()
    ):
        relative = path.relative_to(root)
        if path.is_symlink():
            raise LandingError(f"{label} contains a symlink: {relative.as_posix()}")
        if path.is_file():
            files.append((relative, path))
        elif not path.is_dir():
            raise LandingError(
                f"{label} contains a non-regular entry: {relative.as_posix()}"
            )
    return tuple(files)


def _tree_digest(files: tuple[tuple[Path, Path], ...]) -> str:
    digest = hashlib.sha256()
    for relative, path in files:
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def _require_string(payload: dict[str, Any], key: str, pattern: re.Pattern[str]) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise LandingError(f"source.json has invalid {key}: {value!r}")
    return value


def _validate_source(
    source: dict[str, Any], gate: dict[str, Any], domain: str, version: str
) -> str:
    if source.get("status") != "complete":
        raise LandingError("source.json status is not complete")
    if gate.get("release_verified") is not True:
        raise LandingError("gate_report.json release_verified is not true")
    if source.get("domain") != domain or source.get("version") != version:
        raise LandingError(
            "candidate arguments do not match source.json domain/version"
        )
    cut_id = _require_string(source, "cut_id", CUT_PATTERN)
    for key in ("asb_commit", "tooling_commit", "corpus_commit"):
        _require_string(source, key, COMMIT_PATTERN)
    digest = source.get("output_tree_sha256")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise LandingError("source.json has invalid output_tree_sha256")
    return cut_id


def _validate_receipt_inventory(
    source: dict[str, Any], files: tuple[tuple[Path, Path], ...]
) -> None:
    declared = source.get("receipts")
    observed = sorted(relative.as_posix() for relative, _ in files)
    if declared != observed:
        raise LandingError("receipts tree does not match source.json receipts")


def _validate_descriptor(
    descriptor: dict[str, Any], domain: str, version: str, title: str, cut_id: str
) -> None:
    expected_version = int(VERSION_PATTERN.fullmatch(version).group(1))
    expected = {
        "slug": domain,
        "version": expected_version,
        "title": title,
        "cut_id": cut_id,
        "status": "candidate",
    }
    mismatches = [
        key for key, value in expected.items() if descriptor.get(key) != value
    ]
    if mismatches:
        raise LandingError(f"collection.yaml mismatch: {', '.join(mismatches)}")
    for key in ("skills_count", "tools_count"):
        value = descriptor.get(key)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise LandingError(f"collection.yaml has invalid {key}: {value!r}")


def _resolve_directory(path: Path, label: str) -> Path:
    if path.is_symlink():
        raise LandingError(f"{label} cannot be a symlink: {path}")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        raise LandingError(f"{label} is unavailable: {path}: {exc}") from exc


def _validate_candidate(options: argparse.Namespace) -> CandidateInput:
    candidate = _resolve_directory(options.candidate, "candidate")
    receipts = _resolve_directory(options.receipts, "receipts")
    if (
        candidate == receipts
        or candidate in receipts.parents
        or receipts in candidate.parents
    ):
        raise LandingError("candidate and receipts must be separate trees")
    candidate_files = _regular_files(candidate, "candidate")
    receipt_files = _regular_files(receipts, "receipts")
    source = _read_json(receipts / "source.json", "source.json")
    gate = _read_json(receipts / "gate_report.json", "gate_report.json")
    cut_id = _validate_source(source, gate, options.domain, options.version)
    _validate_receipt_inventory(source, receipt_files)
    descriptor = _read_yaml(candidate / "collection.yaml", "collection.yaml")
    _validate_descriptor(
        descriptor, options.domain, options.version, options.title, cut_id
    )
    if _tree_digest(candidate_files) != source["output_tree_sha256"]:
        raise LandingError(
            "candidate tree does not match source.json output_tree_sha256"
        )
    return CandidateInput(
        candidate, receipts, candidate_files, receipt_files, source, descriptor
    )


def _git(repo: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )


def _git_output(repo: Path, *arguments: str) -> str:
    result = _git(repo, *arguments)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise LandingError(f"git {' '.join(arguments)} failed: {detail}")
    return result.stdout.strip()


def _local_identity(repo: Path) -> tuple[str, str] | None:
    values = []
    for key in ("user.name", "user.email"):
        result = _git(repo, "config", "--local", "--get", key)
        if result.returncode not in (0, 1):
            raise LandingError(
                f"cannot read repository identity: {result.stderr.strip()}"
            )
        values.append(result.stdout.strip() if result.returncode == 0 else "")
    return (values[0], values[1]) if all(values) else None


def _fallback_identity(
    options: argparse.Namespace, repo: Path
) -> tuple[str, str] | None:
    if _local_identity(repo) is not None:
        return None
    name = (options.author_name or "").strip()
    email = (options.author_email or "").strip()
    if not name or not email:
        raise LandingError("no git identity; provide --author-name and --author-email")
    if "\n" in name or "\n" in email:
        raise LandingError("author identity cannot contain a newline")
    return name, email


def _ensure_absent_path(repo: Path, relative: str) -> None:
    path = repo / relative
    if path.exists() or path.is_symlink():
        raise LandingError(f"landing target already exists: {relative}")
    for parent in path.parents:
        if parent == repo:
            break
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            raise LandingError(
                f"landing target has unsafe parent: {parent.relative_to(repo)}"
            )


def _validate_marketplace(
    repo: Path, relative: str, domain: str, collection_path: str
) -> dict[str, Any] | None:
    path = repo / relative
    if not path.exists() and not path.is_symlink():
        _ensure_absent_path(repo, relative)
        return None
    if not path.is_file() or path.is_symlink():
        raise LandingError(f"{relative} must be a tracked regular file")
    if _git(repo, "ls-files", "--error-unmatch", "--", relative).returncode:
        raise LandingError(f"{relative} must be a tracked regular file")

    marketplace = _read_json(path, relative)
    if marketplace.get("schema_version") != "1.0":
        raise LandingError(f"{relative} has invalid schema_version")
    if marketplace.get("name") != f"asb-skills-{domain}":
        raise LandingError(f"{relative} has invalid name")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list):
        raise LandingError(f"{relative} has invalid plugins")

    source = f"./{collection_path}"
    if any(
        isinstance(plugin, dict) and plugin.get("source") == source
        for plugin in plugins
    ):
        raise ConflictError(f"marketplace already lists {source}")
    return marketplace


def _paths_overlap(first: Path, second: Path) -> bool:
    return first == second or first in second.parents or second in first.parents


def _validate_repository(
    options: argparse.Namespace, inputs: CandidateInput, paths: tuple[str, str, str]
) -> RepositoryInput:
    repo = _resolve_directory(options.repo, "repository")
    if _paths_overlap(repo, inputs.candidate) or _paths_overlap(repo, inputs.receipts):
        raise LandingError("repository and input trees cannot overlap")
    if _git(repo, "rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        raise LandingError("repository is not a git worktree")
    if Path(_git_output(repo, "rev-parse", "--show-toplevel")).resolve() != repo:
        raise LandingError("--repo must name the git worktree root")
    if _git_output(repo, "branch", "--show-current") != "main":
        raise LandingError("repository must be checked out on main")
    if _git_output(repo, "status", "--porcelain", "--untracked-files=all"):
        raise LandingError("repository worktree is dirty")
    collection_path, receipts_path, marketplace_path = paths
    marketplace = _validate_marketplace(
        repo, marketplace_path, options.domain, collection_path
    )
    for relative in (collection_path, receipts_path):
        _ensure_absent_path(repo, relative)
    zenodo = repo / ".zenodo.json"
    if not zenodo.is_file() or zenodo.is_symlink():
        raise LandingError("repository root .zenodo.json must be a regular file")
    if _git(repo, "ls-files", "--error-unmatch", "--", ".zenodo.json").returncode:
        raise LandingError("repository root .zenodo.json must be tracked")
    return RepositoryInput(repo, _fallback_identity(options, repo), marketplace)


def _validate_options(options: argparse.Namespace) -> None:
    if not DOMAIN_PATTERN.fullmatch(options.domain):
        raise LandingError(f"invalid domain slug: {options.domain!r}")
    if not VERSION_PATTERN.fullmatch(options.version):
        raise LandingError(f"invalid version: {options.version!r}")
    if not options.title.strip() or "\n" in options.title:
        raise LandingError("title must be a non-empty single line")


def _build_plan(options: argparse.Namespace) -> LandingPlan:
    _validate_options(options)
    inputs = _validate_candidate(options)
    cut_id = inputs.source["cut_id"]
    collection_path = f"collections/{options.domain}/{options.version}"
    receipts_path = f"receipts/{cut_id}"
    marketplace_path = ".claude-plugin/marketplace.json"
    branch = f"candidate/{cut_id}"
    message = f"feat(candidate): {options.domain} {options.version} candidate {cut_id}"
    repository = _validate_repository(
        options, inputs, (collection_path, receipts_path, marketplace_path)
    )
    branch_result = _git(
        repository.root, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"
    )
    if branch_result.returncode == 0:
        raise ConflictError(f"branch already exists: {branch}")
    if branch_result.returncode != 1:
        raise LandingError(
            f"cannot inspect branch {branch}: {branch_result.stderr.strip()}"
        )
    return LandingPlan(
        inputs,
        repository,
        branch,
        collection_path,
        receipts_path,
        marketplace_path,
        message,
    )


def _marketplace(plan: LandingPlan) -> dict[str, Any]:
    domain = plan.inputs.source["domain"]
    descriptor = plan.inputs.descriptor
    cut_id = plan.inputs.source["cut_id"]
    title = descriptor["title"]
    description = (
        f"{title}, candidate from cut {cut_id}: {descriptor['skills_count']} "
        f"evidence-grounded skills over {descriptor['tools_count']} tools, each "
        "derived from a peer-reviewed method paper, generated by the "
        f"AgenticScienceBuilder pipeline. Not a release; see receipts/{cut_id}/."
    )
    repository = f"https://github.com/HolobiomicsLab/asb-skills-{domain}"
    return {
        "schema_version": "1.0",
        "name": f"asb-skills-{domain}",
        "description": (
            f"ASB {domain} skill collections: evidence-grounded scientific-agent "
            "skills and tool records from the AgenticScienceBuilder pipeline. "
            "Registry, tooling and governance: "
            "https://github.com/HolobiomicsLab/asb-skill-collections."
        ),
        "owner": dict(OWNER),
        "publisher": dict(OWNER),
        "release": False,
        "plugins": [
            {
                "name": domain,
                "source": f"./{plan.collection_path}",
                "description": description,
                "version": "0.1.0",
                "author": dict(AUTHOR),
                "license": "CC-BY-4.0",
                "keywords": [domain],
                "homepage": repository,
                "repository": repository,
            }
        ],
    }


def _copy_files(files: tuple[tuple[Path, Path], ...], destination: Path) -> None:
    for relative, source in files:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target, follow_symlinks=False)


def _write_marketplace(plan: LandingPlan) -> None:
    path = plan.repository.root / plan.marketplace_path
    path.parent.mkdir(parents=True, exist_ok=True)
    marketplace = _marketplace(plan)
    if plan.repository.marketplace is not None:
        candidate = dict(marketplace["plugins"][0])
        candidate["release"] = False
        marketplace = dict(plan.repository.marketplace)
        marketplace["plugins"] = [*marketplace["plugins"], candidate]
    path.write_text(
        json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _commit_body(plan: LandingPlan) -> str:
    source = plan.inputs.source
    return "\n".join(
        [
            f"asb_commit: {source['asb_commit']}",
            f"tooling_commit: {source['tooling_commit']}",
            f"corpus_commit: {source['corpus_commit']}",
            f"cut_id: {source['cut_id']}",
            f"receipts: {plan.receipts_path}/",
        ]
    )


def _run_git_write(repo: Path, *arguments: str) -> None:
    result = _git(repo, *arguments)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        raise LandingError(f"git {' '.join(arguments)} failed: {detail}")


def _commit(plan: LandingPlan) -> None:
    arguments = []
    if plan.repository.fallback_identity is not None:
        name, email = plan.repository.fallback_identity
        arguments.extend(("-c", f"user.name={name}", "-c", f"user.email={email}"))
    arguments.extend(("commit", "-m", plan.message, "-m", _commit_body(plan)))
    _run_git_write(plan.repository.root, *arguments)


def _rollback(plan: LandingPlan) -> str | None:
    repo = plan.repository.root
    failures = []
    for arguments in (("reset", "--hard", "main"), ("checkout", "main")):
        result = _git(repo, *arguments)
        if result.returncode:
            failures.append((result.stderr or result.stdout).strip())
    for relative in (plan.collection_path, plan.receipts_path, plan.marketplace_path):
        tracked = _git(repo, "ls-files", "--error-unmatch", "--", relative)
        if tracked.returncode == 0:
            continue
        if tracked.returncode != 1:
            failures.append((tracked.stderr or tracked.stdout).strip())
            continue
        path = repo / relative
        try:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            elif path.exists() or path.is_symlink():
                path.unlink()
        except OSError as exc:
            failures.append(f"cannot remove untracked {relative}: {exc}")
    result = _git(repo, "branch", "-D", plan.branch)
    if result.returncode:
        failures.append((result.stderr or result.stdout).strip())
    return "; ".join(filter(None, failures)) or None


def _execute(plan: LandingPlan) -> dict[str, Any]:
    repo = plan.repository.root
    moves_zenodo = all(
        relative.as_posix() != ".zenodo.json"
        for relative, _ in plan.inputs.candidate_files
    )
    checkout = _git(repo, "checkout", "-b", plan.branch, "main")
    if checkout.returncode:
        if (
            _git(
                repo, "show-ref", "--verify", "--quiet", f"refs/heads/{plan.branch}"
            ).returncode
            == 0
        ):
            raise ConflictError(f"branch already exists: {plan.branch}")
        raise LandingError(
            f"cannot create branch {plan.branch}: {checkout.stderr.strip()}"
        )
    try:
        _copy_files(plan.inputs.candidate_files, repo / plan.collection_path)
        _copy_files(plan.inputs.receipt_files, repo / plan.receipts_path)
        _write_marketplace(plan)
        if moves_zenodo:
            _run_git_write(
                repo,
                "mv",
                "--",
                ".zenodo.json",
                f"{plan.collection_path}/.zenodo.json",
            )
        _run_git_write(
            repo,
            "add",
            "--",
            plan.collection_path,
            plan.receipts_path,
            plan.marketplace_path,
        )
        _commit(plan)
        if _git_output(repo, "status", "--porcelain", "--untracked-files=all"):
            raise LandingError("repository is dirty after candidate commit")
        commit = _git_output(repo, "rev-parse", "HEAD")
        file_count = (
            len(plan.inputs.candidate_files)
            + len(plan.inputs.receipt_files)
            + 1
            + moves_zenodo
        )
        return {"branch": plan.branch, "commit": commit, "files": file_count}
    except (LandingError, OSError) as exc:
        rollback_error = _rollback(plan)
        suffix = f"; rollback failed: {rollback_error}" if rollback_error else ""
        raise LandingError(f"landing failed: {exc}{suffix}") from exc


def _dry_run(plan: LandingPlan) -> dict[str, Any]:
    result = {
        "branch": plan.branch,
        "dry_run": True,
        "message": plan.message,
        "paths": {
            "collection": plan.collection_path,
            "marketplace": plan.marketplace_path,
            "receipts": plan.receipts_path,
            "zenodo": f"{plan.collection_path}/.zenodo.json",
        },
    }
    if plan.repository.marketplace is not None:
        result["marketplace"] = {"path": plan.marketplace_path, "mode": "merge"}
    return result


def main(argv: list[str] | None = None) -> int:
    """Validate and land one candidate, returning 0 success, 1 failure, or 2 conflict."""
    options = _parser().parse_args(argv)
    try:
        plan = _build_plan(options)
        result = _dry_run(plan) if options.dry_run else _execute(plan)
    except ConflictError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except (LandingError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
