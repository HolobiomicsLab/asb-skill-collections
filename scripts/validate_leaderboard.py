"""
Validate a benchmark/leaderboard.jsonld file against the ASB leaderboard schema.

Schema has a result_type discriminator: agent | rag_system | hybrid.

Each entry must include:
  result_type        -- "agent" | "rag_system" | "hybrid"
  submitter_handle   -- GitHub handle (string)
  submitter_orcid    -- ORCID (string, optional)
  agent_or_system_name  -- display name (string)
  image_digest       -- Docker SHA256 or commit SHA (string)
  submitted_at       -- ISO 8601 timestamp (string)
  scores             -- dict mapping challenge_id (str) to numeric score
  metrics            -- dict of any additional metrics (optional, default {})

Usage:
    python scripts/validate_leaderboard.py <leaderboard.jsonld>

Exit codes:
  0 -- valid
  1 -- validation errors found
  2 -- invocation error (file not found, JSON parse error)
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

VALID_RESULT_TYPES = {"agent", "rag_system", "hybrid"}

ENTRY_REQUIRED_FIELDS = [
    "result_type",
    "submitter_handle",
    "agent_or_system_name",
    "image_digest",
    "submitted_at",
    "scores",
]


def _validate_entry(entry: dict, index: int) -> list[str]:
    """Return list of error strings for one leaderboard entry."""
    errors: list[str] = []
    prefix = f"Entry[{index}]"

    # Check result_type discriminator first
    rt = entry.get("result_type")
    if rt not in VALID_RESULT_TYPES:
        errors.append(
            f"{prefix}: result_type={rt!r} is not one of "
            f"{sorted(VALID_RESULT_TYPES)}"
        )

    # Check required fields
    for field in ENTRY_REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"{prefix}: missing required field '{field}'")

    # Validate scores: must be dict with numeric values
    scores = entry.get("scores")
    if scores is not None:
        if not isinstance(scores, dict):
            errors.append(f"{prefix}: 'scores' must be a dict, got {type(scores).__name__}")
        else:
            for challenge_id, score in scores.items():
                if not isinstance(score, (int, float)):
                    errors.append(
                        f"{prefix}: scores[{challenge_id!r}]={score!r} is not numeric"
                    )

    # Validate submitted_at: must look like ISO 8601
    submitted_at = entry.get("submitted_at", "")
    if submitted_at and not re.match(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", submitted_at
    ):
        errors.append(
            f"{prefix}: submitted_at={submitted_at!r} is not a valid ISO 8601 timestamp"
        )

    # submitter_handle must be a non-empty string
    handle = entry.get("submitter_handle", "")
    if handle is not None and not isinstance(handle, str):
        errors.append(f"{prefix}: submitter_handle must be a string")
    elif not handle:
        errors.append(f"{prefix}: submitter_handle must be a non-empty string")

    return errors


def validate_leaderboard(path: pathlib.Path) -> list[str]:
    """
    Validate the leaderboard.jsonld file at path.

    Args:
        path: Path to leaderboard.jsonld.

    Returns:
        List of error strings. Empty list means valid.

    Raises:
        FileNotFoundError: if path does not exist.
        json.JSONDecodeError: if file is not valid JSON.
    """
    data = json.loads(path.read_text())
    errors: list[str] = []

    # Top-level type check
    top_type = data.get("@type", "")
    if "Leaderboard" not in str(top_type):
        errors.append(
            f"Top-level @type={top_type!r} does not contain 'Leaderboard'"
        )

    # entries must be a list
    entries = data.get("entries", [])
    if not isinstance(entries, list):
        errors.append("'entries' must be a list")
        return errors

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"Entry[{i}] is not a dict")
            continue
        errors.extend(_validate_entry(entry, i))

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a leaderboard.jsonld against the ASB leaderboard schema."
    )
    parser.add_argument("leaderboard", help="Path to leaderboard.jsonld")
    args = parser.parse_args()

    path = pathlib.Path(args.leaderboard)

    try:
        errors = validate_leaderboard(path)
    except FileNotFoundError:
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"ERROR: JSON parse error: {exc}", file=sys.stderr)
        sys.exit(2)

    if errors:
        print(f"VALIDATION FAILED: {len(errors)} error(s)")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        entries = json.loads(path.read_text()).get("entries", [])
        print(f"OK: leaderboard is valid ({len(entries)} entries)")
        sys.exit(0)


if __name__ == "__main__":
    main()
