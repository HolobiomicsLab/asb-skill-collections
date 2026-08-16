---
name: missing-value-imputation-strategy-selection
description: Use when after mark_nas() has replaced non-NA missing-value codes (e.g.,
  0, 1) with R's NA in the exprs matrix of a MetaboSet object, and you need to decide
  whether to apply random forest imputation, simple imputation strategies, or defer
  imputation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - notame
  - R
  - missForest
  - doParallel
  - Biobase
  techniques:
  - LC-MS
  license_tier: restricted
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
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package
  by Bioconductor'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo10040135
  all_source_dois:
  - 10.3390/metabo10040135
  - 10.1093/bioinformatics/btr597
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Missing-Value Imputation Strategy Selection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Select and apply an appropriate missing-value imputation strategy (random forest, simple imputation, or other methods) for LC-MS metabolomics data based on data quality, missingness patterns, and analytical requirements. This skill bridges NA marking and imputation execution by determining which algorithm best preserves feature relationships while minimizing bias.

## When to use

After mark_nas() has replaced non-NA missing-value codes (e.g., 0, 1) with R's NA in the exprs matrix of a MetaboSet object, and you need to decide whether to apply random forest imputation, simple imputation strategies, or defer imputation. Use this skill when missingness is substantial enough to affect multivariate analysis but selective enough that the choice of algorithm will materially affect downstream inference.

## When NOT to use

- Data contains no missing values (NA count = 0); imputation is unnecessary.
- Missingness is non-random and feature-dependent (e.g., consistently missing at low concentrations); neither random forest nor simple imputation will resolve MNAR bias — consider sensitivity analysis or reporting uncertainty instead.
- Downstream analysis explicitly requires handling missing data (e.g., survival analysis or mixed models); imputation may hide rather than preserve uncertainty.

## Inputs

- MetaboSet object with NA values in exprs matrix
- Flag status for low-quality or high-missingness features (from flag_detection or flag_quality)
- Metadata on missingness mechanism (MCAR vs. MNAR if available)

## Outputs

- MetaboSet object with imputed exprs matrix
- Imputation method metadata (algorithm used, parameters, random seed)

## How to apply

First, assess the extent and pattern of missingness: if features have extensive missing data (high proportion of NAs), flag them before imputation to avoid poor model training. Second, decide on algorithm: random forest imputation is recommended because it leverages observed feature and sample relationships as predictors, but simple imputation (mean, median, minimum detection limit) is appropriate for MCAR (missing completely at random) scenarios or when computational resources are limited. Third, apply impute_rf() on good-quality (non-flagged) features first to predict missing values via random forest regression. Fourth, optionally apply impute_rf() again with all_features=TRUE to impute any flagged features, ensuring a complete matrix for multivariate analysis. Set a seed number before imputation for reproducibility. The choice hinges on whether you trust feature correlations (random forest) versus assuming each feature is independent (simple imputation).

## Related tools

- **notame** (provides mark_nas(), impute_rf(), impute_simple() functions for marking and selecting imputation strategy on MetaboSet objects) — https://github.com/hanhineva-lab/notame
- **missForest** (implements parallelized random forest imputation algorithm; called by notame's impute_rf())
- **doParallel** (enables parallel processing of random forest imputation for computational efficiency)
- **Biobase** (provides ExpressionSet class on which MetaboSet is built; stores exprs matrix and feature/sample metadata)

## Examples

```
set.seed(42); imputed_metaboset <- impute_rf(metaboset_object); imputed_metaboset_full <- impute_rf(metaboset_object, all_features=TRUE)
```

## Evaluation signals

- Imputed exprs matrix has no remaining NA values and preserves original non-missing entries unchanged.
- Imputed values fall within plausible ranges (e.g., non-negative for intensity data; within observed quartiles for the feature) and do not introduce outliers.
- Random seed is documented and reproducible; re-running impute_rf() with same seed reproduces identical imputation.
- If random forest was chosen: verify that non-flagged features were used as predictors; check that flagged features (if imputed with all_features=TRUE) do not drive multivariate clustering.
- Comparison of multivariate model (e.g., PCA, PLS-DA) before and after imputation shows expected retention of biological signal and absence of artificial batch effects introduced by imputation.

## Limitations

- Random forest imputation assumes that observed features contain sufficient information to predict missing values; fails if missingness is highly feature-specific (MNAR) or if most features are also missing at the same samples.
- Simple imputation (mean, median, minimum detection limit) does not account for feature correlations and can bias covariance-based methods (PCA, PLS); appropriate only for MCAR scenarios.
- Computational cost of random forest scales with feature count and sample size; parallelization via doParallel is needed for large metabolomics matrices but may not be available in all computing environments.
- The notame package API is experimental and subject to breaking changes; impute_rf() and impute_simple() signatures or defaults may shift between versions.

## Evidence

- [other] Random forest imputation recommended: "Imputing missing values, multiple strategies available. Random forest imputation recommended"
- [other] Mark missing values before imputation: "First, mark the missing values as ```NA```. Many peak picking programs mark missing values as 0 or 1"
- [other] Two-stage imputation workflow: "Apply impute_rf() on good-quality (non-flagged) features to predict missing values via random forest regression using observed features and samples as predictors. Apply impute_rf() again with"
- [other] Random forest uses feature correlations: "The implementation we use (from the missForest package) can be parallelized"
- [other] Simple imputation as alternative: "```impute_simple``` for the simple imputation strategies"
- [other] Reproducibility via random seed: "Set a seed number for reproducibility. Apply impute_rf() on good-quality (non-flagged) features"
