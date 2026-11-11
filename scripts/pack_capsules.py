#!/usr/bin/env python3
"""Pack and screen local ASB build capsules without depositing or uploading."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from collections import Counter
from pathlib import Path

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts import capsule_screen, zenodo_deposit
try:
    from scripts.promote_benchmark_layer import _CAPSULE_KEEP
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from promote_benchmark_layer import _CAPSULE_KEEP
from scripts.release_capsule_truth import crate_problems, slug_from_build
from scripts.release_gate import _build_email_allowlist

BUILD_FILES = ("build_manifest.json", "workflow.yaml", "validation_assertions.jsonld")
CAPSULE_FILES = ("eval.json", "validation.json")
EVAL_KEYS = {"task_id", "inputs", "expected_outputs", "checks"}
PIPELINE_NAME = "AgenticScienceBuilder"
# The pipeline repository is private: linked only with --pipeline-public.
PIPELINE_URL = f"https://github.com/HolobiomicsLab/{PIPELINE_NAME}"
# Citation keys that may point at a private domain repository.
PRIVATE_CITATION_KEYS = ("url", "repository-code")
REGISTRY = Path(__file__).resolve().parent.parent / "collections.yaml"
TOOLING_URL = "https://github.com/HolobiomicsLab/asb-skill-collections"
DOI_PLACEHOLDER = "ZENODO_DOI_RESERVED_AFTER_PUBLICATION"


def write_json(path: Path, value) -> None:
    """Write stable, human-readable JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    """Stream a file SHA-256 digest."""
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def normalize_doi(value) -> str | None:
    """Normalize a DOI for corpus and access-record joins."""
    if not isinstance(value, str):
        return None
    value = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "doi:"):
        value = value.removeprefix(prefix)
    return value or None


def discover_builds(view: Path, limit: int | None) -> list[Path]:
    """Return immediate build directories or paper-view symlinks in sorted order."""
    builds = [entry for entry in sorted(view.iterdir()) if entry.is_dir() and (entry / "build_manifest.json").is_file()]
    return builds[:limit] if limit is not None else builds


def load_access_records(path: Path | None) -> dict[str, dict]:
    """Index same-DOI access overrides without depending on registry paths."""
    if path is None:
        return {}
    records = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(records, dict):
        records = records.get("papers") or records.get("records") or []
    return {normalize_doi(row.get("doi")): row for row in records if normalize_doi(row.get("doi"))}


def resolve_paper(build_name: str, corpus: dict, overrides: dict) -> dict:
    """Join released corpus metadata first, then apply a same-DOI override."""
    papers = {paper.get("name"): paper for paper in corpus.get("papers") or []}
    paper = dict(papers.get(build_name) or {})
    doi = normalize_doi(paper.get("doi"))
    access = dict(paper.get("access") or {})
    source = "released_corpus" if access else "unmatched"
    override = overrides.get(doi)
    if override:
        access = dict(override.get("access") or access)
        source = "access_override"
    return {"doi": doi, "access": access, "access_source": source, "matched": bool(paper)}


def copy_selected(source: Path, destination: Path, relative: str) -> bool:
    """Copy one regular file into the staged build."""
    origin = source / relative
    if not origin.is_file():
        return False
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(origin, target)
    return True


def stage_build(source: Path, destination: Path, with_indicium: bool) -> tuple[list[str], list[Path]]:
    """Copy only G1 slim-plus members and return missing files and capsules."""
    missing = [name for name in BUILD_FILES if not copy_selected(source, destination, name)]
    for directory in ("ledger",):
        if (source / directory).is_dir():
            shutil.copytree(source / directory, destination / directory)
        else:
            missing.append(directory + "/")
    if with_indicium and not copy_selected(source, destination, "indicium.jsonld"):
        missing.append("indicium.jsonld")
    capsules = sorted(path for path in (source / "capsules").iterdir() if path.is_dir())
    for capsule in capsules:
        target = destination / "capsules" / capsule.name
        for name in _CAPSULE_KEEP:
            origin = capsule / name
            if origin.is_dir():
                shutil.copytree(origin, target / name)
            elif not copy_selected(capsule, target, name):
                missing.append(f"capsules/{capsule.name}/{name}")
        for name in CAPSULE_FILES:
            if not copy_selected(capsule, target, name):
                missing.append(f"capsules/{capsule.name}/{name}")
    return missing, capsules


