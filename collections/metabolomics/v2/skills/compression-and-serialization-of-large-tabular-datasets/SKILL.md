---
name: compression-and-serialization-of-large-tabular-datasets
description: Use when when consolidating multiple cleaned and validated data sources (organism, structure, reference subgraphs) into a single denormalized table containing hundreds of thousands of rows and many columns, and the result must be stored, archived, or transmitted with minimal storage overhead while.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3174
  tools:
  - R
  - R data.table
  - gzip
  - 1_integrating.R
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

# compression-and-serialization-of-large-tabular-datasets

## Summary

Serialize and compress large denormalized tabular datasets into compressed columnar formats (e.g., .tsv.gz) to enable efficient storage, transport, and downstream processing of structure-organism-reference tables. This skill ensures that consolidated multi-source data can be preserved without loss while reducing disk footprint.

## When to use

When consolidating multiple cleaned and validated data sources (organism, structure, reference subgraphs) into a single denormalized table containing hundreds of thousands of rows and many columns, and the result must be stored, archived, or transmitted with minimal storage overhead while maintaining row integrity and lineage information.

## When NOT to use

- Input table is already in a columnar binary format (e.g., Parquet, HDF5) — use columnar export instead.
- Downstream analysis requires random-access to individual rows or requires the table to remain in memory decompressed — consider alternative storage formats.
- The dataset is too small (<10 MB uncompressed) to justify compression overhead — store as plain TSV.

## Inputs

- denormalized tabular dataset (R data.frame or data.table with structure-organism-reference columns)
- cleaned organism table (interim/tables/2_cleaned/organism/cleaned.tsv.gz)
- cleaned structure table (interim/tables/2_cleaned/structure/named.tsv.gz)
- cleaned reference table (interim/tables/2_cleaned/reference/cleaned.tsv.gz)
- original integrated table with preserved identifiers (interim/tables/0_original/table.tsv.gz)

## Outputs

- compressed curated table (interim/tables/3_curated/table.tsv.gz)
- denormalized .tsv.gz archive suitable for Zenodo deposition

## How to apply

After performing sequential left join operations to consolidate organism, structure, reference, and annotation data into a single denormalized table, serialize the result to a tab-separated values (.tsv) format using R data.table or equivalent, then compress using gzip (producing .tsv.gz). Ensure all rows from the original table are preserved during joins, and flag validated entries to enable downstream filtering. The compression step reduces the denormalized table to a portable, archivable format suitable for both immediate downstream analysis and long-term Zenodo deposition. Decompress only when needed for analysis to minimize I/O.

## Related tools

- **R data.table** (Serialize denormalized table to tab-separated format with efficient column and row handling)
- **gzip** (Compress TSV to .tsv.gz format for archival and transport)
- **1_integrating.R** (Perform left join operations to consolidate organism, structure, and reference subgraphs before serialization) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# In R, after consolidating organism/structure/reference tables:
final_table <- fread('interim/tables/3_curated/table.tsv.gz')
fwrite(final_table, 'interim/tables/3_curated/table.tsv', sep='\t')
system('gzip -f interim/tables/3_curated/table.tsv')
```

## Evaluation signals

- Output file exists at interim/tables/3_curated/table.tsv.gz with non-zero size and valid gzip magic number.
- Decompressed .tsv.gz contains all rows from the original table (row count preserved or increased by validated entries only).
- All organism_id, structure_id, and reference_id foreign keys are present and non-null in the denormalized table before compression.
- Gzip compression reduces file size to <50% of uncompressed TSV (typical for structured data with redundancy).
- Downstream processes (e.g., 3_analyzing stage) can successfully decompress and load the table without corruption.

## Limitations

- Compression overhead (gzip) is negligible for large tables but may not be worthwhile for very small datasets (<10 MB).
- Denormalization increases table size compared to normalized schema, so compression is critical for archival and transport.
- Random access to individual rows requires full decompression; use columnar formats (Parquet) if frequent partial access is needed.
- The article does not specify a maximum row count or column count validation threshold, so consumer processes must handle arbitrary scale.

## Evidence

- [methods] Consolidate all columns into a single denormalized table and compress to interim/tables/3_curated/table.tsv.gz, ensuring all rows from the original table are preserved and validated entries are flagged.: "Consolidate all columns into a single denormalized table and compress to interim/tables/3_curated/table.tsv.gz, ensuring all rows from the original table are preserved and validated entries are"
- [other] 588694 unique referenced structure-organism pairs (484174 in 3D|2D format): "588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
- [other] 231330 unique curated structures in 3D and 153956 in 2D format from 42166 unique organisms: "231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms"
- [readme] Outputs of the lotus-processor will be regularly archived at https://zenodo.org/record/5665295: "Outputs of the lotus-processor will be regularly archived at https://zenodo.org/record/5665295"
