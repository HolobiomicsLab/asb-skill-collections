#!/usr/bin/env python3
"""Assemble one domain candidate through S4, S3, S5, and S6."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

# Direct script execution places only scripts/ on the import path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from asb_skill_collections import layout


REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
CREATORS = SCRIPTS / "release_creators.yaml"
MODEL = "BAAI/bge-small-en-v1.5"
MODEL_ALIASES = frozenset({"bge-small-en-v1.5", MODEL})
DEFAULT_THRESHOLDS = "0.95,0.90"
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{7,40}$")
DOMAIN_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
VERSION_RE = re.compile(r"^v[1-9][0-9]*$")
STAGE_SCRIPT_NAMES = (
    "join_corpus_records.py",
    "collect_from_cut.py",
    "bootstrap_indexes.py",
    "run_candidate_gates.py",
    "same_paper_pairs.py",
)
EXPECTED_RECEIPTS = frozenset(
    {
        "bootstrap.txt",
        "bootstrap_receipt.json",
        "check_license_tiers.txt",
        "check_provenance_tiers.txt",
        "check_tools_index.txt",
        "checks.json",
        "collect.txt",
        "collect_receipt.json",
        "corpus.yaml",
        "corpus_join_receipt.json",
        "evidence_trim_receipt.json",
        "gate.txt",
        "gate_report.json",
        "gates.txt",
        "join.txt",
        "lint.txt",
        "mapping.json",
        "same_paper.txt",
        "same_paper_pairs.json",
        "source.json",
        "verify.txt",
    }
)


class DriverError(RuntimeError):
    """The driver inputs or a local pipeline operation are invalid."""


class ConflictError(DriverError):
    """Existing state differs from the requested candidate assembly."""


@dataclass(frozen=True)
class Stage:
    """One ordered candidate assembly operation."""

    name: str
    command: tuple[str, ...]
    log_name: str | None


def _json_bytes(value: Any) -> bytes:
    """Render deterministic human-readable JSON."""
    return (
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    ).encode("utf-8")


def _sha256_file(path: Path) -> str:
    """Return a required regular file's hexadecimal SHA-256 digest."""
    if not path.is_file() or path.is_symlink():
        raise DriverError(f"required regular file is missing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _disk_tree(root: Path) -> dict[str, bytes]:
    """Read every regular candidate file by its POSIX relative path."""
    if not root.exists() and not root.is_symlink():
        return {}
    if root.is_symlink() or not root.is_dir():
        raise ConflictError(f"candidate is not a regular directory: {root}")
    files: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ConflictError(f"candidate contains a symlink: {path}")
        if path.is_file():
            files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


def _tree_digest(root: Path) -> str:
    """Match the collector's sorted path plus content-digest algorithm."""
    digest = hashlib.sha256()
    for relative, content in sorted(_disk_tree(root).items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(content).digest())
    return digest.hexdigest()


def _absolute(path: Path) -> Path:
    """Normalize a caller path without following its final component."""
    return Path(os.path.abspath(path))


def _parse_thresholds(value: str) -> tuple[float, float]:
    """Parse calibrated auto-merge and suggestion thresholds."""
    try:
        fields = value.split(",")
        if len(fields) != 2:
            raise ValueError
        auto_merge, suggest = (float(field) for field in fields)
    except ValueError as exc:
        raise DriverError("thresholds must be two comma-separated numbers") from exc
    if not 1.0 >= auto_merge >= suggest > 0.0:
        raise DriverError("thresholds must satisfy 1 >= auto_merge >= suggest > 0")
    return auto_merge, suggest


def _validate_model(value: str) -> str:
    """Require the embedding model calibrated for Decision 7 thresholds."""
    if value not in MODEL_ALIASES:
        raise DriverError("model must be bge-small-en-v1.5 or BAAI/bge-small-en-v1.5")
    return MODEL


def _validate_date(value: str) -> None:
    """Require a canonical caller-supplied verification date."""
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError as exc:
        raise DriverError(f"verified-on must be YYYY-MM-DD: {value!r}") from exc
    if parsed != value:
        raise DriverError(f"verified-on must be canonical: {value!r}")


def _validate_commit(value: str, label: str) -> None:
    """Require one caller-provided short or full hexadecimal revision."""
    if not COMMIT_RE.fullmatch(value):
        raise DriverError(f"{label} must be 7 to 40 hexadecimal characters")


def _is_within(path: Path, parent: Path) -> bool:
    """Return whether path is parent itself or one of its descendants."""
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _validate_options(options: argparse.Namespace) -> None:
    """Validate and normalize every non-receipt driver input."""
    options.view_label = str(options.cut)
    for name in ("asb_commit", "tooling_commit", "corpus_commit"):
        _validate_commit(getattr(options, name), name.replace("_", "-"))
    if not DOMAIN_RE.fullmatch(options.domain):
        raise DriverError(f"invalid domain slug: {options.domain!r}")
    if not VERSION_RE.fullmatch(options.version):
        raise DriverError("version must be v<N> with N greater than zero")
    _validate_date(options.verified_on)
    options.model_id = _validate_model(options.model)
    options.auto_merge, options.suggest = _parse_thresholds(options.thresholds)
    for name in ("cut", "builds", "tiered", "out", "receipts"):
        setattr(options, name, _absolute(getattr(options, name)))
    if options.view_source is not None:
        options.view_source = _absolute(options.view_source)
    if not options.cut.is_dir() or not options.builds.is_dir():
        raise DriverError("cut and builds must be existing directories")
    _sha256_file(options.tiered)
    _sha256_file(CREATORS)
    if options.view_source is not None:
        _sha256_file(options.view_source)
    if _is_within(options.out, options.cut) or _is_within(
        options.receipts, options.cut
    ):
        raise DriverError("output and receipts must not be inside the cut")
    if _is_within(options.receipts, options.out):
        raise DriverError("receipts must not be inside the candidate")


def _threshold_argument(options: argparse.Namespace) -> str:
    """Render validated threshold floats for the S6 subprocess."""
    return f"{options.auto_merge:g},{options.suggest:g}"


def _stage_commands(options: argparse.Namespace) -> list[Stage]:
    """Build the five script calls and intervening corpus copy operation."""
    corpus_staging = options.receipts / "corpus.yaml"
    candidate_corpus = options.out / "corpus.yaml"
    plugin_repo = f"https://github.com/HolobiomicsLab/asb-skills-{options.domain}"

    def script(name: str) -> tuple[str, str]:
        return sys.executable, str(SCRIPTS / name)

    return [
        Stage(
            "join",
            (
                *script("join_corpus_records.py"),
                "--builds",
                str(options.builds),
                "--tiered",
                str(options.tiered),
                "--domain",
                options.domain,
                "--version",
                options.version,
                "--out",
                str(corpus_staging),
                "--verified-on",
                options.verified_on,
                "--receipts",
                str(options.receipts),
            ),
            "join.txt",
        ),
        Stage(
            "collect",
            (
                *script("collect_from_cut.py"),
                "--cut",
                str(options.cut),
                "--builds",
                str(options.builds),
                "--domain",
                options.domain,
                "--version",
                options.version,
                "--out",
                str(options.out),
                "--license",
                "CC-BY-4.0",
                "--plugin-repo",
                plugin_repo,
                "--creators",
                str(CREATORS),
                "--corpus",
                str(corpus_staging),
                "--receipts",
                str(options.receipts),
            ),
            "collect.txt",
        ),
        Stage(
            "copy_corpus",
            ("copy", str(corpus_staging), str(candidate_corpus)),
            None,
        ),
        Stage(
            "bootstrap",
            (
                *script("bootstrap_indexes.py"),
                str(options.out),
                "--corpus",
                str(candidate_corpus),
                "--receipts",
                str(options.receipts),
            ),
            "bootstrap.txt",
        ),
        Stage(
            "gates",
            (
                *script("run_candidate_gates.py"),
                str(options.out),
                "--corpus",
                str(candidate_corpus),
                "--receipts",
                str(options.receipts),
            ),
            "gates.txt",
        ),
        Stage(
            "same_paper",
            (
                *script("same_paper_pairs.py"),
                "--view",
                str(options.cut),
                "--out",
                str(options.receipts / "same_paper_pairs.json"),
                "--model",
                options.model,
                "--thresholds",
                _threshold_argument(options),
            ),
            "same_paper.txt",
        ),
    ]


def _offline_environment() -> dict[str, str]:
    """Return the fixed credential-free stage environment."""
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


def _execute(command: tuple[str, ...]) -> tuple[int, str]:
    """Run one stage subprocess and capture combined output."""
    try:
        result = subprocess.run(
            list(command),
            cwd=REPO,
            env=_offline_environment(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        return 1, f"ERROR: could not execute stage: {exc}\n"
    return result.returncode, result.stdout


def _copy_corpus(source: Path, destination: Path) -> tuple[int, str]:
    """Copy the joined corpus into the candidate with conflict semantics."""
    try:
        content = source.read_bytes()
        if destination.exists() or destination.is_symlink():
            if destination.is_file() and not destination.is_symlink():
                if destination.read_bytes() == content:
                    return 0, "corpus already identical\n"
            return 2, f"CONFLICT: candidate corpus differs: {destination}\n"
        destination.write_bytes(content)
        return 0, f"copied corpus to {destination}\n"
    except OSError as exc:
        return 1, f"ERROR: could not copy corpus: {exc}\n"


def _read_existing_source(path: Path) -> dict[str, Any] | None:
    """Read an existing source receipt or classify malformed state as conflict."""
    if not path.exists() and not path.is_symlink():
        return None
    if path.is_symlink() or not path.is_file():
        raise ConflictError(f"source receipt is not a regular file: {path}")
    try:
        source = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConflictError(f"invalid existing source receipt: {path}") from exc
    if not isinstance(source, dict):
        raise ConflictError(f"existing source receipt is not an object: {path}")
    return source


def _existing_run_status(
    source: dict[str, Any] | None, cut_id: str, output: Path
) -> str | None:
    """Return identical or reject every non-resumable existing run state."""
    if source is None:
        return None
    if source.get("cut_id") != cut_id:
        raise ConflictError(
            f"source cut_id {source.get('cut_id')!r} differs from {cut_id!r}"
        )
    if source.get("status") != "complete":
        raise ConflictError(f"source status is not complete: {source.get('status')!r}")
    actual = _tree_digest(output)
    if source.get("output_tree_sha256") != actual:
        raise ConflictError(
            "source output_tree_sha256 differs from the current candidate"
        )
    return "identical"


def _validate_fresh_destination(output: Path, receipts: Path) -> None:
    """Require absent or empty regular roots before the first stage."""
    for path, label in ((output, "candidate"), (receipts, "receipts")):
        if not path.exists() and not path.is_symlink():
            continue
        if path.is_symlink() or not path.is_dir():
            raise ConflictError(f"{label} is not a regular directory: {path}")
        if any(path.iterdir()):
            raise ConflictError(f"fresh {label} directory is not empty: {path}")


def _script_hashes() -> dict[str, str]:
    """Digest the five stage scripts invoked by the driver."""
    return {name: _sha256_file(SCRIPTS / name) for name in STAGE_SCRIPT_NAMES}


def _source_base(options: argparse.Namespace, cut_id: str) -> dict[str, Any]:
    """Build the caller pins and deterministic stage provenance."""
    return {
        "asb_commit": options.asb_commit,
        "tooling_commit": options.tooling_commit,
        "corpus_commit": options.corpus_commit,
        "view": options.view_label,
        "view_source_sha256": (
            _sha256_file(options.view_source)
            if options.view_source is not None
            else None
        ),
        "cut_id": cut_id,
        "domain": options.domain,
        "version": options.version,
        "model": options.model_id,
        "thresholds": {
            "auto_merge": options.auto_merge,
            "suggest": options.suggest,
            "embed_view": "name_tools",
        },
        "stage_script_sha256": _script_hashes(),
    }


def _write_source(path: Path, payload: dict[str, Any]) -> None:
    """Create source.json without replacing existing ownership evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(_json_bytes(payload))
    except FileExistsError as exc:
        raise ConflictError(f"source receipt appeared during run: {path}") from exc


def _record_failure(
    options: argparse.Namespace,
    cut_id: str,
    stage: str,
    exit_code: int,
) -> None:
    """Write a deterministic terminal receipt for the first failed stage."""
    payload = {
        "status": "failed",
        **_source_base(options, cut_id),
        "failed_stage": stage,
        "exit_code": exit_code,
    }
    _write_source(options.receipts / "source.json", payload)


def _prepare_collect_output(output: Path) -> tuple[int, str]:
    """Remove a caller-provided empty directory before the collector."""
    if not output.exists() and not output.is_symlink():
        return 0, ""
    try:
        if output.is_symlink() or not output.is_dir() or any(output.iterdir()):
            return 2, f"CONFLICT: candidate is no longer empty: {output}\n"
        output.rmdir()
    except OSError as exc:
        return 1, f"ERROR: could not prepare candidate: {exc}\n"
    return 0, ""


def _run_stage(stage: Stage, options: argparse.Namespace) -> int:
    """Execute one script/copy stage and retain its required driver log."""
    prefix = ""
    if stage.name == "collect":
        code, prefix = _prepare_collect_output(options.out)
        if code:
            options.receipts.mkdir(parents=True, exist_ok=True)
            (options.receipts / "collect.txt").write_text(prefix, encoding="utf-8")
            return code
    if stage.name == "copy_corpus":
        code, output = _copy_corpus(
            options.receipts / "corpus.yaml", options.out / "corpus.yaml"
        )
    else:
        code, output = _execute(stage.command)
    if stage.log_name is not None:
        options.receipts.mkdir(parents=True, exist_ok=True)
        (options.receipts / stage.log_name).write_text(
            prefix + output, encoding="utf-8"
        )
    return code


def _copy_mapping(output: Path, receipts: Path) -> None:
    """Copy the collector mapping into the receipt root without replacement."""
    source = output / "mapping.json"
    content = source.read_bytes()
    destination = receipts / "mapping.json"
    if destination.exists() or destination.is_symlink():
        if destination.is_file() and not destination.is_symlink():
            if destination.read_bytes() == content:
                return
        raise ConflictError(f"existing mapping receipt differs: {destination}")
    destination.write_bytes(content)


def _complete_source(options: argparse.Namespace, cut_id: str) -> dict[str, Any]:
    """Build source.json after every output and receipt is complete."""
    return {
        "status": "complete",
        **_source_base(options, cut_id),
        "output_tree_sha256": _tree_digest(options.out),
        "receipts": sorted(EXPECTED_RECEIPTS),
    }


def _finalize(options: argparse.Namespace, cut_id: str) -> None:
    """Copy mapping, enforce the receipt set, and write complete source.json."""
    _copy_mapping(options.out, options.receipts)
    current = {path.name for path in options.receipts.iterdir()}
    expected_before_source = EXPECTED_RECEIPTS - {"source.json"}
    if current != expected_before_source:
        missing = sorted(expected_before_source - current)
        extra = sorted(current - expected_before_source)
        raise ConflictError(f"receipt set differs; missing={missing}, extra={extra}")
    _write_source(options.receipts / "source.json", _complete_source(options, cut_id))


def _dry_run_payload(stages: list[Stage], cut_id: str) -> dict[str, Any]:
    """Render all real stage arguments without executing or writing them."""
    return {
        "status": "dry-run",
        "dry_run": True,
        "cut_id": cut_id,
        "commands": [
            {"stage": stage.name, "command": list(stage.command)} for stage in stages
        ],
    }


def _run(options: argparse.Namespace) -> int:
    """Preflight and execute one complete candidate assembly."""
    _validate_options(options)
    coverage = options.cut / layout.ADVERTISED_DIRNAME / "coverage_summary.json"
    cut_id = _sha256_file(coverage)[:12]
    source_path = options.receipts / "source.json"
    existing = _read_existing_source(source_path)
    status = _existing_run_status(existing, cut_id, options.out)
    if status == "identical":
        print(json.dumps({"cut_id": cut_id, "status": status}, sort_keys=True))
        return 0
    _validate_fresh_destination(options.out, options.receipts)
    stages = _stage_commands(options)
    if options.dry_run:
        print(json.dumps(_dry_run_payload(stages, cut_id), sort_keys=True))
        return 0
    for stage in stages:
        code = _run_stage(stage, options)
        if code:
            _record_failure(options, cut_id, stage.name, code)
            print(
                json.dumps(
                    {"cut_id": cut_id, "status": "failed", "stage": stage.name},
                    sort_keys=True,
                )
            )
            return 2 if code == 2 else 1
    try:
        _finalize(options, cut_id)
    except ConflictError:
        _record_failure(options, cut_id, "finalize", 2)
        raise
    except (DriverError, OSError) as exc:
        _record_failure(options, cut_id, "finalize", 1)
        raise DriverError(str(exc)) from exc
    print(
        json.dumps(
            {"cut_id": cut_id, "receipts": str(options.receipts), "status": "complete"},
            sort_keys=True,
        )
    )
    return 0


def _parser() -> argparse.ArgumentParser:
    """Build the public one-command candidate assembly parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cut", required=True, type=Path)
    parser.add_argument("--builds", required=True, type=Path)
    parser.add_argument("--tiered", required=True, type=Path)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--receipts", required=True, type=Path)
    parser.add_argument("--asb-commit", required=True)
    parser.add_argument("--tooling-commit", required=True)
    parser.add_argument("--corpus-commit", required=True)
    parser.add_argument("--verified-on", required=True)
    parser.add_argument("--view-source", type=Path)
    parser.add_argument("--model", default="bge-small-en-v1.5")
    parser.add_argument("--thresholds", default=DEFAULT_THRESHOLDS)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the driver with exit 0 success, 1 failure, and 2 conflict."""
    try:
        return _run(_parser().parse_args(argv))
    except ConflictError as exc:
        print(f"CONFLICT: {exc}", file=sys.stderr)
        return 2
    except (
        DriverError,
        OSError,
        UnicodeError,
        ValueError,
        TypeError,
        json.JSONDecodeError,
        shutil.Error,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
