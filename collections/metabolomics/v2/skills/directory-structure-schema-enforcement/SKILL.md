---
name: directory-structure-schema-enforcement
description: Use when you have raw or partially organized natural products data from multiple sources (GNPS molecular networking, AntiSMASH BGC predictions, BigScape clustering, MIBiG metadata) and need to prepare them for NPLinker integration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3960
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0080
  tools:
  - nplinker
  - Python
  - MIBiG
  - Dynaconf
  - GNPS
  - AntiSMASH
  - BigScape
  - NPLinker
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
evidence_spans:
- NPLinker is a python framework for data mining microbial natural products
- GNPSDownloader, GNPSExtractor
- Python version ≥3.11
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# directory-structure-schema-enforcement

## Summary

Validate and organize multi-source genomics and metabolomics input directories against a declarative configuration schema, ensuring NPLinker receives correctly structured GNPS, AntiSMASH, BigScape, and MIBiG data. This skill automates the DatasetArranger stage, which enforces Dynaconf schema compliance and manages both local and cloud (PODP) data sources with automatic download and retry logic.

## When to use

Apply this skill when you have raw or partially organized natural products data from multiple sources (GNPS molecular networking, AntiSMASH BGC predictions, BigScape clustering, MIBiG metadata) and need to prepare them for NPLinker integration. Trigger conditions: you have a Dynaconf configuration file (nplinker.toml) specifying root_dir, mode (local or podp), and data source paths; you need to validate that all required directories exist and conform to expected layouts; and you want to automatically download missing data or regenerate derived outputs (e.g., BigScape results) rather than fail.

## When NOT to use

- Your input data is already structured and loaded into memory as NPLinker DatasetLoader objects; use this skill only for directory preparation, not in-memory validation.
- You are working with a custom data integration pipeline that does not use Dynaconf configuration or does not require schema validation against nplinker.toml; this skill is specific to NPLinker's declarative config model.
- Your GNPS, AntiSMASH, or MIBiG data is already in a post-processed or filtered state outside the expected directory structure; this skill enforces a rigid directory layout and will overwrite existing MIBiG copies.

## Inputs

- nplinker.toml configuration file (Dynaconf format)
- root_dir path (local filesystem or PODP project identifier)
- mode setting ('local' or 'podp')
- GNPS directory or PODP GNPS data source
- antismash directory (BGC predictions)
- mibig directory or MIBiG metadata source
- BigScape directory or clustering data source
- strain_mappings.json (if present)
- strains_selected.json (optional)

## Outputs

- validated arrangement of input directories with confirmed paths
- Dynaconf configuration object (validated against schema)
- GNPS molecular networking data (organized in gnps/ subdirectory)
- AntiSMASH BGC directory (organized in antismash/ subdirectory)
- BigScape clustering results (v1 or v2 format in bigscape/ subdirectory)
- MIBiG metadata (in mibig/ subdirectory)
- strain_mappings.json (validated or auto-generated)
- configuration ready for DatasetLoader consumption

## How to apply

Load and validate the nplinker.toml configuration file against the Dynaconf schema, checking root_dir, mode setting, and required keys for GNPS, BigScape, and MIBiG. For each data source (GNPS, AntiSMASH, BigScape, MIBiG), apply mode-specific logic: in local mode, raise a validation error if required directories are missing; in podp mode, automatically download and extract missing data, retrying up to 2 times on validation failure. For GNPS and AntiSMASH, accept either missing-but-required (local mode fails, podp mode downloads) or present-but-invalid (podp mode overwrites). For BigScape, support both v1 (mix_clustering_c{cutoff}.tsv) and v2 (data_sqlite.db) formats, downloading or regenerating if missing. Always download MIBiG metadata automatically, replacing any existing copy. Validate strain_mappings.json (auto-generate for podp mode; validate for local mode) and optionally validate strains_selected.json. Return a validated arrangement of all input directories and configuration ready for DatasetLoader consumption.

## Related tools

