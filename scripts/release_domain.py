#!/usr/bin/env python3
"""Run one traced, resumable domain release without performing owner actions."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import zenodo_deposit
from scripts.check_collections_manifest import checkout_counts, compute_tree_digest

STATE_SCHEMA = "asb-release-state/1"
STAGES = (
    "gate", "land", "deposit-plan", "deposit-draft", "record-doi", "receipt", "manifest", "tag",
)
DOI_PATTERN = re.compile(r"^10\.5281/zenodo\.\d+$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VERSION_PATTERN = re.compile(r"^v[1-9][0-9]*$")
DOMAIN_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOOLING_ROOT = Path(__file__).resolve().parents[1]


class ReleaseError(RuntimeError):
    """A stage refusal whose reason is safe to print."""


@dataclass(frozen=True)
class CommandResult:
    """Captured outcome of one local command."""

    returncode: int
    stdout: str = ""
    stderr: str = ""


class SubprocessRunner:
    """Run local commands without a shell and capture their output."""

    def __call__(self, command: list[str], cwd: Path) -> CommandResult:
        environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        completed = subprocess.run(
            command, cwd=cwd, env=environment, capture_output=True, text=True, check=False,
        )
        return CommandResult(completed.returncode, completed.stdout, completed.stderr)


@dataclass
class ReleaseContext:
    """Resolved options and injectable side-effect boundaries for one invocation."""

    args: argparse.Namespace
    runner: Callable
    request: Callable | None
    now: Callable[[], str]
    state: dict
    commands: list[dict]

    @property
    def collection(self) -> Path:
        candidate = self.args.candidate
        return candidate.resolve() if candidate else self.args.repo_root / self.release_path

    @property
    def release_path(self) -> str:
        return f"collections/{self.args.domain}/{self.args.version}"

    def command(self, command: list[str], cwd: Path | None = None) -> CommandResult:
        directory = (cwd or self.args.tooling_root).resolve()
        result = self.runner(command, directory)
        self.commands.append({
            "argv": command, "cwd": str(directory), "exit_code": result.returncode,
        })
        if result.stdout:
            print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
        if result.stderr:
            print(result.stderr, end="" if result.stderr.endswith("\n") else "\n", file=sys.stderr)
        return result

    def sibling(self, relative: str, arguments: list[str]) -> CommandResult:
        return self.command([sys.executable, str(self.args.tooling_root / relative), *arguments])

    def git_commit(self) -> str:
        result = self.command(["git", "rev-parse", "HEAD"], self.args.repo_root)
        if result.returncode:
            raise ReleaseError("cannot read the domain repository HEAD")
        return result.stdout.strip()

    def owner(self, action: str) -> None:
        line = f"OWNER: {action}"
        print(line)
        self.state.setdefault("owner_prompts", []).append(line)

    def release_date(self) -> str:
        """Use the stage timestamp unless the caller supplies a release date."""
        return self.args.released or self.now()[:10]


def utc_now() -> str:
    """Return the default UTC timestamp; callers can inject a fixed clock."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(path: Path) -> str:
    """Hash one file's exact bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(root: Path) -> str:
    """Hash regular files by relative path and bytes, excluding dot directories."""
    lines = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink() or any(
                part.startswith(".") and part != ".zenodo.json" for part in path.relative_to(root).parts):
            continue
        relative = path.relative_to(root).as_posix()
        lines.append(f"{sha256(path)}  {relative}\n")
    return "sha256:" + hashlib.sha256("".join(sorted(lines)).encode()).hexdigest()


def load_state(path: Path, args: argparse.Namespace) -> dict:
    """Load a compatible state file or initialise its stable identity."""
    if path.is_file():
        state = json.loads(path.read_text(encoding="utf-8"))
        expected = (STATE_SCHEMA, args.domain, args.version)
        actual = (state.get("schema"), state.get("domain"), state.get("version"))
        if actual != expected:
            raise ReleaseError("state schema, domain or version does not match this invocation")
        return state
    return {
        "schema": STATE_SCHEMA,
        "domain": args.domain,
        "version": args.version,
        "repo_root": str(args.repo_root),
        "tooling_root": str(args.tooling_root),
        "stages": {},
        "owner_prompts": [],
    }


def receipt_log_path(context: ReleaseContext) -> Path:
    """Place the log beside existing receipts, otherwise beside the state file."""
    cut_id = context.state.get("cut_id") or "pending"
    receipts = context.args.repo_root / "receipts" / cut_id
    if receipts.is_dir():
        return receipts / "release_log.md"
    if context.args.receipts and context.args.stage != "land":
        return context.args.receipts / "release_log.md"
    for source in sorted((context.args.repo_root / "receipts").glob("*/source.json")):
        try:
            record = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if record.get("domain") == context.args.domain and record.get("version") == context.args.version:
            return source.parent / "release_log.md"
    return context.args.state.with_name("release_log.md")


def serialise_log(state: dict) -> str:
    """Render the durable stage trace as deterministic Markdown."""
    lines = [f"# Release log: {state['domain']} {state['version']}", "",
             "| Stage | Done at | Repository commit | Digests |", "|---|---|---|---|"]
    for stage in STAGES:
        record = state["stages"].get(stage)
        if not record:
            continue
        digests = json.dumps(record.get("digests", {}), sort_keys=True)
        lines.append(
            f"| {stage} | {record.get('done_at', '')} | {record.get('repo_commit', '')} | `{digests}` |"
        )
    if state.get("owner_prompts"):
        lines.extend(["", "## Owner actions", ""])
        lines.extend(f"- {prompt}" for prompt in state["owner_prompts"])
    return "\n".join(lines) + "\n"


def save_state(context: ReleaseContext) -> None:
    """Persist state before returning from either success or a refusal."""
    context.args.state.parent.mkdir(parents=True, exist_ok=True)
    temporary = context.args.state.with_suffix(context.args.state.suffix + ".tmp")
    temporary.write_text(json.dumps(context.state, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    temporary.replace(context.args.state)
    log_path = receipt_log_path(context)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(serialise_log(context.state), encoding="utf-8")


def normalise(value):
    """Convert Paths and nested command inputs to stable JSON values."""
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {key: normalise(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalise(item) for item in value]
    return value


def stage_inputs(context: ReleaseContext) -> dict:
    """Return the options that define the requested stage's behaviour."""
    relevant = {
        "gate": {"candidate"},
        "land": {"candidate", "title", "plugin_name", "author_name", "author_email"},
        "deposit-plan": {"record_id", "publication_date", "sandbox", "extra_file", "first_release"},
        "deposit-draft": {"record_id", "publication_date", "sandbox", "extra_file", "first_release"},
        "record-doi": {"doi", "released"}, "receipt": {"candidate"},
        "manifest": {"commit", "source_commit", "tag_name", "released", "regen"},
        "tag": {"commit", "tag_name", "verify"},
    }[context.args.stage]
    return normalise({key: value for key, value in vars(context.args).items() if key in relevant})


