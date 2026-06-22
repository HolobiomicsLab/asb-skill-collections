---
name: graph-neural-network-model-loading
description: Use when when you need to evaluate GNN performance on collision cross section prediction using the enveda/ccs-prediction repository, either by loading an existing pre-trained model checkpoint or by retraining from scratch using deposited datasets and published hyperparameters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  tools:
  - train-test.py
  - Poetry
  - Makefile
  - Zenodo Dataset (DOI:10.5281/zenodo.11199061)
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
---

# Graph Neural Network Model Loading

## Summary

Load pre-trained graph neural network models from serialized files (.h5 format) or retrain them using provided training pipelines and hyperparameters for collision cross section prediction tasks. This skill enables reproducible inference and generalizability evaluation by ensuring consistent model state across experimental runs.

## When to use

When you need to evaluate GNN performance on collision cross section prediction using the enveda/ccs-prediction repository, either by loading an existing pre-trained model checkpoint or by retraining from scratch using deposited datasets and published hyperparameters. Use this skill when reproducibility of reported metrics (MAE, R², or other regression statistics) is required.

## When NOT to use

- Input data does not contain required columns (smiles, adduct, ccs); preprocess to match data_processing notebooks specification first.
- Model file is corrupted or not in .h5 format; validate file integrity before loading.
- You require model architecture modification or novel hyperparameter exploration beyond the published pipeline; use the repository as a training framework reference instead.

## Inputs

- Pre-trained GNN model file (.h5 format)
- Training dataset (Parquet format with smiles, coordinates, adduct, ccs columns)
- Test/validation dataset (Parquet format, same schema)
- Model parameter configuration (JSON file with hyperparameters)
- Model training script (scripts/train-test.py)

## Outputs

- Loaded GNN model (in-memory PyTorch/TensorFlow object)
- Trained model checkpoint file (.h5)
- Predictions on test/validation set (Parquet or CSV)
- Performance metrics file (MAE, R², or other regression statistics)
- Training log (stdout/stderr, e.g., train-metlin-test-ccsbase.out)

## How to apply

First, clone or access the enveda/ccs-prediction GitHub repository and install dependencies using Poetry (poetry install). Load the pre-trained graph neural network model from the deposited .h5 file, or optionally retrain it using the provided training pipeline (scripts/train-test.py) with specified hyperparameters including dropout rate (e.g., 0.1), number of epochs (e.g., 400), and training data in Parquet format. Ensure input datasets follow the data format specifications documented in notebooks/data_processing/2_data_splits.ipynb, with required columns: smiles (SMILES strings), coordinates (3D coordinates, optional), adduct (ion form), and ccs (collision cross section target values). Pass the loaded or retrained model to generate predictions on validation or test sets, then compute reported performance metrics (mean absolute error, R², or other regression statistics) for comparison against published results.

## Related tools

- **train-test.py** (Executes GNN training and prediction pipeline with specified datasets, hyperparameters, and output paths) — https://github.com/enveda/ccs-prediction
- **Poetry** (Dependency and environment manager for installing GNN training framework and pre-commit hooks)
- **Makefile** (Provides pre-configured training commands (e.g., make train-metlin-test-metlin) for common model configurations) — https://github.com/enveda/ccs-prediction
- **Zenodo Dataset (DOI:10.5281/zenodo.11199061)** (Hosts pre-computed predictions and model outputs for direct download without retraining) — https://zenodo.org/badge/DOI/10.5281/zenodo.11199061.svg

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5" --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --dropout-rate 0.1 --epochs 400
```

## Evaluation signals

- Loaded model produces deterministic predictions on identical test set inputs across multiple runs (verify by comparing prediction files)
- Computed metrics (MAE, R²) match or fall within reported ranges from Engler et al. (2024) for the same train-test split combination
- Model checkpoint file is written to specified path and can be reloaded without errors on subsequent invocations
- Predictions output file contains expected schema: predictions column with float values and input features (smiles, adduct, true ccs) preserved
- Training log file records convergence (loss decreasing over epochs) and final epoch validation metrics are logged

## Limitations

- Original METLIN-CCS and CCSBase datasets must be manually downloaded from their respective databases (CCSBase: https://ccsbase.net/query; Metlin: https://metlin.scripps.edu/) due to licensing; the repository provides processing notebooks but not the raw data.
- Model generalizability is constrained by the training data distribution; cross-dataset evaluation (e.g., train on METLIN, test on CCSBase) may show degraded performance due to systematic differences in instrument platforms or data collection protocols.
- 3D coordinates are optional but recommended; if coordinates are not provided (--coordinates-present flag omitted), the model generates them from SMILES, which may introduce conformer sampling variability.
- Performance is sensitive to hyperparameter choices (dropout rate, epochs, learning rate); the published pipeline uses fixed hyperparameters and may not be optimal for new datasets or adduct types not represented in training data.

## Evidence

- [other] Load the pre-trained graph neural network model or retrain it using the provided training pipeline and hyperparameters.: "Load the pre-trained graph neural network model or retrain it using the provided training pipeline and hyperparameters."
- [readme] poetry install poetry run pre-commit install: "poetry install
poetry run pre-commit install"
- [readme] poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5": "poetry run python scripts/train-test.py \
	--prefix "train-metlin-test-ccsbase" \
	--train-input-file "ccs-prediction/metlin_train_3d.parquet" \
	--test-input-file "ccs-prediction/ccsbase_3d.parquet""
- [other] Generate collision cross section predictions on the validation or test set. Compute reported performance metrics (e.g., mean absolute error, R², or other regression statistics): "Generate collision cross section predictions on the validation or test set. Compute reported performance metrics (e.g., mean absolute error, R², or other regression statistics)"
- [readme] see notebooks/data_processing/2_data_splits.ipynb for details on the format: "see notebooks/data_processing/2_data_splits.ipynb for details on the format"
- [readme] smiles-column-name column name of the smiles, adduct-column-name column name of the adduct, ccs-column-name column name of the ccs: "smiles-column-name column name of the smiles, adduct-column-name column name of the adduct, ccs-column-name column name of the ccs"
- [readme] coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates): "coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates)"
