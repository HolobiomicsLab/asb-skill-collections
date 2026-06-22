---
name: regression-metric-computation-and-comparison
description: Use when you have trained two or more regression models (e.g., original vs. alternative GNN architectures) on the same training set and need to evaluate which generalizes better on held-out test data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - PyTorch Geometric (PyG)
  - PyTorch
  - train-test.py
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

# regression-metric-computation-and-comparison

## Summary

Compute and compare regression performance metrics (RMSE, MAE, prediction accuracy) across alternative model architectures on held-out test sets to quantify predictive performance differences. This skill validates whether alternative GNN architectures improve or degrade collision cross section prediction accuracy relative to a baseline.

## When to use

You have trained two or more regression models (e.g., original vs. alternative GNN architectures) on the same training set and need to evaluate which generalizes better on held-out test data. Use this skill when you want to produce a side-by-side performance table documenting metrics, training time, and inference speed to support architecture selection decisions.

## When NOT to use

- Models were trained on different datasets or data splits — results would conflate architecture and dataset effects.
- Hyperparameters, loss function, or optimization settings differ between architectures — isolating architecture effect requires matched training conditions.
- Test set contains predominantly out-of-distribution molecules not seen during training — generalization metrics may not reflect in-distribution performance.

## Inputs

- trained model (original GNN architecture, .h5 format)
- trained model (alternative GNN architecture, .h5 format)
- held-out test set (parquet format with smiles, 3D coordinates, adduct, observed CCS columns)

## Outputs

- comparative performance table (CSV or tabular format)
- regression metrics per architecture (RMSE, MAE, prediction accuracy values)
- training time and inference speed comparison (seconds or throughput)

## How to apply

After training both the original and alternative GNN architectures on identical training sets with matched hyperparameters, loss functions, and optimization settings, generate predictions on the held-out test set for each model. Compute prediction accuracy, root mean squared error (RMSE), mean absolute error (MAE), and other regression metrics by comparing predicted vs. observed collision cross section values. Organize results in a comparative performance table documenting metric values, training time, and inference speed side-by-side for both architectures. The rationale is that identical train/test splits and hyperparameters isolate the effect of architecture choice, allowing fair comparison of generalization performance.

## Related tools

- **PyTorch Geometric (PyG)** (Implements and trains alternative GNN architectures (Graph Attention Networks, Message-Passing Neural Networks) with equivalent input/output dimensions to baseline)
- **PyTorch** (Core framework for model training, inference, and metric computation on test batches)
- **train-test.py** (Orchestrates training and evaluation pipeline; accepts model parameters, input files, and hyperparameters via CLI arguments) — https://github.com/enveda/ccs-prediction

## Examples

```
python scripts/train-test.py --prefix 'train-metlin-test-ccsbase' --train-input-file 'ccs-prediction/metlin_train_3d.parquet' --test-input-file 'ccs-prediction/ccsbase_3d.parquet' --parameter-path 'parameter/parameter-train-metlin-test-metlin.json' --model-output-file 'model/train-metlin-test-metlin.h5' --coordinates-column-name 'coordinates' --coordinates-present --smiles-column-name 'smiles' --adduct-column-name 'adduct' --ccs-column-name 'ccs' --dropout-rate 0.1 --epochs 400
```

## Evaluation signals

- Metrics are computed on the same held-out test set for both architectures with no data leakage from training set.
- RMSE and MAE values fall within expected ranges for CCS prediction (check against baseline model performance documented in paper).
- Training time and inference speed are measured under identical hardware/batch conditions to ensure fair comparison.
- Comparative table contains all specified columns (architecture name, RMSE, MAE, accuracy, training time, inference speed) with no missing values.
- Metric differences between architectures are interpretable (i.e., not dominated by numerical precision artifacts or rounding errors).

## Limitations

- Metrics on a single test set may not reflect performance on unseen datasets with different chemical composition or adduct distribution (generalizability may vary across domains).
- Training time and inference speed depend heavily on hardware (GPU/CPU type, memory), batch size, and implementation details — comparisons are valid only within identical experimental conditions.
- RMSE is sensitive to outlier predictions; if test set contains extreme CCS values, RMSE may be dominated by a few mispredictions rather than typical error distribution.

## Evidence

- [other] Evaluate both the original and alternative architectures on the held-out test set, computing prediction accuracy, RMSE, MAE, and other relevant regression metrics for CCS prediction.: "Evaluate both the original and alternative architectures on the held-out test set, computing prediction accuracy, RMSE, MAE, and other relevant regression metrics for CCS prediction."
- [other] Generate a comparative performance table documenting metric values, training time, and inference speed for both architectures side-by-side.: "Generate a comparative performance table documenting metric values, training time, and inference speed for both architectures side-by-side."
- [other] Train the alternative GNN on the training set using the same hyperparameters, loss function, and optimization settings as the original baseline, monitoring validation performance.: "Train the alternative GNN on the training set using the same hyperparameters, loss function, and optimization settings as the original baseline, monitoring validation performance."