def is_noop(context: ReleaseContext) -> bool:
    """Recognise an already completed stage with identical inputs."""
    record = context.state["stages"].get(context.args.stage)
    return bool(record and record.get("status") == "done" and record.get("inputs") == stage_inputs(context))


def complete_stage(context: ReleaseContext, outputs: dict, digests: dict | None = None) -> None:
    """Commit one successful stage record to the in-memory trace."""
    context.state["stages"][context.args.stage] = {
        "status": "done",
        "done_at": context.now(),
        "repo_commit": context.git_commit(),
        "inputs": stage_inputs(context),
        "outputs": normalise(outputs),
        "digests": normalise(digests or {}),
        "commands": context.commands,
    }
    save_state(context)
    print(f"{context.args.stage}: done")


def require_previous(context: ReleaseContext, stage: str) -> dict:
    """Read a prerequisite stage record or refuse with its stage name."""
    record = context.state["stages"].get(stage)
    accepted = {"done", "waiting"} if stage == "deposit-draft" else {"done"}
    if not record or record.get("status") not in accepted:
        raise ReleaseError(f"{context.args.stage} requires completed stage {stage}")
    return record


def require_success(result: CommandResult, label: str) -> None:
    """Turn a failed local check into a concise refusal."""
    if result.returncode:
        raise ReleaseError(f"{label} exited {result.returncode}")


def discover_cut_id(context: ReleaseContext) -> str | None:
    """Read a landed cut identity when source.json is available."""
    source_path = context.args.receipts / "source.json" if context.args.receipts else None
    if source_path and source_path.is_file():
        return json.loads(source_path.read_text(encoding="utf-8"))["cut_id"]
    for source in sorted((context.args.repo_root / "receipts").glob("*/source.json")):
        source_record = json.loads(source.read_text(encoding="utf-8"))
        if source_record.get("domain") == context.args.domain and source_record.get("version") == context.args.version:
            return source_record["cut_id"]
    return None


def run_gate(context: ReleaseContext) -> dict:
    """Run the strict gate and surface scan on the selected collection tree."""
    gate = context.sibling("scripts/release_gate.py", [str(context.collection), "--strict", "--quiet"])
    surface = context.sibling("scripts/check_release_surface.py", [str(context.collection)])
    require_success(gate, "strict release gate")
    require_success(surface, "release surface check")
    report_path = context.collection / "gate_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    cut_id = discover_cut_id(context)
    if cut_id:
        context.state["cut_id"] = cut_id
    return ({"release_verified": report["release_verified"], "collection": context.collection},
            {"gate_report": sha256(report_path), "candidate_tree": tree_digest(context.collection)})