def tooling_commit() -> str:
    """Read the current tooling revision without changing Git state."""
    root = Path(__file__).resolve().parent.parent
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def input_digests(access_records: Path | None, deny_file: Path | None) -> dict:
    """Digest the optional runtime inputs whose content must not be written."""
    digests = {}
    if access_records:
        digests["access_records_sha256"] = digest(access_records)
    if deny_file:
        digests["deny_patterns_file_sha256"] = digest(deny_file)
    return digests


def source_receipt(view_name: str, collection: Path, extra_digests: dict) -> dict:
    """Bind the run to input trees and exact record files, not machine locators."""
    return {
        "view": view_name,
        "collection": collection.name,
        "collection_files": {
            name: digest(collection / name) for name in ("corpus.yaml", "collection.yaml", "CITATION.cff", ".zenodo.json")
            if (collection / name).is_file()
        },
        **extra_digests,
    }


def load_collection(root: Path) -> dict:
    """Read the four released-collection files the packer and the deposit tool use."""
    return {
        "collection": yaml.safe_load((root / "collection.yaml").read_text(encoding="utf-8")),
        "corpus": yaml.safe_load((root / "corpus.yaml").read_text(encoding="utf-8")),
        "citation": yaml.safe_load((root / "CITATION.cff").read_text(encoding="utf-8")),
        "template": json.loads((root / ".zenodo.json").read_text(encoding="utf-8")),
    }


def collection_version_doi(loaded: dict) -> str:
    """Return the collection's current version DOI, read from its citation first."""
    citation, collection = loaded["citation"], loaded["collection"]
    doi = normalize_doi(citation.get("doi") or collection.get("version_doi") or collection.get("doi"))
    if not doi:
        raise ValueError("The collection has no version DOI")
    return doi


def released_names(corpus: dict) -> set[str]:
    """Return the build names of the papers the released corpus includes."""
    return {paper.get("name") for paper in corpus.get("papers") or [] if paper.get("status") == "included"}


def build_slug(source_name: str) -> str:
    """Return the archive slug of a build directory name."""
    return slug_from_build(source_name.split("__")[-1])


def build_input_receipt(source: Path, with_indicium: bool) -> dict:
    """Digest exactly the selected source members before screening."""
    files = [source / name for name in BUILD_FILES + (("indicium.jsonld",) if with_indicium else ())]
    files.extend(path for path in (source / "ledger").rglob("*") if path.is_file())
    for capsule in sorted((source / "capsules").iterdir()):
        if not capsule.is_dir():
            continue
        for name in _CAPSULE_KEEP + list(CAPSULE_FILES):
            member = capsule / name
            if member.is_file():
                files.append(member)
            elif member.is_dir():
                files.extend(path for path in member.rglob("*") if path.is_file())
    return {path.relative_to(source).as_posix(): digest(path) for path in sorted(files)}


def private_repositories(registry: Path = REGISTRY, pipeline_public: bool = False) -> tuple[str, ...]:
    """Return the private repositories: every domain repository of the registry and the pipeline.

    The screen rewrites their URLs and `capsules_deposit.py plan` refuses any
    that remains. With `pipeline_public` the pipeline is left out of the list.
    """
    document = yaml.safe_load(registry.read_text(encoding="utf-8")) or {}
    names = {domain["repository"] for domain in (document.get("domains") or {}).values()
             if isinstance(domain, dict) and domain.get("repository")}
    if not pipeline_public:
        names.add(f"HolobiomicsLab/{PIPELINE_NAME}")
    return tuple(sorted(names))


