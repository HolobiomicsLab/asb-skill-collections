#!/usr/bin/env python3
"""Take a build-capsules pack to a citable Zenodo record, up to a reviewed draft.

Five subcommands, in the order a maintainer runs them:

  refresh     rewrite the descriptive files of an existing pack against the
              collection as it is now (its current version DOI and label), and
              copy the build zips unchanged after checking each one against
              MANIFEST.json. Builds whose paper is not an included paper of the
              released corpus are dropped. Never writes into the source pack.
  archive     write one deterministic zip per record holding the build zips,
              stored without recompression, and the descriptive files.
  plan        offline: build the archive, check the pack, and write
              deposit-plan.json with the metadata, the files and the refusals.
  create      on the owner's terminal only: create a first-release draft as a
              new Zenodo record from a plan. Never publishes.
  record-doi  after the owner publishes: write the capsules block on the
              released version's row of collections.yaml, the README table
              cell and the catalogue.

HTTP, zip headers, md5 checks, creators and metadata validation come from
`scripts/zenodo_deposit.py`; the descriptive files come from
`scripts/pack_capsules.py`, so a refreshed pack and a full pack agree.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import io
import json
import re
import shutil
import sys
import urllib.parse
import zipfile
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts import capsule_screen, check_collections_manifest, pack_capsules, regen_catalogue, zenodo_deposit
from scripts.release_domain import dump_registry, registry_dates

TOOLING_ROOT = Path(__file__).resolve().parent.parent
PLAN_SCHEMA = "asb-capsules-deposit-plan/1"
PLAN_FILE = "deposit-plan.json"
UPLOAD_DIR = "upload"
# Uploaded beside the archive so a reader can browse them on the record page.
BROWSABLE_FILES = ("README.md", "MANIFEST.json", "capsules.jsonl", "SCREEN.json", "benchmark-manifest.json")
DESCRIPTIVE_FILES = BROWSABLE_FILES + ("zenodo/metadata.json", "hf/README.md", "capsules.parquet")
LOCAL_PATH_MARKERS = ("/Users/", "/Volumes/", "/private/")
CHUNK_BYTES = 1024 * 1024
FIRST_SHOWN = 3
README_CAPSULES = re.compile(r" \(build capsules: \[[^\]]*\]\([^)]*\)\)$")
TAKEDOWN_URL = "https://github.com/HolobiomicsLab/asb-skill-collections/issues"


class CapsulesError(RuntimeError):
    """A step cannot proceed; the message says why."""


@dataclass(frozen=True)
class BuiltArchive:
    """The record archive: its path, digests, size and member count."""

    path: Path
    sha256: str
    md5: str
    size: int
    members: int


def read_json(path: Path):
    """Read one JSON document."""
    return json.loads(path.read_text(encoding="utf-8"))


def read_rows(path: Path) -> list[dict]:
    """Read capsules.jsonl."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def file_digests(path: Path) -> tuple[str, str, int]:
    """Stream a file once and return its sha256, md5 and size."""
    sha, md5, size = hashlib.sha256(), hashlib.md5(), 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK_BYTES), b""):
            sha.update(chunk)
            md5.update(chunk)
            size += len(chunk)
    return sha.hexdigest(), md5.hexdigest(), size


def zipped_entries(manifest: dict) -> list[dict]:
    """Return the manifest entries that declare a build zip."""
    return [entry for entry in manifest["builds"] if entry.get("sha256")]


def build_set_problems(pack: Path, manifest: dict) -> list[str]:
    """Compare the zips on disk with the manifest by name and size, without reading them."""
    declared = {entry["zip_member"]: entry for entry in zipped_entries(manifest)}
    present = {f"builds/{path.name}": path for path in (pack / "builds").glob("*.zip")} if (pack / "builds").is_dir() else {}
    problems = [f"{name}: zip absent from MANIFEST.json" for name in sorted(set(present) - set(declared))]
    problems += [f"{name}: listed in MANIFEST.json, zip missing" for name in sorted(set(declared) - set(present))]
    for name in sorted(set(declared) & set(present)):
        size = present[name].stat().st_size
        if size != declared[name]["bytes"]:
            problems.append(f"{name}: {size} bytes on disk, MANIFEST.json says {declared[name]['bytes']}")
    return problems


def verified_bytes(pack: Path, entry: dict) -> bytes:
    """Read one build zip and refuse it when its sha256 differs from the manifest."""
    data = (pack / entry["zip_member"]).read_bytes()
    if hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise CapsulesError(f"{entry['zip_member']}: sha256 differs from MANIFEST.json")
    return data