def land_arguments(context: ReleaseContext, dry_run: bool) -> list[str]:
    """Translate orchestration options into the existing landing CLI."""
    args = context.args
    if not (args.candidate and args.receipts and args.title):
        raise ReleaseError("land requires --candidate, --receipts and --title")
    arguments = [
        "--candidate", str(args.candidate), "--receipts", str(args.receipts),
        "--repo", str(args.repo_root), "--domain", args.domain, "--version", args.version,
        "--title", args.title,
    ]
    for option, value in (
        ("--plugin-name", args.plugin_name), ("--author-name", args.author_name),
        ("--author-email", args.author_email),
    ):
        if value:
            arguments.extend([option, value])
    return arguments + (["--dry-run"] if dry_run else [])


def run_land(context: ReleaseContext) -> dict:
    """Dry-run candidate landing, then execute only when explicitly requested."""
    dry = context.sibling("scripts/land_candidate.py", land_arguments(context, True))
    require_success(dry, "candidate landing dry run")
    if not context.args.execute:
        context.owner("rerun land with --execute after reviewing the dry run")
        raise WaitingForOwner("landing dry run complete")
    landed = context.sibling("scripts/land_candidate.py", land_arguments(context, False))
    require_success(landed, "candidate landing")
    result = json.loads(landed.stdout.strip().splitlines()[-1])
    context.state["cut_id"] = discover_cut_id(context)
    context.owner(f"create and merge the candidate pull request for branch {result['branch']}")
    return result, {"candidate_tree": compute_tree_digest(context.args.repo_root, context.release_path)}


def deposit_options(context: ReleaseContext, out_dir: Path) -> argparse.Namespace:
    """Build the exact options consumed by zenodo_deposit's preparation seam."""
    args = context.args
    return argparse.Namespace(
        repo_root=args.repo_root, tooling_root=args.tooling_root, domain=args.domain,
        version=args.version, extra_file=args.extra_file, sandbox=args.sandbox,
        record_id=args.record_id, publication_date=args.publication_date, out_dir=out_dir,
        first_release=args.first_release, community=zenodo_deposit.DEFAULT_COMMUNITY,
    )


def prepare_deposit(context: ReleaseContext, out_dir: Path):
    """Prepare and validate the archive and metadata through the existing deposit tool."""
    prepared = zenodo_deposit._prepare(deposit_options(context, out_dir), out_dir)
    _, _, _, _, problems, _, refusals, _, _ = prepared
    if context.args.first_release:
        registry = context.args.tooling_root / "collections.yaml"
        document = yaml.safe_load(registry.read_text(encoding="utf-8")) if registry.is_file() else {}
        domain = (document.get("domains") or {}).get(context.args.domain, {})
        if domain.get("concept_doi"):
            refusals = [*refusals,
                        "domain already has a concept DOI; use the normal new-version deposit path"]
    if problems or refusals:
        raise ReleaseError("deposit preparation refused: " + "; ".join(problems + refusals))
    return prepared


def run_deposit_plan(context: ReleaseContext) -> dict:
    """Record the exact offline archive, extra files and metadata payload."""
    with tempfile.TemporaryDirectory() as scratch:
        prepared = prepare_deposit(context, Path(scratch))
        host, record, payload, dropped, _, archive, _, _, extras = prepared
        print(zenodo_deposit._describe(*prepared))
        outputs = {
            "host": host, "record_id": record or None, "first_release": context.args.first_release,
            "archive": archive.path.name,
            "archive_size": archive.size, "archive_entries": archive.entries,
            "metadata": payload, "dropped_lineage_relations": dropped,
            "extra_files": [{"name": extra.path.name, "sha256": extra.sha256, "size": extra.size}
                            for extra in extras],
        }
        digests = {"archive_sha256": archive.sha256}
        digests.update({f"extra:{extra.path.name}": extra.sha256 for extra in extras})
        return outputs, digests


def version_items(payload) -> list[dict]:
    """Accept both the envelope and bare-list forms of the versions endpoint."""
    if isinstance(payload, list):
        return payload
    hits = payload.get("hits", {}) if isinstance(payload, dict) else {}
    return hits.get("hits", []) if isinstance(hits, dict) else []


def find_pending_draft(context: ReleaseContext, base: str, record: str, token: str) -> dict | None:
    """Find the record's unpublished next-version draft through the deposit API."""
    payload = zenodo_deposit._call("versions list", "GET", f"{base}/{record}/versions", token)
    candidates = []
    for version in version_items(payload):
        state = str(version.get("state") or version.get("status") or "").lower()
        submitted = version.get("submitted") is True or state in {"done", "published"}
        if not submitted and (state in {"unsubmitted", "draft", "in_progress"} or version.get("submitted") is False):
            candidates.append(version)
    if len(candidates) > 1:
        raise ReleaseError("multiple pending next-version drafts found; owner must select one")
    if not candidates:
        return None
    draft_url = candidates[0].get("links", {}).get("self") or f"{base}/{candidates[0]['id']}"
    return zenodo_deposit._call("pending draft fetch", "GET", draft_url, token)


