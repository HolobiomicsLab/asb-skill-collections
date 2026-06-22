---
name: cox-regression-model-fitting
description: Use when you have expression or metabolomic feature matrices, paired with event indicators (e.g., disease recurrence, mortality) and follow-up times for a cohort of samples, and you need to derive risk scores or prognosis indices for survival prediction or patient stratification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa162
  all_source_dois:
  - 10.1093/gigascience/giaa162
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cox-regression-model-fitting

## Summary

Fit Cox proportional hazards models (Cox-PH and deep-learning Cox-nnet variants) to metabolomics or gene expression data paired with survival event/time vectors to generate personalized prognosis indices and risk stratification. This skill enables survival prediction at both individual metabolite and aggregated pathway levels.

## When to use

You have expression or metabolomic feature matrices, paired with event indicators (e.g., disease recurrence, mortality) and follow-up times for a cohort of samples, and you need to derive risk scores or prognosis indices for survival prediction or patient stratification. Use this when your goal is personalized risk modeling rather than group-level association testing.

## When NOT to use

- Input lacks both event and time vectors (unpaired or cross-sectional survival data cannot be modeled).
- Feature matrix is already a pre-computed prognosis index or risk score (avoid double-modeling).
- Sample size is very small (n < 20–30) relative to feature count, risking overfitting even with regularization.

## Inputs

- Survival event vector (binary: 0/1 or censoring status)
- Follow-up time vector (numeric, in appropriate time units)
- Expression or metabolomic feature matrix (samples × features; numeric)
- Cross-validation parameters (nfold integer, typically 5)
- Regularization penalty alpha (numeric, 0 ≤ alpha ≤ 1)

## Outputs

- Prognosis index (risk scores per sample)
- Risk group assignments (stratified by quantile method)
- Model coefficients or learned weights
- Survival predictions at metabolite level
- Survival predictions at pathway level
- Results table (sample identifiers, prognosis indices, risk groups)

## How to apply

Load survival event and time vectors alongside expression/metabolomic feature data into R. Invoke lilikoi.prognosis with regularization parameter alpha (0 for no penalty, >0 for L1/L2 regularization), nfold (typically 5 for cross-validation), method='quantile' for risk group stratification, and coxnnet flag (TRUE for deep-learning Cox-nnet, FALSE for classical Cox-PH). The function optimizes model coefficients using gradient-based methods and returns prognosis indices (risk scores) and predicted risk groups for each sample. Extract the prognosis index table and survival predictions at both metabolite and pathway levels for downstream interpretation.

## Related tools

- **Lilikoi v2.0** (R package implementing lilikoi.prognosis function with Cox-PH and Cox-nnet model fitting, cross-validation, and prognosis index calculation) — https://github.com/lanagarmire/lilikoi2
- **Cox-PH** (Classical Cox proportional hazards regression backbone for survival modeling)
- **Cox-nnet** (Deep-learning variant of Cox regression using gradient-based optimization for non-linear survival prediction)
- **R** (Programming environment for running lilikoi.prognosis and survival analysis workflows)

## Examples

```
lilikoi.prognosis(event=event_vector, time=time_vector, exprdata=expression_matrix, alpha=0, nfold=5, method="quantile", coxnnet=TRUE, coxnnet_method="gradient")
```

## Evaluation signals

- Prognosis indices are numeric, finite, and have non-zero variance across samples (not constant or all NA).
- Risk group assignments are discrete (e.g., 'Low', 'Medium', 'High') or integer-valued quantile bins with balanced or expected prevalence.
- Model convergence is achieved within gradient descent (warnings or non-convergence flags should be inspected).
- Cross-validation fold predictions show reasonable discrimination: concordance index (C-index) or log-rank test p-value on held-out folds should be reported and compared to null/random baseline.
- Prognosis indices correlate with actual survival outcomes: Kaplan–Meier curves stratified by predicted risk groups should show separation (log-rank p < 0.05 is typical).

## Limitations

- Cox-PH assumes proportional hazards; violation of this assumption can bias estimates (test with Schoenfeld residuals or use stratified analysis).
- Deep-learning Cox-nnet requires careful hyperparameter tuning (alpha, nfold, cvlambda) and may overfit on small cohorts; validation on independent data is essential.
- Regularization parameter alpha must be chosen; cross-validation on cvlambda sequence is recommended but adds computational cost.
- No changelog provided in repository documentation; reproducibility across package versions may require pinning Lilikoi v2.0 release tag.
- Method assumes complete follow-up times and event indicators; missing or miscoded survival data will propagate into predictions.

## Evidence

- [other] The lilikoi.prognosis function accepts survival event and time vectors, expression data, regularization parameter alpha (0 for no penalty), cross-validation fold count (nfold=5), prognosis index method ('quantile'), and a coxnnet flag (TRUE) with gradient-based optimization to compute survival predictions at both metabolite and pathway levels.: "accepts survival event and time vectors, expression data, regularization parameter alpha (0 for no penalty), cross-validation fold count (nfold=5), prognosis index method ('quantile'), and a coxnnet"
- [intro] the most significant addition of prognosis prediction, implemented by Cox-PH model and the deep-learning based Cox-nnet model: "the most significant addition of prognosis prediction, implemented by Cox-PH model and the deep-learning based Cox-nnet model"
- [other] Invoke the Lilikoi v2.0 prognosis module with parameters: alpha=0 (no regularization penalty), nfold=5 (5-fold cross-validation), quantile method for risk stratification, and coxnnet=TRUE to fit the deep-learning Cox-nnet model.: "Invoke the Lilikoi v2.0 prognosis module with parameters: alpha=0 (no regularization penalty), nfold=5 (5-fold cross-validation), quantile method for risk stratification, and coxnnet=TRUE to fit the"
- [other] Extract the prognosis index (risk scores) and survival predictions for each sample. 4. Generate a results table containing sample identifiers, prognosis indices, and predicted risk groups.: "Extract the prognosis index (risk scores) and survival predictions for each sample. Generate a results table containing sample identifiers, prognosis indices, and predicted risk groups"
- [readme] lilikoi.prognosis(event, time, exprdata, percent=percent, alpha=0, nfold=5, method="quantile", cvlambda=cvlambda,python.path=NULL,coxnnet=FALSE,coxnnet_method="gradient"): "lilikoi.prognosis(event, time, exprdata, percent=percent, alpha=0, nfold=5, method="quantile", cvlambda=cvlambda,python.path=NULL,coxnnet=FALSE,coxnnet_method="gradient")"
