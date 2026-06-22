---
name: data-augmentation-metabolomics
description: Use when you have preprocessed and normalized ROI feature data extracted from mzXML or mzML mass spectrometry files and seek to increase feature representation and robustness before statistical modeling or machine learning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - ROIpeaks
  - MSroiaug
  - Bioinformatic Toolbox
  - Statistics And Machine Learning Toolbox
  - Wavelet Toolbox
  - Image Processing Toolbox
  - Signal Processing Toolbox
  - MATLAB R2024a
  - ZMat toolbox
  - msconvert
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-augmentation-metabolomics

## Summary

Apply parameter-driven data augmentation to preprocessed ROI feature matrices from untargeted metabolomics MS data (CE-MS, LC-MS) to increase feature diversity and improve model robustness. This skill uses the MSroiaug function to systematically augment regions of interest after ROI detection and preprocessing, enabling more reliable untargeted metabolite discovery across multi-platform datasets.

## When to use

You have preprocessed and normalized ROI feature data extracted from mzXML or mzML mass spectrometry files and seek to increase feature representation and robustness before statistical modeling or machine learning. Augmentation is particularly valuable when working with small or imbalanced multi-platform datasets (CE-MS, LC-MS) where natural biological variation across samples is limited, or when you need to boost confidence in detected metabolic features through synthetic augmentation of ROI intensity patterns.

## When NOT to use

- Input data is already a large, balanced, multi-replicate feature table with high statistical power; augmentation adds redundancy without benefit.
- Analysis goal requires strict preservation of original feature distributions (e.g., quantitative biomarker validation, regulatory compliance, or absolute metabolite quantification).
- Preprocessing or ROI detection has not yet been applied; augmentation assumes cleaned, normalized, and localized features.

## Inputs

- Preprocessed ROI feature matrix (numerical array)
- ROI metadata and detection parameters
- Augmentation configuration parameters (e.g., scaling factors, perturbation ranges)

## Outputs

- Augmented ROI feature matrix (expanded numerical array)
- Augmentation metadata and transformation log
- Feature annotation and traceability information

## How to apply

After loading converted MS data (mzXML/mzML format) into MATLAB R2024a and applying ROIpeaks detection and preprocessing normalization, invoke the MSroiaug function with user-configured augmentation parameters to systematically expand the preprocessed ROI feature matrix. The augmentation function applies parameter-controlled transformations to ROI intensity patterns, generating synthetic variants that preserve the chemical and biological structure of detected features while introducing controlled variation. Configure augmentation parameters to control the degree and type of feature modification (e.g., intensity scaling, retention time perturbation, isotopic pattern variation). Export the augmented feature matrix alongside processing metadata for downstream statistical or machine learning analysis. The rationale is that augmented features reduce overfitting, improve generalization across batches and acquisition platforms, and increase statistical power for metabolite detection without requiring additional experimental samples.

## Related tools

- **MSroiaug** (Applies parameter-controlled augmentation transformations to preprocessed ROI feature matrices)
- **ROIpeaks** (Detects regions of interest from mass spectrometry data prior to preprocessing and augmentation)
- **MATLAB R2024a** (Execution environment for running MSroiaug and ROI processing pipeline with required toolboxes)
- **ZMat toolbox** (Provides data compression and encoding support for efficient storage of augmented feature matrices) — http://github.com/fangq/zmat
- **msconvert** (Converts raw MS data to mzXML or mzML format prior to ROI detection and augmentation pipeline) — http://proteowizard.sourceforge.net/download.html

## Evaluation signals

- Augmented feature matrix dimensions increase proportionally to augmentation parameter settings; row count (features) or column count (samples) should reflect configured augmentation multiplicity.
- Statistical distributions of augmented features (intensity, retention time, m/z) remain within biologically plausible ranges and do not introduce artificial outliers or violate physical MS constraints.
- Augmentation metadata log documents all transformation parameters and traceability links between original and augmented features; each augmented feature must be traceable to its source ROI.
- Downstream machine learning or statistical models trained on augmented features demonstrate improved generalization (e.g., cross-validation accuracy, reduced overfitting) compared to non-augmented features, measured on held-out or independent validation data.
- No systematic bias or drift in augmented feature distributions relative to original features; distribution moments (mean, variance, skewness) should remain consistent with preprocessing-normalized distributions.

## Limitations

- Augmentation parameters must be tuned empirically; aggressive augmentation may introduce artifacts that violate MS physical constraints (e.g., impossible isotopic patterns or mass calibration violations).
- Augmentation is most effective for untargeted discovery and model robustness; it is not suitable for absolute quantification, regulatory biomarker validation, or scenarios requiring strict feature traceability to raw data.
- AriumMS implementation requires MATLAB R2024a or newer and multiple licensed toolboxes (Bioinformatic, Statistics and Machine Learning, Wavelet, Image Processing, Signal Processing, Parallel Computing, Database); deployment cost and reproducibility may be limited in non-MATLAB environments.
- Augmentation assumes preprocessing and ROI detection have been performed correctly; errors in earlier pipeline stages (e.g., misaligned retention times, poor peak picking) will propagate and amplify through augmentation.

## Evidence

- [readme] Set parameters are then used to perform ROI search, data preprocessing and data augmentation.: "Set parameters are then used to perform ROI search, data preprocessing and data augmentation."
- [other] AriumMS implements a three-stage pipeline where user-set parameters drive sequential execution of ROI search, data preprocessing, and data augmentation stages. These stages use ROIpeaks and MSroiaug functions developed by Tauler, Gorrochategui, and Jaumot to process converted MS data.: "These stages use ROIpeaks and MSroiaug functions developed by Tauler, Gorrochategui, and Jaumot to process converted MS data."
- [other] Apply MSroiaug function to augment the preprocessed ROI data according to augmentation parameters.: "Apply MSroiaug function to augment the preprocessed ROI data according to augmentation parameters."
- [readme] All in one tool for untargeted Metabolomics by ROI and augmentation of multiple Data sets.: "All in one tool for untargeted Metabolomics by ROI and augmentation of multiple Data sets."
- [other] Load converted MS data (mzXML or mzML format) into MATLAB R2024a environment with required toolboxes (Bioinformatic, Statistics and Machine Learning, Wavelet, Image Processing, Signal Processing, Parallel Computing).: "Load converted MS data (mzXML or mzML format) into MATLAB R2024a environment with required toolboxes"
