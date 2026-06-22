---
name: mixed-effects-model-interpretation
description: Use when your metabolomics dataset contains hierarchical or repeated structure (e.g., multiple samples per batch, multiple compounds per internal standard group, or QC replicates measured across runs) and you need to model the relationship between a continuous outcome (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_2269
  tools:
  - R
  - GetFeatistics
  - lme4
  - AER
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)
- The **GetFeatistics** (GF) package provides several functions useful for the elaboration of metabolomics data
- linear models with mixed effects (random and fixed), using the _lmer_ function from the lme4 package
- TOBIT linear models, using the _tobit_ function of the AER package
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

# mixed-effects-model-interpretation

## Summary

Fit and interpret linear mixed-effects regression models to metabolomics concentration or feature intensity data using the lme4 package, accounting for both fixed effects (e.g., treatment, compound type) and random effects (e.g., batch, sample block) to improve model accuracy and generalizability.

## When to use

Your metabolomics dataset contains hierarchical or repeated structure (e.g., multiple samples per batch, multiple compounds per internal standard group, or QC replicates measured across runs) and you need to model the relationship between a continuous outcome (e.g., predicted concentration, peak intensity) and predictors while controlling for unobserved heterogeneity at the batch or sample level.

## When NOT to use

- Your data are already aggregated or averaged per group (no within-group replication to model).
- Sample sizes are very small (< 20 observations per random-effect level) and variance components cannot be reliably estimated.
- Outcome data are heavily censored or bounded (e.g., detection limits); use TOBIT regression (AER::tobit) instead.
- You have no natural hierarchical structure or repeated measures; ordinary linear regression (lm) is more parsimonious.

## Inputs

- Peak area or intensity table (samples × compounds matrix)
- Sample metadata table (sample type: blank/curve/qc/unknown, known concentration values)
- Compound metadata with internal standard assignments and grouping identifiers
- Long-format data frame with outcome, fixed predictors, and random-effect grouping variable

## Outputs

- Fitted lme4 model object (lmerMod)
- Fixed effects coefficients with standard errors and p-values
- Random effects variance components and intercepts by group
- Model fit statistics (AIC, BIC, log-likelihood)
- Residual diagnostics (fitted vs. residuals, Q-Q plot)
- Predictions with confidence intervals accounting for both fixed and random effects

## How to apply

Load your intensity or concentration table (samples in rows, compounds in columns) along with metadata indicating sample type, known concentrations (for calibration), and grouping variables (e.g., batch ID, internal standard assignment). Prepare a long-format data frame with outcome, fixed effects (e.g., compound, sample type, known concentration), and random intercept variables. Fit a linear mixed model using lmer() from lme4, specifying fixed effects as main terms and random effects using the (1|grouping_variable) syntax for random intercepts. Extract model coefficients (slopes, intercepts), variance components, and likelihood ratio test statistics to assess the contribution of random effects. Validate using diagnostic plots (residuals vs. fitted, Q-Q plot) and model comparison (AIC/BIC) between nested models with and without random effects.

## Related tools

- **lme4** (Fit linear mixed-effects models with random intercepts and slopes to hierarchically structured metabolomics data)
- **GetFeatistics** (Wrapper function (get_targeted_elaboration) that internally calls lmer for concentration predictions and model summary extraction from targeted metabolomics data) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Host environment for lme4 and model specification, version ≥ 4.3.1)
- **AER** (Alternative for censored regression (TOBIT models) when outcome has detection limits or censoring)

## Examples

```
library(lme4); model <- lmer(predicted_conc ~ known_conc + (1|internal_standard), data=conc_data); summary(model); anova(model, model_without_random)
```

## Evaluation signals

- Random effects variance is substantially > 0 (not negligible) and likelihood ratio test comparing nested models (with vs. without random intercept) is significant (p < 0.05), justifying the mixed-effects structure.
- Residual diagnostic plots (residuals vs. fitted, Q-Q plot) show approximately normal, homoscedastic residuals with no systematic patterns or outliers.
- Fixed effects coefficients are stable and interpretable: e.g., slope of known_concentration on predicted_concentration ≈ 1 and intercept ≈ 0 for a well-calibrated curve; p-values for fixed effects are consistent with biological expectations.
- Model comparison via AIC or BIC shows the mixed model provides better fit than ordinary linear regression or simpler random-intercept models.
- Random intercepts by group (e.g., by batch or internal standard) are approximately normally distributed around zero and exhibit reasonable variance (not dominated by a single outlier).

## Limitations

- Variance components may be poorly estimated if random-effect levels are too few (< 5–10 groups) or sample sizes within groups are very small.
- lme4 uses frequentist inference; Bayesian alternatives (e.g., brms, rstanarm) may provide more stable estimates of uncertainty and random effects when data are sparse.
- The article does not detail handling of crossed or nested random effects; application is limited to simple random-intercept structures as implemented in GetFeatistics::get_targeted_elaboration.
- No changelog was found for GetFeatistics, making it unclear whether mixed-effects methodology or parameter defaults have changed across versions.

## Evidence

- [intro] linear models with mixed effects (random and fixed), using the _lmer_ function from the lme4 package: "linear models with mixed effects (random and fixed), using the _lmer_ function from the lme4 package"
- [other] get_targeted_elaboration returns a list containing: results_concentrations (calculated concentrations), results_accuracy (accuracy % for curve and QC points), cv_internal_standards (relative standard deviation of internal standard intensities), compound_legend (input metadata), summary_regression_models (slope, intercept, R² values), and regression_models (fitted linear regression models).: "get_targeted_elaboration returns a list containing: results_concentrations (calculated concentrations), results_accuracy (accuracy % for curve and QC points), cv_internal_standards (relative standard"
- [other] Call the get_targeted_elaboration function with these three data frames as inputs. 3. Extract and organize the resulting list containing concentrations (predicted and actual values), accuracy metrics (e.g., R-squared, mean absolute error), and regression model summaries (coefficients, statistics): "Call the get_targeted_elaboration function with these three data frames as inputs. 3. Extract and organize the resulting list containing concentrations (predicted and actual values), accuracy metrics"
- [intro] advanced statistics such as multiple regression linear models with mixed effects: "advanced statistics such as multiple regression linear models with mixed effects"
- [readme] All the figures of this package are created as ggplot object, so they can be furhter modified following the ggplot2 sintax: "All the figures of this package are created as ggplot object, so they can be furhter modified following the ggplot2 sintax"
