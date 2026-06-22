---
name: p-value-and-confidence-interval-interpretation
description: Use when after running gentab_lm_long with mode='lm' to obtain a results table for multiple metabolomic features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0625
  tools:
  - R
  - GetFeatistics
  - lme4
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

# p-value-and-confidence-interval-interpretation

## Summary

Interpretation of statistical significance and effect precision in metabolomics regression models by reading beta coefficients, 95% confidence intervals, p-values, and FDR-corrected p-values from the gentab_lm_long output table. This skill enables assessment of both the magnitude and certainty of metabolite-variable associations.

## When to use

After running gentab_lm_long with mode='lm' to obtain a results table for multiple metabolomic features. Use this skill when you need to determine which independent variables show statistically significant associations with dependent metabolomic variables, interpret the direction and size of those associations, and distinguish between raw p-values and multiple-testing-corrected thresholds to control false discovery rate in high-dimensional metabolomics screening.

## When NOT to use

- Results from univariate tests (t-tests, ANOVA) without multiple testing correction — use FDR methods first.
- Raw p-values in high-dimensional screening without FDR adjustment — metabolomics requires correction for multiple comparisons.
- Confidence intervals that include zero with statistically significant raw p-value — likely a multiple-testing artifact; verify FDR-corrected p-value.

## Inputs

- Long-format results table from gentab_lm_long(mode='lm')
- Table columns: dependent variable name, independent variable name, beta coefficient, 95% CI lower bound, 95% CI upper bound, standard error, p-value, FDR-corrected p-value, negative log-transformed p-value, R-squared or variation percentage

## Outputs

- Interpreted list of statistically significant associations (FDR-corrected p < threshold)
- Annotated results table with significance flags and effect size categories
- Summary of beta coefficients, CI bounds, and inference for each feature-variable pair

## How to apply

Extract from the gentab_lm_long results table the beta slope (direction and magnitude of association), 95% confidence interval bounds (lower and upper), raw p-value, and FDR-corrected p-value for each dependent-independent variable pair. For significance thresholds: use FDR-corrected p-value (not raw p-value) to account for multiple hypothesis testing across many metabolomic features; common cutoffs are FDR-adjusted p < 0.05 or < 0.10 depending on stringency. Assess precision by examining the width of the 95% CI: narrow intervals indicate precise estimates; wide intervals indicate uncertainty. For direction and effect size, interpret the sign and magnitude of the beta coefficient in context of the standardized effect size reported. The negative log-transformed p-value (also in output) can be used for visualization (Manhattan plots). Rationale: in high-dimensional metabolomics, raw p-values inflate Type I error; FDR correction is essential. CI width reflects sample size and residual variance; narrow CI + small p-value + large |beta| indicates robust association.

## Related tools

- **GetFeatistics** (Generates long-format regression results table with beta, CI, p-values, and FDR-corrected p-values via gentab_lm_long(mode='lm')) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Execution environment for gentab_lm_long and results interpretation scripts (version ≥ 4.3.1 required))
- **lme4** (Underlying package for linear models that gentab_lm_long wraps; used for lm() function computation)
- **ggplot2** (Visualization of p-values and confidence intervals (e.g., forest plots, Manhattan plots for negative log p-values))

## Examples

```
# After running gentab_lm_long with mode='lm' to produce results_table
results <- gentab_lm_long(data=long_data, formula=metabolite ~ age + sex + bmi, mode='lm')
# Interpret: filter(results, FDR_p < 0.05) to identify significant associations; examine beta, CI_lower, CI_upper for effect size and precision.
```

## Evaluation signals

- Verify that FDR-corrected p-values are used for threshold decisions, not raw p-values; raw p < 0.05 should not be interpreted without checking FDR-adjusted p.
- Check that confidence intervals either exclude zero (consistent with p < 0.05) or include zero (consistent with p ≥ 0.05); mismatches indicate calculation or reporting error.
- Confirm that the magnitude of beta coefficient is consistent with the metabolite biology and study design (e.g., direction of association matches hypothesis).
- Validate that negative log-transformed p-value is correctly computed as -log10(p-value); used for Manhattan plot visualization thresholds.
- Ensure results table includes all required columns: beta, SE, 95% CI bounds, p-value, FDR-corrected p-value, and R² or variation percentage for each dependent-independent pair.

## Limitations

- Results depend critically on correct data preparation (long format, no missing values incorrectly coded, appropriate scaling/normalization). Garbage in, garbage out.
- FDR correction assumes independence or positive correlation among tests; if metabolomic features are highly correlated, correction may be conservative.
- Confidence intervals assume normality of residuals; violation (e.g., highly skewed metabolite intensities) may invalidate CI coverage.
- Multiple regression is sensitive to multicollinearity among independent variables; high correlation inflates SE and widens CI without changing p-value in predictable ways.
- No explicit mention in the article of how gentab_lm_long handles ties, outliers, or unbalanced designs; practitioners should check source code or documentation.

## Evidence

- [other] beta slopes, 95% confidence intervals, standard errors, adjusted R-squared, p-values, FDR-corrected p-values, negative log-transformed p-values, and variation percentages for each dependent-independent variable pair: "The gentab_lm_long function with mode='lm' produces a long-format results table containing beta slopes, 95% confidence intervals, standard errors, adjusted R-squared, p-values, FDR-corrected"
- [other] formula structure for multiple regression in lm mode: "Call gentab_lm_long from the GetFeatistics package with the specified formula (e.g., dependent_variable ~ fixed_effect_1 + fixed_effect_2) and configure output options for confidence intervals and"
- [other] results extraction requirements: "Extract the results table containing beta coefficients, 95% confidence interval bounds, p-values, FDR-adjusted p-values, and variation percentage (R² or similar metric)."
- [readme] advanced statistics capabilities of the package: "Getting streamlined elaboration of targeted and non-targeted metabolomics data, including elaboration of feature tables, separate QC processing, advanced statistics such as multiple regression linear"
- [readme] linear model computation via lm function: "linear models (with fixed effects), using the _lm_ function"