def find_pending_first_release(context: ReleaseContext, prepared, base: str, token: str) -> dict | None:
    """Find one unpublished new-record draft with the release's exact title and version."""
    metadata = prepared[2]["metadata"]
    title, version = metadata.get("title"), metadata.get("version")
    payload = zenodo_deposit._call(
        "drafts list", "GET", f"{base}?{urllib.parse.urlencode({'status': 'draft'})}", token,
    )
    candidates = [draft for draft in version_items(payload)
                  if draft.get("metadata", {}).get("title") == title
                  and draft.get("metadata", {}).get("version") == version]
    if len(candidates) > 1:
        raise ReleaseError("multiple pending first-release drafts match this title and version; owner must select one")
    if not candidates:
        return None
    draft_url = candidates[0].get("links", {}).get("self") or f"{base}/{candidates[0]['id']}"
    return zenodo_deposit._call("pending draft fetch", "GET", draft_url, token)


def upload_draft(context: ReleaseContext, prepared, draft: dict, token: str, base: str) -> None:
    """Replace stale files and apply metadata, inheriting only on the new-version path."""
    _, _, template, _, _, archive, _, _, extras = prepared
    for stale in draft.get("files") or []:
        zenodo_deposit._call("stale file delete", "DELETE", f"{base}/{draft['id']}/files/{stale['id']}", token)
    zenodo_deposit.upload_files(draft, archive, extras, token)
    zenodo_deposit.update_metadata(
        draft, template, token, base, inherited=not context.args.first_release,
    )


def run_deposit_draft(context: ReleaseContext) -> dict:
    """Reuse a pending next-version draft or create the first one; never publish."""
    plan = require_previous(context, "deposit-plan")
    with tempfile.TemporaryDirectory() as scratch:
        prepared = prepare_deposit(context, Path(scratch))
        archive = prepared[5]
        if archive.sha256 != plan["digests"]["archive_sha256"]:
            raise ReleaseError("archive sha256 differs from deposit-plan; rerun deposit-plan --force")
        token = zenodo_deposit._token(context.args.sandbox)
        base = f"{prepared[0]}/api/deposit/depositions"
        record = prepared[1]
        if ((record or None) != plan["outputs"]["record_id"] or prepared[0] != plan["outputs"]["host"]
                or context.args.first_release != plan["outputs"].get("first_release", False)):
            raise ReleaseError("record id, host or first-release mode differs from deposit-plan; rerun deposit-plan --force")
        draft = (find_pending_first_release(context, prepared, base, token)
                 if context.args.first_release else find_pending_draft(context, base, record, token))
        reused = draft is not None
        if draft is None:
            if context.args.first_release:
                draft = zenodo_deposit.create_record(prepared, token)
            else:
                created = zenodo_deposit._call(
                    "newversion", "POST", f"{base}/{record}/actions/newversion", token,
                )
                draft = zenodo_deposit._call("draft fetch", "GET", created["links"]["latest_draft"], token)
        upload_draft(context, prepared, draft, token, base)
    url = draft["links"].get("html") or f"{prepared[0]}/deposit/{draft['id']}"
    print(f"draft {draft['id']} {'reused' if reused else 'created'}, not published: {url}")
    print(f"uploaded {archive.path.name} sha256 {archive.sha256}")
    outputs = {"draft_url": url, "draft_id": str(draft["id"]), "reused": reused}
    if context.args.first_release:
        context.owner(
            f"publish the reviewed Zenodo draft at {url}; publishing mints both the version DOI and the concept DOI"
        )
        context.owner("run record-doi --doi <version DOI>, then manifest --concept-doi <concept DOI>")
        outputs.update(conceptrecid=str(draft["conceptrecid"]), first_release=True)
    else:
        context.owner(f"publish the reviewed Zenodo draft at {url}, then run record-doi --doi <version DOI>")
    raise WaitingForOwner("draft ready", outputs, {"archive_sha256": archive.sha256})


def update_collection_citation(path: Path, doi: str, released: str, version: str) -> None:
    """Insert or replace the version DOI while preserving unrelated CFF bytes."""
    text = path.read_text(encoding="utf-8")
    text, count = re.subn(r"(?m)^doi:.*$", f"doi: {doi}", text)
    if not count:
        match = re.search(r"(?m)^version:.*$", text)
        if not match:
            raise ReleaseError(f"collection CITATION.cff lacks a version field: {path}")
        text = text[:match.end()] + f"\ndoi: {doi}" + text[match.end():]
    text, count = re.subn(r"(?m)^date-released:.*$", f"date-released: '{released}'", text)
    if not count:
        text = re.sub(r"(?m)^(doi:.*)$", f"\\1\ndate-released: '{released}'", text, count=1)
    document = yaml.safe_load(text)
    identifiers = [item for item in document.get("identifiers", [])
                   if not (item.get("type") == "doi" and str(item.get("description", "")).startswith(
                       f"Zenodo version DOI of {version} "))]
    identifiers.insert(0, {
        "type": "doi", "value": doi,
        "description": f"Zenodo version DOI of {version} ({released})",
    })
    document["identifiers"] = identifiers
    document["doi"] = doi
    document["date-released"] = released
    path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")


