---
name: gradient-space-optimization-search
description: Use when after fitting a Gaussian Process regression model to prior LC-MS gradient runs (retention times, separation efficiency scores, or compound identification counts).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - scikit-learn
  - BAGO
  - Python
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1101/2023.09.08.556930
  title: BAGO
- doi: 10.1002/9780470508183
  title: ''
evidence_spans:
- a :class:`sklearn.preprocessing.StandardScaler` object used to scale the data
- a :class:`sklearn.gaussian_process.GaussianProcessRegressor` object
- BAGO is a Bayesian optimization strategy for LC gradient optimization for MS-based small molecule analysis
- A :class:`ms1Spectrum` object (supported by :mod:`bago`)
- Download and install Python 3.8 or later from `python.org`
- model.computeNextGradient()
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

# Reconstruct the acquisition-function dispatch that proposes the next gradient

## Summary

This skill applies Bayesian optimization acquisition functions (Expected Improvement, Probability of Improvement, Upper Confidence Bound, and exploration/exploitation variants) to a fitted Gaussian Process model to select the next LC gradient proposal. It is used to efficiently navigate the gradient parameter space and converge on optimal separation conditions within ~10 experimental runs.

## When to use

Apply this skill after fitting a Gaussian Process regression model to prior LC-MS gradient runs (retention times, separation efficiency scores, or compound identification counts). Use it when you need to propose the next gradient to test in an active Bayesian optimization loop, particularly when your goal is to maximize separation efficiency or omics-scale compound detection within a limited budget of experimental runs.

## When NOT to use

- Do not use this skill before fitting a Gaussian Process model; first collect and fit initial gradient runs.
- Do not apply this skill if your gradient parameter space is already fully explored or if you have already converged to a satisfactory optimum (no significant improvement expected).
- Do not use this skill if your input gridX is extremely sparse or does not adequately cover the feasible gradient domain; re-generate the search space first.

## Inputs

- Trained Gaussian Process regression model (gpModel object with fitted hyperparameters)
- Scaled training data (scaledX: feature matrix of prior gradient runs)
- Grid search space (gridX: discretized gradient parameter domain, scaled)
- Model uncertainty estimates (mean and variance predictions from GP across gridX)
- Acquisition function parameter (acqFunc: one of 'ei', 'pi', 'ucb', 'eps', 'explore', 'exploit', 'rand')
- Current best separation efficiency or objective value (for EI/PI computation)
- Epsilon value (for epsilon-greedy; proportion of exploratory actions)

## Outputs

- Next proposed gradient parameter vector (unscaled, in original gradient space)
- Acquisition function value at the selected point
- Grid point index identifying the selected location in gridX

## How to apply

Retrieve the trained Gaussian Process model object (gpModel) with fitted parameters, scaled training data (scaledX), and a grid-discretized search space (gridX) covering the gradient parameter domain. Query the GP to generate predicted mean and variance across gridX. Select and apply your chosen acquisition function: Expected Improvement (EI) maximizes expected gain over the current best-observed separation efficiency; Probability of Improvement (PI) maximizes the probability of any improvement; Upper Confidence Bound (UCB) balances exploration and exploitation using mean + (scaling_factor × variance); epsilon-greedy randomly explores with probability epsilon or exploits with probability (1 − epsilon); pure exploration maximizes predicted variance; pure exploitation maximizes predicted mean. Identify the grid point with the highest acquisition function value, retrieve its unscaled gradient parameters, and return as the next proposed gradient. The choice of acquisition function controls exploration vs. exploitation trade-off: EI and PI are conservative; UCB offers tunable balance; pure exploration is used early in optimization to map the space; pure exploitation is used when converging on a known promising region.

## Related tools

- **BAGO** (Bayesian optimization framework that encapsulates GP fitting, acquisition function dispatch, and gradient proposal; provides both Python package and Windows GUI for LC gradient optimization) — https://github.com/huaxuyu/bago
- **scikit-learn** (Provides Gaussian Process regression (GaussianProcessRegressor) for fitting the predictive model and StandardScaler for feature scaling) — https://scikit-learn.org
- **Python** (Programming language runtime for implementing and executing the acquisition function dispatch logic within Jupyter Notebook or standalone scripts) — https://python.org

