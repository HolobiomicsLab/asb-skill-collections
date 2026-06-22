---
name: spectral-quality-metrics-extraction
description: Use when you have multi-sample MS1 data (from Agilent, Thermo, Bruker, or mzML formats) and need to quantify ion-level quality attributes—such as signal consistency, noise characteristics, or chromatographic stability—to either flag outlier samples or validate data fitness for downstream.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3664
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - IonToolPack
  - PeakQC
  - Mirador
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

# spectral-quality-metrics-extraction

## Summary

Extract comprehensive quality metrics from MS1 spectral data to characterize per-ion signal properties (intensity distribution, signal-to-noise, retention time stability) across a sample cohort. This enables detection of anomalous ion behavior and supports both global and targeted quality assessment in multi-sample mass spectrometry studies.

## When to use

Apply this skill when you have multi-sample MS1 data (from Agilent, Thermo, Bruker, or mzML formats) and need to quantify ion-level quality attributes—such as signal consistency, noise characteristics, or chromatographic stability—to either flag outlier samples or validate data fitness for downstream quantitation or statistical analysis. Use it before or alongside global QC approaches (e.g., PCA) to gain per-ion resolution of quality issues.

## When NOT to use

- Input is already a normalized feature table (ion × sample matrix); skip to outlier detection or statistical analysis.
- Only global quality assessment is required (e.g., PCA on aggregate sample scores); per-ion metrics are unnecessary.
- MS data lacks sufficient sample replication (n < 3) to estimate meaningful distribution or stability statistics.

## Inputs

- Raw MS1 mass spectrometry data files (Agilent .d, Thermo .raw, Bruker .d, mzML formats)
- Sample metadata or cohort definition (list of sample identifiers)
- Optional: user-specified ion targets (m/z list, CSV format) or auto-tracked ion list

## Outputs

- Per-ion metrics table (intensity distribution, signal-to-noise, retention time stability per ion and sample)
- Outlier flags for ion–sample pairs exhibiting anomalous behavior
- Quality control report containing per-ion metrics, outlier flags, and sample quality rankings

## How to apply

Load MS1 mass spectrometry data from multiple instrument formats using IonToolPack. Extract ion intensity features from MS1 spectra across all samples to build a normalized feature matrix. For each ion (either user-specified targets or auto-tracked features), compute per-ion metrics: intensity distribution statistics (mean, variance, range), signal-to-noise ratios across samples, and retention time stability (e.g., variance or drift). Identify ions exhibiting anomalous behavior by applying statistical thresholds (e.g., coefficient of variation outliers, signal-to-noise floor violations) or by cross-referencing with sample-level outlier flags from global QC. Report per-ion metrics alongside sample quality rankings to prioritize investigation of problematic ion–sample pairs.

## Related tools

- **IonToolPack** (Software suite that loads multi-format MS1 data and houses the PeakQC pipeline for metrics extraction and outlier detection) — https://github.com/pnnl/IonToolPack
- **PeakQC** (Automated quality control pipeline embedded in IonToolPack that implements per-ion metrics extraction and outlier detection following PCA-based global assessment) — https://github.com/pnnl/IonToolPack
- **Mirador** (Raw MS data visualization tool in IonToolPack; used to inspect extracted ion chromatograms (XIC) and validate ion signal quality before metrics extraction) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- Per-ion metrics table is complete and non-empty: every tracked ion has intensity mean, variance, SNR, and retention time stability values for all samples in the cohort.
- Outlier flags are consistent with sample-level QC results: ions flagged as anomalous in outlier samples show elevated metrics deviation (e.g., >3 standard deviations from cohort mean).
- Retention time stability metric (e.g., RT variance or drift) is bounded and reasonable for the chromatographic method (typically <1 min RT window per ion across samples).
- Signal-to-noise ratios are positive and span an interpretable range (e.g., 1–1000); samples with SNR < background threshold are marked for review.
- Quality rankings correlate with independent QC indicators (e.g., total ion current, number of detected features, or PCA distance from cohort center).

## Limitations

- Metrics extraction depends on reliable ion detection and feature alignment across samples; misalignment or missing features in some samples will inflate stability metrics and reduce outlier sensitivity.
- Signal-to-noise calculation requires noise level estimation, which may be unreliable in data with very high background or in direct infusion modes with limited baseline regions.
- Per-ion metrics are omics-agnostic but assume MS1-level data; MS/MS fragmentation spectra are not used for per-ion QC and must be evaluated separately using spectral library matching tools.
- Small sample cohorts (n < 5) may yield unstable distribution estimates and over-sensitive or under-sensitive outlier thresholds; cohort size should be documented and considered when interpreting flags.

## Evidence

- [other] Extract ion intensity features from MS1 spectra across all samples to build a feature matrix.: "Extract ion intensity features from MS1 spectra across all samples to build a feature matrix."
- [other] Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the sample cohort.: "Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the sample cohort."
- [other] Identify user-specified or auto-tracked ion targets that exhibit anomalous behavior in outlier samples.: "Flag user-specified or auto-tracked ion targets that exhibit anomalous behavior in outlier samples."
- [readme] Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection for either user specified ion targets or auto-tracked ions.: "Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection for either user"
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
