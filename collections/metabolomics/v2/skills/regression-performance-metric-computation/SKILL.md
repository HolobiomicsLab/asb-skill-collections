---
name: regression-performance-metric-computation
description: Use when after generating collision cross section predictions on a validation or test set using a trained graph neural network model, and you need to quantify prediction accuracy and compare against reported performance metrics in the literature or prior experimental runs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3361
  tools:
  - train-test.py
  - sklearn.metrics
  - reproduce_figures notebooks
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1186/s13321-024-00899-w
  title: mol2ccs
- doi: 10.5281/zenodo.11199061
  title: ''
- doi: 10.5281/zenodo.11199061.svg
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mol2ccs_cq
    doi: 10.1186/s13321-024-00899-w
    title: mol2ccs
  dedup_kept_from: coll_mol2ccs_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00899-w
  all_source_dois:
  - 10.1186/s13321-024-00899-w
  - 10.5281/zenodo.11199061
  - 10.5281/zenodo.11199061.svg
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# regression-performance-metric-computation

## Summary

Compute standard regression performance metrics (mean absolute error, R², and other statistics) on model predictions against ground-truth labels to quantify generalizability of graph neural network collision cross section predictions. This skill validates whether a trained model reproduces reported performance benchmarks.

## When to use

After generating collision cross section predictions on a validation or test set using a trained graph neural network model, and you need to quantify prediction accuracy and compare against reported performance metrics in the literature or prior experimental runs.

## When NOT to use

- Predictions have not yet been generated on the test set—first run the model inference step.
- Test set labels are missing or misaligned with predictions (shape or index mismatch).
- You are evaluating classification performance rather than regression—use classification metrics (accuracy, F1, ROC-AUC) instead.

## Inputs

- predicted_ccs_values (numeric array or column from predictions file)
- ground_truth_ccs_values (numeric column from test/validation dataset parquet file)
- test_set_metadata (dataset identifiers, e.g., 'ccsbase_3d.parquet', 'metlin_train_3d.parquet')

## Outputs

- metrics_file (JSON or CSV with MAE, R², and other regression statistics)
- performance_summary (structured record of metric names and values for comparison against reported benchmarks)

## How to apply

Load the model's predicted collision cross section values and the corresponding ground-truth CCS values from the test or validation dataset (typically stored in parquet format with columns like 'ccs' for ground truth and prediction output). Compute mean absolute error (MAE), R² (coefficient of determination), and any other regression statistics reported in the paper. Save the computed metrics to a structured output file (e.g., JSON or CSV) that records the metric names, values, and optionally dataset split metadata (train set, test set). The rationale is that regression metrics on held-out data directly measure model generalizability across different CCS databases (e.g., training on METLIN and testing on CCSBase reveals cross-database performance).

## Related tools

- **train-test.py** (Generates predictions and can optionally compute metrics; orchestrates model evaluation workflow) — https://github.com/enveda/ccs-prediction
- **sklearn.metrics** (Python library providing mean_absolute_error, r2_score, and other regression metric functions)
- **reproduce_figures notebooks** (Jupyter notebooks that compute and visualize performance metrics for manuscript figures) — https://github.com/enveda/ccs-prediction/tree/main/notebooks/reproduce_figures

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5" --ccs-column-name "ccs" --dropout-rate 0.1 --epochs 400
```

## Evaluation signals

- Computed metrics match or closely reproduce the values reported in Engler et al. (2024) for each train/test dataset pair (e.g., 'train-metlin-test-ccsbase').
- Metrics file contains all expected fields: metric name (e.g., 'MAE', 'R2'), numeric value, and dataset split identifiers.
- R² is in range [−∞, 1] and MAE is non-negative; for good models on CCS prediction, R² should be > 0.8 and MAE should be < ~5 Ų (depending on database and adduct).
- Predictions and ground-truth arrays have matching lengths and no NaN/inf values in metric computation.
- Cross-database generalization comparison: metrics for 'train-metlin-test-ccsbase' should be interpretable as a measure of domain shift (expected to be worse than same-database splits).

## Limitations

- Metrics are sensitive to data preprocessing and normalization; ensure training and test sets are processed identically (coordinates present/absent, SMILES canonicalization, adduct encoding).
- R² can be misleading if the test set distribution differs significantly from training (cross-database evaluation may show lower R² even if model is sound).
- No single metric fully captures generalizability; MAE and R² should be reported together with residual analysis and per-adduct or per-molecular-weight-bin breakdowns (see reproduce_figures notebooks).
- Pre-trained model weights and hyperparameters (dropout=0.1, epochs=400) must match those used to generate reported metrics; using different hyperparameters will produce non-comparable results.

## Evidence

- [other] Compute reported performance metrics (e.g., mean absolute error, R², or other regression statistics) and save results to a metrics file.: "Compute reported performance metrics (e.g., mean absolute error, R², or other regression statistics) and save results to a metrics file."
- [readme] Predictions are available and can be directly downloaded from [...] The files should be unzipped and placed in the `data` directory.: "Predictions are available and can be directly downloaded from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11199061.svg)](https://doi.org/10.5281/zenodo.11199061). The files should be unzipped"
- [readme] Run the notebooks located in the `notebooks` corresponding to each analysis. [...] reproduce_figures: the name of the notebooks indicates which notebook can reproduce which figures of the manuscript: "Run the notebooks located in the `notebooks` corresponding to each analysis. [...] reproduce_figures: the name of the notebooks indicates which notebook can reproduce which figures"
- [readme] prefix is used to generate the output files of the predictions of the test set: "prefix is used to generate the output files of the predictions of the test set"
