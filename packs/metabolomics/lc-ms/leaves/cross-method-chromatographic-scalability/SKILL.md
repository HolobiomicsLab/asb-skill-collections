---
name: cross-method-chromatographic-scalability
description: Use when you have a pretrained RT-Transformer model checkpoint from a
  large, well-characterized chromatographic dataset (e.g., SMRT) and need to predict
  retention times for a different chromatographic method or instrument condition represented
  in a smaller, domain-specific dataset (e.g., PredRet).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3373
  tools:
  - Python
  - torch
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - scikit-learn
  - tqdm
  - RT-Transformer
  - torch_geometric
  - rdkit-pypi
  - PredRet
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
- Python 3.9
- torch
- torch-scatter
- torch-sparse
- torch-cluster
- scikit-learn
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rt_transformer_cq
    doi: 10.1093/bioinformatics/btae084
    title: RT-Transformer
  dedup_kept_from: coll_rt_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae084
  all_source_dois:
  - 10.1093/bioinformatics/btae084
  - 10.1038/s41467-019-13680-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Cross-Method Chromatographic Scalability via Transfer Learning

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Transfer a pretrained retention time prediction model (RT-Transformer) from one chromatographic dataset (SMRT) to a target chromatographic method (PredRet) by freezing early encoder layers, retraining a task-specific head, and validating mean absolute error across held-out test molecules. This skill addresses the scalability gap in retention time prediction across different chromatographic conditions.

## When to use

You have a pretrained RT-Transformer model checkpoint from a large, well-characterized chromatographic dataset (e.g., SMRT) and need to predict retention times for a different chromatographic method or instrument condition represented in a smaller, domain-specific dataset (e.g., PredRet). Use this skill when retraining the full model from scratch is infeasible or when the target dataset is too small to support independent training.

## When NOT to use

- Target dataset has fundamentally different chemical classes or ionization modes not represented in the pretraining data; transfer learning may propagate systematic biases.
- You have no pretraining data or checkpoint available; train a model from scratch instead.
- Experimental retention times for the target method are unavailable or highly noisy; validation and fine-tuning will fail.

## Inputs

- Pretrained RT-Transformer model checkpoint (.pth file)
- Target chromatographic dataset (CSV format with 'InChI' and 'RT' columns)
- Molecular structures (InChI strings or SMILES)

## Outputs

- Transfer-learned model weights (PyTorch .pth checkpoint)
- Prediction table (CSV: molecule_id, predicted_rt, experimental_rt, absolute_error)
- Validation and test metrics (MAE, RMSE per scikit-learn)

## How to apply

Load the pretrained RT-Transformer checkpoint and the target chromatographic dataset (as CSV with InChI and RT columns). Preprocess molecular structures by generating fingerprints and graph representations using RDKit and PyTorch Geometric, converting them to tensor form. Freeze the early encoder layers of the pretrained model to preserve learned chemical features, then attach a new task-specific prediction head tuned to the target chromatographic method. Train on the target dataset using mean absolute error (MAE) or root mean squared error (RMSE) loss, monitoring validation performance with scikit-learn metrics. Evaluate the adapted model on a held-out test set and compute cross-method prediction accuracy (MAE between predicted and experimental retention times). Export model weights and generate predictions as a CSV table (molecule_id, predicted_rt, experimental_rt, absolute_error) for downstream metabolite identification workflows.

## Related tools

- **RT-Transformer** (Pretrained encoder–decoder model that combines fingerprint and molecular graph data to predict retention times; serves as the base for transfer learning.) — https://github.com/01dadada/RT-Transformer
- **torch** (Deep learning framework for model loading, layer freezing, optimizer configuration, and backpropagation during fine-tuning.)
- **torch_geometric** (Graph neural network library used to convert molecular structures to graph representations and apply graph convolution layers.)
- **rdkit-pypi** (Chemistry informatics library used to parse InChI strings, generate molecular fingerprints, and construct graph data from molecules.)
- **scikit-learn** (Metrics library for computing MAE, RMSE, and other validation statistics on predicted vs. experimental retention times.)
- **PredRet** (Online repository hosting chromatographic datasets with molecular structures and retention time annotations for diverse target methods.) — http://predret.org/

## Examples

```
python ./transfer.py  # after preparing target data as 'data.csv' with 'InChI' and 'RT' columns and downloading pretrained model checkpoint
```

## Evaluation signals

- Mean absolute error (MAE) between predicted and experimental retention times on the held-out test set is below a domain-acceptable threshold (typically <1–2 min for liquid chromatography).
- Validation MAE converges and does not increase over training epochs, indicating no overfitting to the target dataset.
- Cross-method prediction accuracy (MAE computed across different chromatographic conditions in the test set) remains consistent, confirming transferability.
- Output CSV contains no missing values and all predicted retention times fall within the experimental range of the target dataset.
- Model weights export successfully and can be loaded into an inference script without shape mismatches or dtype errors.

## Limitations

- Transfer learning may fail if the target chromatographic method employs fundamentally different ionization modes, solvents, or column chemistries not represented in the SMRT pretraining data.
- Current retention time prediction methods lack sufficient scalability to transfer from one specific chromatographic method to another without domain-specific tuning.
- If the target dataset is very small (<100 samples), overfitting to target-specific noise is likely even with frozen early layers; consider using regularization or data augmentation.
- Predictions inherit systematic biases from the pretraining distribution; performance may degrade on out-of-distribution molecules or metabolites structurally distinct from the SMRT training set.

## Evidence

- [other] Freeze or partially unfreeze early layers of the RT-Transformer encoder and configure a new task-specific head for the target chromatographic method.: "Freeze or partially unfreeze early layers of the RT-Transformer encoder and configure a new task-specific head for the target chromatographic method."
- [other] Train the adapted model on the PredRet dataset using torch with a mean absolute error or root mean squared error loss function, monitoring validation performance with scikit-learn metrics.: "Train the adapted model on the PredRet dataset using torch with a mean absolute error or root mean squared error loss function, monitoring validation performance with scikit-learn metrics."
- [other] Evaluate the transfer-learned model on a held-out test set from the PredRet data and compute cross-method prediction accuracy (e.g., mean absolute error between predicted and experimental retention times).: "Evaluate the transfer-learned model on a held-out test set from the PredRet data and compute cross-method prediction accuracy (e.g., mean absolute error between predicted and experimental retention"
- [intro] Liquid chromatography retention times prediction can assist in metabolite identification, which is a critical task and challenge in non-targeted metabolomics.: "Liquid chromatography retention times prediction can assist in metabolite identification, which is a critical task and challenge in non-targeted metabolomics."
- [intro] Current retention time prediction methods lack sufficient scalability to transfer from one specific chromatographic method to another: "Current retention time prediction methods lack sufficient scalability to transfer from one specific chromatographic method to another"
- [readme] Prepare your dataset as a csv file which has "InChI" and "RT" columns. Rename it as "data.csv" at the root directory. download the pre-trained model from huggingface. Run transfer.py: "Prepare your dataset as a csv file which has "InChI" and "RT" columns. Rename it as "data.csv" at the root directory. download the pre-trained model from huggingface. Run transfer.py"
