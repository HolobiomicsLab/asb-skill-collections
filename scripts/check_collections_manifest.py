"""Validate domain-release manifests, catalogue entries, and local checkouts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

SCHEMA = "asb-collections-manifest/1"
COUNTS = ("skills", "tools", "workflows", "papers")
CATALOGUE_COUNTS = {count: f"{count}_count" for count in COUNTS}
REQUIRED_RELEASE_KEYS = {
    "version",
    "path",
    "tag",
    "commit",
    "source_commit",
    "tree_digest",
    "version_doi",
    "released",
    *COUNTS,
}
DOI_PATTERN = re.compile(r"^10\.5281/zenodo\.\d+$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SUPERSEDED_KEYS = {"tag", "commit", "tree_digest", "version_doi", "released"}
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
CAPSULES_COUNTS = (
    "builds_packed", "builds_left_out", "builds_not_released", "capsules",
    "benchmark_capsules", "archive_bytes",
)
CAPSULES_KEYS = {
    "version_doi", "concept_doi", "record_id", "supplements", "archive_sha256",
    "published", *CAPSULES_COUNTS,
}


def compute_tree_digest(repository: Path, release_path: str) -> str:
    """Hash sorted digest/path lines for regular files below a release tree."""
    root = repository.resolve()
    if not root.is_dir():
        raise ValueError(f"checkout is not a directory: {repository}")
    collection = (root / release_path).resolve()
    if root != collection and root not in collection.parents:
        raise ValueError(f"release path escapes checkout: {release_path}")
    if not collection.is_dir():
        raise ValueError(f"release path is not a directory: {release_path}")
    lines = []
    for directory, dirnames, filenames in os.walk(collection, followlinks=False):
        parent = Path(directory)
        dirnames[:] = [name for name in dirnames if not (parent / name).is_symlink()]
        for filename in filenames:
            path = parent / filename
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                continue
            if not stat.S_ISREG(mode):
                continue
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            relative = path.relative_to(root).as_posix()
            lines.append(f"{digest.hexdigest()}  {relative}\n")
    return "sha256:" + hashlib.sha256("".join(sorted(lines)).encode()).hexdigest()


def git_tree_digest(repository: Path, commit: str, release_path: str) -> str:
    """Hash the release tree as committed at ``commit``, read from git objects.

    The lines are those of ``compute_tree_digest``: regular blobs only, symbolic
    links (mode 120000) and submodules excluded, paths relative to the repository
    root. A clean checkout of ``commit`` gives the same digest from the filesystem.
    """
    root = repository.resolve()
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "-z", "--full-tree", commit, "--", release_path],
        cwd=root, capture_output=True, check=False,
    )
    if listing.returncode:
        raise ValueError(
            f"cannot list {release_path} at {commit}: {listing.stderr.decode(errors='replace').strip()}"
        )
    entries = []
    for record in listing.stdout.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, kind, oid = meta.split()
        if kind != b"blob" or mode == b"120000":
            continue
        entries.append((oid.decode(), path.decode("utf-8")))
    if not entries:
        raise ValueError(f"release path has no files at {commit}: {release_path}")
    batch = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    )
    lines = []
    try:
        for oid, path in entries:
            batch.stdin.write(oid.encode() + b"\n")
            batch.stdin.flush()
            header = batch.stdout.readline().split()
            if len(header) != 3 or header[1] != b"blob":
                raise ValueError(f"cannot read blob {oid} for {path}")
            data = batch.stdout.read(int(header[2]))
            batch.stdout.read(1)
            lines.append(f"{hashlib.sha256(data).hexdigest()}  {path}\n")
    finally:
        batch.stdin.close()
        batch.wait()
    return "sha256:" + hashlib.sha256("".join(sorted(lines)).encode()).hexdigest()


def release_path_drift(repository: Path, commit: str, release_path: str) -> list[str]:
    """List paths under ``release_path`` whose checkout bytes are not those of ``commit``.

    Covers tracked files that differ from ``commit`` (staged or not) and every
    untracked file, ignored ones included, since the filesystem digest and the
    release counts would read them.
    """
    root = repository.resolve()
    drift = []
    for command in (
        ["git", "diff", "--name-only", "-z", commit, "--", release_path],
        ["git", "ls-files", "--others", "-z", "--", release_path],
    ):
        result = subprocess.run(command, cwd=root, capture_output=True, check=False)
        if result.returncode:
            raise ValueError(
                f"cannot compare {release_path} with {commit}: "
                f"{result.stderr.decode(errors='replace').strip()}"
            )
        drift.extend(name.decode("utf-8") for name in result.stdout.split(b"\0") if name)
    return sorted(set(drift))


def checkout_counts(collection: Path) -> dict[str, int]:
    """Read release totals from the collection indexes and source corpus.

    A router-shaped release carries ``skills_index.json``, ``tools_index.json``
    and ``workflows/workflows_index.json``. A legacy tree (the v1 collections)
    has none of them: its skills are the ``SKILL.md`` files under ``skills/``,
    its tools the YAML files under ``tools/``, and it ships no workflows.
    """
    skills_index = collection / "skills_index.json"
    if skills_index.is_file():
        with skills_index.open(encoding="utf-8") as stream:
            skills = len(json.load(stream))
    else:
        skills = sum(1 for _ in (collection / "skills").rglob("SKILL.md"))
    tools_index = collection / "tools_index.json"
    if tools_index.is_file():
        with tools_index.open(encoding="utf-8") as stream:
            tools = len(json.load(stream))
    else:
        tools = len(list((collection / "tools").glob("*.yaml")))
    workflows_index = collection / "workflows" / "workflows_index.json"
    if workflows_index.is_file():
        with workflows_index.open(encoding="utf-8") as stream:
            workflows = len(json.load(stream))
    else:
        workflows = 0
    with (collection / "corpus.yaml").open(encoding="utf-8") as stream:
        corpus = yaml.safe_load(stream)
    return {
        "skills": skills,
        "tools": tools,
        "workflows": workflows,
        "papers": len(corpus["papers"]),
    }


def load_json(path: Path) -> Any:
    """Load JSON with a consistent UTF-8 contract."""
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def catalogue_entries(path: Path) -> dict[tuple[str, str], dict]:
    """Index catalogue collection entries by domain slug and string version."""
    catalogue = load_json(path)
    return {
        (str(entry.get("slug")), str(entry.get("version"))): entry
        for entry in catalogue.get("collections", [])
        if isinstance(entry, dict)
    }


def validate_release(
    slug: str, release: Any, entries: dict, checkout: Path | None
) -> list[str]:
    """Return every disagreement found for one domain release."""
    label = f"{slug}/v{release.get('version', '?') if isinstance(release, dict) else '?'}"
    if not isinstance(release, dict):
        return [f"{label}: release must be a mapping"]
    failures = []
    status = release.get("status")
    is_legacy = status == "legacy"
    if status is not None and not is_legacy:
        failures.append(f"{label}: invalid status {status!r}")
    release_path = release.get("path")
    if (
        not isinstance(release_path, str)
        or not release_path
        or Path(release_path).is_absolute()
        or ".." in Path(release_path).parts
    ):
        failures.append(f"{label}: invalid relative path {release_path!r}")
    failures.extend(
        f"{label}: missing required key {key}"
        for key in sorted(REQUIRED_RELEASE_KEYS - release.keys())
    )
    if is_legacy:
        for key in ("tag", "version_doi"):
            if release.get(key) is not None:
                failures.append(f"{label}: legacy {key} must be null")
    else:
        if release.get("tag") is not None and (
            not isinstance(release["tag"], str) or not release["tag"]
        ):
            failures.append(f"{label}: invalid tag {release.get('tag')!r}")
        if not DOI_PATTERN.fullmatch(str(release.get("version_doi", ""))):
            failures.append(
                f"{label}: invalid version_doi {release.get('version_doi')!r}"
            )
    if not COMMIT_PATTERN.fullmatch(str(release.get("commit", ""))):
        failures.append(f"{label}: invalid commit {release.get('commit')!r}")
    if not DIGEST_PATTERN.fullmatch(str(release.get("tree_digest", ""))):
        failures.append(f"{label}: invalid tree_digest {release.get('tree_digest')!r}")
    failures.extend(validate_counts(label, release))
    failures.extend(validate_superseded(label, release))
    failures.extend(validate_capsules(label, release))
    failures.extend(validate_catalogue(label, release, entries))
    if checkout is not None:
        failures.extend(validate_checkout(label, release, checkout))
    return failures


def validate_counts(label: str, release: dict) -> list[str]:
    """Require integer, non-negative release totals."""
    return [
        f"{label}: invalid {key} count {release.get(key)!r}"
        for key in COUNTS
        if not isinstance(release.get(key), int)
        or isinstance(release.get(key), bool)
        or release[key] < 0
    ]


def validate_superseded(label: str, release: dict) -> list[str]:
    """Check the optional trace of earlier releases of the same major version.

    A patch release (for example v3.0.1 after v3.0.0) replaces the row's tag,
    commit, digest, DOI and date; the replaced values stay listed here.
    """
    if "superseded" not in release:
        return []
    superseded = release["superseded"]
    if not isinstance(superseded, list) or not superseded:
        return [f"{label}: superseded must be a non-empty list"]
    failures = []
    tags = []
    for index, entry in enumerate(superseded):
        where = f"{label}: superseded[{index}]"
        if not isinstance(entry, dict):
            failures.append(f"{where} must be a mapping")
            continue
        if set(entry) != SUPERSEDED_KEYS:
            failures.append(f"{where} keys must be {', '.join(sorted(SUPERSEDED_KEYS))}")
        tag = entry.get("tag")
        if not isinstance(tag, str) or not tag:
            failures.append(f"{where}: invalid tag {tag!r}")
        tags.append(tag)
        if not COMMIT_PATTERN.fullmatch(str(entry.get("commit", ""))):
            failures.append(f"{where}: invalid commit {entry.get('commit')!r}")
        if not DIGEST_PATTERN.fullmatch(str(entry.get("tree_digest", ""))):
            failures.append(f"{where}: invalid tree_digest {entry.get('tree_digest')!r}")
        if not DOI_PATTERN.fullmatch(str(entry.get("version_doi", ""))):
            failures.append(f"{where}: invalid version_doi {entry.get('version_doi')!r}")
        if not DATE_PATTERN.fullmatch(str(entry.get("released", ""))):
            failures.append(f"{where}: invalid released {entry.get('released')!r}")
    if release.get("tag") in tags:
        failures.append(f"{label}: superseded repeats the current tag {release.get('tag')!r}")
    if len(tags) != len(set(map(str, tags))):
        failures.append(f"{label}: superseded tags must be unique")
    return failures


def validate_capsules(label: str, release: dict) -> list[str]:
    """Check the optional block of the published build-capsules record of a release.

    `scripts/capsules_deposit.py record-doi` writes it. `supplements` names the
    collection version DOI the record supplements: the row's DOI or a superseded one.
    """
    if "capsules" not in release:
        return []
    block = release["capsules"]
    where = f"{label}: capsules"
    if not isinstance(block, dict):
        return [f"{where} must be a mapping"]
    failures = []
    if set(block) != CAPSULES_KEYS:
        failures.append(f"{where} keys must be {', '.join(sorted(CAPSULES_KEYS))}")
    for key in ("version_doi", "concept_doi", "supplements"):
        if not DOI_PATTERN.fullmatch(str(block.get(key, ""))):
            failures.append(f"{where}: invalid {key} {block.get(key)!r}")
    if str(block.get("version_doi")).rsplit(".", 1)[-1] != str(block.get("record_id")):
        failures.append(f"{where}: record_id {block.get('record_id')!r} is not the record of {block.get('version_doi')!r}")
    supplemented = [release.get("version_doi")] + [
        entry.get("version_doi") for entry in release.get("superseded") or [] if isinstance(entry, dict)
    ]
    if block.get("supplements") not in supplemented:
        failures.append(f"{where}: supplements {block.get('supplements')!r} is not a version DOI of this row")
    failures.extend(
        f"{where}: invalid {key} {block.get(key)!r}" for key in CAPSULES_COUNTS
        if not isinstance(block.get(key), int) or isinstance(block.get(key), bool) or block[key] < 0
    )
    if not SHA256_PATTERN.fullmatch(str(block.get("archive_sha256", ""))):
        failures.append(f"{where}: invalid archive_sha256 {block.get('archive_sha256')!r}")
    if not DATE_PATTERN.fullmatch(str(block.get("published", ""))):
        failures.append(f"{where}: invalid published {block.get('published')!r}")
    return failures


def validate_catalogue(label: str, release: dict, entries: dict) -> list[str]:
    """Compare the release DOI and shared count fields with the catalogue."""
    key = (str(release.get("slug", label.split("/")[0])), str(release.get("version")))
    entry = entries.get(key)
    if entry is None:
        return [f"{label}: catalogue entry missing"]
    failures = []
    is_legacy = release.get("status") == "legacy"
    if is_legacy and not entry.get("doi"):
        pass
    elif entry.get("doi") != release.get("version_doi"):
        failures.append(
            f"{label}: catalogue doi {entry.get('doi')!r} != {release.get('version_doi')!r}"
        )
    for count, catalogue_key in CATALOGUE_COUNTS.items():
        if entry.get(catalogue_key) != release.get(count):
            failures.append(
                f"{label}: catalogue {catalogue_key} {entry.get(catalogue_key)!r} "
                f"!= {release.get(count)!r}"
            )
    return failures


def validate_checkout(label: str, release: dict, checkout: Path) -> list[str]:
    """Recompute the release digest and totals from a domain checkout."""
    release_path = release.get("path")
    if (
        not isinstance(release_path, str)
        or not release_path
        or Path(release_path).is_absolute()
        or ".." in Path(release_path).parts
    ):
        return []
    collection = checkout / release_path
    try:
        digest = compute_tree_digest(checkout, release_path)
        actual = checkout_counts(collection)
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        json.JSONDecodeError,
        yaml.YAMLError,
    ) as error:
        return [f"{label}: checkout validation failed: {error}"]
    failures = []
    if digest != release.get("tree_digest"):
        failures.append(
            f"{label}: tree_digest expected {release.get('tree_digest')} got {digest}"
        )
    for key in COUNTS:
        if actual[key] != release.get(key):
            failures.append(
                f"{label}: checkout {key} expected {release.get(key)} got {actual[key]}"
            )
    return failures


def audit(manifest_path: Path, catalogue_path: Path, checkouts: dict[str, Path]) -> list[str]:
    """Validate a manifest and return human-readable disagreement lines."""
    with manifest_path.open(encoding="utf-8") as stream:
        manifest = yaml.safe_load(stream)
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        return [f"manifest: schema must be {SCHEMA}"]
    domains = manifest.get("domains")
    if not isinstance(domains, dict):
        return ["manifest: domains must be a mapping"]
    entries = catalogue_entries(catalogue_path)
    failures = []
    for slug, domain in domains.items():
        failures.extend(validate_domain(slug, domain, entries, checkouts.get(slug)))
    return failures


def validate_domain(
    slug: str, domain: Any, entries: dict, checkout: Path | None
) -> list[str]:
    """Validate domain metadata and every declared release."""
    if not isinstance(domain, dict):
        return [f"{slug}: domain must be a mapping"]
    failures = []
    if not domain.get("repository"):
        failures.append(f"{slug}: missing repository")
    releases = domain.get("releases")
    all_legacy = isinstance(releases, list) and bool(releases) and all(
        isinstance(release, dict) and release.get("status") == "legacy"
        for release in releases
    )
    if domain.get("concept_doi") is None and all_legacy:
        pass  # a domain with only legacy releases has no Zenodo lineage yet
    elif not DOI_PATTERN.fullmatch(str(domain.get("concept_doi", ""))):
        failures.append(f"{slug}: invalid concept_doi {domain.get('concept_doi')!r}")
    releases = domain.get("releases")
    if not isinstance(releases, list) or not releases:
        return failures + [f"{slug}: releases must be a non-empty list"]
    for release in releases:
        failures.extend(validate_release(slug, release, entries, checkout))
    return failures


def release_summaries(manifest_path: Path, checkouts: dict[str, Path]) -> list[str]:
    """Format one success summary per release after a clean audit."""
    with manifest_path.open(encoding="utf-8") as stream:
        manifest = yaml.safe_load(stream)
    summaries = []
    for slug, domain in manifest["domains"].items():
        for release in domain["releases"]:
            counts = " ".join(f"{key}={release[key]}" for key in COUNTS)
            verified = "tree=verified" if slug in checkouts else "catalogue=verified"
            summaries.append(f"OK {slug}/v{release['version']}: {counts} {verified}")
    return summaries


def parse_checkout(value: str) -> tuple[str, Path]:
    """Parse a repeatable slug=path checkout argument."""
    slug, separator, path = value.partition("=")
    if not separator or not slug or not path:
        raise argparse.ArgumentTypeError("expected <slug>=<path>")
    return slug, Path(path).resolve()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line options without accessing the network or Git."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("collections.yaml"))
    parser.add_argument("--catalogue", type=Path)
    parser.add_argument("--checkout", action="append", type=parse_checkout, default=[])
    arguments = parser.parse_args(argv)
    if arguments.catalogue is None:
        arguments.catalogue = arguments.manifest.parent / "catalogue.jsonld"
    return arguments


def main(argv: list[str] | None = None) -> int:
    """Print every disagreement, or one summary per validated release."""
    arguments = parse_args(argv)
    checkouts = dict(arguments.checkout)
    if len(checkouts) != len(arguments.checkout):
        print("usage: each --checkout slug must be unique")
        return 2
    try:
        failures = audit(arguments.manifest, arguments.catalogue, checkouts)
    except (OSError, ValueError, TypeError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f"manifest: validation failed: {error}")
        return 1
    if failures:
        print("\n".join(failures))
        return 1
    print("\n".join(release_summaries(arguments.manifest, checkouts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
