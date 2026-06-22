---
name: pls-pls-da-classification-modeling
description: Use when you have a preprocessed peak table (feature matrix with samples × peaks), known sample class labels or group membership, and a goal to classify or discriminate between two or more sample groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - SMART Statistical Analysis module
derived_from:
- doi: 10.1021/acs.analchem.5c03225
  title: SMART 2.0
evidence_spans:
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_smart_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03225
  all_source_dois:
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pls-pls-da-classification-modeling

## Summary

Build partial least-squares (PLS) or discriminant analysis (PLS-DA) classification models on preprocessed metabolomics peak tables to predict sample class membership and identify discriminative metabolic features. This skill is applied when the analysis goal is to distinguish between sample groups (e.g., disease vs. control) and rank features by their importance for classification.

## When to use

Apply this skill when you have a preprocessed peak table (feature matrix with samples × peaks), known sample class labels or group membership, and a goal to classify or discriminate between two or more sample groups. Use PLS-DA specifically when the number of metabolomic features greatly exceeds the number of samples, or when you need to identify which peaks are most important for distinguishing between groups.

## When NOT to use

- Input data is raw mass spectrometry data (.raw, .d, mzXML) rather than a preprocessed peak table—use data import and preprocessing modules first.
- Analysis goal is association analysis or regression with continuous covariates—use ANCOVA instead.
- Analysis goal is pathway enrichment or systems biology interpretation—use IOPA (integrative omics pathway analysis) instead.
- Sample groups have very small size (n < 5 per class) without external validation cohort—risk of overfitting.

## Inputs

- Preprocessed peak table (feature matrix: samples × peaks, numeric intensity values)
- Sample metadata with class labels or group membership (categorical phenotype assignments)
- Peak identifiers (m/z, retention time, or peak names)

## Outputs

- PLS/PLS-DA model object (fitted model coefficients and latent components)
- Variable importance scores (VIP scores or feature loadings for each peak)
- Classification metrics table (accuracy, sensitivity, specificity, confusion matrix)
- Results table with peak identifiers, importance scores, and classification statistics

## How to apply

Load the preprocessed peak table (intensity matrix) and sample metadata (phenotype/grouping information) into R. Parse the analysis type parameter to invoke PLS or PLS-DA modeling on the peak features, using class membership as the response variable. Build the model using peak intensities as predictors; the algorithm will identify latent components that maximize covariance between features and class labels. Extract variable importance scores (VIP scores or loadings) for each peak to rank their contribution to classification. Compute classification performance metrics including accuracy, sensitivity, and specificity on a held-out test set or via cross-validation. Aggregate results into a results table with peak identifiers, VIP scores, and classification metrics. Higher VIP scores and improved classification metrics (accuracy > random baseline, sensitivity and specificity both > 0.7) indicate the model has captured meaningful discriminatory patterns in the metabolome.

## Related tools

- **R** (Host language and runtime for implementing PLS/PLS-DA model fitting, VIP score computation, and classification metrics evaluation.) — https://www.r-project.org
- **SMART Statistical Analysis module** (Wraps PLS/PLS-DA modeling as part of the integrated metabolomics analysis pipeline; dispatches model fitting and metric computation.) — https://github.com/YuJenL/SMART

## Evaluation signals

- Classification metrics (accuracy, sensitivity, specificity) exceed random baseline (0.5 for binary classification) and are consistent across cross-validation folds.
- Variable importance (VIP) scores are computed for all peaks; peaks with VIP > 1 are typically considered important contributors to class discrimination.
- Results table contains non-null entries for all peaks with valid peak identifiers and numeric scores aligned to the input feature matrix dimensions.
- Model object is serializable and predictions on held-out test samples match the length and class labels of the input metadata.
- Feature loadings and model coefficients show interpretable direction (positive or negative association with each class) and do not contain NaN or Inf values.

## Limitations

- PLS-DA assumes linear relationships between peak intensities and class membership; non-linear patterns may be missed.
- Performance is sensitive to class imbalance (unequal group sizes); small class groups can lead to overfitting or biased VIP scores.
- The method requires sufficient samples per class (typically n ≥ 5–10) relative to the number of features to avoid overfitting; no formal sample size guidance is provided in the SMART documentation.
- Peak preprocessing choices (normalization, transformation, QC filtering) strongly influence model performance; results are not robust to arbitrary preprocessing pipelines.
- No built-in feature for external validation cohort or independent test set handling; users must manually partition or use cross-validation.

## Evidence

- [other] PLS/PLS-DA model fitting and classification: "For PLS/PLS-DA: build partial least-squares or discriminant analysis models using peak features to predict class membership; compute variable importance scores and classification metrics (accuracy,"
- [readme] Statistical Analysis module description in README: "Statistical Analysis: Perform association analysis (ANCOVA), classification analysis (PLS/PLS-DA), and integrative omics pathway analysis (IOPA)"
- [other] Input requirement: preprocessed peak table: "Load the preprocessed peak table (feature matrix with samples × peaks) into R. Parse the analysis type parameter (ANCOVA, PLS/PLS-DA, or IOPA) and sample metadata (phenotype/grouping information)."
- [other] Workflow outputs and aggregation: "Aggregate results (p-values, effect sizes, importance scores, or pathway statistics) into a single results table with peak identifiers and test-specific metrics."
