---
name: molecular-property-prediction-feature-construction
description: Use when when you have molecular structures (SMILES or graph formats) and need to predict a physicochemical or spectral property (e.g., infrared spectra) using a graph neural network architecture. Use this skill when the base model architecture (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3454
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemprop_ir
    doi: 10.1021/acs.jcim.1c00055
    title: Chemprop-IR
  dedup_kept_from: coll_chemprop_ir
schema_version: 0.2.0
---

# molecular-property-prediction-feature-construction

## Summary

Extract and construct domain-specific molecular features (e.g., spectral features for infrared predictions) from molecular graph representations to serve as input to message passing neural networks. This skill bridges raw molecular input (SMILES/graphs) to learned molecular representations suitable for property prediction tasks.

## When to use

When you have molecular structures (SMILES or graph formats) and need to predict a physicochemical or spectral property (e.g., infrared spectra) using a graph neural network architecture. Use this skill when the base model architecture (e.g., chemprop) requires spectral or domain-specific features beyond standard atom/bond embeddings, or when you are extending an existing model (like chemprop) with new feature extraction logic.

## When NOT to use

- Input molecules are already featurized as a numerical feature matrix; use this skill only when starting from raw molecular structure formats (SMILES/graphs).
- The prediction task does not require spectral features or domain-specific feature engineering; use standard chemprop feature extraction instead.
- You lack access to the chemprop-IR codebase or detailed specification of the required spectral feature set.

## Inputs

- SMILES strings (molecular structures)
- Parsed molecular graphs (atoms, bonds, connectivity)
- chemprop or chemprop-IR model architecture definition

## Outputs

- Feature tensors (shape: [num_molecules, num_spectral_features])
- Validated feature matrix ready for downstream neural network input

## How to apply

First, load or clone the chemprop-IR repository and identify the spectral features component that extends the base chemprop architecture. Parse the feature extraction implementation to understand the named spectral features and their construction logic from molecular graphs. Instantiate the spectral feature extraction module with your molecular input (SMILES strings or pre-parsed molecular graphs), which will parse molecular connectivity and compute feature tensors. Test the extraction on a small representative set of molecules (e.g., 5–10 examples) to verify that output feature tensors match the expected dimensionality and data type (e.g., shape [num_molecules, num_features]). Validate that extracted features conform to the dimensionality and type constraints defined in the chemprop-IR architecture specification before scaling to full datasets.

## Related tools

- **chemprop** (Base message passing neural network architecture for molecular property prediction; extended by chemprop-IR) — https://github.com/chemprop/chemprop
- **chemprop-IR** (Extension of chemprop with spectral feature extraction for infrared spectral predictions) — https://github.com/chemprop/chemprop

## Evaluation signals

- Extracted feature tensor has expected shape [num_molecules, num_spectral_features] matching architecture specification.
- Feature data type (e.g., float32) and value ranges match those defined in chemprop-IR documentation.
- Feature extraction produces consistent, deterministic output across multiple runs on the same input molecules.
- Feature dimensionality aligns with the input layer of the downstream message passing neural network.
- No NaN, Inf, or missing values in output feature tensor; all molecules produce valid feature vectors.

## Limitations

- Spectral feature extraction is task-specific; features designed for infrared prediction may not transfer directly to other property prediction tasks.
- Requires valid, parseable molecular structures (SMILES); malformed or ambiguous SMILES may fail silently or produce invalid features.
- Feature extraction logic is tightly coupled to chemprop-IR codebase; changes to the architecture or feature definitions require code modification.
- No changelog documented for chemprop-IR, making it difficult to track changes or compatibility across versions.

## Evidence

- [intro] Message passing neural networks can be used for infrared spectral predictions: "This repository contains message passing neural networks for spectral predictions as described in the paper"
- [intro] chemprop-IR extends chemprop with spectral features for molecular property prediction: "The `chemprop-IR` architecture is an extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]"
- [intro] Spectral features are designed specifically for infrared predictions: "chemprop-IR is an extension of chemprop that incorporates new spectral features designed specifically for infrared spectral predictions using message passing neural networks"
- [other] Feature extraction requires validation of tensor shape and format: "Test the feature extraction on a small set of example molecules to verify that feature tensors are produced in the correct shape and format. Validate that the extracted features match the expected"
