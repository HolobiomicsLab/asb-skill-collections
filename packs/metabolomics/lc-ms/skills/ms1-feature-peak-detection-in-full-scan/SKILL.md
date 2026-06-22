---
name: ms1-feature-peak-detection-in-full-scan
description: Use when you have merged MS1 spectra (output from spectral binning/merging steps) from a full-scan FIA-MS or LC-MS acquisition and need to identify distinct molecular features before accurate mass annotation or background filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3291
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SmartPeak
  - SmartPeakGUI
  - SmartPeakCLI
  - OpenMS
  - pyOpenMS
  - BFAIR
  techniques:
  - LC-MS
  - direct-infusion-MS
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

# ms1-feature-peak-detection-in-full-scan

## Summary

Detects MS1 features (molecular ions) from full-scan mass spectrometry data by applying peak-picking algorithms to merged spectra. This is a foundational step in untargeted metabolomics workflows that converts raw spectral bins into discrete, annotatable molecular features.

## When to use

Apply this skill when you have merged MS1 spectra (output from spectral binning/merging steps) from a full-scan FIA-MS or LC-MS acquisition and need to identify distinct molecular features before accurate mass annotation or background filtering. Use it in semi-targeted or untargeted workflows where analyte masses are unknown and must be discovered from the full m/z range (typically 0–1500 m/z in FIA-MS).

## When NOT to use

- Input is already a manually curated or vendor-provided target feature list (use only for targeted methods with known analyte masses).
- Spectra have not been merged or binned; apply MERGE_SPECTRA first to reduce noise and improve peak signal.
- Raw data is from a targeted SIM or MRM acquisition (use PICK_MRM_FEATURES instead, which is optimized for single-ion monitoring).

## Inputs

- merged spectra (mzML or OpenMS FeatureMap format with binned m/z and time axes)
- mass spectrometry resolution setting (e.g., 12000 for FIAMS)
- m/z range bounds (e.g., 0–1500 for FIA-MS FullScan)

## Outputs

- MS1 feature list (FeatureMap or feature table with m/z, retention time, intensity, charge state)
- peak picking parameters and QC metrics (e.g., number of features detected, intensity statistics)

## How to apply

After loading raw mass spectrometry data and merging spectra along the time axis using bin_step of 20 (or equivalent), apply PICK_MS1_FEATURES to the merged spectra to extract discrete peaks. The algorithm identifies local maxima in the m/z and retention-time space, respecting the mass resolution setting (e.g., FIAMS resolution of 12000). Each detected peak is assigned a mass-to-charge ratio, intensity, and temporal coordinate. Validate that the number and intensity distribution of picked features are reasonable for your sample type (e.g., blank samples should yield fewer features than treated samples); compare feature counts and intensity patterns across injections in the same sequence to judge consistency.

## Related tools

- **SmartPeak** (orchestrates MS1 feature detection via PICK_MS1_FEATURES workflow module; provides graphical and CLI interfaces for workflow execution and QC visualization) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakGUI** (allows interactive workflow design, feature visualization (line plots, heatmaps, matrices), and result inspection including chromatogram overlays for debugging peak-picking failures) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (underlying toolkit providing the FeatureFinderMetabo and FeatureFinderCentroided algorithms used by PICK_MS1_FEATURES for peak detection)
- **pyOpenMS** (Python binding for programmatic access to peak-picking functions; enables custom scripting and batch processing of feature detection)
- **BFAIR** (provides post-processing tools for untargeted FIA-MS metabolomics, including feature filtering, background estimation, and downstream analysis pipelines) — https://github.com/AutoFlowResearch/BFAIR

## Evaluation signals

- Feature count is consistent across replicate injections of the same sample (low coefficient of variation in number of detected features).
- Blank samples yield significantly fewer detected features than treated samples (validate by comparing feature lists before and after FILTER_FEATURES_BACKGROUND_INTERFERENCES).
- Picked m/z values align with expected adducts after SEARCH_ACCURATE_MASS mapping (e.g., [M+H]+ clusters appear at nominal mass + 1.008 Da).
- Feature intensity distribution shows expected enrichment in low m/z region typical of metabolites (validate via histogram or heatmap visualization in SmartPeakGUI).
- Merging of adducts (MERGE_FEATURES) consolidates multiple m/z peaks into single compounds without losing true distinct metabolites (check feature count before and after merging).

## Limitations

- Peak-picking sensitivity depends critically on mass resolution setting and spectral binning parameters; suboptimal bin_step or resolution can cause missed features or false positives.
- Isobaric and near-isobaric metabolites may not be resolved at moderate mass resolution (≤12000 ppm); require higher resolution (Orbitrap, TOF) to separate.
- Background interferences in blank samples can cause spurious feature detection; must be estimated and filtered using ESTIMATE_FEATURE_BACKGROUND_INTERFERENCES and FILTER_FEATURES_BACKGROUND_INTERFERENCES to avoid false annotations.
- No changelog documented for the SmartPeak version used; reproducibility and parameter defaults may vary between releases.

## Evidence

- [methods] Detect MS1 features from merged spectra using PICK_MS1_FEATURES: "Detect MS1 features from merged spectra using PICK_MS1_FEATURES."
- [methods] Extract spectra windows with FIAMS resolution set to 12000 and max_mz to 1500: "Extract spectra windows over the acquisition time range (0–30 min) using EXTRACT_SPECTRA_WINDOWS with FIAMS resolution set to 12000 and max_mz to 1500."
- [methods] Merge spectra along the time axis using bin_step of 20 before peak detection: "Merge spectra along the time axis using bin_step of 20 with MERGE_SPECTRA."
- [intro] SmartPeak automates workflow steps from peak detection and integration over calibration curve optimization, to quality control reporting: "SmartPeak automates workflow steps from peak detection and integration over calibration curve optimization, to quality control reporting"
- [readme] README describes feature visualization in multiple forms including line plots and heatmaps: "The results can be viewed in a graphical form as a line plot or as a heatmap with ``View | features (line)``."
- [methods] Background filtering follows feature detection in the workflow: "Filter features based on blank signal intensity threshold using FILTER_FEATURES_BACKGROUND_INTERFERENCES."
