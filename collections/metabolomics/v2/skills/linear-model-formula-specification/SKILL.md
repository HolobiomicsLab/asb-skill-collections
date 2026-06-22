---
name: linear-model-formula-specification
description: Use when when you have metabolomic feature intensities (dependent variables) and want to quantify how independent variables (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3957
  tools:
  - R
  - GetFeatistics
  - lme4
  - AER
  - ggplot2
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
---

# linear-model-formula-specification

## Summary

Specify and configure linear regression model formulas in R to quantify associations between independent variables (fixed effects) and dependent metabolomic variables, producing standardized effect sizes with statistical significance and confidence intervals. This skill bridges study design to computational implementation in the GetFeatistics package.

## When to use

When you have metabolomic feature intensities (dependent variables) and want to quantify how independent variables (e.g., treatment groups, continuous covariates, study factors) associate with each feature, expressed as standardized effect sizes (beta slopes), 95% confidence intervals, p-values, and FDR-corrected p-values. Use this skill when your research question requires not just group differences but regression coefficients with uncertainty estimates and significance testing.

## When NOT to use

- Input is already a results table with pre-computed coefficients and p-values; formula specification is a design step, not a post-hoc reporting step.
- You have only a wide-format table (samples in rows, features in columns) without metadata columns for independent variables; convert to long format first.
- Your dependent variable is categorical (binary or multi-class outcome); use logistic or multinomial regression models instead, which require different formula syntax and link functions.

## Inputs

- Long-format data frame with one row per observation
- Column for dependent variable (metabolomic feature intensity or normalized value)
- Columns for all fixed effect independent variables (categorical or continuous)
- Columns for random grouping factors (if mixed effects model)
- R formula string in standard R syntax (e.g., 'metabolite ~ treatment + age')

## Outputs

- Results table (CSV/TSV) with one row per dependent-independent variable pair
- Beta slope coefficients (standardized effect sizes)
- 95% confidence interval lower and upper bounds
- Standard errors
- Unadjusted p-values
- FDR-corrected p-values
- Negative log-transformed p-values
- Adjusted R-squared or variation percentage per feature
- ggplot2 objects for visualization (if generated)

## How to apply

Construct a model formula in R syntax (e.g., dependent_variable ~ fixed_effect_1 + fixed_effect_2) that specifies the dependent metabolomic variable on the left side and all fixed effects on the right side separated by '+' operators. For linear models (lm mode in gentab_lm_long), include all independent variables as additive terms; for mixed effects models (lmer mode), append random effect terms (e.g., + (1|grouping_factor)) for random intercepts. Pass this formula to gentab_lm_long() along with the long-format data frame where one row represents one observation and columns contain the dependent variable, all independent variables, and grouping factors. Configure output options for confidence interval calculation (typically 95%) and enable FDR correction for multiple testing across all feature-predictor pairs. The function iterates over each dependent variable and produces beta coefficients, standard errors, CI bounds, p-values, FDR-adjusted p-values, and variation percentages (R² or similar).

## Related tools

- **GetFeatistics** (Primary R package providing gentab_lm_long() function to implement linear regression formulas and produce standardized results tables with effect sizes, confidence intervals, and FDR-corrected p-values for metabolomic features.) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Computing environment for formula specification, data manipulation, and execution of linear models; requires version ≥ 4.3.1.)
- **lme4** (Provides lmer() function for mixed effects models with random intercepts and slopes; integrated into GetFeatistics for mode='lmer' specifications.)
- **AER** (Provides tobit() function for censored (TOBIT) regression models; available as an alternative model mode in GetFeatistics.)
- **ggplot2** (All figures and visualizations generated by GetFeatistics functions are ggplot objects, allowing downstream customization following ggplot2 syntax.)

## Examples

```
gentab_lm_long(data = long_metabolomics_df, formula = metabolite_intensity ~ treatment + age + sex, mode = 'lm', conf_level = 0.95, fdr_correct = TRUE)
```

## Evaluation signals

- Formula parses without syntax errors in R and correctly identifies dependent variable (left of ~) and all independent variables (right of ~, separated by +).
- Results table contains exactly one row per unique combination of dependent variable and independent variable; if N_features × N_predictors rows do not appear, formula may not have iterated over all features correctly.
- Beta coefficients, standard errors, and 95% CI bounds are internally consistent: SE values are positive, CI lower bound ≤ beta ≤ CI upper bound, and p-value reflects the magnitude and direction of the effect size.
- FDR-adjusted p-values are ≥ unadjusted p-values and monotonically ordered; verify no adjusted p-value is smaller than its corresponding unadjusted p-value.
- Adjusted R-squared or variation percentage per feature is between 0 and 1 (or 0–100% if percentage); R² increases monotonically as additional fixed effects are added (nested model comparison).

## Limitations

- Formula specification assumes additive linear relationships; interactions or polynomial terms must be explicitly specified in the formula (e.g., treatment*age or poly(age, 2)) and are not automatically tested.
- The long-format data structure requires one row per observation; wide-format feature tables (samples × compounds) must be reshaped first, increasing preprocessing burden.
- Multiple testing correction (FDR) is applied across all feature-predictor pairs; if the number of features is very large (e.g., thousands in untargeted metabolomics), FDR adjustment may be conservative and mask genuine associations.
- Mixed effects models (lmer mode) require careful specification of random intercept grouping factors; misspecified random effects can lead to convergence failures or unreliable confidence intervals.
- No automatic handling of missing data; NA values in independent variables or dependent variables must be addressed (removal or imputation) before formula execution.

## Evidence

- [other] Research question and finding from task card: "What are the associations between independent variables (fixed effects) and each dependent metabolomic variable, expressed as standardized effect sizes with statistical significance and confidence"
- [other] Formula specification method from task workflow: "Call gentab_lm_long from the GetFeatistics package with the specified formula (e.g., dependent_variable ~ fixed_effect_1 + fixed_effect_2)"
- [other] Output description from task card findings: "The gentab_lm_long function with mode='lm' produces a long-format results table containing beta slopes, 95% confidence intervals, standard errors, adjusted R-squared, p-values, FDR-corrected p-values"
- [intro] Data format requirement from enriched index: "Prepare the data in long format with one row per observation and columns for the dependent variable, independent variables, and grouping factors"
- [intro] Multiple regression model types from enriched index: "linear models (with fixed effects), using the _lm_ function...linear models with mixed effects (random and fixed), using the _lmer_ function from the lme4 package"
- [other] Output extraction instruction from task workflow: "Extract the results table containing beta coefficients, 95% confidence interval bounds, p-values, FDR-adjusted p-values, and variation percentage"
