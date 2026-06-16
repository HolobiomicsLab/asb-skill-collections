---
name: database-metadata-enumeration
description: Use when when you have downloaded a curated structure-organism dataset (such as LOTUS) and need to verify the reported counts of unique entities (source databases, organisms, structures, and their pairs) to confirm dataset integrity, assess data coverage, or reproduce published statistics in a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Python 3
  - lotus-processor
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- standardizing.R, 1_integrating.R, 1_cleaningOriginal.R, 4_cleaningTaxonomy.R, 5_addingOTL.R
- 1_integrating.R
- 221[[smiles.py]], 260[[3_cleaningAndEnriching/sanitizing.py]], 280[[3_cleaningAndEnriching/stereocounting.py]]
- R - Python 3 - Java >= 17
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus
schema_version: 0.2.0
---

# database-metadata-enumeration

## Summary

Enumerate and count distinct database sources, organisms, structures, and structure-organism pairs within a curated natural products dataset to verify dataset composition and metadata completeness. This skill validates the scale and scope of a data collection against documented headline statistics.

## When to use

When you have downloaded a curated structure-organism dataset (such as LOTUS) and need to verify the reported counts of unique entities (source databases, organisms, structures, and their pairs) to confirm dataset integrity, assess data coverage, or reproduce published statistics in a methods section or supplementary material.

## When NOT to use

- If the input data is already aggregated or summarized (i.e., not at the raw structure-organism pair row level), direct enumeration will not work; you must trace back to the original pair-level tables.
- If source database attribution is missing or encoded in a non-standardized way in your dataset version, enumeration of source databases may be incomplete or unreliable.
- If you only have 2D structures but the reported statistic separates 3D and 2D counts, you cannot independently verify the split.

## Inputs

- Structure-organism pair TSV/CSV files (3D and 2D variants)
- Dataset metadata or source attribution columns
- Zenodo dataset deposit (record 3778405 or equivalent)

## Outputs

- Verification table with counts of unique structure-organism pairs, structures, organisms, and source databases
- Absolute and relative difference columns comparing reported vs. computed values
- Boolean validation result (all counts match or discrepancies identified)

## How to apply

Load the TSV or CSV structure-organism pair tables (available in 3D and 2D variants) into R or Python. For each entity type, apply deduplication by grouping on the relevant identifier column: count unique structure identifiers across the dataset, count unique organism identifiers, count unique structure-organism pair references (raw/unreferenced pairs), and enumerate source database identifiers from the metadata or source attribution columns. Organize counts separately by dimensionality (3D vs 2D) if applicable. Compile all counts into a verification table, then compare each reported value against your computed values using absolute difference (count_reported − count_computed) and relative percentage difference ((|difference| / count_reported) × 100). Use this comparison to identify any discrepancies that may indicate missing data, filtering steps, or version differences.

## Related tools

- **R** (Load TSV/CSV files, perform deduplication, count unique identifiers, and construct verification tables using base R or dplyr group_by/summarise operations.) — https://www.r-project.org/
- **Python 3** (Load structure-organism pair files (using pandas), deduplicate records, count unique entities by column grouping, and generate comparison tables.) — https://www.python.org/
- **lotus-processor** (Reference implementation and workflow orchestration for LOTUS dataset processing; includes standardization, cleaning, and integration steps that precede enumeration.) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# R example: load and count unique pairs
library(readr)
pairs_3d <- read_tsv('lotus_3d_pairs.tsv.gz')
n_pairs_3d <- n_distinct(pairs_3d$structure_id, pairs_3d$organism_id)
n_structures_3d <- n_distinct(pairs_3d$structure_id)
n_organisms <- n_distinct(c(pairs_3d$organism_id, pairs_2d$organism_id))
n_databases <- length(unique(pairs_3d$source_db))
verification <- data.frame(entity=c('pairs_3d','structures_3d','organisms','databases'), reported=c(588694,231330,42166,31), computed=c(n_pairs_3d,n_structures_3d,n_organisms,n_databases))
```

## Evaluation signals

- Reported count of structure-organism pairs (588,694 for 3D and 484,174 for 2D) matches your enumeration with relative difference ≤ 2%.
- Reported count of unique curated structures (231,330 for 3D and 153,956 for 2D) matches your deduplication output.
- Reported count of unique organisms (42,166 across all data) is reproducible by aggregating organism identifiers across both 3D and 2D files.
- Reported count of source databases (31 initial open databases) can be confirmed by enumerating distinct source identifiers in metadata.
- All enumeration counts are consistent across multiple independent runs, and the relative differences lie within measurement and versioning variance (typically < 5%).

## Limitations

- Enumeration results are sensitive to dataset version and snapshot date; the LOTUS dataset is regularly updated, so counts will differ between Zenodo deposits and git snapshots.
- If structure or organism identifiers contain whitespace, encoding issues, or duplicated representations (e.g., synonym variants), naive deduplication may overcount or undercount unique entities.
- Source database attribution may be incomplete, missing, or encoded differently across legacy or newly added data sources, making enumeration of the 31 databases fragile.
- 3D/2D separation is a characteristic of the LOTUS dataset; other structure-organism datasets may not have this dimension, limiting transferability.

## Evidence

- [methods] LOTUS dataset composition: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
- [methods] Curated structures count: "231330 | 153956 (3D|2D) unique curated structures"
- [methods] Organism uniqueness: "42166 unique organisms"
- [methods] Source database enumeration: "originating from 31 initial open databases"
- [other] Workflow for enumeration: "count unique referenced (raw) structure-organism pairs by grouping on structure identifier and organism identifier columns"
- [readme] Data format and source: "Download the LOTUS dataset deposit from Zenodo (record 3778405) and extract the curated structure-organism tables in TSV or CSV format"