def outside(path: Path, pack: Path) -> Path:
    """Refuse an output directory that is the pack or lies inside it."""
    path, pack = path.resolve(), pack.resolve()
    if path == pack or pack in path.parents:
        raise CapsulesError(f"output {path} is inside the pack; the pack is never written")
    return path


# refresh ---------------------------------------------------------------------

def refresh_args(args, loaded: dict, manifest: dict, screen: dict, not_released: list[str]):
    """Rebuild the packer's receipt values from the old pack and the collection now."""
    inputs = manifest.get("source_inputs") or {}
    return SimpleNamespace(
        out=args.out, date=args.date, collection=args.collection,
        citation=loaded["citation"], version_doi=pack_capsules.collection_version_doi(loaded),
        view_name=inputs.get("view"),
        receipt_digests={key: value for key, value in inputs.items() if key not in {"view", "collection", "collection_files"}},
        with_indicium=bool((manifest.get("inclusion_policy") or {}).get("with_indicium")),
        strict=bool(screen.get("strict")), not_released=not_released,
        pipeline_public=pipeline_public(manifest),
    )


def pipeline_public(manifest: dict) -> bool:
    """Read whether the pack was screened with the pipeline declared public."""
    return bool((manifest.get("inclusion_policy") or {}).get("pipeline_public"))


def released_split(manifest: dict, rows: list[dict], released: set[str]):
    """Split builds and rows into those of released papers and the slugs left out."""
    kept = [entry for entry in manifest["builds"] if entry["source_name"] in released]
    dropped = {entry["build_slug"] for entry in manifest["builds"]} - {entry["build_slug"] for entry in kept}
    not_released = sorted(set(manifest.get("not_released") or []) | dropped)
    kept_slugs = {entry["build_slug"] for entry in kept}
    return kept, [row for row in rows if row["build_slug"] in kept_slugs], not_released


def copy_verified(source: Path, target: Path, entry: dict) -> None:
    """Copy one build zip while hashing it, and refuse a copy whose digest differs."""
    hasher = hashlib.sha256()
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as reader, target.open("wb") as writer:
        for chunk in iter(lambda: reader.read(CHUNK_BYTES), b""):
            hasher.update(chunk)
            writer.write(chunk)
    if hasher.hexdigest() != entry["sha256"]:
        target.unlink()
        raise CapsulesError(f"{entry['zip_member']}: sha256 differs from MANIFEST.json")


def run_refresh(args) -> int:
    """Regenerate the descriptive files of a pack into a new directory."""
    out = outside(args.out, args.pack)
    if out.exists() and any(out.iterdir()):
        raise CapsulesError(f"output directory is not empty: {out}")
    manifest = read_json(args.pack / "MANIFEST.json")
    problems = build_set_problems(args.pack, manifest)
    if problems:
        raise CapsulesError("; ".join(problems))
    loaded = pack_capsules.load_collection(args.collection)
    kept, rows, not_released = released_split(manifest, read_rows(args.pack / "capsules.jsonl"),
                                              pack_capsules.released_names(loaded["corpus"]))
    out.mkdir(parents=True, exist_ok=True)
    for entry in (entry for entry in kept if entry.get("sha256")):
        copy_verified(args.pack / entry["zip_member"], out / entry["zip_member"], entry)
    screen = read_json(args.pack / "SCREEN.json")
    pack_capsules.write_records(refresh_args(args, loaded, manifest, screen, not_released), loaded, kept, rows)
    packed_rows = pack_capsules.packed_capsule_rows(kept, rows)
    left_out = sum(len(build["capsule_ids"]) for build in kept if not build.get("sha256"))
    print(json.dumps({"builds": len(kept), "capsules": len(packed_rows),
                      "capsules_left_out": left_out, "not_released": len(not_released)}))
    return 0


# archive ---------------------------------------------------------------------

def archive_name(manifest: dict) -> str:
    """Return the record archive's file name."""
    return f"asb-{manifest['domain']}-v{manifest['collection_version']}-build-capsules.zip"


