"""Complete the compact router fixture for offline gate rehearsals (test helper, not a shipped script)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys

import yaml

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from asb_skill_collections import layout


def skill_metadata(index: list[dict], kb_bundle: dict) -> dict[str, dict]:
    """Return consistent synthetic gate metadata for each indexed skill."""
    metadata = {}
    for row in index:
        slug = row["slug"]
        doi = kb_bundle["skills"][slug]["dois"][0]
        metadata[slug] = {
            "license": "CC-BY-4.0",
            "evidence_spans": [{"doi": doi, "text": f"Synthetic fixture evidence for {slug}."}],
            "metadata": {
                "license_tier": row["license_tier"],
                "provenance_tier": "literature",
                "edam_topics": row["edam_topics"],
            },
        }
    return metadata


def update_leaf(path: Path, additions: dict) -> None:
    """Preserve a leaf's body and noncommercial acknowledgement block."""
    fence, frontmatter, body = path.read_text(encoding="utf-8").split("---\n", 2)
    document = yaml.safe_load(frontmatter)
    document["description"] = "Use when " + document["description"][0].lower() + document["description"][1:]
    metadata = dict(additions["metadata"])
    if "tool_license" in document.get("metadata", {}):
        metadata["tool_license"] = document["metadata"]["tool_license"]
    document.update(additions)
    document["metadata"] = metadata
    text = fence + "---\n" + yaml.safe_dump(document, sort_keys=False) + "---\n" + body
    path.write_text(text, encoding="utf-8")


def update_indexes(collection: Path) -> None:
    """Record DOI provenance and declared tool links in the copied indexes."""
    index_path = collection / "skills_index.json"
    kb_bundle = json.loads((collection / "kb_bundle.json").read_text(encoding="utf-8"))
    index = json.loads(index_path.read_text(encoding="utf-8"))
    additions = skill_metadata(index, kb_bundle)
    for row in index:
        slug = row["slug"]
        row["provenance_tier"] = "literature"
        row["dois"] = kb_bundle["skills"][slug]["dois"]
        row["tools_used"] = [tool.lower() for tool in row["tools"]]
        update_leaf(layout.leaf_dir(collection) / slug / "SKILL.md", additions[slug])
    index_path.write_text(json.dumps(index, indent=1) + "\n", encoding="utf-8")


def update_tools(collection: Path) -> None:
    """Give each synthetic tool a matching record and tool-licence evidence."""
    index_path = collection / "tools_index.json"
    tools = json.loads(index_path.read_text(encoding="utf-8"))
    evidence = {}
    records = collection / "tools"
    records.mkdir(exist_ok=True)
    for tool in tools:
        slug = tool["slug"]
        licence = "MIT" if tool["license_tier"] == "open" else "CC-BY-NC-4.0"
        tool.update(license=licence, license_detection="license-file", license_subject="tool", used_by_skills=[])
        evidence[slug] = {"license": licence}
        record = {"slug": slug, "name": tool["name"], "license_tier": tool["license_tier"]}
        (records / f"{slug}.yaml").write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
    index_path.write_text(json.dumps(tools, indent=1) + "\n", encoding="utf-8")
    (collection / "tool_licenses.json").write_text(json.dumps(evidence, indent=1) + "\n", encoding="utf-8")


def prepare(source: Path, destination: Path) -> Path:
    """Copy the source fixture and complete only its rehearsal metadata."""
    collection = destination / "collections" / "fixture" / "v1"
    collection.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, collection, dirs_exist_ok=True)
    update_indexes(collection)
    update_tools(collection)
    corpus_path = collection / "corpus.yaml"
    corpus = yaml.safe_load(corpus_path.read_text(encoding="utf-8"))
    for paper in corpus["papers"]:
        paper["license_tier"] = "open"
    corpus_path.write_text(yaml.safe_dump(corpus, sort_keys=False), encoding="utf-8")
    return collection


def main() -> int:
    """Materialize the rehearsal fixture at the requested destination."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    options = parser.parse_args()
    print(prepare(options.source, options.destination))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
