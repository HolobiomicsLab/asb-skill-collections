---
name: structure-organism-pair-counting-and-deduplication
description: Use when when you have downloaded a curated structure-organism dataset (such as LOTUS) in TSV or CSV format with separate 2D and 3D structure-organism pair tables, and need to produce authoritative headline counts of unique referenced pairs, unique curated structures, unique organisms, and source.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0154
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

# structure-organism-pair-counting-and-deduplication

## Summary

Count and deduplicate structure-organism pairs and their constituent entities (unique structures, organisms, references) from curated natural products databases, separately for 2D and 3D molecular representations. This skill validates dataset integrity and produces summary statistics essential for understanding the scope and composition of structure-organism knowledge bases.

## When to use

When you have downloaded a curated structure-organism dataset (such as LOTUS) in TSV or CSV format with separate 2D and 3D structure-organism pair tables, and need to produce authoritative headline counts of unique referenced pairs, unique curated structures, unique organisms, and source databases to verify dataset completeness or support comparative analysis.

## When NOT to use

- Input files are already preprocessed into deduplicated summary counts (rather than raw pair records)
- The dataset combines 2D and 3D representations without explicit dimensionality labeling, making separate quantification impossible
- Source attribution metadata is missing or inconsistent, preventing reliable enumeration of source databases

## Inputs

- 3D structure-organism pair table (TSV or CSV with structure identifier, organism identifier, and source attribution columns)
- 2D structure-organism pair table (TSV or CSV with structure identifier, organism identifier, and source attribution columns)
- Dataset metadata or source attribution reference table

## Outputs

- Verification table with counts of unique referenced structure-organism pairs (3D and 2D)
- Count of unique curated structures (3D and 2D)
- Count of unique organisms across all records
- Count of source databases enumerated from metadata
- Summary comparison table with absolute and relative differences against reported values

## How to apply

Load the 3D and 2D structure-organism pair files separately using R or Python. For each dimensionality: (1) count unique referenced (raw) structure-organism pairs by grouping on structure identifier and organism identifier columns and removing duplicates; (2) count unique curated structure identifiers by deduplicating the structure ID field; (3) count unique organism identifiers across all records; (4) enumerate distinct source database identifiers from metadata or source attribution columns. Compile counts into a verification table with absolute and relative difference columns comparing observed counts against expected or previously reported values. The 2D and 3D counts should be reported separately to reflect the distinct molecular representations in the dataset.

## Related tools

- **R** (Load TSV/CSV files, group by structure and organism identifiers, deduplicate records, and aggregate counts into verification tables) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Load and parse structure-organism pair files, apply deduplication via pandas groupby or set operations, and generate summary statistics) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# Load and count in R
library(data.table)
pairs_3d <- fread('structure_organism_pairs_3d.tsv')
pairs_2d <- fread('structure_organism_pairs_2d.tsv')
cat('3D pairs:', nrow(unique(pairs_3d[, .(structure_id, organism_id)])), '\n')
cat('Unique 3D structures:', length(unique(pairs_3d$structure_id)), '\n')
cat('Unique organisms:', length(unique(c(pairs_3d$organism_id, pairs_2d$organism_id))), '\n')
```

## Evaluation signals

- Reported 3D and 2D unique referenced pair counts match or are within documented tolerance of 588,694 and 484,174 respectively
- Reported 3D and 2D unique curated structure counts match or are within tolerance of 231,330 and 153,956 respectively
- Reported unique organism count matches or is within tolerance of 42,166
- Enumerated source database count matches or is within tolerance of 31 initial open databases
- Verification table shows minimal absolute differences (< 1%) between observed and reported values, indicating data integrity

## Limitations

- Counts depend critically on consistent and complete structure and organism identifier fields; missing or null identifiers will underestimate unique entity counts
- Source database attribution must be present and standardized in the dataset; inconsistent naming or missing metadata will make enumeration unreliable
- Separate 2D/3D counts assume clear dimensionality labeling in the source tables; ambiguous or mixed representations cannot be reliably separated
- Large datasets may require memory-efficient grouping or streaming approaches; loading entire TSV files into memory may fail on resource-constrained systems

## Evidence

- [other] 588,694 (3D) and 484,174 (2D) unique referenced structure-organism pairs, 231,330 (3D) and 153,956 (2D) unique curated structures, 42,166 unique organisms, and 31 source databases: "The EnrichedIndex reports LOTUS contains 588,694 (3D) and 484,174 (2D) unique referenced structure-organism pairs, 231,330 (3D) and 153,956 (2D) unique curated structures, 42,166 unique organisms,"
- [other] Count unique referenced (raw) structure-organism pairs by grouping on structure identifier and organism identifier columns: "count unique referenced (raw) structure-organism pairs by grouping on structure identifier and organism identifier columns"
- [other] Count unique curated structure identifiers across the 3D and 2D datasets separately by deduplicating the structure ID field: "Count unique curated structure identifiers across the 3D and 2D datasets separately by deduplicating the structure ID field."
- [other] Count unique organism identifiers across all structure-organism records to obtain the organism total: "Count unique organism identifiers across all structure-organism records to obtain the organism total."
- [other] Enumerate the source database identifiers present in the dataset metadata or source attribution columns to verify the count of 31 initial databases: "Enumerate the source database identifiers present in the dataset metadata or source attribution columns to verify the count of 31 initial databases."
- [other] Compile all counts into a verification table and compare against the reported values with absolute and relative difference columns: "Compile all counts into a verification table and compare against the reported values with absolute and relative difference columns."