def screen_build(root: Path, paper: dict, collection_meta: dict, options: dict) -> tuple[dict, dict]:
    """Screen every staged text file and return counts and per-capsule quotes."""
    context = capsule_screen.context_for(paper.get("doi") or "", paper.get("access") or {})
    context.email_allowlist, context.email_role = _build_email_allowlist(collection_meta)
    context.deny_patterns = options["deny_patterns"]
    context.private_repositories = options["private_repositories"]
    budget = capsule_screen.QuoteBudget()
    counts = capsule_screen.empty_counts()
    failures = []
    quotes_by_capsule = {}
    for path in sorted(member for member in root.rglob("*") if member.is_file()):
        relative = path.relative_to(root).as_posix()
        if path.suffix.lower() not in capsule_screen.TEXT_SUFFIXES:
            continue
        capsule_dir = path.parent if path.name == "ro-crate-metadata.json" else None
        if capsule_dir is not None:
            original = json.loads(path.read_text(encoding="utf-8"))
            pruned = capsule_screen.prune_crate_document(original, capsule_dir)
            counts["crates_pruned"] += int(pruned != original)
        result = capsule_screen.screen_text(
            path.read_text(encoding="utf-8"), relative, context, budget, capsule_dir
        )
        path.write_text(result.text, encoding="utf-8")
        counts.update(result.counts)
        failures.extend(result.failures)
        if "capsules" in path.relative_to(root).parts:
            capsule_id = path.relative_to(root).parts[1]
            aggregate = quotes_by_capsule.setdefault(capsule_id, {"count": 0, "characters": 0, "longest": 0, "truncated": 0, "dropped": 0})
            for key, value in result.quotes.items():
                aggregate[key] = max(aggregate[key], value) if key == "longest" else aggregate[key] + value
    for crate in sorted(root.glob("capsules/*/ro-crate-metadata.json")):
        problems = crate_problems(crate.parent)
        failures.extend(f"{crate.relative_to(root).as_posix()}: {problem}" for problem in problems)
    counts["failures"] = len(failures)
    counts["spans_dropped_by_access_class"] = counts["spans_dropped"] if context.drop_quotes else 0
    return {"counts": dict(sorted(counts.items())), "failures": failures, "quote_retention": context.retention}, quotes_by_capsule


def validation_state(path: Path) -> tuple[str, dict]:
    """Apply m30's explicit present, clean, and strict summary rules."""
    try:
        payload = read_json(path)
    except (ValueError, TypeError):
        return "invalid", {}
    summary = payload.get("summary") or {}
    try:
        values = {key: int(summary.get(key, 0) or 0) for key in ("n_claims_checked", "n_supported", "n_partial", "n_unsupported", "n_drift")}
    except (TypeError, ValueError):
        return "invalid", {}
    state = "present"
    if values["n_claims_checked"] > 0 and values["n_unsupported"] == 0 and values["n_drift"] == 0:
        state = "clean"
    if values["n_claims_checked"] > 0 and values["n_supported"] == values["n_claims_checked"] and not any(values[key] for key in ("n_partial", "n_unsupported", "n_drift")):
        state = "strict"
    return state, values


def eval_state(path: Path) -> tuple[str, dict]:
    """Apply m30's complete operational definition rule."""
    try:
        payload = read_json(path)
    except (ValueError, TypeError):
        return "invalid", {"task_id": None, "checks": 0}
    complete = EVAL_KEYS.issubset(payload) and isinstance(payload.get("checks"), list) and bool(payload["checks"]) and not payload.get("validation_errors")
    return ("complete" if complete else "partial"), {"task_id": payload.get("task_id"), "checks": len(payload.get("checks") or [])}


def read_json(path: Path) -> dict:
    """Read a required staged JSON object, failing loudly on invalid input."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} is not a JSON object")
    return value


def zip_build(root: Path, target: Path) -> dict:
    """Write a sorted deterministic archive with canonical timestamps and modes."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w") as archive:
        for source in sorted(path for path in root.rglob("*") if path.is_file()):
            name = source.relative_to(root).as_posix()
            archive.writestr(zenodo_deposit._zip_info(name, source), source.read_bytes(), compresslevel=9)
    return {"member": target.name, "bytes": target.stat().st_size, "sha256": digest(target)}


