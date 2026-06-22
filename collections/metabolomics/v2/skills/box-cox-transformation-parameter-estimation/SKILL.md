---
name: box-cox-transformation-parameter-estimation
description: 'Use when you have raw LC-MS feature-intensity tables (rows: samples, columns: metabolite features, values: raw intensities) with non-normal, skewed distributions and need to normalize them prior to statistical analysis.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R ≥4.1.2
  - R
  - 'OUKS (step 7: Normalization.R)'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.1c00392
  all_source_dois:
  - 10.1021/acs.jproteome.1c00392
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Box-Cox Transformation Parameter Estimation

## Summary

Estimate the Box-Cox λ parameter from feature-intensity data distribution to enable adaptive power transformation normalization of metabolomic features. This skill is essential for handling skewed metabolite intensity distributions in LC-MS untargeted metabolomics workflows.

## When to use

Apply this skill when you have raw LC-MS feature-intensity tables (rows: samples, columns: metabolite features, values: raw intensities) with non-normal, skewed distributions and need to normalize them prior to statistical analysis. This is particularly relevant when raw metabolite intensities span multiple orders of magnitude or show evidence of heteroscedasticity across sample groups.

## When NOT to use

- Input already contains log-transformed or pre-normalized intensities — applying Box-Cox would double-normalize and distort the data.
- Feature columns contain zero or negative values — standard Box-Cox transformation requires strictly positive inputs; preprocessing (e.g., pseudocount addition) would be needed first.
- Analysis requires interpretability of raw intensity units (e.g., for absolute quantification or external method comparison) — transformed values sacrifice direct instrumental meaning.

## Inputs

- Feature-intensity table (CSV or R data frame): rows are samples, columns are metabolite features, values are raw LC-MS intensities

## Outputs

- Normalized feature-intensity table with Box-Cox transformed values replacing raw intensities
- Estimated λ parameters per feature (for QC and reproducibility documentation)

## How to apply

For each metabolite feature column independently, estimate the optimal Box-Cox λ parameter from the observed intensity distribution. The λ parameter is estimated from the data itself (not fixed a priori) to adaptively determine the strength of the power transformation needed: λ near 1 indicates minimal transformation, λ near 0 approximates a log transformation, and λ < 0 applies reciprocal-like transformations. Apply the estimated λ to transform the feature column using the Box-Cox formula, replacing raw intensities with normalized values. The adaptive approach allows different features with different skewness profiles to receive appropriate, feature-specific normalizing transformations.

## Related tools

- **R** (Execution environment for Box-Cox parameter estimation and feature transformation (≥4.1.2 required for OUKS implementation)) — https://cloud.r-project.org/
- **OUKS (step 7: Normalization.R)** (Implements Adaptive Box-Cox Transformation normalization for feature-intensity tables within the nine-step LC-MS metabolomic workflow) — https://github.com/plyush1993/OUKS

## Examples

```
# In R, using OUKS step 7; after loading feature-intensity table into object 'ft':
# source('7. Normalization.R')
# The script applies Box-Cox transformation: lambda_est <- boxcox(ft[, feature_col]); ft_normalized[, feature_col] <- (ft[, feature_col]^lambda_est - 1) / lambda_est
```

## Evaluation signals

- Post-transformation feature distributions are more symmetric (visually or by skewness metrics) compared to raw distributions; Q-Q plots should show tighter adherence to normality.
- Estimated λ parameters are reproducible across repeated runs on the same data and vary logically across features (e.g., more skewed features receive more extreme λ adjustments).
- Homogeneity of variance across sample groups is improved (e.g., Levene's test p-value increases post-transformation), confirming reduction of heteroscedasticity.
- Output normalized table has identical dimensions and row/column order as input; no samples or features are dropped or reordered.
- Transformed intensity values are finite, positive, and within expected ranges (no NaN, Inf, or negative values introduced); feature scaling is preserved such that relative differences between samples remain interpretable.

## Limitations

- Box-Cox transformation requires strictly positive intensity values; zeros or negative measurements must be handled separately (e.g., via pseudocount addition or missing value imputation) before applying this skill.
- The transformation is feature-wise independent; it does not account for inter-feature correlations or multivariate structure; subsequent statistical methods must still handle covariance appropriately.
- Estimated λ parameters are data-dependent and sample-size sensitive; small or unbalanced sample sets may yield unstable parameter estimates; external validation or regularization may be needed for reliable reproducibility.
- The skill assumes that the raw intensity distribution is the primary normalization target; it does not address batch effects, signal drift, or technical variation — those corrections should be applied before (step 4: Correction) or integrated alongside this step.
- Transformation of extreme outliers (very high or very low intensities) can magnify their influence; quality control and outlier handling in earlier steps (e.g., step 6: Filtering) should precede this skill to avoid distortion.

## Evidence

- [other] Apply the Adaptive Box-Cox Transformation to each feature column independently, estimating the Box-Cox λ parameter from the data distribution.: "Apply the Adaptive Box-Cox Transformation to each feature column independently, estimating the Box-Cox λ parameter from the data distribution."
- [other] OUKS step 7 implements Adaptive Box-Cox Transformation normalization to normalize feature-intensity tables.: "OUKS step 7 implements Adaptive Box-Cox Transformation normalization to normalize feature-intensity tables."
- [other] Load the feature-intensity table (rows: samples, columns: metabolite features, values: raw intensities) into R.: "Load the feature-intensity table (rows: samples, columns: metabolite features, values: raw intensities) into R."
- [readme] "7. Normalization": Adaptive Box-Cox Transformation normalization was implemented.: ""7. Normalization": Adaptive Box-Cox Transformation normalization was implemented."
- [readme] R based open-source collection of scripts called OUKS (Omics Untargeted Key Script) providing comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox: "R based open-source collection of scripts called OUKS (Omics Untargeted Key Script) providing comprehensive nine step LC-MS untargeted metabolomic profiling data processing toolbox"
