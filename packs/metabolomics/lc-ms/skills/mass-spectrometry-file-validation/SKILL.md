---
name: mass-spectrometry-file-validation
description: Use when after MSConvert has converted vendor-specific raw mass spectrometry data (ThermoFisher, Agilent, or equivalent formats) on a Linux system and before initiating analysis in MSThunder.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
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

# mass-spectrometry-file-validation

## Summary

Validate the integrity and format compliance of mass spectrometry data files after conversion from vendor-specific raw formats (ThermoFisher .raw, Agilent .d) to MSThunder-compatible formats via MSConvert. This skill ensures that converted files are suitable for downstream deep learning-based nontargeted analysis of organic pollutants.

## When to use

After MSConvert has converted vendor-specific raw mass spectrometry data (ThermoFisher, Agilent, or equivalent formats) on a Linux system and before initiating analysis in MSThunder. Use this skill whenever you need to verify that the converted file preserves spectral integrity, contains expected MS1/MS2 metadata, and conforms to MSThunder's input requirements.

## When NOT to use

- The input file is still in vendor-specific raw format (ThermoFisher .raw, Agilent .d) and has not yet been converted by MSConvert.
- You are validating files intended for use with non-MSThunder analysis pipelines or different mass spectrometry software that may have different format requirements.
- The converted file has already been successfully ingested and processed by MSThunder without errors; re-validation is redundant.

## Inputs

- Converted mass spectrometry data file (MSThunder-compatible format, output from MSConvert)
- Reference metadata about the original raw file (vendor format, instrument type, ion mode)

## Outputs

- Validation report (pass/fail status with identified errors or warnings)
- Verified converted file ready for MSThunder batch processing

## How to apply

Following MSConvert command-line conversion on Ubuntu 20.04, validate the converted file by (1) checking file format compliance against MSThunder specifications (e.g., presence of MS1 and MS2 spectra, retention time data, precursor m/z values); (2) verifying that critical metadata fields (ion mode, scan type, instrument source) are intact and parseable; (3) confirming file size and structure integrity are consistent with input raw-data size; (4) optionally performing a test load into MSThunder's interface to confirm batch-processed files can be ingested without errors. The rationale is that conversion artifacts, truncation, or metadata loss during vendor format translation can silently compromise downstream identification accuracy in the deep learning model; early detection prevents wasted computational resources and unreliable pollutant predictions.

## Related tools

- **MSConvert** (Converts vendor-specific raw mass spectrometry data to MSThunder-compatible format prior to validation)
- **MSThunder** (Destination analysis tool; validation confirms file format compliance with MSThunder's batch-processing requirements) — github.com/LQZ0123/MSThunder
- **Ubuntu 20.04** (Operating environment where MSConvert conversion and file validation are performed)

## Evaluation signals

- Converted file can be successfully loaded into MSThunder's interface without import errors or missing metadata warnings.
- MS1 and MS2 spectral data are present and non-empty; retention time range aligns with expected chromatographic window for the original raw data.
- Precursor m/z values, ion modes (Positive/Negative), and scan metadata are intact and parseable by MSThunder's model inference layer.
- File size is consistent with the expected output of vendor-format conversion (typically 30–70% of original raw file size for mzML/mzXML); significant size loss or truncation indicates corruption.
- No floating-point NaN, Inf, or null values appear in critical spectral intensity or m/z columns that would cause downstream feature extraction failure.

## Limitations

- The current version of MSThunder does not yet support offline processing of raw data, so validation must occur before submission for online processing or manual email-based conversion.
- MSConvert compatibility depends on vendor SDK availability; some proprietary raw formats may fail to convert or lose metadata during translation.
- Validation can confirm structural integrity but cannot guarantee chemical accuracy of peak assignments or spectral quality; low signal-to-noise ratios or instrument artifacts may pass validation but yield poor identification results.
- File size and metadata checks are heuristic and may not catch subtle corruption in spectral intensity arrays or retention time calibration errors that only manifest during deep learning inference.

## Evidence

- [other] Raw data from ThermoFisher, Agilent, and other vendors is processed in a Linux system and converted via MSConvert, after which the converted file is returned for subsequent analysis using MSThunder.: "our process the raw data in a Linux system and return the converted file. Then, you can subsequently analyze the data using MSThunder after"
- [other] Validate converted file integrity and format compliance is a required step in the MSConvert conversion workflow before MSThunder analysis.: "4. Validate converted file integrity and format compliance. 5. Return the converted file for downstream MSThunder analysis."
- [readme] The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert.: "The current version is compatible with ThermoFisher, Agilent, and other vendors whose raw data can be converted via MSConvert"
- [readme] Batch-processed files must be placed in the MSThunder directory before analysis begins.: "First, the batch-processed files need to be placed in the MSThunder directory."
- [readme] MSThunder provides MS1/MS2 spectra, TIC, retention time, and precursor information that must be validated.: "enter the specified 'precursor/retention time' to search for the TIC of the precursor ion and the MS2 information at that retention time"
