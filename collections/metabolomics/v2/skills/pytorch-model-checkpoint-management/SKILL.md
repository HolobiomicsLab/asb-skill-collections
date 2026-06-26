---
name: pytorch-model-checkpoint-management
description: Use when you have a pretrained GNN-RT model trained on a reference molecular
  database and need to adapt it to predict LC retention times on a different in-house
  molecular dataset with potentially different chromatographic conditions or chemical
  space.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_2258
  tools:
  - PyTorch
  - Python
  - Anaconda
  - RDKit
  - Preprocess.py
  - Transferlearning.py
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c04071
  title: GNN-RT
evidence_spans:
- conda install pytorch
- Anaconda for python 3.6
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gnn_rt_cq
    doi: 10.1021/acs.analchem.0c04071
    title: GNN-RT
  dedup_kept_from: coll_gnn_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c04071
  all_source_dois:
  - 10.1021/acs.analchem.0c04071
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# PyTorch Model Checkpoint Management

## Summary

Load, configure, and fine-tune pretrained PyTorch GNN-RT models on new molecular datasets via transfer learning, preserving learned weights while adapting to target data distributions. This skill enables practitioners to reuse validated models across different in-house LC–MS databases without retraining from scratch.

## When to use

You have a pretrained GNN-RT model trained on a reference molecular database and need to adapt it to predict LC retention times on a different in-house molecular dataset with potentially different chromatographic conditions or chemical space. Use this skill when retraining from scratch is infeasible but the pretrained model's learned molecular graph representations are expected to transfer.

## When NOT to use

- Your target dataset has a fundamentally different chemical space or measurement regime (e.g., different LC column chemistry, mobile phase, or ion source) where pretrained representations may not transfer; retraining from scratch may be more appropriate.
- You lack a held-out validation set from the target database to evaluate transfer-learning success; model selection and hyperparameter tuning require independent validation data.
- The input spectra files are not standardized or preprocessed; Preprocess.py must complete successfully first to generate valid molecular graphs.

## Inputs

- Pretrained PyTorch GNN-RT model checkpoint (.pth or .pt file)
- Spectra files in data directory (raw molecular chromatography data)
- Molecular structures and measured retention time labels
- Transfer-learning hyperparameter configuration

## Outputs

- Fine-tuned PyTorch model checkpoint with adapted GNN weights
- Validation set predictions and retention time error metrics
- Training loss and accuracy curves during transfer-learning optimization

## How to apply

First, prepare your target dataset by placing spectra files in the data directory and running Preprocess.py to generate standardized molecular graphs and retention time labels using RDKit. Load the pretrained GNN-RT model in PyTorch and configure transfer-learning hyperparameters (learning rate, batch size, number of epochs). Run Transferlearning.py to fine-tune the pretrained GNN weights on the target database by backpropagation through the graph convolution layers. Finally, evaluate the adapted model on a held-out validation set from the target database and record prediction accuracy and loss metrics to confirm convergence and generalization.

## Related tools

- **PyTorch** (Deep learning framework for loading pretrained models, configuring transfer-learning hyperparameters, and backpropagation through GNN layers)
- **RDKit** (Converts molecular structures into standardized graph representations for input to the GNN model during preprocessing) — https://github.com/rdkit/rdkit
- **Preprocess.py** (Prepares user-supplied database by generating standardized molecular graphs and retention time labels before transfer learning) — https://github.com/Qiong-Yang/GNN-RT
- **Transferlearning.py** (Main executable script that loads pretrained weights and fine-tunes on target database) — https://github.com/Qiong-Yang/GNN-RT
- **Anaconda** (Python environment manager for installing PyTorch, RDKit, and runtime dependencies)

## Examples

```
python Transferlearning.py --pretrained_model pretrained_gnn_rt.pth --data_dir ./data --epochs 50 --learning_rate 0.001 --batch_size 32
```

## Evaluation signals

- Validation set prediction accuracy improves monotonically or plateaus over transfer-learning epochs (no divergence or loss explosion)
- Mean absolute error (MAE) or root mean squared error (RMSE) on retention time predictions falls within acceptable range on held-out validation set from target database
- Training loss and validation loss curves show convergence without overfitting (loss values decrease and stabilize, validation loss does not diverge from training loss)
- Fine-tuned model checkpoint can be loaded without shape mismatch or weight dimension errors, confirming layer compatibility with target data
- Model predictions on a subset of known standards from the target database match measured retention times within experimental measurement uncertainty

## Limitations

- Transfer learning assumes the pretrained model's learned molecular graph representations generalize to the target dataset; if the target chemical space or measurement conditions differ fundamentally, transfer learning may degrade performance below that of a model trained from scratch.
- Hyperparameter tuning (learning rate, batch size, number of fine-tuning epochs) is dataset-dependent and requires validation data; no universal transfer-learning schedule is provided in the article or README.
- The README provides no changelog or versioning information, making it difficult to track which pretrained checkpoint versions are compatible with specific Transferlearning.py revisions.

## Evidence

- [other] Load the pretrained GNN-RT model in PyTorch and configure transfer-learning hyperparameters.: "Load the pretrained GNN-RT model in PyTorch and configure transfer-learning hyperparameters."
- [other] Run Transferlearning.py to apply transfer learning to the in-house database.: "run [Preprocess.py], [Train.py] and [Transferlearning.py]"
- [other] Prepare the user-supplied database using Preprocess.py to generate standardized molecular graphs and retention time labels.: "Prepare the user-supplied database using Preprocess.py to generate standardized molecular graphs and retention time labels."
- [other] Evaluate the adapted model on a held-out validation set from the target database and record prediction accuracy and loss metrics.: "Evaluate the adapted model on a held-out validation set from the target database and record prediction accuracy and loss metrics."
- [readme] The GNN-RT can obtain the data-driven representations of molecules through the end-to-end learning with GNN, and predict the retention time with the GNN-learned representations.: "The GNN-RT can obtain the data-driven representations of molecules through the end-to-end learning with GNN, and predict the retention time with the GNN-learned representations."
