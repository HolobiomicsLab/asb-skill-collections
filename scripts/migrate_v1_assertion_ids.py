#!/usr/bin/env python3
"""Apply the approved paper scopes to the shipped v1 validation assertions.

Run with ASB a91f6688's src directory on PYTHONPATH and an ASB-capable Python:
    python scripts/migrate_v1_assertion_ids.py --confirmed-doi COLLECTION/RECORD=DOI

Repeat --confirmed-doi for the four identities recorded in CHANGELOG.md. This
prints the JSON plan; add --apply to write it. The caller confirmed those papers
against Crossref (title, journal, year), 2026-09-14. They are explicit migration
inputs, not paper-specific rules in general code.

The production DOI validator and scope helper are required, never vendored.
Identity comes from the exact same-collection workflow/build provenance join,
with four caller-confirmed exceptions. Claim-level asserted_by is not identity.
All records are preflighted before writing; an already migrated tree is a no-op.
Receipts must subsequently be regenerated with scripts/release_gate.py.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

import yaml

# The migration is runnable by path, just like the other repository scripts.
if __package__ in (None, ""):
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from asb_skill_collections import layout

ROOT = Path(__file__).resolve().parent.parent
COLLECTIONS = ("epigenomics", "metabolomics", "transcriptomics")
PREFIX = "asbval:assertion/"
WORKFLOW_SUFFIX = "#workflow-characterisation"


def _read_bytes(path: Path, root: Path) -> bytes:
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
        raise ValueError(f"Not a regular input inside the checkout: {path}")
    return path.read_bytes()


def _assertions(document: dict) -> list[dict]:
    return [
        node for node in document.get("@graph", [])
        if str(node.get("@type", "")).startswith("asbval:")
        or str(node.get("@id", "")).startswith(PREFIX)
    ]


def _blank_ids(document: dict) -> dict:
    result = deepcopy(document)
    for node in _assertions(result):
        node["@id"] = ""
    return result


def plan_migration(
    root: Path, confirmed_dois: dict[tuple[str, str], str] | None = None,
) -> tuple[list[tuple[Path, bytes, bytes]], dict]:
    """Resolve every identity and check the complete proposed write set."""
    # Lazy imports keep --help usable without an ASB installation. PYTHONPATH
    # selects the production revision; no local approximation is permitted.
    from agentic_science_builder.declared_source_identity import _validate_declared_doi
    from agentic_science_builder.validation_assertions import _assertion_scope

    root = root.resolve()
    confirmed_dois = confirmed_dois or {}
    unused_confirmations = set(confirmed_dois)
    build_sources = defaultdict(list)
    for collection in COLLECTIONS:
        unit = root / "collections" / collection / "v1"
        for path in layout.iter_skill_md(unit):
            text = _read_bytes(path, root).decode("utf-8")
            match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", text, re.S)
            if match is None:
                raise ValueError(f"Missing frontmatter: {path}")
            frontmatter = yaml.safe_load(match.group(1))
            for source in (frontmatter.get("provenance") or {}).get("sources") or []:
                if not isinstance(source, dict) or not source.get("build") or not source.get("doi"):
                    continue
                doi, status, reason = _validate_declared_doi(source["doi"])
                if status != "known":
                    raise ValueError(f"Invalid source DOI in {path}: {reason}")
                build_sources[(collection, source["build"])].append({
                    "skill": path.relative_to(root).as_posix(),
                    "build": source["build"],
                    "raw_doi": source["doi"],
                    "doi": doi,
                })

    writes = []
    rows = []
    summary = {}
    doi_records = {}
    assertion_ids = set()
    metadata_records = []
    for collection in COLLECTIONS:
        paths = sorted((root / "collections" / collection / "v1" / "indicium").glob("*.jsonld"))
        if not paths:
            raise ValueError(f"No v1 indicium records for {collection}")
        counts = Counter(records=len(paths))
        for path in paths:
            relative = path.relative_to(root).as_posix()
            raw = _read_bytes(path, root)
            document = json.loads(raw)
            nodes = _assertions(document)
            builds = {
                node["@id"][:-len(WORKFLOW_SUFFIX)]
                for node in document.get("@graph", [])
                if node.get("@type") == "asbext:WorkflowCharacterisation"
                and str(node.get("@id", "")).endswith(WORKFLOW_SUFFIX)
            }
            sources = [source for build in sorted(builds)
                       for source in build_sources[(collection, build)]]
            candidates = {source["doi"] for source in sources}
            record_key = (collection, path.stem)
            if record_key in confirmed_dois:
                confirmed = confirmed_dois[record_key]
                unused_confirmations.remove(record_key)
                doi, status, reason = _validate_declared_doi(confirmed)
                if status != "known":
                    raise ValueError(f"Invalid confirmed DOI for {relative}: {reason}")
                if candidates and candidates != {doi}:
                    raise ValueError(f"Joined and confirmed DOI conflict for {relative}")
                candidates.add(doi)
            if len(candidates) != 1:
                raise ValueError(f"Need one valid source DOI for {relative}: {sorted(candidates)}")
            doi = next(iter(candidates))
            if doi in doi_records:
                raise ValueError(f"Repeated DOI {doi}: {doi_records[doi]} and {relative}")
            doi_records[doi] = relative
            if not nodes:
                counts["records_without_assertions"] += 1
                continue

            # All shipped records use indent=2, ASCII escaping, insertion order,
            # and no final newline. Accept a final newline without changing it.
            ending = b"\n" if raw.endswith(b"\n") else b""
            if json.dumps(document, indent=2).encode("utf-8") + ending != raw:
                raise ValueError(f"Unsupported serialization; refusing to reformat {relative}")
            scope = _assertion_scope(path.parent, source_doi=doi)
            if not scope or not scope.startswith("paper/"):
                raise ValueError(f"Production helper did not return a paper scope: {relative}")
            before = deepcopy(document)
            rewritten = 0
            for node in nodes:
                old_id = node.get("@id", "")
                if not isinstance(old_id, str) or not old_id.startswith(PREFIX):
                    raise ValueError(f"Unexpected validation assertion ID in {relative}: {old_id!r}")
                suffix = old_id[len(PREFIX):]
                if suffix.startswith(scope + "/"):
                    suffix = suffix[len(scope) + 1:]
                elif suffix.startswith(("paper/", "input-sha256/")):
                    raise ValueError(f"Conflicting existing assertion scope in {relative}: {old_id}")
                if not suffix.startswith(("card/", "skill/", "claim/")):
                    raise ValueError(f"Unexpected local assertion suffix in {relative}: {suffix}")
                node["@id"] = f"{PREFIX}{scope}/{suffix}"
                if node["@id"] in assertion_ids:
                    raise ValueError(f"Duplicate assertion ID in {relative}: {node['@id']}")
                assertion_ids.add(node["@id"])
                rewritten += node["@id"] != old_id
            if _blank_ids(before) != _blank_ids(document):
                raise ValueError(f"Non-ID assertion change in {relative}")
            if "asbval:build_metadata" in document:
                metadata = document["asbval:build_metadata"]
                if not isinstance(metadata, dict):
                    raise ValueError(f"Malformed build metadata in {relative}")
                metadata["assertion_id_scope"] = scope
                metadata_records.append(relative)
            after = json.dumps(document, indent=2).encode("utf-8") + ending
            if after != raw:
                writes.append((path, raw, after))
            counts["assertion_records"] += 1
            counts["assertions"] += len(nodes)
            counts["rewritten_ids"] += rewritten
            counts["changed_records"] += after != raw
            rows.append({
                "record": relative,
                "doi": doi,
                "doi_source": "workflow_build_join" if sources else "caller_confirmed",
                "source_evidence": sources,
                "assertion_count": len(nodes),
                "rewritten_ids": rewritten,
                "before_sha256": hashlib.sha256(raw).hexdigest(),
                "after_sha256": hashlib.sha256(after).hexdigest(),
            })
        summary[collection] = dict(counts)
    if unused_confirmations:
        raise ValueError(f"Confirmed DOI inputs name unknown records: {sorted(unused_confirmations)}")
    return writes, {
        "collections": summary,
        "distinct_assertion_ids": len(assertion_ids),
        "resolved_record_dois": len(doi_records),
        "build_metadata_records": metadata_records,
        "confirmed_doi_inputs": {f"{domain}/{record}": doi
                                 for (domain, record), doi in sorted(confirmed_dois.items())},
        "records": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Collections checkout (default: this repo)")
    parser.add_argument("--apply", action="store_true", help="Write the preflighted migration; default is dry-run")
    parser.add_argument("--confirmed-doi", action="append", default=[], metavar="COLLECTION/RECORD=DOI",
                        help="Caller-confirmed identity for a record without a source join; repeat as needed")
    args = parser.parse_args()
    confirmations = {}
    for value in args.confirmed_doi:
        record, separator, doi = value.partition("=")
        collection, slash, stem = record.partition("/")
        if (not separator or not doi or not slash or collection not in COLLECTIONS
                or not re.fullmatch(r"[A-Za-z0-9_-]+", stem)):
            parser.error(f"Invalid --confirmed-doi input: {value!r}; use COLLECTION/RECORD=DOI")
        key = (collection, stem)
        if key in confirmations:
            parser.error(f"Repeated --confirmed-doi record: {record}")
        confirmations[key] = doi
    writes, report = plan_migration(args.root, confirmations)
    if args.apply:
        # Recheck the entire write set before the first write to catch edits
        # made while identity resolution was running.
        for path, before, _ in writes:
            if _read_bytes(path, args.root.resolve()) != before:
                raise ValueError(f"Record changed during preflight: {path}")
        for path, _, after in writes:
            path.write_bytes(after)
    report["applied"] = args.apply
    report["changed_records"] = len(writes)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
