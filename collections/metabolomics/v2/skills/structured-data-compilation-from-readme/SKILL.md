---
name: structured-data-compilation-from-readme
description: Use when when a scientific software repository documents multiple standalone tools, web applications, or resources with associated metadata (URLs, publications, taxonomic coverage) in its README, and you need to create a machine-readable inventory for downstream indexing, validation, or reuse.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0219
  - http://edamontology.org/topic_3365
  tools:
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - metadataMASST
  - GNPS_MASST
  - microbe_masst
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
evidence_spans:
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
- Aggregated search outputs can be generated and visualized using metadataMASST
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_microbemasst
    doi: 10.1038/s41564-023-01575-9
    title: microbemasst
  dedup_kept_from: coll_microbemasst
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41564-023-01575-9
  all_source_dois:
  - 10.1038/s41564-023-01575-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Structured Data Compilation from README

## Summary

Extract and validate enumerated resources (tools, URLs, publications, metadata) from repository README documentation into a structured inventory format (CSV/JSON). This skill ensures reproducible discovery and verification of multi-component scientific software ecosystems where human-readable documentation is the authoritative source.

## When to use

When a scientific software repository documents multiple standalone tools, web applications, or resources with associated metadata (URLs, publications, taxonomic coverage) in its README, and you need to create a machine-readable inventory for downstream indexing, validation, or reuse. Particularly valuable when the README is the primary source of truth for tool enumeration and URL references.

## When NOT to use

- Tool metadata is scattered across multiple disparate files or external wikis with no single authoritative source document.
- README lists tools without URLs or publication references (insufficient metadata density for meaningful inventory).
- The goal is to discover undocumented or experimental tools; this skill only captures formally listed resources.

## Inputs

- Repository README.md file (plaintext or markdown)
- README section listing tool names and URLs
- Associated publication references or DOI links

## Outputs

- Structured inventory file (CSV or JSON format)
- Inventory with columns/fields: application_name, live_url, publication_doi_or_link, verification_status
- Validation report documenting URL accessibility and metadata completeness
- Optional: supplementary metadata file (e.g., taxonomic lineage counts, indexed data sources)

## How to apply

Locate and parse the README file to identify all documented standalone applications and their associated metadata (live URLs, publication DOI/links, feature coverage). Extract each application name, URL, and publication reference; validate that each URL responds correctly and publications are accessible. Structure the extracted data into a consistent format (CSV with columns: application_name, live_url, publication_doi_or_link, verification_status; or JSON with parallel fields). Include coverage metadata (e.g., taxonomic lineage counts, indexed data sources) when available in the README. Verify schema consistency across all rows and document any verification failures or inaccessible resources.

## Related tools

- **microbeMASST** (Domain-specific MASST application for microbial mass spectrometry search) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific MASST application for plant mass spectrometry search) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific MASST application for tissue mass spectrometry search) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific MASST application for microbiome mass spectrometry search) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific MASST application for food mass spectrometry search) — https://masst.gnps2.org/foodmasst2/
- **metadataMASST** (Aggregation and visualization tool for search outputs across all domain-specific MASSTs) — https://masst.gnps2.org/metadatamasst/
- **GNPS_MASST** (Source code repository containing standalone web application implementations) — https://github.com/mwang87/GNPS_MASST
- **microbe_masst** (Batch search and processing pipeline implementation) — https://github.com/robinschmid/microbe_masst

## Evaluation signals

- All six domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, metadataMASST) are present in the compiled inventory with non-empty URL and publication fields.
- Each live URL in the inventory is HTTP-accessible (responds with 2xx or 3xx status) and the resource loads without 404 or 5xx errors.
- All publication DOIs or links are valid and resolvable (either to PubMed, bioRxiv, Nature, or equivalent peer-review platform).
- Inventory file conforms to declared schema (CSV has all expected columns; JSON has consistent key-value structure across all records) with no missing required fields.
- Metadata coverage (e.g., taxonomic lineage counts from README table) is accurately transcribed and matches the source values (e.g., 'microbeMASST: 8 Kingdom, 20 Phylum, …').

## Limitations

- README documentation may become stale; URLs or publication references can break or change without immediate notice. Periodic re-validation is required.
- Some domain-specific MASSTs may still be under development (marked as preprint on bioRxiv); peer-reviewed status may change, requiring inventory updates.
- Batch processing (via jobs.py) requires Python 3.10 and the Fast Search API; compilation skill does not validate pipeline execution, only data structure.
- Taxonomic lineage metadata and indexed data source counts are static at the time of README generation; these reflect historical coverage and may differ from live database state.

## Evidence

- [readme] Six domain-specific MASST applications with URLs listed in README: "Standalone Web Apps:
1. [microbeMASST](https://masst.gnps2.org/microbemasst/)
2. [plantMASST](https://masst.gnps2.org/plantmasst/)
3. [tissueMASST](https://masst.gnps2.org/tissuemasst/)
4."
- [readme] Associated publication links for each tool: "Publications associated with the search tools:
1. [microbeMASST - Nature Microbiology](https://www.nature.com/articles/s41564-023-01575-9)
2. [plantMASST -"
- [readme] Taxonomic lineage coverage metadata in structured table: "| Tool | Kingdom | Phylum | Class | Order | Family | Genus | Species | Strain |
|---|---|---|---|---|---|---|---|---|
| microbeMASST | 8 | 20 | 48 | 124 | 278 | 561 | 1379 | 542 |
| plantMASST | 1 |"
- [intro] Workflow for batch compilation from source repository: "This repository contains the code and data for the different domain-specific MASSTs currently under development in the Dorrestein Lab at UC San Diego"
- [readme] Scope: single-spectrum vs batch search capability: "The code for the different standalone web applications, which allow users to search one spectrum at a time, can be found in GNPS_MASST"
