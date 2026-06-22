---
name: raw-ms-data-format-conversion
description: Use when you have raw UPLC-HRMS data from ThermoFisher or Agilent instruments and need to feed it into MSThunder for nontargeted pollutant identification. Your input is a vendor binary format (.raw or .d) that MSThunder cannot directly ingest. Environment constraints (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MSThunder
  - Ubuntu
  - MSConvert
  - Ubuntu 20.04
  techniques:
  - LC-MS
derived_from:
- doi: 10.1016/j.enceco.2025.07.022
  title: MSThunder
evidence_spans:
- MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water
- available through our experiments conducted on an Ubuntu 20.04 environment
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msthunder_cq
    doi: 10.1016/j.enceco.2025.07.022
    title: MSThunder
  dedup_kept_from: coll_msthunder_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.enceco.2025.07.022
  all_source_dois:
  - 10.1016/j.enceco.2025.07.022
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# raw-ms-data-format-conversion

## Summary

Convert vendor-specific raw mass spectrometry data (ThermoFisher .raw, Agilent .d) to MSThunder-compatible formats using MSConvert on a Linux system. This skill bridges incompatible instrument formats and downstream deep-learning analysis pipelines for unknown pollutant identification.

## When to use

You have raw UPLC-HRMS data from ThermoFisher or Agilent instruments and need to feed it into MSThunder for nontargeted pollutant identification. Your input is a vendor binary format (.raw or .d) that MSThunder cannot directly ingest. Environment constraints (e.g., no offline processing support in current MSThunder version) require preprocessing on a dedicated Linux system before analysis.

## When NOT to use

- Input data is already in open format (mzML, mzXML, netCDF) compatible with MSThunder—conversion is redundant.
- Raw data originates from instruments not supported by MSConvert (e.g., certain older or proprietary systems without vendor drivers).
- Analysis environment is Windows-only and offline processing is required—current MSThunder version does not support offline raw-data processing on Windows; use online submission to [redacted-email] or Zenodo/GNPS database instead.

## Inputs

- ThermoFisher .raw file
- Agilent .d directory
- Other vendor-proprietary mass spectrometry raw data formats
- Linux system with MSConvert and vendor libraries installed

## Outputs

- MSThunder-compatible mass spectrometry data file (mzML or mzXML)
- Converted file integrity report

## How to apply

Install MSConvert on Ubuntu 20.04 or compatible Linux system alongside vendor-specific libraries. Obtain the raw vendor file (.raw, .d, or equivalent format) and invoke MSConvert command-line with output format targeting MSThunder compatibility—typically mzML or mzXML. Validate converted file integrity by checking schema compliance and file size consistency with input. Return the converted file to the analysis environment where MSThunder will load and process it. The conversion step is prerequisite; do not skip validation, as format corruption downstream will fail spectral matching and structure prediction.

## Related tools

- **MSConvert** (Command-line utility that performs vendor-to-open-format conversion of raw mass spectrometry data on Linux; outputs MSThunder-compatible formats)
- **MSThunder** (Deep-learning nontargeted analytical framework that accepts converted mass spectrometry data for unknown organic pollutant identification in water) — https://github.com/LQZ0123/MSThunder
- **Ubuntu 20.04** (Operating system on which MSConvert and Linux-side raw data processing must be executed to ensure compatibility and vendor library availability)

## Evaluation signals

- Converted file is readable by MSThunder without format errors or schema validation failures.
- File size of converted output is consistent with expected compression ratio (typically 30–50% of original .raw size for mzML).
- Precursor ion m/z values, retention times, and MS2 fragmentation patterns in converted file match metadata recorded in original vendor file (spot-check via MSConvert validation tools).
- MSThunder successfully loads converted file, displays TIC and MS1 spectra, and executes precursor/RT queries without crashes or missing data.
- No data loss detected: total ion count (TIC) area and spectral count before and after conversion remain proportional (>90% recovery expected).

## Limitations

- Current MSThunder version does not support offline processing of raw data; conversion must be performed on a dedicated Linux system and file returned for remote or subsequent analysis.
- Vendor-specific libraries and MSConvert installation on Linux requires system administration privileges and correct driver configuration; mismatched library versions can silently corrupt converted output.
- Online processing capability for UPLC-HRMS data is under development; users with unsupported instrument formats or conversion failures must submit raw files to [redacted-email] or upload to Zenodo/GNPS for manual processing.
- Windows environment supports only pre-converted case files (e.g., 'Pesticides' example); native Windows conversion is not available.

## Evidence

- [readme] The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert: "The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert"
- [readme] Raw data processing workflow: Linux system conversion then return for MSThunder analysis: "our process the raw data in a Linux system and return the converted file. Then, you can subsequently analyze the data using MSThunder after"
- [readme] Offline processing limitation and online submission alternative: "Due to environment configuration issues, the current version does not yet support offline processing of raw data. If you want to analyze other data on UPLC-HRMS, you can send the raw file to our"
- [readme] Ubuntu 20.04 environment for experiments and conversion: "available through our experiments conducted on an Ubuntu 20.04 environment"
- [intro] Five-step workflow from installation to validation to downstream analysis: "1. Install and configure MSConvert on a Linux system (Ubuntu 20.04 or compatible). 2. Obtain vendor-specific raw data file(s) (ThermoFisher .raw, Agilent .d, or equivalent format). 3. Execute"
