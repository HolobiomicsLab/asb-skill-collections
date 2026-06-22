---
name: bigscape-output-version-detection-and-compatibility
description: 'Use when when preparing NPLinker input data and the BigScape directory exists but its format is unknown or mixed (e.g., migrated workflows, third-party data, or legacy archives). Specifically: if local mode and BigScape directory is missing, generate it;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0620
  tools:
  - nplinker
  - Python
  - BigScape
  - MIBiG
  - NPLinker
  - Dynaconf
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
evidence_spans:
- NPLinker is a python framework for data mining microbial natural products
- GNPSDownloader, GNPSExtractor
- Python version ≥3.11
- NPLinker can run BigScape automatically if the `bigscape` directory does not exist
- mibig directory contains the MIBiG metadata
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_2_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_2_cq
schema_version: 0.2.0
---

# BigScape Output Version Detection and Compatibility

## Summary

Detect and handle BigScape clustering outputs in both v1 (mix_clustering_c{cutoff}.tsv) and v2 (data_sqlite.db) formats to ensure NPLinker can process heterogeneous BGC clustering results. This skill resolves format compatibility issues that arise when integrating AntiSMASH BGC data via different BigScape pipeline versions.

## When to use

When preparing NPLinker input data and the BigScape directory exists but its format is unknown or mixed (e.g., migrated workflows, third-party data, or legacy archives). Specifically: if local mode and BigScape directory is missing, generate it; if PODP mode and BigScape data is missing or invalid, download or generate it (with retry logic up to 2 times on validation failure).

## When NOT to use

- BigScape has not been run on the AntiSMASH data and automatic execution is disabled in the workflow.
- The user explicitly prefers to skip BGC clustering and only use raw antiSMASH GenBank files.
- Input data contains neither v1 TSV nor v2 SQLite outputs and no mechanism to generate them is available.

## Inputs

- BigScape directory (local path or remote PODP reference)
- AntiSMASH BGC data directory (already validated)
- Dynaconf configuration (mode: local or podp, root_dir, BigScape settings)

## Outputs

- Validated BigScape output directory path
- Detected format identifier (v1 or v2)
- Format-specific metadata (e.g., list of cutoff values for v1, database schema for v2)
- Ready-to-consume BigScape data for DatasetLoader

## How to apply

During DatasetArranger data-preparation stage, after validating the AntiSMASH directory, check the BigScape directory for clustering outputs. First, detect whether v1 files (mix_clustering_c{cutoff}.tsv pattern matching one or more cutoff values) or v2 files (data_sqlite.db SQLite database) are present. If v1 detected, parse TSV format; if v2 detected, query the SQLite database. If neither format is found and mode is local, either download pre-computed BigScape results or trigger BigScape to run on the AntiSMASH data. If mode is PODP and data is missing or validation fails, download and extract from remote source, with automatic retry up to 2 times on validation errors. Store the validated format identifier alongside the directory path so downstream DatasetLoader knows which parser to invoke.

## Related tools

- **BigScape** (Generates BGC clustering outputs (v1 TSV or v2 SQLite) that NPLinker consumes during data preparation; can be run automatically if output directory does not exist)
- **NPLinker** (Orchestrates version detection and compatibility handling via DatasetArranger module; routes detected format to appropriate parser in DatasetLoader) — https://github.com/NPLinker/nplinker
- **Dynaconf** (Configuration management system that specifies BigScape directory location, mode (local/podp), and fallback behavior (download/generate))

## Examples

```
from nplinker.data_preparation import DatasetArranger; arranger = DatasetArranger(config_file='nplinker.toml'); validated_dirs = arranger.arrange(); print(f"BigScape format: {validated_dirs['bigscape_format']}, path: {validated_dirs['bigscape_dir']}")
```

## Evaluation signals

- Detected format identifier matches file system contents (v1: mix_clustering_c*.tsv files present; v2: data_sqlite.db present and readable).
- Validation of v1 TSV structure confirms at least GCF ID and cluster assignment columns; for v2, SQLite database integrity check passes without errors.
- DatasetLoader successfully parses the detected format and populates GCF objects without schema mismatches or missing required fields.
- Retry logic correctly re-attempts download/generation on transient validation failures (up to 2 retries) and logs failure reason on max retries exceeded.
- Metadata extraction (e.g., cutoff values for v1, table schemas for v2) is consistent with documented BigScape v1/v2 output specifications.

## Limitations

- Mixed format directories (containing both v1 and v2 outputs) may cause ambiguity; the skill assumes one format per directory.
- SQLite database corruption in v2 format may not be detected until DatasetLoader attempts to query it; pre-flight integrity checks are recommended.
- Automatic BigScape execution (if missing) can be CPU- and time-intensive; local mode deployments should pre-compute or cache results.
- PODP mode retry logic (max 2 attempts) may be insufficient for transient network failures; user may need manual re-invocation.

## Evidence

- [other] support both BigScape v1 (mix_clustering_c{cutoff}.tsv) and v2 (data_sqlite.db) formats: "support both BigScape v1 (mix_clustering_c{cutoff}.tsv) and v2 (data_sqlite.db) formats"
- [other] if in local mode and directory missing, download or generate it; if in podp mode and missing/invalid, download or generate it (retry up to 2 times): "if in local mode and directory missing, download or generate it; if in podp mode and missing/invalid, download or generate it (retry up to 2 times)"
- [other] NPLinker can run BigScape automatically if the `bigscape` directory does not exist: "NPLinker can run BigScape automatically if the `bigscape` directory does not exist"
- [other] For BigScape data: if in local mode and directory missing, download or generate it; if in podp mode and missing/invalid, download or generate it (retry up to 2 times on validation failure): "For BigScape data: if in local mode and directory missing, download or generate it; if in podp mode and missing/invalid, download or generate it (retry up to 2 times on validation failure)"