def build_archive(pack: Path, out: Path, inspect=None) -> BuiltArchive:
    """Write the record archive, verifying each build zip against the manifest.

    Build zips are stored without recompression; the descriptive files are
    deflated. Members are sorted with fixed timestamps and modes. `inspect`, when
    given, receives (member name, bytes) for each build zip.
    """
    manifest = read_json(pack / "MANIFEST.json")
    problems = build_set_problems(pack, manifest)
    if problems:
        raise CapsulesError("; ".join(problems))
    members = {name: None for name in DESCRIPTIVE_FILES if (pack / name).is_file()}
    members.update({entry["zip_member"]: entry for entry in zipped_entries(manifest)})
    out.mkdir(parents=True, exist_ok=True)
    target = out / archive_name(manifest)
    partial = target.with_suffix(".partial")
    try:
        write_members(pack, partial, members, inspect)
    except BaseException:
        partial.unlink(missing_ok=True)
        raise
    partial.replace(target)
    sha, md5, size = file_digests(target)
    return BuiltArchive(target, sha, md5, size, len(members))


def write_members(pack: Path, target: Path, members: dict, inspect) -> None:
    """Write the sorted members; an entry dict marks a build zip to verify and store."""
    with zipfile.ZipFile(target, "w") as archive:
        for name in sorted(members):
            info = zenodo_deposit._zip_info(name, pack / name)
            entry = members[name]
            if entry is None:
                archive.writestr(info, (pack / name).read_bytes(), compresslevel=9)
                continue
            data = verified_bytes(pack, entry)
            if inspect is not None:
                inspect(name, data)
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, data)


def run_archive(args) -> int:
    """Build the record archive and print its digest."""
    built = build_archive(args.pack, outside(args.out, args.pack))
    print(f"{built.path}\nsha256 {built.sha256}\nmd5 {built.md5}\nsize {built.size} bytes\nmembers {built.members}")
    return 0


# plan ------------------------------------------------------------------------

def text_problems(label: str, text: str, url_pattern: re.Pattern, check_paths: bool) -> list[str]:
    """List private-repository URLs and, when asked, local absolute paths in one text."""
    problems = []
    match = url_pattern.search(text) if url_pattern else None
    if match:
        problems.append(f"{label}: private repository URL {match.group(0)}")
    if check_paths:
        problems += [f"{label}: local absolute path {marker}" for marker in LOCAL_PATH_MARKERS if marker in text]
    return problems


def build_zip_findings(name: str, data: bytes, url_pattern) -> list[tuple[str, str, str]]:
    """Return (member, URL, build zip) for each private-repository URL in a build zip's text members."""
    findings = []
    if url_pattern is None:
        return findings
    with zipfile.ZipFile(io.BytesIO(data)) as inner:
        for member in inner.namelist():
            if Path(member).suffix.lower() in capsule_screen.TEXT_SUFFIXES:
                match = url_pattern.search(inner.read(member).decode("utf-8", errors="replace"))
                if match:
                    findings.append((member, match.group(0), name))
    return findings


def grouped_zip_problems(findings: list[tuple[str, str, str]]) -> list[str]:
    """Report one refusal per member and URL, with the count of build zips and the first few."""
    groups = {}
    for member, url, name in findings:
        groups.setdefault((member, url), []).append(name)
    return [f"{member} in {len(names)} build zips: private repository URL {url} (first: {', '.join(names[:FIRST_SHOWN])})"
            for (member, url), names in sorted(groups.items())]


def screen_problems(manifest: dict, screen: dict) -> list[str]:
    """Refuse a build that has a zip while its screen shows a failure or a deny hit."""
    zipped = {entry["build_slug"] for entry in zipped_entries(manifest)}
    problems = []
    for build in screen.get("builds") or []:
        if build["build_slug"] not in zipped:
            continue
        if build.get("failures"):
            problems.append(f"SCREEN.json: build {build['build_slug']} has a zip and {len(build['failures'])} screen failures")
        if (build.get("counts") or {}).get("deny_hits"):
            problems.append(f"SCREEN.json: build {build['build_slug']} has a zip and deny hits")
    return problems


def release_problems(manifest: dict, rows: list[dict], released: set[str]) -> list[str]:
    """Refuse zips and capsule rows of builds that are not included papers of the collection."""
    by_slug = {entry["build_slug"]: entry for entry in manifest["builds"]}
    problems = [f"MANIFEST.json: build {entry['build_slug']} has a zip and its paper is not an included paper of the collection"
                for entry in zipped_entries(manifest) if entry["source_name"] not in released]
    stray = sorted({row["build_slug"] for row in rows if row["build_slug"] not in by_slug})
    problems += [f"capsules.jsonl: rows of build {slug}, which MANIFEST.json does not list" for slug in stray]
    unreleased = sorted({row["build_slug"] for row in rows
                         if row["build_slug"] in by_slug and by_slug[row["build_slug"]]["source_name"] not in released})
    problems += [f"capsules.jsonl: rows of build {slug}, whose paper is not an included paper of the collection" for slug in unreleased]
    return problems


