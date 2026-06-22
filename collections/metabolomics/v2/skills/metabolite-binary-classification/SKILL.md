---
name: metabolite-binary-classification
description: Use when you have a preprocessed metabolomics dataset with a binary outcome variable (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_0091
  tools:
  - MeTEor
  - R
  - tidyverse
  - VIM
  - MetaboAnalyst
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-binary-classification

## Summary

Apply logistic regression, random forest, and XGBoost classifiers to binary classification tasks on preprocessed metabolomics data (e.g., covid_data), evaluating performance via cross-validation and extracting feature importance. This skill is essential when the research question requires comparing algorithmic predictive power on metabolite profiles under a specified validation scheme.

## When to use

You have a preprocessed metabolomics dataset with a binary outcome variable (e.g., case/control, disease/healthy) and need to assess which of three standard algorithms (logistic regression, random forest, XGBoost) achieves the highest classification performance, or when you need to identify the most discriminative metabolites via feature importance rankings across algorithms.

## When NOT to use

- Your outcome variable is continuous rather than binary—use regression models instead.
- Your dataset is severely imbalanced (>95:5 case:control ratio) without synthetic oversampling or class weight adjustments—address imbalance first.
- You have missing values in metabolites or outcome that have not been imputed or rows removed—preprocess via KNN imputation or listwise deletion before classification.

## Inputs

- Preprocessed metabolomics dataset with binary outcome variable (wide or long format, numeric metabolite values, no missing values or imputed via KNN)
- Categorical binary grouping variable (e.g., disease status, treatment response)
- Metabolite feature set (filtered and normalized, optionally dimensionality-reduced)

## Outputs

- Per-algorithm classification performance metrics (accuracy, precision, recall, F1, AUC, sensitivity, specificity)
- ROC curves and/or confusion matrices for each algorithm
- Ranked feature importance lists (top 10 metabolites per algorithm)
- Cross-validation fold predictions and probability scores
- Model coefficient/weight estimates for interpretation

## How to apply

Load your preprocessed metabolomics dataset (e.g., covid_data in wide or long format) into MeTEor via the Configurator module, specifying the timepoint, categorical grouping variable (binary outcome), and metabolites of interest. In the Prediction module, configure the test set size (typically 20–30%) and cross-validation scheme (stratified 5-fold or leave-one-out cross-validation is recommended for small cohorts). Train each of the three algorithms sequentially: logistic regression (LR), random forest (RF), and extreme gradient boosting (XGBoost/XGB). For each model, record performance metrics (accuracy, precision, recall, F1-score, AUC) and ROC curves (if test set size > 0%). Extract and rank the ten most important features from each model to identify overlapping discriminative metabolites. Compare performance metrics across algorithms to determine which achieves the best generalization under the chosen validation scheme.

## Related tools

- **MeTEor** (R Shiny application that implements the Prediction module for training and evaluating logistic regression, random forest, and XGBoost classifiers on metabolomics data with built-in cross-validation, performance metrics, ROC curve visualization, and feature importance extraction.) — https://github.com/scibiome/meteor
- **R** (Statistical programming language in which MeTEor is built; underlying engine for model training, cross-validation, and metric computation.)
- **tidyverse** (R package for data manipulation and preprocessing (used for data reshaping, filtering, and formatting before classification).)
- **VIM** (R package for imputation methods; used for KNN-based handling of missing values in metabolite data prior to classification.)
- **MetaboAnalyst** (Web-based tool for metabolite ID conversion and enrichment; used to map discriminative metabolites to biochemical pathways and public compound databases.) — https://www.metaboanalyst.ca

## Examples

```
library(MeTEor); data('covid_data'); meteor() # Launch MeTEor, configure dataset in Configurator with covid_data, select binary outcome and metabolite features, navigate to Prediction module, set stratified 5-fold cross-validation and 20% test split, train LR, RF, XGB sequentially, record performance metrics and top-10 feature importance lists.
```

## Evaluation signals

- ROC curves are generated and AUC is reported for each algorithm (AUC > 0.7 indicates moderate discriminative ability; check for crossing or non-monotonic curves suggesting numerical issues).
- Confusion matrices and per-class metrics (sensitivity, specificity) are computed; verify that recall and precision are not spuriously high (potential sign of class imbalance or data leakage).
- Feature importance rankings are consistent across cross-validation folds (top-ranked metabolites should appear in ≥70% of folds); high variance in feature ranks suggests instability.
- Cross-validation performance estimates (e.g., mean AUC across folds) are reported with confidence intervals or standard deviations; narrow intervals indicate reproducible performance.
- Test set performance (if held-out) is within 5–10% of cross-validation estimates; large gaps suggest overfitting.

## Limitations

- Classification performance is highly dependent on data quality and preprocessing; metabolites with >10% missing values should be removed or imputed consistently before training.
- Small sample sizes (n < 50) may lead to unstable feature importance rankings; leave-one-out cross-validation is preferred for small cohorts but is computationally expensive for large datasets.
- Random forest and XGBoost can overfit on high-dimensional metabolite data; consider feature selection or regularization (e.g., recursive feature elimination) if the feature count exceeds sample count.
- Binary classification assumes two discrete classes; multicategorical outcomes require different approaches (e.g., multinomial logistic regression or one-vs-rest).
- Feature importance from tree-based models (RF, XGBoost) is biased toward high-cardinality features; permutation importance or SHAP values may provide alternative perspectives.

## Evidence

- [other] MeTEor implements three classification algorithms—logistic regression (LR), random forest (RF), and extreme gradient boosting (XGB)—for binary classification tasks on metabolomics data such as covid_data, with performance evaluated under cross-validation conditions.: "MeTEor implements three classification algorithms—logistic regression (LR), random forest (RF), and extreme gradient boosting (XGB)—for binary classification tasks on metabolomics data such as"
- [other] Train logistic regression (LR) model and record performance metrics and ROC curve (if test set size > 0%). Train random forest (RF) model and record performance metrics and ROC curve (if test set size > 0%). Train XGBoost (XGB) model and record performance metrics and ROC curve (if test set size > 0%).: "Train logistic regression (LR) model and record performance metrics and ROC curve (if test set size > 0%). Train random forest (RF) model and record performance metrics and ROC curve (if test set"
- [other] Access the Prediction module and select test set size and cross-validation type (stratified 5-fold cross-validation or leave-one-out cross-validation).: "Access the Prediction module and select test set size and cross-validation type (stratified 5-fold cross-validation or leave-one-out cross-validation)."
- [other] Retrieve and record the ten most important features identified by the models (or fewer if not all features are used).: "Retrieve and record the ten most important features identified by the models (or fewer if not all features are used)."
- [readme] **Prediction models:** Logistic regression, Random Forest, XGBoost: "**Prediction models:** Logistic regression, Random Forest, XGBoost"
