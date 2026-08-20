---
name: spectral-feature-engineering
description: Use when you have molecular structures (SMILES or graph representations)
  and need to predict or analyze infrared spectral properties using message passing
  neural networks.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - chemprop
  - chemprop-IR
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
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

# spectral-feature-engineering

## Summary

Extract and engineer spectral features from molecular structures using message passing neural networks for infrared spectral prediction tasks. This skill implements domain-specific feature construction within the chemprop-IR pipeline to transform molecular representations into tensors suitable for spectral property prediction.

## When to use

Apply this skill when you have molecular structures (SMILES or graph representations) and need to predict or analyze infrared spectral properties using message passing neural networks. Use it specifically when working with the chemprop-IR architecture, which requires spectral features designed for IR spectral prediction rather than standard molecular property prediction.

## When NOT to use

- Input is already a pre-computed feature table or spectral feature matrix — skip directly to model training
- Working with non-IR spectral prediction tasks (e.g., mass spectrometry, NMR) where domain-specific IR features are not applicable
- Molecular property prediction using base chemprop without IR spectral extension — use standard chemprop feature extraction instead

## Inputs

- SMILES strings or molecular graph representations
- Molecular structure files (chemprop-compatible format)
- List of molecule identifiers with associated structural data

## Outputs

- Feature tensors with dimensions matching chemprop-IR spectral feature specification
- Extracted spectral feature matrices (numerical arrays)
- Feature metadata documenting feature names and construction parameters

## How to apply

Load the chemprop-IR repository and identify the spectral features component within the extended architecture. Parse the feature extraction implementation to understand the named spectral features and their construction logic from the message passing framework. Instantiate the spectral feature extraction module with molecular inputs (SMILES strings or molecular graphs), ensuring proper parsing through the chemprop graph representation layer. Execute feature extraction on your molecular dataset, verifying that the output tensors match the expected dimensionality and data types defined in the chemprop-IR specification. Validate feature shapes and data types against the architecture specification before passing to downstream IR spectral prediction layers.

## Related tools

- **chemprop** (Base message passing neural network architecture providing molecular graph representation and feature encoding pipeline) — https://github.com/chemprop/chemprop
- **chemprop-IR** (Extended chemprop architecture that implements spectral features specifically designed for infrared spectral predictions) — https://github.com/chemprop/chemprop

## Evaluation signals

- Feature tensor shape matches the expected dimensionality defined in chemprop-IR architecture specification
- Feature data types are consistent (floating-point tensors with appropriate precision)
- Feature extraction produces non-null, non-NaN values for valid molecular inputs
- Extracted features for identical molecules (duplicate SMILES) produce identical feature tensors
- Feature extraction completes without errors on a diverse set of example molecules from the training dataset

## Limitations

- Spectral features are specialized for infrared prediction and may not generalize to other spectral modalities or molecular property prediction tasks
- Feature extraction depends on accurate molecular graph parsing; malformed or unusual SMILES strings may fail or produce incorrect representations
- No changelog or version tracking information provided, making it difficult to track feature changes or improvements across chemprop-IR versions

## Evidence

- [intro] chemprop-IR is an extension of chemprop with new spectral features: "The `chemprop-IR` architecture is an extension of `chemprop` described in the paper [Analyzing Learned Molecular Representations for Property Prediction]"
- [intro] Message passing neural networks for spectral prediction: "This repository contains message passing neural networks for spectral predictions as described in the paper"
- [intro] chemprop-IR extends chemprop with spectral features for molecular property prediction: "chemprop-IR is an extension of `chemprop` that incorporates new spectral features designed specifically for infrared spectral predictions using message passing neural networks"
- [other] Implementation workflow includes molecular input handling and feature extraction validation: "Implement or instantiate the spectral feature extraction module with molecular input handling (SMILES/graph parsing)"
- [other] Feature validation through dimensionality and data type checks: "Validate that the extracted features match the expected dimensionality and data types defined in the chemprop-IR architecture"
