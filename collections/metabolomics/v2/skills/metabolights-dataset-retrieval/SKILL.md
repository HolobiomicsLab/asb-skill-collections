---
name: metabolights-dataset-retrieval
description: Use when you have a MetaboLights dataset identifier (e.g., MTBLS1124) and need to download a specific mzML file (e.g., QC07.mzML) from the public repository for visualization, quality control assessment, or integration into a metabolomics workflow. The USI format mzspec:MTBLS1124:QC07.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - GNPS LCMS Visualization Dashboard
  - MetaboLights REST API
  - pymzML
derived_from:
- doi: 10.1038/s41592-021-01339-5
  title: GNPS Dashboard
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnps_dashboard_cq
    doi: 10.1038/s41592-021-01339-5
    title: GNPS Dashboard
  dedup_kept_from: coll_gnps_dashboard_cq
schema_version: 0.2.0
---

# metabolights-dataset-retrieval

## Summary

Retrieve and validate mzML mass spectrometry files from the MetaboLights public repository using Uniform Spectrum Identifiers (USI) and the GNPS LCMS Visualization Dashboard. This skill enables programmatic access to deposited metabolomics datasets for downstream spectrum visualization and analysis.

## When to use

You have a MetaboLights dataset identifier (e.g., MTBLS1124) and need to download a specific mzML file (e.g., QC07.mzML) from the public repository for visualization, quality control assessment, or integration into a metabolomics workflow. The USI format mzspec:MTBLS1124:QC07.mzML is supported by the GNPS LCMS Visualization Dashboard and the MetaboLights REST API.

## When NOT to use

- The input is a proprietary mass spectrometry vendor file format (e.g., .raw, .d) that has not been converted to mzML; use vendor-specific converters first.
- You require data from a private or restricted-access MetaboLights dataset; this skill applies only to public datasets.
- The file identifier or accession number is malformed or does not exist in the MetaboLights repository.

## Inputs

- Uniform Spectrum Identifier (USI) string in format mzspec:MTBLS<accession>:<file_identifier>.mzML
- MetaboLights accession identifier (e.g., MTBLS1124)
- MetaboLights file name or path (e.g., QC07.mzML)

## Outputs

- Downloaded mzML file in local storage
- Validated mzML spectrum container object (e.g., pymzML object)
- Accessible spectrum list with indexed offsets and metadata
- Confirmation of XML schema compliance and file integrity

## How to apply

Parse the USI string to extract the MetaboLights accession number (e.g., MTBLS1124) and file identifier (e.g., QC07.mzML). Query the MetaboLights REST API or download service to retrieve the file manifest and locate the target mzML file. Download the mzML file from the MetaboLights repository to local storage. Validate the downloaded file using an mzML validator (e.g., pymzML parser or mzML indexer) to confirm XML schema compliance, presence of spectrum list, and indexed offset integrity. Load the validated mzML file into an mzML spectrum container (e.g., pymzML object) to enable downstream spectrum access and metadata retrieval for visualization or further analysis.

## Related tools

- **GNPS LCMS Visualization Dashboard** (Web interface for resolving USIs and visualizing mzML spectra from MetaboLights datasets) — https://github.com/Wang-Bioinformatics-Lab/GNPS_LCMSDashboard
- **MetaboLights REST API** (Programmatic query and download service for MetaboLights dataset manifests and files)
- **pymzML** (Python parser for validating mzML XML structure, indexing spectrum offsets, and loading spectrum containers)

## Evaluation signals

- Downloaded mzML file exists in local storage and is not truncated or corrupted.
- mzML XML structure is valid and conforms to the mzML schema (verified by mzML validator or pymzML parser without parse errors).
- Spectrum list element is present and contains ≥1 spectrum entries with valid indexed offsets.
- Spectrum container object successfully loads in pymzML or equivalent with accessible scan metadata (scan number, retention time, m/z array, intensity array).
- File size and checksum (if provided by MetaboLights) match expected values for the QC07.mzML file.

## Limitations

- This skill requires internet connectivity to query the MetaboLights REST API or download service.
- MetaboLights does not guarantee availability or stability of all deposited datasets; files may be temporarily unavailable or removed.
- The skill applies only to public MetaboLights datasets; restricted or embargoed datasets are not accessible.
- Large mzML files (>1 GB) may exceed memory or disk constraints during validation and loading on resource-limited systems.
- Network timeouts or partial downloads may require retry logic or resumable download support not detailed in the workflow.

## Evidence

- [other] The GNPS LCMS Visualization Dashboard documentation lists mzspec:MTBLS1124:QC07.mzML as an example MetaboLights public dataset source, indicating this USI format is supported for dataset retrieval and visualization.: "Metabolights public datasets - [mzspec:MTBLS1124:QC07.mzML]"
- [other] Parse the USI string mzspec:MTBLS1124:QC07.mzML to extract the MetaboLights accession (MTBLS1124) and file identifier (QC07.mzML).: "Parse the USI string mzspec:MTBLS1124:QC07.mzML to extract the MetaboLights accession (MTBLS1124) and file identifier (QC07.mzML)"
- [other] Query the MetaboLights REST API or download service using accession MTBLS1124 to retrieve the file manifest and locate QC07.mzML.: "Query the MetaboLights REST API or download service using accession MTBLS1124 to retrieve the file manifest and locate QC07.mzML"
- [other] Validate the downloaded file against mzML schema using an mzML validator (e.g., mzML indexer or pymzML parser) to confirm XML structure, presence of spectrum list, and indexed offset integrity.: "Validate the downloaded file against mzML schema using an mzML validator (e.g., mzML indexer or pymzML parser) to confirm XML structure, presence of spectrum list, and indexed offset integrity"
- [other] Load the validated mzML file into an mzML spectrum container (e.g., pymzML object or equivalent data structure) to enable downstream spectrum access and metadata retrieval.: "Load the validated mzML file into an mzML spectrum container (e.g., pymzML object or equivalent data structure) to enable downstream spectrum access and metadata retrieval"
