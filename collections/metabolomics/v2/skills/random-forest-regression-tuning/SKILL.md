---
name: random-forest-regression-tuning
description: Use when your MetaboSet object contains missing values (marked as NA) in the expression matrix after quality flagging, but you need complete data for multivariate analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - notame
  - R
  - missForest
  - doParallel
  - Biobase
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- The implementation we use (from the missForest package) can be parallelized
- Load the libraries (doParallel is used for parallel processing)
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package by Bioconductor'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_notame_cq
    doi: 10.3390/metabo10040135
    title: notame
  dedup_kept_from: coll_notame_cq
schema_version: 0.2.0
---

# Random Forest Regression Tuning

## Summary

Configure and apply random forest regression to impute missing values in LC-MS metabolomics data, using observed features and samples as predictors to generate missing abundance estimates. This skill tunes the random forest algorithm via reproducibility seeds and feature quality filtering to balance imputation accuracy with computational efficiency.

## When to use

Your MetaboSet object contains missing values (marked as NA) in the expression matrix after quality flagging, but you need complete data for multivariate analysis. Random forest imputation is appropriate when features are of sufficient quality and you have adequate sample size to learn feature co-abundance patterns; use this when simple imputation strategies (mean/median) are insufficient.

## When NOT to use

- Expression matrix contains no missing values (imputation is unnecessary).
- Data is already fully imputed or has undergone simple imputation; applying random forest twice risks over-smoothing.
- Sample size is very small (<10 samples) relative to feature count, reducing the reliability of learned co-abundance patterns.

## Inputs

- MetaboSet object with NA-marked missing values in exprs matrix
- Feature quality flags (from flag_quality or flag_detection steps)
- Random seed value for reproducibility

## Outputs

- MetaboSet object with complete (imputed) expression matrix
- Imputed abundance values replacing all NA entries

## How to apply

Set a random seed for reproducibility, then apply impute_rf() in two passes: first on non-flagged (high-quality) features to learn the imputation model from reliable features, then with all_features=TRUE to impute any remaining flagged features. The random forest regressor learns feature-feature and sample-sample relationships from observed values to predict missing entries. Parallelization via doParallel can accelerate this step. Key decision: filter low-quality features before the first pass, as they introduce noise into the imputation model; flagged features are imputed only after the model is trained on good features.

## Related tools

- **notame** (wrapper package that implements impute_rf() for random forest imputation within the MetaboSet workflow) — https://github.com/hanhineva-lab/notame
- **missForest** (core random forest imputation implementation, supports mixed-type data and parallel processing)
- **doParallel** (parallelization backend for accelerating random forest imputation across CPU cores)
- **Biobase** (provides ExpressionSet class on which MetaboSet is built, stores expression matrix and feature/sample metadata)

## Examples

```
set.seed(123); metaboset_imputed <- impute_rf(metaboset, all_features=FALSE); metaboset_imputed <- impute_rf(metaboset_imputed, all_features=TRUE)
```

## Evaluation signals

- All NA values in the exprs matrix are replaced with numeric values; no NAs remain after impute_rf() with all_features=TRUE.
- Imputed values fall within biologically plausible ranges (e.g., similar magnitude to observed values for that feature across samples).
- Reproducibility check: re-running impute_rf() with the same seed produces identical imputed values.
- Feature correlation structure pre- and post-imputation should be preserved; random forest imputation respects observed co-abundance relationships.
- Downstream multivariate models (PCA, PLS-DA) should not show artificial clustering or artefacts introduced by imputation.

## Limitations

- Random forest imputation assumes missing-at-random (MAR) mechanism; if missingness is not random (e.g., systematic dropout below detection limit), imputation may introduce bias.
- With large numbers of flagged (low-quality) features, the first pass on high-quality features alone may not capture all relevant predictive relationships, reducing accuracy of downstream imputation.
- Computational cost scales with feature count and sample size; very large datasets may require significant parallelization overhead.
- The choice of seed affects the random forest's initialization; while results are reproducible, different seeds can produce slightly different imputations due to bootstrap variability.

## Evidence

- [other] Apply impute_rf() on good-quality (non-flagged) features to predict missing values via random forest regression using observed features and samples as predictors.: "Apply impute_rf() on good-quality (non-flagged) features to predict missing values via random forest regression using observed features and samples as predictors."
- [other] Apply impute_rf() again with all_features=TRUE to impute any flagged features, ensuring complete data matrix for multivariate analysis.: "Apply impute_rf() again with all_features=TRUE to impute any flagged features, ensuring complete data matrix for multivariate analysis."
- [other] Set a seed number for reproducibility.: "Set a seed number for reproducibility."
- [other] The implementation we use (from the missForest package) can be parallelized: "The implementation we use (from the missForest package) can be parallelized"
- [readme] Imputing missing values, multiple strategies available. Random forest imputation recommended: "Imputing missing values, multiple strategies available. Random forest imputation recommended"
