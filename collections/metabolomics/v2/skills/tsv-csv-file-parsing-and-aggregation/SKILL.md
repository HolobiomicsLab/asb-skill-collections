---
name: tsv-csv-file-parsing-and-aggregation
description: Use when you have TSV or CSV files containing structure-organism pairs (with columns for structure identifier and organism identifier) and need to count unique pairs, unique structures, unique organisms, or enumerate source database identifiers to validate or report dataset scale.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_2258
  tools:
  - R
  - Python 3
  - R (readr, data.table, dplyr)
  - Python (pandas)
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus
schema_version: 0.2.0
---

# TSV/CSV File Parsing and Aggregation

## Summary

Load delimited structure-organism pair tables (TSV/CSV) from a curated natural products dataset and aggregate them by unique identifiers (structure ID, organism ID) to produce count statistics. This skill is essential for verifying dataset composition and deriving headline metrics for documented structure-organism relationships.

## When to use

You have TSV or CSV files containing structure-organism pairs (with columns for structure identifier and organism identifier) and need to count unique pairs, unique structures, unique organisms, or enumerate source database identifiers to validate or report dataset scale. This applies when reproducing published statistics or auditing data provenance in natural products databases.

## When NOT to use

- Input files are already in memory as aggregated summary tables rather than raw record-level pairs.
- Structure and organism identifiers are not present in the same table or cannot be linked.
- Data format is not delimited text (e.g., binary formats such as HDF5, Parquet, or SQLite databases require different I/O tools).

## Inputs

- TSV or CSV file(s) containing 3D structure-organism pairs with structure ID and organism ID columns
- TSV or CSV file(s) containing 2D structure-organism pairs with structure ID and organism ID columns
- Metadata or source attribution field(s) linking records to source database identifiers

## Outputs

- Count of unique referenced 3D structure-organism pairs (integer)
- Count of unique referenced 2D structure-organism pairs (integer)
- Count of unique 3D curated structure identifiers (integer)
- Count of unique 2D curated structure identifiers (integer)
- Count of unique organism identifiers across all records (integer)
- Count of distinct source database identifiers (integer)
- Verification table with counts, benchmarks, and absolute/relative differences

## How to apply

Load the 3D and 2D structure-organism pair files into a data frame using R (readr or data.table) or Python (pandas). Group records by the structure identifier and organism identifier columns to obtain unique referenced pairs; count these groups separately for 3D and 2D data. Deduplicate the structure ID field across all records to count unique curated structures. Aggregate organism identifiers across all structure-organism records to obtain the organism total. Enumerate the distinct source database identifiers from metadata or source attribution columns. Compile all counts into a verification table and compare absolute and relative differences against reported benchmark values (e.g., 588,694 3D pairs, 231,330 3D structures, 42,166 organisms, 31 source databases).

## Related tools

- **R (readr, data.table, dplyr)** (Load, parse, and aggregate TSV/CSV tables; group by identifiers and count unique values) — https://www.r-project.org/
- **Python (pandas)** (Load, parse, and aggregate TSV/CSV files using DataFrames; group, deduplicate, and count operations) — https://pandas.pydata.org/
- **lotus-processor** (Source repository providing curated LOTUS structure-organism pair datasets and standardized table schemas) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# R example:
library(readr); library(dplyr)
pairs_3d <- read_tsv('structure_organism_3d.tsv')
unique_pairs_3d <- n_distinct(pairs_3d %>% select(structure_id, organism_id))
unique_structures_3d <- n_distinct(pairs_3d$structure_id)
unique_organisms <- n_distinct(c(pairs_3d$organism_id, pairs_2d$organism_id))

# Python example:
import pandas as pd
pairs_3d = pd.read_csv('structure_organism_3d.tsv', sep='\t')
unique_pairs_3d = pairs_3d[['structure_id', 'organism_id']].drop_duplicates().shape[0]
unique_structures_3d = pairs_3d['structure_id'].nunique()
unique_organisms = pd.concat([pairs_3d['organism_id'], pairs_2d['organism_id']]).nunique()
```

## Evaluation signals

- Counts of unique 3D and 2D structure-organism pairs match or closely approximate the reported benchmark values (588,694 and 484,174 respectively), with relative difference < 1%.
- Counts of unique 3D and 2D curated structures match reported benchmarks (231,330 and 153,956), indicating correct deduplication by structure ID.
- Total unique organism identifiers equals or is consistent with the reported value of 42,166, validating organism aggregation across all pairs.
- Enumerated source database identifiers yield a count of 31 initial databases, matching the documented data sources.
- Verification table with absolute and relative difference columns shows all benchmark comparisons and confirms internal consistency (e.g., unique 3D pairs ≥ unique 3D structures).

## Limitations

- Parsing accuracy depends on correct file encoding declaration and consistent delimiter usage; irregular quoting or escape sequences may cause row misalignment.
- Identifier columns must be clean and non-null; missing or malformed identifiers will reduce unique counts and produce false negatives.
- Source database attribution may be inconsistent or absent in some records, making enumeration of the 31 source databases incomplete if relying solely on the primary data table.
- The workflow assumes 3D and 2D datasets are independent files; if data is interleaved or partially overlapping, group-and-count logic must account for dimensional stratification.

## Evidence

- [methods] Download and count unique pairs: "Download the LOTUS dataset deposit from Zenodo (record 3778405) and extract the curated structure-organism tables in TSV or CSV format. Load the 3D and 2D structure-organism pair files using R or"
- [methods] Deduplicate and enumerate identifiers: "Count unique curated structure identifiers across the 3D and 2D datasets separately by deduplicating the structure ID field. Count unique organism identifiers across all structure-organism records to"
- [methods] Reported benchmark statistics: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs, 231330 | 153956 (3D|2D) unique curated structures, 42166 unique organisms, originating from 31 initial open databases"
- [methods] Verification and comparison: "Compile all counts into a verification table and compare against the reported values with absolute and relative difference columns."
- [readme] Required tools: "What you need is: R, Python 3, Java >= 17"
