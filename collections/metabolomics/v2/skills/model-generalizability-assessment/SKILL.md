---
name: model-generalizability-assessment
description: Use when you have a pre-trained GNN model for CCS prediction and need
  to verify that it generalizes to test data that was held out during training. Use
  it specifically when comparing model performance across different molecular datasets
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3665
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0176
  tools:
  - enveda/ccs-prediction repository (model code and pre-trained weights)
  - PyTorch Geometric
  - enveda/ccs-prediction repository
  - train-test.py script
  techniques:
  - ion-mobility-MS
  license_tier: open
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

# model-generalizability-assessment

## Summary

Evaluate whether a trained graph neural network model for collision cross section prediction generalizes effectively to held-out test data by computing standard regression metrics (RMSE, MAE, R²) and comparing against baseline values. This skill is essential for validating whether GNN models can reliably predict CCS across diverse molecular datasets beyond their training distribution.

## When to use

Apply this skill when you have a pre-trained GNN model for CCS prediction and need to verify that it generalizes to test data that was held out during training. Use it specifically when comparing model performance across different molecular datasets (e.g., METLIN-CCS vs. CCSBase) or when validating that a model trained on one dataset can predict accurately on another held-out dataset.

## When NOT to use

- Input data has not been preprocessed or standardized to match the training pipeline (use data preprocessing skill first)
- No held-out test set or pre-defined train/test split exists (use data partitioning skill first)
- Model checkpoint is missing or incompatible with the inference framework

## Inputs

- Pre-trained GNN model checkpoint (.h5 format)
- Test dataset in parquet format with columns: smiles, adduct, ccs, coordinates (optional)
- Parameter configuration JSON file specifying model hyperparameters
- Column name mappings for smiles, adduct, ccs, and coordinates

## Outputs

- Numerical generalizability metrics (RMSE, MAE, R² values)
- Tabulated results comparing predictions to ground-truth test labels
- Metrics aggregated and compared against reported baseline values
- Output prefix-named prediction files from test set inference

## How to apply

Load the pre-trained GNN model checkpoint and the held-out test dataset, ensuring data preprocessing (standardization, coordinate formatting) matches the training pipeline. Partition the data or use the pre-defined test split specified in the repository. Execute model inference on the test set to generate CCS predictions. Compute three generalizability metrics: RMSE (root mean squared error), MAE (mean absolute error), and R² (coefficient of determination) by comparing predictions against ground-truth test labels. Aggregate results into a results table and compare metric values against reported baselines from the paper to verify reproducibility and assess whether generalization performance meets expectations.

## Related tools

- **PyTorch Geometric** (Graph neural network framework for loading, executing, and performing inference with pre-trained GNN model checkpoints)
- **enveda/ccs-prediction repository** (Source of pre-trained model weights, test datasets, parameter configurations, and training/inference scripts) — https://github.com/enveda/ccs-prediction
- **train-test.py script** (Python script in repository for training models and generating test set predictions) — https://github.com/enveda/ccs-prediction

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5" --coordinates-column-name "coordinates" --coordinates-present --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --dropout-rate 0.1 --epochs 400
```

## Evaluation signals

- Computed RMSE, MAE, and R² values match or closely approximate the reported baseline metrics in the paper within expected numerical precision
- Test set predictions are generated successfully for all samples without runtime errors or NaN values
- Metrics are aggregated and tabulated in a consistent format enabling direct comparison to Table 1 or equivalent results in the publication
- R² value is positive and typically > 0.7 for well-generalizing models; RMSE and MAE should be in reasonable ranges relative to the CCS value distribution
- Generalizability assessment reveals consistent or declining performance across different training/test dataset combinations (e.g., train-metlin-test-ccsbase vs. train-ccsbase-test-metlin)

## Limitations

- Generalizability assessment depends critically on the quality and representation of the held-out test set; if test data is too similar to training data, metrics may overestimate real-world generalization
- Metrics (RMSE, MAE, R²) are aggregated statistics that may mask poor performance on specific molecular subgroups or adduct types; per-group evaluation is recommended for thorough assessment
- Model generalization can degrade significantly when test data comes from a different instrument, acquisition protocol, or chemical space than the training set, limiting transferability across diverse experimental conditions
- The presence of 3D coordinates is optional; if coordinates are not provided, the model generates them, introducing variability that may affect reported metrics

## Evidence

- [other] Compute generalizability metrics (RMSE, MAE, R²) comparing predictions against ground-truth test labels: "Compute generalizability metrics (RMSE, MAE, R²) comparing predictions against ground-truth test labels. Aggregate results and tabulate metric values alongside reported baseline values for"
- [other] Execute model inference on the test set using the trained GNN to generate collision cross section predictions: "Execute model inference on the test set using the trained GNN to generate collision cross section predictions."
- [other] Load the CCS dataset and apply any required preprocessing or standardization consistent with training: "Load the CCS dataset and apply any required preprocessing or standardization consistent with training. Partition data into train/validation/test splits or load the held-out test set as specified in"
- [readme] Poetry command to train models with explicit train and test input files: "poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet""
- [readme] Model evaluation outputs specified with standardized column expectations: "ccs-column-name column name of the ccs, dropout-rate dropout rate of the model, epochs number of epochs to train the model"
