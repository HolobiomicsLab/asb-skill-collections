---
name: separation-efficiency-calculation-from-retention-times
description: Use when you have extracted retention times from MS1 spectra for top signals in a single LC-MS/MS run and need to evaluate whether that gradient's separation performance is sufficient, or when you are building the objective function for an iterative gradient optimization loop where each candidate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
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

# separation-efficiency-calculation-from-retention-times

## Summary

Computes a scalar metric of LC gradient performance by quantifying compound separation efficiency across retention times detected in MS1 data. This metric serves as the objective function in Bayesian optimization to iteratively identify optimal LC gradients for untargeted MS analysis.

## When to use

Apply this skill when you have extracted retention times from MS1 spectra for top signals in a single LC-MS/MS run and need to evaluate whether that gradient's separation performance is sufficient, or when you are building the objective function for an iterative gradient optimization loop where each candidate gradient must be scored on a single metric before proposing the next gradient to test.

## When NOT to use

- When you have fewer than 3–5 resolved top signals in MS1 data; insufficient spacing information makes efficiency estimation unreliable.
- When the goal is method development on a known, fixed gradient; this skill is for optimization loops, not single-run characterization.
- When compounds are not well-separated by retention time (e.g., coelution dominates); separation efficiency will not discriminate between gradients meaningfully.

## Inputs

- ms1Spectrum objects (collection of MS1 scans from a single LC-MS/MS run)
- gradient parameters (encoded as numerical vector via standardscaler normalization)
- retention time list (from top signals in MS1 data)
- raw LC-MS data file (mzML or mzXML format)

## Outputs

- separation efficiency score (scalar; numerical measure of compound separation performance)
- retention time intervals (list of gaps between consecutive top-signal retention times)
- (x, y) training pair for Gaussian process: (encoded gradient, efficiency score)

## How to apply

After running an LC-MS/MS experiment with a candidate gradient, extract all MS1 scans into ms1Spectrum objects and identify the top signals (e.g., top N peaks by intensity). From these signals, collect their retention times. Compute separation efficiency by measuring the spacing (time gaps) between consecutive retention times of the top signals—typically averaging or summing these intervals to produce a single scalar that reflects how well compounds are spread across the gradient window. This efficiency score then becomes the y-value in the Gaussian process model: paired with the encoded gradient parameters (x-value), it trains the model to predict which untested gradients will yield better separation. Higher separation efficiency indicates better resolution and is the quantity that Bayesian acquisition functions (Expected Improvement, etc.) use to propose the next gradient point.

## Related tools

- **pyopenms** (Load raw LC-MS data (mzML/mzXML) and extract MS1/MS2 spectra into Spectrum objects for retention time and intensity querying)
- **bago** (Compute separation efficiency from retention times via sepEfficiency() function; integrate efficiency scores into the Bayesian optimization loop) — https://github.com/huaxuyu/bago
- **scikit-learn** (Fit Gaussian process regression model to (encoded gradient, efficiency) pairs and predict performance of candidate gradients)
- **Python** (Scripting environment for implementing the efficiency calculation and Bayesian optimization workflow)

## Examples

```
from bago import sepEfficiency; efficiency = sepEfficiency(retention_times=[2.5, 5.1, 8.3, 12.7, 18.2])
```

## Evaluation signals

- Separation efficiency score is a positive scalar (>0) and increases monotonically (or at least does not decrease) with better gradient spacing of top signals.
- Retention time intervals are strictly positive and sorted in ascending order of retention time; no gaps are negative or out-of-order.
- When compared across successive runs in the optimization loop, the efficiency score from the proposed gradient (via acquisition function) should be higher than the previous best observed efficiency, or the Gaussian process confidence interval should be tight around the prediction.
- The encoded gradient parameters (input to the GP model) and efficiency scores (output) form a balanced training set with no duplicate or trivial (zero-efficiency) entries.
- Gaussian process model converges within 10 runs: the best efficiency observed by run 10 should be within ~10–20% of the theoretical maximum separation achievable for the sample.

## Limitations

- Separation efficiency metric depends critically on definition of 'top signals'—if the threshold for signal selection is too loose, noisy minor peaks inflate spacing; if too strict, genuine peaks are missed.
- The metric assumes that maximizing retention time spacing uniformly improves identification and quantification, but does not directly measure mass accuracy, MS2 signal intensity, or chemical class coverage.
- Works best for small-molecule untargeted analysis; may not generalize to lipids, peptides, or other analyte classes with different ionization or retention behavior.
- Separation efficiency is a univariate summary; it discards information about peak width, asymmetry, and resolution that might matter for specific analytes.
- The metric is local to a single LC column, sample, and MS instrument configuration; transfer to different hardware or sample types requires re-optimization.

## Evidence

- [intro] Separation efficiency was defined to evaluate the performance of a gradient.: "Separation efficiency was defined to evaluate the performance of a gradient."
- [methods] Find top signals in MS1 data and compute separation efficiency (retention time spacing metric) for the initial gradient run.: "Find top signals in MS1 data and compute separation efficiency (retention time spacing metric) for the initial gradient run."
- [methods] Calculate the separation efficiency using a series of retention times: "Calculate the separation efficiency using a series of retention times"
- [methods] Fit a Gaussian process regression model to training data (gradient encodings as input, separation efficiency as output) using scikit-learn.: "Fit a Gaussian process regression model to training data (gradient encodings as input, separation efficiency as output) using scikit-learn."
- [methods] Repeat steps 2–5 for successive runs, updating the model with new MS data from each gradient trial, until reaching the stopping criterion (≤10 runs or convergence).: "Repeat steps 2–5 for successive runs, updating the model with new MS data from each gradient trial, until reaching the stopping criterion (≤10 runs or convergence)."
- [methods] Separation efficiency was defined to evaluate omics-scale compound separation performance: "Separation efficiency was defined to evaluate omics-scale compound separation performance"
