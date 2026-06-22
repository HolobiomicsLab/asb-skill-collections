---
name: multi-algorithm-comparative-analysis
description: Use when when you have prepared metabolomics data (e.g., covid_data) with a binary outcome variable and need to select the most appropriate predictive algorithm for your classification task.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3375
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

# multi-algorithm-comparative-analysis

## Summary

Systematically train and evaluate multiple classification algorithms (logistic regression, random forest, XGBoost) on the same metabolomics dataset under identical cross-validation conditions to compare their performance metrics and identify algorithm-specific feature importance. This skill is essential for determining which algorithm best generalizes to binary classification tasks on metabolomic biomarkers.

## When to use

When you have prepared metabolomics data (e.g., covid_data) with a binary outcome variable and need to select the most appropriate predictive algorithm for your classification task. Apply this skill after data preprocessing (imputation, normalization, format conversion) and feature selection, when you want to benchmark the three algorithms implemented in MeTEor under controlled cross-validation (stratified k-fold or leave-one-out) to report comparative performance and robustness.

## When NOT to use

- Input dataset contains missing values or non-numeric metabolite columns — preprocess and impute first using KNN or other methods.
- Outcome variable is continuous (regression) rather than binary — use regression algorithm comparison instead.
- Sample size is extremely small (n < 20) — cross-validation schemes may be unreliable; consider leave-one-out cross-validation or external validation cohorts.

## Inputs

- Preprocessed metabolomics dataset in long format (rows: observations, columns: metabolite features + outcome variable)
- Binary outcome variable (categorical grouping variable)
- Metabolite feature matrix (numeric type, missing values imputed, normalized)
- Cross-validation configuration (fold count, stratification preference)

## Outputs

- Per-algorithm classification performance metrics (accuracy, sensitivity, specificity, AUC, precision, F1-score)
- ROC curves for each algorithm (if test set size > 0%)
- Feature importance rankings (top 10 features per algorithm)
- Cross-validation fold scores or holdout test set predictions
- Comparative summary table of algorithm performance

## How to apply

Load the preprocessed metabolomics dataset into MeTEor and configure it via the Configurator module, specifying the timepoint, categorical grouping variable (binary outcome), and metabolite features of interest. In the Prediction module, set the test set size and cross-validation scheme (stratified 5-fold cross-validation or leave-one-out cross-validation are options). Train logistic regression (LR), random forest (RF), and XGBoost (XGB) models sequentially, recording performance metrics (accuracy, sensitivity, specificity, AUC) and ROC curves for each. Extract the ten most important features ranked by each algorithm to assess feature selection consistency and interpretability. Compare performance across algorithms using the same evaluation metric (e.g., AUC or cross-validation fold scores) to select the model with the highest generalization capability and most reliable feature rankings.

## Related tools

- **MeTEor** (R Shiny application for training and comparing logistic regression, random forest, and XGBoost classifiers on metabolomics data with integrated cross-validation and feature importance extraction) — https://github.com/scibiome/meteor
- **R** (Statistical computing environment for executing MeTEor and underlying algorithm implementations)

## Examples

```
library(MeTEor); data(covid_data); meteor() # Configure dataset in Configurator (select binary outcome and metabolite features), then use Prediction module: select stratified 5-fold CV, train LR/RF/XGB models, compare AUC and extract top-10 features from each.
```

## Evaluation signals

- Each algorithm produces non-null performance metrics (AUC, accuracy, sensitivity, specificity) and ROC curves for the same cross-validation splits.
- Feature importance rankings are consistent across folds for the same algorithm (low variance in top-10 features across CV splits).
- Cross-validation fold scores sum correctly to the reported overall performance metric; no missing fold results.
- Algorithm ranking by AUC or primary metric is reproducible across independent runs with the same random seed.
- Feature importance lists from RF and XGB contain metabolite names matching the input feature set; LR produces coefficient magnitudes that correlate with RF/XGB importance for top features.

## Limitations

- MeTEor's prediction module does not natively support multiclass classification; this skill is restricted to binary outcomes.
- Feature importance from logistic regression (coefficient magnitude) may not be directly comparable to tree-based importances (mean decrease in impurity or gain); interpretation requires algorithm-specific context.
- Small sample sizes or highly imbalanced outcomes may produce unstable feature rankings and inflated cross-validation scores; stratified cross-validation is recommended but does not guarantee robustness with n < 50.
- XGBoost and Random Forest are computationally expensive on high-dimensional metabolomics datasets (thousands of features); feature pre-selection is advisable.

## Evidence

- [other] task_002 finding: "MeTEor implements three classification algorithms—logistic regression (LR), random forest (RF), and extreme gradient boosting (XGB)—for binary classification tasks on metabolomics data such as"
- [other] task_002 workflow steps 2–5: "Access the Prediction module and select test set size and cross-validation type (stratified 5-fold cross-validation or leave-one-out cross-validation). Train logistic regression (LR) model and record"
- [other] task_002 research question: "What are the per-algorithm classification performance scores when MeTEor's three algorithms (logistic regression, random forest, and gradient boosting) are applied to binary classification on"
- [readme] README feature list: "Prediction models: Logistic regression, Random Forest, XGBoost"
- [other] task_002 workflow step 6: "Retrieve and record the ten most important features identified by the models (or fewer if not all features are used)."
