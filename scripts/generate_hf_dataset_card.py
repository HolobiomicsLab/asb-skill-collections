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


def _cff_to_bibtex(cff: dict, slug: str, version) -> str:
    """Render a minimal BibTeX @misc entry from CITATION.cff fields."""
    authors = []
    for a in (cff.get("authors") or []):
        if not isinstance(a, dict):
            continue
        if a.get("family-names"):
            authors.append(f"{a['family-names']}, {a.get('given-names', '')}".strip().rstrip(','))
        elif a.get("name"):
            authors.append("{" + str(a["name"]) + "}")
    author_str = " and ".join(authors) if authors else "{Holobiomics Lab}"
    title = cff.get("title", f"ASB Skill Collection: {slug}")
    # date-released may parse as a datetime.date (PyYAML) or a string;
    # normalise to a YYYY-MM-DD string before split.
    _dr = cff.get("date-released") or ""
    year = str(_dr).split("-")[0] if _dr else "2026"
    doi = cff.get("doi") or ""
    cite_key = f"asb{slug.replace('-', '')}v{version}"
    lines = [
        f"@misc{{{cite_key},",
        f"  author = {{{author_str}}},",
        f"  title  = {{{title}}},",
        f"  year   = {{{year}}},",
    ]
    if doi:
        lines.append(f"  doi    = {{{doi}}},")
        lines.append(f"  url    = {{https://doi.org/{doi}}},")
    lines.append(f"  note   = {{HuggingFace dataset: HolobiomicsLab/asb-{slug}-v{version}}},")
    lines.append("}")
    return "\n".join(lines)


def _size_category(n_items: int) -> str:
    """HF size category bin per https://huggingface.co/docs/hub/datasets-cards."""
    if n_items < 1000:        return "n<1K"
    if n_items < 10_000:      return "1K<n<10K"
    if n_items < 100_000:     return "10K<n<100K"
    if n_items < 1_000_000:   return "100K<n<1M"
    return "1M<n<10M"


def generate_readme(
    collection: dict,
    citation: Optional[dict],
    *,
    n_skills: int = 0,
    n_tasks: int = 0,
    n_tools: int = 0,
    n_papers: int = 0,
) -> str:
    """
    Generate the full HF Dataset card README.md content.

    Adheres to the HuggingFace dataset card best-practices at
    https://huggingface.co/docs/hub/datasets-cards — includes all five
    canonical H2 sections (Dataset Description, Structure, Creation,
    Considerations for Using the Data, Additional Information) plus a
    real BibTeX citation rendered from CITATION.cff.

    Parameters
    ----------
    collection : dict
        Parsed collection.yaml (must contain title, slug, version, domain).
    citation : dict or None
        Parsed CITATION.cff (may be None or empty).
    n_skills, n_tasks, n_tools, n_papers : int
        Item counts used for size_categories + dataset-structure description.

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

    tags = ["agentic-ai", "scientific-agents", domain, "asb",
            "skill-collection", "claude-code-plugin"]
    tags_str = "[" + ", ".join(tags) + "]"

    total_items = n_skills + n_tasks + n_tools
    size_cat = _size_category(total_items if total_items > 0 else 100)

    bibtex = _cff_to_bibtex(citation or {}, slug, version) if citation else ""

    frontmatter = f"""---
license: apache-2.0
tags: {tags_str}
task_categories: [text-generation, question-answering]
size_categories: [{size_cat}]
language: [en]
pretty_name: "{pretty_name}"
annotations_creators: [machine-generated, expert-generated]
language_creators: [expert-generated]
multilinguality: [monolingual]
source_datasets: [original]
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

## Dataset Description

