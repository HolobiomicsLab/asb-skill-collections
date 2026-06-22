---
name: principal-component-analysis-interpretation
description: Use when when you have normalized MS1 ion intensity features from multiple samples and need to assess overall data quality, detect systematic batch effects or instrumental drift, or identify which samples deviate significantly from the cohort norm in an omics-agnostic manner (metabolomics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - IonToolPack
  - PeakQC
  - Mirador
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00146
  all_source_dois:
  - 10.1021/jasms.4c00146
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# principal-component-analysis-interpretation

## Summary

Interpret PCA results on MS1 mass spectrometry data to identify global quality issues and outlier samples through examination of principal component loadings, sample scores, and statistical distance metrics. This skill enables rapid detection of cohort-wide acquisition or processing problems and sample-specific anomalies.

## When to use

When you have normalized MS1 ion intensity features from multiple samples and need to assess overall data quality, detect systematic batch effects or instrumental drift, or identify which samples deviate significantly from the cohort norm in an omics-agnostic manner (metabolomics, lipidomics, proteomics).

## When NOT to use

- Input is already a processed feature table or abundance matrix that has undergone dimensionality reduction or feature selection, reducing the interpretability of PCA loadings as indicators of raw data quality.
- Analysis goal is to identify ion-specific biomarkers or discriminate between predefined sample classes; use supervised methods (PLS-DA, random forest) instead.
- Samples are few (< 10) relative to the number of ions, making PCA score distributions unstable and statistical distance thresholds unreliable.

## Inputs

- Raw MS1 mass spectrometry data files (Agilent .d, Thermo .raw, Bruker .d, mzML)
- Normalized MS1 ion intensity feature matrix (samples × ions)
- Optionally: user-specified ion targets or auto-tracked ion list

## Outputs

- PCA loadings matrix (ions × principal components)
- PCA sample scores (samples × principal components)
- Outlier sample flags and statistical distance values
- Per-ion quality metrics (intensity, SNR, retention time stability) for outlier samples
- Quality control report with sample rankings and anomaly annotations

## How to apply

Extract ion intensity features from MS1 spectra across all samples to build a normalized feature matrix. Apply PCA to compute principal components and sample scores, visualizing the variance structure. Examine PCA loadings to identify which ions drive variance and whether loadings suggest systematic issues (e.g., instrument drift, batch effect). Calculate statistical distances (Mahalanobis or Euclidean) from each sample to the cohort center in PCA score space. Flag samples exceeding a distance threshold (e.g., 3 standard deviations or a percentile cutoff) as quality outliers. Cross-reference outlier samples with per-ion metrics (intensity distribution, signal-to-noise, retention time stability) to diagnose whether anomalies are global or ion-specific. Generate a quality report ranking samples and flagging problematic ions in outliers.

## Related tools

- **PeakQC** (Automated quality control pipeline that implements PCA analysis on MS1 data for global and per-ion assessment, outlier detection, and comprehensive metrics extraction.) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Software suite providing graphical interface to load raw MS data from multiple instrument formats and execute PeakQC pipeline with visualization and report generation.) — https://github.com/pnnl/IonToolPack
- **Mirador** (Component of IonToolPack for raw MS data visualization (XIC, XIM heatmaps, MS/MS plots) to visually confirm quality anomalies flagged by PCA interpretation.) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- PCA loadings should show clear separation or clustering of ions if a dominant quality issue exists; diffuse loadings suggest no systematic problem.
- Outlier samples should have statistical distances (Mahalanobis/Euclidean) in PCA score space that exceed the chosen threshold (e.g., 3σ from cohort center) and form a distinct tail in a distance distribution histogram.
- Per-ion metrics (intensity, SNR, retention time stability) of outlier samples should exhibit anomalous values (e.g., low SNR, high RT drift) that explain their PCA score deviation, validating the PCA interpretation.
- Sample rankings from the quality report should correlate with known instrument maintenance events, batch boundaries, or acquisition date/time if such metadata are available.
- Removal or reprocessing of flagged outlier samples should yield a new PCA model with tighter clustering and reduced variance explained by early principal components, indicating improved cohort homogeneity.

## Limitations

- PCA assumes linear relationships among ions; non-linear quality issues (e.g., ion-specific detector saturation) may not be captured.
- Outlier thresholds (distance percentile or standard deviation cutoff) are arbitrary and may require tuning for different instrument platforms, acquisition methods, or sample matrices.
- PCA is unsupervised and cannot distinguish between biological variance and technical quality issues without additional metadata (instrument ID, acquisition date, sample type); users must interpret loadings and outliers in experimental context.
- Per-ion metrics extraction is required to diagnose the root cause of PCA outliers; PCA scores alone indicate a problem exists but not what or where.

## Evidence

- [other] PeakQC implements a two-level quality control approach: global quality assessment via PCA analysis on MS1 data, followed by detailed per-ion assessment involving comprehensive metrics extraction and outlier detection: "PeakQC implements a two-level quality control approach: global quality assessment via PCA analysis on MS1 data, followed by detailed per-ion assessment involving comprehensive metrics extraction and"
- [other] Extract ion intensity features from MS1 spectra across all samples to build a feature matrix; apply PCA to the normalized MS1 feature matrix to compute principal components and sample scores for global quality assessment: "Extract ion intensity features from MS1 spectra across all samples to build a feature matrix. Apply PCA to the normalized MS1 feature matrix to compute principal components and sample scores for"
- [other] Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the sample cohort; identify outlier samples on the PCA score space using statistical distance thresholding (e.g., Mahalanobis or Euclidean distance from the cohort center): "Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the sample cohort. Identify outlier samples on the PCA score space using statistical distance"
- [other] Generate a comprehensive quality control report containing PCA loadings, sample scores, per-ion metrics, outlier flags, and sample quality rankings: "Generate a comprehensive quality control report containing PCA loadings, sample scores, per-ion metrics, outlier flags, and sample quality rankings."
- [readme] IonToolPack reads data from multiple instrument formats and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
- [readme] PeakQC: Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection: "PeakQC: Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection for either"
