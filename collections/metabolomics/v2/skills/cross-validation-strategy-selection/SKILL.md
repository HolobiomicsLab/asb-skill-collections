---
name: cross-validation-strategy-selection
description: Use when when preparing to train supervised binary classification models
  (logistic regression, random forest, XGBoost) on metabolomics datasets in MeTEor,
  you must first decide between stratified k-fold cross-validation (suitable for larger,
  balanced cohorts) and leave-one-out cross-validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3957
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MeTEor
  - R
  license_tier: restricted
derived_from:
- doi: 10.1093/bioadv/vbae178
  title: MeTEor
- doi: 10.1007/978-3-319-47656-8_6
  title: ''
evidence_spans:
- library(MeTEor)
- 'You can perform binary classification using three different algorithms: logistic
  regression (LR), random forest (RF), and XGBoost (XGB).'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-validation-strategy-selection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Selection and configuration of appropriate cross-validation schemes (stratified k-fold or leave-one-out) for binary classification tasks on metabolomics data in MeTEor. This skill ensures that model performance metrics and ROC curves are computed under appropriate validation conditions that match the data structure and sample size.

## When to use

When preparing to train supervised binary classification models (logistic regression, random forest, XGBoost) on metabolomics datasets in MeTEor, you must first decide between stratified k-fold cross-validation (suitable for larger, balanced cohorts) and leave-one-out cross-validation (suitable for small sample sizes or highly imbalanced classes). This decision directly affects the reliability of downstream performance metrics and feature importance estimates.

## When NOT to use

- When the dataset is already split into independent training and test cohorts collected under different conditions; in such cases, use a single held-out test set without cross-validation to avoid information leakage.
- When sample size is extremely large (n > 10,000) and computational cost of leave-one-out cross-validation is prohibitive; use stratified k-fold with k ≤ 10 instead.
- When conducting exploratory data analysis before model training; cross-validation is applied during the model-training phase, not during preprocessing or EDA.

## Inputs

- Configured metabolomics dataset (timepoint, grouping variable, metabolite features selected)
- Binary outcome variable
- Sample size and class distribution

## Outputs

- Cross-validation scheme specification (cv_type, k, test_size)
- Stratified fold assignments (if stratified k-fold selected)
- Test set indices (if test_size > 0%)

## How to apply

Within MeTEor's Prediction module, after configuring your dataset via the Configurator (selecting timepoint, categorical grouping variable, and metabolites), access the cross-validation options and specify: (1) test set size as a percentage (0% for pure cross-validation, >0% to also hold out a separate test set); (2) cross-validation type—stratified 5-fold cross-validation maintains class balance within folds and is preferred for moderately sized cohorts, whereas leave-one-out cross-validation iteratively trains on n−1 samples and tests on the held-out sample, minimizing bias but at higher computational cost for large datasets. Stratified cross-validation is recommended when class imbalance exists to ensure each fold reflects the original class distribution. The choice impacts both computational time and the stability of performance metrics (ROC curves, sensitivity, specificity) reported after model training.

## Related tools

- **MeTEor** (R Shiny application hosting the Prediction module where cross-validation strategy is selected and applied during model training) — https://github.com/scibiome/meteor
- **R** (Statistical programming language underlying MeTEor's cross-validation and model implementation)

## Examples

```
In MeTEor's Prediction module UI: set 'Cross-validation type' to 'stratified 5-fold cross-validation', 'Test set size' to '20%', then click 'Train Model' to apply the selected CV strategy before fitting logistic regression, random forest, and XGBoost.
```

## Evaluation signals

- Fold assignments are stratified: class proportions in each fold match the overall class distribution within ±5%.
- Test set size (if specified) equals the stated percentage; training set size = total_n × (1 − test_size/100).
- Cross-validation loop executes without errors; all k folds (or n iterations for LOO) produce valid performance metrics.
- ROC curves and performance metrics (sensitivity, specificity, AUC) are computed for each fold and aggregated (mean ± SD or CI reported).
- Reproducibility: setting a random seed produces identical fold assignments across runs.

## Limitations

- Stratified k-fold cross-validation assumes k ≤ min(count per class); with severe class imbalance, some folds may contain very few positive cases, leading to unstable metric estimates.
- Leave-one-out cross-validation becomes computationally prohibitive for n > 1,000; MeTEor does not explicitly document runtime bounds or adaptive fallback strategies.
- MeTEor's Prediction module does not document whether cross-validation is performed *within* hyperparameter tuning or only *after* hyperparameters are fixed; this affects optimism in reported metrics.
- The article and README do not provide guidance on choosing k for stratified k-fold (e.g., why 5 is default) or how class imbalance thresholds trigger the recommendation for leave-one-out.

## Evidence

- [other] cross-validation type (stratified 5-fold cross-validation or leave-one-out cross-validation): "Access the Prediction module and select test set size and cross-validation type (stratified 5-fold cross-validation or leave-one-out cross-validation)."
- [other] cross-validation during model training with performance metrics: "Train logistic regression (LR) model and record performance metrics and ROC curve (if test set size > 0%)."
- [readme] stratified k-fold maintains class representation: "Prediction models: Logistic regression, Random Forest, XGBoost"
