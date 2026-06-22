---
name: dictionary-and-metadata-extraction-from-relational-data
description: 'Use when after performing left-join operations on cleaned organism, structure, and reference subgraphs but before final table denormalization. Trigger conditions: (1) you have a unified table with repeated entity_id columns (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0625
  tools:
  - R
  - R data.table
  - 1_integrating.R
  - gzip compression
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus_cq
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus_cq
schema_version: 0.2.0
---

# dictionary-and-metadata-extraction-from-relational-data

## Summary

Extract unique entities and their associated metadata from denormalized relational tables by grouping on entity identifiers and materializing separate dictionary and metadata artifacts. This skill is essential when consolidating multi-source data into a unified table and you need to support downstream lookup, validation, and cross-referencing without repeating entity information across thousands of rows.

## When to use

Apply this skill after performing left-join operations on cleaned organism, structure, and reference subgraphs but before final table denormalization. Trigger conditions: (1) you have a unified table with repeated entity_id columns (e.g., organism_id, structure_id, reference_id appearing in hundreds of thousands of rows); (2) you need to create standalone lookup dictionaries to enable efficient validation and external export (e.g., to Wikidata); (3) you want to preserve entity metadata (taxonomic rank, chemical formula, DOI) separately from the de-normalized fact table to reduce redundancy and enable targeted enrichment.

## When NOT to use

- Input is already a set of separate normalized tables with no denormalized fact table — you do not need to extract dictionaries if they already exist as independent artifacts.
- You are performing a one-off ad-hoc query and do not need reusable lookup artifacts; skip extraction if downstream consumers will not reference or validate against dictionaries.
- Entity metadata is sparse, inconsistent, or unmapped across sources — extraction will produce incomplete dictionaries that may give false confidence in coverage.

## Inputs

- consolidated denormalized table (TSV.GZ format, e.g., interim/tables/3_curated/table.tsv.gz)
- cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz)
- final and named structure data (interim/tables/1_translated/structure/final.tsv.gz, interim/tables/2_cleaned/structure/named.tsv.gz)
- cleaned reference table (interim/tables/2_cleaned/reference/cleaned.tsv.gz)
- NP-classifier structure annotations (interim/dictionaries/structure/npclassifier/smiles_np_classified.tsv.gz)

## Outputs

- organism dictionary (interim/dictionary/organism/dictionary.tsv.gz)
- organism metadata (interim/dictionary/organism/metadata.tsv.gz)
- structure dictionary (interim/dictionary/structure/dictionary.tsv.gz)
- structure metadata (interim/dictionary/structure/metadata.tsv.gz)
- reference dictionary mapping references to organisms (interim/dictionary/reference/dictionaryOrganism.tsv.gz)
- reference metadata (interim/dictionary/reference/metadata.tsv.gz)
- validation report (entity completeness and orphan check)

## How to apply

Load the consolidated denormalized table (e.g., interim/tables/3_curated/table.tsv.gz containing 588,694 structure-organism pairs). For each entity type (organism, structure, reference), group rows by the entity identifier (organism_id, structure_id, reference_id), extract unique entity values and all associated metadata columns, and write to separate dictionary and metadata TSV files (compressed). For organisms, materialize interim/dictionary/organism/dictionary.tsv.gz (unique organism names and identifiers) and interim/dictionary/organism/metadata.tsv.gz (taxonomic rank, authority, lineage if available). Repeat for structures (dictionary plus chemical metadata: SMILES, InChI, molecular weight, NP-classifier label) and references (reference dictionary mapping reference_id to organism_id, DOI, authors, title). Validate that all entity_id values in the main table have a corresponding entry in each dictionary; flag orphaned or missing references. Use R data.table grouping operations (.SD, keyby) for memory efficiency on large tables (>500k rows).

## Related tools

- **R data.table** (Memory-efficient grouping and aggregation of large denormalized tables using .SD and keyby operations to extract unique entities and metadata)
- **1_integrating.R** (Script that consolidates cleaned organism, structure, and reference subgraphs via left joins; feeds the denormalized input to dictionary extraction) — https://github.com/lotusnprod/lotus-processor
- **gzip compression** (Compress all output dictionary and metadata TSV files (.tsv.gz) for efficient storage and transfer)

