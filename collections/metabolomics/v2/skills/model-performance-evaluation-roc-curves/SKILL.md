---
name: model-performance-evaluation-roc-curves
description: Use when you have a binary classification task on metabolomics data (e.g., covid_data) and need to benchmark multiple algorithms to determine which produces the highest discriminative power.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2275
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

# model-performance-evaluation-roc-curves

## Summary

Evaluate and compare binary classification model performance by training logistic regression, random forest, and XGBoost models on metabolomics data under cross-validation and recording performance metrics and ROC curves for each algorithm. This skill is essential when assessing which supervised learning approach best discriminates between two metabolic phenotypes.

## When to use

Apply this skill when you have a binary classification task on metabolomics data (e.g., covid_data) and need to benchmark multiple algorithms to determine which produces the highest discriminative power. Use it after data preprocessing, imputation, and normalization are complete, and when you have defined a categorical outcome variable (e.g., disease status, treatment response) and selected your metabolite feature set.

## When NOT to use

- Input outcome variable is not binary (use multi-class classification methods instead)
- Metabolomics data has not been imputed and normalized (preprocess first)
- Test set size is 0% and ROC curves are not required (use training metrics only if appropriate for your research question)

## Inputs

- metabolomics dataset (e.g., covid_data) in MeTEor-compatible format
- categorical grouping variable (binary outcome)
- selected metabolite features (numeric columns)
- cross-validation configuration (fold count, stratification)

## Outputs

- logistic regression performance metrics and ROC curve
- random forest performance metrics and ROC curve
- XGBoost performance metrics and ROC curve
- top ten most important features per model
- comparative performance summary across algorithms

## How to apply

Within MeTEor's Prediction module, configure the cross-validation scheme (stratified 5-fold or leave-one-out) and test set size (>0% to generate ROC curves). Train each of the three algorithms sequentially—logistic regression, random forest, and XGBoost—recording performance metrics (accuracy, AUC, sensitivity, specificity) and ROC curves for each. Retrieve and document the ten most important features identified by each model to assess feature consistency and biological plausibility. Compare performance metrics across algorithms to identify the best-performing model; models trained on the same cross-validation scheme with the same test/train split ensure fair comparison.

## Related tools

- **MeTEor** (R Shiny application implementing logistic regression, random forest, and XGBoost prediction models with cross-validation and ROC curve visualization for binary classification on metabolomics data) — https://github.com/scibiome/meteor
- **R** (Statistical computing environment in which MeTEor runs)

## Examples

```
library(MeTEor); meteor() # Launch MeTEor app → load covid_data via Configurator → navigate to Prediction module → set cross-validation to 'stratified 5-fold', test set size to 20% → train Logistic Regression, Random Forest, XGBoost sequentially → record ROC curves and feature importance
```

## Evaluation signals

- ROC curves are generated for each algorithm (when test set size > 0%); curves should show typical sigmoid shape with AUC ≥ 0.5
- Performance metrics (accuracy, AUC, sensitivity, specificity) are recorded and comparable across all three algorithms using the same cross-validation scheme
- Top ten features are retrieved and documented for each model; overlapping features across models suggest robust biomarkers
- Cross-validation folds and test/train splits are consistent across all three model trainings to ensure fair comparison
- No algorithm performance metrics are missing; if a metric cannot be computed, document the reason (e.g., single class in a fold)

## Limitations

- ROC curves require test set size > 0%; when test set size = 0%, ROC curves are not generated and only cross-validation metrics are available
- Class imbalance in the binary outcome may inflate or deflate performance metrics; stratified cross-validation mitigates this but does not eliminate the issue
- Feature importance rankings differ across algorithms (logistic regression uses coefficient magnitude, random forest and XGBoost use tree-based importance); direct comparison of importance scores across models is not recommended
- MeTEor is designed for longitudinal metabolomics data; non-temporal or cross-sectional metabolomics may not fully utilize all application features

## Evidence

- [other] Train logistic regression (LR) model and record performance metrics and ROC curve (if test set size > 0%): "Train logistic regression (LR) model and record performance metrics and ROC curve (if test set size > 0%)."
- [other] MeTEor implements three classification algorithms—logistic regression (LR), random forest (RF), and extreme gradient boosting (XGB): "MeTEor implements three classification algorithms—logistic regression (LR), random forest (RF), and extreme gradient boosting (XGB)—for binary classification tasks on metabolomics data such as"
- [other] Retrieve and record the ten most important features identified by the models (or fewer if not all features are used): "Retrieve and record the ten most important features identified by the models (or fewer if not all features are used)."
- [other] Select test set size and cross-validation type (stratified 5-fold cross-validation or leave-one-out cross-validation): "Access the Prediction module and select test set size and cross-validation type (stratified 5-fold cross-validation or leave-one-out cross-validation)."
- [readme] Prediction models: Logistic regression, Random Forest, XGBoost: "**Prediction models:** Logistic regression, Random Forest, XGBoost"
