---
name: multi-platform-ms-integration
description: Use when you have untargeted metabolomics data from multiple MS instruments
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3373
  tools:
  - ROIpeaks
  - MSroiaug
  - Bioinformatic Toolbox
  - Statistics And Machine Learning Toolbox
  - Wavelet Toolbox
  - Image Processing Toolbox
  - Signal Processing Toolbox
  - msconvert
  - MATLAB R2024a
  - ZMat
  techniques:
  - LC-MS
  - CE-MS
  license_tier: restricted
derived_from:
- doi: 10.1007/s00216-023-04715-6
  title: AriumMS
- doi: 10.1038/protex.2015.102
  title: ''
evidence_spans:
- functions (ROIpeaks, MSroiaug) developed by Romà Tauler, Eva Gorrochategui and Joaquim
  Jaumot
- 'Required toolboxes for the app version: Bioinformatic Toolbox, Statistics And Machine
  Learning Toolbox, Wavelet Toolbox, Image Processing Toolbox, Signal Processing Toolbox,
  Parallel Computing'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ariumms_cq
    doi: 10.1007/s00216-023-04715-6
    title: AriumMS
  dedup_kept_from: coll_ariumms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-04715-6
  all_source_dois:
  - 10.1007/s00216-023-04715-6
  - 10.1038/protex.2015.102
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-platform-ms-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Unified preprocessing and feature extraction across heterogeneous mass spectrometry platforms (CE-MS and LC-MS) by converting vendor formats to standardized mzXML/mzML, then applying parameter-driven ROI detection, normalization, and augmentation. Enables cross-platform metabolomics studies without platform-specific reimplementation.

## When to use

You have untargeted metabolomics data from multiple MS instruments (e.g., both capillary electrophoresis-MS and liquid chromatography-MS) in vendor-native or unconverted formats, and you need to extract comparable features across all platforms using the same ROI, preprocessing, and augmentation logic. Applies when you must unify feature detection across instruments that differ in ionization, separation, or detector characteristics but analyze the same biological samples.

## When NOT to use

- Input is already a finalized, cross-platform feature table or consensus peak list — ROI detection and augmentation are redundant.
- Data are from a single MS platform or instrument — use platform-specific preprocessing; multi-platform integration adds no value.
- Vendor software has already performed proprietary peak picking and alignment — re-applying ROI search may introduce conflicting peak calls or inconsistent feature definitions.

## Inputs

- Vendor MS data files (raw proprietary formats: .raw, .d, .ms, etc.)
- mzXML or mzML format files (after msconvert conversion)
- ROI search parameter configuration (mass tolerance, intensity threshold, retention-time window)
- Data preprocessing parameter set (normalization method, intensity scaling factor, alignment tolerance)
- Data augmentation parameter set (augmentation method, sample-level or feature-level augmentation flags)

## Outputs

- Augmented feature matrix (rows=features, columns=samples, aligned across platforms)
- Feature metadata (m/z, retention time, platform origin, ROI coordinates)
- Processing metadata (parameters used, number of ROIs detected per platform, preprocessing statistics)
- Exported feature tables (standardized format for downstream multivariate or statistical analysis)

## How to apply

First, convert all vendor MS data files to mzXML or mzML format using msconvert (ProteoWizard); this standardization allows downstream tools to parse mass, retention time, and intensity uniformly. Load the converted files into MATLAB R2024a with required toolboxes (Bioinformatic, Statistics and Machine Learning, Wavelet, Image Processing, Signal Processing, Parallel Computing). Apply the ROIpeaks function with uniform ROI search parameters (e.g., mass-window width, intensity threshold) to detect candidate m/z × time regions across all platform datasets. Execute data preprocessing on detected ROIs to apply consistent normalization (e.g., intensity scaling, retention-time alignment) to all platforms simultaneously. Finally, apply MSroiaug augmentation using identical augmentation parameters to all preprocessed ROI sets, ensuring feature matrices from different platforms are comparable. Export augmented feature matrices and metadata to enable cross-platform statistical analysis (e.g., multivariate or univariate comparisons).

## Related tools

- **msconvert** (Converts vendor MS data (raw, .d, .ms) to standardized mzXML/mzML formats for uniform parsing across platforms) — http://proteowizard.sourceforge.net/download.html
- **ROIpeaks** (Detects regions of interest (m/z × retention-time windows) from converted MS data using user-set mass tolerance and intensity thresholds) — https://doi.org/10.1038/protex.2015.102
- **MSroiaug** (Augments preprocessed ROI feature data according to configurable augmentation parameters to enrich training sets or expand feature coverage) — https://doi.org/10.1038/protex.2015.102
- **MATLAB R2024a** (Execution environment and orchestration platform for sequential pipeline execution (ROI detection, preprocessing, augmentation) with required Toolboxes)
- **ZMat** (Data compression and encoding library integrated for efficient storage and transmission of large augmented feature matrices) — http://github.com/fangq/zmat

## Evaluation signals

- Feature matrix dimensions match across platforms after augmentation (rows = union of detected ROIs, columns = total samples) and no NaN/Inf entries are present in intensity values.
- ROI detection consistency: verify that known metabolite m/z values (internal standards, reference compounds) are detected on all platforms within configured mass tolerance (e.g., ±5 ppm); absence on any platform indicates preprocessing or parameter misconfiguration.
- Augmentation metadata report: confirm that augmentation parameters (method, sample count, feature count before/after) are logged and consistent across platforms; augmentation should increase feature count or sample count as configured.
- Cross-platform correlation of intensities for spiked-in or endogenous landmarks: compute Pearson or Spearman correlation of intensity ranks for well-known metabolites across platforms; r > 0.7 suggests successful normalization and augmentation.
- Export schema compliance: confirm that output feature tables, metadata, and processing logs conform to expected column names, data types (numeric intensity, integer m/z, float retention time), and row/column order.

## Limitations

- Platform-specific artifacts (ionization bias, detector saturation) are not explicitly corrected; ROI-based ROI search assumes similar signal-to-noise distributions across CE-MS and LC-MS, which may not hold for low-abundance features on one platform.
- Parameter portability is manual: users must empirically verify that ROI search parameters (mass window, intensity threshold) yield comparable numbers of ROIs and similar feature coverage on both platforms; no automated parameter optimization across platforms is described.
- Augmentation may introduce synthetic or biased feature correlations if augmentation method is not platform-aware; the article does not discuss whether augmentation is performed per-platform or globally, which affects downstream statistical validity.
- No changelog or version-history documentation is provided for AriumMS, limiting reproducibility across software updates.
- Computational cost scales with number of platforms, sample count, and augmentation intensity; the article does not benchmark runtime or memory usage for large multi-platform studies.

## Evidence

- [readme] Set parameters are then used to perform ROI search, data preprocessing and data augmentation.: "Set parameters are then used to perform ROI search, data preprocessing and data augmentation."
- [other] AriumMS implements a three-stage pipeline where user-set parameters drive sequential execution of ROI search, data preprocessing, and data augmentation stages.: "AriumMS implements a three-stage pipeline where user-set parameters drive sequential execution of ROI search, data preprocessing, and data augmentation stages."
- [readme] For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project: "For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project"
- [other] These stages use ROIpeaks and MSroiaug functions developed by Tauler, Gorrochategui, and Jaumot to process converted MS data.: "These stages use ROIpeaks and MSroiaug functions developed by Tauler, Gorrochategui, and Jaumot to process converted MS data."
- [readme] All in one tool for untargeted Metabolomics by ROI and augmentation of multiple Data sets.: "All in one tool for untargeted Metabolomics by ROI and augmentation of multiple Data sets."
