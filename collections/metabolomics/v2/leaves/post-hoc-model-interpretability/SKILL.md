---
name: post-hoc-model-interpretability
description: Use when after training a GNN model on molecular structures with continuous
  targets (e.g., CCS values), when you need to understand which node-level (atom)
  or edge-level (bond) features contribute most to individual or aggregate predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3938
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3315
  tools:
  - PyTorch or TensorFlow
  - PyTorch
  - TensorFlow
  - RDKit
  techniques:
  - ion-mobility-MS
  license_tier: open
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

# Post-hoc model interpretability

## Summary

Apply node and edge feature ablation and gradient-based saliency mapping to trained graph neural networks to identify which molecular structural features most strongly drive predictions of collision cross section. This enables attribution analysis of black-box GNN models after training is complete.

## When to use

After training a GNN model on molecular structures with continuous targets (e.g., CCS values), when you need to understand which node-level (atom) or edge-level (bond) features contribute most to individual or aggregate predictions. Use this when stakeholders or downstream applications require explainability of model decisions, or when validating that the model has learned chemically meaningful relationships rather than spurious correlations.

## When NOT to use

- Model is already a transparent, interpretable baseline (e.g., linear regression, decision tree) — direct inspection of coefficients or splits is simpler and more efficient.
- Test set is very small (< 10 molecules) — aggregated importance statistics will be unreliable and prone to noise.
- The goal is real-time prediction explanation for individual samples in production — post-hoc analysis is batch-oriented and computationally expensive for per-query latency constraints.

## Inputs

- Trained GNN model (PyTorch or TensorFlow weights, .h5 format or equivalent)
- Molecular graph representations (node features, edge features, adjacency matrices for test set molecules)
- Test set with SMILES, 3D coordinates (if used during training), and ground-truth CCS values (parquet or equivalent tabular format)
- Model parameters and training configuration (JSON)

## Outputs

- Ranked feature-importance table (CSV or DataFrame with feature names and importance scores)
- Ablation scores per feature (numeric ranking of prediction delta per ablated feature)
- Gradient-based saliency maps (per-feature gradient magnitudes averaged across test set)
- Visualization: bar plot or heatmap of feature importance sorted by contribution magnitude

## How to apply

Load the trained GNN model weights and molecular graph representations (node features, edge features, adjacency) from a test set with ground-truth CCS values. Apply systematic feature ablation by masking individual node or edge features and measuring the change in predicted CCS; rank features by magnitude of prediction change. In parallel, compute gradient-based saliency maps by backpropagating through the model with respect to input node and edge features using automatic differentiation. Aggregate ablation and gradient scores across the test set to obtain a global feature importance ranking. Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution magnitude. The rationale is that ablation directly measures predictive impact while gradients capture local sensitivity; combined, they provide complementary signal about which structural drivers the model relies on.

## Related tools

- **PyTorch** (Framework for loading trained GNN weights, executing forward passes, and computing gradients via backpropagation for saliency map generation)
- **TensorFlow** (Alternative framework for loading trained GNN weights and computing gradient-based saliency maps via automatic differentiation)
- **RDKit** (Molecular toolkit for parsing SMILES, constructing and manipulating molecular graphs, and extracting node/edge feature descriptors from structures)

## Evaluation signals

- Feature importance scores are stable and reproducible across multiple runs with the same random seed; ablation and gradient scores show consistent ranking.
- Ablated features with highest importance scores correspond to chemically intuitive structural patterns (e.g., functional groups known to affect ion-neutral interactions or charge stabilization in collision cross section).
- Gradient saliency maps show non-zero sensitivity only on relevant parts of the molecular graph (e.g., heteroatoms, polar groups, stereogenic centers) and zero or near-zero gradients on invariant or irrelevant substructures.
- Aggregate feature importance across the test set exhibits a power-law or Pareto distribution (a small number of features explain most variance), consistent with sparse chemical drivers; if all features have similar importance, the model may not have learned meaningful structure.
- Removing the top-N ranked features (e.g., top 10% by importance) degrades test-set prediction accuracy more sharply than removing random features, validating that the ranking captures true predictive contributions.

## Limitations

- Ablation and gradient-based importance are model-specific and do not reflect ground-truth chemical causality; a well-trained model may rely on spurious correlations if the training data distribution is biased.
- Feature importance is data-set dependent: features ranked as highly important on one test set (e.g., METLIN-CCS) may rank differently on another (e.g., CCSBase), reflecting distribution shift and generalization gaps.
- Gradient-based saliency is most reliable near the decision boundary; in regions of high model confidence (flat loss landscape), gradients may be numerically small and unreliable, especially for ReLU-activated networks.
- Computational cost scales with test set size and model complexity; gradient computation via backpropagation and per-feature ablation (O(# features) forward passes) can be prohibitive for very large graphs or models.
- The choice of ablation strategy (masking, zeroing, replacing with mean) affects results; no universally agreed-upon ablation scheme exists for graph neural networks, so results are sensitive to implementation details.

## Evidence

- [other] Apply node and edge feature ablation by systematically removing or masking individual structural features and measuring the change in predicted CCS value.: "Apply node and edge feature ablation by systematically removing or masking individual structural features and measuring the change in predicted CCS value."
- [other] Compute gradient-based saliency maps with respect to input node and edge features using backpropagation through the trained model.: "Compute gradient-based saliency maps with respect to input node and edge features using backpropagation through the trained model."
- [other] Aggregate ablation and gradient scores across the test set to rank features by importance.: "Aggregate ablation and gradient scores across the test set to rank features by importance."
- [other] Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution magnitude.: "Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution magnitude."
- [other] This repository contains code and data for evaluating graph neural networks trained to predict collision cross section, enabling post-hoc attribution analysis to identify key structural drivers.: "This repository contains code and data for evaluating graph neural networks trained to predict collision cross section, enabling post-hoc attribution analysis to identify key structural drivers."
