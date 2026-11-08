#!/usr/bin/env python3
"""Move corpus tool licences out of the paper-access namespace."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import yaml

# Direct script execution places only scripts/ on the import path.
if __package__ in (None, ""):
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.license_tier import (
    SUBJECT_PAPER,
    SUBJECT_TOOL,
    TOOL_LICENSE_KEYS,
    licence_subject,
)


def _new_tool_license(entry: dict) -> dict:
    """Build the canonical corpus tool-licence block from one legacy entry."""
    access = entry.get("access") if isinstance(entry.get("access"), dict) else {}
    return {
        "spdx": access.get("license"),
        "detection": entry.get("license_detection"),
        "verified_on": access.get("verified_on"),
        "source": entry.get("repo_url"),
    }


def migrate_document(document: dict) -> tuple[dict, dict]:
    """Return a migrated copy and counts, refusing ambiguous licensed entries."""
    migrated = copy.deepcopy(document)
    summary = {"moved": 0, "left": 0, "refused": 0}
    for entry in migrated.get("papers") or []:
        subject = entry.get("license_subject")
        access = entry.get("access") if isinstance(entry.get("access"), dict) else {}
        if subject == SUBJECT_TOOL:
            block = entry.get("tool_license")
            expected = _new_tool_license(entry)
            if block is not None and block != expected:
                summary["refused"] += 1
                continue
            entry["tool_license"] = expected
            access.pop("license", None)
            entry.pop("license_detection", None)
            entry.pop("license_subject", None)
            summary["moved"] += 1
            continue
        if subject == SUBJECT_PAPER:
            entry.pop("license_subject", None)
            summary["left"] += 1
            continue
        if subject is not None:
            summary["refused"] += 1
            continue
        block = entry.get("tool_license")
        if block is not None:
            if not isinstance(block, dict) or set(block) != set(TOOL_LICENSE_KEYS):
                summary["refused"] += 1
            else:
                summary["left"] += 1
            continue
        if access.get("license") is not None and licence_subject(entry) != SUBJECT_PAPER:
            summary["refused"] += 1
        else:
            summary["left"] += 1
    return migrated, summary


def migrate(corpus: Path, output: Path, dry_run: bool = False) -> tuple[dict, bool]:
    """Migrate one corpus, writing only when classification is complete."""
    document = yaml.safe_load(corpus.read_text(encoding="utf-8")) or {}
    migrated, summary = migrate_document(document)
    changed = migrated != document
    summary["changed"] = changed
    if summary["refused"] == 0 and changed and not dry_run:
        output.write_text(
            yaml.safe_dump(migrated, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    return summary, changed


def main(argv: list[str] | None = None) -> int:
    """Run the corpus migration command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    output = args.out or args.corpus
    summary, changed = migrate(args.corpus, output, args.dry_run)
    print(json.dumps(summary, sort_keys=True))
    if summary["refused"]:
        print("Refused ambiguous entries; nothing written.")
        return 2
    if not changed:
        print("No changes needed.")
    elif args.dry_run:
        print("Dry run; nothing written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
