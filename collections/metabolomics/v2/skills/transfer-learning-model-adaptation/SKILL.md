---
name: transfer-learning-model-adaptation
description: Use when you have a pre-trained ABCoRT model checkpoint and a new chromatography dataset (e.g., Eawag_XBridgeC18_364.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - Python
  - PyG
  - RDKit
  - Pandas
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - train_transfer_FE.py
  - PyTorch
  - PyG (PyTorch Geometric)
  - TorchMetrics
  - torch-scatter, torch-sparse, torch-cluster
  - torch
  - scikit-learn
  - tqdm
  - rdkit-pypi
  - torch_geometric
  - RT-Transformer
derived_from:
- doi: 10.1021/acs.jcim.4c02179
  title: ABCoRT
- doi: 10.1093/bioinformatics/btae084
  title: ''
- doi: 10.1038/s41467-019-13680-7
  title: ''
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
  - build: coll_rt_transformer_cq
    doi: 10.1093/bioinformatics/btae084
    title: RT-Transformer
  dedup_kept_from: coll_abcort_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.4c02179
  all_source_dois:
  - 10.1021/acs.jcim.4c02179
  - 10.1093/bioinformatics/btae084
  - 10.1038/s41467-019-13680-7
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# transfer-learning-model-adaptation

## Summary

Fine-tune a pre-trained graph neural network model on a domain-specific chromatography dataset using PyTorch and PyG to adapt learned representations for improved retention time prediction on new chemical libraries. This skill enables rapid model customization without retraining from scratch.

## When to use

You have a pre-trained ABCoRT model checkpoint and a new chromatography dataset (e.g., Eawag_XBridgeC18_364.xlsx with SMILES and measured retention times) from a different column, instrument, or chemical space, and you need to adapt the model's feature extraction layers to this domain without full retraining.

## When NOT to use

- The input dataset is not in .xlsx format or lacks SMILES and retention time columns; preprocess to this schema first.
- You are training a model from scratch (no pre-trained checkpoint available); use the main training script (train_SMRT.py) instead.
- The dataset is from the same chromatography platform and chemical space as the original training data; direct inference without fine-tuning may be sufficient.

## Inputs

- Pre-trained ABCoRT model checkpoint (.pth or similar PyTorch format)
- Transfer-learning dataset file (.xlsx format with SMILES column and retention time measurements)
- Command-line parameters (--DataSet flag with dataset filename)

## Outputs

- Fine-tuned model checkpoint with adapted feature extraction layers
- Training logs and metrics (loss, validation accuracy, monitored via TorchMetrics)
- Retention time predictions on the new chromatography domain

## How to apply

Load the pre-trained model checkpoint and the transfer-learning dataset (supplied as .xlsx with SMILES and retention time columns) into memory using Pandas and Python. Execute the train_transfer_FE.py script, passing the dataset filename via the --DataSet command-line flag; the script will convert SMILES to molecular graphs using RDKit, construct feature embeddings via PyG, and perform fine-tuning on the feature extraction layers using PyTorch. Monitor training loss and validation metrics via TorchMetrics throughout the epochs to detect convergence and overfitting. Save the resulting fine-tuned checkpoint and training logs for subsequent inference on new compounds.

## Related tools

- **train_transfer_FE.py** (Main script that orchestrates fine-tuning of the feature extraction layers using the transfer dataset) — github.com/RiverCCC/ABCoRT
- **PyTorch** (Deep learning framework for model loading, parameter optimization, and checkpoint management)
- **PyG (PyTorch Geometric)** (Graph neural network library for constructing molecular graphs and graph convolution operations)
- **RDKit** (Cheminformatics toolkit for converting SMILES strings to molecular graph representations)
- **Pandas** (Data loading and preprocessing of the .xlsx transfer dataset)
- **TorchMetrics** (Monitoring training and validation metrics during fine-tuning to assess convergence)
- **torch-scatter, torch-sparse, torch-cluster** (PyG dependencies providing efficient graph operations and aggregation)

## Examples

```
python train_transfer_FE.py --DataSet Eawag_XBridgeC18_364.xlsx
```

## Evaluation signals

- Training loss converges smoothly over epochs and validation loss plateaus without divergence, as monitored via TorchMetrics.
- Fine-tuned model predictions on a held-out test subset of the transfer dataset exhibit lower mean absolute error (MAE) or root mean squared error (RMSE) in retention time compared to the base pre-trained model, confirming domain adaptation.
- The saved fine-tuned checkpoint loads successfully in PyTorch and produces predictions with the same input/output shape and dimensionality as the original model.
- Training logs record all hyperparameters (learning rate, batch size, number of epochs) and final metric values for reproducibility.
- The fine-tuned model generalizes to new compounds in the same chromatography domain without catastrophic forgetting of pre-trained representations.

## Limitations

- Transfer learning performance depends on the size and representativeness of the target dataset; very small datasets (< 50 compounds) may overfit.
- The approach assumes the new dataset uses the same molecular representation (SMILES) and retention time measurement protocol as the pre-training data; incompatible formats will require preprocessing.
- No changelog or version history is documented in the repository, making it difficult to track which pre-trained checkpoint versions are compatible with specific transfer datasets.

## Evidence

- [other] Transfer learning on the Eawag_XBridgeC18_364 dataset is executed by running the train_transfer_FE.py script with the dataset name passed as a command-line argument via the --DataSet flag.: "Execute train_transfer_FE.py with the --DataSet parameter set to Eawag_XBridgeC18_364.xlsx"
- [other] The workflow involves loading pre-trained checkpoint, executing the transfer learning script with PyTorch and PyG, monitoring via TorchMetrics, and saving the fine-tuned model.: "Load the pre-trained model checkpoint and transfer-learning dataset (Eawag_XBridgeC18_364.xlsx) using Python and Pandas. 2. Execute train_transfer_FE.py with the --DataSet parameter set to"
- [intro] The project involves training a model and running transfer learning on thirteen transfer learning datasets.: "train the Model and run the transfer learning on thirteen transfer learning data sets"
- [readme] Repository README documents the exact CLI invocation for transfer learning.: "python train_transfer_FE.py --DataSet  Eawag_XBridgeC18_364.xlsx"
