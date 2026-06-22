---
name: longitudinal-data-analysis
description: Use when you have imputed metabolomics data in long format (with id, time, categorical grouping variable, metabolite names, and numeric values) and need to rank metabolites by evidence of difference across groups or time trajectories.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MeTEor
  - R
  - tidyverse
derived_from:
- doi: 10.1093/bioadv/vbae178
  title: MeTEor
- doi: 10.1007/978-3-319-47656-8_6
  title: ''
evidence_spans:
- library(MeTEor)
- 'You can perform binary classification using three different algorithms: logistic regression (LR), random forest (RF), and XGBoost (XGB).'
- library(tidyverse) library(VIM) library(laeken) library(MeTEor)
- library(tidyverse)
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

# longitudinal-data-analysis

## Summary

Apply repeated measures ANOVA and linear mixed models to imputed, long-format metabolomics datasets to identify and rank metabolites by statistical significance across time points and treatment groups. This skill enables feature selection and group comparison in longitudinal metabolomics studies.

## When to use

You have imputed metabolomics data in long format (with id, time, categorical grouping variable, metabolite names, and numeric values) and need to rank metabolites by evidence of difference across groups or time trajectories. Use this when your analysis goal is feature prioritization for downstream modeling, not exploratory visualization or unsupervised clustering.

## When NOT to use

- Input data is already in wide format (metabolites as columns) — convert to long format first.
- Missing data has not been imputed — apply imputation before fitting ANOVA models.
- Analysis goal is unsupervised exploration (e.g., dimensionality reduction, clustering) rather than hypothesis-driven feature ranking.
- Data contains extreme outliers or severe violations of normality that have not been addressed; consider transformation or robust alternatives.

## Inputs

- Imputed metabolomics dataset in long format with columns: subject id, time point, grouping variable (categorical), metabolite name, and numeric metabolite value
- Metabolite feature list (names)
- Design specification: random effect (subject), fixed effect (grouping variable)

## Outputs

- Ranked feature table (CSV) with columns: metabolite name, F-statistic, p-value, rank
- ANOVA model objects (one per metabolite) with parameter estimates and test statistics

## How to apply

Load the imputed long-format metabolomics dataset and fit a repeated measures ANOVA model for each metabolite, specifying the grouping variable as the fixed effect and subject id as the random effect. Extract the F-statistic and p-value from each ANOVA output. Rank all metabolites by p-value (ascending) or F-statistic (descending) to prioritize those with the strongest statistical evidence of group difference. Export the ranked feature table as CSV with columns: metabolite name, F-statistic, p-value, and rank. The rationale is that repeated measures ANOVA accounts for within-subject correlation over time while testing between-group effects, making it appropriate for longitudinal designs where multiple measurements per subject are correlated.

## Related tools

- **MeTEor** (R Shiny application for fitting repeated measures ANOVA, linear mixed models, and mixed ANOVA to longitudinal metabolomics data; provides interface for model fitting, visualization, and feature ranking) — https://github.com/scibiome/meteor
- **R** (Statistical computing environment; base language for ANOVA model fitting and data manipulation)
- **tidyverse** (Data wrangling and transformation to prepare long-format dataset, filter results, and export ranked tables)

## Evaluation signals

- Ranked feature table has no missing F-statistics or p-values; all metabolites in input list appear in output with valid numeric ranks.
- P-values are monotonically non-decreasing when sorted ascending; ranks are sequential integers from 1 to number of metabolites.
- F-statistics are positive and statistically consistent with reported p-values (high F → low p-value).
- ANOVA model diagnostics (residual normality, homogeneity of variance) are documented for top-ranked metabolites; at least one plot or test should be shown.
- Comparison with alternative methods (e.g., linear mixed model) yields similar rank ordering for top features, indicating robustness.

## Limitations

- Repeated measures ANOVA assumes sphericity (homogeneity of variance of differences between time points); violations may require Mauchly test correction or use of linear mixed models as alternative.
- Method assumes data are approximately normally distributed within groups after imputation; severe non-normality may require transformation or non-parametric alternatives (e.g., Friedman test).
- Missing data mechanism must be missing completely at random (MCAR) or missing at random (MAR) for imputation to be valid; imputation under missing not at random (MNAR) may bias p-values and ranks.
- P-value ranking does not account for multiple comparison correction across metabolites; consider Bonferroni, FDR, or q-value adjustment for confirmatory settings.
- No changelog found for MeTEor version history; reproducibility depends on recording exact version, function parameters, and imputation method used.

## Evidence

- [other] Repeated measures ANOVA operates on imputed metabolomics data to identify and rank metabolites by their statistical significance, enabling prioritization of features for downstream statistical analysis.: "Repeated measures ANOVA operates on imputed metabolomics data to identify and rank metabolites by their statistical significance, enabling prioritization of features for downstream statistical"
- [other] For each metabolite, fit a repeated measures ANOVA model with the grouping variable as the fixed effect and id as the random effect (subject).: "For each metabolite, fit a repeated measures ANOVA model with the grouping variable as the fixed effect and id as the random effect (subject)."
- [other] Load the imputed long-format metabolomics dataset (with id, time, categorical grouping variable, metabolite names, and numeric values).: "Load the imputed long-format metabolomics dataset (with id, time, categorical grouping variable, metabolite names, and numeric values)."
- [readme] Statistical models: Linear Mixed Models, Repeated Measures ANOVA, Mixed ANOVA, Friedman test: "Statistical models: Linear Mixed Models, Repeated Measures ANOVA, Mixed ANOVA, Friedman test"
- [other] The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor.: "The dataset contains missing values, which need to be addressed before conducting analysis in MeTEor."
- [other] The data format is being transformed from wide to long format to make it compatible with MeTEor.: "The data format is being transformed from wide to long format to make it compatible with MeTEor."
