---
name: spectral-data-format-conversion
description: Use when you have raw LC–MS data in vendor-proprietary or uncorrected formats (e.g., .raw, .d) and need to perform targeted peak detection, retention-time correction, or automated quality metrics on identified compounds. The input files must be converted to .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Spectra
  - xcms
  - R
  - knitr
  - kableExtra
  - ProteoWizard MSConvert
  - TARDIS
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- loads MS data as `Spectra` objects so it's easily integrated with other tools
- It makes use of an established retention time correction algorithm from the `xcms` package
- R package for *TArgeted Raw Data Integration In Spectrometry*
- knitr::include_graphics
- kableExtra::kable
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis
schema_version: 0.2.0
---

# Spectral Data Format Conversion

## Summary

Convert raw mass spectrometry data files to centroided .mzML format, a prerequisite for targeted peak detection and quality assessment in LC–MS metabolomics workflows. This ensures compatibility with downstream tools like TARDIS that require standardized, centroided spectral representation.

## When to use

You have raw LC–MS data in vendor-proprietary or uncorrected formats (e.g., .raw, .d) and need to perform targeted peak detection, retention-time correction, or automated quality metrics on identified compounds. The input files must be converted to .mzML with centroiding applied before running targeted extraction tools like tardisPeaks().

## When NOT to use

- Input data is already in centroided .mzML format — skip conversion and load directly into Spectra.
- Profile-mode spectra are required for your analysis (e.g., high-resolution isotope pattern analysis) — centroiding loses intensity information across the profile.
- You are working with data from instruments that produce native .mzML output (e.g., some newer instruments) — verify file format before conversion.

## Inputs

- Vendor raw mass spectrometry data files (e.g., .raw, .d, or other proprietary formats)
- ProteoWizard MSConvert configuration or CLI parameters

## Outputs

- Centroided .mzML files ready for import into Spectra package
- Spectral data in standardized format compatible with retention-time correction and targeted peak detection

## How to apply

Use ProteoWizard's MSConvert tool to convert vendor raw files to .mzML format with centroiding enabled. Centroiding reduces noise and converts profile mode spectra to discrete peak lists, which is required for reliable m/z and intensity-based peak detection in TARDIS. Ensure all input files undergo this conversion uniformly before constructing a target list (compound ID, name, m/z, RT, polarity) and passing the converted files to the targeted extraction workflow. Verify that the output .mzML files contain centroided spectra and can be read as Spectra objects in R.

## Related tools

- **ProteoWizard MSConvert** (Converts vendor-proprietary mass spectrometry raw files to centroided .mzML format for downstream targeted analysis)
- **Spectra** (Loads converted .mzML files as Spectra objects in R for downstream TARDIS processing)
- **TARDIS** (Downstream tool that requires centroided .mzML input for targeted peak detection and quality assessment) — https://github.com/pablovgd/TARDIS

## Evaluation signals

- Output .mzML files can be successfully read by the Spectra R package without errors or warnings.
- Inspect a sample EIC (extracted ion chromatogram) from the converted files to verify peaks are cleanly separated and represent centroided data (discrete m/z points rather than profiles).
- The number of scans and retention time range in converted .mzML matches the original vendor file metadata.
- Centroiding reduced file size and noise compared to profile-mode input, observable in peak signal-to-noise ratio when visualized.
- Subsequent tardisPeaks() execution with screening_mode=FALSE completes without format-related errors and produces expected output tables (AUC, Max Intensity, SNR, peak_cor).

## Limitations

- Centroiding is lossy: converts continuous intensity profiles to discrete m/z values, which may reduce resolution for fine isotope pattern analysis.
- File conversion can introduce timeout issues when handling large datasets; the TARDIS README recommends increasing R's timeout setting (e.g., options(timeout = '300')).
- Vendor-specific metadata (e.g., instrument configuration, calibration data) may not fully transfer to .mzML; verify critical instrument parameters are preserved in the output.
- MSConvert centroiding algorithm parameters (peak-picking method, noise threshold) vary by instrument type; users should verify that chosen parameters suit their instrument and metabolite concentration range.

## Evidence

- [intro] Input files need to be converted to the .mzML format and have to be centroided: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] File conversion using MSConvert (ProteoWizard): "For file conversion using MSConvert (ProteoWizard)"
- [intro] loads MS data as Spectra objects for integration with downstream tools: "loads MS data as `Spectra` objects so it's easily integrated with other tools"
- [readme] Timeout setting recommendation for large datasets: "Since the package contains some example data, connection timeout is often an issue. You can increase your timeout setting in R using: options(timeout = "300")"