def pack_one(source: Path, stage_parent: Path, out: Path, paper: dict, collection_meta: dict, options: dict) -> tuple[dict, list[dict], dict]:
    """Stage, screen, and archive one build, returning its receipt rows."""
    started = time.monotonic()
    slug = build_slug(source.name)
    stage_root = stage_parent / slug
    stage_root.mkdir()
    missing, capsules = stage_build(source, stage_root, options["with_indicium"])
    screen, quotes = screen_build(stage_root, paper, collection_meta, options)
    screen["failures"].extend(f"missing:{name}" for name in missing)
    screen["counts"]["failures"] = len(screen["failures"])
    rows = capsule_rows(stage_root, slug, paper, capsules, quotes)
    for row in rows:
        if "invalid" in {row["validation_state"], row["eval_state"]}:
            screen["failures"].append(f"capsules/{row['capsule_id']}: invalid_validation_or_eval")
    screen["counts"]["failures"] = len(screen["failures"])
    entry = {
        "build_slug": slug,
        "source_name": source.name,
        "paper_doi": paper.get("doi"),
        "access_class": capsule_screen.access_class_for(paper.get("access") or {}),
        "license": (paper.get("access") or {}).get("license"),
        "access_source": paper.get("access_source"),
        "capsule_ids": [row["capsule_id"] for row in rows],
        "zip_member": f"builds/{slug}.zip",
        "validation_state": aggregate_validation(rows),
        "eval_state": "complete" if rows and all(row["eval_state"] == "complete" for row in rows) else "partial",
        "screen": screen,
        "input_sha256": build_input_receipt(source, options["with_indicium"]),
    }
    if not screen["failures"]:
        entry.update(zip_build(stage_root, out / "builds" / f"{slug}.zip"))
    else:
        entry.update({"bytes": 0, "sha256": None})
    entry["wall_seconds"] = round(time.monotonic() - started, 3)
    return entry, rows, screen


def capsule_rows(root, build_slug, paper, capsules, quotes) -> list[dict]:
    """Create one metadata-table row per staged capsule."""
    rows = []
    for capsule in capsules:
        validation, claims = validation_state(root / "capsules" / capsule.name / "validation.json")
        evaluation, eval_details = eval_state(root / "capsules" / capsule.name / "eval.json")
        rows.append({
            "build_slug": build_slug,
            "capsule_id": capsule.name,
            "paper_doi": paper.get("doi"),
            "access_class": capsule_screen.access_class_for(paper.get("access") or {}),
            "license": (paper.get("access") or {}).get("license"),
            "task_id": eval_details["task_id"],
            "eval_state": evaluation,
            "eval_checks": eval_details["checks"],
            "validation_state": validation,
            "claims": claims,
            "quotes_after_screen": quotes.get(capsule.name, {}),
        })
    return rows


def aggregate_validation(rows: list[dict]) -> str:
    """Summarize build validation conservatively from its capsules."""
    states = {row["validation_state"] for row in rows}
    if states == {"strict"}:
        return "strict"
    if states <= {"strict", "clean"}:
        return "clean"
    return "present"


def make_manifest(args, collection, builds, rows) -> dict:
    """Build the versioned archive-set manifest.

    `not_released` lists the slugs of builds whose paper is not an included
    paper of the released corpus; they are neither staged nor zipped.
    """
    return {
        "schema": "asb-capsules-manifest/1",
        "domain": collection.get("domain") or collection.get("slug"),
        "collection_version": str(collection["version"]),
        "collection_version_doi": args.version_doi,
        "cut_id": collection.get("cut_id"),
        "tooling_commit": tooling_commit(),
        "generation_date": args.date,
        "inclusion_policy": {
            "capsule_members": _CAPSULE_KEEP + list(CAPSULE_FILES),
            "build_members": ["ledger"] + list(BUILD_FILES),
            "with_indicium": args.with_indicium,
            "pipeline_public": args.pipeline_public,
        },
        "build_count": len(builds),
        "builds_packed": sum(bool(build.get("sha256")) for build in builds),
        "builds_left_out": sum(not build.get("sha256") for build in builds),
        "capsule_count": len(rows),
        "capsules_left_out": sum(len(build["capsule_ids"]) for build in builds if not build.get("sha256")),
        "total_bytes": sum(build["bytes"] for build in builds),
        "not_released_count": len(args.not_released),
        "not_released": args.not_released,
        "source_inputs": source_receipt(args.view_name, args.collection, args.receipt_digests),
        "builds": builds,
    }


