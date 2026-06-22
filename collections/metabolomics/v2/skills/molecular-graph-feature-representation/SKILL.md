---
name: molecular-graph-feature-representation
description: Use when when you have molecular structures (as SMILES, SDF, or graph adjacency) and need to predict continuous properties (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3704
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - chemprop
  - chemprop-IR
  - RDKit
derived_from:
- doi: 10.1021/acs.jcim.1c00055
  title: Chemprop-IR
evidence_spans:
- extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemprop_ir_cq
    doi: 10.1021/acs.jcim.1c00055
    title: Chemprop-IR
  dedup_kept_from: coll_chemprop_ir_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.1c00055
  all_source_dois:
  - 10.1021/acs.jcim.1c00055
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-graph-feature-representation

## Summary

Extract and transform molecular structures into learned graph-based feature representations suitable for property prediction tasks. This skill bridges molecular chemistry (atoms, bonds, connectivity) and neural network inputs by converting SMILES or molecular graphs into featurized node and edge embeddings that capture chemical semantics for downstream message passing architectures.

## When to use

When you have molecular structures (as SMILES, SDF, or graph adjacency) and need to predict continuous properties (e.g., infrared spectral intensities, molecular properties) using message passing neural networks, and the raw chemical connectivity alone is insufficient — you must learn or apply feature representations that encode chemical context.

## When NOT to use

- Input is already a pre-computed featurized tensor or embedding matrix from a prior model run.
- Predicting properties that do not depend on molecular connectivity (e.g., pure solubility from external database lookup).
- Working with non-molecular data (e.g., time series, images, text without chemical interpretation).

## Inputs

- molecular structures (SMILES strings or RDKit mol objects)
- molecular graph adjacency or bond connectivity (edges)
- property labels or target spectra for supervised learning (optional)

## Outputs

- featurized molecular graphs (node feature tensors, edge feature tensors)
- atom embeddings (learned or fixed representations)
- bond embeddings (learned or fixed representations)
- message passing network-ready input tensors

## How to apply

Begin by parsing molecular structures (SMILES or molecular graph formats) into atom and bond lists using RDKit or equivalent cheminformatics tools. Define or retrieve featurization modules that map each atom to a learned embedding (e.g., atom type, degree, formal charge, hybridization) and each bond to edge features (bond type, aromaticity). These featurized nodes and edges become inputs to the message passing network's initial hidden states. In chemprop-IR, spectral-specific features may be appended to the base atom/bond representations to bias the network toward infrared-relevant chemistry. Validate that the featurized tensor shapes match the message passing layer input specifications and that feature dimensionality is consistent across the training set.

## Related tools

- **chemprop** (Base message passing neural network architecture that accepts featurized molecular graphs and performs property prediction; spectral features are incorporated into its featurization and embedding modules) — https://github.com/chemprop/chemprop
- **chemprop-IR** (Extended version of chemprop that adds infrared spectral prediction–specific features and output layers to the featurized molecular graph representation) — https://github.com/gfm-collab/chemprop-IR
- **RDKit** (Cheminformatics toolkit used to parse SMILES/molecular structures into atom, bond, and connectivity data that feed featurization pipelines)

## Evaluation signals

- Featurized tensor shapes must match message passing network input layer specifications (e.g., node_features ∈ ℝ^(num_atoms × d_atom), edge_features ∈ ℝ^(num_bonds × d_edge)).
- Feature values must be within expected ranges (e.g., one-hot or normalized categorical features ∈ [0, 1]; learned embeddings checked for NaN or inf).
- Comparing layer counts and parameter counts of the reconstructed model against reference checkpoints or model summaries to confirm feature incorporation is structurally sound.
- Training convergence and validation loss trajectory — a well-designed featurization should allow the message passing network to reduce loss monotonically on held-out validation molecules.
- Spectral prediction accuracy (e.g., RMSE or correlation with ground-truth infrared spectra) must improve above a naive baseline when spectral features are included.

## Limitations

- Featurization design is chemistry-domain-dependent; generic atom/bond features may not capture infrared-relevant chemical properties without explicit spectral feature engineering.
- No changelog or public documentation of chemprop-IR architectural changes was found, making reverse-engineering of spectral-specific features necessary and error-prone.
- Learned feature representations depend on training data quality and quantity; insufficient or biased training molecules may produce poor generalizations to out-of-distribution test sets.
- Feature incompatibility: if the featurized representation dimensionality or semantics diverges from the message passing network's initialization assumptions, the model will fail to train or converge.

## Evidence

- [intro] message passing neural networks for spectral predictions: "message passing neural networks for spectral predictions as described in the paper [Message Passing Neural Networks for Infrared Spectral Predictions]"
- [intro] chemprop-IR extends chemprop with new spectral features: "The `chemprop-IR` architecture is an extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]"
- [other] Extract and document all new layers, input processing steps, and loss functions specific to infrared spectral prediction: "Extract and document all new layers, input processing steps, and loss functions specific to infrared spectral prediction from the chemprop-IR source code"
- [other] Validate reconstructed architecture by comparing layer counts, input/output tensor shapes, and parameter counts: "Validate that the reconstructed architecture matches the documented chemprop-IR structure by comparing layer counts, input/output tensor shapes, and parameter counts against reference checkpoints or"
- [other] base chemprop message passing architecture and model classes: "Clone the base chemprop repository from github.com/chemprop/chemprop and examine the core message passing architecture and model classes"
