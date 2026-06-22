---
name: ms1-data-preprocessing-normalization
description: Use when when you have loaded raw MS1 data from multiple instrument formats (Agilent, Thermo, Bruker, mzML) across a multi-sample cohort and need to prepare the ion intensity feature matrix for PCA analysis or cross-sample quality assessment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - IonToolPack
  - PeakQC
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- IonToolPack is a software suite housing tools for mass spectrometry data
- IonToolPack is a software suite housing tools for mass spectrometry data.
- 'PeakQC: Automated quality control pipeline by PCA analysis on MS1 data'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakqc_cq
    doi: 10.1021/jasms.4c00146
    title: PeakQC
  dedup_kept_from: coll_peakqc_cq
schema_version: 0.2.0
---

# ms1-data-preprocessing-normalization

## Summary

Normalize MS1 mass spectrometry ion intensity features across sample cohorts to remove instrument and systematic bias before PCA-based quality control and outlier detection. This preprocessing step ensures that global quality assessment and per-ion metrics are computed on a comparable, scale-adjusted feature matrix.

## When to use

When you have loaded raw MS1 data from multiple instrument formats (Agilent, Thermo, Bruker, mzML) across a multi-sample cohort and need to prepare the ion intensity feature matrix for PCA analysis or cross-sample quality assessment. Apply this skill before computing principal components or comparing sample quality metrics, especially when instrument response, total ion current (TIC), or retention time drift may confound the cohort.

## When NOT to use

- Input is already a normalized feature table or PCA score matrix — skip to outlier detection.
- MS1 data is from a single instrument run with stable conditions — normalization may introduce noise rather than reduce bias.
- Ion features have been log-transformed and z-scored by upstream software — re-normalizing risks over-correction and rank distortion.

## Inputs

- Raw MS1 data files (Agilent .d, Thermo .raw, Bruker .d, mzML formats)
- Ion intensity feature matrix extracted from MS1 spectra across sample cohort
- Sample metadata (optional, for stratified normalization)

## Outputs

- Normalized MS1 feature matrix (centered, scaled, ready for PCA)
- Normalization parameters (mean, standard deviation, or TIC values per sample)
- Quality control report documenting normalization method and feature statistics

## How to apply

After extracting ion intensity features from MS1 spectra across all samples using IonToolPack, normalize the feature matrix to remove systematic bias and standardize feature scales. The normalization step precedes PCA computation: center and scale the feature matrix (e.g., by TIC normalization, log transformation, or z-score standardization) so that subsequent PCA loadings and sample scores reflect global quality patterns rather than instrument artifacts. Choose the normalization method based on data distribution and the nature of expected artifacts (e.g., TIC normalization for intensity drift, log transformation for heavy-tailed ion distributions). Verify that the normalized matrix has zero or near-zero mean and uniform variance across features before proceeding to PCA. This ensures that Mahalanobis or Euclidean distance thresholding for outlier detection operates on a statistically sound feature space.

## Related tools

- **IonToolPack** (Parent software suite providing MS data loading, feature extraction, and integrated PeakQC quality control pipeline) — https://github.com/pnnl/IonToolPack
- **PeakQC** (Downstream tool that applies PCA analysis on the normalized MS1 feature matrix for global quality assessment and outlier detection) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- Normalized feature matrix has mean ≈ 0 and standard deviation ≈ 1 (or other target scale) across all features.
- No single sample dominates principal component loadings due to extreme total ion current or intensity values.
- PCA variance explained by PC1 is distributed across biological or cohort structure, not driven by a single outlier sample.
- Euclidean or Mahalanobis distances computed on normalized scores are statistically comparable across the sample cohort (no feature-scale artifacts).
- Normalization method is documented in QC report with explicit transformation equations and per-sample scaling factors.

## Limitations

- Normalization choice (TIC, log, z-score, etc.) is method-dependent and not automatically optimized; choice should match ion intensity distribution and expected artifacts.
- Extreme outliers in ion intensity (e.g., single hyper-abundant ion or saturated detector response) may dominate normalization statistics; consider robust scaling or outlier trimming before normalization.
- No automatic handling of missing values or zero-intensity features; sparse MS1 data may require imputation strategy before normalization.
- Cross-instrument cohorts may require instrument-specific normalization factors or batch correction; simple global normalization may mask instrument-level drift.

## Evidence

- [other] Extract ion intensity features from MS1 spectra across all samples to build a feature matrix.: "Extract ion intensity features from MS1 spectra across all samples to build a feature matrix."
- [other] Apply PCA to the normalized MS1 feature matrix to compute principal components and sample scores for global quality assessment.: "Apply PCA to the normalized MS1 feature matrix to compute principal components and sample scores for global quality assessment."
- [readme] Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection: "Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection"
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
- [readme] Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML"
