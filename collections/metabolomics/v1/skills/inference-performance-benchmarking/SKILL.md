---
name: inference-performance-benchmarking
description: Use when you have trained two or more graph neural network models on the same CCS dataset split (using identical hyperparameters, loss functions, and optimization settings) and need to rigorously compare their held-out test performance to determine which architecture balances prediction accuracy.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  tools:
  - PyTorch Geometric (PyG)
  - PyTorch
  - scikit-learn metrics
derived_from:
- doi: 10.1186/s13321-024-00899-w
  title: mol2ccs
evidence_spans:
- enveda/ccs-prediction
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mol2ccs
    doi: 10.1186/s13321-024-00899-w
    title: mol2ccs
  dedup_kept_from: coll_mol2ccs
schema_version: 0.2.0
---

# Inference-Performance Benchmarking

## Summary

Evaluate and compare the computational efficiency and predictive accuracy of alternative GNN architectures for collision cross section prediction by measuring inference speed, training time, and regression metrics (RMSE, MAE) on held-out test sets. This skill enables quantitative assessment of whether architectural changes improve model performance without sacrificing generalizability.

## When to use

You have trained two or more graph neural network models on the same CCS dataset split (using identical hyperparameters, loss functions, and optimization settings) and need to rigorously compare their held-out test performance to determine which architecture best balances prediction accuracy with computational cost.

## When NOT to use

- Models were trained on different dataset splits or with different hyperparameters—metrics will not be directly comparable; ensure identical training conditions before benchmarking.
- Test set has significant domain shift from training data (e.g., testing on CCSBase when trained on METLIN only)—use separate generalization evaluation workflows to assess cross-dataset performance.
- Input is validation performance only—the article emphasizes evaluating on held-out test sets; validation metrics do not guarantee generalizability.

## Inputs

- Trained alternative GNN model checkpoint (PyTorch .pt or .h5 format)
- Baseline GNN model checkpoint for comparison
- Held-out test set in parquet format with columns: smiles, coordinates (optional), adduct, ccs
- Model parameter configuration (JSON) specifying architecture, dropout rate, and optimization hyperparameters

## Outputs

- Comparative performance metrics table (CSV or DataFrame) with rows for each architecture and columns: RMSE, MAE, prediction accuracy, training time (seconds), inference speed (molecules/second)
- Test set predictions (parquet or CSV) with predicted and ground-truth CCS values for each architecture
- Inference timing profile (JSON or text) recording wall-clock time and throughput for batch inference

## How to apply

After training alternative GNN architectures (e.g., GAT, MPNN) with equivalent input/output dimensions to a baseline model on the training set, evaluate both on the held-out test set by computing prediction accuracy, RMSE, MAE, and other regression metrics for CCS predictions. Measure training time and inference speed for each architecture under identical conditions. Generate a comparative performance table documenting metric values, training time, and inference speed side-by-side to identify which architecture achieves superior generalization. Use the test set metrics as the primary decision signal—do not rely on validation performance alone—since the goal is to assess generalizability on unseen molecular structures.

## Related tools

- **PyTorch Geometric (PyG)** (Load alternative GNN architectures, instantiate graph data loaders, and execute forward passes for inference on test batches)
- **PyTorch** (Manage model checkpoints, compute loss functions, and profile training/inference timing)
- **scikit-learn metrics** (Calculate RMSE, MAE, and other regression evaluation metrics from predicted vs. ground-truth CCS values)

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin.h5" --coordinates-column-name "coordinates" --coordinates-present --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --dropout-rate 0.1 --epochs 400
```

## Evaluation signals

- Test set RMSE and MAE values for both architectures are numerically valid (non-NaN, finite) and fall within expected ranges for CCS prediction (typically < 5% error on held-out molecules).
- Inference speed (molecules/second) is measured consistently using identical batch sizes and hardware; reported values differ by ≤ 10% across repeated runs to ensure stability.
- Comparative table is complete with no missing metric values; architectures use equivalent input/output dimensions (verified against model configuration JSON) to ensure fair comparison.
- Test set predictions include both baseline and alternative architectures with identical molecule ordering and adduct types; no systematic bias in residuals (predicted − ground-truth CCS) for either architecture.
- Training time difference between architectures is explained by documented parameter counts and graph operation complexity (e.g., attention mechanisms in GAT vs. message passing in MPNN).

## Limitations

- Benchmark results are specific to the hardware and software environment used (GPU model, PyTorch/PyG versions, batch size); inference speed may not transfer to different deployment targets.
- The README does not specify tolerance thresholds or error budgets for declaring one architecture 'superior'—practitioners must define domain-appropriate thresholds (e.g., 'RMSE improvement > 2%') before benchmarking.
- Test set performance depends on dataset composition and preprocessing (coordinate generation, 3D structure quality); results may not generalize to molecules outside the METLIN and CCSBase distributions.
- Inference benchmarking measures point estimates; multiple runs and confidence intervals are recommended but not detailed in the provided workflows.

## Evidence

- [other] Evaluate both the original and alternative architectures on the held-out test set, computing prediction accuracy, RMSE, MAE, and other relevant regression metrics for CCS prediction.: "Evaluate both the original and alternative architectures on the held-out test set, computing prediction accuracy, RMSE, MAE, and other relevant regression metrics"
- [other] Train the alternative GNN on the training set using the same hyperparameters, loss function, and optimization settings as the original baseline, monitoring validation performance.: "Train the alternative GNN on the training set using the same hyperparameters, loss function, and optimization settings as the original baseline"
- [other] Generate a comparative performance table documenting metric values, training time, and inference speed for both architectures side-by-side.: "Generate a comparative performance table documenting metric values, training time, and inference speed for both architectures side-by-side"
- [other] The paper evaluates graph neural networks for predicting collision cross section, establishing a baseline for GNN-based approaches that can be extended with alternative architectures.: "The paper evaluates graph neural networks for predicting collision cross section, establishing a baseline for GNN-based approaches"
