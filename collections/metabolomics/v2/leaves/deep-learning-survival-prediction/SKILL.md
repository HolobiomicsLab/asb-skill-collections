---
name: deep-learning-survival-prediction
description: Use when you have metabolomic or expression feature data, sample-level
  event indicators (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0208
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Lilikoi v2.0
  - R
  - Cox-nnet
  - Cox-PH
  license_tier: open
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

# deep-learning-survival-prediction

## Summary

Fit a Cox-nnet deep-learning survival model on metabolomic or expression data paired with event/time vectors to generate personalized risk stratification and prognosis indices. This skill integrates regularization, cross-validation, and gradient-based optimization to produce both individual-level risk scores and pathway-level survival predictions.

## When to use

You have metabolomic or expression feature data, sample-level event indicators (e.g., censoring status), and follow-up times, and you want to predict survival risk at both the metabolite/gene and pathway levels while accounting for non-linear relationships between features and survival outcomes.

## When NOT to use

- Event/time vectors are missing or incomplete; Cox models require complete follow-up data.
- Feature matrix contains only a handful of metabolites and no pathway grouping is available; deep learning requires sufficient feature dimensionality and sample size to avoid overfitting.
- Survival data violates the proportional hazards assumption; traditional Cox-PH may be more appropriate.

## Inputs

- event vector (binary: 0=censored, 1=event occurred)
- time vector (follow-up duration per sample)
- expression/metabolomic feature matrix (samples × features)
- cvlambda parameter (regularization sequence; optional)
- percent parameter (train/test split ratio; optional)

## Outputs

- prognosis index (numeric risk scores per sample)
- risk group assignments (categorical, e.g., low/medium/high)
- metabolite-level survival predictions
- pathway-level survival predictions
- cross-validation performance metrics

## How to apply

Load the survival event vector, follow-up time vector, and expression/metabolite feature matrix into R. Invoke lilikoi.prognosis() with coxnnet=TRUE, setting alpha=0 (no regularization penalty) or a non-zero value if feature selection is desired, nfold=5 for 5-fold cross-validation, method='quantile' for risk group stratification, and coxnnet_method='gradient' for optimization. The function applies Cox-nnet (a deep-learning variant of the Cox proportional hazards model) with gradient-based fitting to learn non-linear interactions between features and survival. Extract the resulting prognosis index (risk scores per sample) and risk group assignments; these represent personalized survival predictions that can be used for patient stratification or prognostic validation.

## Related tools

- **Lilikoi v2.0** (R package implementing lilikoi.prognosis() function with Cox-nnet and Cox-PH modules for survival prediction) — https://github.com/lanagarmire/lilikoi2
- **Cox-nnet** (Deep-learning survival model variant that learns non-linear associations between expression/metabolite features and survival outcomes)
- **Cox-PH** (Classical Cox proportional hazards baseline model; integrated as alternative to Cox-nnet)
- **R** (Computational environment and language for executing Lilikoi prognosis workflows)

## Examples

```
lilikoi.prognosis(event=event, time=time, exprdata=exprdata, alpha=0, nfold=5, method="quantile", coxnnet=TRUE, coxnnet_method="gradient")
```

## Evaluation signals

- Prognosis index values are numeric and sample counts match input expression matrix row count.
- Risk group assignments partition samples into categorical strata; verify median survival times differ significantly between groups via log-rank test.
- Cross-validation fold performance metrics (e.g., concordance index) are ≥ 0.6, indicating discrimination better than random chance.
- Prognosis index correlates positively with event occurrence and inversely with follow-up time in validation subset (Spearman ρ > 0.3).
- Pathway-level predictions are derived and distinct from metabolite-level predictions, confirming hierarchical integration.

## Limitations

- Cox-nnet assumes proportional hazards; violations may reduce model calibration.
- Requires sufficient sample size and event count (rule of thumb: ≥10–20 events per feature) to avoid overfitting; small cohorts benefit from stronger regularization (alpha > 0).
- Gradient-based optimization may converge to local minima; multiple random seeds or ensemble approaches can mitigate.
- No changelog found in repository documentation; users should verify version compatibility.
- Metabolite-to-pathway mapping depends on MetaTOpathway conversion and HMDB database completeness; missing or ambiguous identifiers may exclude features from pathway analysis.

## Evidence

- [other] The lilikoi.prognosis function integrates Cox-nnet with hyperparameters: "The lilikoi.prognosis function accepts survival event and time vectors, expression data, regularization parameter alpha (0 for no penalty), cross-validation fold count (nfold=5), prognosis index"
- [intro] Cox-nnet is a deep-learning survival model: "the most significant addition of prognosis prediction, implemented by Cox-PH model and the deep-learning based Cox-nnet model"
- [intro] Lilikoi v2.0 adds deep-learning classification: "The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods."
- [other] Workflow for invoking lilikoi.prognosis: "Invoke the Lilikoi v2.0 prognosis module with parameters: alpha=0 (no regularization penalty), nfold=5 (5-fold cross-validation), quantile method for risk stratification, and coxnnet=TRUE to fit the"
- [readme] Lilikoi v2 is a comprehensive metabolomics package in R: "Lilikoi v2 is a modern, comprehensive package to enable metabolomics analysis in R programming environment."
