---
name: molecular-structure-attribution
description: Use when you have a trained GNN model predicting CCS values from molecular
  graphs and need to understand which structural features (node and edge attributes)
  are most influential for specific predictions or across a test set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_0176
  tools:
  - PyTorch or TensorFlow
  - PyTorch
  - TensorFlow
  - RDKit
  - enveda/ccs-prediction
  techniques:
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
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

# molecular-structure-attribution

## Summary

Identify which molecular structural features (atoms, bonds, functional groups) most strongly drive graph neural network predictions of collision cross section (CCS) through ablation and gradient-based attribution. This enables post-hoc interpretation of black-box GNN models trained on molecular graphs.

## When to use

You have a trained GNN model predicting CCS values from molecular graphs and need to understand which structural features (node and edge attributes) are most influential for specific predictions or across a test set. Use this skill when model predictions must be explained to domain experts, when validating whether the model has learned chemically reasonable decision rules, or when identifying which molecular descriptors drive CCS variation.

## When NOT to use

- Model predictions are not available or the trained model cannot be loaded—attribution requires forward passes through the model.
- Input is already a pre-computed feature importance ranking from another method—this skill is for deriving attributions from a trained GNN, not aggregating external rankings.
- You only have SMILES strings without 3D coordinates and the model was trained with coordinates-present=true—the model will attempt to generate 3D structures, but this may introduce noise in attribution if structure generation is unstable.

## Inputs

- Trained GNN model weights (PyTorch or TensorFlow .h5/.pt format)
- Molecular graph representations (node and edge feature tensors)
- Test set of molecules with ground-truth CCS values (parquet or CSV format with SMILES, CCS, adduct columns)
- 3D coordinates (optional, required only if coordinates-present flag is set)

## Outputs

- Ranked feature-importance table (node and edge features sorted by ablation/gradient score)
- Feature importance visualization (bar plot or heatmap)
- Aggregated ablation scores per feature across test set
- Gradient-based saliency maps per feature

## How to apply

Load trained GNN model weights and the corresponding test set of molecules with ground-truth CCS values. Apply two complementary attribution strategies: (1) Node and edge feature ablation—systematically mask or remove individual structural features and measure the change in predicted CCS value; (2) Gradient-based saliency maps—compute gradients of the model output with respect to input node and edge features via backpropagation. Aggregate ablation scores and gradient magnitudes across the test set to rank features by contribution. Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution magnitude. Features with the largest changes in CCS prediction or steepest gradients are most important for the model's decision-making.

## Related tools

- **PyTorch** (Gradient computation and model inference for GNN-based CCS prediction)
- **TensorFlow** (Alternative framework for loading trained GNN models and computing gradients)
- **RDKit** (Molecular graph construction and feature extraction from SMILES)
- **enveda/ccs-prediction** (Source repository containing trained GNN models, molecular graph representations, and example workflows for CCS attribution) — https://github.com/enveda/ccs-prediction

## Examples

```
poetry run python scripts/train-test.py --prefix "train-metlin-test-ccsbase" --train-input-file "ccs-prediction/metlin_train_3d.parquet" --test-input-file "ccs-prediction/ccsbase_3d.parquet" --coordinates-present --smiles-column-name "smiles" --adduct-column-name "adduct" --ccs-column-name "ccs"
```

## Evaluation signals

- Feature importance scores sum to a meaningful total magnitude (e.g., within expected bounds of model gradient norms or ablation-induced CCS changes).
- Top-ranked features correspond to known chemically important structural descriptors for CCS (e.g., molecular weight, degree, aromaticity, polar surface area).
- Ablation and gradient-based rankings show high correlation or agreement on top-k features, indicating robustness of the attribution method.
- Feature importance distribution is sparse (few dominant features) or dense (many moderate contributions) in alignment with model architecture and training data complexity.
- Ablation-induced CCS changes are monotonic with feature importance rank—removing high-importance features causes larger CCS prediction shifts than removing low-importance features.

## Limitations

- Attribution quality depends on test set representativeness; biased or small test sets may yield misleading feature rankings.
- Gradient-based saliency maps can be noisy in models with ReLU activations or dropout; smoothing or integrated gradients may be needed for stability.
- Ablation studies assume feature independence; masking one feature may change the marginal effect of other features due to nonlinearities in the GNN.
- Results are model-specific; different GNN architectures, training datasets, or hyperparameters (e.g., dropout rate 0.1) may produce different attributions for the same molecules.
- 3D coordinate quality affects downstream attributions; if coordinates are generated on-the-fly from SMILES, errors in structure generation propagate into feature representations.

## Evidence

- [other] Apply node and edge feature ablation by systematically removing or masking individual structural features and measuring the change in predicted CCS value.: "Apply node and edge feature ablation by systematically removing or masking individual structural features and measuring the change in predicted CCS value."
- [other] Compute gradient-based saliency maps with respect to input node and edge features using backpropagation through the trained model.: "Compute gradient-based saliency maps with respect to input node and edge features using backpropagation through the trained model."
- [other] Aggregate ablation and gradient scores across the test set to rank features by importance.: "Aggregate ablation and gradient scores across the test set to rank features by importance."
- [other] Load trained GNN model weights and molecular graph representations from the repository (enveda/ccs-prediction).: "Load trained GNN model weights and molecular graph representations from the repository (enveda/ccs-prediction)."
- [readme] coordinates-column-name column name of the 3d coordinates for each smiles, coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates): "coordinates-present if the coordinates are present (if not given, the model will use the smiles to generate the 3d coordinates)"
