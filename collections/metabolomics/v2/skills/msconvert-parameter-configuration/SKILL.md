---
name: msconvert-parameter-configuration
description: Use when you have acquired raw mass spectrometry data from ThermoFisher, Agilent, or compatible vendors in their native formats (.raw, .d, or equivalent) and need to prepare it for nontargeted analysis using MSThunder on a Linux system.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MSThunder
  - MSConvert
  - Ubuntu
  - Ubuntu 20.04
derived_from:
- doi: 10.1016/j.enceco.2025.07.022
  title: MSThunder
evidence_spans:
- MSThunder provide a deep learning-based nontargeted analytical framework for the accurate and rapid identification of unknown organic pollutants in water
- other vendors whose raw data can be converted via MSConvert
- The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert.
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
---

# msconvert-parameter-configuration

## Summary

Configure and execute MSConvert command-line conversion of vendor-specific raw mass spectrometry data (ThermoFisher .raw, Agilent .d) into MSThunder-compatible formats on a Linux system. This skill bridges proprietary vendor formats and open analytical frameworks by applying appropriate output format parameters and validating file integrity post-conversion.

## When to use

You have acquired raw mass spectrometry data from ThermoFisher, Agilent, or compatible vendors in their native formats (.raw, .d, or equivalent) and need to prepare it for nontargeted analysis using MSThunder on a Linux system. The input files must be converted to an MSThunder-compatible format before downstream deep learning-based pollutant identification can proceed.

## When NOT to use

- Input is already in an open, MSThunder-compatible format (e.g., mzML, mzXML) — skip directly to MSThunder analysis.
- Raw data is from a vendor not supported by MSConvert — this skill cannot bridge incompatible proprietary formats.
- Offline raw data processing is required but the MSThunder version in use does not support offline mode — data must be sent to authors or uploaded to online repository instead.

## Inputs

- ThermoFisher raw mass spectrometry data file (.raw format)
- Agilent raw mass spectrometry data directory (.d format)
- Other vendor-compatible raw mass spectrometry data formats
- MSConvert executable and configuration (Linux/Ubuntu 20.04)

## Outputs

- MSThunder-compatible converted mass spectrometry data file (open format, e.g. mzML)
- Conversion validation report (file integrity, format compliance, metadata presence)

## How to apply

Install MSConvert on an Ubuntu 20.04 (or compatible) Linux system alongside vendor-specific SDK libraries. Obtain the vendor raw data file(s) and invoke MSConvert via command line with output format parameters targeting MSThunder compatibility (typically mzML or equivalent open format). After conversion completes, validate the converted file's integrity by checking file size, format compliance against schema, and presence of expected spectral metadata (MS1, MS2, retention time, precursor m/z). Return the validated converted file for subsequent MSThunder analysis. The rationale is that MSThunder requires standardized, vendor-agnostic input; MSConvert acts as the format translator, and validation prevents downstream failures due to corrupted or incomplete conversions.

## Related tools

- **MSConvert** (Command-line mass spectrometry data format converter; translates vendor-specific raw formats into open, standardized formats compatible with MSThunder)
- **MSThunder** (Downstream deep learning framework that consumes the converted data files for nontargeted identification of unknown organic pollutants) — https://github.com/LQZ0123/MSThunder
- **Ubuntu 20.04** (Tested Linux operating system environment for MSConvert installation and raw data processing)

## Evaluation signals

- Converted file exists and is non-empty; file size is proportional to input raw data size (not truncated).
- Converted file passes format schema validation (well-formed mzML, mzXML, or equivalent; valid XML/binary structure).
- Metadata integrity: converted file contains expected elements (MS1 spectra, MS2 spectra, retention times, precursor m/z values, scan identifiers) with no missing or null critical fields.
- File can be opened and parsed by MSThunder without errors during the Input button workflow step.
- Comparison of spectral peak counts, RT range, and m/z range between original vendor metadata and converted file shows consistency (no data loss).

## Limitations

- Current MSThunder version does not support offline processing of raw data due to environment configuration issues; users must send raw files to authors or upload to online repositories (Zenodo, GNPS) and use online analysis.
- MSConvert compatibility is vendor-specific; only ThermoFisher, Agilent, and select other vendors are explicitly supported—proprietary formats from unsupported vendors cannot be converted.
- Online processing capability for UPLC-HRMS raw data is under development and not yet available; converted files may require manual submission and processing delays.
- No changelog is available; version compatibility and known issues with specific MSConvert or vendor SDK versions are not documented.

## Evidence

- [readme] The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert: "The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert"
- [readme] Raw data processing and conversion workflow with return of converted file: "our process the raw data in a Linux system and return the converted file. Then, you can subsequently analyze the data using MSThunder after"
- [readme] Ubuntu 20.04 as the tested environment: "The training data, code, model parameters and candidates used for training and prediction are available through our experiments conducted on an Ubuntu 20.04 environment"
- [readme] Offline processing limitation: "Due to environment configuration issues, the current version does not yet support offline processing of raw data"
- [readme] Online development status: "We are developing the relevant functionality and will make it available online as soon as possible"
