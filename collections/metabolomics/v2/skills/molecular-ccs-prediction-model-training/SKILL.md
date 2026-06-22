---
name: molecular-ccs-prediction-model-training
description: Use when you have a curated dataset of small molecules with SMILES, optional 3D coordinates, adduct information, and experimentally measured CCS values (in Ångströms or similar units), and you want to train a GNN model to predict CCS on held-out test molecules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  tools:
  - PyTorch Geometric (PyG)
  - PyTorch
  - enveda/ccs-prediction
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
---

# molecular-ccs-prediction-model-training

## Summary

Train and evaluate graph neural network models to predict collision cross section (CCS) values for small molecules from SMILES strings and optional 3D coordinates. This skill enables comparative evaluation of different GNN architectures on standardized train/test splits from curated databases (METLIN-CCS, CCSBase).

## When to use

You have a curated dataset of small molecules with SMILES, optional 3D coordinates, adduct information, and experimentally measured CCS values (in Ångströms or similar units), and you want to train a GNN model to predict CCS on held-out test molecules. Use this skill when you need to establish a baseline GNN architecture or compare alternative message-passing designs (GAT, MPNN, GraphConv) under controlled hyperparameter conditions.

## When NOT to use

- Input molecules lack SMILES or valid molecular structure representation.
- Experimental CCS values are missing or contain >20% gaps in the dataset.
- You are only doing model inference on pre-trained weights without re-training or architecture modification.

## Inputs

- training dataset (parquet): molecules with SMILES, 3D coordinates (optional), adduct, measured CCS
- test dataset (parquet): same schema as training, held-out molecules
- parameter configuration file (JSON): hyperparameters, learning rate, dropout rate, epoch count
- GNN architecture definition: PyTorch Geometric module (GraphConv, GAT, MPNN, or custom)

## Outputs

- trained model checkpoint (HDF5 or PyTorch state_dict)
- model parameters file (JSON): serialized hyperparameters used during training
- predictions on test set (parquet or CSV): predicted CCS, ground truth CCS, residuals
- performance metrics table: RMSE, MAE, R², training time, inference latency for each architecture

## How to apply

Prepare training and test datasets in parquet format with columns for SMILES, 3D coordinates (optional), adduct, and measured CCS. Load a pre-configured parameter file (JSON) specifying model hyperparameters, dropout rate, and epoch count. Execute the training script (e.g., `train-test.py`) with identical hyperparameters and loss function for both baseline and alternative architectures to ensure fair comparison. Train on the training set while monitoring validation performance, then evaluate both models on the held-out test set using regression metrics (RMSE, MAE, R²). Generate a comparative table documenting metric values, training time, and inference speed side-by-side to establish which architecture generalizes better.

## Related tools

- **PyTorch Geometric (PyG)** (Graph neural network layers (GraphConv, GAT, MPNN) for molecule encoding and message passing) — https://pytorch-geometric.readthedocs.io/
- **PyTorch** (Tensor operations, model training loop, optimization, and loss computation) — https://pytorch.org/
- **enveda/ccs-prediction** (Reference repository with training scripts, data splits, and baseline model implementations) — https://github.com/enveda/ccs-prediction

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5" --coordinates-column-name "coordinates" --coordinates-present --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --dropout-rate 0.1 --epochs 400
```

## Evaluation signals

- Test set RMSE and MAE fall within expected range (typically <5–10% of CCS median value for well-trained models).
- Validation loss converges monotonically or plateaus within 100–200 epochs without divergence.
- Predictions on held-out test set show no systematic bias (residual mean ≈ 0) and are normally distributed.
- Alternative GNN architecture metrics are directly comparable to baseline (same dataset split, loss function, optimization settings).
- Training time and inference latency are logged and reported for both architectures in the comparative table.

## Limitations

- Model training requires 3D coordinates if using spatial graph convolutions; if coordinates are absent, they must be generated externally (not yet automated in the pipeline).
- Performance is dataset-dependent: models trained on METLIN may not generalize equally to CCSBase due to different ionization conditions, instruments, or chemical space coverage.
- Baseline models (SigmaCCS, GraphCCS) are available as external references but are not included in this repository for direct architectural comparison.
- No changelog or version control information provided in the README, making it difficult to track which exact model versions were used in published results.

## Evidence

- [other] Implement an alternative message-passing GNN architecture (Graph Attention Network or Message-Passing Neural Network) with equivalent input/output dimensions to the original model.: "Implement an alternative message-passing GNN architecture (Graph Attention Network or Message-Passing Neural Network) with equivalent input/output dimensions to the original model."
- [other] Train the alternative GNN on the training set using the same hyperparameters, loss function, and optimization settings as the original baseline, monitoring validation performance.: "Train the alternative GNN on the training set using the same hyperparameters, loss function, and optimization settings as the original baseline, monitoring validation performance."
- [other] Evaluate both the original and alternative architectures on the held-out test set, computing prediction accuracy, RMSE, MAE, and other relevant regression metrics for CCS prediction.: "Evaluate both the original and alternative architectures on the held-out test set, computing prediction accuracy, RMSE, MAE, and other relevant regression metrics for CCS prediction."
- [readme] poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5": "poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet""
- [readme] coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates): "coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates)"
- [readme] Each user should download the raw database (as excel/csv) and read them in the two notebooks for each database located at https://github.com/enveda/ccs-prediction/tree/main/notebooks/data_processing.: "Each user should download the raw database and read them in the two notebooks for each database for data processing."
