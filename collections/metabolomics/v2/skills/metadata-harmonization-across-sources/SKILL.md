---
name: metadata-harmonization-across-sources
description: Use when you have completed independent batch searches across one or more domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) and received multiple separate output files (_microbe.html, _plant.json, _matches.tsv, _library.tsv, _datasets.tsv, _count_domain.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
  - Fast Search API
  - jobs.py
  - GNPS_MASST
derived_from:
- doi: 10.1038/s41564-023-01575-9
  title: microbemasst
evidence_spans:
- Aggregated search outputs can be generated and visualized using metadataMASST
- microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST
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

# metadata-harmonization-across-sources

## Summary

Ingest, parse, normalize, and aggregate search output files from multiple domain-specific MASST tools into a unified, structured format compatible with visualization and downstream analysis. This skill enables integration of spectrum identifiers, match scores, and metadata fields across heterogeneous MASST domains (microbes, plants, tissues, microbiomes, food) into a single consolidated artifact.

## When to use

You have completed independent batch searches across one or more domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) and received multiple separate output files (_microbe.html, _plant.json, _matches.tsv, _library.tsv, _datasets.tsv, _count_domain.tsv) that need to be combined into a single searchable summary. Use this skill when your research question requires unified access to match scores and metadata across domains, or when you need to visualize aggregated results in the metadataMASST web interface.

## When NOT to use

- You are analyzing a single spectrum at a time — use individual domain-specific MASST web applications instead of batch aggregation.
- Your search outputs are already integrated into a single GNPS/MassIVE analysis — this skill is for external aggregation of independently run domain tools.
- You need real-time or streaming result aggregation — this skill assumes complete, static output files from finished batch runs.

## Inputs

- Domain-specific MASST search output files (HTML trees: _microbe.html, _plant.html, _tissue.html, _microbiome.html, _food.html)
- JSON tree files from domain-specific MASST runs
- TSV match tables (_matches.tsv) from Fast Search API output
- TSV library tables (_library.tsv) with GNPS library identifications
- TSV dataset count tables (_datasets.tsv) with sample distribution
- TSV domain-specific count files (_count_domain.tsv) with per-domain match statistics

## Outputs

- Unified aggregated table or structured format (TSV or JSON) combining records from all input domains
- Merged metadata summary artifact compatible with metadataMASST web interface
- Cross-reference lookup table mapping spectrum identifiers to source domain(s)
- Validation report documenting completeness, consistency, and schema conformance

## How to apply

Load all search output files (JSON trees, TSV match tables, count files) from each completed domain-specific MASST run. Parse and normalize each output by extracting spectrum identifiers, cosine match scores, metadata fields (taxonomy, sample origin, dataset provenance), and domain-specific annotations. Merge records by spectrum identifier into a unified table or structured format, preserving source domain information as a cross-reference field. Validate the aggregated output for completeness (all input spectra represented), consistency (no duplicate records with conflicting scores), and schema conformance with metadataMASST input requirements. Generate the combined artifact in a format compatible with the metadataMASST web interface for interactive exploration.

## Related tools

- **metadataMASST** (Target visualization and aggregation interface that consumes harmonized multi-domain search outputs) — https://masst.gnps2.org/metadatamasst/
- **microbeMASST** (Domain-specific search tool producing output files to be aggregated) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific search tool producing output files to be aggregated) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific search tool producing output files to be aggregated) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific search tool producing output files to be aggregated) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific search tool producing output files to be aggregated) — https://masst.gnps2.org/foodmasst2/
- **Fast Search API** (Backend API executed by jobs.py to generate domain-specific TSV outputs for aggregation) — https://fasst.gnps2.org/fastsearch/
- **jobs.py** (Batch processing script that orchestrates multi-domain MASST searches and generates harmonizable output files) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py
- **GNPS_MASST** (Source code repository for domain-specific MASST web applications) — https://github.com/mwang87/GNPS_MASST

## Evaluation signals

- All spectrum identifiers from input files are present in the aggregated output; no spectra are dropped during merging.
- Match scores and metadata fields preserve their original values from domain-specific outputs; no data corruption or unit conversion errors occur.
- Cross-domain records for the same spectrum show consistent taxonomy, sample metadata, and dataset provenance across all domains in which they appear.
- The aggregated output validates against the metadataMASST input schema (confirmed by successful upload or schema validation tool).
- Row counts and unique spectrum counts in the aggregated table match expectations: e.g., if input domain files contain N_microbe + N_plant + ... spectra with some overlaps, aggregated count should equal the union size.

## Limitations

- The skill requires domain-specific MASST tools to complete successfully; if any domain run fails or times out, that domain's records will be absent from the harmonized output.
- Fast Search API failures may result in incomplete match lists in _matches.tsv files. The README notes this is handled by re-running jobs.py multiple times with skip_existing=True, but this is not automatic.
- Metadata field schemas vary across domains (e.g., taxonomy depth in microbeMASST vs. plantMASST), so normalization may require domain-specific mapping logic or loss of granular information.
- The skill assumes input files follow the naming convention established by jobs.py (_domain.html, _matches.tsv, _library.tsv, etc.); non-standard file names or structures will not be recognized.

## Evidence

- [other] metadataMASST accepts aggregated search outputs from one or more domain-specific MASST runs: "metadataMASST accepts aggregated search outputs from one or more domain-specific MASST runs and produces visualizable summary artifacts"
- [other] Parsing and normalization of search results across domains: "Parse and normalize search results, extracting spectrum identifiers, match scores, and metadata fields across domain sources."
- [other] Aggregation workflow step merging records from multiple sources: "Aggregate results by merging records from multiple MASST outputs into a unified table or structured format."
- [other] Output generation for visualization: "Generate a combined visualizable summary artifact compatible with the metadataMASST web interface."
- [readme] Batch search workflow produces multiple output file types: "A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html (e.g., _microbe.html). A series of JSON files for the different trees will be"
- [readme] Fast Search API basis for batch outputs: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
- [readme] Domain-specific MASST tools produce parallel outputs: "This repository contains the code and data for the different domain-specific MASSTs currently under development in the Dorrestein Lab at UC San Diego. This includes microbeMASST, plantMASST,"
- [other] Aggregation validation requirement: "Validate the aggregated output for completeness and consistency across input sources."