def make_screen(builds: list[dict], strict: bool) -> dict:
    """Aggregate non-sensitive screen measurements."""
    totals = Counter()
    for build in builds:
        totals.update(build["screen"]["counts"])
    return {
        "schema": "asb-capsules-screen/1",
        "strict": strict,
        "totals": dict(sorted(totals.items())),
        "builds": [{"build_slug": build["build_slug"], **build["screen"]} for build in builds],
    }


def make_zenodo(collection, template, args) -> dict:
    """Create deposit-ready metadata without contacting Zenodo."""
    domain = collection.get("domain") or collection.get("slug")
    description = (
        f"Screened slim-plus build capsules supplementing ASB {domain} v{collection['version']}. "
        f"The builds were produced by the {PIPELINE_NAME} pipeline. "
        "Generated metadata is CC-BY-4.0. Source quotations are bounded by field and DOI, "
        "and dropped for restricted or unresolved access. Rights holders may request takedown "
        "through the asb-skill-collections issue tracker."
    )
    related = [
        {"relation": "isSupplementTo", "identifier": args.version_doi, "scheme": "doi"},
        {"relation": "references", "identifier": TOOLING_URL, "scheme": "url"},
    ]
    if args.pipeline_public:
        related.append({"relation": "isCompiledBy", "identifier": PIPELINE_URL, "scheme": "url"})
    return {
        "title": f"ASB {domain} v{collection['version']} build capsules",
        "upload_type": "dataset",
        "publication_date": args.date,
        "description": description,
        "access_right": "open",
        "license": "cc-by-4.0",
        "creators": collection_creators(collection, args.citation, Path(__file__).resolve().parent.parent),
        "keywords": template.get("keywords") or [],
        "subjects": template.get("subjects") or [],
        "communities": [{"identifier": "asb_skill_collections"}],
        "related_identifiers": related,
        "version": f"{domain}-v{collection['version']}-capsules",
        "language": template.get("language", "eng"),
    }


def collection_creators(collection, citation, tooling_root: Path) -> list[dict]:
    """Use collection-declared creators, with the release creator file as fallback."""
    declared = (collection.get("roles") or {}).get("zenodo_authors")
    if declared:
        return [zenodo_deposit._zenodo_creator(entry) for entry in declared]
    authors = citation.get("authors") or []
    if authors:
        creators = []
        for author in authors:
            if author.get("name"):
                creators.append({"name": author["name"]})
            else:
                creators.append({"name": f"{author['family-names']}, {author['given-names']}"})
        return creators
    return zenodo_deposit.expected_creators(tooling_root)


def make_hf_card(collection, citation, manifest, args) -> str:
    """Render a local dataset card with JSONL or optional Parquet configuration."""
    domain = collection.get("domain") or collection.get("slug")
    table = "capsules.parquet" if (args.out / "capsules.parquet").is_file() else "capsules.jsonl"
    public_citation = {key: value for key, value in citation.items() if key not in PRIVATE_CITATION_KEYS}
    pipeline = PIPELINE_URL if args.pipeline_public else f"{PIPELINE_NAME} (private repository)"
    return f"""---
license: cc-by-4.0
task_categories: [question-answering]
size_categories: [{size_category(manifest['capsule_count'])}]
language: [en]
pretty_name: "ASB {domain} v{collection['version']} build capsules"
configs:
  - config_name: capsules
    data_files: "{table}"
---

# ASB {domain} v{collection['version']} build capsules

This local archive set contains {manifest['builds_packed']} per-build deterministic zips and {manifest['capsule_count']} capsule metadata rows. The metadata table is `{table}`. `benchmark-manifest.json` filters the complete operational evaluations without duplicating their payloads.

## Layout

- `builds/<build-slug>.zip`: screened slim-plus ledgers, evaluations, evidence, inputs, provenance and pruned RO-Crates.
- `MANIFEST.json`, `capsules.jsonl` and `SCREEN.json`: archive, capsule and screen receipts.
- `benchmark-manifest.json`: the complete-evaluation subset.

## Records and licence

Collection: https://doi.org/{args.version_doi}

Capsules record: {DOI_PLACEHOLDER} (reserved only after publication).

Generated metadata is CC-BY-4.0. Source quotations remain subject to bounded quotation rights and access-class redaction. This card does not grant a licence to removed source text.

Pipeline: {pipeline}

Tooling: {TOOLING_URL}

## Citation

```yaml
{yaml.safe_dump(public_citation, sort_keys=False).strip()}
```

Local generation only: no dataset repository is created or uploaded by the packer.
"""


