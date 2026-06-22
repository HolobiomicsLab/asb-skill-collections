---
name: blank-sample-background-interference-estimation
description: Use when after MS1 feature detection and accurate mass annotation, when you have identified a set of blank injections (negative controls) run in the same analytical sequence segment as your biological or study samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3678
  tools:
  - SmartPeak
  - SmartPeakGUI
  - SmartPeakCLI
  - OpenMS
  - pyOpenMS
  - BFAIR
derived_from:
- doi: 10.1021/acs.analchem.0c03421
  title: SmartPeak
evidence_spans:
- SmartPeak automates targeted and quantitative metabolomics data processing
- SmartPeak GUI provides functionality to facilitate users to get up and running as quickly as possible
- SmartPeak CLI provides an equivalent of SmartPeak GUI application, however with a possibility to run in headless mode
- SmartPeak CLI provides an equivalent of SmartPeak GUI application
- The software is based on the OpenMS toolkit
- The software is based on the OpenMS toolkit.
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
---

# blank-sample-background-interference-estimation

## Summary

Estimates background noise and interference signals from blank samples within the same sequence segment to enable subsequent filtering of low-confidence metabolite features. This skill is essential in untargeted FIA-MS and LC-MS workflows to distinguish true analyte signals from instrumental and solvent artifacts.

## When to use

Apply this skill after MS1 feature detection and accurate mass annotation, when you have identified a set of blank injections (negative controls) run in the same analytical sequence segment as your biological or study samples. Use it specifically when you need to quantify baseline interference intensity for each detected feature before deciding which features to retain in downstream analysis.

## When NOT to use

- Blank samples are not available or not run in the same sequence segment—background estimation requires authentic negative controls from the same analytical batch to account for instrument drift and carry-over.
- Features have already been filtered or merged across multiple analytical segments—background estimation is most reliable when applied before feature merging.
- Your analysis goal is targeted metabolomics with predefined SRM/MRM transitions—this skill is designed for untargeted MS1 feature discovery, not for monitoring known analytes with internal standards.

## Inputs

- MS1 feature list with m/z, retention time, and detected peak intensities
- mzML or raw mass spectrometry data files for blank (negative control) injections
- Sequence file with sample metadata and blank injection identifiers
- Accurate mass annotations (from SEARCH_ACCURATE_MASS step)

## Outputs

- Background interference intensity estimates per feature (e.g., blank mean, max, or SD)
- Feature background estimation table (CSV or mzTab format)
- Background statistics metadata attached to each feature

## How to apply

First, extract all blank sample injections from your sequence file that belong to the same analytical segment as your study samples. For each detected MS1 feature (m/z and retention time), measure the signal intensity (peak height or area) in the blank injections using the same peak detection and integration parameters applied to study samples. Calculate a background intensity statistic (e.g., mean, median, or maximum) across the blank replicates for each feature. Store these background estimations alongside the original feature annotations. This enables the next filtering step (FILTER_FEATURES_BACKGROUND_INTERFERENCES) to apply a signal-to-noise threshold (e.g., sample feature intensity > 3× blank mean) and remove features whose study-sample signals are not significantly elevated above background.

## Related tools

- **SmartPeak** (Automates the complete FIA-MS workflow including background estimation via ESTIMATE_FEATURE_BACKGROUND_INTERFERENCES step) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (Command-line interface for programmatic execution of background interference estimation workflows) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying feature detection and integration algorithms used by SmartPeak for MS1 peak quantification in blanks and samples)
- **pyOpenMS** (Python API for parsing and processing mzTab annotations and feature lists containing background metadata)
- **BFAIR** (Post-processing and statistical analysis of untargeted FIA-MS data including background-filtered feature tables) — https://github.com/AutoFlowResearch/BFAIR

## Evaluation signals

- Background intensity estimates are non-zero and realistic (not saturated or below instrument detection limit) for a majority of features.
- Background mean intensity is lower than study sample intensity for features retained after filtering (i.e., signal-to-noise ratio > threshold).
- Features removed by FILTER_FEATURES_BACKGROUND_INTERFERENCES have background intensity ≥ study sample intensity, confirming they are noise-dominated.
- Background estimation results are stored in a parseable format (CSV or mzTab) with clear column headers (feature_id, background_intensity_mean, background_intensity_sd, blank_injection_count).
- Number of blank injections used for background estimation matches the count in the sequence file for the segment; verify no blanks were missed or duplicated.

## Limitations

- Requires at least 2–3 blank injections per sequence segment for statistically meaningful background estimation; sparse blanks may not capture instrumental drift.
- Background estimation assumes blank and sample injections use identical acquisition parameters (resolution, m/z window, integration method); parameter mismatches invalidate comparison.
- Cannot distinguish between true low-abundance analytes and background noise in blanks if the blank itself is contaminated or if sample carry-over from previous injections affects blank peaks.
- Absolute background intensity varies with instrument calibration, column condition, and solvent lot; re-estimation is recommended when significant instrument maintenance is performed or solvents are replaced.

## Evidence

- [methods] Estimate background interferences from blank samples in the same sequence segment using ESTIMATE_FEATURE_BACKGROUND_INTERFERENCES.: "Estimate background interferences from blank samples in the same sequence segment using ESTIMATE_FEATURE_BACKGROUND_INTERFERENCES."
- [methods] Filter features based on blank signal intensity threshold using FILTER_FEATURES_BACKGROUND_INTERFERENCES.: "Filter features based on blank signal intensity threshold using FILTER_FEATURES_BACKGROUND_INTERFERENCES."
- [other] SmartPeak automates workflow steps from peak detection and integration over calibration curve optimization, to quality control reporting, which form the basis for configuring analysis types such as FIAMS FullScan Unknowns.: "SmartPeak automates workflow steps from peak detection and integration over calibration curve optimization, to quality control reporting"
- [readme] Tools for analyzing untargeted FIA-MS metabolomics data: "Tools for analyzing untargeted FIA-MS metabolomics data"