def update_root_citation(path: Path, doi: str, released: str, version: str) -> None:
    """Upsert this version's DOI in the root CFF identifier list."""
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    description = f"Zenodo version DOI of {version} ({released})"
    identifiers = document.setdefault("identifiers", [])
    for item in identifiers:
        if item.get("value") == doi or str(item.get("description", "")).startswith(
                f"Zenodo version DOI of {version} "):
            item.update(type="doi", value=doi, description=description)
            break
    else:
        identifiers.append({"type": "doi", "value": doi, "description": description})
    path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")


def update_readme(path: Path, doi: str, released: str, release_path: str) -> None:
    """Update the release-table row selected by its collection path."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    for index, line in enumerate(lines):
        if not line.lstrip().startswith("|") or f"`{release_path}`" not in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            raise ReleaseError(f"README release row has fewer than six cells: {path}")
        cells[-2] = released
        cells[-1] = f"[{doi}](https://doi.org/{doi})"
        ending = "\n" if line.endswith("\n") else ""
        lines[index] = "| " + " | ".join(cells) + " |" + ending
        path.write_text("".join(lines), encoding="utf-8")
        return
    raise ReleaseError(f"README has no release-table row for {release_path}")


def update_usage(path: Path, doi: str, version: str) -> None:
    """Replace the collection citation paragraph, leaving source-paper citation intact."""
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(?ms)^1\. \*\*The collection\*\*.*?(?=^2\. \*\*Every source paper|\Z)"
    )
    replacement = (
        f"1. **The collection**, using {version}'s `CITATION.cff` and the version DOI of its\n"
        f"   Zenodo record, `{doi}`.\n"
    )
    updated, count = pattern.subn(replacement, text, count=1)
    if not count:
        raise ReleaseError(f"USAGE.md lacks the numbered collection citation paragraph: {path}")
    path.write_text(updated, encoding="utf-8")


def emit_hub_manifest(context: ReleaseContext) -> Path | None:
    """Call the hub-owned emitter as a subprocess when a hub and receipts exist."""
    if not context.args.hub_root:
        return None
    receipts = context.args.receipts
    if receipts is None:
        cut_id = context.state.get("cut_id")
        if not cut_id:
            raise ReleaseError("--hub-root requires --receipts or a cut id in the state")
        receipts = context.args.repo_root / "receipts" / cut_id
    emitter = context.args.hub_root / "docs/asbb/release-manifest/gen_release_manifest.py"
    if not emitter.is_file():
        raise ReleaseError(f"hub release emitter is missing: {emitter}")
    output = context.args.hub_root / "releases" / context.args.domain / "RELEASE.yaml"
    arguments = [
        "--domain", context.args.domain, "--receipts", str(receipts), "--version", context.args.version,
        "--allow-placeholders", "--out", str(output),
    ]
    for role in ("asb", "tooling", "corpus", "data"):
        value = getattr(context.args, f"{role}_commit")
        if value:
            arguments.extend(["--sha", f"{role}={value}"])
    if context.args.receipts_commit:
        arguments.extend(["--receipts-commit", context.args.receipts_commit])
    result = context.command([sys.executable, str(emitter), *arguments], context.args.hub_root)
    require_success(result, "hub release manifest emitter")
    return output


def run_record_doi(context: ReleaseContext) -> dict:
    """Record a minted DOI on all four domain surfaces and refresh the hub trace."""
    args = context.args
    args.released = context.release_date()
    if not DOI_PATTERN.fullmatch(args.doi):
        raise ReleaseError("--doi must be a Zenodo DOI with a numeric record id")
    collection = context.collection
    before = {path: path.read_bytes() for path in citation_paths(context)}
    update_collection_citation(collection / "CITATION.cff", args.doi, args.released, args.version)
    update_root_citation(args.repo_root / "CITATION.cff", args.doi, args.released, args.version)
    update_readme(args.repo_root / "README.md", args.doi, args.released, context.release_path)
    update_usage(collection / "USAGE.md", args.doi, args.version)
    context.state["doi"] = args.doi
    context.state["released"] = args.released
    concept = read_concept_doi(context, args.doi)
    hub_manifest = emit_hub_manifest(context)
    merge_commit = args.commit or None
    if merge_commit and not COMMIT_PATTERN.fullmatch(merge_commit):
        raise ReleaseError("--commit must name the full merged DOI pull request commit")
    changed = [path for path, content in before.items() if path.read_bytes() != content]
    paths = citation_paths(context) + ([hub_manifest] if hub_manifest else [])
    outputs = {"changed_files": changed, "hub_manifest": hub_manifest, "merge_commit": merge_commit}
    if concept:
        outputs.update(concept_doi=concept["conceptdoi"], conceptrecid=concept["conceptrecid"])
        print(
            f"concept DOI {concept['conceptdoi']} (record {concept['conceptrecid']}); "
            f"next: manifest --concept-doi {concept['conceptdoi']}"
        )
    return outputs, {
        path.name: sha256(path) for path in paths if path
    }


def read_concept_doi(context: ReleaseContext, doi: str) -> dict | None:
    """Read the published record's concept DOI after a first-release draft."""
    draft = context.state["stages"].get("deposit-draft", {})
    if not draft.get("outputs", {}).get("first_release"):
        return None
    record_id = doi.rsplit(".", 1)[-1]
    host = zenodo_deposit.SANDBOX_URL if context.args.sandbox else zenodo_deposit.ZENODO_URL
    try:
        status, payload = zenodo_deposit._request("GET", f"{host}/api/records/{record_id}", "")
    except zenodo_deposit.ZenodoError:
        status, payload = None, None
    concept_doi = (payload or {}).get("conceptdoi")
    conceptrecid = (payload or {}).get("conceptrecid")
    if not (status and 200 <= status < 300 and concept_doi and conceptrecid
            and DOI_PATTERN.fullmatch(str(concept_doi))):
        context.owner(
            "read the concept DOI from the published record, then run "
            "manifest --concept-doi <concept DOI>"
        )
        return None
    return {"conceptdoi": str(concept_doi), "conceptrecid": str(conceptrecid)}


