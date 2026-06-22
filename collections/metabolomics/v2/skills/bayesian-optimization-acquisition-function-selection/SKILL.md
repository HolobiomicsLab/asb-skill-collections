---
name: bayesian-optimization-acquisition-function-selection
description: Use when after fitting a Gaussian Process regression model to prior LC-MS gradient evaluations (where gradients are encoded as input and separation efficiency is output), use this skill to decide which candidate gradient to test next.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - BAGO
  - pyopenms
  - scikit-learn
  - Python
  - bago (Python package)
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
---

# bayesian-optimization-acquisition-function-selection

## Summary

Select and apply an acquisition function to a fitted Gaussian Process model to propose the next LC gradient point for evaluation in a Bayesian optimization loop. This skill determines whether to favor exploration, exploitation, or a balanced trade-off when navigating the gradient parameter space.

## When to use

After fitting a Gaussian Process regression model to prior LC-MS gradient evaluations (where gradients are encoded as input and separation efficiency is output), use this skill to decide which candidate gradient to test next. Apply it when you have ≤10 total allowed runs and need to efficiently allocate remaining trials to improve separation efficiency.

## When NOT to use

- If the Gaussian Process model has not yet been fitted to any prior gradient evaluations (no training data available); acquisition function selection requires a trained model.
- If the search space (gridX) is empty or does not cover the relevant gradient parameter bounds; the function cannot propose a meaningful gradient.
- If separation efficiency has already converged or plateaued across multiple consecutive runs; further Bayesian optimization acquisitions will not yield improvement and budget should be spent on confirmatory replicates instead.

## Inputs

- fitted Gaussian Process regression model (gpModel with mean and variance predictions)
- scaled training data (scaledX: prior gradient encodings and separation efficiency measurements)
- grid search space (gridX: all candidate unscaled gradient parameters within bounds)
- current best separation efficiency metric (scalar)
- acquisition function selector (string: 'ei', 'pi', 'ucb', 'eps', 'explore', 'exploit', or 'rand')
- epsilon parameter (float, if acqFunc='eps')
- UCB scaling factor (float, if acqFunc='ucb')

## Outputs

- next gradient proposal (unscaled parameter vector to evaluate in the next LC-MS run)
- acquisition function value at selected point (scalar)
- grid indices or coordinates of the selected point

## How to apply

Retrieve the trained GP model (gpModel), scaled training data (scaledX), grid search space (gridX), and the user-specified acquisition function parameter (acqFunc). Query the GP model to generate predicted mean and variance across gridX. Select the acquisition function: Expected Improvement (EI) maximizes improvement over the current best separation efficiency; Probability of Improvement (PI) maximizes the probability of any improvement; Upper Confidence Bound (UCB) balances exploration and exploitation by computing mean + (scaling factor × variance); pure exploration maximizes predicted variance; pure exploitation maximizes predicted mean; epsilon-greedy randomly samples with probability epsilon or exploits with probability (1-epsilon). Identify the grid point with the highest acquisition function value and retrieve the corresponding unscaled gradient parameters as the proposal for the next experimental run.

## Related tools

- **scikit-learn** (Provides GaussianProcessRegressor for fitting mean and variance predictions; used to compute acquisition function values across the search space)
- **BAGO** (Implements the acquisition function dispatch and computeNextGradient() method that wraps acquisition function selection and returns the next gradient proposal) — https://github.com/huaxuyu/bago
- **bago (Python package)** (Provides programmatic support for acquisition function selection within the Bayesian optimization workflow) — https://github.com/huaxuyu/bago

## Examples

```
from bago import computeNextGradient; next_gradient = computeNextGradient(gpModel, scaledX, gridX, current_best_efficiency, acqFunc='ei')
```

## Evaluation signals

- The selected gradient point lies within gridX and its acquisition function value is strictly greater than or equal to all other grid points (greedy optimality).
- The returned unscaled gradient parameters are within the predefined bounds (e.g., flow rate, temperature, organic modifier range) specified at the start of optimization.
- Successive acquisition function selections produce a sequence that exhibits reduced redundancy (i.e., the same point is not proposed twice in a row unless the model has not been updated).
- Over the course of ≤10 runs, the maximum separation efficiency found increases monotonically or plateaus, indicating non-wasteful exploration.
- Comparison of acquisition functions on the same model shows that Expected Improvement and Probability of Improvement identify regions where mean+variance is high, while pure exploitation selects only the highest predicted mean, confirming functional differentiation.

## Limitations

- Acquisition function effectiveness depends on the quality and diversity of prior training data; if all prior gradients cluster in a subregion of parameter space, the GP model may be poorly calibrated elsewhere and acquisition proposals may be unreliable.
- The choice of acquisition function (EI, PI, UCB, etc.) is user-specified and not automated; misalignment between the user's intention (exploration vs. exploitation) and the chosen function can waste runs.
- The method assumes the GP model accurately captures the separation efficiency landscape; if the landscape is multimodal or noisy, the model may converge to a local optimum within 10 runs.
- Epsilon-greedy and other stochastic acquisition functions introduce variability in proposals; reproducibility may require fixing random seeds.
- The grid search space (gridX) must be pre-computed and finite; for very high-dimensional gradient spaces or continuous unbounded parameters, discretization or approximation strategies are required.

## Evidence

- [other] Acquisition function dispatch that proposes the next gradient: "How does BAGO select the next gradient proposal by applying an acquisition function to a fitted Gaussian Process model within the Bayesian optimization loop?"
- [methods] Expected Improvement selects points where improvement is maximized: "Expected Improvement (EI) selects points where expected improvement over current best is maximized"
- [methods] Probability of Improvement selects based on improvement probability: "Probability of Improvement (PI) selects where improvement is most probable"
- [methods] Upper Confidence Bound balances exploration and exploitation: "Upper Confidence Bound (UCB) balances exploration and exploitation"
- [methods] Pure exploration and exploitation strategies: "pure exploration maximizes predicted variance; pure exploitation maximizes predicted mean"
- [methods] Epsilon-greedy uses epsilon parameter for exploration proportion: "epsilon-greedy uses a parameter to determine the proportion of exploratory actions"
- [methods] Query GP model for mean and variance predictions: "Query the GP model to generate predicted mean and variance across the entire search space (gridX)"
- [methods] Identify highest acquisition function value: "Identify the grid point with the highest acquisition function value"
- [readme] BAGO enables acquisition function selection for efficiency: "Wonder why BAGO is efficient? Read more about acquisition functions"
