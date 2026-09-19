#!/usr/bin/env python3
"""Run the six candidate checks and retain their combined output receipts."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
CHECK_SPECS = (
    ("gate", "gate.txt", "release_gate.py"),
    ("lint", "lint.txt", "lint_skill_descriptions.py"),
    ("check_license_tiers", "check_license_tiers.txt", "check_license_tiers.py"),
    (
        "check_provenance_tiers",
        "check_provenance_tiers.txt",
        "check_provenance_tiers.py",
    ),
    ("check_tools_index", "check_tools_index.txt", "check_tools_index.py"),
    ("verify", "verify.txt", "release_gate.py"),
)


class GateRunnerError(RuntimeError):
    """The gate-runner inputs or receipt destination are invalid."""


def _json_bytes(value: Any) -> bytes:
    """Render deterministic readable JSON."""
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def _offline_environment() -> dict[str, str]:
    """Preserve the process environment while removing provider credentials."""
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


def _commands(candidate: Path, corpus: Path, receipts: Path) -> list[list[str]]:
    """Return the exact six commands in their release order."""
    gate_report = receipts / "gate_report.json"
    gate = [
        sys.executable,
        str(SCRIPTS / "release_gate.py"),
        str(candidate),
        "--strict",
        "--corpus",
        str(corpus),
        "--report",
        str(gate_report),
    ]
    verify = [
        sys.executable,
        str(SCRIPTS / "release_gate.py"),
        str(candidate),
        "--verify",
        "--corpus",
        str(corpus),
        "--report",
        str(gate_report),
    ]
    standalone = {
        name: [sys.executable, str(SCRIPTS / script), str(candidate)]
        for name, _, script in CHECK_SPECS[1:-1]
    }
    return [gate, *[standalone[name] for name, _, _ in CHECK_SPECS[1:-1]], verify]


def _run_command(command: list[str], log_path: Path) -> int:
    """Run one check and always preserve its combined output."""
    try:
        result = subprocess.run(
            command,
            cwd=REPO,
            env=_offline_environment(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        output, code = result.stdout, result.returncode
    except OSError as exc:
        output, code = f"ERROR: could not execute check: {exc}\n", 1
    log_path.write_text(output, encoding="utf-8")
    return code


def _validate_paths(candidate: Path, corpus: Path, receipts: Path) -> None:
    """Validate all source and destination roots without creating them."""
    if not candidate.is_dir() or candidate.is_symlink():
        raise GateRunnerError(f"candidate directory does not exist: {candidate}")
    if not corpus.is_file():
        raise GateRunnerError(f"corpus file does not exist: {corpus}")
    if receipts.exists() and (not receipts.is_dir() or receipts.is_symlink()):
        raise GateRunnerError(f"receipts path is not a regular directory: {receipts}")


def _parser() -> argparse.ArgumentParser:
    """Build the public S5 gate-runner argument parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--corpus", required=True, type=Path)
    parser.add_argument("--receipts", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def _run(options: argparse.Namespace) -> int:
    """Execute all six checks or print their dry-run plan."""
    candidate = Path(os.path.abspath(options.candidate))
    corpus = Path(os.path.abspath(options.corpus))
    receipts = Path(os.path.abspath(options.receipts))
    _validate_paths(candidate, corpus, receipts)
    commands = _commands(candidate, corpus, receipts)
    if options.dry_run:
        print(
            json.dumps(
                {"stage": "S5", "dry_run": True, "commands": commands},
                sort_keys=True,
            )
        )
        return 0
    receipts.mkdir(parents=True, exist_ok=True)
    statuses: dict[str, int] = {}
    for (name, filename, _), command in zip(CHECK_SPECS, commands, strict=True):
        statuses[name] = _run_command(command, receipts / filename)
    code = 0 if all(status == 0 for status in statuses.values()) else 1
    payload = {"stage": "S5", "exit_code": code, "checks": statuses}
    (receipts / "checks.json").write_bytes(_json_bytes(payload))
    print(json.dumps(payload))
    return code


def main(argv: list[str] | None = None) -> int:
    """Run candidate checks with deterministic receipts and no suppressed failures."""
    try:
        return _run(_parser().parse_args(argv))
    except (GateRunnerError, OSError, UnicodeError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
