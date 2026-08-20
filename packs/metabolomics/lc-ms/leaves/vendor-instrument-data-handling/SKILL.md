---
name: vendor-instrument-data-handling
description: Use when you have acquired raw mass spectrometry data in vendor-proprietary formats (ThermoFisher, Agilent, or equivalent) and need to analyze it using MSThunder for unknown organic pollutant identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# vendor-instrument-data-handling

## Summary

Convert raw mass spectrometry data from multiple vendor formats (ThermoFisher .raw, Agilent .d, etc.) into a standardized, analysis-ready format via MSConvert on a Linux system, enabling downstream deep learning-based nontargeted pollutant identification in MSThunder. This skill bridges proprietary instrument output to open analytical frameworks.

## When to use

You have acquired raw mass spectrometry data in vendor-proprietary formats (ThermoFisher, Agilent, or equivalent) and need to analyze it using MSThunder for unknown organic pollutant identification. Apply this skill when the raw data is NOT yet in MSThunder-compatible format and you require standardized, validated input for subsequent deep learning-based MS2 matching and structure prediction.

## When NOT to use

- Input is already in MSThunder-compatible format or has been previously converted and validated — skip directly to MSThunder analysis.
- Raw data is from an instrument or vendor not supported by MSConvert (e.g., custom or legacy instruments without vendor drivers).
- You require offline processing of raw data — the current MSThunder version does not yet support offline raw data handling; files must be sent to the curator or uploaded to GNPS/Zenodo for remote conversion.

## Inputs

- Raw vendor instrument data file (ThermoFisher .raw, Agilent .d, or equivalent)
- MSConvert installation and configuration on Ubuntu 20.04

## Outputs

- MSThunder-compatible converted data file (mzML or mzXML format)
- Conversion log and validation report

## How to apply

Install MSConvert on a Linux system (Ubuntu 20.04 or compatible) and obtain the vendor-specific raw data file. Execute MSConvert via command-line targeting MSThunder-compatible output format (typically mzML or mzXML). Validate the converted file for integrity and schema compliance, then return the converted file to the analyst for loading into MSThunder's interface. The conversion step is performed upstream of MSThunder analysis on a separate Linux environment; the converted file is then transferred back for GUI-based precursor/MS2 search, candidate ranking, and structure prediction.

## Related tools

- **MSConvert** (Command-line tool for converting vendor raw mass spectrometry data into standardized MSThunder-compatible formats)
- **MSThunder** (Deep learning-based nontargeted analytical framework that accepts converted MS data for unknown organic pollutant identification) — https://github.com/LQZ0123/MSThunder
- **Ubuntu 20.04** (Linux operating system environment required for MSConvert installation and raw data conversion workflow)

## Examples

```
msconvert input_file.raw --mzML --outdir /path/to/output
```

## Evaluation signals

- Converted file is readable by MSThunder's input loader without schema errors or format validation failures.
- MSThunder successfully populates MS1 spectra, MS2 fragmentation patterns, and retention time data from the converted file when queried via the GUI.
- File integrity check confirms no data corruption during conversion (e.g., spectrum count, m/z range, and RT range match expected values from raw data metadata).
- Candidate structure prediction returns plausible matches with stable ranking scores when a known reference compound is queried from the converted data.
- Conversion log contains no warnings or errors related to vendor-specific header parsing or format compatibility.

## Limitations

- The current MSThunder version does not support offline processing of raw data; users must send files to the maintainer ([redacted-email]) or upload to Zenodo/GNPS for remote conversion.
- MSConvert support depends on availability of vendor-specific drivers; unsupported or legacy instrument formats may fail conversion.
- Conversion workflow requires a separate Linux environment; Windows users cannot run MSConvert locally and must rely on curator-provided conversion service.
- Converted file size and complexity may impact downstream MSThunder processing performance; very large batch files may require segmentation.

## Evidence

- [other] Raw data from ThermoFisher, Agilent, and other vendors is processed in a Linux system and converted via MSConvert, after which the converted file is returned for subsequent analysis using MSThunder.: "our process the raw data in a Linux system and return the converted file. Then, you can subsequently analyze the data using MSThunder after"
- [readme] MSConvert conversion is the standardized pathway for handling vendor proprietary formats before MSThunder analysis.: "The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert"
- [readme] Environment and platform constraints are critical to the workflow design.: "Due to environment configuration issues, the current version does not yet support offline processing of raw data"
- [readme] Ubuntu 20.04 is the validated operational environment for the conversion workflow.: "The training data, code, model parameters and candidates used for training and prediction are available through our experiments conducted on an Ubuntu 20.04 environment"
- [readme] Files must be placed in the MSThunder directory for downstream processing after conversion.: "First, the batch-processed files need to be placed in the MSThunder directory"