def holdings_problems(manifest: dict, rows: list[dict], benchmark: dict) -> list[str]:
    """Refuse table rows that point at a build zip the record does not hold."""
    packed = {entry["build_slug"] for entry in zipped_entries(manifest)}
    problems = []
    for label, table_rows in (("capsules.jsonl", rows), ("benchmark-manifest.json", benchmark.get("capsules") or [])):
        stale = sorted({row.get("build_slug") for row in table_rows if row.get("build_slug") not in packed})
        problems += [f"{label}: rows of build {slug}, which has no zip in the record" for slug in stale]
    stale_builds = sorted({entry.get("build_slug") for entry in benchmark.get("builds") or []
                           if entry.get("build_slug") not in packed})
    problems += [f"benchmark-manifest.json: build {slug} has no zip in the record" for slug in stale_builds]
    return problems


def doi_problems(manifest: dict, metadata: dict, current: str) -> list[str]:
    """Require the pack and its metadata to supplement the collection's current version DOI."""
    supplements = [related.get("identifier") for related in metadata.get("related_identifiers") or []
                   if related.get("relation") == "isSupplementTo"]
    problems = []
    if [pack_capsules.normalize_doi(value) for value in supplements] != [current]:
        problems.append(f"zenodo/metadata.json: isSupplementTo is {supplements}, the collection's current version DOI is {current}; run refresh")
    if manifest.get("collection_version_doi") != current:
        problems.append(f"MANIFEST.json: collection_version_doi is {manifest.get('collection_version_doi')}, the collection's is {current}; run refresh")
    return problems


def collection_problems(manifest: dict, collection: dict) -> list[str]:
    """Require the pack to describe the collection it is planned against."""
    domain = collection.get("domain") or collection.get("slug")
    if manifest.get("domain") == domain and manifest.get("collection_version") == str(collection.get("version")):
        return []
    return [f"MANIFEST.json describes {manifest.get('domain')} v{manifest.get('collection_version')}, "
            f"the collection is {domain} v{collection.get('version')}"]


def metadata_problems(metadata: dict, tooling_root: Path) -> list[str]:
    """Run the deposit API checks and the release creators check."""
    problems = [f"zenodo/metadata.json: {problem}" for problem in zenodo_deposit.validate_metadata(metadata)]
    expected = zenodo_deposit.expected_creators(tooling_root)
    return problems + [f"zenodo/metadata.json: {problem}" for problem in zenodo_deposit.creator_problems(metadata, expected)]


def descriptive_problems(pack: Path, url_pattern: re.Pattern) -> list[str]:
    """Scan every descriptive file for private-repository URLs and local paths."""
    problems = []
    for name in DESCRIPTIVE_FILES:
        path = pack / name
        if path.is_file() and path.suffix != ".parquet":
            problems += text_problems(name, path.read_text(encoding="utf-8"), url_pattern, True)
    return problems


def pack_refusals(args, pack: dict, loaded: dict) -> list[str]:
    """Collect every refusal that does not need the archive."""
    released = pack_capsules.released_names(loaded["corpus"])
    current = pack_capsules.collection_version_doi(loaded)
    refusals = collection_problems(pack["manifest"], loaded["collection"])
    refusals += screen_problems(pack["manifest"], pack["screen"])
    refusals += release_problems(pack["manifest"], pack["rows"], released)
    refusals += holdings_problems(pack["manifest"], pack["rows"], pack["benchmark"])
    refusals += doi_problems(pack["manifest"], pack["metadata"], current)
    refusals += metadata_problems(pack["metadata"], args.tooling_root)
    return refusals + descriptive_problems(args.pack, pack["url_pattern"])


def upload_files(args, built: BuiltArchive | None, record_readme: str) -> list[dict]:
    """Copy the browsable files beside the archive and describe every upload."""
    upload = args.out / UPLOAD_DIR
    upload.mkdir(parents=True, exist_ok=True)
    paths = [built.path] if built else []
    for name in BROWSABLE_FILES:
        if name == "README.md":
            (upload / name).write_text(record_readme, encoding="utf-8")
        else:
            shutil.copyfile(args.pack / name, upload / name)
        paths.append(upload / name)
    files = []
    for path in paths:
        sha, md5, size = file_digests(path)
        files.append({"name": path.name, "path": path.relative_to(args.out).as_posix(), "bytes": size, "sha256": sha, "md5": md5})
    return files


