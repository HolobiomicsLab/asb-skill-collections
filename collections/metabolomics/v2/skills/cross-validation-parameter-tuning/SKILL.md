---
name: cross-validation-parameter-tuning
description: Use when when building Cox-PH or Cox-nnet survival models from expression or metabolomic feature matrices paired with event/time vectors, and you need to select optimal regularization strength (alpha), cross-validation fold count (nfold), risk stratification method, and optimization strategy before.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3745
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Lilikoi v2.0
  - R
  - Cox-nnet
  - Cox-PH
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis in R programming environment.
- the deep-learning based Cox-nnet model
- prognosis prediction, implemented by Cox-PH model
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lilikoi_v2_0_cq
    doi: 10.1093/gigascience/giaa162
    title: Lilikoi V2.0
  dedup_kept_from: coll_lilikoi_v2_0_cq
schema_version: 0.2.0
---

# cross-validation-parameter-tuning

## Summary

Optimize Cox regression and neural network hyperparameters (regularization penalty α, fold count, optimization method) through k-fold cross-validation to generate robust survival predictions from metabolomic or expression data. This skill ensures that prognosis models generalize well across held-out data partitions and avoid overfitting.

## When to use

When building Cox-PH or Cox-nnet survival models from expression or metabolomic feature matrices paired with event/time vectors, and you need to select optimal regularization strength (alpha), cross-validation fold count (nfold), risk stratification method, and optimization strategy before generating final prognosis indices and risk group assignments.

## When NOT to use

- Input data lacks survival time or event information — prognosis prediction requires both paired event and time vectors.
- Feature matrix has fewer samples than nfold × 2 — insufficient data to create meaningful cross-validation partitions.
- Goal is exploratory classification (disease vs. control) rather than survival prediction — use lilikoi.machine_learning instead.

## Inputs

- survival event vector (binary: 0/1 or censoring indicator)
- survival time vector (numeric: follow-up or event time)
- expression or metabolomic feature matrix (samples × features)
- alpha parameter (numeric: regularization penalty; 0 = no penalty)
- nfold (integer: number of cross-validation folds; typically 5)
- method string ('quantile' for prognosis index stratification)
- cvlambda (numeric or vector: lambda penalty search range)
- coxnnet flag (boolean: TRUE for Cox-nnet, FALSE for Cox-PH)

## Outputs

- prognosis index vector (numeric risk scores per sample)
- risk group assignments (stratified by quantile or threshold)
- cross-validation fold assignments (which folds each sample belongs to)
- results table with columns: sample_id, prognosis_index, risk_group
- model performance metrics across folds (if returned by lilikoi.prognosis)

## How to apply

Load survival event and time vectors alongside a feature matrix (metabolomic or expression data). Invoke lilikoi.prognosis() with cross-validation parameters: alpha (typically 0 for no L1/L2 penalty, or a positive value for regularization), nfold (commonly 5 for 5-fold CV), method ('quantile' for risk stratification), and coxnnet flag (TRUE to use deep-learning Cox-nnet, FALSE for standard Cox-PH). Set cvlambda to control lambda parameter search during cross-validation. The function partitions data into nfold subsets, fits the model on nfold-1 folds, evaluates on the held-out fold, and repeats; it reports both the prognosis index (risk scores) and predicted risk group assignments. Extract the results table containing sample identifiers, prognosis indices, and risk group classifications to assess model stability and predictive performance across folds.

## Related tools

- **Lilikoi v2.0** (R package hosting lilikoi.prognosis() function; executes Cox-PH and Cox-nnet models with cross-validation parameter tuning) — https://github.com/lanagarmire/lilikoi2
- **Cox-PH** (Standard Cox proportional hazards baseline model for survival prediction when coxnnet=FALSE)
- **Cox-nnet** (Deep-learning-based Cox model activated when coxnnet=TRUE; uses gradient-based optimization within cross-validation)
- **R** (Programming environment in which lilikoi.prognosis() and cross-validation workflows are executed)

## Examples

```
lilikoi.prognosis(event=surv_event, time=surv_time, exprdata=expr_matrix, alpha=0, nfold=5, method='quantile', cvlambda=cvlambda, coxnnet=TRUE, coxnnet_method='gradient')
```

## Evaluation signals

- Cross-validation loop completes without error and produces prognosis indices for 100% of input samples.
- Prognosis indices are numeric, finite (no NaN/Inf), and show variation across samples (not all identical).
- Risk group assignments stratify samples into ≥2 distinct quantile-based strata with expected distribution (e.g., roughly equal counts per group for 'quantile' method).
- Model performance (e.g., concordance index or log-rank test p-value) is computed and reported separately for each cross-validation fold, with consistent trends across folds indicating stable hyperparameter selection.
- Results table row count matches input sample count; no samples are dropped or duplicated during CV partitioning.

## Limitations

- Cross-validation fold count (nfold) must be ≤ sample size; datasets with <5 samples per fold may yield unstable estimates.
- Alpha regularization penalty and cvlambda range must be specified a priori; the function does not automatically optimize these without domain knowledge or a grid search wrapper.
- Cox-nnet deep-learning optimization uses gradient descent and may converge to local minima; results can vary with random seed and initialization.
- No changelog documented in the article or README; versioning and parameter behavior changes across Lilikoi releases are not explicitly tracked.

## Evidence

- [other] alpha=0 (no regularization penalty), nfold=5 (5-fold cross-validation), quantile method for risk stratification, and coxnnet=TRUE to fit the deep-learning Cox-nnet model: "alpha=0 (no regularization penalty), nfold=5 (5-fold cross-validation), quantile method for risk stratification, and coxnnet=TRUE to fit the deep-learning Cox-nnet model"
- [other] The lilikoi.prognosis function accepts survival event and time vectors, expression data, regularization parameter alpha (0 for no penalty), cross-validation fold count (nfold=5), prognosis index method ('quantile'), and a coxnnet flag (TRUE) with gradient-based optimization: "lilikoi.prognosis function accepts survival event and time vectors, expression data, regularization parameter alpha (0 for no penalty), cross-validation fold count (nfold=5), prognosis index method"
- [intro] the most significant addition of prognosis prediction, implemented by Cox-PH model and the deep-learning based Cox-nnet model: "prognosis prediction, implemented by Cox-PH model and the deep-learning based Cox-nnet model"
- [readme] lilikoi.prognosis(event, time, exprdata, percent=percent, alpha=0, nfold=5, method="quantile", cvlambda=cvlambda,python.path=NULL,coxnnet=FALSE,coxnnet_method="gradient"): "lilikoi.prognosis(event, time, exprdata, percent=percent, alpha=0, nfold=5, method="quantile", cvlambda=cvlambda,python.path=NULL,coxnnet=FALSE,coxnnet_method="gradient")"
