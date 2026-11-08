"""Regenerate ``catalogue.jsonld`` from the domain-release manifest.

The current catalogue supplies descriptive metadata (titles, topics, curators)
that is not duplicated in ``collections.yaml``. The manifest supplies release
membership, counts, dates, DOIs and leaf layout. Checkouts verify those counts
without becoming catalogue inputs.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

import yaml

# Invoked by path (`python scripts/x.py`), only `scripts/` lands on sys.path, so
# the repo root has to be added before the sibling package can be imported.
if __package__ in (None, ""):
    import os.path as _p

    sys.path.insert(0, _p.dirname(_p.dirname(_p.abspath(__file__))))

from scripts.check_collections_manifest import COUNTS, checkout_counts, parse_checkout  # noqa: E402

CATALOGUE_CONTEXT = {
    "@vocab": "https://schema.org/",
    "asb": "https://w3id.org/holobiomicslab/asb-skill/",
    "edam": "http://edamontology.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "collections": {"@id": "asb:collections", "@container": "@set"},
    "domain_topics": {"@id": "asb:domainTopics", "@type": "@id", "@container": "@set"},
    "lead_curators": {"@id": "asb:leadCurators", "@container": "@set"},
    "skills_count": {"@id": "asb:skillsCount", "@type": "xsd:integer"},
    "tools_count": {"@id": "asb:toolsCount", "@type": "xsd:integer"},
    "generated_at": {"@id": "asb:generatedAt", "@type": "xsd:dateTime"},
    "released_at": {"@id": "asb:releasedAt", "@type": "xsd:dateTime"},
    "slug": "asb:slug",
    "leaf_dir": "asb:leafDir",
    "status": "asb:status",
}
REGISTRY_ID = "https://w3id.org/holobiomicslab/asb-skill/registry"
MARKETPLACE = pathlib.Path(".claude-plugin") / "marketplace.json"
RELEASED = "released"
STAGED = "staged"
MINTED_DOI = re.compile(r"^10\.\d{4,9}/\S+$")


def is_minted_doi(doi: object) -> bool:
    """Return whether a value is a bare minted DOI."""
    return isinstance(doi, str) and bool(MINTED_DOI.fullmatch(doi.strip()))


def released_collection_dirs(repo_root: pathlib.Path) -> set[str]:
    """Retain local marketplace paths for older callers; ignore remote sources."""
    path = repo_root / MARKETPLACE
    if not path.is_file():
        return set()
    plugins = json.loads(path.read_text(encoding="utf-8")).get("plugins") or []
    sources = [plugin.get("source") for plugin in plugins if isinstance(plugin, dict)]
    return {
        pathlib.PurePosixPath(source.strip()).as_posix().removeprefix("./").rstrip("/")
        for source in sources
        if isinstance(source, str)
    }


def load_collections_manifest(repo_root: pathlib.Path) -> dict:
    """Load the optional registry for shared manifest consumers."""
    path = repo_root / "collections.yaml"
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as stream:
        manifest = yaml.safe_load(stream)
    return manifest if isinstance(manifest, dict) else {}


def require_collections_manifest(repo_root: pathlib.Path) -> dict:
    """Require a domains mapping when generating registry artifacts."""
    manifest = load_collections_manifest(repo_root)
    if not isinstance(manifest.get("domains"), dict):
        raise ValueError(f"manifest must contain a domains mapping: {repo_root / 'collections.yaml'}")
    return manifest


def manifest_release_dirs(repo_root: pathlib.Path) -> set[str]:
    """Return release paths for callers that classify existing catalogue rows."""
    return {
        release["path"]
        for _, release in iter_releases(load_collections_manifest(repo_root))
    }


def collection_status(
    rel_dir: str, released_dirs: set[str], manifest_dirs: set[str] = frozenset()
) -> str:
    """Classify a legacy path without using it for catalogue discovery."""
    return RELEASED if rel_dir in released_dirs | manifest_dirs else STAGED


def _template_entries(catalogue_path: pathlib.Path) -> dict[tuple[str, str], dict]:
    if not catalogue_path.is_file():
        return {}
    with catalogue_path.open(encoding="utf-8") as stream:
        catalogue = json.load(stream)
    return {
        (str(entry.get("slug")), str(entry.get("version"))): entry
        for entry in catalogue.get("collections", [])
        if isinstance(entry, dict)
    }


def _release_entry(slug: str, release: dict, template: dict) -> dict:
    version = str(release["version"])
    entry = dict(template)
    entry["@id"] = template.get(
        "@id",
        f"https://w3id.org/holobiomicslab/asb-skill/collection/{slug}/v{version}",
    )
    entry.setdefault("title", f"ASB {slug.title()} Skill Collection v{version}")
    entry.update(
        version=version,
        slug=slug,
        skills_count=release["skills"],
        tools_count=release["tools"],
        leaf_dir=release.get("leaf_dir", "leaves"),
        status=STAGED if release.get("status") == "legacy" else RELEASED,
    )
    entry.setdefault("domain_topics", [])
    entry.setdefault("lead_curators", [])
    if release.get("released") is not None:
        released = str(release["released"])
        # The manifest records a date; keep the template's full timestamp when
        # it falls on that date, so a regeneration does not rewrite it.
        current = str(template.get("released_at", ""))
        entry["released_at"] = (
            current
            if current.startswith(released) and len(current) > len(released)
            else f"{released}T00:00:00Z"
        )
    doi = release.get("version_doi")
    if is_minted_doi(doi):
        entry["doi"] = doi.strip()
    else:
        entry.pop("doi", None)
    return entry


def iter_releases(manifest: dict) -> list[tuple[str, dict]]:
    """Return releases in deterministic domain/version order."""
    releases = [
        (slug, release)
        for slug, domain in manifest["domains"].items()
        for release in domain.get("releases", [])
    ]
    return sorted(releases, key=lambda item: (item[0], str(item[1]["version"])))


def build_catalogue(
    repo_root: pathlib.Path,
) -> dict:
    """Build one catalogue entry per manifest release."""
    manifest = require_collections_manifest(repo_root)
    templates = _template_entries(repo_root / "catalogue.jsonld")
    entries = []
    for slug, release in iter_releases(manifest):
        key = (slug, str(release["version"]))
        entries.append(_release_entry(slug, release, templates.get(key, {})))
    return {
        "@context": CATALOGUE_CONTEXT,
        "@type": "asb:SkillCollectionRegistry",
        "@id": REGISTRY_ID,
        "name": "ASB Skill Collection Registry",
        "description": (
            "Auto-generated registry of the ASB Skill Collections in the domain "
            "repositories. Each entry's status says whether it is released or staged."
        ),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "collections": entries,
    }


def verify_checkouts(manifest: dict, checkouts: dict[str, pathlib.Path]) -> list[str]:
    """Compare all four release counts with each supplied domain checkout."""
    failures = []
    for slug, release in iter_releases(manifest):
        checkout = checkouts.get(slug)
        if checkout is None:
            continue
        label = f"{slug}/v{release['version']}"
        try:
            actual = checkout_counts(checkout / release["path"])
        except (OSError, KeyError, TypeError, ValueError, yaml.YAMLError) as error:
            failures.append(f"{label}: checkout validation failed: {error}")
            continue
        failures.extend(
            f"{label}: checkout {key} expected {release[key]} got {actual[key]}"
            for key in COUNTS
            if actual[key] != release[key]
        )
    return failures


def write_catalogue(catalogue: dict, output_path: pathlib.Path) -> None:
    """Write stable, human-readable JSON-LD."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(catalogue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    """Regenerate the catalogue or refuse inconsistent checkouts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="Tooling repository root")
    parser.add_argument("--output", default="catalogue.jsonld")
    parser.add_argument(
        "--checkout",
        action="append",
        type=parse_checkout,
        default=[],
        metavar="SLUG=PATH",
        help="Verify release counts against a domain checkout; repeatable",
    )
    arguments = parser.parse_args(argv)
    repo_root = pathlib.Path(arguments.repo_root).resolve()
    checkouts = dict(arguments.checkout)
    if len(checkouts) != len(arguments.checkout):
        print("usage: each --checkout slug must be unique", file=sys.stderr)
        return 2
    try:
        manifest = require_collections_manifest(repo_root)
        failures = verify_checkouts(manifest, checkouts)
    except (OSError, ValueError, TypeError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f"catalogue: {error}", file=sys.stderr)
        return 1
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    output_path = pathlib.Path(arguments.output)
    if not output_path.is_absolute():
        output_path = repo_root / output_path
    catalogue = build_catalogue(repo_root)
    write_catalogue(catalogue, output_path)
    count = len(catalogue["collections"])
    print(f"catalogue.jsonld written to {output_path} ({count} collections)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
