#!/usr/bin/env python3
"""Generate deterministic EDAM slug-list facets from a collection index."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

GENERATOR_VERSION = "1.0.0"
EDAM_IRI_PREFIX = "http://edamontology.org/"
DEFAULT_LABELS = Path(__file__).resolve().parent / "data" / "edam_labels.json"
KINDS = {"topics": "topic", "operations": "operation"}


class FacetError(ValueError):
    """A collection, label table or output directory cannot be processed."""


class SourceDigestMismatch(FacetError):
    """An existing receipt belongs to another collection index."""


def identifier(value: str) -> str:
    """Return the bare EDAM identifier from an IRI or an identifier."""
    return value.rsplit("/", 1)[-1] if value else ""


def split_csv_values(value: str) -> list[str]:
    """Split EDAM's pipe-delimited multivalue cells without blank entries."""
    return [item.strip() for item in value.split("|") if item.strip()]


def infer_edam_version(rows: list[dict[str, str]]) -> str:
    """Infer the release from the newest term when the CSV has no release row."""
    versions = [row["Created in"] for row in rows if row["Created in"][:1].isdigit()]
    if not versions:
        raise FacetError("cannot infer the EDAM version from the Created in column")
    return max(
        versions, key=lambda value: tuple(int(part) for part in value.split("."))
    )


