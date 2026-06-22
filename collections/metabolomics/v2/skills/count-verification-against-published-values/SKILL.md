---
name: count-verification-against-published-values
description: Use when when you have access to a curated dataset (such as LOTUS) with published headline statistics in a peer-reviewed article or enriched index, and you need to validate data integrity, trace reporting accuracy, or establish a reproducible baseline before downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0219
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

# count-verification-against-published-values

## Summary

Independently reproduce and verify aggregate counts of key entities (structure-organism pairs, unique structures, organisms, source databases) from a published natural products dataset by loading curated data files, deduplicating on identifier columns, and comparing results against reported values with absolute and relative difference metrics.

## When to use

When you have access to a curated dataset (such as LOTUS) with published headline statistics in a peer-reviewed article or enriched index, and you need to validate data integrity, trace reporting accuracy, or establish a reproducible baseline before downstream analysis. Use this skill specifically when the source provides TSV/CSV structure-organism pair tables with organism and structure identifier columns, and published counts for both 2D and 3D variants separately.

## When NOT to use

- The dataset has not been released publicly or access restrictions prevent reproducible download.
- Published statistics are reported only as aggregate totals without 2D/3D stratification, preventing independent verification of dimensional variants.
- Source data files are in proprietary formats (e.g. Excel, closed databases) without standardized TSV/CSV exports.

## Inputs

- 3D structure-organism pair table (TSV or CSV with structure_id and organism_id columns)
- 2D structure-organism pair table (TSV or CSV with structure_id and organism_id columns)
- Dataset metadata or source attribution table (to enumerate database identifiers)
- Published headline statistics (structure-organism pair counts, structure counts, organism counts, database counts)

## Outputs

- Verification table with columns: entity_type, dimensionality (2D|3D), observed_count, published_count, absolute_difference, relative_percent_difference
- Boolean validation result (counts match within acceptable tolerance)

## How to apply

Download the dataset deposit from the cited repository (e.g. Zenodo record 3778405 for LOTUS) and extract the 3D and 2D structure-organism pair tables in TSV or CSV format. Load the files into R or Python and count unique referenced structure-organism pairs by grouping on the structure identifier and organism identifier columns; repeat this separately for 3D and 2D tables. Independently count unique curated structure identifiers by deduplicating the structure ID field across 3D and 2D datasets separately (do not merge). Count unique organism identifiers across all structure-organism records to obtain the total organism count. Enumerate source database identifiers present in metadata or attribution columns. Compile all counts into a verification table with columns for observed count, published count, absolute difference, and relative percent difference. Compare each observed count against the published value; a relative difference of ≤1% typically indicates correct reproduction, while deviations >1% warrant investigation of data filtering, version changes, or processing pipeline differences.

## Related tools

- **R** (Load TSV/CSV tables, deduplicate identifier columns using dplyr/data.table, compute counts via group_by and n_distinct(), generate comparison tables) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Load TSV/CSV with pandas, deduplicate using drop_duplicates() on identifier columns, compute unique counts via groupby and nunique(), compute absolute and relative differences) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# Load 3D and 2D pair tables and verify counts
df_3d <- read.csv('structure_organism_3d.tsv', sep='\t')
df_2d <- read.csv('structure_organism_2d.tsv', sep='\t')
pairs_3d <- nrow(df_3d)
pairs_2d <- nrow(df_2d)
structures_3d <- n_distinct(df_3d$structure_id)
structures_2d <- n_distinct(df_2d$structure_id)
organisms <- n_distinct(c(df_3d$organism_id, df_2d$organism_id))
verification <- data.frame(entity=c('pairs_3d', 'pairs_2d', 'structures_3d', 'structures_2d', 'organisms'), observed=c(pairs_3d, pairs_2d, structures_3d, structures_2d, organisms), published=c(588694, 484174, 231330, 153956, 42166), percent_diff=round(100*(c(pairs_3d, pairs_2d, structures_3d, structures_2d, organisms)-c(588694, 484174, 231330, 153956, 42166))/c(588694, 484174, 231330, 153956, 42166), 2))
```

## Evaluation signals

- Observed counts for 3D structure-organism pairs match published value (588,694) within ±1 relative percent difference.
- Observed counts for 2D structure-organism pairs match published value (484,174) within ±1 relative percent difference.
- Observed count of unique 3D structures matches published value (231,330) within ±1 relative percent difference.
- Observed count of unique 2D structures matches published value (153,956) within ±1 relative percent difference.
- Observed count of unique organisms matches published value (42,166) within ±1 relative percent difference; enumerated source databases match published count of 31.

## Limitations

- Verification depends on dataset version consistency; updates or re-releases may alter counts, necessitating comparison against the specific version cited in the published article.
- Published statistics may reflect intermediate processing steps (e.g. after curation but before validation filtering); pipeline version differences can lead to discrepancies even with correct reproduction logic.
- Deduplication logic assumes identifier fields are correctly populated and standardized across all rows; missing, null, or inconsistently formatted identifiers will reduce observed counts and complicate root-cause analysis.

## Evidence

- [other] LOTUS contains 588,694 (3D) and 484,174 (2D) unique referenced structure-organism pairs, 231,330 (3D) and 153,956 (2D) unique curated structures, 42,166 unique organisms, and 31 source databases.: "LOTUS contains 588,694 (3D) and 484,174 (2D) unique referenced structure-organism pairs, 231,330 (3D) and 153,956 (2D) unique curated structures, 42,166 unique organisms, and 31 source databases."
- [other] Count unique referenced (raw) structure-organism pairs by grouping on structure identifier and organism identifier columns.: "count unique referenced (raw) structure-organism pairs by grouping on structure identifier and organism identifier columns"
- [other] Count unique curated structure identifiers across the 3D and 2D datasets separately by deduplicating the structure ID field.: "Count unique curated structure identifiers across the 3D and 2D datasets separately by deduplicating the structure ID field"
- [other] Compile all counts into a verification table and compare against the reported values with absolute and relative difference columns.: "Compile all counts into a verification table and compare against the reported values with absolute and relative difference columns"
- [readme] LOTUS is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented structure-organism pairs should allow a more complete understanding of organisms and their chemistry.: "LOTUS is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented"
