---
name: data-lineage-preservation-in-etl-pipelines
description: Use when when consolidating entries from multiple heterogeneous source
  databases into a unified table, and you need to maintain auditable connections between
  final curated records and their original source entries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0622
  tools:
  - R
  - data.table
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

# data-lineage-preservation-in-etl-pipelines

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Preserve and track the origin, transformations, and identifiers of data records as they flow through multi-stage extraction, transformation, and curation pipelines. This skill ensures that denormalized final tables maintain explicit links to original source records, enabling reproducibility and traceability of derived data.

## When to use

When consolidating entries from multiple heterogeneous source databases into a unified table, and you need to maintain auditable connections between final curated records and their original source entries. Specifically: (1) you have loaded cleaned subgraph tables (organism, structure, reference) from different intermediate stages, (2) you are performing sequential join operations to denormalize them, and (3) you require proof that all rows from the original table are preserved and can be traced back.

## When NOT to use

- The input tables are already fully deduplicated and do not need row-level traceability.
- You are performing destructive transformations (e.g., aggregation or sampling) where intermediate rows are intentionally discarded; use validation and sampling skills instead.
- Original source identifiers are not available or have already been removed from the dataset.

## Inputs

- Original integrated table (interim/tables/0_original/table.tsv.gz)
- Cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz)
- Translated structure table (interim/tables/1_translated/structure/final.tsv.gz)
- Named structure table (interim/tables/2_cleaned/structure/named.tsv.gz)
- NP-classifier structure annotations (interim/dictionaries/structure/npclassifier/smiles_np_classified.tsv.gz)
- Cleaned reference table (interim/tables/2_cleaned/reference/cleaned.tsv.gz)

## Outputs

- Curated denormalized table (interim/tables/3_curated/table.tsv.gz) with all columns consolidated and original record identifiers preserved
- Organism dictionary and metadata (interim/dictionary/organism/dictionary.tsv.gz, interim/dictionary/organism/metadata.tsv.gz)
- Structure dictionary and metadata (interim/dictionary/structure/dictionary.tsv.gz, interim/dictionary/structure/metadata.tsv.gz)
- Reference-organism mapping dictionary and metadata (interim/dictionary/reference/dictionaryOrganism.tsv.gz, interim/dictionary/reference/metadata.tsv.gz)

## How to apply

Load the original integrated table first (e.g., interim/tables/0_original/table.tsv.gz) to establish a baseline record set with original identifiers. Then perform left join operations in sequence, joining organism data by organism_id, structure data by structure_id, and reference data by reference_id from their respective cleaned/translated intermediate stages. Append NP-classifier annotations by SMILES or structure identifier. Before consolidating into the final denormalized table (interim/tables/3_curated/table.tsv.gz), validate that: (a) row counts match or exceed the original, (b) original identifiers are preserved in output columns, (c) all join operations are left-outer (not inner), and (d) any rows with missing values in joined fields are explicitly flagged or documented. Compress output and document which intermediate tables contributed to each column.

## Related tools

- **R** (Execute 1_integrating.R script to perform sequential join operations and consolidate subgraph tables) — https://github.com/lotusnprod/lotus-processor
- **data.table** (Efficient join and aggregation operations on large TSV tables in R)

## Examples

```
Rscript 1_integrating.R --original interim/tables/0_original/table.tsv.gz --organisms interim/tables/2_cleaned/organism/cleaned.tsv.gz --structures interim/tables/1_translated/structure/final.tsv.gz --references interim/tables/2_cleaned/reference/cleaned.tsv.gz --output interim/tables/3_curated/table.tsv.gz
```

## Evaluation signals

- Row count of final table ≥ row count of original table; any reduction must be justified and documented.
- All original record identifiers present in output; no silent dropping of rows during joins.
- Join operations are left-outer (verified by presence of all original_id values in final table).
- Derived dictionaries (organism, structure, reference) extracted from unique entries and contain expected metadata columns.
- Spot-check: randomly select 5–10 rows from final table and trace each back to its original source and intermediate tables; all lookups must succeed.

## Limitations

- If intermediate cleaned tables have already deduplicated or filtered records, row count preservation cannot be guaranteed from the original alone; document filtering rationale at each stage.
- Join keys (organism_id, structure_id, reference_id) must be stable across all intermediate tables; mismatched or missing keys will result in unmapped rows or NULL values in output.
- Large denormalized tables (588694+ rows as in LOTUS) require sufficient memory for in-memory join operations; streaming or chunked processing may be needed on resource-constrained systems.
- No automatic detection of conflicting values when the same join key appears with different attribute values in source tables; manual conflict resolution required.

## Evidence

- [methods] The 2_curating stage uses 1_integrating.R to consolidate entries through organism, structure, and reference subgraphs, producing an integrated curated table.: "The 2_curating stage uses 1_integrating.R to consolidate entries through organism, structure, and reference subgraphs, producing an integrated curated table."
- [methods] Load the original integrated table from interim/tables/0_original/table.tsv.gz to preserve original record identifiers and lineage.: "Load the original integrated table from interim/tables/0_original/table.tsv.gz to preserve original record identifiers and lineage."
- [methods] Perform left join operations in sequence: join organisms by organism_id, join structure data by structure_id, join reference data by reference_id, and append NP-classifier annotations by SMILES or structure identifier.: "Perform left join operations in sequence: join organisms by organism_id, join structure data by structure_id, join reference data by reference_id, and append NP-classifier annotations by SMILES or"
- [methods] Consolidate all columns into a single denormalized table and compress to interim/tables/3_curated/table.tsv.gz, ensuring all rows from the original table are preserved and validated entries are flagged.: "Consolidate all columns into a single denormalized table and compress to interim/tables/3_curated/table.tsv.gz, ensuring all rows from the original table are preserved and validated entries are"
- [intro] LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research: "*LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research"
- [methods] 588694 unique referenced structure-organism pairs (484174 in 3D|2D format): "588694 unique referenced structure-organism pairs (484174 in 3D|2D format)"
