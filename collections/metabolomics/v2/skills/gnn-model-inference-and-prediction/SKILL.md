---
name: gnn-model-inference-and-prediction
description: Use when you have a pre-trained GNN model checkpoint, a test dataset
  with molecular representations (SMILES, 3D coordinates, adducts) and ground-truth
  labels, and need to quantify how well the model generalizes to held-out data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_3372
  tools:
  - enveda/ccs-prediction repository (model code and pre-trained weights)
  - PyTorch Geometric
  - enveda/ccs-prediction
  - train_and_predict.py
  techniques:
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-024-00899-w
  title: mol2ccs
evidence_spans:
- enveda/ccs-prediction
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mol2ccs
    doi: 10.1186/s13321-024-00899-w
    title: mol2ccs
  dedup_kept_from: coll_mol2ccs
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00899-w
  all_source_dois:
  - 10.1186/s13321-024-00899-w
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gnn-model-inference-and-prediction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Execute forward passes through trained graph neural network models on held-out test datasets to generate molecular property predictions (e.g., collision cross section values) and compute generalizability metrics (RMSE, MAE, R²) to validate model performance on unseen data.

## When to use

You have a pre-trained GNN model checkpoint, a test dataset with molecular representations (SMILES, 3D coordinates, adducts) and ground-truth labels, and need to quantify how well the model generalizes to held-out data. This is the evaluation step after model training, when you want to verify reproducibility of reported baseline metrics or assess model performance across different molecular datasets.

## When NOT to use

- Model checkpoint is missing or incompatible with the inference framework (e.g., .h5 file trained in TensorFlow 1.x but you are using PyTorch).
- Test dataset column schema (smiles, adduct, ccs) does not match the training schema, or required columns are missing entirely.
- You have only a training set and need to perform model training first—this skill assumes a pre-trained, frozen model.

## Inputs

- Pre-trained GNN model checkpoint file (.h5 format)
- Test dataset (parquet or CSV format with columns: smiles, coordinates or smiles-only, adduct, ccs)
- Parameter file (JSON) containing model hyperparameters and training configuration
- Data preprocessing specification (column names, normalization constants from training)

## Outputs

- Predicted collision cross section values (numeric array or column)
- Regression evaluation metrics: RMSE, MAE, R² computed on test set
- Tabulated results file (CSV or log output) with predictions and metrics

## How to apply

Load the pre-trained GNN model from its serialized checkpoint (.h5 or equivalent format). Prepare the test dataset by applying the same preprocessing and standardization pipeline used during training—including column naming (smiles, coordinates, adduct, ccs), data type conversions, and feature engineering. Execute model inference on the entire test set to generate predictions. Compute regression metrics (RMSE, MAE, R²) by comparing predicted values against ground-truth test labels. Tabulate results alongside reported baseline values from the paper to verify reproducibility. If coordinates are absent from the input, the model will generate 3D coordinates from SMILES before inference.

## Related tools

- **PyTorch Geometric** (GNN framework for loading and executing graph-based model inference)
- **enveda/ccs-prediction** (Repository containing pre-trained model checkpoints, inference scripts, and test data splits) — https://github.com/enveda/ccs-prediction
- **train_and_predict.py** (Wrapper functions for model prediction (wrapper_predict)) — https://github.com/enveda/ccs-prediction/blob/main/mol2ccs/train_and_predict.py

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --model-output-file "model/train-metlin-test-metlin.h5" --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --coordinates-present
```

## Evaluation signals

- Predicted CCS values fall within the expected physical range and match ground-truth distributions (histogram/QQ-plot alignment).
- Computed RMSE, MAE, and R² values are numerically equivalent or very close (within rounding error) to reported baseline metrics in the paper.
- No NaN, infinite, or out-of-bounds predictions; all test samples produce valid outputs.
- Per-dataset metrics (e.g., train-METLIN-test-CCSBase) can be reproduced by running the exact Makefile command with consistent input files and parameter settings.

## Limitations

- The model requires consistent data preprocessing: if input data omit the adduct or coordinates column, or if column names differ from training, inference will fail or produce erroneous predictions.
- 3D coordinate generation from SMILES alone (when coordinates-present=False) introduces additional computational cost and potential stereoisomer ambiguity; pre-computed coordinates are preferred for reproducibility.
- Model generalization is dataset-specific: the same model trained on METLIN will not generalize identically to CCSBase; cross-dataset evaluation requires explicit reporting of train/test dataset pairs.
- Metrics (RMSE, MAE, R²) are aggregate statistics and may mask systematic errors on subpopulations (e.g., specific adduct types or mass ranges); error distribution analysis is recommended.

## Evidence

- [other] Execute model inference on the test set using the trained GNN to generate collision cross section predictions. Compute generalizability metrics (RMSE, MAE, R²) comparing predictions against ground-truth test labels.: "Execute model inference on the test set using the trained GNN to generate collision cross section predictions. Compute generalizability metrics (RMSE, MAE, R²) comparing predictions against"
- [other] Load the CCS dataset and apply any required preprocessing or standardization consistent with training. Partition data into train/validation/test splits or load the held-out test set as specified in the repository.: "Load the CCS dataset and apply any required preprocessing or standardization consistent with training. Partition data into train/validation/test splits or load the held-out test set as specified in"
- [readme] coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates): "coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates)"
- [readme] Train the model based on your own training dataset with [wrapper_train] and predict with [wrapper_predict] function.: "Train the model based on your own training dataset with [wrapper_train] and predict with [wrapper_predict] function."
- [readme] Predictions are available and can be directly downloaded from Zenodo. The files should be unzipped and placed in the `data` directory.: "Predictions are available and can be directly downloaded from Zenodo. The files should be unzipped and placed in the `data` directory."
