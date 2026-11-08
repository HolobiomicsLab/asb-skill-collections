"""Validate domain-release manifests, catalogue entries, and local checkouts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

import yaml

SCHEMA = "asb-collections-manifest/1"
COUNTS = ("skills", "tools", "workflows", "papers")
CATALOGUE_COUNTS = {"skills": "skills_count", "tools": "tools_count"}
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


def checkout_counts(collection: Path) -> dict[str, int]:
    """Read release totals from the collection indexes and source corpus."""
    with (collection / "skills_index.json").open(encoding="utf-8") as stream:
        skills = json.load(stream)
    with (collection / "tools_index.json").open(encoding="utf-8") as stream:
        tools = json.load(stream)
    with (collection / "workflows" / "workflows_index.json").open(
        encoding="utf-8"
    ) as stream:
        workflows = json.load(stream)
    with (collection / "corpus.yaml").open(encoding="utf-8") as stream:
        corpus = yaml.safe_load(stream)
    return {
        "skills": len(skills),
        "tools": len(tools),
        "workflows": len(workflows),
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
    if not DOI_PATTERN.fullmatch(str(domain.get("concept_doi", ""))):
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
