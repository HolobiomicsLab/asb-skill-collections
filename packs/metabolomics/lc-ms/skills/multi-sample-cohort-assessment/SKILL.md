---
name: multi-sample-cohort-assessment
description: Use when when you have MS1 mass spectrometry data from multiple samples (a cohort) acquired across an instrument run or batch, and you need to identify which samples deviate from cohort norms or which ion targets show anomalous behavior.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - IonToolPack
  - PeakQC
  techniques:
  - LC-MS
  - direct-infusion-MS
  - ion-mobility-MS
  - tandem-MS
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

# multi-sample-cohort-assessment

## Summary

A two-level quality control approach for mass spectrometry cohorts that combines PCA-based global quality assessment on MS1 data with per-ion metrics extraction and outlier detection. Use this skill to identify both systematic quality issues across sample batches and ion-specific anomalies in individual samples.

## When to use

When you have MS1 mass spectrometry data from multiple samples (a cohort) acquired across an instrument run or batch, and you need to identify which samples deviate from cohort norms or which ion targets show anomalous behavior. Apply this skill before quantitation or comparative analysis to flag samples requiring re-acquisition, re-processing, or exclusion.

## When NOT to use

- Single-sample analysis: PCA and cohort-level statistical thresholding require multiple samples to establish norm and variance.
- Already-processed feature tables or pre-filtered peak lists: the skill operates on raw ion intensity data; if input is already quantitated or de-noised, outlier detection sensitivity may be compromised.
- Real-time or streaming acquisition: the method requires complete cohort assembly before PCA; use only after all samples in a batch have been acquired.

## Inputs

- Raw MS data files (Agilent .d, Thermo .raw, Bruker .d, mzML) from multiple samples
- Ion targets (user-specified or auto-tracked) for per-ion assessment
- MS acquisition metadata (LC-MS, LC-IMS-MS, DDA, DIA, direct infusion)

## Outputs

- PCA score matrix and loadings for global quality assessment
- Per-ion metrics table (intensity distribution, signal-to-noise, retention time stability)
- Outlier sample flags and statistical distance scores
- Per-ion anomaly flags for outlier samples
- Comprehensive quality control report (PDF, CSV) with sample quality rankings

## How to apply

Load raw MS data from multiple samples in supported formats (Agilent .d, Thermo .raw, Bruker .d, mzML) using IonToolPack. Extract ion intensity features across all samples to build a feature matrix, then normalize and apply PCA to compute principal components and sample scores for global assessment. Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the cohort. Identify outlier samples by computing statistical distance (Mahalanobis or Euclidean) from the cohort center in PCA score space; apply a distance threshold to flag outliers. For user-specified or auto-tracked ion targets, flag anomalous per-ion behavior in outlier samples (e.g., extreme intensity, unstable retention time). Generate a comprehensive report with PCA loadings, sample scores, per-ion metrics, outlier flags, and quality rankings to enable informed sample triage.

## Related tools

- **IonToolPack** (Container software suite that implements the full multi-sample cohort assessment workflow via the PeakQC tool and handles multi-format raw MS data import.) — https://github.com/pnnl/IonToolPack
- **PeakQC** (Core tool within IonToolPack that executes automated PCA-based global quality control, per-ion metrics extraction, outlier detection, and report generation.) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- PCA score plot shows expected sample clustering with outliers separated by > 2–3 standard deviations in principal component space.
- Outlier samples identified by Mahalanobis/Euclidean distance exhibit correlated per-ion anomalies (e.g., low signal-to-noise or unstable retention time) rather than random flags.
- Per-ion metrics (intensity, SNR, RT stability) show expected distributions for non-outlier samples and clear deviation in flagged outliers.
- Quality control report ranks samples and flags are reproducible when the same cohort is re-processed with identical parameters.
- Outlier samples coincide with known instrument issues, batch effects, or sample preparation problems documented in experimental metadata.

## Limitations

- PCA sensitivity depends on feature matrix coverage and normalization; sparse or highly skewed ion intensity distributions may obscure global patterns.
- Outlier detection thresholds (distance cutoffs) are statistical and require tuning; no universal threshold applies across all instrument types, acquisition modes, or sample types.
- Per-ion anomaly detection assumes ion targets are present in most cohort samples; auto-tracked ions in sparse or variable datasets may yield high false-positive flags.
- The tool is omics-agnostic but does not automatically distinguish between true analytical anomalies (e.g., instrument drift, contamination) and biological signal; expert interpretation required.

## Evidence

- [other] PeakQC implements a two-level quality control approach: global quality assessment via PCA analysis on MS1 data, followed by detailed per-ion assessment involving comprehensive metrics extraction and outlier detection for either user-specified ion targets or auto-tracked ions.: "PeakQC implements a two-level quality control approach: global quality assessment via PCA analysis on MS1 data, followed by detailed per-ion assessment involving comprehensive metrics extraction and"
- [other] Extract ion intensity features from MS1 spectra across all samples to build a feature matrix. Apply PCA to the normalized MS1 feature matrix to compute principal components and sample scores for global quality assessment. Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the sample cohort.: "Extract ion intensity features from MS1 spectra across all samples to build a feature matrix. Apply PCA to the normalized MS1 feature matrix to compute principal components and sample scores for"
- [other] Identify outlier samples on the PCA score space using statistical distance thresholding (e.g., Mahalanobis or Euclidean distance from the cohort center).: "Identify outlier samples on the PCA score space using statistical distance thresholding (e.g., Mahalanobis or Euclidean distance from the cohort center)."
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
- [readme] Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection: "Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection"
