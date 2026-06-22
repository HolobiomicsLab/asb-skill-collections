---
name: bayesian-model-update-with-experimental-data
description: Use when you have completed one or more LC-MS gradient runs, extracted separation efficiency metrics from the resulting MS1 and MS2 spectra, and need to incorporate those real experimental observations into your Gaussian process model to improve the next gradient proposal.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - BAGO
  - pyopenms
  - scikit-learn
  - Python
  - bago
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2023.09.08.556930
  title: BAGO
- doi: 10.1002/9780470508183
  title: ''
evidence_spans:
- BAGO is a Bayesian optimization strategy for LC gradient optimization for MS-based small molecule analysis
- A :class:`ms1Spectrum` object (supported by :mod:`bago`)
- A :class:`MSExperiment` object (supported by :mod:`pyopenms`)
- a :class:`sklearn.preprocessing.StandardScaler` object used to scale the data
- a :class:`sklearn.gaussian_process.GaussianProcessRegressor` object
- Download and install Python 3.8 or later from `python.org`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bago_cq
    doi: 10.1101/2023.09.08.556930
    title: BAGO
  dedup_kept_from: coll_bago_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2023.09.08.556930
  all_source_dois:
  - 10.1101/2023.09.08.556930
  - 10.1002/9780470508183
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bayesian-model-update-with-experimental-data

## Summary

Iteratively update a Gaussian process regression model with newly acquired LC-MS experimental data to refine predictions of separation efficiency and identify optimal gradient parameters. This skill enables closed-loop optimization where each new gradient trial yields MS1/MS2 spectra, separation metrics, and model retraining until convergence or a predefined stopping criterion is reached.

## When to use

Apply this skill when you have completed one or more LC-MS gradient runs, extracted separation efficiency metrics from the resulting MS1 and MS2 spectra, and need to incorporate those real experimental observations into your Gaussian process model to improve the next gradient proposal. Use this when the current model's predictions are stale and must be refined with fresh LC-MS data before selecting the subsequent gradient point to evaluate.

## When NOT to use

- If you have not yet acquired experimental LC-MS data from at least one gradient trial; the model requires labeled training observations.
- If the raw MS data is corrupted, incomplete, or cannot be parsed into ms1Spectrum and ms2Spectrum objects by pyopenms.
- If you are in the initial design phase and have not yet defined or validated your separation efficiency metric; model retraining assumes this metric is stable and reproducible across runs.

## Inputs

- mzML or mzXML raw LC-MS data file
- ms1Spectrum objects (extracted MS1 scans)
- ms2Spectrum objects (extracted MS2 scans)
- gradient parameter encoding (numeric vector, prior runs)
- separation efficiency metric (prior observations)
- trained Gaussian process regression model (from prior iteration or initialization)

## Outputs

- updated Gaussian process regression model (retrained with new data)
- separation efficiency value for current gradient
- model convergence/stopping criterion assessment (Boolean or metric)
- updated training dataset (prior + new gradient/efficiency pair)

## How to apply

After each LC-MS gradient trial: (1) extract MS1 and MS2 spectra from the raw LC-MS data (mzML or mzXML format) using pyopenms into ms1Spectrum and ms2Spectrum objects; (2) identify top signals in the MS1 data and compute separation efficiency (a retention time spacing metric) as the performance label for this gradient; (3) encode the tested gradient parameters and scale them with sklearn StandardScaler to match the feature space of prior runs; (4) retrain the Gaussian process regression model using scikit-learn with all prior gradient encodings and separation efficiency values plus the new observation; (5) evaluate convergence or stopping criterion (typically ≤10 total runs or plateau in model improvement). Repeat this cycle until the stopping criterion is satisfied, at which point the final trained model represents the optimized gradient landscape.

## Related tools

- **pyopenms** (Parses mzML/mzXML files and extracts MS1 and MS2 spectra into standardized objects for separation efficiency computation)
- **scikit-learn** (Provides Gaussian process regression model training (fit method) and StandardScaler for feature normalization of gradient encodings)
- **bago** (Implements the complete Bayesian optimization workflow, including ms1Spectrum/ms2Spectrum object handling, separation efficiency calculation, and model retraining orchestration) — https://github.com/huaxuyu/bago/

## Examples

```
from bago import readRawData, extractMS1, extractMS2, findTopSignals, sepEfficiency, fit; ms_exp = readRawData('gradient_trial_5.mzML'); ms1_spectra = extractMS1(ms_exp); top_signals = findTopSignals(ms1_spectra); sep_eff = sepEfficiency(top_signals); model_updated = fit(model_prior, gradient_encodings_all, [sep_eff_prior_1, ..., sep_eff])
```

## Evaluation signals

- The retrained Gaussian process model shows improved prediction accuracy on held-out prior observations (e.g., lower mean squared error or higher log-likelihood than the previous model iteration).
- Separation efficiency computed from the new gradient trial is numerically valid (non-negative, within expected range for the sample and LC method), and the model's prediction for that gradient (before update) differs meaningfully from the observed value, confirming the new data is informative.
- The model's posterior uncertainty (predictive variance) decreases in regions of parameter space where new observations were added, and remains high in unexplored regions, indicating appropriate Bayesian updating.
- Stopping criterion is evaluated correctly: either the total number of gradient trials reaches the bound (≤10 runs) or the improvement in separation efficiency between successive runs falls below a convergence threshold.
- The updated model's acquisition function output (e.g., Expected Improvement) identifies the next gradient point correctly, and that point differs from previously tested gradients, confirming the model has learned from the new data.

## Limitations

- Model retraining assumes that separation efficiency is deterministic and reproducible across repeated runs of the same gradient; instrumental noise or day-to-day LC drift can degrade model reliability.
- Gaussian process regression may become computationally expensive if the number of prior gradient runs approaches or exceeds 100; scikit-learn's implementation scales roughly O(n³) in the number of training points.
- The separation efficiency metric is defined at the omics scale (aggregate compound separation performance); it may mask optimization opportunities for specific, rare, or poorly-ionized analytes that dominate the LC-MS signal.
- Model retraining is most effective when gradient encodings cover a diverse and contiguous portion of the search space; sparse or clustered prior evaluations can lead to poor extrapolation and suboptimal next-point proposals.

## Evidence

- [other] Fit a Gaussian process regression model to training data (gradient encodings as input, separation efficiency as output) using scikit-learn.: "Fit a Gaussian process regression model to training data (gradient encodings as input, separation efficiency as output) using scikit-learn."
- [other] Repeat steps 2–5 for successive runs, updating the model with new MS data from each gradient trial, until reaching the stopping criterion (≤10 runs or convergence).: "Repeat steps 2–5 for successive runs, updating the model with new MS data from each gradient trial, until reaching the stopping criterion (≤10 runs or convergence)."
- [other] Find top signals in MS1 data and compute separation efficiency (retention time spacing metric) for the initial gradient run.: "Find top signals in MS1 data and compute separation efficiency (retention time spacing metric) for the initial gradient run."
- [readme] Separation efficiency was defined to evaluate the performance of a gradient.: "Separation efficiency was defined to evaluate the performance of a gradient."
- [readme] Model LC-MS experiment to evaluate compound separation performance: "Model LC-MS experiment to evaluate compound separation performance"
