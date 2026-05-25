"""
Generate HuggingFace Dataset card README.md from collection.yaml + CITATION.cff.

Usage:
    python scripts/generate_hf_dataset_card.py \\
        --collection collections/metabolomics/v1/collection.yaml \\
        [--citation collections/metabolomics/v1/CITATION.cff] \\
        [--output collections/metabolomics/v1/hf_README.md]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

import yaml


REQUIRED_COLLECTION_KEYS = {"title", "slug", "version", "domain"}


def parse_collection_yaml(text: str) -> dict:
    """Parse collection.yaml text. Raises ValueError if required keys missing."""
    data = yaml.safe_load(text)
    if not data:
        raise ValueError("Empty collection YAML")
    missing = REQUIRED_COLLECTION_KEYS - set(data.keys())
    if missing:
        raise ValueError(f"collection.yaml missing required keys: {missing}")
    return data


def parse_citation_cff(text: str) -> dict:
    """Parse CITATION.cff text. Returns dict (may be empty on parse error)."""
    try:
        return yaml.safe_load(text) or {}
    except yaml.YAMLError:
        return {}


def generate_readme(collection: dict, citation: Optional[dict]) -> str:
    """
    Generate the full HF Dataset card README.md content.

    Parameters
    ----------
    collection : dict
        Parsed collection.yaml (must contain title, slug, version, domain).
    citation : dict or None
        Parsed CITATION.cff (may be None or empty).

    Returns
    -------
    str
        Full README.md content (YAML frontmatter + body).
    """
    title = collection["title"]
    slug = collection["slug"]
    version = collection["version"]
    domain = str(collection["domain"]).lower()
    description = collection.get("description", "")

    doi = "PLACEHOLDER"
    if citation:
        doi = citation.get("doi", "PLACEHOLDER") or "PLACEHOLDER"

    pretty_name = f"ASB {title} Benchmark v{version}"

    tags = ["agentic-ai", "scientific-agents", domain, "asb"]
    tags_str = "[" + ", ".join(tags) + "]"

    frontmatter = f"""---
license: apache-2.0
tags: {tags_str}
task_categories: [text-generation, question-answering]
size_categories: [n<1K]
language: [en]
pretty_name: "{pretty_name}"
configs:
  - config_name: skills
    data_files: "skills/**/SKILL.md"
  - config_name: benchmark
    data_files: "benchmark/tasks/**/task.md"
  - config_name: tools
    data_files: "tools/**/*.yaml"
homepage: "https://github.com/HolobiomicsLab/asb-skill-collections"
doi: "{doi}"
---"""

    body = f"""
# {pretty_name}

{description}

## Programmatic access

```python
from datasets import load_dataset

ds_skills = load_dataset("HolobiomicsLab/asb-{slug}-v{version}", "skills")
ds_bench  = load_dataset("HolobiomicsLab/asb-{slug}-v{version}", "benchmark")
ds_tools  = load_dataset("HolobiomicsLab/asb-{slug}-v{version}", "tools")
```

## Citation

If you use this dataset in research, please cite using the DOI above.
See `CITATION.cff` in the source repository for the full citation.

## License

Apache-2.0 for synthesis layer; fair-use for verbatim paper quotes.
"""

    return frontmatter + "\n" + body


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", required=True, help="Path to collection.yaml")
    parser.add_argument("--citation", default=None, help="Path to CITATION.cff (optional)")
    parser.add_argument("--output", default=None, help="Output path (default: stdout)")
    args = parser.parse_args(argv)

    collection_path = Path(args.collection)
    if not collection_path.exists():
        print(f"ERROR: collection.yaml not found: {collection_path}", file=sys.stderr)
        return 1

    collection = parse_collection_yaml(collection_path.read_text())

    citation = None
    if args.citation:
        cit_path = Path(args.citation)
        if cit_path.exists():
            citation = parse_citation_cff(cit_path.read_text())

    readme = generate_readme(collection=collection, citation=citation)

    if args.output:
        Path(args.output).write_text(readme)
        print(f"Written to {args.output}")
    else:
        print(readme)

    return 0


if __name__ == "__main__":
    sys.exit(main())