## Examples

```
Rscript 1_integrating.R --input interim/tables/0_original/table.tsv.gz --organism interim/tables/2_cleaned/organism/cleaned.tsv.gz --structure interim/tables/1_translated/structure/final.tsv.gz --reference interim/tables/2_cleaned/reference/cleaned.tsv.gz --output interim/tables/3_curated/ --extract-dictionaries TRUE
```

## Evaluation signals

- All unique organism_id, structure_id, and reference_id values in the main table have exactly one corresponding row in their respective dictionaries (no missing or duplicate keys).
- No NULL or NA values in primary identifier columns (organism_id, structure_id, reference_id) in any dictionary; metadata columns may have NAs only if documented as expected (e.g., unpopulated taxonomic ranks for poorly characterized organisms).
- Row counts: organism dictionary ≤ 42,166 (documented unique organisms); structure dictionary ≤ 231,330 (3D format) or 153,956 (2D format); reference dictionary ≤ count of unique references in original data.
- Cross-reference validation: reference dictionary entries that map reference_id to organism_id should allow joining back to organism dictionary without orphaned references.
- File sizes and compression ratios are reasonable (e.g., organism metadata <10 MB when compressed, structure metadata <50 MB); extreme sizes may indicate duplication or aggregation errors.

## Limitations

- Entity metadata completeness varies by source: some organisms may lack taxonomic rank or authority data; some structures may lack SMILES or InChI. Dictionaries will reflect this incompleteness and should be documented with coverage metadata.
- Large denormalized tables (>500k rows) require in-memory grouping; users with <8 GB RAM may need to process organism, structure, and reference dictionaries sequentially or in chunks rather than all at once.
- The skill assumes unique entity identifiers (organism_id, structure_id, reference_id) are stable and consistent across the consolidated table; if identifiers are duplicated or inconsistently formatted, extraction will produce erroneous dictionaries.
- Circular or hierarchical metadata (e.g., reference_id → organism_id → taxonomy → higher-level organism) is flattened into separate dictionaries; recovery of these relationships requires joining across dictionaries on output, not a single artifact.

## Evidence

- [methods] Generate derived organism dictionary (interim/dictionary/organism/dictionary.tsv.gz) and metadata (interim/dictionary/organism/metadata.tsv.gz) by extracting unique organism entries and their associated metadata.: "Generate derived organism dictionary (interim/dictionary/organism/dictionary.tsv.gz) and metadata (interim/dictionary/organism/metadata.tsv.gz) by extracting unique organism entries and their"
- [methods] Generate derived structure dictionary (interim/dictionary/structure/dictionary.tsv.gz) and metadata (interim/dictionary/structure/metadata.tsv.gz) similarly.: "Generate derived structure dictionary (interim/dictionary/structure/dictionary.tsv.gz) and metadata (interim/dictionary/structure/metadata.tsv.gz) similarly."
- [methods] Generate derived reference dictionary (interim/dictionary/reference/dictionaryOrganism.tsv.gz) and metadata (interim/dictionary/reference/metadata.tsv.gz) mapping references to organisms.: "Generate derived reference dictionary (interim/dictionary/reference/dictionaryOrganism.tsv.gz) and metadata (interim/dictionary/reference/metadata.tsv.gz) mapping references to organisms."
- [methods] Consolidate all columns into a single denormalized table and compress to interim/tables/3_curated/table.tsv.gz, ensuring all rows from the original table are preserved and validated entries are flagged.: "Consolidate all columns into a single denormalized table and compress to interim/tables/3_curated/table.tsv.gz, ensuring all rows from the original table are preserved and validated entries are"
- [methods] 588694 unique referenced structure-organism pairs (484174 in 3D|2D format) and 231330 unique curated structures in 3D and 153956 in 2D format from 42166 unique organisms: "231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms"
