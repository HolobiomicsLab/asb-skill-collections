---
name: feature-ablation-analysis
description: Use when when you have a trained GNN model for molecular property prediction
  (e.g., collision cross section) and need to identify which graph structural features—atomic
  properties, bond types, or higher-order graph descriptors—are driving the model's
  predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_2840
  tools:
  - PyTorch or TensorFlow
  - PyTorch
  - TensorFlow
  - RDKit
  - enveda/ccs-prediction repository
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

# feature-ablation-analysis

## Summary

Systematically remove or mask individual molecular structural features (node and edge attributes) from graph neural network inputs and measure the resulting change in predicted collision cross section, enabling post-hoc attribution analysis to rank features by importance for model predictions.

## When to use

When you have a trained GNN model for molecular property prediction (e.g., collision cross section) and need to identify which graph structural features—atomic properties, bond types, or higher-order graph descriptors—are driving the model's predictions. Use this when model interpretability is required to validate whether predictions align with chemical intuition or to discover novel structure–property relationships.

## When NOT to use

- Model is a simple baseline (e.g., linear regression or random forest) that does not require deep post-hoc interpretation
- Input is already a hand-crafted molecular descriptor table; ablation is designed for learned graph representations, not engineered feature sets
- Test set is too small (<50 molecules) to aggregate robust ablation statistics across the population

## Inputs

- Trained GNN model weights (PyTorch or TensorFlow checkpoint)
- Molecular graph representations with node and edge feature tensors
- Test set molecules (SMILES strings or RDKit molecule objects)
- Ground-truth collision cross section values (numeric)
- 3D coordinates (optional, if model was trained with coordinates)

## Outputs

- Ranked feature-importance table (feature name, ablation score, gradient score, contribution rank)
- Feature-importance bar plot or heatmap visualization
- Ablation score matrix (features × molecules)
- Gradient-based saliency maps (node-level and edge-level attributions)

## How to apply

Load trained GNN model weights and molecular graph representations from the repository. Select a representative test set of molecules with ground-truth CCS values. Systematically ablate individual node features (e.g., atomic number, charge, hybridization) and edge features (e.g., bond type, bond order) by masking or removing them, then measure the change in predicted CCS value for each ablation. Compute gradient-based saliency maps using backpropagation through the trained model with respect to input node and edge features as an alternative or complementary ranking. Aggregate ablation and gradient scores across the test set to rank features by absolute contribution magnitude. Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution magnitude to identify the top structural drivers.

## Related tools

- **PyTorch** (Framework for implementing gradient-based backpropagation through the trained GNN model to compute saliency maps and ablation forward passes)
- **TensorFlow** (Alternative framework for implementing gradient-based backpropagation through the trained GNN model to compute saliency maps and ablation forward passes)
- **RDKit** (Parse and manipulate SMILES strings into molecular graph representations; generate node and edge feature vectors for input to ablation)
- **enveda/ccs-prediction repository** (Source of pre-trained GNN model weights, molecular graph utilities, and example test sets (METLIN-CCS and CCSBase) formatted for ablation analysis) — https://github.com/enveda/ccs-prediction

## Evaluation signals

- Ablation scores are non-negative and ranked in descending order by magnitude; top-ranked features have the largest impact on CCS prediction changes
- Gradient-based saliency maps and ablation rankings show consistent agreement on which features are important (high correlation between methods)
- Test-set aggregated ablation scores are stable (low variance across random subsamples of the test set), indicating robust feature rankings
- Top-ranked features align with known chemical determinants of ion mobility (e.g., molecular weight, polarity, cross-sectional area), validating model interpretability
- Ablated features with zero or near-zero importance score do not alter predictions when removed, confirming their non-contribution to the model

## Limitations

- Ablation assumes feature independence; masking one feature does not account for interaction effects with other features, potentially underestimating or overestimating importance of correlated structural properties
- Gradient-based saliency maps are sensitive to model architecture and training dynamics; poorly converged or overfit models may produce unstable or misleading gradients
- Test-set results are specific to the molecular distribution used; feature importance may differ for out-of-distribution compounds or different ion-adduct types (e.g., [M+H]+ vs. [M+Na]+)
- Computational cost scales with test-set size and number of features; large graphs or many ablations may be slow on CPU-only hardware

## Evidence

- [other] Apply node and edge feature ablation by systematically removing or masking individual structural features and measuring the change in predicted CCS value.: "Apply node and edge feature ablation by systematically removing or masking individual structural features and measuring the change in predicted CCS value."
- [other] Compute gradient-based saliency maps with respect to input node and edge features using backpropagation through the trained model.: "Compute gradient-based saliency maps with respect to input node and edge features using backpropagation through the trained model."
- [other] Aggregate ablation and gradient scores across the test set to rank features by importance.: "Aggregate ablation and gradient scores across the test set to rank features by importance."
- [other] Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution magnitude.: "Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution magnitude."
- [other] Load trained GNN model weights and molecular graph representations from the repository (enveda/ccs-prediction).: "Load trained GNN model weights and molecular graph representations from the repository (enveda/ccs-prediction)."