def plan_counts(manifest: dict, rows: list[dict], benchmark: dict) -> dict:
    """Count what the record holds."""
    packed_slugs = {entry["build_slug"] for entry in zipped_entries(manifest)}
    packed_rows = [row for row in rows if row.get("build_slug") in packed_slugs]
    left_out_rows = [row for row in rows if row.get("build_slug") not in packed_slugs]
    benchmark_rows = [row for row in benchmark.get("capsules") or [] if row.get("build_slug") in packed_slugs]
    return {
        "builds_packed": len(packed_slugs),
        "builds_left_out": len(manifest["builds"]) - len(packed_slugs),
        "builds_not_released": len(manifest.get("not_released") or []),
        "capsules": len(packed_rows),
        "capsules_left_out": manifest.get("capsules_left_out", len(left_out_rows)),
        "benchmark_capsules": len(benchmark_rows),
    }


def screen_failure_classes(manifest: dict) -> dict[str, int]:
    """Count left-out builds by broad, reader-facing failure class."""
    classes = {}
    for build in manifest["builds"]:
        if build.get("sha256"):
            continue
        labels = set()
        if (build.get("screen", {}).get("counts") or {}).get("deny_hits"):
            labels.add("deny-list hit")
        for failure in build.get("screen", {}).get("failures") or []:
            reason = failure.rsplit(": ", 1)[-1]
            if reason.startswith("missing:"):
                labels.add("missing required archive members")
            elif "invalid_validation_or_eval" in reason:
                labels.add("invalid evaluation or validation metadata")
            elif reason != "deny_hits":
                labels.add(reason.replace("_", " "))
        for label in labels or {"other screen failure"}:
            classes[label] = classes.get(label, 0) + 1
    return dict(sorted(classes.items()))


def make_record_readme(manifest: dict, counts: dict, archive: str) -> str:
    """Render the public README uploaded beside the archive."""
    failure_lines = "\n".join(
        f"- {count} build{'s' if count != 1 else ''}: {label}."
        for label, count in screen_failure_classes(manifest).items()
    ) or "- None."
    return f"""# ASB {manifest['domain']} v{manifest['collection_version']} build capsules

This record supplements the ASB {manifest['domain']} v{manifest['collection_version']} collection at https://doi.org/{manifest['collection_version_doi']}.

## Files on this record

- `{archive}`: the archive of screened build zips and their local generation receipts.
- `README.md`: this record guide.
- `MANIFEST.json`: every considered build, including screen failures, and the archive counts and checksums.
- `capsules.jsonl`: one row per capsule held by the record.
- `SCREEN.json`: content-screen counts and failures.
- `benchmark-manifest.json`: the {counts['benchmark_capsules']} capsules with a complete operational evaluation.

Inside `{archive}`, each row of `capsules.jsonl` maps `build_slug` to `builds/<build_slug>.zip`. Open that nested zip and use the row's `capsule_id` to find the capsule under `capsules/<capsule_id>/`, including its evaluation, evidence, inputs, provenance and pruned RO-Crate.

## Contents and exclusions

- Builds packed: {counts['builds_packed']}.
- Capsules packed: {counts['capsules']}.
- Benchmark capsules: {counts['benchmark_capsules']}.
- Builds left out by the screen: {counts['builds_left_out']}.
- Capsules left out with those builds: {counts['capsules_left_out']}.
- Builds not packed because their paper is not in the released corpus: {counts['builds_not_released']}.

Screen failure classes count builds and may overlap:

{failure_lines}

The screen names private repository URLs without linking them and redacts emails and phone-shaped numbers. It replaces build-machine paths with portable locators. It caps or drops quotations according to the source access class. See `SCREEN.json` for the measured counts and per-build failures.

Generated metadata is licensed CC-BY-4.0. Source quotations retain their original rights status and are included only as bounded quotations; this record does not relicense them.

For a takedown request, use the public tooling issue tracker: {TAKEDOWN_URL}.

## Citation

Cite this record by its DOI and cite the supplemented collection at https://doi.org/{manifest['collection_version_doi']}.
"""