def size_category(count: int) -> str:
    """Map row counts to HuggingFace size categories."""
    if count < 1000:
        return "n<1K"
    if count < 10000:
        return "1K<n<10K"
    if count < 100000:
        return "10K<n<100K"
    return "100K<n<1M"


def write_archive_readme(out: Path, manifest: dict, screen: dict) -> None:
    """Write the archive-set guide."""
    text = f"""# ASB {manifest['domain']} v{manifest['collection_version']} build capsules

Local screened archive set generated on {manifest['generation_date']}. No deposit, upload, or collection-record change was performed.

- `builds/`: one deterministic zip per build that passed the screen.
- `MANIFEST.json`: build and archive receipt.
- `capsules.jsonl`: one metadata row per capsule.
- `SCREEN.json`: content-screen counts and failures.
- `benchmark-manifest.json`: complete-evaluation subset.
- `zenodo/metadata.json` and `hf/README.md`: local record descriptions.

Builds considered: {manifest['build_count']}. Builds packed: {manifest['builds_packed']}. Builds left out by the screen: {manifest['builds_left_out']}.

Capsules packed: {manifest['capsule_count']}. Capsules left out with their builds: {manifest['capsules_left_out']}.

Builds left out because their paper is not an included paper of the released corpus: {manifest['not_released_count']}. They are listed by slug under `not_released` in `MANIFEST.json`.
"""
    (out / "README.md").write_text(text, encoding="utf-8")


def maybe_write_parquet(rows: list[dict], path: Path) -> bool:
    """Write Parquet only when the optional dependency is already available."""
    try:
        import pyarrow
        import pyarrow.parquet
    except ImportError:
        return False
    table = pyarrow.Table.from_pylist(rows)
    pyarrow.parquet.write_table(table, path)
    return True


def packed_capsule_rows(builds: list[dict], rows: list[dict]) -> list[dict]:
    """Return only capsule rows whose build has a zip in the record."""
    packed_slugs = {build["build_slug"] for build in builds if build.get("sha256")}
    return [row for row in rows if row["build_slug"] in packed_slugs]


def write_records(args, loaded: dict, builds: list[dict], rows: list[dict]) -> None:
    """Write every descriptive file of a pack from its build entries and capsule rows.

    The packer and `capsules_deposit.py refresh` both call this, so a refreshed
    pack holds what a full pack with the same inputs would write. `args` carries
    out, date, version_doi, citation, view_name, receipt_digests, with_indicium,
    strict, not_released, pipeline_public and the collection root.
    """
    collection = loaded["collection"]
    rows = packed_capsule_rows(builds, rows)
    manifest = make_manifest(args, collection, builds, rows)
    screen = make_screen(builds, args.strict)
    write_json(args.out / "MANIFEST.json", manifest)
    write_json(args.out / "SCREEN.json", screen)
    with (args.out / "capsules.jsonl").open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    maybe_write_parquet(rows, args.out / "capsules.parquet")
    metadata = make_zenodo(collection, loaded["template"], args)
    problems = zenodo_deposit.validate_metadata(metadata)
    if problems:
        raise ValueError("Invalid Zenodo metadata: " + "; ".join(problems))
    write_json(args.out / "zenodo" / "metadata.json", metadata)
    (args.out / "hf").mkdir(exist_ok=True)
    (args.out / "hf" / "README.md").write_text(make_hf_card(collection, loaded["citation"], manifest, args), encoding="utf-8")
    write_json(args.out / "benchmark-manifest.json", make_benchmark(builds, rows, args.version_doi))
    write_archive_readme(args.out, manifest, screen)


