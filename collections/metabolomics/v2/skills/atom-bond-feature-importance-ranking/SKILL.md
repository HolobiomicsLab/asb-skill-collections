---
name: atom-bond-feature-importance-ranking
description: Use when you have a trained GNN model for molecular property prediction (such as CCS) and need to understand which atomic and bond features are most influential in driving predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3318
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

# atom-bond-feature-importance-ranking

## Summary

Post-hoc attribution analysis of graph neural network predictions to identify and rank which molecular structural features (node and edge attributes) drive model predictions of collision cross section. This skill enables interpretation of GNN decision logic through ablation and gradient-based saliency scoring.

## When to use

Apply this skill when you have a trained GNN model for molecular property prediction (such as CCS) and need to understand which atomic and bond features are most influential in driving predictions. Use it to validate model chemistry, identify spurious correlations, or guide feature engineering for downstream molecular design.

## When NOT to use

- Model has not been trained or weights are not available—feature importance requires a fitted model.
- Input is a pre-computed feature importance table or ranking from another method; use this skill only to generate attributions from a neural network.
- Test set is too small (<10–20 molecules) to support reliable aggregated importance ranking across structural diversity.

## Inputs

- Trained GNN model weights (PyTorch .pt or TensorFlow .h5 format)
- Molecular graph representations (node features, edge features, adjacency)
- Test set molecules with SMILES strings and ground-truth CCS values (Parquet or CSV)

## Outputs

- Ranked feature-importance table (CSV or table with feature names and scores)
- Bar plot or heatmap visualization of ablation and/or gradient scores
- Saliency maps or per-molecule feature attribution heatmaps

## How to apply

Load the trained GNN model weights and molecular graph representations (node and edge features encoded from SMILES or 3D coordinates). Select a representative test set of molecules with ground-truth CCS values. Perform systematic node and edge feature ablation by masking or removing individual features and measuring the change in predicted CCS value—features with larger prediction deltas are more important. In parallel, compute gradient-based saliency maps by backpropagating loss gradients with respect to input node and edge feature tensors to quantify local sensitivity. Aggregate ablation scores and gradient magnitudes across the test set (e.g., by mean or median), rank features by importance magnitude, and generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution. Validate that top-ranked features align with known chemistry (e.g., electronegativity, molecular weight contributions) and that ablation sensitivity follows gradient magnitude trends.

## Related tools

- **PyTorch** (Gradient computation via backpropagation and tensor manipulation for saliency map generation)
- **TensorFlow** (Alternative deep-learning framework for model loading and gradient-based attribution)
- **RDKit** (Parsing SMILES, generating molecular graphs, and extracting node/edge chemical features)

## Examples

```
# Load model, select test molecules, ablate features and compute saliency; aggregate and rank by importance.
poetry run python -c "import torch; from ccs_prediction.model import load_model; from ccs_prediction.attribution import ablate_features, compute_saliency; model = load_model('model/train-metlin-test-ccsbase.h5'); test_graphs = load_test_set('ccs-prediction/ccsbase_3d.parquet'); ablation_scores = [ablate_features(model, g) for g in test_graphs]; saliency_maps = [compute_saliency(model, g) for g in test_graphs]; importance = aggregate_and_rank(ablation_scores, saliency_maps); importance.to_csv('feature_importance.csv')"
```

## Evaluation signals

- Top-ranked features correspond to known molecular drivers of CCS (e.g., mass, polarity, cross-sectional geometry); chemistry alignment validates interpretation.
- Ablation scores (prediction delta) correlate positively with gradient magnitudes; divergence suggests confounded importance signals.
- Feature importance distribution is non-uniform and sparse (not uniform across all features), indicating the model has learned selective feature usage rather than distributed reliance.
- Reproducibility: same molecules and model produce identical ablation and gradient scores across independent runs.
- Ablated model predictions degrade gracefully (monotonic increase in error) as top-k features are sequentially removed, rather than collapsing abruptly.

## Limitations

- Gradient-based saliency can be noisy in flat loss regions or for highly non-linear models; smoothing or averaging across multiple seeds may be required.
- Ablation-based importance is sensitive to feature masking strategy (e.g., zero-masking vs. random permutation) and can conflate feature main effects with interactions.
- Feature importance is model-specific and does not directly prove ground-truth causal relationships; highly correlated features may show spurious mutual attribution.
- Computational cost scales with test set size and model depth; large-scale attribution can be expensive for million-molecule datasets.

## Evidence

- [other] Apply node and edge feature ablation by systematically removing or masking individual structural features and measuring the change in predicted CCS value.: "Apply node and edge feature ablation by systematically removing or masking individual structural features and measuring the change in predicted CCS value."
- [other] Compute gradient-based saliency maps with respect to input node and edge features using backpropagation through the trained model.: "Compute gradient-based saliency maps with respect to input node and edge features using backpropagation through the trained model."
- [other] Aggregate ablation and gradient scores across the test set to rank features by importance. Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution magnitude.: "Aggregate ablation and gradient scores across the test set to rank features by importance. Generate a ranked feature-importance table and visualization (bar plot or heatmap) sorted by contribution"
- [other] Load trained GNN model weights and molecular graph representations from the repository: "Load trained GNN model weights and molecular graph representations from the repository (enveda/ccs-prediction)."
- [readme] This repository contains code and data described in detail in our paper (Engler et al., 2024). ... See the commands in the Makefile to train the models.: "This repository contains code and data described in detail in our paper (Engler et al., 2024)."
