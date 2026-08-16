---
name: parameter-driven-preprocessing-pipeline
description: Use when you have converted mass spectrometry data in mzXML or mzML format and need to extract metabolic features via region-of-interest (ROI) search followed by preprocessing and augmentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ROIpeaks
  - MSroiaug
  - Bioinformatic Toolbox
  - Statistics And Machine Learning Toolbox
  - Wavelet Toolbox
  - Image Processing Toolbox
  - Signal Processing Toolbox
  - MATLAB R2024a
  - Bioinformatics Toolbox
  - Statistics and Machine Learning Toolbox
  - Parallel Computing Toolbox
  - ZMat toolbox
  - msconvert
  - AriumMS
  techniques:
  - LC-MS
  - CE-MS
derived_from:
- doi: 10.1007/s00216-023-04715-6
  title: AriumMS
evidence_spans:
- functions (ROIpeaks, MSroiaug) developed by Romà Tauler, Eva Gorrochategui and Joaquim Jaumot
- 'Required toolboxes for the app version: Bioinformatic Toolbox, Statistics And Machine Learning Toolbox, Wavelet Toolbox, Image Processing Toolbox, Signal Processing Toolbox, Parallel Computing'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# parameter-driven-preprocessing-pipeline

## Summary

A skill for executing sequential ROI detection, data normalization, and feature augmentation on mass spectrometry data using user-configurable parameters to control each processing stage. This skill is essential for untargeted metabolomics workflows where signal extraction, cleaning, and augmentation must be reproducibly tuned across multiple LC-MS or CE-MS datasets.

## When to use

Use this skill when you have converted mass spectrometry data in mzXML or mzML format and need to extract metabolic features via region-of-interest (ROI) search followed by preprocessing and augmentation. Specifically apply it when: (1) you must systematically detect signals across m/z and retention time dimensions; (2) detected regions require normalization and artifact removal before feature analysis; (3) you need to augment sparse or noisy ROI data to improve coverage; and (4) parameters must be tunable across multiple datasets to ensure consistency.

## When NOT to use

- Input data is already a processed feature matrix (e.g., pre-extracted ion chromatograms or aligned peaks from other software) — skip to statistical analysis instead.
- MS data is in vendor-specific binary format without prior conversion to mzXML/mzML — run msconvert (ProteoWizard) first.
- You require targeted analysis of a predefined set of known metabolites — use targeted quantitation workflows instead of ROI-based untargeted detection.

## Inputs

- mzXML file (converted MS raw data)
- mzML file (converted MS raw data)
- ROI search parameters (m/z tolerance, retention time window, intensity threshold, minimum peak width)
- preprocessing configuration (normalization method, background subtraction method, noise floor threshold)
- augmentation parameters (expansion window, interpolation method, edge handling strategy)

## Outputs

- augmented feature matrix (rows: features/ROIs, columns: samples; values: normalized intensities)
- ROI metadata table (m/z center, retention time center, detected width, augmentation status)
- processing report (parameters used, number of ROIs detected, number augmented, data quality metrics)

## How to apply

Load converted MS data (mzXML or mzML format) into MATLAB R2024a with required toolboxes (Bioinformatics, Statistics and Machine Learning, Wavelet, Image Processing, Signal Processing, Parallel Computing). Define ROI search parameters (e.g., m/z tolerance, retention time window, intensity threshold) and apply the ROIpeaks function to identify regions of interest from the mass spectrometry data. Execute the preprocessing step on identified ROIs to normalize feature intensities and remove background artifacts according to configured thresholds. Apply the MSroiaug function to augment preprocessed ROI data using augmentation parameters that control expansion or interpolation of detected signals. Export the augmented feature matrix and processing metadata, validating that all ROIs have been processed and that augmentation parameters were consistently applied across the dataset.

## Related tools