def make_benchmark(builds: list[dict], rows: list[dict], version_doi: str) -> dict:
    """Select the complete-evaluation capsules without copying their payloads.

    Rows keep the sorted key order of capsules.jsonl, so a pack refreshed from
    that file writes the same bytes.
    """
    benchmark_rows = [json.loads(json.dumps(row, sort_keys=True)) for row in rows if row["eval_state"] == "complete"]
    benchmark_ids = {(row["build_slug"], row["capsule_id"]) for row in benchmark_rows}
    benchmark_builds = [
        dict(build, capsule_ids=[value for value in build["capsule_ids"] if (build["build_slug"], value) in benchmark_ids])
        for build in builds
        if build.get("sha256") and any((build["build_slug"], value) in benchmark_ids for value in build["capsule_ids"])
    ]
    return {"schema": "asb-capsules-benchmark/1", "collection_version_doi": version_doi, "capsule_count": len(benchmark_rows), "capsules": benchmark_rows, "builds": benchmark_builds}


def bind_collection(args) -> dict:
    """Load the collection and set the receipt values every writer reads from args."""
    loaded = load_collection(args.collection)
    args.citation = loaded["citation"]
    args.version_doi = collection_version_doi(loaded)
    return loaded


def run(args) -> int:
    """Run the local packer and return a process status."""
    loaded = bind_collection(args)
    args.view_name = args.view.name
    args.receipt_digests = input_digests(args.access_records, args.deny_patterns_file)
    args.out.mkdir(parents=True, exist_ok=True)
    released = released_names(loaded["corpus"])
    sources = discover_builds(args.view, args.limit)
    args.not_released = sorted(build_slug(source.name) for source in sources if source.name not in released)
    overrides = load_access_records(args.access_records)
    deny_patterns = tuple(line.strip() for line in args.deny_patterns_file.read_text(encoding="utf-8").splitlines() if line.strip()) if args.deny_patterns_file else ()
    options = {"with_indicium": args.with_indicium, "deny_patterns": deny_patterns,
               "private_repositories": private_repositories(pipeline_public=args.pipeline_public)}
    builds, rows = [], []
    with tempfile.TemporaryDirectory(prefix="capsules-stage-", dir=args.out) as temporary:
        for source in (source for source in sources if source.name in released):
            paper = resolve_paper(source.name, loaded["corpus"], overrides)
            entry, capsule_data, _ = pack_one(source, Path(temporary), args.out, paper, loaded["collection"], options)
            builds.append(entry)
            rows.extend(capsule_data)
    timings = [{"build_slug": build["build_slug"], "wall_seconds": build.pop("wall_seconds")} for build in builds]
    failed = any(build["screen"]["failures"] for build in builds)
    if args.strict and failed:
        shutil.rmtree(args.out / "builds", ignore_errors=True)
    write_records(args, loaded, builds, rows)
    packed_rows = packed_capsule_rows(builds, rows)
    left_out = sum(len(build["capsule_ids"]) for build in builds if not build.get("sha256"))
    print(json.dumps({"builds": len(builds), "capsules": len(packed_rows), "capsules_left_out": left_out,
                      "not_released": len(args.not_released), "wall_seconds_by_build": timings}))
    return int(args.strict and failed)


def parse_args(argv=None):
    """Parse the packer command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--view", type=Path, required=True)
    parser.add_argument("--collection", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--access-records", type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--with-indicium", action="store_true")
    parser.add_argument("--deny-patterns-file", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--pipeline-public", action="store_true",
                        help=f"link the {PIPELINE_NAME} repository and keep its URLs; leave off while it is private")
    args = parser.parse_args(argv)
    args.view = args.view.resolve()
    args.collection = args.collection.resolve()
    args.out = args.out.resolve()
    return args


def main(argv=None) -> int:
    """Command-line entry point."""
    return run(parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
