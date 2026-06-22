---
name: flat-file-parsing-and-loading
description: Use when when you have published LOTUS flat files (TSV or compressed TSV.GZ) containing structure-organism pairs and need to enumerate unique structures, group by organism prevalence, or validate record counts against gold-standard benchmarks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Python 3
  - R (data.table, base read.csv)
  - Python 3 (pandas.read_csv, gzip)
  - Make
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

# flat-file-parsing-and-loading

## Summary

Parse and load structure-organism pair data from published LOTUS flat files into memory, extracting documented 2D/3D structure identifiers, organism associations, and reference metadata for subsequent binning and validation. This is a foundational data ingestion step that establishes the integrity of source records before downstream analysis.

## When to use

When you have published LOTUS flat files (TSV or compressed TSV.GZ) containing structure-organism pairs and need to enumerate unique structures, group by organism prevalence, or validate record counts against gold-standard benchmarks. Apply this skill as the first step in any replication or extension of LOTUS-based analyses.

## When NOT to use

- Data is already loaded in memory or in a relational database; use direct schema queries instead.
- Input is a proprietary binary format (HDF5, Parquet) without documented LOTUS correspondence; confirm file origin first.
- Organism counts or structure identifiers have already been binned; this skill is redundant if the source file has been preprocessed.

## Inputs

- LOTUS published flat file (TSV or TSV.GZ format)
- structure-organism pair records with columns: structure ID, organism taxon, reference metadata

## Outputs

- in-memory table (R data.frame, Python DataFrame) with all structure-organism pairs
- load summary report documenting row count, column schema, and validation status

## How to apply

Load the published LOTUS flat file(s) using language-native table parsers (R data.table, Python pandas) that preserve column names and data types. Retain all columns for structure identifiers (2D/3D), organism references, and source citations. Parse compressed formats (TSV.GZ) directly without manual decompression. Validate that the total number of rows matches the documented reference counts (e.g., 588694 | 484174 for 3D|2D unique referenced structure-organism pairs); if discrepancies appear, flag them for investigation before proceeding to grouping or binning operations. Document the exact file path, load timestamp, and row/column schema in a summary report.

## Related tools

- **R (data.table, base read.csv)** (parse and load TSV/TSV.GZ files into R data.frame or data.table for fast row enumeration and schema validation) — https://github.com/lotusnprod/lotus-processor
- **Python 3 (pandas.read_csv, gzip)** (parse TSV/TSV.GZ files into pandas DataFrame; handle decompression and column type inference) — https://github.com/lotusnprod/lotus-processor
- **Make** (orchestrate flat-file loading as a reproducible workflow step within the LOTUS processor pipeline) — https://github.com/lotusnprod/lotus-processor

## Examples

```
library(data.table); lotus_2d <- fread('LOTUS_2D_structure_organism_pairs.tsv.gz'); cat(nrow(lotus_2d), 'rows loaded; expected 484174 for 2D pairs')
```

## Evaluation signals

- Row count of loaded table matches published gold-standard counts (588694 for 3D pairs, 484174 for 2D pairs, or subset thereof).
- All expected columns are present (structure identifier, organism, reference); no silent data loss or truncation.
- No parsing errors or warnings; compression handling (GZ) succeeds without manual decompression.
- Summary report documents load timestamp, file path, row/column dimensions, and any missing or malformed records.
- Unique structure and organism counts can be verified post-load (e.g., 231330 | 153956 curated structures for 3D|2D; 42166 unique organisms).

## Limitations

- LOTUS flat files are snapshots; if the underlying database is updated, files must be re-downloaded from Zenodo to reflect current data.
- TSV format is line-delimited text; very large files (>10 GB) may require streaming or chunked reading to fit in memory.
- No built-in integrity checks for malformed organism names or duplicate structure–organism pairs within the file; downstream cleaning steps are required.
- Organism or structure identifiers may contain special characters or encodings; ensure appropriate locale/encoding settings (UTF-8) during parsing.

## Evidence

- [methods] Load the LOTUS 2D structure-organism pairs table from the published flat file.: "Load the LOTUS 2D structure-organism pairs table from the published flat file."
- [methods] 588694 | 484174 (3D|2D) unique referenced structure-organism pairs: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
- [readme] The data used to support the findings of this study have been deposited on Zenodo [https://zenodo.org/communities/the-lotus-initiative]. A snapshot of the repository at the time of publication is also available under the same link.: "data used to support the findings of this study have been deposited on Zenodo [https://zenodo.org/communities/the-lotus-initiative]"
- [intro] LOTUS is a comprehensive collection of documented structure-organism pairs designed to enable computational understanding of organisms and their chemistry.: "LOTUS is a comprehensive collection of documented structure-organism pairs designed to enable computational understanding"
- [methods] 231330 | 153956 (3D|2D) unique curated structures; 42166 unique organisms; originating from 31 initial open databases: "231330 | 153956 (3D|2D) unique curated structures; 42166 unique organisms"
