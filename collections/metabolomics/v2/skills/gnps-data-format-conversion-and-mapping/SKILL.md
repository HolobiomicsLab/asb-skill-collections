---
name: gnps-data-format-conversion-and-mapping
description: Use when you have GNPS molecular networking output (from GNPS1 at https://gnps.ucsd.edu
  or GNPS2 at https://gnps2.org) that must be integrated with antiSMASH BGC data and
  MIBiG metadata for natural product mining.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - nplinker
  - Python
  - GNPS
  - MIBiG
  - Dynaconf
  - PODP (Paired Omics Data Platform)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
evidence_spans:
- NPLinker is a python framework for data mining microbial natural products
- GNPSDownloader, GNPSExtractor
- Python version ≥3.11
- NPLinker requires GNPS molecular networking data as input
- NPLinker requires GNPS molecular networking data as input. It currently accepts
  data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows.
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

# gnps-data-format-conversion-and-mapping

## Summary

Convert and map GNPS molecular networking data into NPLinker's standardized input layout, validating directory structure and file formats for downstream genomics–metabolomics integration. This skill bridges GNPS metabolomics output with NPLinker's data preparation pipeline.

## When to use

You have GNPS molecular networking output (from GNPS1 at https://gnps.ucsd.edu or GNPS2 at https://gnps2.org) that must be integrated with antiSMASH BGC data and MIBiG metadata for natural product mining. Triggers include: (1) GNPS data exists but is not yet organized into NPLinker's expected directory structure, (2) configuration mode is 'local' and you must validate directory presence before running DatasetLoader, or (3) configuration mode is 'podp' and GNPS data must be downloaded/extracted from PODP (Paired Omics Data Platform) and validated on retry.

## When NOT to use

- GNPS data has already been downloaded and validated in a prior run and no update is needed.
- Working entirely in podp mode and PODP backend is unreachable or credentials are not configured.
- GNPS directory structure is corrupted or contains incompatible file formats from a different metabolomics platform (e.g., MassBank or Metlin data).

## Inputs

- nplinker.toml configuration file (Dynaconf format with root_dir, mode, and gnps_dir settings)
- GNPS molecular networking output directory (local path or PODP reference)
- PODP project metadata JSON file (podp mode only)

## Outputs

- Validated GNPS data directory in NPLinker's expected layout
- Configuration object with resolved GNPS path ready for DatasetLoader
- Directory structure confirmation for gnps subdirectory under root_dir

## How to apply

Load and validate the Dynaconf configuration file (nplinker.toml) to determine the mode (local or podp) and root directory path. For local mode, check that the GNPS directory exists at the configured path and raise a data validation error if missing. For podp mode, download and extract GNPS data from PODP if the directory is missing or invalid, with automatic retry (up to 2 times) if validation fails. Ensure the extracted GNPS directory contains the expected molecular networking files (typically tab-separated or JSON network outputs from GNPS). The conversion step maps GNPS output into NPLinker's standardized directory layout, which is then consumed by the DatasetLoader stage. Verify successful conversion by confirming the GNPS directory path is present, readable, and contains valid GNPS output artifacts (e.g., molecular networks, cluster metadata).

## Related tools

- **nplinker** (Main framework orchestrating GNPS data format conversion and validation; provides DatasetArranger module for configuration parsing and directory layout setup) — https://github.com/NPLinker/nplinker
- **Dynaconf** (Configuration validation library used to load and parse nplinker.toml schema, including root_dir, mode (local or podp), and GNPS directory settings)
- **GNPS** (Source data platform providing molecular networking output; NPLinker accepts data from GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows) — https://gnps.ucsd.edu
- **PODP (Paired Omics Data Platform)** (Remote data repository for podp mode; provides project metadata JSON and downloadable GNPS archives when local mode is not used)

## Examples

```
from nplinker.data_preparation import DatasetArranger; arranger = DatasetArranger('nplinker.toml'); validated_config = arranger.arrange()
```

## Evaluation signals

- Configuration file (nplinker.toml) is successfully loaded and validated against Dynaconf schema without errors.
- For local mode: GNPS directory exists at the configured path and is readable; for podp mode: GNPS data is downloaded, extracted, and passes integrity validation.
- The GNPS directory contains expected GNPS output files (molecular network metadata, cluster assignments, or equivalent GNPS workflow outputs).
- No configuration errors (missing root_dir, invalid mode setting) or data validation errors (missing GNPS directory in local mode) are raised by DatasetArranger.
- Subsequent DatasetLoader consumption succeeds with the resolved GNPS path, confirming format and structure compatibility.

## Limitations

- Local mode requires manual GNPS data download and placement; if directory is missing, DatasetArranger raises an error and does not auto-download (unlike podp mode).
- PODP mode retries download/extraction up to 2 times on validation failure; persistent network issues or PODP unavailability will cause the workflow to fail.
- The skill validates directory structure and presence but does not perform deep content validation of GNPS file schemas; corrupted or incompatible GNPS outputs may pass validation but cause downstream DatasetLoader failures.
- Both GNPS1 and GNPS2 workflows are supported, but the exact file formats and metadata structure may differ; NPLinker expects a standardized layout and may not handle edge-case GNPS variants.

## Evidence

- [other] NPLinker requires input data preparation including GNPS molecular networking data, antismash directory containing AntiSMASH BGC data, and mibig directory containing MIBiG metadata, with configuration managed via Dynaconf for either local or PODP (Paired Omics Data Platform) mode.: "NPLinker requires input data preparation including GNPS molecular networking data, antismash directory containing AntiSMASH BGC data, and mibig directory containing MIBiG metadata, with configuration"
- [other] For GNPS data: if in local mode and directory does not exist, raise a data validation error; if in podp mode and directory missing or invalid, download and extract GNPS data (retry up to 2 times on validation failure).: "For GNPS data: if in local mode and directory does not exist, raise a data validation error; if in podp mode and directory missing or invalid, download and extract GNPS data (retry up to 2 times on"
- [other] NPLinker requires GNPS molecular networking data as input: "NPLinker requires GNPS molecular networking data as input"
- [other] currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows: "currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows"