def citation_paths(context: ReleaseContext) -> list[Path]:
    """List the four byte-stable DOI recording surfaces."""
    return [
        context.collection / "CITATION.cff", context.args.repo_root / "CITATION.cff",
        context.args.repo_root / "README.md", context.collection / "USAGE.md",
    ]


def run_receipt(context: ReleaseContext) -> dict:
    """Regenerate and independently verify the strict receipt, then scan the surface."""
    collection = context.collection
    gate = context.sibling("scripts/release_gate.py", [str(collection), "--strict", "--quiet"])
    require_success(gate, "strict receipt regeneration")
    verify = context.sibling("scripts/release_gate.py", [str(collection), "--verify", "--quiet"])
    surface = context.sibling("scripts/check_release_surface.py", [str(collection)])
    require_success(verify, "release receipt verification")
    require_success(surface, "release surface check")
    report = collection / "gate_report.json"
    return {"verified": True}, {"receipt": sha256(report)}


def default_tag(domain: str, version: str) -> str:
    """Use the domain tag convention v<N>.0.0."""
    return f"{domain}-{version}.0.0"


def manifest_row(context: ReleaseContext) -> dict:
    """Compute one complete published release row from state and checkout bytes."""
    args = context.args
    doi = context.state.get("doi")
    if not doi:
        raise ReleaseError("manifest requires the DOI recorded by record-doi")
    commit = args.commit or context.git_commit()
    if not COMMIT_PATTERN.fullmatch(commit):
        raise ReleaseError("manifest commit must be a full 40-character hexadecimal commit")
    source_commit = args.source_commit
    if source_commit == "":
        source_commit = None
    previous = context.state["stages"].get("record-doi", {})
    if previous.get("inputs", {}).get("doi") != context.state.get("doi"):
        raise ReleaseError("manifest requires record-doi for the current DOI")
    if not args.commit:
        raise ReleaseError("manifest requires --commit, the merged DOI pull request commit")
    if source_commit and not COMMIT_PATTERN.fullmatch(source_commit):
        raise ReleaseError("source_commit must be null or a full 40-character hexadecimal commit")
    released = context.state.get("released") or context.release_date()
    return {
        "version": int(args.version[1:]), "path": context.release_path,
        "tag": args.tag_name or default_tag(args.domain, args.version), "commit": commit,
        "source_commit": source_commit,
        "tree_digest": compute_tree_digest(args.repo_root, context.release_path),
        "version_doi": doi, "released": released,
        **checkout_counts(context.collection),
    }


