---
name: feature-importance-ranking
description: Use when after training logistic regression, random forest, and/or XGBoost classifiers on metabolomics data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - MeTEor
  - R
derived_from:
- doi: 10.1093/bioadv/vbae178
  title: MeTEor
- doi: 10.1007/978-3-319-47656-8_6
  title: ''
evidence_spans:
- library(MeTEor)
- 'You can perform binary classification using three different algorithms: logistic regression (LR), random forest (RF), and XGBoost (XGB).'
- library(tidyverse) library(VIM) library(laeken) library(MeTEor)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-importance-ranking

## Summary

Extract and rank the most important metabolite features identified by trained classification models (logistic regression, random forest, XGBoost) to understand which metabolites drive predictions in binary classification tasks on metabolomics data. This skill reveals which compounds are most discriminative for the outcome of interest.

## When to use

After training logistic regression, random forest, and/or XGBoost classifiers on metabolomics data (e.g., covid_data) under cross-validation, when you need to identify which metabolites contribute most strongly to model predictions and may be biologically relevant biomarkers for the classification outcome.

## When NOT to use

- Models have not yet been trained or cross-validation is incomplete—importance cannot be reliably extracted from untrained or in-progress models.
- Input is univariate metabolite screening results (e.g., t-test p-values) rather than multivariate classifier importance—feature ranking from statistical tests does not account for feature interactions captured by ensemble methods.
- Dataset contains fewer than ~10 metabolite features—importance rankings on extremely sparse feature spaces may be unstable and not generalizable.

## Inputs

- trained logistic regression model on metabolomics data
- trained random forest model on metabolomics data
- trained XGBoost model on metabolomics data
- model feature importance scores or coefficients

## Outputs

- ranked list of top 10 metabolite features by importance (logistic regression)
- ranked list of top 10 metabolite features by importance (random forest)
- ranked list of top 10 metabolite features by importance (XGBoost)
- cross-algorithm feature importance comparison

## How to apply

Train classification models using MeTEor's Prediction module on binary classification tasks with cross-validation (stratified 5-fold or leave-one-out). After model convergence, retrieve feature importance scores from each trained model—random forest and XGBoost provide built-in importance rankings based on split counts and gain respectively; logistic regression importance can be derived from absolute coefficients or odds ratios. Rank metabolites by their importance scores and record the top ten features (or fewer if fewer features were used in the model). Compare importance rankings across the three algorithms to identify consistently important metabolites that are likely robust biomarkers rather than algorithm artifacts.

## Related tools

- **MeTEor** (R Shiny application hosting the Prediction module; trains logistic regression, random forest, and XGBoost classifiers and exposes feature importance retrieval) — https://github.com/scibiome/meteor
- **R** (Statistical computing environment; supports MeTEor and underlying classification libraries (glm, randomForest, xgboost packages))

## Examples

```
library(MeTEor); meteor() # Launch MeTEor Shiny app → load covid_data via Configurator → navigate to Prediction module → train LR/RF/XGB models with 5-fold cross-validation → export top 10 feature importance rankings for each model
```

## Evaluation signals

- Top 10 feature lists are non-empty and contain metabolite identifiers that were present in the input feature matrix.
- Feature importance scores are numeric, non-negative, and ranked in descending order for each algorithm.
- The sum or mean of importance scores is stable across repeated cross-validation folds, indicating reproducible rankings.
- Important features identified by multiple algorithms (LR, RF, XGB) overlap meaningfully, suggesting robust biomarker signal rather than algorithm-specific artifacts.
- Top-ranked metabolites have biological plausibility (e.g., known biomarkers for the disease or outcome being classified).

## Limitations

- Feature importance rankings are model-specific and may not reflect true biological significance; high importance could reflect data artifacts, confounding, or overfitting rather than causal biomarker role.
- Logistic regression, random forest, and XGBoost rank features by different mechanisms (coefficient magnitude, split frequency, gradient-based gain), so direct numerical comparison across algorithms is not valid; only rank consensus should be interpreted.
- With very few samples or high-dimensional metabolomics data, importance scores may be unstable and not generalizable to independent cohorts.
- The README does not specify whether MeTEor returns raw or normalized importance scores, or whether feature importance is computed on training or test set—this affects interpretability.

## Evidence

- [other] retrieve and record the ten most important features identified by the models (or fewer if not all features are used): "Retrieve and record the ten most important features identified by the models (or fewer if not all features are used)."
- [readme] Prediction models: Logistic regression, Random Forest, XGBoost: "**Prediction models:** Logistic regression, Random Forest, XGBoost"
- [other] Train logistic regression (LR) model and record performance metrics and ROC curve: "Train logistic regression (LR) model and record performance metrics and ROC curve (if test set size > 0%)."
- [other] Train random forest (RF) model and record performance metrics and ROC curve: "Train random forest (RF) model and record performance metrics and ROC curve (if test set size > 0%)."
- [other] Train XGBoost (XGB) model and record performance metrics and ROC curve: "Train XGBoost (XGB) model and record performance metrics and ROC curve (if test set size > 0%)."