## Examples

```
# After fitting GP model and generating gridX, select next gradient via EI
from bago.acquisition import expected_improvement
acq_values = expected_improvement(gpModel, gridX, current_best)
next_idx = np.argmax(acq_values)
next_gradient = gridX[next_idx]  # Unscaled gradient parameters
```

## Evaluation signals

- The selected grid point has the highest (or near-highest) acquisition function value across the entire gridX domain for the chosen acqFunc.
- The returned gradient parameters are unscaled and lie within the original feasible gradient space (e.g., 0–100% organic solvent, valid time intervals).
- Successive acquisition-function calls with an updated GP model (after observing the new gradient's performance) propose different gradients that explore or exploit regions consistent with the GP's updated belief.
- Over a sequence of Bayesian optimization iterations, the observed best separation efficiency increases monotonically or plateaus near a known optimal region, demonstrating effective search progression.
- When acqFunc='explore' or 'eps' with high epsilon, the predicted variance at selected points is high (uncertainty-driven); when acqFunc='exploit', the predicted mean is high (confidence-driven).

## Limitations

- Acquisition function performance depends critically on the quality of the fitted GP model; poor model fit or insufficient training data can lead to suboptimal proposals.
- The discrete grid approximation of the search space may miss finer-grained optima between grid points; finer grids increase computational cost.
- Epsilon-greedy and pure exploration strategies may propose uninformative gradients early in optimization, delaying convergence compared to information-theoretic methods like EI or PI.
- The method assumes the objective function (separation efficiency, identification count) is smooth and well-modeled by a Gaussian Process; abrupt discontinuities or multi-modal landscapes may not be well-captured.
- No changelog or versioning notes are provided in the public repository documentation, making it difficult to track long-term evolution of acquisition function implementations.

## Evidence

- [other] BAGO implements multiple acquisition functions to propose the next gradient: Expected Improvement (EI) selects points where expected improvement over current best is maximized; Probability of Improvement (PI) selects where improvement is most probable; Upper Confidence Bound (UCB) balances exploration and exploitation; pure exploration maximizes predicted variance; pure exploitation maximizes predicted mean; and epsilon-greedy uses a parameter to determine the proportion of exploratory actions.: "BAGO implements multiple acquisition functions to propose the next gradient: Expected Improvement (EI) selects points where expected improvement over current best is maximized; Probability of"
- [readme] Find an optimal gradient for your LC-MS/MS analysis within 10 runs.: "Find an optimal gradient for your LC-MS/MS analysis within 10 runs."
- [other] For EI, compute expected improvement over current best; for PI, compute probability of improvement; for UCB, compute upper confidence bound using mean + (scaling factor × variance); for epsilon-greedy, randomly sample with probability epsilon or exploit with probability (1-epsilon); for pure exploration, maximize variance; for pure exploitation, maximize mean.: "For EI, compute expected improvement over current best; for PI, compute probability of improvement; for UCB, compute upper confidence bound using mean + (scaling factor × variance); for"
- [other] Receive a trained gpModel object with fitted Gaussian process regression, scaled training data (scaledX), grid search space (gridX), and model uncertainty estimates (mean and variance predictions).: "Receive a trained gpModel object with fitted Gaussian process regression, scaled training data (scaledX), grid search space (gridX), and model uncertainty estimates (mean and variance predictions)."
- [other] Identify the grid point with the highest acquisition function value. Retrieve the corresponding unscaled gradient from gridX and return as output.: "Identify the grid point with the highest acquisition function value. Retrieve the corresponding unscaled gradient from gridX and return as output."
- [readme] Wonder why BAGO is efficient? Read more about acquisition functions.: "Wonder why BAGO is efficient? Read more about acquisition functions."