def load_pack(pack: Path, url_pattern: re.Pattern) -> dict:
    """Read the descriptive files a plan checks."""
    return {
        "manifest": read_json(pack / "MANIFEST.json"),
        "rows": read_rows(pack / "capsules.jsonl"),
        "screen": read_json(pack / "SCREEN.json"),
        "benchmark": read_json(pack / "benchmark-manifest.json"),
        "metadata": read_json(pack / "zenodo" / "metadata.json"),
        "url_pattern": url_pattern,
    }


def make_plan(args) -> dict:
    """Check the pack, build the archive and return the deposit plan."""
    manifest = read_json(args.pack / "MANIFEST.json")
    repositories = pack_capsules.private_repositories(args.tooling_root / "collections.yaml", pipeline_public(manifest))
    pack = load_pack(args.pack, capsule_screen.private_url_pattern(repositories))
    loaded = pack_capsules.load_collection(args.collection)
    refusals = pack_refusals(args, pack, loaded)
    zip_findings = []
    try:
        built = build_archive(args.pack, args.out / UPLOAD_DIR,
                              lambda name, data: zip_findings.extend(build_zip_findings(name, data, pack["url_pattern"])))
    except CapsulesError as error:
        built = None
        refusals.append(f"archive: {error}")
    metadata = dict(pack["metadata"], publication_date=args.date)
    counts = plan_counts(pack["manifest"], pack["rows"], pack["benchmark"])
    archive = built.path.name if built else archive_name(pack["manifest"])
    record_readme = make_record_readme(pack["manifest"], counts, archive)
    refusals += text_problems("upload/README.md", record_readme, pack["url_pattern"], True)
    return {
        "schema": PLAN_SCHEMA,
        "domain": pack["manifest"]["domain"],
        "collection_version": pack["manifest"]["collection_version"],
        "collection_version_doi": pack_capsules.collection_version_doi(loaded),
        "publication_date": args.date,
        "metadata": metadata,
        "archive": {"name": built.path.name, "bytes": built.size, "sha256": built.sha256, "members": built.members} if built else None,
        "files": upload_files(args, built, record_readme),
        "counts": counts,
        "refusals": refusals + grouped_zip_problems(zip_findings),
    }


def describe_plan(plan: dict) -> str:
    """Render the plan summary printed by `plan`."""
    lines = [f"record: ASB {plan['domain']} v{plan['collection_version']} build capsules, supplementing {plan['collection_version_doi']}",
             "metadata:", json.dumps(plan["metadata"], indent=2, ensure_ascii=False), "files:"]
    lines += [f"  {item['name']}  {item['bytes']} bytes  sha256 {item['sha256']}  md5 {item['md5']}" for item in plan["files"]]
    lines += [f"{key}: {value}" for key, value in plan["counts"].items()]
    lines += [f"refused: {refusal}" for refusal in plan["refusals"]] or ["refusals: none"]
    return "\n".join(lines)


def run_plan(args) -> int:
    """Write deposit-plan.json and print it; exit 1 on any refusal."""
    args.out = outside(args.out, args.pack)
    args.out.mkdir(parents=True, exist_ok=True)
    plan = make_plan(args)
    pack_capsules.write_json(args.out / PLAN_FILE, plan)
    print(describe_plan(plan))
    return 1 if plan["refusals"] else 0


# create ----------------------------------------------------------------------

def checked_plan(path: Path) -> tuple[dict, list[Path]]:
    """Load a plan, refuse it when it carries refusals or a file changed since it was written."""
    plan = read_json(path)
    if plan.get("schema") != PLAN_SCHEMA:
        raise CapsulesError(f"{path} is not an {PLAN_SCHEMA} plan")
    if plan.get("refusals"):
        raise CapsulesError("the plan carries refusals: " + "; ".join(plan["refusals"]))
    if not plan.get("archive"):
        raise CapsulesError("the plan has no archive")
    paths = []
    for item in plan["files"]:
        file_path = path.parent / item["path"]
        if not file_path.is_file():
            raise CapsulesError(f"stale plan: {item['path']} is missing")
        if file_digests(file_path) != (item["sha256"], item["md5"], item["bytes"]):
            raise CapsulesError(f"stale plan: {item['path']} changed since the plan was written; run plan again")
        paths.append(file_path)
    return plan, paths


def draft_receipt_path(plan_path: Path, sandbox: bool) -> Path:
    """Return the file beside the plan that records the draft created from it."""
    return plan_path.parent / ("draft-sandbox.json" if sandbox else "draft.json")


