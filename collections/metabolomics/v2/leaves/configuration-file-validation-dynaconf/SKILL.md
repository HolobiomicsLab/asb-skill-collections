---
name: configuration-file-validation-dynaconf
description: Use when when setting up NPLinker for natural products data mining and
  you have a TOML configuration file (nplinker.toml) that specifies root_dir, mode
  (local or podp), and paths to GNPS, AntiSMASH, and MIBiG directories.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0102
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
  tools:
  - nplinker
  - Python
  - Dynaconf
  - MIBiG
  - GNPS
  - AntiSMASH
  - BigScape
  - PODP (Paired Omics Data Platform)
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
evidence_spans:
- NPLinker is a python framework for data mining microbial natural products
- GNPSDownloader, GNPSExtractor
- Python version ≥3.11
- Pass Dynaconf config validation
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# configuration-file-validation-dynaconf

## Summary

Validate and load Dynaconf configuration files for NPLinker data preparation, checking schema compliance and root_dir/mode settings before orchestrating multi-source genomics and metabolomics input staging.

## When to use

When setting up NPLinker for natural products data mining and you have a TOML configuration file (nplinker.toml) that specifies root_dir, mode (local or podp), and paths to GNPS, AntiSMASH, and MIBiG directories. Apply this skill before DatasetLoader consumption to ensure configuration integrity and fail fast on schema or path errors.

## When NOT to use

- If your configuration is already in a format other than TOML or if you have already validated and staged all input data elsewhere.
- If you are running NPLinker in a fully containerized environment where configuration is baked into the image and input paths are immutable.
- If your workflow requires custom configuration validation logic that deviates from the Dynaconf schema or NPLinker's multi-source orchestration requirements.

## Inputs

- nplinker.toml configuration file
- root_dir path specified in config
- GNPS molecular networking data directory (or remote GNPS URL for podp mode)
- AntiSMASH BGC data directory
- MIBiG metadata source
- BigScape clustering results (if pre-computed)
- PODP project metadata JSON (podp mode only)

## Outputs

- Validated Dynaconf configuration object
- Organized gnps directory with molecular networking data
- Organized antismash directory with BGC data
- Organized bigscape directory with clustering results (v1 or v2 format)
- MIBiG metadata directory
- Validated strain_mappings.json
- Optional validated strains_selected.json

## How to apply

Load the Dynaconf configuration file (nplinker.toml) and validate it against the schema, checking that root_dir, mode (local or podp), and required settings for GNPS, BigScape, and MIBiG are present and well-formed. If validation fails, raise a configuration error immediately. For podp mode, download the PODP project metadata JSON if missing. For local mode, verify that input directories exist; for podp mode, download and extract missing data with up to 2 retries on validation failure. Support BigScape v1 (mix_clustering_c{cutoff}.tsv) and v2 (data_sqlite.db) formats. Always auto-download and replace MIBiG data. Validate strain_mappings.json (auto-generate for podp; validate for local) and optionally strains_selected.json. Return a validated arrangement of all input directories and configuration ready for DatasetLoader consumption.

## Related tools

- **Dynaconf** (Configuration file parsing and validation engine; loads and validates nplinker.toml against schema)
- **nplinker** (Data mining framework that consumes validated configuration and staged input directories) — https://github.com/NPLinker/nplinker
- **GNPS** (Source of molecular networking data; validated and staged during configuration setup) — https://gnps.ucsd.edu
- **AntiSMASH** (Source of biosynthetic gene cluster (BGC) data; directory validated and optionally downloaded)
- **BigScape** (Generates or provides BGC clustering results in v1 (TSV) or v2 (SQLite) format; auto-run if missing)
- **MIBiG** (Source of microbial biosynthetic gene cluster metadata; auto-downloaded and replaced during validation)
- **PODP (Paired Omics Data Platform)** (Remote data source for podp mode; metadata JSON downloaded and validated if not present)

## Evaluation signals

- Configuration file loads without Dynaconf schema validation errors.
- root_dir exists and mode is one of {local, podp}.
- For local mode: all required input directories (gnps, antismash, mibig, bigscape if applicable) exist or are created without errors.
- For podp mode: PODP metadata JSON is successfully downloaded and project ID is valid; GNPS, AntiSMASH, and BigScape data are downloaded and extracted within 2 retries on validation failure.
- strain_mappings.json is present and valid JSON (auto-generated for podp; validated for local); strains_selected.json (if present) is valid JSON.
- BigScape data conforms to either v1 (mix_clustering_c{cutoff}.tsv files present) or v2 (data_sqlite.db present) format.
- Return object contains all validated directory paths and configuration ready for DatasetLoader.load_data().

## Limitations

- Dynaconf validation is schema-strict; any missing or misspelled required keys will cause early failure.
- In podp mode, network availability is required for metadata and data download; retries are capped at 2 attempts.
- MIBiG data is always re-downloaded and replaced, which may be time-consuming for large datasets or slow network connections.
- BigScape v1 and v2 format detection is based on file presence; mixed or corrupted formats may not be detected until downstream analysis.
- strain_mappings.json auto-generation for podp mode may fail if PODP project structure is non-standard or metadata is incomplete.

## Evidence

- [other] Load and validate the Dynaconf configuration file (nplinker.toml) against the schema, checking root_dir, mode (local or podp), and required settings for GNPS, BigScape, and MIBiG.: "Load and validate the Dynaconf configuration file (nplinker.toml) against the schema, checking root_dir, mode (local or podp), and required settings for GNPS, BigScape, and MIBiG."
- [other] For podp mode, download the PODP project metadata JSON file if not present and validate it.: "For podp mode, download the PODP project metadata JSON file if not present and validate it."
- [other] Check Dynaconf config validation; if it fails, raise a configuration error.: "Check Dynaconf config validation; if it fails, raise a configuration error."
- [other] For GNPS data: if in local mode and directory does not exist, raise a data validation error; if in podp mode and directory missing or invalid, download and extract GNPS data (retry up to 2 times on validation failure).: "For GNPS data: if in local mode and directory does not exist, raise a data validation error; if in podp mode and directory missing or invalid, download and extract GNPS data (retry up to 2 times on"
- [other] For BigScape data: if in local mode and directory missing, download or generate it; if in podp mode and missing/invalid, download or generate it (retry up to 2 times); support both BigScape v1 (mix_clustering_c{cutoff}.tsv) and v2 (data_sqlite.db) formats.: "For BigScape data: if in local mode and directory missing, download or generate it; if in podp mode and missing/invalid, download or generate it (retry up to 2 times); support both BigScape v1"
- [other] For MIBiG data: always download automatically, removing and replacing any existing data if needed.: "For MIBiG data: always download automatically, removing and replacing any existing data if needed."
- [other] Validate strain_mappings.json (auto-generate for podp mode; validate for local mode); optionally validate strains_selected.json if present.: "Validate strain_mappings.json (auto-generate for podp mode; validate for local mode); optionally validate strains_selected.json if present."
