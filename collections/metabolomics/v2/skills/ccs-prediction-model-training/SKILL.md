---
name: ccs-prediction-model-training
description: Use when you have a dataset of SMILES strings with corresponding experimental CCS measurements and want to build a predictive model that can rapidly generate CCS values for new molecules without running expensive ion-mobility spectrometry experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - Python 3
  - RDKit
  - PyTorch
  - PyG
  - pandas
  - NumPy
  - conda
  - pip
  - PyG (PyTorch Geometric)
  - conda/pip
derived_from:
- doi: 10.1002/cem.70040
  title: PACCS
evidence_spans:
- '[python3](https://www.python.org/)'
- '[RDKit](https://rdkit.org/)'
- '[PyTorch](https://pytorch.org/)'
- '[PyG](https://pytorch-geometric.readthedocs.io/en/latest/)'
- '[pandas](https://pandas.pydata.org/)'
- '[NumPy](https://numpy.org/)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_paccs_cq
    doi: 10.1002/cem.70040
    title: PACCS
  dedup_kept_from: coll_paccs_cq
schema_version: 0.2.0
---

# ccs-prediction-model-training

## Summary

Train a deep-learning neural network to predict collision cross section (CCS) from molecular conformers using voxel projected area features as input. This skill enables generation of large-scale, searchable CCS databases by optimizing a PyTorch model on paired molecular structure and experimental CCS ground-truth labels.

## When to use

You have a dataset of SMILES strings with corresponding experimental CCS measurements and want to build a predictive model that can rapidly generate CCS values for new molecules without running expensive ion-mobility spectrometry experiments. Apply this skill when you need to train PACCS on your own curated dataset to optimize model performance for a specific molecular class or charge state (adduct type).

## When NOT to use

- Input molecules are already represented as pre-computed voxel projected area features (feature table) — skip directly to model training without regenerating conformers and features.
- You lack ground-truth experimental CCS labels; use the pretrained PACCS model for inference instead.
- Your molecules have very few conformational degrees of freedom or are highly constrained; voxel projected area may not capture sufficient structural diversity.

## Inputs

- CSV file containing SMILES strings and adduct type labels
- 3D molecular conformer structures (or SMILES from which conformers are generated)
- Ground-truth experimental CCS values (m/z-normalized collision cross section in Ų)

## Outputs

- Trained PyTorch model checkpoint (serialized weights and architecture)
- Per-molecule CCS predictions on test set
- Model performance metrics (RMSE, MAE, R², correlation coefficient)
- Training/validation loss curves and convergence diagnostics

## How to apply

Begin by preparing training, validation, and test datasets (split as 8:1:1 ratio recommended) from your curated CSV file containing SMILES and adduct information. For each molecule, generate 3D conformers using RDKit's ETKDGv3 and MMFF optimization, then compute voxel projected area features (using Fibonacci grid sampling on three coordinate planes xy, xz, yz and averaging). Construct molecular graph representations and encode adduct type as one-hot vectors. Feed these features into a PyTorch neural network model incorporating optional graph-based message passing from PyG. Train the model using appropriate loss function and learning rate scheduling across epochs, validating on the held-out validation set to prevent overfitting. Use the test set only for final evaluation; output per-molecule CCS predictions and aggregate performance metrics (e.g., RMSE, MAE, correlation).

## Related tools

- **RDKit** (Generate 3D molecular conformers and optimize geometry using ETKDGv3 and MMFF force field; construct molecular graph representations) — https://rdkit.org/
- **PyTorch** (Define, instantiate, and train the deep-learning neural network model; manage optimization, loss computation, and backpropagation across training epochs) — https://pytorch.org/
- **PyG (PyTorch Geometric)** (Optionally incorporate graph neural network layers and message-passing schemes for molecular graph representation learning) — https://pytorch-geometric.readthedocs.io/en/latest/
- **pandas** (Load, organize, and manipulate tabular datasets (SMILES, adduct, CCS labels) for train/validation/test split and batch preparation) — https://pandas.pydata.org/
- **NumPy** (Vectorized numerical operations for feature computation, normalization, and array manipulations during data preprocessing) — https://numpy.org/
- **conda/pip** (Manage Python environment and install all required packages from environment.yml or requirements.txt) — https://github.com/yuxuanliao/PACCS

## Examples

```
from PACCS.Training import PACCS_train
PACS_train(input_path='data/curated_dataset.csv', epochs=200, batchsize=32, output_model_path='models/paccs_trained.pt')
```

## Evaluation signals

- Training and validation loss curves should both decrease monotonically (or near-monotonically) across epochs; validation loss should plateau without diverging, indicating absence of overfitting.
- Model performance metrics (RMSE, MAE, R²) on the held-out test set should be consistent with reported baseline performance (~10–20 Ų RMSE for small-molecule CCS depending on charge state).
- Predicted CCS values should be physically plausible (typically in range 50–500 Ų for small organic molecules) and show monotonic correlation with molecular mass and charge.
- Per-molecule prediction residuals (predicted − experimental) should be approximately normally distributed with zero mean; large systematic biases suggest inadequate feature representation.
- Separate evaluation on external test set (from different data source) should not show dramatic degradation compared to internal test set, indicating generalization.

## Limitations

- Model performance depends critically on the quality and size of the curated training dataset; small or biased datasets lead to poor generalization across molecular space.
- Voxel projected area features assume molecules can be adequately represented as rigid structures; conformational flexibility not fully captured by single conformer or ensemble averaging.
- Model trained on molecules within a specific m/z or charge state range may not extrapolate reliably to different adducts or very large/small molecules.
- Hyperparameters (epochs, batch size, learning rate schedule) require tuning for each dataset; no single set of parameters is universally optimal.

## Evidence

- [other] Prepare training, validation, and test datasets using pandas and NumPy, organizing features and corresponding CCS ground-truth labels.: "Prepare training, validation, and test datasets using pandas and NumPy, organizing features and corresponding CCS ground-truth labels."
- [other] Construct and configure a deep-learning neural network model using PyTorch, optionally incorporating graph-based message passing from PyG for molecular representations.: "Construct and configure a deep-learning neural network model using PyTorch, optionally incorporating graph-based message passing from PyG for molecular representations."
- [other] Train the model on the prepared dataset using PyTorch, optimizing for CCS prediction accuracy across epochs with appropriate loss function and learning rate scheduling.: "Train the model on the prepared dataset using PyTorch, optimizing for CCS prediction accuracy across epochs with appropriate loss function and learning rate scheduling."
- [readme] The curated dataset is randomly split into the training, validation, and test sets in a ratio of 8:1:1.: "The curated dataset is randomly split into the training, validation, and test sets in a ratio of 8:1:1."
- [readme] Train the model based on your own training dataset with [Training.py](PACCS/Training.py) function. PACCS_train(input_path, epochs, batchsize, output_model_path): "Train the model based on your own training dataset with [Training.py](PACCS/Training.py) function. PACCS_train(input_path, epochs, batchsize, output_model_path)"
- [readme] ETKDGv3 returns an EmbedParameters object for the ETKDG method - version 3 (macrocycles). EmbedMultipleConfs generates the 3D conformers of molecules. MMFFOptimizeMoleculeConfs optimizes the 3D conformers of molecules.: "ETKDGv3 returns an EmbedParameters object for the ETKDG method - version 3 (macrocycles). EmbedMultipleConfs generates the 3D conformers of molecules. MMFFOptimizeMoleculeConfs optimizes the 3D"
