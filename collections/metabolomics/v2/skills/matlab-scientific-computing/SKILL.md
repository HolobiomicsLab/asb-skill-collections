---
name: matlab-scientific-computing
description: Use when you have mass spectrometry data in mzXML or mzML format and
  need to systematically extract regions of interest (ROIs) from multi-dimensional
  m/z-intensity-time arrays, normalize feature values, and augment datasets for untargeted
  metabolomics workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - ROIpeaks
  - MSroiaug
  - MATLAB R2024a
  - Bioinformatic Toolbox
  - Statistics And Machine Learning Toolbox
  - Wavelet Toolbox
  - Image Processing Toolbox
  - Signal Processing Toolbox
  - Parallel Computing Toolbox
  - Statistics and Machine Learning Toolbox
  - msconvert
  - ZMat toolbox
  techniques:
  - LC-MS
  - CE-MS
  license_tier: open
derived_from:
- doi: 10.1007/s00216-023-04715-6
  title: AriumMS
evidence_spans:
- functions (ROIpeaks, MSroiaug) developed by Romà Tauler, Eva Gorrochategui and Joaquim
  Jaumot
- MATLAB R2024a or newer
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MATLAB-based scientific computing for mass spectrometry data processing

## Summary

Execute parameter-driven computational pipelines in MATLAB R2024a to perform ROI detection, preprocessing, and augmentation on converted mass spectrometry data (mzXML/mzML). This skill integrates specialized toolboxes (signal processing, image processing, statistics) with domain-specific functions to transform raw MS signals into augmented feature matrices.

## When to use

You have mass spectrometry data in mzXML or mzML format and need to systematically extract regions of interest (ROIs) from multi-dimensional m/z-intensity-time arrays, normalize feature values, and augment datasets for untargeted metabolomics workflows. Use this skill when manual peak picking is infeasible and parameter-driven automation of the full preprocessing chain is required.

## When NOT to use

- Input is already a pre-processed feature table or peak list — skip ROI detection and preprocessing stages.
- Data is in incompatible format (e.g., raw vendor binary, NetCDF) without prior conversion via msconvert.
- MATLAB R2024a or required toolboxes are not available; consider open-source alternatives (e.g., R xcms, Python pymzml-based workflows).

## Inputs

- Mass spectrometry data in mzXML or mzML format (converted from raw instrument output)
- Configuration parameters (ROI search thresholds, preprocessing settings, augmentation rules)
- Single or multiple datasets for batch processing

## Outputs

- Augmented feature matrix (samples × detected features) with normalized intensities
- ROI metadata (m/z values, retention times, feature identifiers)
- Processing logs and quality control metrics

## How to apply

Load converted MS data (mzXML/mzML) into MATLAB R2024a with required toolboxes installed (Bioinformatic, Statistics and Machine Learning, Wavelet, Image Processing, Signal Processing, Parallel Computing). Configure ROI search parameters (e.g., intensity thresholds, m/z tolerance windows) and pass the raw data through the sequential three-stage pipeline: (1) apply ROIpeaks function to detect and localize regions of interest in the mass-intensity-retention-time space; (2) execute data preprocessing on identified ROIs to normalize intensities and remove noise artifacts; (3) apply MSroiaug function with augmentation parameters to expand the feature set across multiple datasets. Export the resulting augmented feature matrix and processing metadata. The rationale is that parameter-driven sequential execution ensures reproducibility, enables batch processing of multiple experiments, and preserves the interpretability of preprocessing stages.

## Related tools

