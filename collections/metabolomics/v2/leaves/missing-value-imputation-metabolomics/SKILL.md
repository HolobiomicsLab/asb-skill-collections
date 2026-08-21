---
name: missing-value-imputation-metabolomics
description: Use when your raw metabolomics dataset contains missing values (NAs)
  in metabolite columns after loading and you have already identified and removed
  metabolite columns with >10% missing data prevalence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - VIM
  - R
  - MeTEor
  - tidyverse
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioadv/vbae178
  title: MeTEor
- doi: 10.1007/978-3-319-47656-8_6
  title: ''
evidence_spans:
- library(VIM)
- library(tidyverse) library(VIM) library(laeken) library(MeTEor)
- library(MeTEor)
- 'You can perform binary classification using three different algorithms: logistic
  regression (LR), random forest (RF), and XGBoost (XGB).'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_meteor_cq
    doi: 10.1093/bioadv/vbae178
    title: MeTEor
  dedup_kept_from: coll_meteor_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbae178
  all_source_dois:
  - 10.1093/bioadv/vbae178
  - 10.1007/978-3-319-47656-8_6
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# missing-value-imputation-metabolomics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply k-nearest neighbor (KNN) imputation to fill missing metabolite values in preprocessed metabolomics datasets after removing sparse columns. This skill bridges data cleaning and statistical readiness by using weighted mean aggregation across nearest neighbors to preserve metabolite relationships while maintaining data integrity for downstream analysis.

## When to use

Your raw metabolomics dataset contains missing values (NAs) in metabolite columns after loading and you have already identified and removed metabolite columns with >10% missing data prevalence. Use this skill when missing values remain in the retained metabolite columns and you need to fill them before statistical analysis (e.g., linear mixed models, PCA, or correlation networks in MeTEor).

## When NOT to use

- Metabolite columns with >10% missing data have not yet been removed; filter sparsely populated columns first.
- All metabolite columns are already complete (0% missing data); imputation is unnecessary.
- Missing values are in metadata or phenotype columns rather than metabolite measurements; use alternative imputation strategies (e.g., mode, forward-fill for time series).

## Inputs

- raw metabolomics dataset (long or wide format, numeric metabolite columns with missing values)
- metabolite column list (after filtering for >10% NA prevalence)
- sample metadata or sample×metabolite matrix

## Outputs

- imputed metabolomics dataset (all NAs in retained metabolite columns filled)
- imputation map or report (optional: which values were imputed and by which neighbors)

## How to apply

First, load the raw metabolomics data (e.g., raw_example_data from MeTEor) and verify that metabolite columns are numeric type. Second, filter out any metabolite column with >10% NA prevalence using column-wise NA checks to avoid imputing from sparse features. Third, apply the VIM package's kNN function with weightedMean aggregation (weightDist=TRUE) to the remaining missing values in metabolite columns; this uses distance-weighted averaging across k nearest neighbors to estimate missing values based on metabolite profiles of similar samples. Finally, verify that all remaining NAs in metabolite columns have been filled and that the numeric type is preserved. The rationale is that KNN imputation preserves the multivariate structure of metabolite co-variation better than mean or median imputation, and distance weighting prioritizes the most similar samples.

## Related tools

- **VIM** (Provides the kNN function with weighted mean aggregation (weightDist=TRUE) for nearest-neighbor imputation of missing metabolite values)
- **MeTEor** (R Shiny application for longitudinal metabolomics analysis; expects preprocessed, imputed metabolomics data as input; implements downstream statistical models (LMM, ANOVA, PCA, correlation networks) on imputed data) — https://github.com/scibiome/meteor
- **R** (Programming environment for loading data, calling VIM functions, and executing preprocessing workflow)
- **tidyverse** (R package suite for data manipulation and filtering (e.g., identifying and removing sparse columns))

## Examples

```
library(VIM); library(MeTEor); data(raw_example_data); imputed_data <- kNN(raw_example_data[, metabolite_cols], k=5, imp_var=FALSE, weightDist=TRUE)
```

## Evaluation signals

- All NAs in retained metabolite columns are replaced with numeric values; no NaN or NA remains in the final metabolite matrix.
- Imputed values fall within the numeric range of observed metabolite values (no negative values if metabolites are abundance measurements, or appropriate range bounds for log-transformed data).
- Row-wise (sample) and column-wise (metabolite) distributions of imputed data are visually and statistically similar to the original complete-case subsets before imputation.
- Downstream statistical models (LMM, PCA, correlation networks in MeTEor) run without errors and produce stable coefficients/loadings; high variance inflation or instability suggests imputation failed.
- Imputation rate (fraction of values filled) is documented and is consistent with the pre-filtering step (i.e., <10% missing per column after filtering).

## Limitations

- KNN imputation assumes missing values are missing at random (MAR); if missingness is systematic or associated with unmeasured confounders, estimates may be biased.
- The choice of k (number of nearest neighbors) is not specified in the article; default k may not be optimal for all metabolomics datasets (small k risks overfitting local structure; large k risks oversmoothing).
- Pre-filtering columns with >10% missingness may remove rare or treatment-specific metabolites; this trade-off between data completeness and feature retention is not discussed in the article.
- Imputation is applied before normalization; order of operations (imputation vs. normalization) can affect downstream statistical inference but is not validated in the provided context.

## Evidence

- [other] Apply k-nearest neighbor imputation using VIM's kNN function with weighted mean aggregation (weightedMean, weightDist=TRUE) to remaining missing values in metabolite columns.: "Apply k-nearest neighbor imputation using VIM's kNN function with weighted mean aggregation (weightedMean, weightDist=TRUE) to remaining missing values in metabolite columns."
- [other] Remove columns with more than 10% NA prevalence before imputation.: "Remove columns with more than 10% NA"
- [other] The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor.: "The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor."
- [other] For the analysis in MeTEor, it is important that metabolite values are variables of the numeric type.: "For the analysis in MeTEor, it is important that metabolite values are variables of the "numeric" type."
- [readme] MeTEor is an R Shiny application that offers the possibility to explore longitudinal metabolomics data.: "MeTEor is an R Shiny application that offers the possibility to explore longitudinal metabolomics data."
