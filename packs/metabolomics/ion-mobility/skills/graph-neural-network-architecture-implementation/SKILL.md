---
name: graph-neural-network-architecture-implementation
description: Use when you have a baseline GNN model trained on a molecular property prediction task (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3324
  tools:
  - PyTorch Geometric (PyG)
  - PyTorch
  - enveda/ccs-prediction
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-neural-network-architecture-implementation

## Summary

Implement alternative graph neural network architectures (e.g., GAT, MPNN) for molecular property prediction tasks and compare their held-out test performance against a baseline GNN model using standardized regression metrics. This skill enables empirical evaluation of architectural choices in graph-based deep learning for chemistry applications.

## When to use

You have a baseline GNN model trained on a molecular property prediction task (e.g., collision cross section) with fixed train/validation/test splits, and you want to quantify whether alternative message-passing or attention-based graph architectures improve or degrade generalization performance without introducing confounding variables like different hyperparameters or data preprocessing.

## When NOT to use

- The baseline model does not exist or was trained on different data splits or hyperparameters — architectural comparisons require strict parameter parity.
- You are performing hyperparameter optimization or cross-validation — this skill fixes hyperparameters to isolate architectural effects.
- The input data schema differs between train and test (e.g., missing coordinates or inconsistent column names) — data preparation must precede this skill.

## Inputs

- Pre-trained baseline GNN model (PyTorch or PyTorch Geometric format, e.g., .h5 or checkpoint)
- Preprocessed training dataset (parquet or CSV with SMILES, 3D coordinates, adduct, target property)
- Preprocessed validation dataset (same schema)
- Preprocessed held-out test dataset (same schema)
- Hyperparameter configuration file (JSON) specifying dropout rate, epochs, learning rate, batch size, loss function

## Outputs

- Trained alternative GNN model checkpoint or weights file
- Test set predictions (CSV or parquet with SMILES, predicted value, ground truth, residual)
- Comparative performance table (CSV or markdown) with RMSE, MAE, accuracy, training time, and inference speed for baseline vs. alternative architecture
- Validation learning curves (optional: loss/metric plots over epochs for both architectures)

## How to apply

Clone the reference repository (enveda/ccs-prediction) to access the original model architecture, preprocessed dataset splits (training, validation, test sets), and hyperparameter configurations. Implement an alternative GNN architecture (Graph Attention Network or Message-Passing Neural Network) with identical input/output dimensions to the baseline. Train the alternative architecture on the training set using the same loss function, optimizer settings, dropout rate, and epoch count as the original baseline, monitoring validation performance to detect overfitting. Evaluate both architectures on the held-out test set, computing prediction accuracy, RMSE, MAE, and any domain-specific metrics (e.g., absolute error in CCS units). Generate a comparative performance table documenting metric values, training time, and inference speed side-by-side. The key rationale is strict hyperparameter and data split alignment: architectural differences alone should account for performance variations.

## Related tools

- **PyTorch Geometric (PyG)** (Provides pre-built GNN layer modules (GAT, MessagePassing, GraphConv) and graph data structures for implementing alternative architectures with consistent input/output interfaces.) — https://github.com/pyg-team/pytorch_geometric
- **PyTorch** (Core deep learning framework for training and inference; handles autograd, loss computation, and optimization steps.) — https://github.com/pytorch/pytorch
- **enveda/ccs-prediction** (Reference repository containing baseline model code, dataset splits, hyperparameter configurations, and train/test scripts.) — https://github.com/enveda/ccs-prediction

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase-gat" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --parameter-path "parameter/parameter-train-metlin-test-metlin.json" --model-output-file "model/train-metlin-test-metlin-gat.h5" --coordinates-column-name "coordinates" --coordinates-present --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --dropout-rate 0.1 --epochs 400
```

## Evaluation signals

- Both architectures converge on the same test set (no NaN or infinite predictions) and produce numeric outputs in the expected range for the target property (e.g., CCS values > 0).
- Test set RMSE and MAE for the alternative architecture differ from baseline by >0.1% (indicating meaningful architectural effect) while validation curves show similar convergence behavior (hyperparameter parity verified).
- Training time and inference speed are reported for both architectures; inference speed ratio reflects model size differences (e.g., GAT typically slower due to attention computation).
- Residual distributions (prediction − ground truth) are approximately symmetric and homoscedastic for both architectures; major asymmetries suggest data leakage or train/test contamination.
- The comparative table is reproducible: re-running with the same random seed produces identical metric values (±1e-6 due to floating-point precision).

## Limitations

- Comparison is valid only when both architectures are trained on identical data splits and hyperparameters; even modest differences (e.g., different learning rate schedules or batch sizes) conflate architectural effects with tuning effects.
- The held-out test set must be truly independent and not used during hyperparameter selection; if test performance was used to tune the baseline, the comparison is biased.
- Inference speed comparisons depend on hardware (GPU model, memory bandwidth) and implementation details (batch size, graph sparsity); results may not generalize across hardware platforms.
- Alternative architectures with significantly more parameters (e.g., larger attention heads) may show inflated performance due to overfitting even on held-out data; controlling model capacity is necessary for fair comparison.

## Evidence

- [other] Implement an alternative message-passing GNN architecture (Graph Attention Network or Message-Passing Neural Network) with equivalent input/output dimensions to the original model.: "Implement an alternative message-passing GNN architecture (Graph Attention Network or Message-Passing Neural Network) with equivalent input/output dimensions to the original model."
- [other] Train the alternative GNN on the training set using the same hyperparameters, loss function, and optimization settings as the original baseline, monitoring validation performance.: "Train the alternative GNN on the training set using the same hyperparameters, loss function, and optimization settings as the original baseline, monitoring validation performance."
- [other] Evaluate both the original and alternative architectures on the held-out test set, computing prediction accuracy, RMSE, MAE, and other relevant regression metrics for CCS prediction.: "Evaluate both the original and alternative architectures on the held-out test set, computing prediction accuracy, RMSE, MAE, and other relevant regression metrics for CCS prediction."
- [other] Generate a comparative performance table documenting metric values, training time, and inference speed for both architectures side-by-side.: "Generate a comparative performance table documenting metric values, training time, and inference speed for both architectures side-by-side."
- [readme] See the commands in the `Makefile` to train the models. Run them as `make train-metlin-test-metlin`: "See the commands in the `Makefile` to train the models. Run them as `make train-metlin-test-metlin`"
