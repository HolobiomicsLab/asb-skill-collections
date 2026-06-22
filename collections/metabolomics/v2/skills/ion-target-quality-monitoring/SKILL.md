---
name: ion-target-quality-monitoring
description: 'Use when you have MS1 data from multiple samples and need to assess whether particular ion targets (e.g., internal standards, biomarkers, or metabolites of interest) maintain consistent quality across the cohort. Trigger on: (1) suspicion of sample-to-sample variability in ion signal;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3520
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

# ion-target-quality-monitoring

## Summary

Monitor the quality and anomalous behavior of user-specified or auto-tracked ion targets across a sample cohort by extracting per-ion metrics (intensity distribution, signal-to-noise, retention time stability) and flagging outliers in global quality space. This skill detects instrumental drift, sample degradation, or data acquisition failures affecting specific ions of interest.

## When to use

Apply this skill when you have MS1 data from multiple samples and need to assess whether particular ion targets (e.g., internal standards, biomarkers, or metabolites of interest) maintain consistent quality across the cohort. Trigger on: (1) suspicion of sample-to-sample variability in ion signal; (2) need to correlate per-ion anomalies with global quality outliers identified by PCA; (3) requirement to flag which ions drive sample QC failures.

## When NOT to use

- Input data is already aggregated into a feature table (e.g., normalized peak areas per ion per sample); use this skill on raw or minimally processed MS1 spectra.
- Only global quality assessment is required and per-ion diagnosis is not needed; use PCA-based global quality control alone.
- Ion targets are unknown or undefined; use automated ion discovery or feature detection workflows before applying this skill.

## Inputs

- MS1 mass spectrometry data in Agilent .d, Thermo .raw, Bruker .d, or mzML format from multiple samples
- Ion intensity feature matrix extracted from MS1 spectra across all samples
- PCA sample scores and Mahalanobis or Euclidean distances from cohort center (from global quality assessment step)
- User-specified ion target list (m/z values and optional retention time ranges) OR auto-tracked ion set from previous acquisition

## Outputs

- Per-ion metrics table: intensity distribution, signal-to-noise ratios, retention time stability for each tracked ion
- Outlier flags: ions with anomalous behavior in outlier samples (binary or severity score per ion–sample pair)
- Per-ion quality rankings within each sample cohort
- Quality control report containing per-ion metrics, outlier flags, and cross-reference to global PCA outlier samples

## How to apply

After loading MS1 data from multiple instrument formats (Agilent .d, Thermo .raw, Bruker .d, mzML) via IonToolPack, extract intensity features to build a feature matrix and apply PCA for global quality assessment. In parallel, calculate per-ion metrics—including intensity distribution statistics, signal-to-noise ratios, and retention time stability—across all samples in the cohort. Identify outlier samples using statistical distance thresholding (e.g., Mahalanobis or Euclidean distance from the cohort center in PCA score space). For each user-specified ion target or auto-tracked ion, cross-reference its per-ion metrics against the outlier sample set: flag ions exhibiting anomalous behavior (e.g., intensity collapse, SNR degradation, or retention time drift) in samples marked as global outliers. The rationale is that per-ion anomalies localize quality problems, enabling diagnosis of whether failures are instrument-wide or analyte-specific.

## Related tools

- **PeakQC** (Automated quality control pipeline that performs PCA analysis on MS1 data, calculates per-ion metrics (intensity distribution, signal-to-noise, retention time stability), and flags outlier samples; core engine for this skill) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Software suite that loads MS1 data from multiple instrument formats and hosts the PeakQC tool; provides unified interface and omics-agnostic functionality) — https://github.com/pnnl/IonToolPack
- **Mirador** (Raw MS data visualization and export; allows manual inspection of extracted ion chromatograms (XIC) to validate per-ion quality flags) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- Per-ion metrics table is non-empty and contains valid numerical values for all tracked ions across all samples (intensity, SNR, retention time)
- Outlier flags are consistent: ions flagged as anomalous in a given sample also appear in the global PCA outlier sample set (verified by cross-reference)
- Retention time stability is within expected tolerance (e.g., <±2 min drift for LC-MS); outliers exceed this threshold
- Signal-to-noise ratios for non-outlier samples cluster near the median SNR; outliers show SNR degradation (e.g., >2 standard deviations below mean)
- Quality report can be exported as CSV or PDF and includes per-ion metrics, outlier flags, sample quality rankings, and PCA loadings for reproducibility

## Limitations

- Requires multiple samples in the cohort to establish statistical distance thresholds; performance degrades with <5–10 samples
- Per-ion metrics are sensitive to peak detection parameters (m/z tolerance, retention time window); misconfiguration may produce spurious outliers
- Auto-tracked ions depend on consistent peak detection across samples; missing or misaligned peaks in outlier samples may yield uninformative metrics
- Retention time stability assessment assumes consistent chromatographic conditions; instrumental temperature drift or column aging may confound the signal
- No changelog available for PeakQC; version stability and metric definitions across releases are not documented

## Evidence

- [other] Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the sample cohort: "Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the sample cohort."
- [other] Flag user-specified or auto-tracked ion targets that exhibit anomalous behavior in outlier samples: "Flag user-specified or auto-tracked ion targets that exhibit anomalous behavior in outlier samples."
- [other] Identify outlier samples on the PCA score space using statistical distance thresholding (e.g., Mahalanobis or Euclidean distance from the cohort center): "Identify outlier samples on the PCA score space using statistical distance thresholding (e.g., Mahalanobis or Euclidean distance from the cohort center)."
- [readme] PeakQC: Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection for either user specified ion targets or auto-tracked ions: "PeakQC: Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection for either"
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities: "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
