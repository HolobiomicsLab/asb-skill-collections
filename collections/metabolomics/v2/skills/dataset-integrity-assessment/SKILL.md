---
name: dataset-integrity-assessment
description: Use when when you have downloaded a released version of a structured dataset (e.g., LOTUS from Zenodo) and need to confirm it matches the documented headline statistics before downstream analysis, or when auditing data integrity after ingestion into a processing pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - R
  - Python 3
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus
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

# dataset-integrity-assessment

## Summary

Systematically verify the completeness and accuracy of a curated structure-organism dataset by reproducing reported aggregate statistics (unique pairs, structures, organisms, sources) and comparing observed counts against published benchmarks using absolute and relative difference metrics.

## When to use

When you have downloaded a released version of a structured dataset (e.g., LOTUS from Zenodo) and need to confirm it matches the documented headline statistics before downstream analysis, or when auditing data integrity after ingestion into a processing pipeline.

## When NOT to use

- When comparing counts across different dataset versions or snapshots (use change-tracking instead of direct reproduction).
- When the input files are raw (non-curated) database exports prior to standardization and integration.
- When only a sample or subset of the dataset is available (e.g., test mode); request full dataset release or document the subset scope.

## Inputs

- 3D structure-organism pair TSV/CSV file with structure ID and organism ID columns
- 2D structure-organism pair TSV/CSV file with structure ID and organism ID columns
- Dataset metadata or source attribution file listing database provenance

## Outputs

- Verification table with observed counts, reported counts, absolute differences, and relative differences for all aggregate statistics
- Boolean integrity report indicating pass/fail for each count category

## How to apply

Load the structure-organism pair tables (3D and 2D TSV/CSV files) into R or Python. Group by structure identifier and organism identifier columns to enumerate unique referenced (raw) structure-organism pairs separately for 3D and 2D subsets. Deduplicate the structure ID field across all records to count unique curated structures per dimension. Count unique organism identifiers across all structure-organism records regardless of dimension. Enumerate source database identifiers in the metadata or source attribution columns to verify the documented database count. Compile all counts into a verification table with columns for observed value, reported value, absolute difference, and relative difference (%). Documented targets for LOTUS are: 588,694 (3D) and 484,174 (2D) unique referenced structure-organism pairs; 231,330 (3D) and 153,956 (2D) unique curated structures; 42,166 unique organisms; and 31 initial source databases.

## Related tools

- **R** (Counting and deduplication of structure, organism, and source identifiers; verification table generation) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Data loading, grouping, and statistical comparison of observed versus reported counts) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# R example: Count unique pairs in 3D structure-organism file
lotus_3d <- read.csv('lotus_3d_pairs.tsv', sep='\t')
unique_pairs_3d <- nrow(unique(lotus_3d[, c('structure_id', 'organism_id')]))
unique_structures_3d <- length(unique(lotus_3d$structure_id))
cat('3D pairs:', unique_pairs_3d, '| Expected: 588694 | Diff:', 588694 - unique_pairs_3d)
```

## Evaluation signals

- Observed count of 3D unique referenced structure-organism pairs matches or is within <1% relative difference of 588,694.
- Observed count of 2D unique referenced structure-organism pairs matches or is within <1% relative difference of 484,174.
- Observed unique curated structures (3D and 2D combined or separately) align with reported counts (231,330 for 3D, 153,956 for 2D) within <1% relative difference.
- Observed unique organism count matches or is within <1% relative difference of 42,166.
- Enumerated source database identifiers total 31 or document any discrepancy with explanation (e.g., database mergers, removals).

## Limitations

- This skill reproduces published aggregate statistics only; it does not validate the semantic correctness or taxonomic accuracy of individual organism assignments or structure records.
- Relative difference tolerance thresholds (e.g., <1%) are not explicitly stated in the source material and should be set according to the dataset's version and release notes.
- Source database count verification depends on the presence and format of provenance metadata in the dataset; missing or inconsistently annotated source fields will prevent accurate enumeration.
- The skill assumes TSV/CSV input format; other serializations (JSON, RDF, SQL dumps) require prior format conversion.

## Evidence

- [other] 588,694 (3D) and 484,174 (2D) unique referenced structure-organism pairs, 231,330 (3D) and 153,956 (2D) unique curated structures, 42,166 unique organisms, and 31 source databases: "The EnrichedIndex reports LOTUS contains 588,694 (3D) and 484,174 (2D) unique referenced structure-organism pairs, 231,330 (3D) and 153,956 (2D) unique curated structures, 42,166 unique organisms,"
- [other] Count unique referenced (raw) structure-organism pairs by grouping on structure identifier and organism identifier columns: "Load the 3D and 2D structure-organism pair files using R or Python and count unique referenced (raw) structure-organism pairs by grouping on structure identifier and organism identifier columns."
- [other] Count unique curated structure identifiers and enumerate source database identifiers: "Count unique curated structure identifiers across the 3D and 2D datasets separately by deduplicating the structure ID field. Count unique organism identifiers across all structure-organism records to"
- [other] Compile counts into verification table with absolute and relative difference columns: "Compile all counts into a verification table and compare against the reported values with absolute and relative difference columns."
- [readme] Download the LOTUS dataset deposit from Zenodo: "The data used to support the findings of this study have been deposited on Zenodo. A snapshot of the repository at the time of publication is also available under the same link."