- **ROIpeaks** (Core function for region-of-interest detection in multi-dimensional MS data; identifies m/z-retention-time clusters above noise threshold)
- **MSroiaug** (Data augmentation function that expands and replicates preprocessed ROI features across multiple datasets to increase training signal)
- **MATLAB R2024a** (Host computing environment providing numerical array operations, parallel processing, and graphical output)
- **Bioinformatic Toolbox** (Provides MS-specific I/O routines and sequence/mass analysis utilities)
- **Signal Processing Toolbox** (Enables filtering, wavelet decomposition, and noise reduction on MS intensity profiles)
- **Image Processing Toolbox** (Supports 2D/3D imaging operations for m/z-retention-time heatmaps and morphological ROI refinement)
- **Wavelet Toolbox** (Provides multi-scale decomposition for baseline removal and feature extraction from noisy MS spectra)
- **Statistics and Machine Learning Toolbox** (Enables statistical normalization, dimensionality reduction, and quality assessment of augmented features)
- **Parallel Computing Toolbox** (Accelerates batch processing of multiple datasets using multi-core parallelization)
- **msconvert** (Pre-processing tool for converting vendor-specific raw MS files to standardized mzXML or mzML interchange formats) — http://proteowizard.sourceforge.net/download.html
- **ZMat toolbox** (Optional data compression/decompression utility for efficient storage and transmission of large MS feature matrices) — http://github.com/fangq/zmat

## Evaluation signals

- Output feature matrix dimensions match expected sample count × detected ROI count; no NaN or infinite values.
- Preprocessing stage successfully normalizes ROI intensities to unit range or z-score; verify by sampling intensity statistics before/after.
- MSroiaug augmentation increases feature count without introducing duplicates; cross-check augmented feature IDs for uniqueness.
- Processing metadata logs contain timestamps, parameter values, and stage-completion flags for each dataset; log file size > 0 and contains expected keywords.
- Exported files (feature matrix, ROI table, metadata) conform to expected schema (e.g., comma-separated or tab-delimited text); load and verify row/column counts match pipeline input specification.

## Limitations

- Requires MATLAB R2024a (or newer) and all seven listed toolboxes; licensing cost and availability may restrict adoption in resource-limited settings.
- Performance on very large datasets (>1 GB m/z-intensity arrays) depends on available RAM and parallel computing setup; out-of-core processing not explicitly documented.
- ROIpeaks and MSroiaug function behavior is parameter-dependent and may require empirical tuning for new instrument types or ionization modes (CE-MS vs. LC-MS); no adaptive parameter selection mechanism described.
- Data must be pre-converted to mzXML/mzML via msconvert; incompatible with raw vendor formats (e.g., .raw, .d folders) without external conversion step.
- AriumMS repository carries no documented changelog or version history, limiting reproducibility across releases; community support or bug-fix turnaround unclear.

## Evidence

- [other] AriumMS implements a three-stage pipeline where user-set parameters drive sequential execution of ROI search, data preprocessing, and data augmentation stages.: "Set parameters are then used to perform ROI search, data preprocessing and data augmentation."
- [readme] The pipeline processes converted mzXML and mzML format MS data files.: "For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project"
- [readme] The core functions ROIpeaks and MSroiaug were developed by recognized chemometricians (Tauler, Gorrochategui, Jaumot).: "It uses functions (ROIpeaks, MSroiaug) developed by Romà Tauler, Eva Gorrochategui and Joaquim Jaumot"
- [readme] Seven specific MATLAB toolboxes are required to run the AriumMS application.: "Required toolboxes for the app version: Bioinformatic Toolbox, Statistics And Machine Learning Toolbox, Wavelet Toolbox, Image Processing Toolbox, Signal Processing Toolbox, Parallel Computing"
- [readme] MATLAB R2024a or newer is the required computing environment.: "MATLAB R2024a or newer"
- [readme] AriumMS is an integrated tool for untargeted metabolomics applied to multi-platform (CE-MS and LC-MS) datasets.: "All in one tool for untargeted Metabolomics by ROI and augmentation of multiple Data sets."
- [readme] The ZMat toolbox is integrated for optional data compression within the AriumMS pipeline.: "and ZMat toolbox written by Qianqian Fang http://github.com/fangq/zmat."
