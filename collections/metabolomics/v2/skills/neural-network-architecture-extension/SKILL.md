---
name: neural-network-architecture-extension
description: Use when you have a working base MPNN model (e.g., chemprop) and need
  to add task-specific feature processing layers (spectral, electronic, or domain
  features) to improve predictions on a specialized molecular property or spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - chemprop
  - chemprop-IR
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jcim.1c00055
  title: Chemprop-IR
evidence_spans:
- extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations
  for Property Prediction]
- The `chemprop-IR` architecture is an extension of `chemprop`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemprop_ir
    doi: 10.1021/acs.jcim.1c00055
    title: Chemprop-IR
  dedup_kept_from: coll_chemprop_ir
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

# neural-network-architecture-extension

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extend an existing message passing neural network (MPNN) architecture by integrating domain-specific feature modules—such as spectral feature encoders—into the base model definition and validating parameter flow and output shapes. This skill is essential when adapting general-purpose molecular models to specialized prediction tasks (e.g., infrared spectral forecasting) that require learned representations beyond standard molecular graphs.

## When to use

Apply this skill when you have a working base MPNN model (e.g., chemprop) and need to add task-specific feature processing layers (spectral, electronic, or domain features) to improve predictions on a specialized molecular property or spectrum. Trigger conditions: (1) baseline model exists and is versioned in a public repository, (2) a research question articulates what additional learned representations the extension should capture, and (3) you can define a clear interface (input type, output shape) between the base model and the new feature module.

## When NOT to use

- The base model is not available or not versioned in a public repository; extension requires reverse-engineering or guessing the original architecture.
- The task does not require additional learned features beyond the base model's graph representation (e.g., standard SMILES-to-property prediction with no spectral or structural domain knowledge).
- Input data lacks the auxiliary spectral or domain features that the extension is designed to encode; mismatch will cause shape errors or undefined behavior.

## Inputs

- Base MPNN model definition (Python module or checkpoint)
- Molecular input representation (SMILES string or graph object)
- Auxiliary spectral or domain features (tensor or feature array, shape depending on task)

## Outputs

- Extended neural network model (instantiated with spectral features module attached)
- Forward pass output tensor (predictions or learned embeddings)
- Model summary log (parameter counts, layer names, output shapes)

## How to apply

First, clone and review the base MPNN repository (e.g., github.com/chemprop/chemprop) to understand the model definition, message passing loop, and layer composition. Second, design and implement the spectral feature module as a standalone layer or encoder, specifying its input signature (e.g., molecular graph + optional auxiliary spectral data) and output shape. Third, integrate the spectral features module into the model definition by attaching it to the base architecture—typically by concatenating its learned representations with the final message-passing embeddings or inserting it as an intermediate bottleneck. Fourth, instantiate the extended model, load pre-trained weights for the base component if available, and run a forward pass on a sample molecular input (SMILES or graph representation) with the expected auxiliary data. Finally, verify the forward pass output shape, parameter counts, and gradient flow by logging model summary before and after extension and confirming that gradients propagate through both base and extension layers during backpropagation.

## Related tools

- **chemprop** (Base message passing neural network providing molecular graph encoding and initial feature extraction; extended by attaching spectral feature modules) — https://github.com/chemprop/chemprop
- **chemprop-IR** (Reference implementation of extended chemprop with spectral features for infrared spectral predictions; demonstrates integration pattern and expected output behavior)

## Evaluation signals

- Forward pass completes without shape mismatches or runtime errors; output tensor has expected dimensionality (e.g., batch_size × num_spectral_bins or batch_size × num_tasks).
- Model summary shows all parameters from base model plus new spectral feature module; total parameter count is reasonable relative to base-only model.
- Gradient flow during backpropagation reaches both base and extension layers (check gradients are non-zero and finite); loss decreases over training steps.
- Output predictions on validation set improve (lower MSE, higher cosine similarity, or task-specific metric) compared to base model alone on the same molecular inputs.
- Model weights can be saved and reloaded without loss of precision; checkpoint integrity verified by comparing forward pass outputs before and after reload.

## Limitations

- Extension design and module integration are not automated; user must manually define the feature module interface and attachment point in the base architecture.
- Spectral or auxiliary feature data must be pre-computed and aligned with molecular inputs; no guidance provided in the article on feature engineering or preprocessing.
- No changelog or versioning strategy documented; reproducibility may be affected if base chemprop is updated without corresponding updates to the extension.
- Evaluation is limited to forward pass shape validation and manual inspection; no automated unit tests or continuous integration mentioned for detecting architectural mismatches.

## Evidence

- [intro] The chemprop-IR architecture is an extension of chemprop with new spectral features: "The `chemprop-IR` architecture is an extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]"
- [other] Clone the chemprop repository and review the base MPNN architecture: "Clone the chemprop repository from github.com/chemprop/chemprop and review the base message passing neural network architecture."
- [other] Implement and attach the spectral features module as an extension layer: "Implement the spectral features module as an extension layer to the base chemprop model, integrating it into the model definition."
- [other] Execute forward pass on sample molecular input and verify model compilation: "Execute a forward pass on a sample molecular input (SMILES or graph representation) to verify model compilation and parameter flow."
- [other] Log model summary and forward pass output shape to confirm integration: "Log model summary and forward pass output shape to confirm successful integration."
- [intro] Message passing neural networks applied to spectral predictions: "This repository contains message passing neural networks for spectral predictions as described in the paper"
