---
name: risk-stratification-and-prognosis-indexing
description: Use when when you have paired survival data (event indicator and follow-up
  time vectors), expression or metabolomic feature matrices, and need to generate
  individual prognosis indices and assign samples to risk groups for downstream prognostic
  classification or treatment planning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - Lilikoi v2.0
  - R
  - Cox-nnet
  - Cox-PH
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification,
  in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis
  in R programming environment.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# risk-stratification-and-prognosis-indexing

## Summary

Compute personalized survival risk scores and stratify samples into prognostic groups using Cox proportional hazards models (Cox-PH or deep-learning Cox-nnet) applied to metabolomic or expression data paired with event/time vectors. This skill transforms continuous survival predictions into categorical risk strata for clinical decision-making.

## When to use

When you have paired survival data (event indicator and follow-up time vectors), expression or metabolomic feature matrices, and need to generate individual prognosis indices and assign samples to risk groups for downstream prognostic classification or treatment planning.

## When NOT to use

- Input expression/metabolomic data is already a pre-computed risk score or prognosis index—apply this skill to raw features, not derived scores.
- Survival event/time vectors are missing or incomplete; Cox models require complete pairs for all samples.
- The cohort has very few events (n < 10–20 events); Cox models may overfit and cross-validation will be unstable.

## Inputs

- Survival event vector (binary: event occurred or censored)
- Survival time vector (numeric: follow-up duration)
- Expression data matrix or metabolomic feature matrix (rows=samples, columns=features)
- Optional: percent threshold for feature selection
- Optional: cvlambda for lambda tuning in cross-validation

## Outputs

- Prognosis index (continuous risk scores, one per sample)
- Risk group assignments (categorical, typically stratified by quantile)
- Sample identifiers paired with prognosis indices and risk groups
- Survival predictions at metabolite and pathway levels

## How to apply

Load survival event/time vectors and expression/metabolomic data into the lilikoi.prognosis function with specified hyperparameters: alpha (regularization strength; 0 for no penalty), nfold (cross-validation folds, typically 5), method (e.g., 'quantile' for risk stratification), and coxnnet flag (TRUE for deep-learning Cox-nnet; FALSE for classical Cox-PH). The function applies gradient-based optimization with the selected Cox model to compute continuous prognosis indices (risk scores) at both metabolite and pathway levels. Extract the prognosis index and predicted risk groups for each sample. Validate that risk groups show stratified survival curves and that the cross-validation fold count and regularization parameter are documented.

## Related tools

- **Lilikoi v2.0** (Implements the lilikoi.prognosis function for Cox-PH and Cox-nnet prognosis prediction with hyperparameter tuning and risk stratification) — https://github.com/lanagarmire/lilikoi2
- **Cox-PH** (Classical Cox proportional hazards regression model for survival prediction)
- **Cox-nnet** (Deep-learning based Cox model using gradient-based optimization for nonlinear survival prediction)
- **R** (Programming environment for executing lilikoi prognosis workflows)

## Examples

```
lilikoi.prognosis(event=survival_events, time=survival_times, exprdata=expr_matrix, alpha=0, nfold=5, method="quantile", coxnnet=TRUE, coxnnet_method="gradient")
```

## Evaluation signals

- Prognosis index is numeric, continuous, and ranges plausibly (typically unbounded; check for outliers or NaNs).
- Risk group assignments are categorical and non-empty; group sizes are roughly balanced or reflect expected class prevalence.
- All input samples have a corresponding prognosis index and risk group assignment (no missing values after execution).
- Kaplan–Meier survival curves for each risk group are visibly stratified with non-overlapping confidence intervals and significant log-rank test (p < 0.05).
- Cross-validation folds are balanced and reported; alpha and nfold parameters match the invocation and are documented.

## Limitations

- Requires complete survival event and time pairs; samples with missing event or time data must be removed before analysis.
- Cox models assume proportional hazards; check assumption violation using residual diagnostics (e.g., Schoenfeld residuals); if violated, consider stratified or time-varying coefficient models.
- Deep-learning Cox-nnet may overfit on small cohorts (n < 100–200 samples); cross-validation and regularization (alpha parameter) are essential.
- Risk stratification is data-driven (quantile-based); group cutoffs may not be reproducible or clinically meaningful across independent cohorts.
- No changelog or version compatibility matrix provided; reproducibility may require pinning to a specific Lilikoi v2.0 release.

## Evidence

- [other] Cox-nnet integration and prognosis function hyperparameters: "The lilikoi.prognosis function accepts survival event and time vectors, expression data, regularization parameter alpha (0 for no penalty), cross-validation fold count (nfold=5), prognosis index"
- [intro] Core prognosis prediction capability: "the most significant addition of prognosis prediction, implemented by Cox-PH model and the deep-learning based Cox-nnet model"
- [readme] Lilikoi v2.0 design and scope: "The new Lilikoi v2 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods. It also has several new modules, including the most"
- [readme] Lilikoi prognosis function signature and workflow: "lilikoi.prognosis(event, time, exprdata, percent=percent, alpha=0, nfold=5, method="quantile", cvlambda=cvlambda,python.path=NULL,coxnnet=FALSE,coxnnet_method="gradient")"
- [other] Output and results structure: "Extract the prognosis index (risk scores) and survival predictions for each sample. 4. Generate a results table containing sample identifiers, prognosis indices, and predicted risk groups"
