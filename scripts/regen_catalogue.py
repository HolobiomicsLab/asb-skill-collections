"""
Regenerate catalogue.jsonld at the repo root by walking collections/ directory.

JSON-LD schema: @type SkillCollectionRegistry (LinkML class from asb-schema).
Each collection entry carries: @id (w3id IRI), title, version, slug, domain_topics
(EDAM IRIs), doi, released_at, skills_count, tools_count, lead_curators[].

Output is deterministic: collections sorted alphabetically by slug; timestamps
are UTC ISO 8601 with Z suffix.

Usage:
    python scripts/regen_catalogue.py [--repo-root .] [--output catalogue.jsonld]
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

import yaml


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
}

REGISTRY_ID = "https://w3id.org/holobiomicslab/asb-skill/registry"


def _load_collection_yaml(path: pathlib.Path) -> dict:
    """Load and return a collection.yaml, raising ValueError on bad content."""
    with open(path) as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected dict in {path}, got {type(data)}")
    return data


def _collection_entry(col_yaml: dict) -> dict:
    """Convert a collection.yaml dict to a catalogue entry dict."""
    entry: dict = {}

    # @id: use explicit or construct from slug + version
    iri = col_yaml.get("@id")
    if not iri:
        slug = col_yaml.get("slug", "")
        version = col_yaml.get("version", "")
        iri = f"https://w3id.org/holobiomicslab/asb-skill/collection/{slug}/v{version}"
    entry["@id"] = iri

    # Required fields
    entry["title"] = col_yaml.get("title", "")
    entry["version"] = str(col_yaml.get("version", ""))
    entry["slug"] = col_yaml.get("slug", "")
    entry["skills_count"] = int(col_yaml.get("skills_count", 0))
    entry["tools_count"] = int(col_yaml.get("tools_count", 0))

    # Optional fields
    domain_topics = col_yaml.get("domain_topics") or []
    entry["domain_topics"] = list(domain_topics)

    doi = col_yaml.get("doi")
    if doi:
        entry["doi"] = doi

    released_at = col_yaml.get("released_at")
    if released_at:
        entry["released_at"] = str(released_at)

    lead_curators = col_yaml.get("lead_curators") or []
    entry["lead_curators"] = list(lead_curators)

    return entry


def build_catalogue(repo_root: pathlib.Path) -> dict:
    """
    Walk repo_root/collections/ and build a catalogue dict.

    Args:
        repo_root: Path to the repository root.

    Returns:
        A dict suitable for serialisation as JSON-LD.
    """
    collections_dir = repo_root / "collections"
    entries: list[dict] = []

    if collections_dir.exists():
        # Walk all collection.yaml files: collections/<slug>/v<N>/collection.yaml
        for col_yaml_path in sorted(collections_dir.glob("**/collection.yaml")):
            try:
                col_data = _load_collection_yaml(col_yaml_path)
                entry = _collection_entry(col_data)
                entries.append(entry)
            except Exception as exc:
                print(
                    f"WARNING: skipping {col_yaml_path}: {exc}",
                    file=sys.stderr,
                )

    # Sort deterministically by slug
    entries.sort(key=lambda e: (e.get("slug", ""), e.get("version", "")))

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "@context": CATALOGUE_CONTEXT,
        "@type": "asb:SkillCollectionRegistry",
        "@id": REGISTRY_ID,
        "name": "ASB Skill Collection Registry",
        "description": (
            "Auto-generated registry of all released ASB Skill Collections."
        ),
        "generated_at": now_utc,
        "collections": entries,
    }


def write_catalogue(catalogue: dict, output_path: pathlib.Path) -> None:
    """Serialise catalogue dict to JSON-LD at output_path (deterministic, 2-space indent)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(catalogue, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regenerate catalogue.jsonld from collections/ directory."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path to the repository root (default: current directory)",
    )
    parser.add_argument(
        "--output",
        default="catalogue.jsonld",
        help="Output path for catalogue.jsonld (default: catalogue.jsonld)",
    )
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    output_path = pathlib.Path(args.output)
    if not output_path.is_absolute():
        output_path = repo_root / output_path

    catalogue = build_catalogue(repo_root)
    write_catalogue(catalogue, output_path)

    count = len(catalogue["collections"])
    print(
        f"catalogue.jsonld written to {output_path} "
        f"({count} collection{'s' if count != 1 else ''})"
    )


if __name__ == "__main__":
    main()