- **Dynaconf** (configuration file loader and schema validator for nplinker.toml; validates root_dir, mode, and required settings for GNPS, BigScape, and MIBiG)
- **GNPS** (molecular networking data source; provides mass spectrometry networking results that must be downloaded, extracted, and validated for NPLinker input) — https://gnps.ucsd.edu
- **AntiSMASH** (biosynthetic gene cluster (BGC) prediction source; antismash directory contains BGC data that must be validated and organized into expected layout)
- **BigScape** (BGC clustering tool; generates v1 (mix_clustering_c{cutoff}.tsv) or v2 (data_sqlite.db) output that NPLinker auto-runs or accepts pre-computed)
- **MIBiG** (biosynthetic gene cluster metadata database; mibig directory contains reference metadata, automatically downloaded and replaced on each run)
- **NPLinker** (target framework; DatasetArranger is the data-preparation stage that validates directory structure and configuration before DatasetLoader consumption) — https://github.com/NPLinker/nplinker

## Evaluation signals

- Dynaconf configuration file parses without error and all required keys (root_dir, mode, GNPS path, BigScape path, MIBiG path) are present and valid.
- All required input directories (gnps/, antismash/, bigscape/, mibig/) exist and contain the expected file types (e.g., GNPS networking results, AntiSMASH .gbk files, BigScape .tsv or .db, MIBiG JSON metadata).
- strain_mappings.json is present and valid JSON; strains_selected.json (if present) is valid JSON and does not conflict with strain_mappings.
- For podp mode: PODP project metadata JSON is downloaded, parsed, and validated; missing data sources are downloaded and extracted with no validation failures after retries.
- For local mode: all required directories are confirmed present; if any are missing, a clear configuration error is raised naming the missing path.
- BigScape data conforms to v1 (named .tsv files with cutoff patterns) or v2 (single data_sqlite.db) format; either is accepted, but format is consistently reported in the returned arrangement.
- MIBiG metadata is present and contains expected JSON structure; any pre-existing mibig/ directory is replaced with freshly downloaded data.

## Limitations

- Local mode requires all data directories to pre-exist; if a directory is missing, the skill fails rather than attempting download—use podp mode for automatic data retrieval.
- BigScape v1 and v2 formats are both supported, but the skill must detect which version is present; if both or neither format is detected, behavior is undefined.
- MIBiG metadata is always re-downloaded, replacing any existing data; users cannot preserve custom or locally modified MIBiG copies.
- Retry logic (up to 2 attempts) applies only to podp mode data downloads; network failures in podp mode may exhaust retries and leave data incomplete.
- Dynaconf schema validation is strict; any deviation from the expected nplinker.toml structure will raise a configuration error with limited guidance on which field failed.
- strain_mappings.json auto-generation is only performed for podp mode; local mode assumes a pre-existing, valid strain_mappings.json and will fail if it is missing or invalid.

## Evidence

- [other] NPLinker requires input data preparation including GNPS molecular networking data, antismash directory containing AntiSMASH BGC data, and mibig directory containing MIBiG metadata, with configuration managed via Dynaconf for either local or PODP (Paired Omics Data Platform) mode.: "NPLinker requires input data preparation including GNPS molecular networking data, antismash directory containing AntiSMASH BGC data, and mibig directory containing MIBiG metadata, with configuration"
- [other] Load and validate the Dynaconf configuration file (nplinker.toml) against the schema, checking root_dir, mode (local or podp), and required settings for GNPS, BigScape, and MIBiG.: "Load and validate the Dynaconf configuration file (nplinker.toml) against the schema, checking root_dir, mode (local or podp), and required settings for GNPS, BigScape, and MIBiG"
- [other] For GNPS data: if in local mode and directory does not exist, raise a data validation error; if in podp mode and directory missing or invalid, download and extract GNPS data (retry up to 2 times on validation failure).: "if in local mode and directory does not exist, raise a data validation error; if in podp mode and directory missing or invalid, download and extract GNPS data (retry up to 2 times on validation"
- [other] For BigScape data: if in local mode and directory missing, download or generate it; if in podp mode and missing/invalid, download or generate it (retry up to 2 times); support both BigScape v1 (mix_clustering_c{cutoff}.tsv) and v2 (data_sqlite.db) formats.: "support both BigScape v1 (mix_clustering_c{cutoff}.tsv) and v2 (data_sqlite.db) formats"
- [other] For MIBiG data: always download automatically, removing and replacing any existing data if needed.: "For MIBiG data: always download automatically, removing and replacing any existing data if needed"
- [other] Validate strain_mappings.json (auto-generate for podp mode; validate for local mode); optionally validate strains_selected.json if present.: "Validate strain_mappings.json (auto-generate for podp mode; validate for local mode); optionally validate strains_selected.json if present"
