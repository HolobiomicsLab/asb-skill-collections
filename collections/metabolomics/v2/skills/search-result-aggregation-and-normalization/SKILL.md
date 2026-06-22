---
name: search-result-aggregation-and-normalization
description: Use when you have executed batch searches across two or more domain-specific MASST tools and obtained separate output files (_microbe.json, _plant.json, _tissue.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - metadataMASST
  - microbeMASST
  - plantMASST
  - tissueMASST
  - microbiomeMASST
  - foodMASST
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
---

# search-result-aggregation-and-normalization

## Summary

Combine and normalize search output files from multiple domain-specific MASST tools (microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST) into unified, structured artifacts compatible with metadataMASST visualization. This skill reconciles heterogeneous spectrum match results across domains into a single coherent summary.

## When to use

You have executed batch searches across two or more domain-specific MASST tools and obtained separate output files (_microbe.json, _plant.json, _tissue.json, etc.), and you need to merge these results into a single visualizable summary for cross-domain comparison or comprehensive metabolite annotation.

## When NOT to use

- Single-domain search output: if you only ran one MASST tool, there is nothing to aggregate — pass the output directly to metadataMASST visualization.
- Unaggregated raw spectral data: if you have raw MS/MS spectra (.mgf) or USI lists, execute the batch search first using jobs.py before attempting aggregation.
- Pre-aggregated metadataMASST output: if the results are already in metadataMASST format, this skill is redundant.

## Inputs

- Output files from one or more domain-specific MASST batch searches (_matches.tsv, _library.tsv, _datasets.tsv, _count_domain.tsv, _domain.json, _domain.html)
- Spectrum identifiers and match metadata from multiple MASST tools

## Outputs

- Unified aggregated table or structured JSON combining results from all domain-specific MASST searches
- Visualizable summary artifact compatible with metadataMASST web interface
- Consolidated match records with spectrum IDs, cosine scores, and cross-domain metadata

## How to apply

Load search output files from each domain-specific MASST run (typically _matches.tsv, _library.tsv, _datasets.tsv, and _count_domain.tsv files). Parse and normalize the results by extracting spectrum identifiers, cosine match scores, and domain-specific metadata fields using a common schema. Merge records from multiple MASST outputs by aligning on shared spectrum IDs and consolidating duplicate matches while preserving domain-specific annotations. Aggregate match counts and dataset information across domains. Generate a unified output table or structured JSON artifact that combines all domain results and is compatible with the metadataMASST web interface for interactive visualization. Validate the aggregated output by checking that all input spectra are represented, no records were lost in the merge, and consistency is maintained across metadata fields.

## Related tools

- **metadataMASST** (Target visualization and exploration platform that consumes aggregated search output) — https://masst.gnps2.org/metadatamasst/
- **microbeMASST** (Domain-specific MASST tool generating searchable microbial metabolomics results to be aggregated) — https://masst.gnps2.org/microbemasst/
- **plantMASST** (Domain-specific MASST tool generating searchable plant metabolomics results to be aggregated) — https://masst.gnps2.org/plantmasst/
- **tissueMASST** (Domain-specific MASST tool generating searchable tissue metabolomics results to be aggregated) — https://masst.gnps2.org/tissuemasst/
- **microbiomeMASST** (Domain-specific MASST tool generating searchable microbiome metabolomics results to be aggregated) — https://masst.gnps2.org/microbiomemasst/
- **foodMASST** (Domain-specific MASST tool generating searchable food metabolomics results to be aggregated) — https://masst.gnps2.org/foodmasst2/
- **jobs.py** (Python batch execution script that generates the individual domain-specific MASST output files to be aggregated) — https://github.com/robinschmid/microbe_masst/blob/master/code/jobs.py
- **GNPS_MASST** (Parent repository containing code for all standalone MASST web applications) — https://github.com/mwang87/GNPS_MASST

## Evaluation signals

- All spectra from input domain-specific MASST searches appear in the aggregated output with no data loss.
- Spectrum identifiers, cosine match scores, and metadata fields are preserved and correctly mapped across all domains.
- Merged records do not duplicate matches found in multiple domain searches; consolidation logic correctly identifies and deduplicates cross-domain hits.
- The aggregated artifact is successfully consumed by metadataMASST web interface without schema or format errors.
- Aggregated match counts per dataset and per domain match the sum of individual domain-specific MASST outputs.

## Limitations

- Aggregation requires all input MASST tools to complete successfully; if some domain searches fail or timeout, those results will be missing from the unified summary.
- The Fast Search API used by jobs.py may fail on some entries, requiring multiple sequential re-runs until no new output is generated (as noted in the README).
- Currently supported domains are limited to microbeMASST, plantMASST, tissueMASST, microbiomeMASST, and foodMASST; adding new domain tools requires schema extension.
- Aggregation preserves only the metadata fields extracted by individual MASST tools; if a domain tool does not report a particular field, that information is lost in the unified output.

## Evidence

- [other] metadataMASST accepts aggregated search outputs from one or more domain-specific MASST runs and produces visualizable summary artifacts: "metadataMASST accepts aggregated search outputs from one or more domain-specific MASST runs and produces visualizable summary artifacts"
- [other] Parse and normalize search results across domain sources: "Parse and normalize search results, extracting spectrum identifiers, match scores, and metadata fields across domain sources"
- [other] Aggregate results by merging records from multiple MASST outputs: "Aggregate results by merging records from multiple MASST outputs into a unified table or structured format"
- [other] metadataMASST web interface compatibility: "Generate a combined visualizable summary artifact compatible with the metadataMASST web interface"
- [readme] Batch search outputs from jobs.py: "Running jobs.py allows users to leverage the Fast Search API and execute a batch search of multiple MS/MS spectra against the current indexed data in GNPS/MassIVE, Metabolomics Workbench,"
- [readme] Output files generated by batch search: "A series of interactive HTML trees files will be generated for each domain-specific MASST ending with _domain.html (e.g., _microbe.html)"
- [other] Validation step for aggregation: "Validate the aggregated output for completeness and consistency across input sources"
