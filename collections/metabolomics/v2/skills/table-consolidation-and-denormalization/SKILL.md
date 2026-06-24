---
name: table-consolidation-and-denormalization
description: Use when when you have cleaned, normalized organism, structure, and reference
  tables from separate cleaning pipelines (e.g., after 2_curating stage) and must
  integrate them into a single queryable table while maintaining referential integrity
  and generating lookup dictionaries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - R
  - data.table
  - gzip/compression utilities
  license_tier: restricted
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

# table-consolidation-and-denormalization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Consolidate normalized organism, structure, and reference tables into a single denormalized curated table by performing sequential left-join operations and appending external annotations (e.g., NP-classifier), while preserving all original rows and generating derived dictionaries for each entity type. This skill is essential when integrating multi-source biological and chemical data into a unified structure-organism-reference knowledgebase.

## When to use

When you have cleaned, normalized organism, structure, and reference tables from separate cleaning pipelines (e.g., after 2_curating stage) and must integrate them into a single queryable table while maintaining referential integrity and generating lookup dictionaries. Specifically triggered when you possess cleaned organism data, translated/cleaned structure data, cleaned reference data, and external structural annotations (e.g., NP-classifier), and your goal is to produce a denormalized curated table (e.g., interim/tables/3_curated/table.tsv.gz) that preserves all original rows from the source table and enables downstream validation and analysis.

## When NOT to use

- Input tables are already denormalized or merged; consolidation would introduce redundancy or lose reference integrity.
- Original table identifiers are not available or have been lost; you cannot preserve row lineage and validation status.
- Cleaning and translation pipelines have not been completed; tables contain inconsistent or unvalidated entries that would propagate downstream.

## Inputs

- interim/tables/0_original/table.tsv.gz (original integrated table with record identifiers and lineage)
- interim/tables/2_cleaned/organism/cleaned.tsv.gz (cleaned organism data)
- interim/tables/1_translated/structure/final.tsv.gz (final structure data)
- interim/tables/2_cleaned/structure/named.tsv.gz (named structure data)
- interim/dictionaries/structure/npclassifier/smiles_np_classified.tsv.gz (NP-classifier structure annotations)
- interim/tables/2_cleaned/reference/cleaned.tsv.gz (cleaned reference data)

## Outputs

- interim/tables/3_curated/table.tsv.gz (denormalized curated structure-organism-reference table with all rows preserved and validated entries flagged)
- interim/dictionary/organism/dictionary.tsv.gz (derived organism lookup dictionary)
- interim/dictionary/organism/metadata.tsv.gz (organism metadata)
- interim/dictionary/structure/dictionary.tsv.gz (derived structure lookup dictionary)
- interim/dictionary/structure/metadata.tsv.gz (structure metadata)
- interim/dictionary/reference/dictionaryOrganism.tsv.gz (reference-to-organism mapping dictionary)
- interim/dictionary/reference/metadata.tsv.gz (reference metadata)

## How to apply

Load the original integrated table (interim/tables/0_original/table.tsv.gz) to anchor all row identifiers and preserve lineage. Sequentially load cleaned organism data (interim/tables/2_cleaned/organism/cleaned.tsv.gz), final structure data (interim/tables/1_translated/structure/final.tsv.gz), named structure data (interim/tables/2_cleaned/structure/named.tsv.gz), NP-classifier annotations (interim/dictionaries/structure/npclassifier/smiles_np_classified.tsv.gz), and cleaned reference data (interim/tables/2_cleaned/reference/cleaned.tsv.gz) using data.table or equivalent. Perform left-join operations in sequence: join organisms by organism_id, structures by structure_id, references by reference_id, and append NP-classifier annotations by SMILES or structure identifier. Extract unique organism, structure, and reference entries to generate derived dictionaries (organism/dictionary.tsv.gz, structure/dictionary.tsv.gz, reference/dictionaryOrganism.tsv.gz) and corresponding metadata tables. Consolidate all columns into a single denormalized table, compress to interim/tables/3_curated/table.tsv.gz, and flag validated entries while ensuring all rows from the original table are preserved.

## Related tools

- **R** (Execute 1_integrating.R script for join operations and denormalization logic) — https://github.com/lotusnprod/lotus-processor
- **data.table** (Perform efficient left-join operations on cleaned and translated tables in R)
- **gzip/compression utilities** (Compress consolidated table to interim/tables/3_curated/table.tsv.gz)

## Examples

```
Rscript 1_integrating.R --original interim/tables/0_original/table.tsv.gz --organism interim/tables/2_cleaned/organism/cleaned.tsv.gz --structure interim/tables/1_translated/structure/final.tsv.gz --reference interim/tables/2_cleaned/reference/cleaned.tsv.gz --npclassifier interim/dictionaries/structure/npclassifier/smiles_np_classified.tsv.gz --output interim/tables/3_curated/table.tsv.gz
```

## Evaluation signals

- All rows from interim/tables/0_original/table.tsv.gz are preserved in the output table; row count matches or exceeds original count (accounting for splits/denormalization).
- All organism_id, structure_id, and reference_id foreign keys are populated post-join with no unexpected nulls (unless intentional for unmatched rows in outer joins).
- Derived dictionaries (organism, structure, reference) contain unique entries corresponding to joined data; no orphaned or duplicate entries in dictionaries.
- Validated entries are flagged with consistent, boolean validation status column; distribution of validated vs. unvalidated rows is documented.
- Output file (interim/tables/3_curated/table.tsv.gz) decompresses without corruption; column schema matches documented specification (all organism, structure, reference, and NP-classifier columns present).

## Limitations

- Row count may increase if 1:many or m:m joins occur (e.g., one organism mapped to multiple structures); document join cardinality and verify denormalization is intentional.
- NP-classifier annotations are appended by SMILES or structure identifier; missing or incorrectly formatted SMILES values will result in annotation gaps; validate SMILES format before join.
- Lineage and validation status depend on correct preservation of original table identifiers; if primary keys are corrupted or renamed during cleaning, traceability is lost.
- No changelog is documented; version history and updates to cleaning, translation, or annotation pipelines are not tracked, complicating reproducibility and debugging.

## Evidence

- [methods] Consolidation via sequential joins and dictionary extraction: "Perform left join operations in sequence: join organisms by organism_id, join structure data by structure_id, join reference data by reference_id, and append NP-classifier annotations by SMILES or"
- [methods] Input table inventory and sources: "Load cleaned organism data from interim/tables/2_cleaned/organism/cleaned.tsv.gz, final structure data from interim/tables/1_translated/structure/final.tsv.gz, named structure data from"
- [methods] Lineage preservation and original table role: "Load the original integrated table from interim/tables/0_original/table.tsv.gz to preserve original record identifiers and lineage."
- [methods] Dictionary derivation procedure: "Generate derived organism dictionary (interim/dictionary/organism/dictionary.tsv.gz) and metadata (interim/dictionary/organism/metadata.tsv.gz) by extracting unique organism entries and their"
- [methods] Output specification and row preservation: "Consolidate all columns into a single denormalized table and compress to interim/tables/3_curated/table.tsv.gz, ensuring all rows from the original table are preserved and validated entries are"
