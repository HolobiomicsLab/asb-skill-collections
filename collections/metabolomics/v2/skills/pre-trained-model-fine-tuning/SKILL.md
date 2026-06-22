---
name: pre-trained-model-fine-tuning
description: Use when you have a small training dataset for molecular property prediction (e.g., <500 samples from PredRet or MoNA databases) and a pre-trained GNN model is available that was trained on a related, larger molecular corpus.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3372
  tools:
  - PyTorch
  - DGL (Deep Graph Library)
  - RDKit
  - retention_time_gnn
derived_from:
- doi: 10.1021/acs.analchem.3c03177
  title: retention_time_gnn
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_retention_time_gnn_cq
    doi: 10.1021/acs.analchem.3c03177
    title: retention_time_gnn
  dedup_kept_from: coll_retention_time_gnn_cq
schema_version: 0.2.0
---

# pre-trained-model-fine-tuning

## Summary

Transfer a pre-trained graph neural network model to a new retention time prediction task by loading frozen encoder weights and retraining only the prediction head on a small target dataset. This approach leverages knowledge from large pre-training corpora (METLIN-SMRT) to overcome data scarcity in specialized domains.

## When to use

You have a small training dataset for molecular property prediction (e.g., <500 samples from PredRet or MoNA databases) and a pre-trained GNN model is available that was trained on a related, larger molecular corpus. Transfer learning is especially beneficial when the target dataset is too small to train a model from scratch without overfitting.

## When NOT to use

- Input dataset is already large (>5000 samples) — training from scratch may be more efficient and avoid catastrophic forgetting.
- Pre-trained model was trained on a domain unrelated to your target task (e.g., pre-training on proteins, transfer to small-molecule LC-MS) — domain mismatch may render encoder weights unhelpful.
- You require interpretability of learned features and cannot afford to use a frozen pre-trained encoder — fine-tuning end-to-end may be necessary.

## Inputs

- Pre-trained GNN model checkpoint (PyTorch .pt or .pth file)
- Target dataset with molecular structures (SMILES or graph representations) and retention time labels
- Molecular graph representations (nodes as atom features, edges as bonds)

## Outputs

- Fine-tuned model checkpoint with updated prediction head weights
- Retention time predictions on target dataset test set
- Performance metrics (MAE, RMSE, R²) on target domain

## How to apply

Load the pre-trained GNN encoder checkpoint from the repository (e.g., weights learned during run_pretrain.py on METLIN-SMRT). Freeze the encoder layers to preserve learned molecular graph representations. Replace or retrain only the task-specific prediction head (the regression head for retention time) on your target dataset using run_transfer.py with the target flag (e.g., -t FEM_long). Use early stopping or validation monitoring to prevent overfitting on the small target dataset. Evaluate using standard metrics (e.g., mean absolute error, R²) on a held-out test set from the target domain.

## Related tools

- **PyTorch** (Deep learning framework for loading, freezing, and fine-tuning GNN model weights and managing backpropagation on the prediction head)
- **DGL (Deep Graph Library)** (Graph neural network library for encoding molecular graph structures and performing message passing in frozen encoder layers)
- **RDKit** (Cheminformatics toolkit for converting SMILES strings to molecular graphs (nodes, edges, atom features) for GNN input)
- **retention_time_gnn** (Reference implementation providing pre-trained encoder, transfer learning script (run_transfer.py), and dataset loaders) — https://github.com/seokhokang/retention_time_gnn

## Examples

```
python run_transfer.py -t FEM_long
```

## Evaluation signals

- Prediction head loss decreases monotonically over epochs on the validation set (no divergence); validation metrics plateau before test evaluation.
- Test set MAE and RMSE on the target domain are substantially lower than a baseline model trained from scratch on the same small target dataset.
- Model maintains reasonable predictions across the range of retention times in the target dataset (no collapse to constant or mean value).
- Frozen encoder weights do not change after fine-tuning (verify weight checksums or inspect gradient flow — gradients should be None for encoder layers).
- Cross-validation or repeated train–test splits show consistent performance, indicating the model generalizes rather than memorizing the small target dataset.

## Limitations

- Performance depends critically on similarity between the pre-training domain (METLIN-SMRT) and the target domain (PredRet, MoNA); if molecular structures or LC-MS conditions differ substantially, transfer may provide minimal benefit.
- Small target datasets (the intended use case) provide limited signal for tuning the prediction head; overfitting remains a risk even with a frozen encoder — regularization and early stopping are essential.
- The approach assumes the pre-trained encoder has learned generalizable molecular representations; if the encoder was trained with different atom feature encodings or graph construction rules than the target dataset uses, compatibility issues may arise.
- Retention time is highly dependent on chromatographic conditions (column chemistry, gradient, temperature, pH); pre-training on one LC-MS platform may not transfer well to drastically different instrumental setups.

## Evidence

- [intro] Pytorch implementation of the model described in the paper: "Pytorch implementation of the model described in the paper"
- [intro] Retention time prediction using pre-trained graph neural networks on small training datasets: "Retention Time Prediction by Learning from Small Training Dataset with Pre-Trained Graph Neural Network"
- [readme] Transfer learning workflow with model pre-training and evaluation scripts: "run_pretrain.py - script for model pre-training
run_transfer.py - script for model transfer learning and evaluation"
- [readme] GNN architecture composed of encoder and task-specific layers: "gnn/*.py - GNN architecture"
- [readme] Multiple target datasets from specialized databases for evaluation: "The target datasets from PredRet database can be downloaded from http://predret.org/
The target datasets from MoNA database can be downloaded from https://mona.fiehnlab.ucdavis.edu/"
