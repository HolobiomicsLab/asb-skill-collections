---
name: distribution-shape-adaptation-in-normalization
description: Use when after imputation and correction, when metabolomic feature intensities exhibit heteroscedastic variance or non-normal distributions across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R ≥4.1.2
  - R
  - OUKS (Omics Untargeted Key Script)
derived_from:
- doi: 10.1021/acs.jproteome.1c00392
  title: Omics Untargeted Key Script
evidence_spans:
- '[![](https://img.shields.io/badge/R≥4.1.2-5fb9ed.svg?style=flat&logo=r&logoColor=white?)](https://cran.r-project.org/index.html)'
- R based open-source collection of scripts called :red_circle:*OUKS*
- R ≥4.1.2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_omics_untargeted_key_script_cq
    doi: 10.1021/acs.jproteome.1c00392
    title: Omics Untargeted Key Script
  dedup_kept_from: coll_omics_untargeted_key_script_cq
schema_version: 0.2.0
---

# Adaptive Box-Cox Transformation Normalization

## Summary

Applies Adaptive Box-Cox Transformation to normalize feature-intensity tables by independently estimating and applying a shape parameter (λ) to each metabolite feature, enabling variance-stabilization and distribution reshaping without requiring a priori knowledge of feature distributions.

## When to use

After imputation and correction, when metabolomic feature intensities exhibit heteroscedastic variance or non-normal distributions across samples. Apply this skill when raw intensities show sample-dependent variance inflation or when features span multiple orders of magnitude, particularly before statistical testing that assumes normality (e.g., t-tests, ANOVA).

## When NOT to use

- Input feature-intensity table already normalized by another method (e.g., quantile normalization, log-transformation, median normalization).
- Features contain negative intensities or zero values without prior pseudocount addition; Box-Cox requires strictly positive data.
- Downstream analysis explicitly assumes log-normality or already accounts for non-normal distributions (e.g., robust regression, rank-based tests).

## Inputs

- feature-intensity table (rows=samples, columns=metabolite features, numeric intensities)
- raw LC-MS untargeted metabolomic data post-imputation and post-correction

## Outputs

- normalized feature-intensity table with Box-Cox-transformed intensities
- λ parameter estimates per feature (for reproducibility and diagnostics)

## How to apply

Load the feature-intensity table (rows = samples, columns = metabolite features, values = raw intensities) into R. For each feature column independently, estimate the optimal Box-Cox λ parameter from its empirical distribution using maximum-likelihood or profile-likelihood estimation. Apply the Box-Cox transformation y_transformed = (y^λ - 1) / λ (or log(y) when λ ≈ 0) to all intensity values for that feature. Output the normalized feature-intensity table with transformed values replacing raw intensities. The adaptation to each feature's individual distribution shape is the key: avoid applying a single global λ across all features, as heterogeneous feature behaviors (e.g., right-skewed vs. left-skewed) require feature-specific parameters.

## Related tools

- **R ≥4.1.2** (runtime environment for implementing Box-Cox transformation estimation and feature-wise transformation application) — https://cran.r-project.org/index.html
- **OUKS (Omics Untargeted Key Script)** (integrated workflow package; step 7 (Normalization.R) implements Adaptive Box-Cox Transformation) — https://github.com/plyush1993/OUKS

## Examples

```
source('7. Normalization.R'); normalized_data <- apply(feature_intensity_table, 2, function(x) { lambda <- estimate_boxcox_lambda(x); if (abs(lambda) < 0.001) log(x) else ((x^lambda - 1) / lambda) })
```

## Evaluation signals

- Each transformed feature exhibits reduced or stabilized variance across samples compared to raw intensities (quantified via Levene's test or Breusch-Pagan test for homoscedasticity).
- Transformed feature distributions approach normality (assessed via Shapiro-Wilk test, Q-Q plots, or histogram visualization per feature).
- λ parameters show feature-specific variation (not converging to a single value); features with right-skew have λ < 1, left-skew have λ > 1, near-normal have λ ≈ 1.
- Downstream statistical tests (t-test, ANOVA) on normalized features meet normality and homoscedasticity assumptions better than on raw intensities.
- Reproducibility: λ parameters remain stable when re-estimating from the same feature-intensity table.

## Limitations

- Box-Cox requires strictly positive intensities; features with zeros or negative values must be handled via pseudocount (e.g., add small positive constant or 1/2 minimum non-zero value) before transformation.
- λ estimation is data-driven and may be unstable for features with sparse data, extreme outliers, or small sample sizes; outlier detection or robust estimation methods are recommended prior to or concurrent with λ fitting.
- The skill addresses variance heterogeneity and distributional shape but does not account for batch effects, run-order drift, or biological confounding; these must be corrected in earlier steps (step 4: Correction.R).
- Interpretation of transformed intensities becomes less intuitive (units no longer represent raw abundance); reverse transformation (back-transformation) is required for reporting biological effect sizes in original scale.
- The article and README provide no explicit guidance on parameter selection, sensitivity analysis, or tuning of the Box-Cox fitting algorithm (e.g., choice of optimization routine, convergence criteria, boundary handling).

## Evidence

- [other] OUKS step 7 implements Adaptive Box-Cox Transformation normalization to normalize feature-intensity tables.: "OUKS step 7 implements Adaptive Box-Cox Transformation normalization to normalize feature-intensity tables."
- [other] Load the feature-intensity table (rows: samples, columns: metabolite features, values: raw intensities) into R. Apply the Adaptive Box-Cox Transformation to each feature column independently, estimating the Box-Cox λ parameter from the data distribution.: "Load the feature-intensity table (rows: samples, columns: metabolite features, values: raw intensities) into R. 2. Apply the Adaptive Box-Cox Transformation to each feature column independently,"
- [readme] '7. Normalization': Adaptive Box-Cox Transformation normalization was implemented.: "'7. Normalization': Adaptive Box-Cox Transformation normalization was implemented."
- [other] Output the normalized feature-intensity table with transformed values replacing raw intensities.: "Output the normalized feature-intensity table with transformed values replacing raw intensities."
- [readme] R based open-source collection of scripts called OUKS (Omics Untargeted Key Script) providing comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox: "R based open-source collection of scripts called :red_circle:*OUKS*:large_blue_circle: (*Omics Untargeted Key Script*) providing comprehensive nine step LC-MS untargeted metabolomic profiling data"
