---
name: podp-metadata-retrieval-and-integration
description: Use when when running NPLinker in PODP mode (as opposed to local mode), you need to fetch and validate project metadata from PODP, orchestrate downloads of GNPS molecular networking data, AntiSMASH BGC predictions, BigScape clustering results, and MIBiG reference metadata, then organize them into.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - nplinker
  - Python
  - MIBiG
  - Dynaconf
  - PODP
  - GNPS
  - AntiSMASH
  - BigScape
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

# podp-metadata-retrieval-and-integration

## Summary

Retrieve and validate project metadata from the Paired Omics Data Platform (PODP), then integrate it with locally cached or downloaded GNPS, AntiSMASH, BigScape, and MIBiG datasets to construct a validated input arrangement for NPLinker analysis. This skill handles configuration validation, conditional data download/extraction with retry logic, and strain mapping consolidation.

## When to use

When running NPLinker in PODP mode (as opposed to local mode), you need to fetch and validate project metadata from PODP, orchestrate downloads of GNPS molecular networking data, AntiSMASH BGC predictions, BigScape clustering results, and MIBiG reference metadata, then organize them into the directory structure and format required by NPLinker's DatasetLoader. Use this skill when the nplinker.toml configuration specifies `mode = podp` and you have a valid PODP project identifier.

## When NOT to use

- Input configuration specifies mode='local' rather than mode='podp' — use local file validation and error-raising instead.
- PODP project metadata is already fully cached and validated, and all input directories are present and valid — skip metadata retrieval and go directly to DatasetLoader.
- You only need to validate a local GNPS dataset without downloading or integrating PODP-hosted data — use simpler local-mode validation.

## Inputs

- nplinker.toml configuration file with mode='podp' and valid root_dir
- PODP project identifier (from config or environment)
- Optional existing cached PODP metadata JSON, GNPS archive, AntiSMASH directory, BigScape results, MIBiG directory

## Outputs

- Validated gnps/ directory with molecular networking data
- Validated antismash/ directory with BGC predictions
- Validated bigscape/ directory with clustering results (v1 or v2 format)
- Validated mibig/ directory with reference metadata
- Validated strain_mappings.json file
- Validated configuration object and directory arrangement ready for DatasetLoader

## How to apply

Load and validate the Dynaconf configuration file (nplinker.toml) against the schema, confirming root_dir, mode='podp', and required settings are present. Download the PODP project metadata JSON file if not already cached. For GNPS data: if missing or invalid, download and extract with up to 2 retries on validation failure. For AntiSMASH data: download and extract if missing/invalid, retrying up to 2 times. For BigScape data: download or generate if missing/invalid, supporting both v1 (mix_clustering_c{cutoff}.tsv) and v2 (data_sqlite.db) formats, retrying up to 2 times. Always download and replace MIBiG data automatically. Validate or auto-generate strain_mappings.json; optionally validate strains_selected.json if present. Return a fully validated arrangement of all input directories and configuration ready for DatasetLoader consumption.

## Related tools

- **nplinker** (Main framework for integrating genomics and metabolomics data; orchestrates DatasetArranger and DatasetLoader to consume validated PODP metadata and input directories.) — https://github.com/NPLinker/nplinker
- **Dynaconf** (Configuration management library used to load, validate, and manage the nplinker.toml schema for PODP and local mode settings.)
- **PODP** (Paired Omics Data Platform — remote data source from which project metadata and associated GNPS, AntiSMASH, and MIBiG datasets are downloaded and integrated.)
- **GNPS** (Global Natural Products Social molecular networking platform; provides molecular networking data that must be downloaded and extracted for PODP-mode integration.) — https://gnps.ucsd.edu
- **AntiSMASH** (Biosynthetic Gene Cluster prediction tool; PODP provides AntiSMASH predictions that must be validated and integrated into antismash/ directory.)
- **BigScape** (BGC similarity clustering tool; PODP provides BigScape results (v1 or v2 format) that must be downloaded or generated if missing.)
- **MIBiG** (Minimum Information about a Biosynthetic Gene cluster database; metadata is always auto-downloaded and refreshed to ensure current reference data.)

## Examples

```
from nplinker import DatasetArranger; arranger = DatasetArranger(config_path='nplinker.toml'); validated_arrangement = arranger.validate_and_prepare_podp_inputs(podp_project_id='POP_001234'); dataset = validated_arrangement.load_for_nplinker()
```

## Evaluation signals

- Dynaconf configuration validation succeeds without raising ConfigError; mode='podp', root_dir exists, and required settings are present.
- PODP project metadata JSON file is downloaded (if not cached) and parses without JSON decode errors.
- gnps/ directory exists, contains expected molecular networking files, and passes format validation (e.g., file checksums or metadata schema).
- antismash/ directory exists and contains valid AntiSMASH GBK or JSON output files; no validation errors raised after up to 2 download/extract retries.
- bigscape/ directory exists and contains either v1 (mix_clustering_c*.tsv) or v2 (data_sqlite.db) format files; no validation errors after retries.
- mibig/ directory exists with current MIBiG metadata; strain_mappings.json is either auto-generated (PODP mode) or validated (local mode) without schema errors.
- Return value is a validated arrangement object (dict/struct) with keys for gnps, antismash, bigscape, mibig, config, and metadata; ready to pass to DatasetLoader without further validation.

## Limitations

- Retry logic limited to 2 attempts per failed download/extraction; if retries exhaust, skill raises a data validation error and does not proceed.
- MIBiG data is always auto-downloaded and replaced, even if valid cached data exists; no option to skip refresh or use stale data.
- BigScape v1 and v2 formats are both supported, but if a mixed or unrecognized BigScape directory structure is present, validation may fail; user must manually remove or regenerate.
- PODP project metadata download requires network connectivity and valid PODP API access; offline or network-degraded environments will raise download errors.
- strain_mappings.json auto-generation in PODP mode may produce incomplete or incorrect mappings if PODP metadata is malformed or missing strain identifiers.

## Evidence

- [other] nplinker.toml: "Load and validate the Dynaconf configuration file (nplinker.toml) against the schema, checking root_dir, mode (local or podp), and required settings for GNPS, BigScape, and MIBiG."
- [other] PODP project metadata download: "For podp mode, download the PODP project metadata JSON file if not present and validate it."
- [other] GNPS retry logic: "if in podp mode and directory missing or invalid, download and extract GNPS data (retry up to 2 times on validation failure)"
- [other] AntiSMASH retry logic: "if in podp mode and invalid, download and extract (retry up to 2 times)"
- [other] BigScape v1 and v2 formats: "support both BigScape v1 (mix_clustering_c{cutoff}.tsv) and v2 (data_sqlite.db) formats"
- [other] MIBiG auto-download: "For MIBiG data: always download automatically, removing and replacing any existing data if needed."
- [other] strain_mappings validation: "Validate strain_mappings.json (auto-generate for podp mode; validate for local mode); optionally validate strains_selected.json if present."
- [other] DatasetLoader input preparation: "Return a validated arrangement of all input directories and configuration ready for DatasetLoader consumption."
- [other] NPLinker PODP capability: "NPLinker requires input data preparation including GNPS molecular networking data, antismash directory containing AntiSMASH BGC data, and mibig directory containing MIBiG metadata, with configuration"
