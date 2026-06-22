---
name: gaussian-process-regression-model-fitting
description: Use when after you have accumulated experimental MS data from ≥2 LC gradient trials, extracted separation efficiency metrics (retention time spacing) from each trial, and encoded each gradient as a feature vector.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gaussian-process-regression-model-fitting

## Summary

Fit a Gaussian process regression model to LC gradient encodings and separation efficiency metrics to enable probabilistic prediction of gradient performance and acquisition function-driven selection of the next gradient to evaluate. This skill is the core inference step in BAGO's iterative Bayesian optimization loop.

## When to use

After you have accumulated experimental MS data from ≥2 LC gradient trials, extracted separation efficiency metrics (retention time spacing) from each trial, and encoded each gradient as a feature vector. Use this skill when you need to: (1) model the non-linear relationship between gradient parameters and separation performance, (2) quantify prediction uncertainty to guide exploration vs. exploitation, or (3) compute an acquisition function (Expected Improvement, UCB, etc.) to propose the next gradient point within a bounded number of runs (target: ≤10 total runs).

## When NOT to use

- If you have fewer than 2 prior gradient trials, Gaussian process fitting will have insufficient data to estimate mean, variance, or hyperparameters reliably; use random or grid-based initial sampling instead.
- If separation efficiency has not been computed for all prior trials (e.g., MS data is missing or poorly calibrated), the training targets are invalid and the posterior will be misleading.
- If the gradient search space is discrete and small (e.g., <5 distinct gradients), exhaustive or simple grid search may be more appropriate than Bayesian optimization.

## Inputs

- gradient_encodings: feature matrix (N trials × P parameters, float array), scaled via StandardScaler
- separation_efficiency_scores: vector of N separation efficiency values computed from MS1 retention times
- candidate_search_space: matrix of M candidate gradients to evaluate (M × P, scaled)

## Outputs

- fitted_gp_model: trained GaussianProcessRegressor object with learned hyperparameters
- posterior_mean: predicted separation efficiency for each candidate gradient (M-length vector)
- posterior_variance: uncertainty (variance) of predictions for each candidate (M-length vector)
- next_gradient_proposal: index and encoded parameters of the gradient with highest acquisition function score

## How to apply

Prepare a matrix of gradient encodings (rows = past trials, columns = encoded gradient parameters, scaled using sklearn.preprocessing.StandardScaler) and a corresponding vector of separation efficiency scores (output of sepEfficiency() function applied to retention times from each trial's MS data). Fit a scikit-learn GaussianProcessRegressor to this training data using the default or tuned kernel (e.g., RBF + white noise). After fitting, call predict() and predict_std() to obtain posterior mean and variance for candidate gradients in the search space. Use the posterior distribution to compute an acquisition function (Expected Improvement by default via computeNextGradient()); the function returns both the predicted performance and uncertainty for the highest-scoring candidate. Repeat this fit–predict–acquire cycle on each successive run, appending new MS-derived separation efficiency data to the training set, until convergence or reaching the stopping criterion.

## Related tools

- **scikit-learn** (Provides GaussianProcessRegressor class and StandardScaler for model fitting and input normalization)
- **pyopenms** (Reads raw LC-MS data (mzML/mzXML) into MSExperiment objects; used upstream to extract MS1/MS2 spectra for retention time extraction)
- **bago** (Python package wrapping the end-to-end Bayesian optimization workflow; genSearchSpace() generates candidate gradients, fit() calls this skill, computeNextGradient() applies acquisition function to model output) — https://github.com/huaxuyu/bago

## Evaluation signals

- Model converges: scikit-learn's GaussianProcessRegressor.fit() completes without raising singular matrix or optimization warnings.
- Posterior variance is non-negative everywhere in the search space and decreases near training points (points already evaluated should have lower uncertainty than unexplored regions).
- Successive gradients proposed by computeNextGradient() show increasing separation efficiency across runs, reaching near-optimal performance within 10 runs on benchmark LC-MS data.
- Cross-validation: fit the model on a subset of trials and predict held-out trials; mean absolute error should be <5–10% of the range of separation efficiency observed.
- Acquisition function output is stable: re-fitting the model with the same training data produces the same or very similar next-gradient proposal.

## Limitations

- Gaussian process fitting assumes a smooth, bounded relationship between gradient parameters and separation efficiency; if the landscape is highly multi-modal or discontinuous, the model may miss isolated optima.
- With very few training samples (<3 trials), hyperparameter estimates (length scale, noise variance) may be biased or overfitted; consider using fixed, domain-informed priors.
- Computational cost of GP inference scales as O(N³) where N is the number of training points; beyond ~100 trials, sparse approximations or inducing-point methods may be necessary.
- The choice of acquisition function (Expected Improvement, UCB, pure exploration, etc.) significantly affects gradient selection; no single acquisition function is optimal for all LC-MS scenarios and must be validated empirically.

## Evidence

- [methods] Fit a Gaussian process regression model to training data (gradient encodings as input, separation efficiency as output) using scikit-learn.: "Fit a Gaussian process regression model to training data (gradient encodings as input, separation efficiency as output) using scikit-learn."
- [methods] Generate a search space of candidate gradients using parameter bounds, scaling inputs with sklearn StandardScaler.: "Generate a search space of candidate gradients using parameter bounds, scaling inputs with sklearn StandardScaler."
- [methods] Select the next gradient to evaluate using an acquisition function (Expected Improvement by default) via computeNextGradient().: "Select the next gradient to evaluate using an acquisition function (Expected Improvement by default) via computeNextGradient()."
- [methods] Repeat steps 2–5 for successive runs, updating the model with new MS data from each gradient trial, until reaching the stopping criterion (≤10 runs or convergence).: "Repeat steps 2–5 for successive runs, updating the model with new MS data from each gradient trial, until reaching the stopping criterion (≤10 runs or convergence)."
- [readme] Wonder why BAGO is efficient? Read more about acquisition functions.: "Wonder why BAGO is efficient? Read more about acquisition functions."
