---
name: graph-neural-network-model-inference
description: Use when you have a trained GNN model (stored as .h5 weights) and molecular graph representations (SMILES strings and/or 3D coordinates), and you need to compute predicted CCS values or perform feature importance analysis via ablation or gradient-based saliency mapping.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  tools:
  - PyTorch or TensorFlow
  - PyTorch
  - TensorFlow
  - RDKit
derived_from:
- doi: 10.1186/s13321-024-00899-w
  title: mol2ccs
evidence_spans:
- graph neural networks
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
---

# graph-neural-network-model-inference

## Summary

Load a trained graph neural network model and use it to generate predictions on molecular structures represented as graphs. This skill enables post-hoc analysis of GNN predictions, such as attribution studies to identify which molecular features drive collision cross section predictions.

## When to use

You have a trained GNN model (stored as .h5 weights) and molecular graph representations (SMILES strings and/or 3D coordinates), and you need to compute predicted CCS values or perform feature importance analysis via ablation or gradient-based saliency mapping.

## When NOT to use

- Input molecules lack SMILES or 3D coordinate information (required to build graph representations).
- Model weights are not available or are incompatible with the test set structure.
- You only need raw predictions without interpretability; simpler model serving infrastructure suffices.

## Inputs

- Trained GNN model weights (.h5 file)
- Test set molecules (Parquet or CSV with SMILES, 3D coordinates, adduct, ground-truth CCS)
- Model parameter configuration (JSON)
- RDKit-compatible molecular graph representations

## Outputs

- Predicted CCS values for test molecules
- Feature importance scores (node and edge level)
- Ablation or gradient saliency maps
- Ranked feature-importance table (CSV or DataFrame)
- Feature importance visualization (bar plot or heatmap)

## How to apply

Load the trained GNN model weights from disk (e.g., .h5 file). Prepare a test set of molecules in tabular format (Parquet or CSV) with columns for SMILES, optional 3D coordinates, adduct type, and ground-truth CCS values. Convert SMILES and coordinates into molecular graph representations using RDKit. Pass the graph batch through the loaded model to obtain predicted CCS values. For feature importance, systematically ablate (mask or remove) individual node or edge features and measure the change in predicted CCS, or compute gradient-based saliency maps via backpropagation through the model. Aggregate importance scores across the test set and rank features by contribution magnitude.

## Related tools

- **PyTorch** (Framework for loading and executing the trained GNN model and performing backpropagation-based gradient saliency computation)
- **TensorFlow** (Alternative framework for loading and executing the trained GNN model and computing gradients for feature attribution)
- **RDKit** (Convert SMILES and 3D coordinates to molecular graph representations (nodes, edges, features) for inference)

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --model-output-file "model/train-metlin-test-metlin.h5" --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs" --coordinates-present
```

## Evaluation signals

- Predicted CCS values are within physically plausible range (literature-reported CCS for analogous molecules).
- Ablation of known structurally important features (e.g., functional groups or heteroatom counts) causes larger CCS prediction changes than ablation of inert features.
- Feature importance rankings are consistent across subsets of the test set (stable aggregation).
- Gradient saliency maps highlight chemically interpretable substructures (e.g., polar groups, ring systems) rather than noise.
- Test set predictions show lower error or better generalization metrics than baseline models (SigmaCCS, GraphCCS) on held-out molecules.

## Limitations

- Model generalizability depends on training data domain; predictions on chemical classes not well represented in training (METLIN-CCS or CCSBase) may be less reliable.
- Feature importance analysis assumes the ablation or gradient method is faithful to the model; some feature interactions may be missed or misattributed.
- 3D coordinates, when required, may introduce conformer-dependent bias; results may vary if different conformer generation strategies are used.
- Attribution methods are post-hoc and do not guarantee causality; identified features are correlative with prediction changes.
- Missing SMILES or coordinate data requires model to generate 3D coordinates internally, adding preprocessing uncertainty.

## Evidence

- [other] Load trained GNN model weights and molecular graph representations from the repository: "Load trained GNN model weights and molecular graph representations from the repository (enveda/ccs-prediction)."
- [other] Apply node and edge feature ablation and gradient saliency to identify key structural drivers: "Apply node and edge feature ablation by systematically removing or masking individual structural features and measuring the change in predicted CCS value. Compute gradient-based saliency maps with"
- [other] Ranking features by importance across test molecules: "Aggregate ablation and gradient scores across the test set to rank features by importance. Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution"
- [readme] Input data format and columns required for training and inference: "train-input-file is the training set (see notebooks/data_processing/2_data_splits.ipynb for details on the format). test set (see notebooks/data_processing/2_data_splits.ipynb for details on the"
- [readme] 3D coordinate handling during model inference: "coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates)"
