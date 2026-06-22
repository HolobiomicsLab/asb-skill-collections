---
name: pytorch-neural-network-training
description: Use when you have a PyTorch model architecture (pretrained or freshly initialized), a dataset with molecular structures (as InChI strings or graph representations) and continuous target values (retention times in minutes), and you need to optimize model weights via supervised learning.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3391
  tools:
  - Python
  - torch
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - scikit-learn
  - tqdm
  - torch_geometric
  - rdkit-pypi
  - RT-Transformer
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# PyTorch Neural Network Training

## Summary

Train or fine-tune a PyTorch neural network on labeled molecular data using backpropagation with regression loss functions and validation monitoring. This skill is essential when adapting pretrained models (e.g., RT-Transformer) to new chromatographic datasets or retraining from scratch on retention time prediction tasks.

## When to use

You have a PyTorch model architecture (pretrained or freshly initialized), a dataset with molecular structures (as InChI strings or graph representations) and continuous target values (retention times in minutes), and you need to optimize model weights via supervised learning. Triggers include: (1) transfer learning from SMRT to PredRet chromatographic methods; (2) retraining RT-Transformer on a custom CSV with 'InChI' and 'RT' columns; (3) fine-tuning with partial layer freezing when target chromatographic conditions differ from source data.

## When NOT to use

- Input is classification (e.g., retention time bins or categorical classes instead of continuous values); use cross-entropy loss and classification metrics instead.
- Dataset lacks sufficient labeled examples (<50 molecules) or contains severe class imbalance; risk of overfitting and poor generalization.
- Model architecture is already fully trained and you only need inference; use evaluation/prediction skill instead of retraining.

## Inputs

- PyTorch model checkpoint (.pth file)
- CSV dataset with columns: InChI, RT (retention time in minutes)
- Molecular fingerprint or graph tensor representations (torch.Tensor or torch_geometric.data.Data objects)
- Train/validation/test split indices or fractions

## Outputs

- Trained model weights (.pth checkpoint file)
- Validation and test loss curves (MAE, RMSE per epoch)
- Predictions CSV with columns: molecule_id, predicted_rt, experimental_rt, absolute_error
- Summary metrics: mean absolute error and root mean squared error on held-out test set

## How to apply

Load the pretrained model checkpoint and dataset (CSV with 'InChI' and 'RT' columns) using PyTorch and RDKit. Preprocess molecules by generating molecular fingerprints or graph representations via RDKit and convert to PyTorch tensors using torch_geometric for graph convolution inputs. Configure training hyperparameters: choose a regression loss (mean absolute error or root mean squared error), an optimizer (typically Adam), and a batch size. Optionally freeze early encoder layers if performing transfer learning. Train over multiple epochs, computing validation loss on a held-out fraction at each epoch to monitor for overfitting. Log metrics (MAE, RMSE) using scikit-learn and track progress with tqdm. Export the best model checkpoint (by validation performance) and generate predictions on the test set as a CSV with columns: molecule_id, predicted_rt, experimental_rt, absolute_error.

## Related tools

- **torch** (Core framework for defining, loading, and training neural network models; handles backpropagation and parameter optimization.) — https://pytorch.org
- **torch_geometric** (Converts molecular structures to graph tensor representations and provides graph convolution layers for RT-Transformer encoder.) — https://github.com/pyg-team/pytorch_geometric
- **rdkit-pypi** (Generates molecular fingerprints and parses InChI strings to graph/fingerprint inputs for model training.) — https://www.rdkit.org
- **scikit-learn** (Computes validation and test metrics (MAE, RMSE) and supports train/test splitting.) — https://scikit-learn.org
- **tqdm** (Displays progress bars during training epochs to monitor convergence and runtime.) — https://github.com/tqdm/tqdm
- **RT-Transformer** (Reference model implementation combining fingerprint and molecular graph data for retention time prediction.) — https://github.com/01dadada/RT-Transformer

## Examples

```
python ./transfer.py  # Executes fine-tuning on data.csv with pretrained RT-Transformer checkpoint; or python ./train.py  # Retrains from scratch
```

## Evaluation signals

- Validation loss (MAE or RMSE) monotonically decreases or plateaus over epochs; sharp increases after plateau indicate overfitting.
- Test set mean absolute error between predicted and experimental retention times is <2 minutes (typical for chromatographic prediction; article context implies this is acceptable tolerance).
- Predictions CSV is well-formed: all rows have non-null predicted_rt values, absolute_error column contains non-negative values, and record count matches test set size.
- Exported .pth checkpoint can be reloaded without errors and produces identical predictions on the same input molecules (determinism check).
- Cross-method evaluation: if transfer learning to PredRet from SMRT, report separate MAE/RMSE per chromatographic method to confirm scalability across conditions.

## Limitations

- Different chromatographic conditions may result in different retention times for the same metabolite; transfer learning may not generalize across all methods without adequate target-domain data or domain adaptation.
- Requires molecular structures in standardized format (InChI); malformed or missing structures will cause preprocessing failures.
- Model performance is sensitive to hyperparameter choices (learning rate, batch size, layer freezing strategy in transfer learning); no automated hyperparameter tuning is provided in the README.
- Training on small datasets (<100 molecules) risks overfitting; the article does not discuss minimum dataset size or regularization strategies for limited data.

## Evidence

- [other] Freeze or partially unfreeze early layers of the RT-Transformer encoder and configure a new task-specific head for the target chromatographic method.: "Freeze or partially unfreeze early layers of the RT-Transformer encoder and configure a new task-specific head for the target chromatographic method."
- [other] Train the adapted model on the PredRet dataset using torch with a mean absolute error or root mean squared error loss function, monitoring validation performance with scikit-learn metrics.: "Train the adapted model on the PredRet dataset using torch with a mean absolute error or root mean squared error loss function, monitoring validation performance with scikit-learn metrics."
- [other] Evaluate the transfer-learned model on a held-out test set from the PredRet data and compute cross-method prediction accuracy (e.g., mean absolute error between predicted and experimental retention times).: "Evaluate the transfer-learned model on a held-out test set from the PredRet data and compute cross-method prediction accuracy (e.g., mean absolute error between predicted and experimental retention"
- [readme] Prepare your dataset as a csv file which has "InChI" and "RT" columns.: "Prepare your dataset as a csv file which has "InChI" and "RT" columns."
- [readme] Different chromatographic conditions may result in different retention times for the same metabolite. Current retention time prediction methods lack sufficient scalability to transfer from one specific chromatographic method to another: "Different chromatographic conditions may result in different retention times for the same metabolite. Current retention time prediction methods lack sufficient scalability to transfer"