- **ROIpeaks** (detects regions of interest (ROIs) from mass spectrometry data using m/z and retention time parameters)
- **MSroiaug** (augments preprocessed ROI data according to configured augmentation parameters to improve feature coverage)
- **MATLAB R2024a** (runtime environment for executing the parameter-driven preprocessing pipeline with required toolboxes)
- **Bioinformatics Toolbox** (supports MS data import and biological data structures for pipeline execution)
- **Statistics and Machine Learning Toolbox** (provides normalization, scaling, and statistical preprocessing functions for feature data)
- **Wavelet Toolbox** (enables wavelet-based noise filtering and feature extraction during preprocessing)
- **Image Processing Toolbox** (supports 2D signal processing (m/z vs. retention time plane) for ROI detection and morphological operations)
- **Signal Processing Toolbox** (provides filtering, smoothing, and signal quality assessment functions for preprocessing)
- **Parallel Computing Toolbox** (enables parallelization of ROI detection and augmentation across multiple datasets)
- **ZMat toolbox** (provides data compression/decompression for efficient storage and I/O of large preprocessed feature matrices) — http://github.com/fangq/zmat
- **msconvert** (prerequisite tool to convert vendor-specific MS data to mzXML or mzML format before pipeline input) — http://proteowizard.sourceforge.net/download.html
- **AriumMS** (complete application integrating ROIpeaks, MSroiaug, and parameter management for untargeted metabolomics) — https://github.com/AdrianHaun/AriumMS

## Evaluation signals

- All ROIs detected by ROIpeaks are present in the output feature matrix with no missing samples or features.
- Feature intensities are normalized (e.g., unit variance or robust scaling) and show expected distribution across samples without outliers from preprocessing artifacts.
- Augmented ROIs show continuous or smoothly interpolated intensity values consistent with neighboring detected ROIs; no discontinuous jumps or NaN values.
- Parameter log records that ROI search, preprocessing, and augmentation parameters were applied identically across all input datasets, confirming reproducibility.
- Output augmented feature matrix dimensions match expected sample count × (detected ROIs + augmented ROIs); row and column labels are consistent with input metadata.

## Limitations

- Pipeline requires vendor-specific data to be pre-converted to mzXML or mzML format via external msconvert tool; conversion errors or incomplete format support may cause data loss.
- Parameter tuning (ROI search thresholds, preprocessing method, augmentation window) is dataset-specific; parameters optimized for one LC-MS platform or sample type may not transfer to different instruments or metabolome compositions.
- Memory and computation time scale with dataset size (number of samples, m/z range, retention time resolution); very large metabolomics studies may require Parallel Computing Toolbox optimization or data partitioning.
- Augmentation can produce artificial features if parameters are set too aggressively; overfitting or false-positive ROIs may inflate feature count without biological validity.
- No built-in version control or change tracking documented; updates to MATLAB toolboxes or underlying ROIpeaks/MSroiaug functions may alter preprocessing behavior without warning.

## Evidence

- [readme] Set parameters are then used to perform ROI search, data preprocessing and data augmentation.: "Set parameters are then used to perform ROI search, data preprocessing and data augmentation."
- [other] AriumMS implements a three-stage pipeline where user-set parameters drive sequential execution of ROI search, data preprocessing, and data augmentation stages.: "AriumMS implements a three-stage pipeline where user-set parameters drive sequential execution of ROI search, data preprocessing, and data augmentation stages."
- [other] Apply ROIpeaks function to detect regions of interest from the mass spectrometry data using configured ROI search parameters.: "Apply ROIpeaks function to detect regions of interest from the mass spectrometry data using configured ROI search parameters."
- [other] Execute data preprocessing step on identified ROIs to normalize and clean the feature data.: "Execute data preprocessing step on identified ROIs to normalize and clean the feature data."
- [other] Apply MSroiaug function to augment the preprocessed ROI data according to augmentation parameters.: "Apply MSroiaug function to augment the preprocessed ROI data according to augmentation parameters."
- [readme] For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project: "For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project"
- [readme] Required toolboxes for the app version: Bioinformatic Toolbox, Statistics And Machine Learning Toolbox, Wavelet Toolbox, Image Processing Toolbox, Signal Processing Toolbox, Parallel Computing Toolbox: "Required toolboxes for the app version: Bioinformatic Toolbox, Statistics And Machine Learning Toolbox, Wavelet Toolbox, Image Processing Toolbox, Signal Processing Toolbox, Parallel Computing Toolbox"
- [other] These stages use ROIpeaks and MSroiaug functions developed by Tauler, Gorrochategui, and Jaumot to process converted MS data.: "These stages use ROIpeaks and MSroiaug functions developed by Tauler, Gorrochategui, and Jaumot to process converted MS data."
