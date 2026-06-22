---
name: structure-organism-pair-deduplication
description: Use when you have a curated natural products dataset (e.g., LOTUS platinum validation dataset in TSV format) and need to establish ground-truth counts of unique chemical structures, unique organisms, and unique referenced structure-organism associations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0621
  tools:
  - R
  - Python 3
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
- Python scripts for data parsing and transformation
- 221[[smiles.py]]
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

# structure-organism-pair-deduplication

## Summary

Deduplicate and count unique structure-organism pairs and their constituent entities (structures, organisms) in a curated natural products dataset, stratified by molecular representation format (2D/3D). This skill validates dataset completeness and integrity by confirming expected aggregate counts across multiple deduplication dimensions.

## When to use

Apply this skill when you have a curated natural products dataset (e.g., LOTUS platinum validation dataset in TSV format) and need to establish ground-truth counts of unique chemical structures, unique organisms, and unique referenced structure-organism associations. Use it as a validation step after dataset curation and before downstream analyses that depend on knowing population sizes, sampling biases, or redundancy patterns.

## When NOT to use

- Dataset has not yet been curated or cleaned; deduplication of uncleaned data may produce misleading or inflated counts.
- Structure identifiers are not standardized (e.g., multiple SMILES or InChI variants for the same chemical); deduplication will fail or require upstream canonicalization.
- Organism taxonomy identifiers lack a unified scheme; cross-database or non-standardized identifiers will inflate organism counts.

## Inputs

- Curated structure-organism pair dataset in TSV or gzipped TSV format (platinum.tsv.gz)
- Column schema defining organism identifier field, structure identifier field(s), and molecular representation format field

## Outputs

- Deduplicated structure counts (stratified by 2D/3D representation)
- Deduplicated organism counts
- Deduplicated structure-organism pair counts (stratified by 2D/3D representation)
- Summary table (CSV/TSV) with rows for each metric, columns for count, format, and validation status

## How to apply

Load the curated dataset (e.g., platinum.tsv.gz) into R or Python. Extract and deduplicate structure identifiers (SMILES, InChI, or nominal identifiers) separately for 3D and 2D molecular representations by grouping on the structure field and counting unique entries per format. Extract and deduplicate organism taxonomy identifiers by grouping on the organism field and counting unique entries. Extract and deduplicate structure-organism pair combinations by grouping on both structure and organism fields together, again stratified by 2D/3D format. Compare observed counts against expected aggregates (e.g., 231,330 unique 3D structures, 153,956 unique 2D structures, 42,166 unique organisms, 588,694 total pairs with 484,174 in 3D|2D format). Export results to a structured summary table (CSV or TSF) with rows for each metric type and columns for count value, data format, and validation status.

## Related tools

- **R** (Execute deduplication logic via dplyr/tidyverse pipelines (group_by, distinct, summarize) on in-memory or chunked data frames) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Load, deduplicate, and aggregate structure-organism pairs using pandas (groupby, drop_duplicates, value_counts) or polars for large-scale datasets) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# R example
library(tidyverse)
platinum <- read_tsv("interim/tables/4_analysed/platinum.tsv.gz")
unique_structures_3d <- platinum %>% filter(format == "3D") %>% distinct(structure_id) %>% nrow()
unique_organisms <- platinum %>% distinct(organism_id) %>% nrow()
unique_pairs_3d <- platinum %>% filter(format == "3D") %>% distinct(structure_id, organism_id) %>% nrow()
summary_table <- tibble(metric = c("unique_structures_3d", "unique_organisms", "unique_pairs_3d"), count = c(unique_structures_3d, unique_organisms, unique_pairs_3d))
write_csv(summary_table, "summary_metrics.csv")
```

## Evaluation signals

- Observed counts match expected aggregates within a tolerance (e.g., ≤ 0.1% difference from reported 231,330 3D structures, 153,956 2D structures, 42,166 organisms, 588,694 total pairs).
- Deduplication produces a stable result (rerunning the workflow on the same input yields identical counts).
- Summary table is well-formed: rows represent distinct metric types, columns are consistent across rows, count values are non-negative integers, format labels are consistent (e.g., '3D', '2D', or 'combined').
- No structures or organism–pair combinations are double-counted within a format stratum; sum of 2D and 3D pair counts equals or is consistent with the total reported pairs.
- Deduplication preserves referential integrity: every structure in a pair exists in the structure-only deduplication, and every organism in a pair exists in the organism-only deduplication.

## Limitations

- Deduplication assumes structure identifiers and organism identifiers are already canonicalized and standardized; mixed or non-normalized representations (e.g., different SMILES dialects, mixed taxonomy schemes) will not be collapsed correctly.
- 2D/3D format stratification requires an explicit format column in the dataset; absent or inconsistent format labels may lead to miscounts.
- Large datasets (> 500 million pairs) may require chunked or out-of-core processing in R or Python to avoid memory exhaustion; in-memory deduplication assumes sufficient RAM.

## Evidence

- [methods] Extract and deduplicate structure identifiers (SMILES, InChI, or nominal identifiers) separately for 3D and 2D molecular representations: "Extract and deduplicate structure identifiers (SMILES, InChI, or nominal identifiers) to count unique curated structures, separately for 3D and 2D structure representations."
- [methods] 231330 unique curated structures in 3D and 153956 in 2D format from 42166 unique organisms, with 588694 unique referenced structure-organism pairs: "231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms... 588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
- [readme] LOTUS is a comprehensive collection of documented structure-organism pairs within natural products research: "*LOTUS* is a comprehensive collection of documented structure-organism pairs."
- [readme] R and Python 3 are the required tools for processing workflows: "R, Python 3, Java >= 17"
- [methods] Export counts to a structured summary table with rows for each metric and columns for count value and data format: "Export counts to a structured summary table (CSV or TSV) with rows for each metric and columns for count value and data format."
