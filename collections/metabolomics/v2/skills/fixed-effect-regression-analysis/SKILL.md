---
name: fixed-effect-regression-analysis
description: Use when you have a long-format metabolomics dataset with one row per observation and need to estimate the independent association between one or more fixed effects (e.g., exposure dose, treatment group, demographic variable) and each dependent variable (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - R
  - GetFeatistics
  - lm (base R stats)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fixed-effect-regression-analysis

## Summary

Fit univariate linear regression models with fixed effects to quantify associations between independent variables and metabolomic features, producing standardized effect sizes, confidence intervals, and statistical significance tests. This skill is essential when you need to express dose–response or covariate relationships as regression coefficients with uncertainty quantification and multiple-testing correction.

## When to use

Apply this skill when you have a long-format metabolomics dataset with one row per observation and need to estimate the independent association between one or more fixed effects (e.g., exposure dose, treatment group, demographic variable) and each dependent variable (e.g., metabolite intensity or normalized abundance), while reporting 95% confidence intervals, p-values, and FDR-corrected significance for each metabolite–covariate pair.

## When NOT to use

- Data contains non-independent observations (repeated measures within individuals, hierarchical clustering) — use mixed-effects regression with random intercepts instead via lme4::lmer()
- Dependent variable is heavily censored (many values below detection limit) — use TOBIT censored regression via AER::tobit() instead
- Input is already a feature table with samples in rows and compounds in columns but not in long format — reshape to long format first before applying this skill

## Inputs

- Long-format feature table (one row per observation, columns for dependent metabolite intensities or abundance values)
- Metadata table with fixed effect variables (numerical or categorical covariates of interest)
- Formula specification (e.g., 'metabolite_intensity ~ exposure + age + sex')
- Configuration parameters: confidence interval level (typically 0.95), FDR correction method (e.g., Benjamini–Hochberg)

## Outputs

- Long-format results table containing: beta slopes, 95% confidence interval bounds (lower, upper), standard errors, adjusted R-squared, unadjusted p-values, FDR-corrected p-values, negative log-transformed p-values, and variation percentage (R² or similar metric) for each dependent–independent variable pair
- Structured table (CSV or TSV) suitable for filtering, visualization, and reporting

## How to apply

Prepare the data in long format with one row per observation and columns for the dependent metabolomic variable, fixed effects (independent variables), and any grouping factors. Call gentab_lm_long from the GetFeatistics package with a formula specifying the regression model (e.g., dependent_variable ~ fixed_effect_1 + fixed_effect_2) and set output options to include 95% confidence intervals and FDR correction. The function fits ordinary least-squares regression for each metabolite–independent variable pair, computing beta slopes, standard errors, adjusted R-squared, unadjusted p-values, FDR-adjusted p-values, negative log-transformed p-values, and variation percentages. Extract and format the results table as CSV or TSF for downstream interpretation and visualization.

## Related tools

- **GetFeatistics** (R package providing gentab_lm_long() function to fit fixed-effects linear models and produce long-format results tables with beta coefficients, confidence intervals, and FDR-corrected p-values) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Statistical computing environment (version ≥ 4.3.1) required to run GetFeatistics and underlying lm() function) — https://www.r-project.org
- **lm (base R stats)** (Underlying ordinary least-squares regression function used internally by gentab_lm_long() to fit models and compute coefficients and p-values)
- **ggplot2** (Visualization library for creating publication-quality plots of regression results (effects, confidence intervals, volcano plots) following ggplot2 syntax) — https://ggplot2.tidyverse.org

## Examples

```
gentab_lm_long(data = metabolomics_long, formula = metabolite_intensity ~ exposure_dose + age + sex, mode = 'lm', conf_level = 0.95, fdr_method = 'BH')
```

## Evaluation signals

- Output table has one row per dependent–independent variable pair and includes non-NA beta, SE, p-value, FDR p-value, and confidence interval bounds for all valid model fits
- 95% confidence intervals do not include zero for all significant predictors (FDR p < 0.05) and include zero for all non-significant predictors
- Adjusted R-squared values are between 0 and 1 and reflect explained variance; compare unadjusted and adjusted R² to verify penalty for number of predictors
- FDR-corrected p-values are ≥ their corresponding unadjusted p-values (monotonic ordering) and pass Benjamini–Hochberg validity checks
- Negative log-transformed p-values (-log10(p)) show reasonable magnitude relative to raw p-values (e.g., p=0.05 → -log10(p)≈1.3)

## Limitations

- Assumes linear relationship between fixed effects and dependent metabolite; non-linear or polynomial associations are not captured unless explicitly specified in the formula
- Ordinary least-squares regression is sensitive to outliers and violations of homoscedasticity; inspection of residuals is recommended before reporting results
- No automatic handling of multicollinearity between fixed effects; users must check correlations and consider variable selection or regularization separately
- FDR correction assumes independence (or weak dependence) across tests; highly correlated metabolites may lead to conservative or anticonservative FDR control
- Long-format output is verbose for large numbers of metabolites and predictors; filtering and summarization are necessary for readability

## Evidence

- [other] What are the associations between independent variables (fixed effects) and each dependent metabolomic variable, expressed as standardized effect sizes with statistical significance and confidence intervals?: "What are the associations between independent variables (fixed effects) and each dependent metabolomic variable, expressed as standardized effect sizes with statistical significance and confidence"
- [other] The gentab_lm_long function with mode='lm' produces a long-format results table containing beta slopes, 95% confidence intervals, standard errors, adjusted R-squared, p-values, FDR-corrected p-values, negative log-transformed p-values, and variation percentages for each dependent-independent variable pair.: "The gentab_lm_long function with mode='lm' produces a long-format results table containing beta slopes, 95% confidence intervals, standard errors, adjusted R-squared, p-values, FDR-corrected"
- [other] Prepare the data in long format with one row per observation and columns for the dependent variable, independent variables, and grouping factors. Call gentab_lm_long from the GetFeatistics package with the specified formula (e.g., dependent_variable ~ fixed_effect_1 + fixed_effect_2) and configure output options for confidence intervals and FDR correction.: "Prepare the data in long format with one row per observation and columns for the dependent variable, independent variables, and grouping factors. Call gentab_lm_long from the GetFeatistics package"
- [intro] linear models (with fixed effects), using the _lm_ function from base R: "linear models (with fixed effects), using the _lm_ function"
- [readme] All the figures of this package are created as ggplot object, so they can be furhter modified following the ggplot2 sintax: "All the figures of this package are created as ggplot object, so they can be further modified following the ggplot2 syntax"
