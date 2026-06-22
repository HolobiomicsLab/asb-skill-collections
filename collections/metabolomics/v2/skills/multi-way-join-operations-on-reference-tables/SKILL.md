---
name: multi-way-join-operations-on-reference-tables
description: Use when you have independently cleaned and validated organism, structure, and reference tables (each keyed by organism_id, structure_id, and reference_id respectively) and need to consolidate them into a single denormalized curated table that maintains traceability to the original integrated table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - R
  - R data.table
  - 1_integrating.R
  - Make
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-way-join-operations-on-reference-tables

## Summary

Sequentially join cleaned organism, structure, and reference tables by their identifiers to consolidate multi-source entries into a unified denormalized curated table while preserving original record lineage. This skill is essential when integrating heterogeneous reference data sources into a single comprehensive structure-organism-reference resource.

## When to use

Apply this skill when you have independently cleaned and validated organism, structure, and reference tables (each keyed by organism_id, structure_id, and reference_id respectively) and need to consolidate them into a single denormalized curated table that maintains traceability to the original integrated table. The trigger is the completion of parallel cleaning pipelines (1_cleaningOriginal.R, 3_cleaningTranslated.R, 4_cleaningTaxonomy.R) that produce separate interim/tables/2_cleaned/{organism,structure,reference}/cleaned.tsv.gz files.

## When NOT to use

- Input tables are not yet cleaned or validated — apply cleaning and enrichment steps first (cleaningOriginal, cleaningTranslated, cleaningTaxonomy).
- Original record identifiers and lineage are not critical — use this skill only when audit trail preservation is required.
- Structure-organism pairs need further deduplication or sampling — apply this skill before validation and platinum-standard filtering.

## Inputs

- interim/tables/0_original/table.tsv.gz (original integrated table with record identifiers)
- interim/tables/2_cleaned/organism/cleaned.tsv.gz (cleaned organism data)
- interim/tables/1_translated/structure/final.tsv.gz (translated structure data)
- interim/tables/2_cleaned/structure/named.tsv.gz (named structure data)
- interim/tables/2_cleaned/reference/cleaned.tsv.gz (cleaned reference data)
- interim/dictionaries/structure/npclassifier/smiles_np_classified.tsv.gz (NP-classifier annotations)

## Outputs

- interim/tables/3_curated/table.tsv.gz (denormalized curated table with all consolidated columns)
- interim/dictionary/organism/dictionary.tsv.gz (derived organism dictionary)
- interim/dictionary/organism/metadata.tsv.gz (organism metadata)
- interim/dictionary/structure/dictionary.tsv.gz (derived structure dictionary)
- interim/dictionary/structure/metadata.tsv.gz (structure metadata)
- interim/dictionary/reference/dictionaryOrganism.tsv.gz (reference-to-organism mapping dictionary)
- interim/dictionary/reference/metadata.tsv.gz (reference metadata)

## How to apply

Load the original integrated table from interim/tables/0_original/table.tsv.gz to preserve record identifiers and lineage. Sequentially perform left join operations: join organism data (interim/tables/2_cleaned/organism/cleaned.tsv.gz) by organism_id, join translated and named structure data (interim/tables/1_translated/structure/final.tsv.gz and interim/tables/2_cleaned/structure/named.tsv.gz) by structure_id, join cleaned reference data (interim/tables/2_cleaned/reference/cleaned.tsv.gz) by reference_id, and append NP-classifier structure annotations (interim/dictionaries/structure/npclassifier/smiles_np_classified.tsv.gz) by SMILES or structure identifier. Ensure all rows from the original table are preserved (use left join throughout, not inner join) and flag validated entries. Consolidate all columns into a single denormalized table to facilitate downstream analysis and dictionary generation.

## Related tools

- **R data.table** (Perform sequential left join operations on large compressed tabular data in memory) — https://github.com/lotusnprod/lotus-processor/wiki
- **1_integrating.R** (Main integration script orchestrating multi-way join operations and dictionary generation) — https://github.com/lotusnprod/lotus-processor
- **Make** (Orchestrate the 2_curating stage workflow including join operations) — https://github.com/lotusnprod/lotus-processor

## Examples

```
Rscript 1_integrating.R --original interim/tables/0_original/table.tsv.gz --organism interim/tables/2_cleaned/organism/cleaned.tsv.gz --structure interim/tables/2_cleaned/structure/named.tsv.gz --reference interim/tables/2_cleaned/reference/cleaned.tsv.gz --output interim/tables/3_curated/table.tsv.gz
```

## Evaluation signals

- All rows from interim/tables/0_original/table.tsv.gz are preserved in the output curated table (row count invariant: output ≥ original).
- No null-key violations: every organism_id, structure_id, and reference_id in the original table finds a matching row in the respective cleaned tables or is explicitly flagged as unmatched.
- Derived dictionaries (organism, structure, reference) contain unique entries with consistent metadata cardinality; spot-check organism/structure/reference_id distribution across dictionary and main table.
- Output table schema is flat with all organism, structure, reference, and NP-classifier columns denormalized into a single row per structure-organism-reference triplet.
- Validation flags correctly identify rows where all three cleaned data sources provided complete matches versus partial or missing matches.

## Limitations

- Join key collisions or duplicate identifiers in cleaned tables may cause cartesian product expansion; validate key uniqueness in input tables before joining.
- SMILES-based NP-classifier annotation appending may fail if SMILES standardization differs between source and classifier dictionary; apply consistent SMILES sanitization before join.
- Large denormalized output table may exceed memory in R if structure or reference dictionaries are very large; consider chunked processing or data.table by-reference operations.
- Left join preserves all original rows but may introduce NAs in organism, structure, or reference columns if cleaned tables are incomplete; document and flag such rows.

## Evidence

- [methods] task_002_finding: "The 2_curating stage uses 1_integrating.R to consolidate entries through organism, structure, and reference subgraphs, producing an integrated curated table."
- [methods] task_002_workflow_step_3: "Perform left join operations in sequence: join organisms by organism_id, join structure data by structure_id, join reference data by reference_id, and append NP-classifier annotations by SMILES or"
- [methods] task_002_workflow_step_1: "Load cleaned organism data from interim/tables/2_cleaned/organism/cleaned.tsv.gz, final structure data from interim/tables/1_translated/structure/final.tsv.gz, named structure data from"
- [methods] task_002_workflow_step_2: "Load the original integrated table from interim/tables/0_original/table.tsv.gz to preserve original record identifiers and lineage."
- [methods] task_002_workflow_step_7: "Consolidate all columns into a single denormalized table and compress to interim/tables/3_curated/table.tsv.gz, ensuring all rows from the original table are preserved and validated entries are"
- [methods] lotus_data_scale: "588694 unique referenced structure-organism pairs (484174 in 3D|2D format)"
- [readme] readme_tools: "Please make sure to have Make installed."
