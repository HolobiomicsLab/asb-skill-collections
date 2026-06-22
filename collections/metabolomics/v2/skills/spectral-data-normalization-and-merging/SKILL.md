---
name: spectral-data-normalization-and-merging
description: Use when you have acquired multiple MS1 spectra over a defined acquisition time range (e.g., 0–30 s in FIA-MS) and need to combine them into a unified spectrum before feature detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - OpenMS
  - SmartPeak
  - SmartPeakCLI
  - pyOpenMS
derived_from:
- doi: 10.1021/acs.analchem.0c03421
  title: SmartPeak
evidence_spans:
- The software is based on the OpenMS toolkit
- The software is based on the OpenMS toolkit.
- SmartPeak automates targeted and quantitative metabolomics data processing
- SmartPeak CLI provides an equivalent of SmartPeak GUI application, however with a possibility to run in headless mode
- SmartPeak CLI provides an equivalent of SmartPeak GUI application
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smartpeak_cq
    doi: 10.1021/acs.analchem.0c03421
    title: SmartPeak
  dedup_kept_from: coll_smartpeak_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03421
  all_source_dois:
  - 10.1021/acs.analchem.0c03421
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-data-normalization-and-merging

## Summary

Merge and normalize MS1 spectra acquired across a time window into a single composite spectrum, then perform peak picking to detect molecular features. This skill is essential for FIA-MS and other flow-injection workflows where multiple spectra must be aggregated to improve signal-to-noise and feature detection sensitivity.

## When to use

Apply this skill when you have acquired multiple MS1 spectra over a defined acquisition time range (e.g., 0–30 s in FIA-MS) and need to combine them into a unified spectrum before feature detection. This is particularly valuable for FIA-MS data where metabolite residence time in the ion source spans multiple scans, and signal averaging is needed to overcome individual-scan noise.

## When NOT to use

- Input data is already a feature table or pre-processed peak list — skip directly to annotation.
- You are processing targeted LC-MS/MS data with pre-defined MRM transitions — use chromatographic extraction and peak picking specific to those transitions instead.
- Raw spectra have already been merged or normalized by the instrument acquisition software — verify before re-merging to avoid double-processing.

## Inputs

- raw FIA-MS data (mzML format)
- acquisition time range specification (e.g., 0–30 s)
- MS1 instrument parameters (resolution, max_mz, bin_step)
- mass calibration metadata

## Outputs

- merged composite MS1 spectrum
- MS1 feature list (detected peaks with m/z and intensity)
- feature detection quality metrics

## How to apply

Load raw FIA-MS data and extract spectra windows over the specified acquisition time range using configured MS1 parameters (e.g., resolution 12000, max_mz 1500, bin_step 20). Merge the spectra along the time axis to create a single, normalized composite spectrum. Apply MS1 peak picking on the merged spectrum to detect molecular features at their true m/z and intensity. The rationale is that time-series merging reduces scan-to-scan noise while preserving feature signal, enabling more reliable peak detection and subsequent accurate mass matching against metabolite databases.

## Related tools

- **SmartPeak** (Orchestrates the full workflow including spectrum extraction, merging, and MS1 peak picking via predefined workflow steps (EXTRACT_SPECTRA_WINDOWS, MERGE_SPECTRA, PICK_MS1_FEATURES)) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (Command-line interface for running spectral merging and peak picking workflows non-interactively or within containerized environments) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying toolkit providing MS1 peak picking, spectra merging, and mass calibration algorithms)
- **pyOpenMS** (Python bindings for post-processing and programmatically accessing merged spectrum and peak picking results)

## Examples

```
docker run --rm -ti -v C:/data:/sample-data autoflowresearch/smartpeak-cli:latest bash -c "smartpeak --workflow FIAMS_FullScan --input /sample-data/raw.mzML --time-range 0:30 --resolution 12000 --output /sample-data/features.featureXML"
```

## Evaluation signals

- Merged spectrum signal-to-noise ratio is higher than individual input spectra, with noise floor reduced and peaks sharpened.
- MS1 feature list contains expected number of peaks with m/z values and intensities consistent with the analyte list and within configured mass error tolerance.
- Presence of known reference metabolite m/z values in the feature list (if reference standards were included in the FIA run).
- Peak intensity reproducibility: repeated merges of the same time window produce feature lists with consistent peak heights (within instrument drift tolerances).
- No duplicate or fragmented peaks in the output feature list; each molecular feature is represented once with consolidated m/z and intensity.

## Limitations

- Merging is sensitive to time window selection — too narrow a window reduces signal, too wide includes off-target background or co-eluting contaminants. Optimization requires empirical validation.
- Peak picking quality depends on instrument resolution and calibration; mass error exceeding the configured tolerance (e.g., >5 ppm) will cause missed or misaligned peaks.
- For samples with very high metabolite diversity or dynamic concentration range, aggressive merging can lead to peak overlap or weak peaks obscured by strong neighbours; feature selection filtering may be required post-detection.
- The workflow assumes stable ion source conditions across the acquisition window; rapid changes in pH, temperature, or solvent composition during FIA infusion may degrade merging effectiveness.

## Evidence

- [other] 1. Load raw FIA-MS data and extract spectra windows over the specified acquisition time range (0–30 s) using the FIAMS parameters (resolution 12000, max_mz 1500, bin_step 20). 2. Merge spectra along the time axis and perform MS1 peak picking to detect molecular features.: "1. Load raw FIA-MS data and extract spectra windows over the specified acquisition time range (0–30 s) using the FIAMS parameters (resolution 12000, max_mz 1500, bin_step 20). 2. Merge spectra along"
- [other] SmartPeak automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting, which collectively support the generation of comprehensive data summaries including feature annotations and quality metrics.: "SmartPeak automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting"
- [methods] EXTRACT_SPECTRA_WINDOWS, MERGE_SPECTRA, PICK_MS1_FEATURES: "EXTRACT_SPECTRA_WINDOWS, MERGE_SPECTRA, PICK_MS1_FEATURES"
- [readme] The software is based on the OpenMS toolkit.: "The software is based on the OpenMS toolkit."
- [readme] SmartPeak is an application that encapsulates advanced algorithms to enable fast, accurate, and automated processing of CE-, GC- and LC-MS(/MS) data, and HPLC data for targeted and semi-targeted metabolomics, lipidomics, and fluxomics experiments.: "SmartPeak is an application that encapsulates advanced algorithms to enable fast, accurate, and automated processing of CE-, GC- and LC-MS(/MS) data, and HPLC data for targeted and semi-targeted"
