---
name: mass-spectrometry-outlier-detection
description: Use when you have multi-sample MS1 data (LC-MS, LC-IMS-MS, or direct infusion across any omics domain) and need to detect samples with abnormal global ion intensity patterns or unusual per-ion metric behavior (intensity distribution, signal-to-noise, retention time stability) that may indicate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
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

# mass-spectrometry-outlier-detection

## Summary

Identify outlier samples in MS cohorts via PCA-based statistical distance thresholding on normalized MS1 feature matrices, followed by per-ion anomaly flagging to pinpoint global and localized quality issues. This two-level approach enables both cohort-wide quality assessment and targeted investigation of specific ion behavior in suspect samples.

## When to use

Apply this skill when you have multi-sample MS1 data (LC-MS, LC-IMS-MS, or direct infusion across any omics domain) and need to detect samples with abnormal global ion intensity patterns or unusual per-ion metric behavior (intensity distribution, signal-to-noise, retention time stability) that may indicate instrumental drift, sample degradation, or acquisition failure.

## When NOT to use

- Input is already a curated feature table with outliers pre-removed or quality-filtered; re-running detection may be redundant.
- Cohort size is very small (n < 3–5 samples); PCA-based distance thresholding requires sufficient statistical power to define a meaningful cohort center.
- MS data lacks sufficient ion intensity variation across the sample set; PCA may not separate signal from noise effectively.

## Inputs

- Raw MS data files (Agilent '.d', Thermo '.raw', Bruker '.d', mzML format)
- Multi-sample MS1 mass spectrometry dataset from LC-MS, LC-IMS-MS, or direct infusion
- Optional: user-specified ion targets (m/z values) or auto-tracked ion list

## Outputs

- PCA loadings and sample scores in PCA coordinate space
- Per-ion metrics (intensity distribution, signal-to-noise ratio, retention time stability)
- Statistical distance values (Mahalanobis or Euclidean) for each sample
- Outlier sample flags and anomalous ion behavior flags
- Sample quality rankings
- Comprehensive quality control report (CSV/PDF export)

## How to apply

First, load raw MS data from supported formats (Agilent '.d', Thermo '.raw', Bruker '.d', mzML) using IonToolPack and extract ion intensity features across all samples to construct a feature matrix. Normalize the feature matrix and apply PCA to compute principal components and sample scores for global quality assessment. Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the cohort. Identify outlier samples by computing statistical distance (Mahalanobis or Euclidean distance) from the cohort center in PCA score space using distance thresholding—samples exceeding the statistical distance cutoff are flagged as outliers. For each flagged outlier sample, examine per-ion metrics for user-specified ion targets or auto-tracked ions to detect anomalous behavior. Generate a comprehensive report containing PCA loadings, sample scores, per-ion metrics, outlier flags, and sample quality rankings to support interpretation.

## Related tools

- **IonToolPack** (Umbrella software suite providing MS data I/O (multiple instrument formats), GUI wrapper, and orchestration of PeakQC outlier detection workflow) — https://github.com/pnnl/IonToolPack
- **PeakQC** (Core tool implementing PCA-based quality control, per-ion metrics extraction, and outlier detection via statistical distance thresholding) — https://github.com/pnnl/IonToolPack
- **Mirador** (Visualization and validation tool to inspect raw MS data, extracted ion chromatograms (XIC), and MS/MS mirror plots for outlier sample confirmation) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- PCA score plot shows clear separation of outlier samples from the main cohort cloud; statistical distance values for flagged samples exceed the thresholding cutoff by a visible margin.
- Per-ion metrics for outlier-flagged samples exhibit 2–3 σ deviations in intensity distribution, signal-to-noise ratio, or retention time stability compared to cohort median or inter-quartile range.
- Outlier sample quality rankings are consistent with instrument log anomalies, sample preparation issues, or known experimental perturbations (e.g., column saturation, solvent contamination).
- Replicates or technical duplicates cluster tightly in PCA space and are not flagged as outliers; biological or technical variation is captured orthogonally.
- Per-ion anomaly flags for auto-tracked ions correspond to ions known to be sensitive to the suspected failure mode (e.g., lipid or metabolite ions affected by ionization efficiency changes).

## Limitations

- PCA assumes linear relationships in the feature space; non-linear quality variations (e.g., systematic instrumental artifacts affecting only a subset of m/z or retention time ranges) may not be detected.
- Distance thresholding requires pre-specification or calibration of the statistical cutoff (Mahalanobis or Euclidean); the optimal threshold depends on cohort size and acceptable false-positive/negative rates.
- Per-ion metrics are sensitive to feature extraction parameters (m/z tolerance, retention time window, noise floor); incorrect settings may inflate or suppress anomaly detection.
- Auto-tracked ions may miss outliers affecting rare or low-abundance ions present in only a subset of samples.
- No changelog is provided in the repository, limiting awareness of algorithm changes, parameter defaults, or known issues across versions.

## Evidence

- [other] PeakQC implements a two-level quality control approach: global quality assessment via PCA analysis on MS1 data, followed by detailed per-ion assessment involving comprehensive metrics extraction and outlier detection for either user-specified ion targets or auto-tracked ions.: "PeakQC implements a two-level quality control approach: global quality assessment via PCA analysis on MS1 data, followed by detailed per-ion assessment involving comprehensive metrics extraction and"
- [other] Identify outlier samples on the PCA score space using statistical distance thresholding (e.g., Mahalanobis or Euclidean distance from the cohort center).: "Identify outlier samples on the PCA score space using statistical distance thresholding (e.g., Mahalanobis or Euclidean distance from the cohort center)."
- [other] Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the sample cohort.: "Calculate per-ion metrics (intensity distribution, signal-to-noise, retention time stability) across the sample cohort."
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.)"
- [readme] Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection: "Automated quality control pipeline by PCA analysis on MS1 data for global quality assessment, and detailed assessment with comprehensive metrics extraction and outlier detection"
- [readme] Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode, Direct infusion: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode,"
