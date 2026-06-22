---
name: lc-ms-gradient-encoding-vector-representation
description: Use when when you have a set of candidate LC gradients (parameter combinations) that you wish to evaluate with a Gaussian process model, or when you need to convert raw gradient specifications into a standardized numerical format for Bayesian optimization acquisition function computation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - BAGO
  - pyopenms
  - scikit-learn
  - Python
  - bago
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

# LC-MS Gradient Encoding Vector Representation

## Summary

Encode liquid chromatography gradient parameters (e.g., solvent composition, flow rate, column properties) into numerical vectors suitable for input to machine learning models. This enables omics-scale evaluation of compound separation performance by transforming discrete gradient specifications into continuous feature spaces that Gaussian process regressors can consume.

## When to use

When you have a set of candidate LC gradients (parameter combinations) that you wish to evaluate with a Gaussian process model, or when you need to convert raw gradient specifications into a standardized numerical format for Bayesian optimization acquisition function computation. Use this skill before fitting a GP model or computing the next gradient proposal in an iterative optimization loop.

## When NOT to use

- Gradients have already been encoded or pre-processed by another tool (e.g., XCMS, MS-DIAL); re-encoding may introduce inconsistency.
- You are performing purely manual, non-iterative gradient selection and do not plan to fit a machine learning model.
- Your gradient parameters are categorical (e.g., 'acidic' vs. 'neutral' mobile phase) and require one-hot or ordinal encoding rather than continuous scaling.

## Inputs

- Gradient parameter specification (e.g., initial/final organic %, flow rate, gradient slope, column dimensions)
- Candidate gradient search space (matrix or list of parameter combinations)
- sklearn.preprocessing.StandardScaler fitted on prior gradient runs (optional, for consistency in later rounds)

## Outputs

- Standardized numerical gradient encoding vectors (shape: n_candidates × n_parameters)
- sklearn.preprocessing.StandardScaler object (for reuse in future optimization rounds)

## How to apply

Parse the gradient parameters (e.g., initial organic solvent percentage, flow rate, gradient slope, column length, particle size) from your experimental design or configuration file. Scale each parameter independently using sklearn.preprocessing.StandardScaler to normalize them to zero mean and unit variance across the candidate search space. This scaling ensures that all parameters contribute equally to the distance metrics and acquisition functions used by the Gaussian process. Retain the fitted scaler object so that new candidate gradients can be transformed consistently in subsequent optimization iterations. The resulting encoded vectors become the input X matrix for GP regression, with retention time-based separation efficiency metrics as the corresponding y output.

## Related tools

- **scikit-learn** (Provides StandardScaler for normalization of gradient parameter vectors before GP model input)
- **bago** (Python package that encapsulates gradient encoding and search space generation as part of the Bayesian optimization workflow) — https://github.com/huaxuyu/bago
- **pyopenms** (Used to read and parse raw LC-MS data files (mzML, mzXML) that provide context for gradient specification)

## Examples

```
from sklearn.preprocessing import StandardScaler; from bago import genSearchSpace; gradients = genSearchSpace(bounds={'init_organic': (5, 50), 'final_organic': (50, 95), 'flow_rate': (0.3, 0.5)}); scaler = StandardScaler(); X_encoded = scaler.fit_transform(gradients)
```

## Evaluation signals

- Encoded vectors have zero mean and unit variance across all parameters (check: mean ≈ 0, std ≈ 1 per column after scaling).
- Dimensionality of encoded matrix matches the number of gradient parameters being optimized (e.g., 4 columns for initial %, final %, flow rate, gradient slope).
- StandardScaler fit on training candidates correctly transforms held-out or new gradient candidates without data leakage or scale shift.
- Encoded vectors can be successfully passed to sklearn.gaussian_process.GaussianProcessRegressor.fit() without shape or dtype errors.
- Separation efficiency values computed on gradients corresponding to these encodings fall within the expected range (e.g., 0–1 normalized or 0–100% scale).

## Limitations

- Encoding quality depends on the choice and range of gradient parameters; missing parameters (e.g., column temperature) will not be captured and may limit model predictive power.
- StandardScaler assumes a Gaussian or at least symmetric distribution of parameters; highly skewed or multimodal parameter distributions may benefit from log-transformation or other preprocessing before scaling.
- Encoding does not capture non-linear interactions between gradient parameters; if synergistic effects exist (e.g., flow rate × column length), a higher-dimensional basis function or kernel may be needed.
- The article does not explicitly detail the number or list of gradient parameters used in BAGO; practitioners must determine which parameters are most relevant to their LC-MS platform.

## Evidence

- [other] Generate a search space of candidate gradients using parameter bounds, scaling inputs with sklearn StandardScaler.: "Generate a search space of candidate gradients using parameter bounds, scaling inputs with sklearn StandardScaler."
- [intro] Separation efficiency was defined to evaluate the performance of a gradient.: "Separation efficiency was defined to evaluate the performance of a gradient."
- [other] Fit a Gaussian process regression model to training data (gradient encodings as input, separation efficiency as output) using scikit-learn.: "Fit a Gaussian process regression model to training data (gradient encodings as input, separation efficiency as output) using scikit-learn."
- [readme] Wonder how omics-scale evaluation is achieved? Read more about encodings.: "Wonder how omics-scale evaluation is achieved? Read more about [encodings]."
- [readme] Model LC-MS experiment to evaluate compound separation performance: "Model LC-MS experiment to evaluate compound separation performance"
