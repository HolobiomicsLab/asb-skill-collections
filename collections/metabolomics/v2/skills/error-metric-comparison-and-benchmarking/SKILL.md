---
name: error-metric-comparison-and-benchmarking
description: Use when you have predicted retention times from one or more machine learning models (DNN, Gaussian Process, or ensemble) applied to small-molecule chromatography data, along with corresponding experimental ground-truth retention times, and need to quantify prediction accuracy and rank competing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
  tools:
  - alvaDesc
  - cmmrt (constantino-garcia/cmmrt)
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-022-00613-8
  all_source_dois:
  - 10.1186/s13321-022-00613-8
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# error-metric-comparison-and-benchmarking

## Summary

Evaluate retention time prediction models by computing mean absolute error (MAE) and median absolute error (MdAE) against ground-truth experimental values, then systematically compare these metrics across different approaches and calibration scenarios to establish competitive baselines and assess model robustness.

## When to use

You have predicted retention times from one or more machine learning models (DNN, Gaussian Process, or ensemble) applied to small-molecule chromatography data, along with corresponding experimental ground-truth retention times, and need to quantify prediction accuracy and rank competing methods or calibration strategies (e.g., 10-molecule vs. full-calibration approaches).

## When NOT to use

- Predicted and ground-truth retention times have not yet been computed or acquired; preprocessing and model inference steps must be completed first.
- The retention time dataset contains systematic biases or outliers that have not been assessed; error metrics require data quality assurance.
- Only a single prediction method is available and no baseline or alternative approach exists for comparison; benchmarking requires at least two methods.

## Inputs

- predicted retention times (vector or table with per-molecule predictions)
- ground-truth experimental retention times from reference dataset (METLIN SMRT or chromatography-specific database)
- metadata linking predictions and ground truth (compound identifiers, chromatographic method)

## Outputs

- mean absolute error (MAE) with confidence bounds (e.g., ±1.2 s)
- median absolute error (MdAE) with confidence bounds (e.g., ±0.9 s)
- tabulated error metrics comparing methods or calibration schemes
- error distributions or summary statistics per method for ranking

## How to apply

Calculate MAE and MdAE by comparing predicted retention times to experimental values from the METLIN small molecule dataset (SMRT) or analogous chromatography-retention-time datasets. Compute both metrics because MAE is sensitive to outliers while MdAE provides robustness; tabulate results with confidence intervals or standard deviations (e.g., MAE ± 1.2 s format). Compare error metrics across baseline approaches (e.g., previous projection methods) and the proposed method to verify that competitive error rates are maintained even under resource constraints (e.g., using only 10 calibration molecules). Report both point estimates and uncertainty bounds to enable statistical judgment of whether differences are clinically or practically meaningful.

## Related tools

- **alvaDesc** (generates molecular descriptors and fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) that serve as inputs to retention time prediction models whose outputs are later benchmarked) — https://www.alvascience.com/alvadesc/
- **cmmrt (constantino-garcia/cmmrt)** (implements DNN and Bayesian meta-learned GP models for retention time prediction and projection; error metrics are computed on model outputs) — https://github.com/constantino-garcia/cmmrt

## Examples

```
python -m cmmrt.rt.test_model --predictions predictions.csv --ground_truth experimental_rt.csv --output results/rt_cv.csv
```

## Evaluation signals

- MAE and MdAE values reported with explicit confidence intervals (e.g., 39.2±1.2 s, 17.2±0.9 s) and must fall within expected ranges documented in the article or README.
- Error metrics from the proposed method (e.g., 10-molecule Bayesian meta-learning) are statistically comparable to or better than baseline approaches (previous projection methods); differences should be quantified, not claimed qualitatively.
- MdAE is consistently lower than MAE, consistent with the expected robustness of median to outliers; large discrepancies may signal problematic outliers or heterogeneous error distributions.
- Error metrics computed on held-out or cross-validation folds are reproducible and match tabulated results in supplementary materials or repository outputs (e.g., CSV files in results/rt/ directory).
- Comparison is stratified by chromatographic method, calibration set size, or feature type (descriptors vs. fingerprints) to verify that competitive error rates hold across conditions, not just in aggregate.

## Limitations

- Error metrics (MAE, MdAE) are aggregated and do not reveal per-compound or per-method biases; visualization of residual distributions is needed to detect systematic over- or under-prediction.
- Confidence intervals depend on sample size and cross-validation strategy; sparse test sets (e.g., few molecules per chromatographic method) may yield wide bounds that obscure true differences between methods.
- Comparison to baseline methods requires that published error metrics from prior work are available and computed on the same or analogous datasets; mismatched datasets or evaluation protocols limit validity of benchmarking claims.
- The skill assumes ground-truth experimental retention times are accurate and representative; errors in reference data (e.g., undetected artifacts, instrument drift) propagate into error metrics and confound method comparison.

## Evidence

- [other] Evaluate projected retention times by calculating mean absolute error (MAE) and median absolute error (MdAE) against ground-truth experimental values.: "Evaluate projected retention times by calculating mean absolute error (MAE) and median absolute error (MdAE) against ground-truth experimental values."
- [other] Tabulate error metrics and compare against baseline projection approach results reported in the paper (expected MAE ~39.2±1.2 s, MdAE ~17.2±0.9 s).: "Tabulate error metrics and compare against baseline projection approach results reported in the paper (expected MAE ~39.2±1.2 s, MdAE ~17.2±0.9 s)."
- [intro] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s respectively: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [intro] A Bayesian meta-learning approach enables retention time projection between chromatographic methods from as few as 10 molecules while obtaining competitive error rates compared with previous approaches.: "A Bayesian meta-learning approach enables retention time projection between chromatographic methods from as few as 10 molecules while obtaining competitive error rates compared with previous"
- [readme] test_projections: Tests the performance of GP meta-training for computing projections between CMs. Four CMs of reference are used for the test: FEM long, LIFE old, FEM orbitrap plasma and RIKEN.: "Tests the performance of GP meta-training for computing projections between CMs. Four CMs of reference are used for the test: FEM long, LIFE old, FEM orbitrap plasma and RIKEN."
