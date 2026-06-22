---
name: message-passing-neural-network-implementation
description: Use when when you have molecular input data (SMILES strings or graph representations) and need to predict molecular properties or spectra using graph neural networks. Apply this skill specifically when the base chemprop MPNN must be extended with new feature modules (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_3372
  tools:
  - chemprop
  - chemprop-IR
derived_from:
- doi: 10.1021/acs.jcim.1c00055
  title: Chemprop-IR
evidence_spans:
- extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]
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

# message-passing-neural-network-implementation

## Summary

Implement and extend message passing neural network (MPNN) architectures for molecular property prediction, such as chemprop-IR for infrared spectral predictions. This skill involves reconstructing base MPNN architectures, integrating domain-specific spectral feature extractors, and validating forward pass execution on molecular graph inputs.

## When to use

When you have molecular input data (SMILES strings or graph representations) and need to predict molecular properties or spectra using graph neural networks. Apply this skill specifically when the base chemprop MPNN must be extended with new feature modules (e.g., spectral features for IR prediction), and you need to verify that the architecture compiles and produces correctly shaped outputs.

## When NOT to use

- Input is already a pre-computed feature matrix rather than molecular graphs or SMILES — use direct model inference instead of architecture implementation.
- You need only inference on a pre-trained model without extending or modifying the architecture.
- The prediction task does not require message passing over molecular connectivity (e.g., fixed-size tabular molecular descriptors).

## Inputs

- Molecular representations (SMILES strings or graph format)
- Base MPNN architecture code (chemprop repository)
- Feature extraction module specification
- Example molecule dataset for validation

## Outputs

- Compiled MPNN model with integrated feature modules
- Feature tensor outputs (correct shape and dimensionality)
- Model summary and parameter counts
- Forward pass output logits or predictions

## How to apply

Clone the chemprop repository and review the base message passing neural network architecture to understand parameter flow and layer definitions. Implement new domain-specific feature extraction modules (e.g., spectral features for infrared) as extension layers, integrating them into the model definition at the appropriate point in the forward pass. Instantiate the extended model (e.g., chemprop-IR) with the new module attached, parse the feature extraction logic to identify named spectral features and their construction, and test feature extraction on a small set of example molecules. Execute a forward pass on sample molecular inputs to verify model compilation and confirm that feature tensors are produced in the correct shape and data type. Log model summary and forward pass output shapes to validate successful integration and parameter flow through the extended architecture.

## Related tools

- **chemprop** (Base message passing neural network framework providing the foundational MPNN architecture for molecular property prediction) — https://github.com/chemprop/chemprop
- **chemprop-IR** (Extended MPNN architecture that integrates spectral feature extraction modules for infrared spectral predictions) — https://github.com/chemprop/chemprop

## Evaluation signals

- Model summary prints without errors and shows all layers (base MPNN + spectral feature modules) with expected parameter counts.
- Forward pass on sample SMILES/graph input completes without shape mismatches or NaN values.
- Feature tensor output dimensionality matches the architecture specification (e.g., spectral features have expected named dimensions).
- Extracted feature tensors contain valid numeric values (no NaN, inf, or unexpected data types) in the correct batch/sequence shape.
- Model can be saved and loaded without loss of layer definitions or extension module state.

## Limitations

- The article does not provide specific hyperparameter guidance (learning rate, batch size, number of message passing rounds) for training extended architectures.
- No changelog or version history is available to track changes between chemprop base and chemprop-IR implementations.
- The paper describes the architecture conceptually but does not detail all edge cases in feature extraction for complex molecular inputs (e.g., unusual valence states, disconnected graphs).

## Evidence

- [intro] Architecture reconstruction and spectral feature integration: "The `chemprop-IR` architecture is an extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]"
- [intro] Repository source and base implementation: "available in the [chemprop GiHub repository](https://github.com/chemprop/chemprop)"
- [intro] Core capability: message passing for spectral prediction: "This repository contains message passing neural networks for spectral predictions as described in the paper"
- [intro] Extension scope: spectral feature incorporation: "chemprop-IR extends chemprop with new spectral features for molecular property prediction"