- **Curated by:** Holobiomics Lab (CNRS / Université Côte d'Azur)
- **Funded by:** Holobiomics Lab
- **Shared by:** Holobiomics Lab
- **Language(s) (NLP):** English (en)
- **License:** Apache-2.0 (synthesis layer); fair-use for verbatim paper quotes

This dataset is a curated, evidence-grounded scientific-agent skill + tool +
benchmark collection for the **{domain}** domain. It is produced by the
[AgenticScienceBuilder (ASB)](https://github.com/HolobiomicsLab/AgenticScienceBuilder)
pipeline from peer-reviewed source papers, then human-reviewed by Lead Curators
before release.

### Supported Tasks

- `text-generation`: agent-style skill loading + invocation
- `question-answering`: claim verification benchmark (silver + gold tiers)

### Languages

English (en). Source papers are likewise English.

## Dataset Structure

### Configs

- `skills` — {n_skills} curated, deduplicated procedural skills with EDAM annotations
- `benchmark` — {n_tasks} per-paper tasks + claim-retrieval test sets
- `tools` — {n_tools} third-party software-tool records with SPDX licensing

### Data Fields

Each skill (`SKILL.md`) carries YAML frontmatter:
- `name`, `description`, `when_to_use_negative`
- `edam_operation` / `edam_topics` (ontology-grounded retrieval keys)
- `provenance.source_papers[]` (DOIs back to source articles)
- `provenance.generated_by` (LLM model + prompt_version + seed + ASB version)
- `evidence_spans` (verbatim quotes from source papers, sanitized per access tier)
- `tools` (linked tool records)

Tool records carry: `slug`, `name`, `canonical_url`, `license_spdx`,
`install` recipe, `source_paper_doi`, `evidence_spans`. Full SBOM at
`sbom.cdx.json` (CycloneDX 1.5 format).

### Data Splits

This dataset is not split — it is a single curated artifact. The claim-retrieval
benchmark inside the `benchmark` config does have a silver-tier vs gold-tier
distinction; see `benchmark/claims/per_paper/<doi>/ground_truth.jsonl` (silver)
and `.../gold/ground_truth.jsonl` (gold).

## Dataset Creation

### Curation Rationale

This collection exists to give scientific AI agents access to curated,
evidence-grounded procedural knowledge with full DOI provenance, EDAM ontology
annotations, and a reproducible benchmark for evaluation. The curation goal is
**not coverage** but **quality + traceability**.

### Source Data

Source papers are peer-reviewed and listed in the collection's `corpus.yaml`
ledger ({n_papers} papers, included + excluded). Each paper's access tier
(open-access / hybrid / closed) is verified via Unpaywall + Crossref.

#### Initial Data Collection and Normalization

Source papers are processed by AgenticScienceBuilder, which extracts
SciTask Cards + SciSkill bundles via a multi-agent LLM pipeline. See the
ASB repo for the full pipeline architecture.

#### Who are the source language producers?

The original authors of each cited source paper. Attribution chain at
`NOTICES.md` in the source repo.

### Annotations

Skills + tools are LLM-generated (model + prompt_version + seed recorded
per artifact in `provenance.generated_by`) and human-reviewed by Lead
Curators before release. Claim ground-truth tiers (silver/gold) reflect
attestation depth: silver = automated extraction, gold = curator-verified.

#### Annotation process

Lead Curator reviews each derived skill against the source paper for
factual accuracy + correct attribution. See `CONTRIBUTING.md` in the
source repo for the full curator workflow.

#### Who are the annotators?

LLM agents (model + version recorded per artifact) and verified curators
with ORCID-confirmed identity (L1 + L2 per COI_POLICY).

### Personal and Sensitive Information

No personal or sensitive information is included. Source papers are
peer-reviewed scientific publications.

## Considerations for Using the Data

### Social Impact of Dataset

Provides reproducible scaffolding for scientific AI agents in
**{domain}**. Lowers the barrier to verifiable, traceable agent
behaviour by tying every skill + tool back to a peer-reviewed source.

### Discussion of Biases

- **Source-paper bias:** the dataset reflects whichever papers the
  Lead Curator + community chose to include. Currently {n_papers}
  papers — small sample with all the biases of that selection
  (publication bias, English-language bias, etc.).
- **LLM-generation bias:** skill descriptions and procedural text are
  LLM-generated and may reflect model biases. Always cross-reference
  against the cited source paper.
- **Tool-license bias:** SBOM resolution is curated for the most-cited
  tools in each domain. Unresolved licenses are flagged with
  `license_source: unresolved` — do not assume an unflagged tool is
  safe for commercial use.

### Other Known Limitations

- Verbatim quotations from non-open-access papers are sanitized in
  derived artifacts per `OPEN_ACCESS_POLICY.md` (≤300 chars per span,
  ≤1500 chars cumulative per paper). The CC-BY attribution chain is
  documented in `NOTICES.md`.
- Some skills lack a `## Examples` section (current fill rate is
  partial). See the collection's `CHANGELOG.md` for the known-issue
  log of each release.
- IRIs at `w3id.org/holobiomicslab/asb-*` are stable identifiers but
  may not yet HTTP-resolve until the perma-id/w3id.org redirection PR
  lands. See the source repo README for the temporary fallback.

## Additional Information

### Dataset Curators

- **Lead Curator:** see `MAINTAINERS.md` in the source repo
- **Reviewer attestations:** see `collections/{slug}/v{version}/reviews/`
- **Maintainers:** Holobiomics Lab (CNRS / Université Côte d'Azur)

### Licensing Information

- **Synthesis layer** (skill bodies, tooling, eval scripts): Apache-2.0
- **Verbatim source quotations**: redistributed under their original
  publishing license (CC-BY for OA, fair-use for hybrid/closed). Full
  per-paper attribution chain at `NOTICES.md`.
- **Tool records**: each carries an explicit `license_spdx` field; see
  `sbom.cdx.json` for the CycloneDX inventory.

### Citation Information

```bibtex
{bibtex if bibtex else '@misc{} % CITATION.cff was empty or not provided'}
```

See `CITATION.cff` and `CITATION.bib` in the source repository for the
full citation. The DOI above is the canonical Zenodo identifier for
this release.

### Contributions

Contributions welcome — see `CONTRIBUTING.md` in the source repo for the
curator workflow, COI policy, and attestation process.

## Programmatic access

```python
from datasets import load_dataset

ds_skills = load_dataset("HolobiomicsLab/asb-{slug}-v{version}", "skills")
ds_bench  = load_dataset("HolobiomicsLab/asb-{slug}-v{version}", "benchmark")
ds_tools  = load_dataset("HolobiomicsLab/asb-{slug}-v{version}", "tools")
```
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