def update_manifest(context: ReleaseContext, row: dict) -> Path:
    """Insert or replace the domain release without discarding other domains."""
    path = context.args.tooling_root / "collections.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}
    if document.get("schema") != "asb-collections-manifest/1":
        raise ReleaseError(f"collections.yaml has the wrong schema: {path}")
    domains = document.setdefault("domains", {})
    domain = domains.setdefault(context.args.domain, {
        "repository": f"HolobiomicsLab/asb-skills-{context.args.domain}", "releases": [],
    })
    if domain.get("concept_doi") is None:
        concept_doi = context.args.concept_doi or context.state["stages"].get(
            "record-doi", {}).get("outputs", {}).get("concept_doi", "")
        if not concept_doi:
            raise ReleaseError("first release requires --concept-doi with a numeric Zenodo record id")
        if not DOI_PATTERN.fullmatch(concept_doi):
            raise ReleaseError("invalid concept DOI")
        domain["concept_doi"] = concept_doi
    releases = domain.setdefault("releases", [])
    for index, existing in enumerate(releases):
        if int(existing["version"]) == row["version"]:
            releases[index] = row
            break
    else:
        releases.append(row)
    releases.sort(key=lambda release: int(release["version"]), reverse=True)
    path.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def run_manifest(context: ReleaseContext) -> dict:
    """Write the registry row, validate it, and optionally rebuild public indexes."""
    row = manifest_row(context)
    path = update_manifest(context, row)
    catalogue = context.sibling("scripts/regen_catalogue.py", [
        "--repo-root", str(context.args.tooling_root),
        "--checkout", f"{context.args.domain}={context.args.repo_root}",
    ])
    require_success(catalogue, "catalogue regeneration")
    regenerated = []
    if context.args.regen:
        search = context.sibling("docs-site/build_search_index.py", [
            "--manifest", str(path), "--checkout", f"{context.args.domain}={context.args.repo_root}",
        ])
        require_success(search, "search index regeneration")
        regenerated = [context.args.tooling_root / "docs-site/search_index.json"]
    catalogue_path = context.args.tooling_root / "catalogue.jsonld"
    check = context.sibling("scripts/check_collections_manifest.py", [
        "--manifest", str(path), "--catalogue", str(catalogue_path),
        "--checkout", f"{context.args.domain}={context.args.repo_root}",
    ])
    require_success(check, "collections manifest check")
    outputs = {"manifest": path, "release": row, "catalogue": catalogue_path,
               "regenerated": regenerated}
    digests = {"collections_yaml": sha256(path), "catalogue_jsonld": sha256(catalogue_path)}
    digests.update({item.name: sha256(item) for item in regenerated})
    return outputs, digests


def run_tag(context: ReleaseContext) -> dict:
    """Print owner-only tag commands and optionally verify the remote tag."""
    require_previous(context, "record-doi")
    commit = context.args.commit or context.state["stages"].get("record-doi", {}).get(
        "outputs", {}).get("merge_commit")
    if not commit or not COMMIT_PATTERN.fullmatch(commit):
        raise ReleaseError("tag requires --commit or a full merge commit recorded by manifest")
    tag_name = context.args.tag_name or default_tag(context.args.domain, context.args.version)
    context.owner(f"git tag {shlex.quote(tag_name)} {commit}")
    context.owner(f"git push origin {shlex.quote(tag_name)}")
    verified = None
    if context.args.verify:
        result = context.command(
            ["git", "ls-remote", "--tags", "origin", f"refs/tags/{tag_name}"], context.args.repo_root,
        )
        require_success(result, "remote tag verification")
        lines = [line.split() for line in result.stdout.splitlines() if line.strip()]
        verified = any(fields[0] == commit and fields[1] == f"refs/tags/{tag_name}" for fields in lines)
        if not verified:
            raise ReleaseError(f"remote tag {tag_name} does not point at {commit}")
    if not context.args.verify:
        raise WaitingForOwner("tag commands printed", {"tag": tag_name, "commit": commit})
    return {"tag": tag_name, "commit": commit, "remote_verified": verified}, {}


def print_status(context: ReleaseContext) -> None:
    """Print the state schema and one compact table row per recorded stage."""
    print(f"schema: {context.state['schema']}")
    print(f"release: {context.args.domain} {context.args.version}")
    print("stage | done at | inputs | outputs | digests")
    print("--- | --- | --- | --- | ---")
    for stage in STAGES:
        record = context.state["stages"].get(stage)
        if not record:
            continue
        values = [json.dumps(record.get(key, {}), sort_keys=True) for key in ("inputs", "outputs", "digests")]
        print(f"{stage} | {record.get('done_at', 'waiting')} | {values[0]} | {values[1]} | {values[2]}")
    next_stage = next(
        (stage for stage in STAGES if context.state["stages"].get(stage, {}).get("status") != "done"),
        "complete",
    )
    print(f"next: {next_stage}")


class WaitingForOwner(RuntimeError):
    """A prepared owner decision, recorded with exit status two."""

    def __init__(self, reason: str, outputs: dict | None = None, digests: dict | None = None) -> None:
        super().__init__(reason)
        self.outputs = outputs or {}
        self.digests = digests or {}


def execute_stage(context: ReleaseContext) -> int:
    """Dispatch one stage and translate success, waiting and refusal exit codes."""
    handlers = {
        "gate": run_gate, "land": run_land, "deposit-plan": run_deposit_plan,
        "deposit-draft": run_deposit_draft, "record-doi": run_record_doi,
        "receipt": run_receipt, "manifest": run_manifest, "tag": run_tag,
    }
    if is_noop(context) and not context.args.force:
        print(f"{context.args.stage}: unchanged; no-op")
        return 0
    prerequisites = {"land": "gate", "receipt": "record-doi", "manifest": "receipt"}
    if context.args.stage in prerequisites:
        require_previous(context, prerequisites[context.args.stage])
    if context.args.stage == "record-doi":
        require_previous(context, "deposit-draft")
    try:
        outputs, digests = handlers[context.args.stage](context)
    except WaitingForOwner as waiting:
        context.state["stages"][context.args.stage] = {
            "status": "waiting", "done_at": context.now(), "repo_commit": context.git_commit(),
            "inputs": stage_inputs(context), "outputs": normalise(waiting.outputs),
            "digests": normalise(waiting.digests), "commands": context.commands,
        }
        save_state(context)
        print(f"waiting: {waiting}")
        return 2
    complete_stage(context, outputs, digests)
    return 2 if context.args.stage == "land" else 0


