---
name: graph-neural-network-fine-tuning
description: Use when when you have a pre-trained GNN checkpoint and a smaller, task-specific dataset (e.g., Eawag_XBridgeC18_364.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - Python
  - PyG
  - RDKit
  - Pandas
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - PyTorch
  - PyG (PyTorch Geometric)
  - TorchMetrics
  - torch-scatter, torch-sparse, torch-cluster
derived_from:
- doi: 10.1021/acs.jcim.4c02179
  title: ABCoRT
evidence_spans:
- '**Python**'
- '**PyG**'
- '**RDKit**'
- '- **RDKit**'
- '**Pandas**'
- '**torch-scatter**'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_abcort_cq
    doi: 10.1021/acs.jcim.4c02179
    title: ABCoRT
  dedup_kept_from: coll_abcort_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.4c02179
  all_source_dois:
  - 10.1021/acs.jcim.4c02179
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-neural-network-fine-tuning

## Summary

Fine-tune a pre-trained graph neural network model on a domain-specific dataset using transfer learning to adapt molecular property predictions to new chromatographic conditions or chemical spaces. This skill is applied when a general-purpose GNN model (trained on broad chemical data) must be adapted to a narrower, well-characterized target dataset with limited samples.

## When to use

When you have a pre-trained GNN checkpoint and a smaller, task-specific dataset (e.g., Eawag_XBridgeC18_364.xlsx with ~364 compounds) that represents a different chromatographic condition or chemical domain, and you want to improve prediction accuracy on that domain without retraining from scratch.

## When NOT to use

- Target dataset is already in feature-vector form (not SMILES or molecular graphs) — use standard PyTorch/scikit-learn fine-tuning instead.
- Pre-trained model is from a completely different modality (e.g., image CNN, NLP transformer) — transfer learning may not preserve chemical semantics.
- Target dataset is extremely large (>100k compounds) — full retraining may be more efficient than fine-tuning.

## Inputs

- Pre-trained GNN model checkpoint (PyTorch state_dict)
- Transfer-learning dataset in .xlsx format (compound SMILES, retention time labels, optional molecular properties)
- Dataset name string (passed via --DataSet flag)

## Outputs

- Fine-tuned GNN model checkpoint
- Training logs with per-epoch metrics (loss, validation accuracy, TorchMetrics)
- Model predictions on target dataset

## How to apply

Load the pre-trained model checkpoint and the target transfer-learning dataset (in .xlsx format) using Pandas. Execute the train_transfer_FE.py script with the --DataSet parameter set to your target dataset filename (e.g., --DataSet Eawag_XBridgeC18_364.xlsx). PyTorch and PyG will handle molecular graph construction and forward passes; RDKit converts SMILES to molecular graphs. Monitor training metrics (loss, validation accuracy) via TorchMetrics throughout fine-tuning. Save the fine-tuned model checkpoint and training logs after convergence. The rationale is that transfer learning retains learned chemical patterns from pre-training while allowing model weights to adapt to the target domain's feature distribution and retention-time prediction bias.

## Related tools

- **PyTorch** (Orchestrates gradient-based optimization and checkpoint management during fine-tuning)
- **PyG (PyTorch Geometric)** (Constructs and propagates graph neural network layers for molecular graphs)
- **RDKit** (Converts SMILES strings to molecular graph objects (atoms, bonds, features))
- **Pandas** (Loads and parses transfer-learning dataset (.xlsx files) with compound identifiers and labels)
- **TorchMetrics** (Computes and logs validation metrics (accuracy, loss) for monitoring training convergence)
- **torch-scatter, torch-sparse, torch-cluster** (Low-level graph operations for efficient GNN message passing on molecular graphs)

## Examples

```
python train_transfer_FE.py --DataSet Eawag_XBridgeC18_364.xlsx
```

## Evaluation signals

- Validation loss decreases monotonically (or with acceptable plateaus) over training epochs, indicating the model is learning the target dataset's patterns.
- Fine-tuned model achieves higher prediction accuracy on the target dataset than the pre-trained model alone (measured via holdout test set or cross-validation).
- Training logs contain per-epoch TorchMetrics outputs (e.g., MSE, R²) that match expected ranges for retention-time prediction (typically MSE < 5–10 min² for chromatography).
- Model checkpoint file size and layer weight magnitudes remain stable; absence of NaN or Inf in loss indicates no training collapse.
- Predictions on the target dataset are physically plausible (retention times within observed range, no outliers > 3σ from mean).

## Limitations

- Transfer learning assumes the pre-trained model and target domain share sufficient chemical/chromatographic patterns; if domains are orthogonal, fine-tuning may not improve generalization.
- Small target datasets (< ~100 compounds) risk overfitting; regularization (dropout, weight decay) and early stopping are essential.
- No changelog or versioning mentioned for the ABCoRT repository; reproducibility may be affected by undocumented updates to train_transfer_FE.py or dependency versions.
- The script requires the exact --DataSet parameter format (.xlsx filename); mismatched file paths or formats will cause runtime errors.

## Evidence

- [other] Transfer learning on the Eawag_XBridgeC18_364 dataset is executed by running the train_transfer_FE.py script with the dataset name passed as a command-line argument via the --DataSet flag.: "Transfer learning on the Eawag_XBridgeC18_364 dataset is executed by running the train_transfer_FE.py script with the dataset name passed as a command-line argument via the --DataSet flag."
- [other] Load the pre-trained model checkpoint and transfer-learning dataset (Eawag_XBridgeC18_364.xlsx) using Python and Pandas. Execute train_transfer_FE.py with the --DataSet parameter set to Eawag_XBridgeC18_364.xlsx using PyTorch and PyG for graph neural network operations. Monitor training metrics via TorchMetrics during fine-tuning. Save the fine-tuned model checkpoint and training logs.: "Load the pre-trained model checkpoint and transfer-learning dataset (Eawag_XBridgeC18_364.xlsx) using Python and Pandas. Execute train_transfer_FE.py with the --DataSet parameter set to"
- [readme] If you want to run the transfer learning on thirteen transfer learning data sets, use: python train_transfer_FE.py --DataSet Eawag_XBridgeC18_364.xlsx: "If you want to run the transfer learning on thirteen transfer learning data sets, use: python train_transfer_FE.py --DataSet Eawag_XBridgeC18_364.xlsx"
- [other] The project involves training a model and running transfer learning on thirteen transfer learning datasets: "The project involves training a model and running transfer learning on thirteen transfer learning datasets"
