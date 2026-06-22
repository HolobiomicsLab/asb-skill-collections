---
name: lc-gradient-vector-encoding-and-decoding
description: Use when when preparing LC gradient configurations for Bayesian optimization, or when converting predicted optimal vectors back into actionable LC instrument parameters. Specifically, use this skill when you have a set of gradient parameters to optimize (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0091
  tools:
  - scikit-learn
  - BAGO
  - Python
  - bago Python package
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-gradient vector encoding and decoding

## Summary

Converts between human-readable LC gradient parameters (e.g., flow rate, solvent composition, temperature profiles) and normalized numerical vectors suitable for Bayesian optimization and Gaussian Process regression. This bidirectional transformation enables efficient exploration of high-dimensional gradient space while preserving chemical interpretability.

## When to use

When preparing LC gradient configurations for Bayesian optimization, or when converting predicted optimal vectors back into actionable LC instrument parameters. Specifically, use this skill when you have a set of gradient parameters to optimize (e.g., initial/final %B, flow rate, column temperature) and need to represent them as scaled numeric vectors for GP model training, or conversely when a BO acquisition function has proposed a point in normalized vector space and you need to retrieve the corresponding unscaled gradient parameters for experimental execution.

## When NOT to use

- Input is already a validated, experiment-ready gradient configuration and no optimization is planned.
- Gradient parameters follow categorical or nominal logic (e.g., column choice, detector type) rather than continuous numeric ranges.
- Search space bounds are not well-defined or parameters have non-standard units that cannot be normalized consistently.

## Inputs

- Raw gradient parameter set (e.g., dict or structured object with %B_initial, %B_final, flow_rate, temperature, etc.)
- Parameter bounds and units (lower/upper limits for each dimension)
- Fitted scaler object (sklearn.preprocessing.StandardScaler or equivalent) from training data
- Grid search space (gridX) or predicted vector from acquisition function

## Outputs

- Encoded vector (normalized numeric array, typically shape (n_parameters,), scaled to 0–1 range)
- Decoded gradient parameters (human-readable dict or object with original units and physical meaning)
- Scaler/transformer object (for reproducible forward and inverse transformations)

## How to apply

First, define the bounds and units for each gradient parameter (e.g., %B solvent composition from 5–95%, flow rate in mL/min, temperature in °C). Encode gradient configurations into scaled numeric vectors by normalizing each parameter to a standard range (typically 0–1) using min-max scaling or similar transformation; store the scaler object for later inversion. Use these encoded vectors as inputs to the GP model and search space generation (genSearchSpace). When the acquisition function identifies a promising point in vector space, retrieve the corresponding unscaled gradient by applying the inverse transformation, then validate that decoded parameters fall within physically meaningful instrument limits before proposing them as the next experimental run. The encoding scheme should preserve the chemical semantics of the parameter space (e.g., solvent composition as continuous, not categorical).

## Related tools

- **scikit-learn** (Provides StandardScaler for normalizing gradient parameters to 0–1 range and inverse transformation to recover original units)
- **BAGO** (Bayesian optimization framework that accepts encoded gradient vectors and returns acquisition-function-selected proposals as normalized vectors) — https://github.com/huaxuyu/bago/
- **bago Python package** (Implements genSearchSpace and fit functions that operate on encoded gradient vectors within the BO workflow) — https://github.com/huaxuyu/bago

## Examples

```
from sklearn.preprocessing import StandardScaler; import numpy as np; scaler = StandardScaler(); gradient_raw = np.array([[10, 90, 0.6, 30], [5, 95, 0.4, 25]]); gradient_encoded = scaler.fit_transform(gradient_raw); gradient_decoded = scaler.inverse_transform(gradient_encoded)
```

## Evaluation signals

- Encoded vectors lie within [0, 1] for all dimensions and are reproducible (same input → same output after scaler initialization).
- Decoded parameters match original input values within numeric precision (e.g., < 1e-6 relative error) when scaler is applied and inverted.
- Decoded parameters respect original bounds: %B_initial ≥ min_B and ≤ max_B, flow_rate ≥ min_flow, temperature ≥ min_temp, etc.
- Encoding/decoding is consistent across multiple BO iterations: vectors proposed by the acquisition function decode to valid, distinct gradient configurations.
- Scaler object state (mean, scale) is consistent and documented so that new test vectors can be encoded/decoded without drift.

## Limitations

- Encoding assumes parameter ranges are known and fixed a priori; dynamic or data-driven bounds are not explicitly addressed in the source material.
- Non-linear parameter relationships or unit conversions (e.g., temperature-dependent viscosity effects) are not captured by simple linear scaling; domain knowledge may be needed to encode coupled parameters correctly.
- The source article does not provide explicit guidance on handling ordinal or categorical parameters (e.g., column chemistry); continuous-only encoding is implied.
- Scaler object must be saved and versioned alongside trained GP models to ensure reproducibility across BO iterations and experiments.

## Evidence

- [methods] Receive a trained gpModel object with fitted Gaussian process regression, scaled training data (scaledX), grid search space (gridX), and model uncertainty estimates: "Receive a trained gpModel object with fitted Gaussian process regression, scaled training data (scaledX), grid search space (gridX), and model uncertainty estimates (mean and variance predictions)."
- [methods] Function to fit the data to Gaussian process regression model: "genSearchSpace - generate search space for Gaussian process model"
- [methods] a :class:`sklearn.preprocessing.StandardScaler` object: "a :class:`sklearn.preprocessing.StandardScaler` object"
- [methods] Retrieve the corresponding unscaled gradient from gridX and return as output: "Retrieve the corresponding unscaled gradient from gridX and return as output."
- [readme] Omics-scale evaluation on compound separation - Separation efficiency was defined to evaluate the performance of a gradient: "Wonder how omics-scale evaluation is achieved? Read more about [encodings]"