def resume_stages(context: ReleaseContext) -> int:
    """Continue through prepared stages, stopping at the first owner dependency."""
    for stage in STAGES:
        context.args.stage = stage
        record = context.state["stages"].get(stage)
        if record and record.get("status") == "done" and not context.args.force:
            print(f"{stage}: already done")
            continue
        if stage in {"record-doi", "tag"}:
            context.owner(f"complete prerequisites for {stage}, then invoke that stage explicitly")
            save_state(context)
            return 2
        if stage == "land" and not (context.args.candidate and context.args.receipts and context.args.title):
            print("land: no candidate inputs; skipping an already landed release")
            continue
        code = execute_stage(context)
        if code:
            return code
    return 0


def parser() -> argparse.ArgumentParser:
    """Build the staged release command-line interface."""
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="stage", required=True)
    for stage in (*STAGES, "status"):
        command = commands.add_parser(stage)
        command.add_argument("--domain", required=True)
        command.add_argument("--version", required=True)
        command.add_argument("--repo-root", type=Path, required=True)
        command.add_argument("--hub-root", type=Path)
        command.add_argument("--tooling-root", type=Path, default=TOOLING_ROOT)
        command.add_argument("--state", type=Path, required=True)
        command.add_argument("--force", action="store_true")
        command.add_argument("--resume", action="store_true")
        command.add_argument("--candidate", type=Path)
        command.add_argument("--receipts", type=Path)
        command.add_argument("--extra-file", action="append", default=[])
        command.add_argument("--record-id", default=None)
        command.add_argument("--first-release", action="store_true",
                             help="create a new record and domain lineage, without newversion")
        command.add_argument("--publication-date", default=None)
        command.add_argument("--sandbox", action="store_true")
        command.add_argument("--doi", default="")
        command.add_argument("--released", default="")
        command.add_argument("--concept-doi", default="")
        command.add_argument("--commit", default="")
        command.add_argument("--source-commit", default="")
        for role in ("asb", "tooling", "corpus", "data"):
            command.add_argument(f"--{role}-commit", default="")
        command.add_argument("--receipts-commit", default="")
        command.add_argument("--tag-name", default="")
        command.add_argument("--regen", action="store_true")
        command.add_argument("--verify", action="store_true")
        command.add_argument("--execute", action="store_true")
        command.add_argument("--title", default="")
        command.add_argument("--plugin-name", default="")
        command.add_argument("--author-name", default="")
        command.add_argument("--author-email", default="")
    return root


def validated_args(argv: list[str]) -> argparse.Namespace:
    """Resolve paths and reject malformed release identities before side effects."""
    args = parser().parse_args(argv)
    if not DOMAIN_PATTERN.fullmatch(args.domain) or not VERSION_PATTERN.fullmatch(args.version):
        raise ReleaseError("domain or version is invalid")
    for name in ("repo_root", "tooling_root", "state"):
        setattr(args, name, getattr(args, name).expanduser().resolve())
    for name in ("hub_root", "candidate", "receipts"):
        value = getattr(args, name)
        if value is not None:
            setattr(args, name, value.expanduser().resolve())
    args.extra_file = [str(Path(value).expanduser().resolve()) for value in args.extra_file]
    if args.released and not DATE_PATTERN.fullmatch(args.released):
        raise ReleaseError("--released must be YYYY-MM-DD")
    return args


def main(argv: list[str] | None = None, *, now=None, request=None, runner=None) -> int:
    """Run one release stage with injectable time, HTTP and local command seams."""
    original_request = zenodo_deposit._request
    try:
        args = validated_args(argv)
        state = load_state(args.state, args)
        context = ReleaseContext(args, runner or SubprocessRunner(), request, now or utc_now, state, [])
        args.released = context.release_date()
        args.publication_date = args.publication_date or args.released
        if request is not None:
            zenodo_deposit._request = request
        if args.stage == "status":
            print_status(context)
            return 0
        if args.resume:
            return resume_stages(context)
        return execute_stage(context)
    except (ReleaseError, zenodo_deposit.ZenodoError, OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"refused: {error}", file=sys.stderr)
        if "context" in locals() and args.stage != "status":
            context.state["last_failure"] = {
                "stage": args.stage, "at": context.now(), "reason": str(error), "commands": context.commands,
            }
            save_state(context)
        return 1
    finally:
        zenodo_deposit._request = original_request


if __name__ == "__main__":
    raise SystemExit(main())
