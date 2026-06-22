---
name: gaussian-process-uncertainty-quantification
description: Use when after collecting observed separation efficiency scores at sampled gradient conditions and you need to propose the next gradient to evaluate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3173
  tools:
  - scikit-learn
  - BAGO
  - Python
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
---

# gaussian-process-uncertainty-quantification

## Summary

Fit a Gaussian Process regression model to observed LC-MS gradient performance data and generate mean and variance predictions across a continuous search space to quantify prediction uncertainty. This uncertainty estimate directly enables acquisition function selection and drives the efficiency of Bayesian optimization for gradient discovery.

## When to use

After collecting observed separation efficiency scores at sampled gradient conditions and you need to propose the next gradient to evaluate. The Gaussian Process model and its uncertainty bounds are required inputs to all downstream acquisition functions (EI, PI, UCB, epsilon-greedy) used to select the next gradient point in the Bayesian optimization loop.

## When NOT to use

- Input data has not yet been scaled; Gaussian Process fitting requires normalized features to perform well—scale training data first using StandardScaler or equivalent.
- Fewer than 2 observations are available; Gaussian Process regression requires sufficient data to estimate hyperparameters and covariance structure meaningfully.
- The search space is discrete and very small (< 10 candidate points); grid-based uncertainty quantification becomes inefficient relative to simple exhaustive search.
- Separation efficiency observations contain missing values or are non-numeric; imputation and validation are prerequisite steps.

## Inputs

- Fitted Gaussian Process regression model object (gpModel)
- Scaled training data with observations (scaledX, y_observed)
- Grid search space of candidate gradients (gridX, unscaled)
- User-specified acquisition function parameter (acqFunc: ei, pi, ucb, eps, explore, exploit)

## Outputs

- Predicted mean across search space (array, shape = len(gridX))
- Predicted variance across search space (array, shape = len(gridX))
- Next gradient point proposal (unscaled gradient vector)

## How to apply

Receive scaled training data (scaledX) with corresponding separation efficiency observations and a pre-fitted Gaussian Process regression model. Query the fitted model across the entire grid search space (gridX) to generate predicted mean and variance for each candidate gradient point. The model's posterior variance at each point estimates epistemic uncertainty—regions with high variance indicate points where the model is most uncertain and may offer high information gain. These predictions serve as the foundation for acquisition function evaluation: Expected Improvement computes improvement over the current best using both mean and variance; Upper Confidence Bound balances exploitation (mean) and exploration (variance); pure exploration maximizes variance directly. Verify that variance is highest in underexplored regions and decreases near observed data points, consistent with standard Gaussian Process behavior.

## Related tools

- **scikit-learn** (Provides GaussianProcessRegressor class and StandardScaler for fitting GP models and scaling training data prior to model fitting.)
- **BAGO** (Orchestrates the full Bayesian optimization workflow, invoking Gaussian Process fitting and uncertainty quantification within each iteration of gradient optimization.) — https://github.com/huaxuyu/bago/
- **Python** (Programming language environment for implementing Gaussian Process model fitting and prediction.)

## Examples

```
from sklearn.gaussian_process import GaussianProcessRegressor; from sklearn.preprocessing import StandardScaler; scaler = StandardScaler(); scaledX = scaler.fit_transform(X_train); gp = GaussianProcessRegressor(); gp.fit(scaledX, y_efficiency); mean, std = gp.predict(scaler.transform(gridX), return_std=True)
```

## Evaluation signals

- Predicted variance at training data points is near zero (or minimal); variance increases monotonically away from observed points.
- Predicted mean passes through or near observed training targets; residuals are small and unbiased.
- Variance estimates are positive definite and bounded within a reasonable range reflecting model confidence.
- For a grid of test points, variance is highest in unexplored regions of the gradient space and lowest in heavily sampled regions.
- Acquisition function values (EI, UCB, PI, etc.) computed from these predictions rank candidate points consistently with manual inspection of mean-variance tradeoffs.

## Limitations

- Gaussian Process assumes a smooth underlying function; discontinuous or highly nonlinear separation efficiency landscapes may be poorly modeled.
- Computational cost scales cubically with the number of training observations; >1000 observed gradients may require sparse GP approximations.
- Choice of kernel and hyperparameters significantly affects uncertainty estimates; misspecified priors or fixed hyperparameters can yield overconfident predictions.
- Extrapolation beyond the convex hull of observed data may produce unreliable variance estimates; predictions at extreme gradient points should be interpreted with caution.

## Evidence

- [methods] Workflow step 3: Query the GP model: "Query the GP model to generate predicted mean and variance across the entire search space (gridX)."
- [methods] Acquisition function foundation: "for EI, compute expected improvement over current best; for PI, compute probability of improvement; for UCB, compute upper confidence bound using mean + (scaling factor × variance); for"
- [readme] Integration with Bayesian optimization: "BAGO covers the proposed features needed in creating a gradient optimization workflow based on Bayesian optimization."
- [readme] Separation efficiency metric: "Separation efficiency was defined to evaluate the performance of a gradient."
- [readme] Efficiency claim grounded in acquisition: "Find an optimal gradient for your LC-MS/MS analysis within 10 runs. Wonder why BAGO is efficient? Read more about [acquisition functions]."
