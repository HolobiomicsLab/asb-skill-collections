---
name: natural-product-database-schema-parsing
description: Use when when ingesting raw data from multiple external natural-product
  databases with different formats, field naming conventions, and data structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_2258
  tools:
  - R
  - Python 3
  - Make
  - R (with standardizing.R, common.R scripts)
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
- Python scripts for data parsing and transformation
- 221[[smiles.py]]
- Please make sure to have [Make](https://www.gnu.org/software/make) installed.
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

# natural-product-database-schema-parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse heterogeneous natural-product database formats (TSV, JSON, XML, proprietary schemas) into a unified tabular schema with standardized columns (structure_id, organism, reference, source_db, raw_data). This is the foundational step in aggregating structure-organism pairs from multiple independent sources into a single normalized representation.

## When to use

When ingesting raw data from multiple external natural-product databases with different formats, field naming conventions, and data structures. Apply this skill at the start of a data curation pipeline when you have 31 or more heterogeneous source databases and need to produce a common intermediate tabular format before downstream integration, cleaning, and enrichment.

## When NOT to use

- Data is already in the common schema or has been parsed by a previous run — reuse interim/db/*.tsv outputs directly.
- Source databases are private or proprietary and cannot be accessed or legally ingested into a unified resource.
- You need to validate or enrich the parsed data before integration — defer organism name normalization and reference DOI resolution to downstream cleaning steps (2_curating stage).

## Inputs

- external/dbSource/* (raw databases in TSV, JSON, XML, or proprietary formats)
- database schema documentation or sample records from each source
- source-specific column mappings or data dictionaries

## Outputs

- interim/db/*.tsv (standardized tab-separated tables with columns: structure_id, organism, reference, source_db, raw_data)
- interim/db/organism_taxonomy/*.tsv (partitioned organism records)
- interim/db/structure_metadata/*.tsv (partitioned chemical structure records)
- interim/db/bibliographic_records/*.tsv (partitioned reference metadata)

## How to apply

For each source database in the external/dbSource/ directory, execute a language-specific parsing script (standardizing.R or equivalent) that detects the input format (TSV, JSON, XML, or proprietary schema) and maps source-specific columns to the common schema: structure_id, organism, reference, source_db, and raw_data. Write standardized outputs as tab-separated values into interim/db/*.tsv files partitioned by data type (organism taxonomy, chemical structure metadata, bibliographic records). Validate that output row counts match input source counts and that critical fields (structure_id, organism_name, reference_doi) are not null in >5% of rows. This step preserves source traceability by retaining the original raw_data field while enabling downstream cross-source comparison and deduplication.

## Related tools

- **R (with standardizing.R, common.R scripts)** (Primary parsing engine: detects input format and maps heterogeneous source columns to common schema; handles TSV, JSON, XML input) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Secondary parsing support for format detection and validation of standardized outputs) — https://github.com/lotusnprod/lotus-processor
- **Make** (Orchestrates sequential execution of standardizing.R scripts across all source databases in external/dbSource/) — https://github.com/lotusnprod/lotus-processor

## Examples

```
make MODE=test lotus-bloom
```

## Evaluation signals

- Output row counts match input source counts for each database (no silent row loss during parsing)
- All output *.tsv files conform to the common schema: exactly 5 columns (structure_id, organism, reference, source_db, raw_data) with correct data types
- Null-value frequency in critical fields (structure_id, organism_name, reference_doi) is ≤5% of rows per source database
- Raw source records are completely preserved in the raw_data column, enabling traceability and recovery of unparsed fields
- Partition-specific files (organism_taxonomy/*.tsv, structure_metadata/*.tsv, bibliographic_records/*.tsv) correctly separate data types with no cross-contamination

## Limitations

- Proprietary database schemas or undocumented formats may require manual reverse-engineering; no automated format detection is guaranteed for all legacy systems.
- The common schema (structure_id, organism, reference, source_db, raw_data) is minimal and does not resolve synonym or identifier conflicts — those are addressed in downstream 2_curating stage.
- Large databases (millions of records) may require memory-aware chunking or streaming; no batching strategy is described in the workflow.
- The current approach assumes all 31 databases can be legally ingested; licensing restrictions or access controls must be verified before parsing.

## Evidence

- [methods] For each source database in external/dbSource/, run db/../standardizing.R to parse heterogeneous formats (TSV, JSON, XML, proprietary schemas) into a common schema (columns: structure_id, organism, reference, source_db, raw_data).: "For each source database in external/dbSource/, run db/../standardizing.R to parse heterogeneous formats (TSV, JSON, XML, proprietary schemas) into a common schema"
- [methods] Consolidate standardized outputs into interim/db/*.tsv files partitioned by data type (organism taxonomy, chemical structure metadata, bibliographic records).: "Consolidate standardized outputs into interim/db/*.tsv files partitioned by data type (organism taxonomy, chemical structure metadata, bibliographic records)"
- [methods] Validate output schemas and row counts match input database source counts; verify no critical fields (structure_id, organism_name, reference_doi) are null in >5% of rows.: "Validate output schemas and row counts match input database source counts; verify no critical fields (structure_id, organism_name, reference_doi) are null in >5% of rows"
- [methods] The 1_gathering stage performs external database standardization and translation using R scripts (standardizing.R, common.R, tcm.R) to harmonize data from 31 initial open databases into original tables.: "external database standardization and translation using R scripts (standardizing.R, common.R, tcm.R) to harmonize data from 31 initial open databases"
- [methods] Data originates from 31 initial open databases: "originating from 31 initial open databases"
