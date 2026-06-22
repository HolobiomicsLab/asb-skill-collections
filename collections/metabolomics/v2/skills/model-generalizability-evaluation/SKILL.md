---
name: model-generalizability-evaluation
description: Use when you have a pre-trained or newly retrained graph neural network for collision cross section prediction and need to measure whether its performance generalizes across different molecular datasets (e.g., training on METLIN but evaluating on CCSBase).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3675
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - train-test.py
  - Makefile
  - Mol2CCS wrapper functions
  - reproduce_figures notebooks
derived_from:
- doi: 10.1186/s13321-024-00899-w
  title: mol2ccs
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
---

# model-generalizability-evaluation

## Summary

Evaluate the generalizability of a trained graph neural network model by computing regression performance metrics (MAE, R², etc.) on held-out validation or test datasets with different data distributions. This skill assesses whether a model trained on one collision cross section dataset maintains predictive accuracy when applied to structurally or source-diverse validation sets.

## When to use

Apply this skill when you have a pre-trained or newly retrained graph neural network for collision cross section prediction and need to measure whether its performance generalizes across different molecular datasets (e.g., training on METLIN but evaluating on CCSBase). Use it specifically when comparing train–test splits with different data sources, molecular composition, or ion types to quantify real-world applicability.

## When NOT to use

- Model has not been trained or fine-tuned on any dataset; evaluation requires a fitted model.
- Validation dataset is in a non-standard format (not parquet) or missing required columns (smiles, adduct, ccs reference values).
- You are evaluating model performance only within the same dataset used for training; generalizability specifically requires held-out or cross-source validation.

## Inputs

- pre-trained graph neural network model (.h5 format)
- validation/test dataset (parquet file with columns: smiles, coordinates, adduct, ccs)
- model hyperparameters and training configuration (JSON)
- training pipeline script or Makefile commands

## Outputs

- regression performance metrics file (MAE, R², MSE, correlation coefficients)
- prediction CSV/dataframe with predicted vs. reference CCS values
- generalizability assessment report comparing cross-dataset performance

## How to apply

Load the pre-trained GNN model (or retrain using provided training pipeline and hyperparameters) and the validation/test dataset in the repository's parquet format, specifying column names for SMILES, 3D coordinates (if available), adduct type, and reference CCS values. Generate predictions on the validation set using the trained model. Compute standard regression metrics (mean absolute error, R², mean squared error, or correlation coefficients) comparing predicted CCS values to reference values. Save results to a metrics file and interpret generalizability by comparing performance across datasets with different distributions; poor performance on a held-out dataset indicates limited generalizability. Use manual expert review to validate that metrics are reasonable relative to reported literature values.

## Related tools

- **train-test.py** (Python script for training GNN models and generating predictions on test sets with configurable parameters (dropout, epochs, input/output file paths)) — https://github.com/enveda/ccs-prediction
- **Makefile** (Defines standardized train–test commands (e.g., make train-metlin-test-metlin) that execute training and evaluation workflows with consistent parameter sets) — https://github.com/enveda/ccs-prediction
- **Mol2CCS wrapper functions** (Provides train_and_predict() interface for custom model training and CCS prediction on new datasets) — https://github.com/enveda/ccs-prediction/blob/main/mol2ccs/train_and_predict.py
- **reproduce_figures notebooks** (Jupyter notebooks demonstrating how to load predictions and compute metrics to reproduce published results and figures) — https://github.com/enveda/ccs-prediction/tree/main/notebooks/reproduce_figures

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5" --coordinates-column-name "coordinates" --coordinates-present --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --dropout-rate 0.1 --epochs 400
```

## Evaluation signals

- Computed metrics (MAE, R², MSE) match or closely approximate published values reported in Engler et al. (2024) for the same train–test dataset pair.
- Performance degrades predictably when evaluating a model trained on METLIN against CCSBase or vice versa, reflecting genuine cross-dataset generalization gaps rather than data loading errors.
- Prediction CSV contains no NaN or infinite values; predicted CCS values fall within physiologically reasonable ranges (typically 50–300 Ų for small molecules).
- Metrics file is parseable and contains all expected fields (MAE, R², MSE, count of predictions); no truncation or partial output.
- Manual expert review confirms that reported generalizability conclusions (e.g., good/poor generalization) are consistent with metric magnitudes and literature precedent.

## Limitations

- Model generalizability depends critically on the quality, size, and representativeness of training and validation datasets; small or biased training sets limit transferability.
- Pre-trained models require 3D coordinates or SMILES; if coordinates are unavailable, the model must generate them internally, which introduces additional computational and potential accuracy overhead.
- Evaluation metrics (MAE, R²) assume regression on a continuous CCS variable; they do not directly capture failure modes on rare or out-of-distribution molecular structures.
- The repository's README notes that users must download raw METLIN and CCSBase databases themselves and format them according to notebook specifications; data path and format mismatches are common sources of evaluation failure.

## Evidence

- [other] Can graph neural networks trained and evaluated using the enveda ccs-prediction repository code and data reproduce the reported collision cross section prediction performance metrics?: "Can graph neural networks trained and evaluated using the enveda ccs-prediction repository code and data reproduce the reported collision cross section prediction performance metrics?"
- [other] Load the deposited training and validation datasets according to the repository's data format specifications. Load the pre-trained graph neural network model or retrain it using the provided training pipeline and hyperparameters. Generate collision cross section predictions on the validation or test set. Compute reported performance metrics (e.g., mean absolute error, R², or other regression statistics) and save results to a metrics file.: "Load the deposited training and validation datasets according to the repository's data format specifications. Load the pre-trained graph neural network model or retrain it using the provided training"
- [readme] poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5" --coordinates-column-name "coordinates" --coordinates-present --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --dropout-rate 0.1 --epochs 400: "poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet""
- [readme] Train the model based on your own training dataset with [wrapper_train] and predict with [wrapper_predict] function.: "Train the model based on your own training dataset with [wrapper_train] and predict with [wrapper_predict] function."
- [intro] Evaluating the generalizability of graph neural networks for predicting collision cross section: "Evaluating the generalizability of graph neural networks for predicting collision cross section"
