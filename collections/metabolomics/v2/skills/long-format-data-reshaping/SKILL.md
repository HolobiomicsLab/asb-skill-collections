---
name: long-format-data-reshaping
description: Use when when you have a wide-format feature intensity table (samples in rows, analyzed compounds in columns) and need to conduct multiple regression linear models (lm or lmer) to estimate associations between independent variables (fixed effects) and each metabolomic feature as a dependent.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - GetFeatistics
  - R base reshape / tidyr::pivot_longer / reshape2::melt
  - GetFeatistics::gentab_lm_long
  - R (version ≥4.3.1)
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)
- The **GetFeatistics** (GF) package provides several functions useful for the elaboration of metabolomics data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# long-format-data-reshaping

## Summary

Transform metabolomics feature tables from wide format (samples × compounds) into long format (one row per observation) to enable multivariate regression analysis and statistical modeling. This reshaping is prerequisite for computing standardized effect sizes, confidence intervals, and p-values across dependent-independent variable pairs.

## When to use

When you have a wide-format feature intensity table (samples in rows, analyzed compounds in columns) and need to conduct multiple regression linear models (lm or lmer) to estimate associations between independent variables (fixed effects) and each metabolomic feature as a dependent variable. Long-format reshaping is mandatory before calling gentab_lm_long or similar regression functions that require one row per observation.

## When NOT to use

- Input data is already in long format (one row per observation)—skipping reshape avoids redundant pivoting and potential data loss.
- Your analysis goal is univariate per-feature testing (e.g., t-tests or ANOVA without modeling covariates)—wide format suffices for those workflows.
- You need to retain the original wide-format feature table for visualization (e.g., heatmaps, PCA biplots)—create a separate long copy rather than replacing it.

## Inputs

- wide-format feature intensity table (samples in rows, compounds in columns)
- metadata table with sample classifications and phenotypic variables
- optional compound legend table with internal standards and units

## Outputs

- long-format data frame (one row per feature-sample observation)
- ready-for-regression data structure with dependent and independent variable columns

## How to apply

Load the wide-format intensity table and metadata into R (≥4.3.1). Reshape the data so that each row represents a single observation with columns for: the dependent variable (one feature's intensity values), independent variables (fixed effects of interest), and grouping factors (e.g., sample type, subject ID). Use R's reshape, tidyr::pivot_longer, or melt functions to convert from wide to long format. Ensure no missing values are introduced; if present, handle them according to your analysis plan (e.g., missing_replace=TRUE in GetFeatistics). Once reshaped, pass the long-format data frame and a formula (e.g., dependent_variable ~ fixed_effect_1 + fixed_effect_2) to gentab_lm_long. This workflow enables the regression function to iterate over each feature as the dependent variable and compute beta coefficients, 95% confidence intervals, standard errors, adjusted R², p-values, FDR-corrected p-values, and variation percentages.

## Related tools

- **R base reshape / tidyr::pivot_longer / reshape2::melt** (Perform wide-to-long data reshaping prior to regression)
- **GetFeatistics::gentab_lm_long** (Accept long-format data and iterate regression models over each feature) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R (version ≥4.3.1)** (Environment for data manipulation and reshaping operations)

## Examples

```
library(GetFeatistics); long_data <- reshape2::melt(wide_feature_table, id.vars=c('sample_id'), variable.name='feature', value.name='intensity'); long_data <- merge(long_data, metadata, by='sample_id'); results <- gentab_lm_long(data=long_data, formula=intensity ~ phenotype + covariate, mode='lm')
```

## Evaluation signals

- Check that the long-format data frame has N_samples × N_features rows (one row per feature-sample combination), not N_samples rows.
- Verify that the dependent variable column contains repeated values for the same feature across different samples, and independent variable columns contain sample-level metadata that repeats for all rows of a given sample.
- Confirm that no NA values were introduced during reshaping, or that they match the original data's missing pattern (check summary(long_data)).
- Validate that passing the reshaped long data to gentab_lm_long produces output with N_features rows in the results table (one result row per dependent variable).
- Ensure that columns in the long-format data match the formula specification (e.g., dependent_variable ~ fixed_effect_1 + fixed_effect_2) without column name mismatches.

## Limitations

- Reshaping large feature tables (thousands of compounds, hundreds of samples) can consume significant memory; consider filtering features before reshaping if memory constraints exist.
- Long-format reshaping assumes balanced or semi-balanced designs; if samples have missing features, the data frame will contain NA values that must be handled appropriately in downstream regression (controlled by gentab_lm_long's missing_replace parameter).
- Reshaping discards the original wide-format structure; practitioners should retain a copy if visualization tasks (e.g., heatmaps) require wide format.

## Evidence

- [intro] data preparation step before regression: "Prepare the data in long format with one row per observation and columns for the dependent variable, independent variables, and grouping factors."
- [intro] data structure requirement for gentab_lm_long: "Call gentab_lm_long from the GetFeatistics package with the specified formula (e.g., dependent_variable ~ fixed_effect_1 + fixed_effect_2)"
- [intro] input data format specification: "The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns"
- [intro] long format output from regression: "The gentab_lm_long function with mode='lm' produces a long-format results table containing beta slopes, 95% confidence intervals, standard errors, adjusted R-squared, p-values, FDR-corrected"