def write_draft_receipt(path: Path, draft: dict, host: str, complete: bool) -> None:
    """Record the draft id, concept record id, address and host, and whether setup finished."""
    url = draft["links"].get("html") or f"{host}/deposit/{draft['id']}"
    pack_capsules.write_json(path, {"draft_id": draft["id"], "conceptrecid": draft.get("conceptrecid"),
                                    "url": url, "host": host, "complete": complete})


def run_create(args) -> int:
    """Create a first-release draft as a new record from a plan. Never publishes.

    The receipt beside the plan is written as soon as the draft exists, so a
    rerun after a failure halfway refuses instead of creating a second draft;
    `--again` overrides it.
    """
    receipt = draft_receipt_path(args.plan, args.sandbox)
    if receipt.exists() and not args.again:
        raise CapsulesError(f"a draft was already created from this plan ({receipt}); "
                            "finish it in the web interface, or pass --again to create another")
    plan, paths = checked_plan(args.plan)
    problems = zenodo_deposit.validate_metadata(plan["metadata"])
    if problems:
        raise CapsulesError("metadata rejected by the API: " + "; ".join(problems))
    token = zenodo_deposit._token(args.sandbox)
    host = zenodo_deposit._host(args.sandbox)
    base = f"{host}/api/deposit/depositions"
    draft = zenodo_deposit._call("new record", "POST", base, token, {})
    write_draft_receipt(receipt, draft, host, complete=False)
    for path in paths:
        zenodo_deposit._upload("file upload", f"{draft['links']['bucket']}/{urllib.parse.quote(path.name)}", path, token)
    zenodo_deposit.update_metadata(draft, {"metadata": plan["metadata"]}, token, base, inherited=False)
    write_draft_receipt(receipt, draft, host, complete=True)
    print(f"draft {draft['id']} created as a new record, not published: {read_json(receipt)['url']}")
    print(f"conceptrecid {draft.get('conceptrecid')}")
    return 0


# record-doi ------------------------------------------------------------------

def capsules_block(plan: dict, args) -> dict:
    """Return the registry block of a published capsules record."""
    return {
        "version_doi": args.doi,
        "concept_doi": args.concept_doi,
        "record_id": str(args.record_id),
        "supplements": plan["collection_version_doi"],
        "builds_packed": plan["counts"]["builds_packed"],
        "builds_left_out": plan["counts"]["builds_left_out"],
        "builds_not_released": plan["counts"]["builds_not_released"],
        "capsules": plan["counts"]["capsules"],
        "benchmark_capsules": plan["counts"]["benchmark_capsules"],
        "archive_bytes": plan["archive"]["bytes"],
        "archive_sha256": plan["archive"]["sha256"],
        "published": datetime.date.fromisoformat(args.published or plan["publication_date"]),
    }


def target_release(document: dict, plan: dict) -> dict:
    """Find the registry row of the version the record supplements."""
    domain = (document.get("domains") or {}).get(plan["domain"])
    if not isinstance(domain, dict):
        raise CapsulesError(f"collections.yaml has no domain {plan['domain']}")
    for release in domain.get("releases") or []:
        if str(release.get("version")) == str(plan["collection_version"]):
            dois = [release.get("version_doi")] + [entry.get("version_doi") for entry in release.get("superseded") or []]
            if plan["collection_version_doi"] not in dois:
                raise CapsulesError(f"{plan['collection_version_doi']} is not a version DOI of {plan['domain']} v{plan['collection_version']}")
            return release
    raise CapsulesError(f"collections.yaml has no {plan['domain']} v{plan['collection_version']} row")


def readme_with_capsules(text: str, domain: str, doi: str) -> str:
    """Append the capsules DOI to the version DOI cell of the domain's README row."""
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")] if line.lstrip().startswith("|") else []
        if cells and cells[0] == domain and len(cells) == 7:
            cells[-1] = README_CAPSULES.sub("", cells[-1]) + f" (build capsules: [{doi}](https://doi.org/{doi}))"
            ending = "\n" if line.endswith("\n") else ""
            lines[index] = "| " + " | ".join(cells) + " |" + ending
            return "".join(lines)
    raise CapsulesError(f"README.md has no collections-table row for {domain}")


