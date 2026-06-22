---
name: retention-time-prediction-chromatography
description: Use when you have a new chromatographic dataset with molecular structures (as InChI or SMILES) and experimentally measured retention times, and you want to predict retention times for unannotated metabolites or validate predictions on a held-out test set without retraining from scratch.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - Python
  - torch
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - scikit-learn
  - tqdm
  - RT-Transformer
  - PyTorch
  - RDKit (rdkit-pypi)
  - torch_geometric
  - torch-scatter, torch-sparse, torch-cluster
  techniques:
  - LC-MS
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

# retention-time-prediction-chromatography

## Summary

Transfer a pretrained RT-Transformer model from the SMRT dataset to predict liquid chromatography retention times on new chromatographic methods represented in datasets like PredRet. This skill enables scalable retention time prediction across different chromatographic conditions to assist metabolite identification in non-targeted metabolomics.

## When to use

You have a new chromatographic dataset with molecular structures (as InChI or SMILES) and experimentally measured retention times, and you want to predict retention times for unannotated metabolites or validate predictions on a held-out test set without retraining from scratch. This is particularly valuable when your chromatographic method differs from the SMRT training conditions but you have enough labeled samples (typically hundreds to thousands) to fine-tune the pretrained encoder.

## When NOT to use

- Your chromatographic method is already represented in the SMRT training set with sufficient coverage — use direct inference without transfer learning instead.
- You have fewer than ~100 labeled molecules in your target dataset — insufficient data to reliably fine-tune the model without severe overfitting.
- Your input molecules are not representable as valid InChI or SMILES strings, or your retention times contain missing values or extreme outliers not preprocessed for model input.

## Inputs

- Pretrained RT-Transformer model checkpoint (PyTorch .pth file)
- Target dataset CSV file with 'InChI' and 'RT' columns
- Molecular structures as InChI strings or SMILES
- Experimental retention time annotations (numeric, in minutes or seconds)

## Outputs

- Fine-tuned RT-Transformer model weights (PyTorch checkpoint)
- Predictions CSV with columns: molecule_id, predicted_rt, experimental_rt, absolute_error
- Validation metrics: mean absolute error, root mean squared error, cross-method prediction accuracy

## How to apply

Load the pretrained RT-Transformer checkpoint (best_state_dict.pth or best_state_download_dict.pth from HuggingFace) and your target dataset as a CSV with 'InChI' and 'RT' columns. Preprocess molecules by generating molecular fingerprints and graph representations using RDKit and converting them to PyTorch tensors compatible with torch_geometric layers. Freeze or partially unfreeze early transformer encoder layers and replace the task-specific head; train on the target dataset using mean absolute error or root mean squared error loss, monitoring validation performance with scikit-learn metrics. Evaluate on a held-out test set by computing mean absolute error between predicted and experimental retention times. Export predictions as a CSV with columns: molecule_id, predicted_rt, experimental_rt, absolute_error.

## Related tools

- **RT-Transformer** (Pretrained transformer-based model combining fingerprints and molecular graph representations for retention time prediction; loaded and fine-tuned on target chromatographic data.) — https://github.com/01dadada/RT-Transformer
- **PyTorch** (Deep learning framework for loading checkpoint, training loop, loss computation, and gradient updates during transfer learning.)
- **RDKit (rdkit-pypi)** (Generates molecular fingerprints and converts InChI/SMILES to molecular graph representations for encoder input.)
- **torch_geometric** (Graph neural network library providing graph convolution layers and batch processing for molecular graph inputs.)
- **scikit-learn** (Computes validation metrics (mean absolute error, root mean squared error) to monitor transfer learning performance.)
- **torch-scatter, torch-sparse, torch-cluster** (Low-level primitives for efficient sparse tensor operations and graph batching in torch_geometric.)

## Examples

```
python transfer.py
```

## Evaluation signals

- Mean absolute error (MAE) on held-out test set is ≤ 0.5–1.0 minute (or comparable threshold for your chromatographic method), indicating prediction accuracy within typical retention time variance.
- Validation loss converges and does not diverge after 10–20 epochs, demonstrating stable fine-tuning without catastrophic forgetting of pretrained features.
- Cross-method prediction accuracy: predictions on chromatographic methods not seen during pretraining show significant improvement over predictions from an unfrozen baseline, confirming successful transfer.
- CSV output contains no null values in predicted_rt, experimental_rt, or absolute_error columns, and absolute_error values are non-negative and within expected range (0–5 minutes for typical LC).
- Comparison of predictions before and after transfer learning shows material reduction in MAE on the target dataset, quantifying the benefit of the pretrained initialization.

## Limitations

- Transfer learning assumes sufficient overlap between molecular space in SMRT (pretraining) and the target chromatographic dataset; extreme novel scaffolds may transfer poorly.
- Different chromatographic conditions (column chemistry, temperature, pH, solvent gradient) produce different retention times for the same metabolite; the model must see representative diversity in training data to generalize.
- Current retention time prediction methods lack sufficient scalability to transfer from one specific chromatographic method to another — if your method is drastically different (e.g., supercritical fluid chromatography vs. reverse-phase LC), additional domain adaptation may be needed.
- Requires clean, well-annotated input data with valid InChI strings and accurate retention time labels; incomplete or mislabeled molecules degrade model performance.
- Model predictions reflect the chromatographic conditions and metabolite coverage present in both SMRT and the target dataset; predictions for metabolites outside those chemical spaces are unreliable.

## Evidence

- [readme] Liquid chromatography retention times prediction can assist in metabolite identification, which is a critical task and challenge in non-targeted metabolomics: "Liquid chromatography retention times prediction can assist in metabolite identification, which is a critical task and challenge in non-targeted metabolomics."
- [readme] Different chromatographic conditions result in different retention times for the same metabolite: "different chromatographic conditions may result in different retention times for the same metabolite"
- [readme] Current methods lack sufficient scalability to transfer across chromatographic methods: "Current retention time prediction methods lack sufficient scalability to transfer from one specific chromatographic method to another"
- [readme] Transfer learning workflow: load pretrained checkpoint, prepare target dataset as CSV with InChI and RT columns, download pretrained model, run transfer.py: "Prepare your dataset as a csv file which has "InChI" and "RT" columns. Rename it as "data.csv" at the root directory. download the pre-trained model from [huggingface]. Run transfer.py"
- [other] Model evaluation via held-out test set and cross-method prediction accuracy using retention time metrics: "Evaluate the transfer-learned model on a held-out test set from the PredRet data and compute cross-method prediction accuracy (e.g., mean absolute error between predicted and experimental retention"
- [other] Output format: CSV table with molecule_id, predicted_rt, experimental_rt, absolute_error: "Export model weights and generate predictions for test molecules as a CSV table with columns: molecule_id, predicted_rt, experimental_rt, absolute_error."
- [readme] Datasets: SMRT for pretraining, PredRet for transfer learning: "The SMRT dataset is collect from [this paper]. Datasets for transfer learning is download from [PredRet]"
- [readme] Model combines fingerprint and molecular graph representations: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output."
