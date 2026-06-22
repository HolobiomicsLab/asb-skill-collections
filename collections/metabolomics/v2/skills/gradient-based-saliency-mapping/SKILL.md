---
name: gradient-based-saliency-mapping
description: Use when you have a trained graph neural network model for CCS prediction and need to identify which molecular structural features drive individual predictions or systematic biases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3372
  tools:
  - PyTorch or TensorFlow
  - PyTorch
  - TensorFlow
  - RDKit
  techniques:
  - ion-mobility-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gradient-based-saliency-mapping

## Summary

Compute gradient-based attribution maps that identify which input features (node and edge attributes in molecular graphs) most strongly influence neural network predictions of collision cross section. This post-hoc interpretability method uses backpropagation to quantify the sensitivity of model outputs to perturbations in structural features.

## When to use

Apply this skill when you have a trained graph neural network model for CCS prediction and need to identify which molecular structural features drive individual predictions or systematic biases. Use it after model training is complete to explain why the network assigned a particular CCS value to a molecule, especially when validating generalizability across different molecular datasets (e.g., METLIN-trained models tested on CCSBase).

## When NOT to use

- The trained model is frozen or does not support gradient computation (e.g., compiled with gradient-disabled mode); gradient-based methods require autograd/backprop enabled.
- Input is a simple rule-based or non-differentiable model (e.g., decision trees, random forests); saliency mapping requires continuous, differentiable pathways through the model.
- You have no access to model weights or architecture; gradient-based attribution requires the full computational graph of the trained network.

## Inputs

- Trained GNN model (PyTorch or TensorFlow, saved as .h5 or state_dict)
- Molecular graph representations (node feature tensors, edge feature tensors)
- 3D coordinates (optional, if the model was trained with coordinates_present=True)
- Test set of molecules with SMILES, adduct, and ground-truth CCS values (parquet or CSV format)

## Outputs

- Gradient-based saliency maps (per-molecule gradient tensors with respect to node/edge features)
- Ranked feature-importance table (feature name, mean gradient magnitude, std across test set)
- Feature importance visualization (bar plot or heatmap of top-K features sorted by gradient contribution)
- Aggregated gradient statistics (mean, median, percentile ranks for each molecular feature)

## How to apply

Load the trained GNN model weights and molecular graph representations (node features, edge features, 3D coordinates if available). Select a test set of molecules with ground-truth CCS values. For each molecule, compute the gradient of the predicted CCS value with respect to input node and edge feature tensors using backpropagation through the trained model. Aggregate gradient magnitudes (absolute values) across the test set to rank features by their contribution to predictions. Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by gradient magnitude. Compare gradient rankings across train/test dataset splits to identify whether the model relies on dataset-specific artifacts or generalizable structural patterns.

## Related tools

- **PyTorch** (Enables gradient computation and backpropagation for saliency map generation via torch.autograd.backward() and tensor.grad attribute.)
- **TensorFlow** (Alternative framework for gradient-based attribution using tf.GradientTape() to compute gradients with respect to inputs.)
- **RDKit** (Parses SMILES strings and generates molecular graph representations (atoms, bonds, features) as input to the GNN model.)

## Evaluation signals

- Gradient tensors have the same shape as input node/edge feature tensors; no NaN or Inf values present.
- Aggregated feature-importance rankings are reproducible across multiple runs with fixed random seeds; variance is within expected bounds.
- Top-ranked features align with known chemical drivers of collision cross section (e.g., molecular weight, polar surface area, number of rotatable bonds) when compared to domain literature.
- Gradient saliency maps change systematically across different molecular subsets (e.g., lipids vs. metabolites) and across train/test splits, indicating the model is capturing structure-specific patterns rather than spurious artifacts.
- Feature-importance distributions show no extreme outliers (e.g., single feature > 10× mean gradient); extreme values suggest numerical instability or model saturation.

## Limitations

- Gradient-based saliency maps are sensitive to input normalization and model initialization; features with larger initial scale or weight magnitude may dominate rankings even if causally unimportant.
- Gradients capture local sensitivity around the test point and do not account for interactions between features; a feature with zero gradient locally may still contribute through interactions elsewhere in the input space.
- The interpretation assumes the model has learned meaningful patterns; poorly trained or overfit models may produce gradients that are uninformative or misleading.
- For GNNs trained without 3D coordinates (coordinates_present=False), gradient saliency maps reflect only graph-topology features; structural isomers with different 3D conformations may show identical gradients.
- Aggregation across diverse test molecules may obscure molecule-specific attribution patterns; reporting per-molecule saliency maps alongside aggregate statistics is recommended.

## Evidence

- [other] Apply gradient-based saliency maps with respect to input node and edge features using backpropagation through the trained model.: "Compute gradient-based saliency maps with respect to input node and edge features using backpropagation through the trained model."
- [other] enabling post-hoc attribution analysis to identify key structural drivers: "enabling post-hoc attribution analysis to identify key structural drivers."
- [other] Aggregate ablation and gradient scores across the test set to rank features by importance.: "Aggregate ablation and gradient scores across the test set to rank features by importance."
- [other] Load trained GNN model weights and molecular graph representations from the repository: "Load trained GNN model weights and molecular graph representations from the repository"
- [other] PyTorch or TensorFlow, RDKit: "PyTorch or TensorFlow, RDKit"
