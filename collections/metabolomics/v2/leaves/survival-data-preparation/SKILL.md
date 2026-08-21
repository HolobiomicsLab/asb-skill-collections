---
name: survival-data-preparation
description: Use when when you have clinical survival outcomes (event status and follow-up
  time) and high-dimensional metabolomic or expression data, and you need to feed
  them into Cox-PH or Cox-nnet prognosis models.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0625
  tools:
  - Lilikoi v2.0
  - R
  - Cox-nnet
  - Cox-PH
  techniques:
  - LC-MS
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

# survival-data-preparation

## Summary

Prepare and structure survival event/time vectors alongside expression or metabolomic feature matrices for downstream Cox proportional hazards modeling and prognosis prediction. This skill ensures data alignment and format compliance required by survival analysis modules in Lilikoi v2.0.

## When to use

When you have clinical survival outcomes (event status and follow-up time) and high-dimensional metabolomic or expression data, and you need to feed them into Cox-PH or Cox-nnet prognosis models. Specifically, use this skill when event vectors (0/1 censoring indicators) and time vectors (numeric follow-up durations) must be paired with a feature matrix (metabolites × samples or genes × samples) for risk stratification or survival prediction at both metabolite and pathway levels.

## When NOT to use

- Event vector contains values other than 0 or 1, or time vector contains negative values — data must be cleaned before preparation.
- Sample identifiers in the event/time vectors do not match those in the feature matrix — reorder or merge data first.
- Expression/metabolomic data are already aggregated into pathway-level scores — this skill is for raw or metabolite-level features, not pre-computed pathway indices.

## Inputs

- event vector (binary, 0=censored / 1=event)
- time vector (numeric, non-negative follow-up duration)
- expression or metabolomic data matrix (features × samples)
- sample identifiers (string vector or rownames/colnames)

## Outputs

- aligned survival event vector
- aligned survival time vector
- validated feature matrix with consistent sample ordering
- data integrity report (sample count, event/censoring counts, missing value flags)

## How to apply

Load the survival event vector (binary: 0=censored, 1=event) and time vector (numeric follow-up duration in consistent units) into R alongside the expression/metabolomic data matrix. Ensure sample identifiers and row/column ordering are consistent across all objects. Validate that event values are strictly 0 or 1 and that time values are non-negative. Organize the data so that the feature matrix columns correspond exactly to the event and time vector entries by sample. This preparation step precedes invocation of lilikoi.prognosis() with parameters alpha=0 (no regularization), nfold=5 (5-fold cross-validation), method='quantile' for risk stratification, and coxnnet=TRUE for deep-learning Cox-nnet model fitting. The rationale is to enforce data integrity and traceability before Cox model optimization, reducing downstream fitting errors and ensuring accurate prognosis index (risk score) computation.

## Related tools

- **Lilikoi v2.0** (R package that executes survival prognosis prediction after data preparation; provides lilikoi.prognosis() function accepting prepared event, time, and expression data) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment in which survival event/time vectors and feature matrices are loaded, validated, and formatted)
- **Cox-PH** (Statistical model baseline for prognosis prediction; requires properly aligned survival and feature data)
- **Cox-nnet** (Deep-learning Cox model that accepts prepared survival vectors and expression data for gradient-based optimization)

## Examples

```
dt <- lilikoi.Loaddata(file=system.file("extdata", "plasma_breast_cancer.csv", package = "lilikoi")); event <- dt$Metadata$event; time <- dt$Metadata$time; exprdata <- dt$dataSet; lilikoi.prognosis(event, time, exprdata, alpha=0, nfold=5, method="quantile", coxnnet=TRUE, coxnnet_method="gradient")
```

## Evaluation signals

- Event vector length equals time vector length equals number of columns (samples) in feature matrix.
- Event vector contains only values 0 or 1; no missing/NA entries unless explicitly documented.
- Time vector contains only non-negative numeric values; no negative durations or NAs.
- Sample identifiers in feature matrix columns match event/time vector names or indices in the same order.
- lilikoi.prognosis() executes without sample mismatch errors and returns a results table with sample identifiers, prognosis indices, and risk group assignments.

## Limitations

- The skill assumes survival data are already in event/time format; conversion from other formats (e.g., diagnosis date + last follow-up date) is not covered.
- No handling of competing risks; the binary event indicator assumes a single event type.
- Missing values in event or time vectors are not automatically imputed; they must be handled before preparation.
- Lilikoi v2.0 requires consistent units for time (e.g., days or months); time vector unit conversion must be done prior to this skill.

## Evidence

- [other] The lilikoi.prognosis function accepts survival event and time vectors, expression data, regularization parameter alpha (0 for no penalty), cross-validation fold count (nfold=5), prognosis index method ('quantile'), and a coxnnet flag (TRUE) with gradient-based optimization to compute survival predictions.: "The lilikoi.prognosis function accepts survival event and time vectors, expression data, regularization parameter alpha (0 for no penalty), cross-validation fold count (nfold=5), prognosis index"
- [other] Load survival event/time data and metabolomic/expression feature matrix into R. Invoke the Lilikoi v2.0 prognosis module with parameters: alpha=0 (no regularization penalty), nfold=5 (5-fold cross-validation), quantile method for risk stratification, and coxnnet=TRUE to fit the deep-learning Cox-nnet model.: "Load survival event/time data and metabolomic/expression feature matrix into R. Invoke the Lilikoi v2.0 prognosis module with parameters: alpha=0 (no regularization penalty), nfold=5"
- [other] Extract the prognosis index (risk scores) and survival predictions for each sample. Generate a results table containing sample identifiers, prognosis indices, and predicted risk groups.: "Extract the prognosis index (risk scores) and survival predictions for each sample. Generate a results table containing sample identifiers, prognosis indices, and predicted risk groups."
- [intro] the most significant addition of prognosis prediction, implemented by Cox-PH model and the deep-learning based Cox-nnet model: "the most significant addition of prognosis prediction, implemented by Cox-PH model and the deep-learning based Cox-nnet model"
- [readme] lilikoi.prognosis(event, time, exprdata, percent=percent, alpha=0, nfold=5, method="quantile", cvlambda=cvlambda,python.path=NULL,coxnnet=FALSE,coxnnet_method="gradient"): "lilikoi.prognosis(event, time, exprdata, percent=percent, alpha=0, nfold=5, method="quantile", cvlambda=cvlambda,python.path=NULL,coxnnet=FALSE,coxnnet_method="gradient")"
