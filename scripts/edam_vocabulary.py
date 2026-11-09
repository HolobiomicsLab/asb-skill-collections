#!/usr/bin/env python3
"""Build and query an offline, pinned EDAM vocabulary."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


EDAM_IRI = "http://edamontology.org/"
BRANCHES = ("topic", "operation", "data", "format")
REPLACED_BY = "http://www.geneontology.org/formats/oboInOwl#replacedBy"
IRI_PATTERN = re.compile(r"http://edamontology\.org/(topic|operation|data|format)_([0-9]+)$")


@dataclass(frozen=True)
class Resolution:
    """The resolution of one IRI against a pinned EDAM snapshot."""

    status: str
    id: str | None = None
    label: str | None = None
    replaced_by: str | None = None
    branches: tuple[str, ...] = ()


def infer_release(rows: list[dict[str, str]]) -> str:
    """Infer the release from the maximum numeric Created in value."""
    versions = [row["Created in"] for row in rows if row["Created in"][:1].isdigit()]
    if not versions:
        raise ValueError("cannot infer EDAM release from the Created in column")
    return max(versions, key=lambda value: tuple(map(int, value.split("."))))


def term_from_row(row: dict[str, str]) -> dict:
    """Convert one BioPortal CSV row to a compact vocabulary entry."""
    term_id = row["Class ID"].rstrip("/").rsplit("/", 1)[-1]
    if "_" not in term_id:
        return {"id": term_id}
    branch, number = term_id.split("_", 1)
    if branch not in BRANCHES or not number.isdigit():
        raise ValueError(f"unsupported EDAM class identifier: {term_id}")
    replacement = row.get(REPLACED_BY, "").strip().rstrip("/").rsplit("/", 1)[-1]
    return {
        "id": term_id,
        "branch": branch,
        "label": row["Preferred Label"],
        "obsolete": row["Obsolete"].strip().upper() == "TRUE",
        "replaced_by": replacement or None,
    }


def refresh(source: Path, output: Path, generated_at: str) -> dict:
    """Generate a deterministic vocabulary from a local BioPortal CSV."""
    source = Path(source)
    with source.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    terms = {
        entry["id"]: entry for entry in map(term_from_row, rows)
        if entry["id"].startswith(tuple(branch + "_" for branch in BRANCHES))
    }
    table = {
        "schema": "asb-edam-vocabulary/1",
        "release": infer_release(rows),
        "release_inferred": True,
        "release_inference": "maximum numeric Created in value",
        "source_file": source.name,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "generated_at": generated_at,
        "license": "CC-BY-SA-4.0",
        "terms": dict(sorted(terms.items())),
    }
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(table, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return table


def load(path: Path) -> dict:
    """Load and validate the top-level shape of a vocabulary table."""
    table = json.loads(Path(path).read_text(encoding="utf-8"))
    if not table.get("release") or not isinstance(table.get("terms"), dict):
        raise ValueError(f"invalid EDAM vocabulary: {path}")
    return table


def live_replacement(term: dict, vocabulary: dict) -> str | None:
    """Return a live same-branch replacement identifier, if available."""
    replacement = term.get("replaced_by")
    target = vocabulary["terms"].get(replacement)
    if not target or target["obsolete"] or target["branch"] != term["branch"]:
        return None
    return replacement


def resolve(iri, vocabulary: dict) -> Resolution:
    """Resolve one canonical EDAM IRI into five mutually exclusive statuses."""
    match = IRI_PATTERN.fullmatch(iri) if isinstance(iri, str) else None
    if not match:
        return Resolution("malformed")
    branch, number = match.groups()
    term_id = f"{branch}_{number}"
    term = vocabulary["terms"].get(term_id)
    if term:
        status = "obsolete" if term["obsolete"] else "valid"
        return Resolution(status, term_id, term["label"], live_replacement(term, vocabulary) if term["obsolete"] else None)
    branches = tuple(sorted(
        other for other in BRANCHES if f"{other}_{number}" in vocabulary["terms"]
    ))
    return Resolution("wrong_branch" if branches else "ghost", term_id, branches=branches)


def main(argv: list[str] | None = None) -> int:
    """Run the offline refresh command."""
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    refresh_parser = subcommands.add_parser("refresh")
    refresh_parser.add_argument("--csv", type=Path, required=True)
    refresh_parser.add_argument("--out", type=Path, required=True)
    refresh_parser.add_argument("--date", required=True, help="generation date, YYYY-MM-DD")
    options = parser.parse_args(argv)
    table = refresh(options.csv, options.out, options.date)
    print(f"wrote {len(table['terms'])} EDAM terms to {options.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
