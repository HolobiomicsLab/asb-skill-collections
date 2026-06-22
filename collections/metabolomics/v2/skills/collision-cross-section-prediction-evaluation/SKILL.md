---
name: collision-cross-section-prediction-evaluation
description: Use when you have a pre-trained GNN CCS prediction model and need to assess its predictive performance and cross-dataset generalizability. Use it specifically when evaluating whether models trained on one CCS database (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - enveda/ccs-prediction repository (model code and pre-trained weights)
  - PyTorch Geometric
  - enveda/ccs-prediction repository
  - train-test.py script
  techniques:
  - ion-mobility-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# collision-cross-section-prediction-evaluation

## Summary

Evaluate the generalizability of graph neural network models trained for collision cross section (CCS) prediction by executing inference on held-out test sets and computing standardized accuracy metrics (RMSE, MAE, R²). This skill validates whether CCS predictors trained on one molecular database generalize effectively to unseen compounds and alternative reference datasets.

## When to use

Apply this skill when you have a pre-trained GNN CCS prediction model and need to assess its predictive performance and cross-dataset generalizability. Use it specifically when evaluating whether models trained on one CCS database (e.g., METLIN-CCS) reliably predict CCS values on held-out or external test sets from different databases (e.g., CCSBase).

## When NOT to use

- If you do not have a pre-trained model checkpoint; use training workflow instead.
- If test data has not been preprocessed to match training data format (column names, coordinate presence, standardization).
- If you are evaluating model performance on the same database used for training; use cross-validation or external test sets only.

## Inputs

- pre-trained GNN model checkpoint (.h5 file)
- test dataset in parquet format with columns: SMILES, adducts, CCS ground truth, 3D coordinates (optional)
- model parameters JSON file specifying architecture and hyperparameters
- data splits or designated held-out test set

## Outputs

- predicted CCS values for test set molecules
- generalizability metrics table (RMSE, MAE, R² per test set)
- comparison results against baseline/reported values

## How to apply

Load the pre-trained GNN model checkpoint and the test dataset, ensuring the test data is preprocessed and standardized identically to training data (column names for SMILES, adducts, CCS values, and 3D coordinates must match expectations). Partition data into train/validation/test splits or use the designated held-out test set as documented in the repository. Execute model inference on the test set to generate predicted CCS values. Compute three generalizability metrics—root mean square error (RMSE), mean absolute error (MAE), and coefficient of determination (R²)—by comparing predictions against ground-truth test labels. Aggregate results in a results table and compare against reported baseline values from the paper to verify reproducibility and quantify generalization performance across different molecular databases.

## Related tools

- **PyTorch Geometric** (GNN framework for loading and executing pre-trained graph neural network models)
- **enveda/ccs-prediction repository** (provides pre-trained model checkpoints, test datasets (METLIN-CCS, CCSBase), and inference/evaluation scripts) — https://github.com/enveda/ccs-prediction
- **train-test.py script** (command-line interface for model training and inference with configurable dataset paths and output file generation) — https://github.com/enveda/ccs-prediction

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5" --coordinates-column-name "coordinates" --coordinates-present --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --dropout-rate 0.1 --epochs 400
```

## Evaluation signals

- Predicted CCS values are numeric, finite, and within the expected range for the test dataset (e.g., 100–500 Ų for small organic molecules).
- RMSE, MAE, and R² metrics match or closely reproduce the values reported in Engler et al. 2024 for the same train/test splits.
- R² coefficient is ≥ 0.90 for intra-database evaluation and ≥ 0.85 for cross-database generalization, indicating strong predictive performance.
- Output prediction files are generated with the expected naming convention (prefix-based) and contain all test molecules with predictions and ground-truth values.
- Comparison between cross-database generalization metrics (e.g., train METLIN / test CCSBase) shows consistent degradation relative to same-database test sets, validating generalizability assessment.

## Limitations

- Evaluation assumes test data is formatted identically to training data; mismatched column names or missing 3D coordinates will cause inference to fail or produce invalid predictions.
- Results are specific to the GNN architecture and hyperparameters used during training; different architectures or training datasets may yield different generalization performance.
- Metrics are computed only for molecules present in both the test set and the pre-trained model's feature space; out-of-distribution compounds (e.g., unusual adducts or very large molecules) may be handled poorly.
- The evaluation does not account for potential class imbalance in CCS values; datasets with skewed CCS distributions may show inflated metrics on common ranges and poor performance on rare compounds.

## Evidence

- [other] 4. Execute model inference on the test set using the trained GNN to generate collision cross section predictions. 5. Compute generalizability metrics (RMSE, MAE, R²) comparing predictions against ground-truth test labels.: "Execute model inference on the test set using the trained GNN to generate collision cross section predictions. 5. Compute generalizability metrics (RMSE, MAE, R²)"
- [intro] to evaluate the generalizability of graph neural networks for predicting collision cross section: "to evaluate the generalizability of graph neural networks for predicting collision cross section"
- [readme] poetry run python scripts/train-test.py ... --test-input-file "ccs-prediction/ccsbase_3d.parquet" ... --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs": "test-input-file test set ... --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs""
- [other] Load the CCS dataset and apply any required preprocessing or standardization consistent with training. 3. Partition data into train/validation/test splits or load the held-out test set as specified in the repository.: "Load the CCS dataset and apply any required preprocessing or standardization consistent with training"
- [other] Aggregate results and tabulate metric values alongside reported baseline values for reproducibility verification.: "Aggregate results and tabulate metric values alongside reported baseline values for reproducibility verification"