def check_record_arguments(args) -> None:
    """Refuse malformed DOIs or a record id the version DOI does not name."""
    pattern = check_collections_manifest.DOI_PATTERN
    for name in ("doi", "concept_doi"):
        if not pattern.fullmatch(getattr(args, name)):
            raise CapsulesError(f"--{name.replace('_', '-')} must be a Zenodo DOI")
    if not str(args.record_id).isdigit() or args.doi.rsplit(".", 1)[-1] != str(args.record_id):
        raise CapsulesError("--record-id must be the id the version DOI names")


def run_record_doi(args) -> int:
    """Write the capsules block, the README cell and the catalogue, then validate them."""
    check_record_arguments(args)
    plan, _ = checked_plan(args.plan)
    root = args.manifest.resolve().parent
    paths = {"registry": args.manifest.resolve(), "readme": root / "README.md", "catalogue": root / "catalogue.jsonld"}
    originals = {key: path.read_bytes() for key, path in paths.items()}
    document = yaml.safe_load(originals["registry"].decode("utf-8"))
    release = target_release(document, plan)
    release["capsules"] = capsules_block(plan, args)
    releases = document["domains"][plan["domain"]]["releases"]
    releases[:] = [registry_dates(row) for row in releases]
    registry_text, dropped = dump_registry(document, originals["registry"].decode("utf-8"))
    readme_text = readme_with_capsules(originals["readme"].decode("utf-8"), plan["domain"], args.doi)
    paths["registry"].write_text(registry_text, encoding="utf-8")
    paths["readme"].write_text(readme_text, encoding="utf-8")
    regen_catalogue.write_catalogue(regen_catalogue.build_catalogue(root), paths["catalogue"])
    failures = check_collections_manifest.audit(paths["registry"], paths["catalogue"], {})
    if failures:
        for key, path in paths.items():
            path.write_bytes(originals[key])
        raise CapsulesError("registry check failed, files restored: " + "; ".join(failures))
    for comment in dropped:
        print(f"warning: registry comment dropped, its row changed: {comment}", file=sys.stderr)
    print(f"capsules {args.doi} recorded on {plan['domain']} v{plan['collection_version']}")
    return 0


# command line ----------------------------------------------------------------

def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    commands = parser.add_subparsers(dest="command", required=True)
    refresh = commands.add_parser("refresh", help="rewrite a pack's descriptive files against the collection now")
    refresh.set_defaults(handler=run_refresh)
    archive = commands.add_parser("archive", help="write the record archive")
    archive.set_defaults(handler=run_archive)
    plan = commands.add_parser("plan", help="check a pack and write deposit-plan.json; no network")
    plan.set_defaults(handler=run_plan)
    for command in (refresh, archive, plan):
        command.add_argument("--pack", type=Path, required=True)
        command.add_argument("--out", type=Path, required=True)
    for command in (refresh, plan):
        command.add_argument("--collection", type=Path, required=True, help="released collection root")
        command.add_argument("--date", required=True, type=_date)
    plan.add_argument("--tooling-root", type=Path, default=TOOLING_ROOT,
                      help="root holding collections.yaml and scripts/release_creators.yaml")
    create = commands.add_parser("create", help="create a first-release draft on Zenodo from a plan; never publishes")
    create.set_defaults(handler=run_create)
    create.add_argument("--sandbox", action="store_true", help="use sandbox.zenodo.org and ZENODO_SANDBOX_TOKEN")
    create.add_argument("--again", action="store_true",
                        help="create another draft although draft.json (or draft-sandbox.json) exists beside the plan")
    record = commands.add_parser("record-doi", help="record a published capsules record in collections.yaml")
    record.set_defaults(handler=run_record_doi)
    record.add_argument("--doi", required=True, help="version DOI of the published record")
    record.add_argument("--concept-doi", required=True)
    record.add_argument("--record-id", required=True)
    record.add_argument("--manifest", type=Path, required=True, help="collections.yaml of this repository")
    record.add_argument("--published", type=_date, default=None,
                        help="publication date of the record; defaults to the plan's date")
    for command in (create, record):
        command.add_argument("--plan", type=Path, required=True)
    return parser


def _date(value: str) -> str:
    """Accept only an ISO date."""
    datetime.date.fromisoformat(value)
    return value


def main(argv=None) -> int:
    """Run one subcommand; print errors to stderr and return the exit code."""
    args = _parser().parse_args(argv)
    for name in ("pack", "out", "collection", "tooling_root", "plan"):
        if getattr(args, name, None) is not None:
            setattr(args, name, getattr(args, name).resolve())
    try:
        return args.handler(args)
    except (CapsulesError, zenodo_deposit.ZenodoError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
