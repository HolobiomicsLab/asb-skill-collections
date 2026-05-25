---
license: apache-2.0
tags: [agentic-ai, scientific-agents, metabolomics, asb, skill-collection, claude-code-plugin]
task_categories: [text-generation, question-answering]
size_categories: [n<1K]
language: [en]
pretty_name: "ASB Metabolomics Benchmark v1"
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
doi: "PLACEHOLDER"
---

# ASB Metabolomics Benchmark v1

ASB curated skill + benchmark collection for metabolomics. Derived from 5 peer-reviewed source papers (4 included, 1 documented-excluded) via AgenticScienceBuilder. 106 skills with EDAM annotations, 38 tools with SPDX licensing + CycloneDX SBOM, per-paper benchmark tasks, silver/gold-tiered claim ledger, CC-BY attribution chain.

## Dataset Description

- **Curated by:** Holobiomics Lab (CNRS / Université Côte d'Azur)
- **Funded by:** Holobiomics Lab
- **Shared by:** Holobiomics Lab
- **Language(s) (NLP):** English (en)
- **License:** Apache-2.0 (synthesis layer); fair-use for verbatim paper quotes

This dataset is a curated, evidence-grounded scientific-agent skill + tool +
benchmark collection for the **metabolomics** domain. It is produced by the
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

- `skills` — 0 curated, deduplicated procedural skills with EDAM annotations
- `benchmark` — 0 per-paper tasks + claim-retrieval test sets
- `tools` — 0 third-party software-tool records with SPDX licensing

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
ledger (0 papers, included + excluded). Each paper's access tier
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
**metabolomics**. Lowers the barrier to verifiable, traceable agent
behaviour by tying every skill + tool back to a peer-reviewed source.

### Discussion of Biases

- **Source-paper bias:** the dataset reflects whichever papers the
  Lead Curator + community chose to include. Currently 0
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
- **Reviewer attestations:** see `collections/metabolomics/v1/reviews/`
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
@misc{asbmetabolomicsv1,
  author = {{AgenticScienceBuilder} and {Holobiomics Lab}},
  title  = {Metabolomics v1},
  year   = {2026},
  note   = {HuggingFace dataset: HolobiomicsLab/asb-metabolomics-v1},
}
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

ds_skills = load_dataset("HolobiomicsLab/asb-metabolomics-v1", "skills")
ds_bench  = load_dataset("HolobiomicsLab/asb-metabolomics-v1", "benchmark")
ds_tools  = load_dataset("HolobiomicsLab/asb-metabolomics-v1", "tools")
```