def derive_labels(source: Path, output: Path, generated: str) -> dict:
    """Write a compact topic and operation table from an EDAM release CSV."""
    with source.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    terms = {}
    for row in rows:
        term_id = identifier(row["Class ID"])
        if not term_id.startswith(("topic_", "operation_")):
            continue
        terms[term_id] = {
            "id": term_id,
            "label": row["Preferred Label"],
            "synonyms": split_csv_values(row["Synonyms"]),
            "parents": [
                identifier(parent) for parent in split_csv_values(row["Parents"])
            ],
        }
    table = {
        "edam_version": infer_edam_version(rows),
        "source_file": source.name,
        "generated": generated,
        "license": "CC-BY-SA-4.0",
        "terms": dict(sorted(terms.items())),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    write_json(output, table)
    return table


def load_labels(path: Path) -> dict:
    """Load the versioned EDAM label table and retain its provenance."""
    table = json.loads(path.read_text(encoding="utf-8"))
    if not table.get("edam_version") or not isinstance(table.get("terms"), dict):
        raise FacetError(f"invalid EDAM label table: {path}")
    return table


def load_collection(path: Path) -> tuple[list[dict], dict, str]:
    """Read index rows, collection identity and the exact source digest."""
    index_path = path / "skills_index.json"
    source = index_path.read_bytes()
    rows = json.loads(source)
    if not isinstance(rows, list):
        raise FacetError(f"expected a JSON list in {index_path}")
    metadata = {"path": str(path.resolve()), "version": None}
    metadata_path = path / "collection.yaml"
    if metadata_path.is_file():
        import yaml

        document = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
        metadata["version"] = document.get("version")
    return rows, metadata, hashlib.sha256(source).hexdigest()


def group_rows(
    rows: list[dict], kind: str
) -> tuple[dict[str, set[str]], dict[str, int]]:
    """Group unique slugs by EDAM term and partition leaves outside facets."""
    prefix = KINDS[kind] + "_"
    groups = defaultdict(set)
    uncovered = Counter()
    for row in rows:
        slug = row["slug"]
        values = row.get("edam_topics" if kind == "topics" else "edam_operation")
        terms = {
            identifier(value)
            for value in ([values] if isinstance(values, str) else values or [])
        }
        terms = {term for term in terms if term.startswith(prefix)}
        if not terms:
            uncovered["no_topic" if kind == "topics" else "no_operation"] += 1
        for term in terms:
            groups[term].add(slug)
    return groups, dict(uncovered)


def build_index(
    rows: list[dict],
    groups: dict[str, set[str]],
    uncovered: dict[str, int],
    *,
    threshold: int,
    kind: str,
    labels: dict,
    collection: dict,
    source_digest: str,
) -> dict:
    """Calculate the selected facets, symmetric overlaps and uncovered leaves."""
    selected = {
        term: slugs for term, slugs in groups.items() if len(slugs) >= threshold
    }
    covered = set().union(*selected.values()) if selected else set()
    outside = len(rows) - len(covered)
    no_term = uncovered.get("no_topic" if kind == "topics" else "no_operation", 0)
    facets = []
    for term in sorted(selected):
        slugs = selected[term]
        overlaps = {
            other: len(slugs & selected[other])
            for other in sorted(selected)
            if other != term and slugs & selected[other]
        }
        term_labels = labels["terms"].get(term, {})
        facets.append(
            {
                "id": term,
                "iri": EDAM_IRI_PREFIX + term,
                "label": term_labels.get("label"),
                "synonyms": term_labels.get("synonyms", []),
                "count": len(slugs),
                "overlaps": overlaps,
            }
        )
    return {
        "generator_version": GENERATOR_VERSION,
        "source_digest": source_digest,
        "collection": collection,
        "kind": kind,
        "threshold": threshold,
        "edam_version": labels["edam_version"],
        "facet_count": len(facets),
        "facets": facets,
        "covered": len(covered),
        "uncovered": {
            "no_topic" if kind == "topics" else "no_operation": no_term,
            "under_threshold": outside - no_term,
            "total": outside,
        },
    }


def check_source_digest(index_path: Path, source_digest: str, force: bool) -> None:
    """Refuse to overwrite a receipt from different source bytes unless forced."""
    if not index_path.is_file() or force:
        return
    previous = json.loads(index_path.read_text(encoding="utf-8")).get("source_digest")
    if previous == source_digest:
        return
    raise SourceDigestMismatch(
        f"{index_path}: source digest changed; expected {previous}, actual {source_digest}; "
        "rerun with --force to replace the facets"
    )


def print_table(result: dict) -> None:
    """Print one compact coverage table for normal and dry-run invocations."""
    print(f"{'id':<20} {'count':>6}  label")
    for facet in result["facets"]:
        print(f"{facet['id']:<20} {facet['count']:>6}  {facet['label'] or ''}")
    print(
        f"facets={result['facet_count']} covered={result['covered']} "
        f"uncovered={result['uncovered']['total']}"
    )


def write_json(path: Path, value: dict) -> None:
    """Write stable UTF-8 JSON with a final newline."""
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_facets(out: Path, result: dict) -> None:
    """Write selected sorted slug lists and their receipt after the digest guard."""
    topics = out / result["kind"]
    topics.mkdir(parents=True, exist_ok=True)
    selected = {facet["id"]: facet for facet in result["facets"]}
    for path in topics.glob("*.txt"):
        if path.stem not in selected:
            path.unlink()
    for facet in result["facets"]:
        path = topics / f"{facet['id']}.txt"
        slugs = facet.pop("_slugs")
        path.write_text(
            "".join(f"{slug}\n" for slug in sorted(slugs)), encoding="utf-8"
        )
    write_json(out / "index.json", result)


def run(
    *,
    collection: Path,
    out: Path,
    threshold: int = 50,
    kind: str = "topics",
    labels: Path = DEFAULT_LABELS,
    force: bool = False,
    dry_run: bool = False,
) -> dict:
    """Build an in-memory facet receipt, optionally writing its lists and index."""
    if kind not in KINDS:
        raise FacetError(f"unknown facet kind {kind!r}; choose topics or operations")
    if threshold < 1:
        raise FacetError("threshold must be at least 1")
    rows, metadata, source_digest = load_collection(collection)
    check_source_digest(out / "index.json", source_digest, force)
    groups, uncovered = group_rows(rows, kind)
    result = build_index(
        rows,
        groups,
        uncovered,
        threshold=threshold,
        kind=kind,
        labels=load_labels(labels),
        collection=metadata,
        source_digest=source_digest,
    )
    print_table(result)
    if not dry_run:
        for facet in result["facets"]:
            facet["_slugs"] = sorted(groups[facet["id"]])
        write_facets(out, result)
    return result


def parser() -> argparse.ArgumentParser:
    """Create the facet generator and offline label-refresh command parser."""
    command = argparse.ArgumentParser(description=__doc__)
    subcommands = command.add_subparsers(dest="subcommand")
    refresh = subcommands.add_parser(
        "refresh-labels", help="derive labels from an EDAM CSV"
    )
    refresh.add_argument("--csv", type=Path, required=True)
    refresh.add_argument("--out", type=Path, default=DEFAULT_LABELS)
    refresh.add_argument("--date", required=True, help="generation date, YYYY-MM-DD")
    build = subcommands.add_parser("build", help="generate facets from a collection")
    build.set_defaults(subcommand="build")
    for options, required in ((build, True), (command, False)):
        options.add_argument("--collection", type=Path, required=required)
        options.add_argument("--out", type=Path, required=required)
        options.add_argument("--threshold", type=int, default=50)
        options.add_argument("--kind", choices=tuple(KINDS), default="topics")
        options.add_argument("--labels", type=Path, default=DEFAULT_LABELS)
        options.add_argument("--force", action="store_true")
        options.add_argument("--dry-run", action="store_true")
    return command


def main(argv: list[str] | None = None) -> int:
    """Run a build or label refresh and return a command-line status code."""
    command = parser()
    args = command.parse_args(argv)
    if args.subcommand is None and (args.collection is None or args.out is None):
        command.error("the following arguments are required: --collection, --out")
    try:
        if args.subcommand == "refresh-labels":
            table = derive_labels(args.csv, args.out, args.date)
            print(f"wrote {len(table['terms'])} EDAM terms to {args.out}")
        else:
            run(
                collection=args.collection,
                out=args.out,
                threshold=args.threshold,
                kind=args.kind,
                labels=args.labels,
                force=args.force,
                dry_run=args.dry_run,
            )
    except (FacetError, OSError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
