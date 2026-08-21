---
name: natural-products-structure-organism-association-integration
description: Use when you have separately cleaned and validated tables for organisms
  (interim/tables/2_cleaned/organism/cleaned.tsv.gz), structures (interim/tables/1_translated/structure/final.tsv.gz
  and interim/tables/2_cleaned/structure/named.tsv.gz), references (interim/tables/2_cleaned/reference/cleaned.tsv.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0209
  tools:
  - R
  - R data.table
  - 1_integrating.R
  - gzip / compression utilities
  license_tier: restricted
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.7554/eLife.70780
  all_source_dois:
  - 10.7554/eLife.70780
  - 10.1007/s00044-016-1764-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# natural-products-structure-organism-association-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Consolidate and denormalize cleaned organism, structure, and reference data into a unified curated table by performing sequential left joins and appending enrichment annotations, preserving all original record identifiers and lineage. This skill integrates multiple subgraphs (organism, structure, reference) to produce a single documented structure-organism pair resource suitable for computational natural products research.

## When to use

Apply this skill when you have separately cleaned and validated tables for organisms (interim/tables/2_cleaned/organism/cleaned.tsv.gz), structures (interim/tables/1_translated/structure/final.tsv.gz and interim/tables/2_cleaned/structure/named.tsv.gz), references (interim/tables/2_cleaned/reference/cleaned.tsv.gz), and external annotations (NP-classifier SMILES mappings), and you need to produce a single denormalized structure-organism association table with full lineage and enrichment metadata. Use this skill when your goal is to create a comprehensive reference dataset that preserves traceability back to original sources while consolidating heterogeneous organism and chemical structure metadata.

## When NOT to use

- If organism, structure, or reference tables have not yet been separately cleaned and validated; incomplete upstream curation will propagate errors into the consolidated table.
- If you need to maintain a normalized relational schema for downstream queries; this skill deliberately denormalizes into a flat table for breadth-first access.
- If your goal is to filter or subset the data rather than consolidate it; use this skill only after all filtering and validation steps on individual tables are complete.

## Inputs

- interim/tables/0_original/table.tsv.gz (original integrated table with record identifiers)
- interim/tables/2_cleaned/organism/cleaned.tsv.gz (cleaned organism data)
- interim/tables/1_translated/structure/final.tsv.gz (final translated structure data)
- interim/tables/2_cleaned/structure/named.tsv.gz (named structure data with enrichment)
- interim/tables/2_cleaned/reference/cleaned.tsv.gz (cleaned reference data)
- interim/dictionaries/structure/npclassifier/smiles_np_classified.tsv.gz (NP-classifier structure annotations)

## Outputs

- interim/tables/3_curated/table.tsv.gz (denormalized curated structure-organism-reference table)
- interim/dictionary/organism/dictionary.tsv.gz (derived organism dictionary)
- interim/dictionary/organism/metadata.tsv.gz (organism metadata)
- interim/dictionary/structure/dictionary.tsv.gz (derived structure dictionary)
- interim/dictionary/structure/metadata.tsv.gz (structure metadata)
- interim/dictionary/reference/dictionaryOrganism.tsv.gz (reference-organism mapping)
- interim/dictionary/reference/metadata.tsv.gz (reference metadata)

## How to apply

Load the original integrated table (interim/tables/0_original/table.tsv.gz) as the left-join anchor to preserve original record identifiers and lineage. Sequentially join cleaned organism data by organism_id, then structure data (first the final translated version, then the named version) by structure_id, then reference data by reference_id, and finally append NP-classifier structure annotations by SMILES or structure identifier. For each join, validate that row counts are preserved and that no unintended data loss occurs. After consolidation, generate derived dictionaries and metadata for organisms, structures, and references by extracting unique entries and their associated metadata fields. Compress the final denormalized table to interim/tables/3_curated/table.tsv.gz, ensuring all original rows are retained and validated entries are appropriately flagged. The rationale is to maintain data provenance and traceability while flattening the relational structure into a single queryable resource.

## Related tools

- **R data.table** (Load, join, and consolidate cleaned data tables; perform denormalization and column aggregation) — https://github.com/lotusnprod/lotus-processor
- **1_integrating.R** (Script that executes the sequential left joins on organism, structure, and reference subgraphs to produce the integrated curated table) — https://github.com/lotusnprod/lotus-processor
- **gzip / compression utilities** (Compress denormalized curated table and derived dictionaries to .tsv.gz format for efficient storage and distribution) — https://github.com/lotusnprod/lotus-processor

## Examples

```
Rscript 1_integrating.R --original interim/tables/0_original/table.tsv.gz --organism interim/tables/2_cleaned/organism/cleaned.tsv.gz --structure interim/tables/1_translated/structure/final.tsv.gz --structure-named interim/tables/2_cleaned/structure/named.tsv.gz --reference interim/tables/2_cleaned/reference/cleaned.tsv.gz --npclassifier interim/dictionaries/structure/npclassifier/smiles_np_classified.tsv.gz --output interim/tables/3_curated/table.tsv.gz
```

## Evaluation signals

- All rows from the original table (interim/tables/0_original/table.tsv.gz) are retained in the final curated table; row count should match or be documented if intentional filtering occurred.
- Join operations produce expected row counts: organism_id matches result in correct cardinality, structure_id joins do not introduce duplicates, reference_id joins do not introduce duplicates.
- NP-classifier annotations are successfully appended by SMILES or structure identifier with no unmatched rows flagged as missing annotation data.
- Derived dictionaries contain unique entries with correct metadata mappings; organism dictionary and metadata have consistent row counts, structure dictionary and metadata have consistent row counts, reference-organism mapping is complete.
- Final curated table schema includes all columns from original table plus all enriched columns (translated structure names, NP classifications, reference metadata); schema is validated against expected column list.

## Limitations

- The skill assumes that upstream organism, structure, and reference tables have been independently cleaned and validated; garbage in denormalized table out if upstream tables contain errors.
- Join operations depend on consistent use of organism_id, structure_id, and reference_id keys across all input tables; misaligned or missing keys will result in data loss or null-filled rows.
- NP-classifier annotations are only appended if SMILES identifiers or structure identifiers match; unmatched structures will not receive annotations and should be flagged in QC.
- The denormalized output is not suitable for OLTP workflows; it is designed for read-heavy analytical access and does not enforce relational integrity constraints.

## Evidence

- [methods] Sequential join workflow for organism-structure-reference consolidation: "Perform left join operations in sequence: join organisms by organism_id, join structure data by structure_id, join reference data by reference_id, and append NP-classifier annotations by SMILES or"
- [methods] Original table as anchor for lineage preservation: "Load the original integrated table from interim/tables/0_original/table.tsv.gz to preserve original record identifiers and lineage."
- [methods] Denormalization and dictionary generation rationale: "Consolidate all columns into a single denormalized table and compress to interim/tables/3_curated/table.tsv.gz, ensuring all rows from the original table are preserved and validated entries are"
- [methods] 2_curating stage consolidation objective: "The 2_curating stage uses 1_integrating.R to consolidate entries through organism, structure, and reference subgraphs, producing an integrated curated table."
- [readme] LOTUS resource structure-organism pair definition: "*LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented"
