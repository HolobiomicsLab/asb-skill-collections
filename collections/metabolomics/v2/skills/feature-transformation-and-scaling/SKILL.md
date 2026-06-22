---
name: feature-transformation-and-scaling
description: 'Use when after imputation and QC sample correction when: (1) your peak intensity data show heteroscedastic variance (e.g., variance increases with mean intensity); (2) you aim to improve normality of feature distributions for parametric statistical tests;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - NOREVA
  - impute
  - statTarget
  - limma
  - pcaMethods
  - vsn
  - NormalizeMets
derived_from:
- doi: 10.1038/s41596-021-00636-9
  title: NOREVA
evidence_spans:
- '[![R >3.5](https://img.shields.io/badge/R-%3E3.5-success.svg)](https://www.r-project.org/)'
- devtools::install_github("idrblab/NOREVA")
- BiocManager::install("impute")
- BiocManager::install("statTarget")
- BiocManager::install("limma")
- BiocManager::install("pcaMethods")
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_noreva_cq
    doi: 10.1038/s41596-021-00636-9
    title: NOREVA
  dedup_kept_from: coll_noreva_cq
schema_version: 0.2.0
---

# feature-transformation-and-scaling

## Summary

Apply mathematical transformations (log, square root, Box-Cox) and scaling/normalization to metabolomic peak intensity distributions to stabilize variance, improve normality, and correct for systematic biases across samples. This is a critical preprocessing step in NOREVA that standardizes feature magnitudes before downstream biomarker discovery or differential profiling.

## When to use

Apply this skill after imputation and QC sample correction when: (1) your peak intensity data show heteroscedastic variance (e.g., variance increases with mean intensity); (2) you aim to improve normality of feature distributions for parametric statistical tests; (3) you are preparing data for biomarker discovery or differential abundance profiling where unscaled intensities would inflate the contribution of high-abundance metabolites; or (4) you need to correct for systematic differences in total ion intensity or metabolite abundance across samples.

## When NOT to use

- Input is already log-transformed or from a platform (e.g., RNA-seq counts) where transformation is not appropriate without specialized offset parameters.
- Your study assumes all metabolites are equally important and you have already applied global scaling methods that are incompatible with per-metabolite transformation.
- Data contains zero or negative intensities that cannot be transformed (e.g., log of zero is undefined); handle with imputation first.

## Inputs

- Prepared peak intensity matrix (ExpressionSet or data frame) with rows as metabolites and columns as samples
- Optional metadata indicating sample groups or QC status
- Transformation method code (integer: 1, 2, or 3)
- Normalization method code (integer: 1–20)

## Outputs

- Transformed and scaled peak table (CSV or ExpressionSet object)
- Log of applied transformation and normalization parameters
- Optionally, diagnostic plots (e.g., Q-Q plots, distribution histograms before/after)

## How to apply

Within the NOREVA normulticlassmatrix workflow, specify a transformation method code (1–3) after QC correction and before normalization. Transformation code 1 typically applies log2 transformation; code 2 applies square-root transformation; code 3 applies Box-Cox transformation. The choice depends on your data's deviation from normality and heteroscedasticity patterns. Log transformation is suitable for skewed distributions with wide dynamic ranges; square-root is gentler for moderately skewed data; Box-Cox automatically selects the optimal exponent. After transformation, apply a normalization method (codes 1–20) to scale features: metabolite-based normalization (e.g., divide by sum of each metabolite across samples), sample-based normalization (e.g., divide by total ion intensity per sample), or combined approaches. The rationale is that transformation reduces skewness and stabilizes variance, while normalization corrects for sample-level variation in total analyte abundance, jointly improving signal-to-noise and reducing confounding batch effects.

## Related tools

- **NOREVA** (Orchestrates transformation and normalization via normulticlassmatrix function with method codes) — https://github.com/idrblab/NOREVA
- **vsn** (Variance stabilization and normalization for omics data)
- **limma** (Linear models for microarrays; used for transformation and normalization workflows)
- **NormalizeMets** (Metabolite-specific normalization methods) — https://github.com/metabolomicstats/NormalizeMets

## Examples

```
# In R, after loading NOREVA and preparing input files:
result <- normulticlassmatrix(fileName="prepared_data.txt", datatype=2, imputation=1, QC.correction=2, transformation=1, normalization=5)
```

## Evaluation signals

- Distribution of transformed feature intensities approaches normality (verified by Q-Q plot or Shapiro-Wilk test on a random subset of metabolites).
- Variance is stabilized: log(variance) does not strongly correlate with log(mean) intensity post-transformation.
- Total ion intensity (or chosen scaling metric) is equalized across samples after normalization (coefficient of variation < 15% across samples for a given metabolite).
- Processed peak table contains no NaN, Inf, or negative values for log-transformed data; all values are finite and within expected biological ranges.
- Comparison of within-group vs. between-group variance using PCA or hierarchical clustering shows improved separation of biological groups with reduced technical noise.

## Limitations

- Log transformation is undefined for zero or negative intensities; missing values must be imputed first using NOREVA's imputation step (code 1–4).
- Box-Cox transformation requires iterative parameter estimation and may fail or produce unexpected results if the data contain extreme outliers; robust pre-filtering is recommended.
- Over-transformation (e.g., applying both log and additional scaling) can artificially amplify noise in low-intensity metabolites; verify assumptions before stacking methods.
- The choice of transformation code is heuristic and depends on study assumptions (alpha, beta, gamma); NOREVA scans all combinations, but the optimal method varies by dataset and downstream analysis goal.

## Evidence

- [other] The normulticlassmatrix function accepts a datatype parameter (1, 2, or 3 for datasets without QCSs/ISs, with QCSs, or with ISs respectively), a prepared fileName, optional IS column identifiers, and processing method codes for imputation (1–4), QC sample correction (1–3), transformation (1–3), and normalization (1–20 for metabolite-based, sample-based, or combined approaches), then outputs a single processed peak table.: "processing method codes for imputation (1–4), QC sample correction (1–3), transformation (1–3), and normalization (1–20 for metabolite-based, sample-based, or combined approaches)"
- [other] Select and apply the chosen preprocessing workflow sequence (impute missing values if specified, apply QC signal normalization if specified, apply transformation if specified, apply normalization if specified) using NOREVA's normulticlassmatrix function with the corresponding workflow code.: "apply transformation if specified, apply normalization if specified) using NOREVA's normulticlassmatrix function"
- [readme] The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing workflows.: "enables the pre-processing and assessment of multi-class/time-series metabolomic data"
