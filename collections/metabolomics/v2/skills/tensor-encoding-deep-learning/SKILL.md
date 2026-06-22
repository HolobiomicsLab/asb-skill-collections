---
name: tensor-encoding-deep-learning
description: Use when when you have validated SMILES strings or RDKit molecule objects representing chemical structures and need to feed them into a pre-trained deep learning model (such as PS2MS, NEIMS, or DeepEI) that expects fixed-size numerical tensor inputs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3473
  tools:
  - RDKit
derived_from:
- doi: 10.1021/acs.analchem.3c05019
  title: ps2ms
evidence_spans:
- jhhung/PS2MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05019
  all_source_dois:
  - 10.1021/acs.analchem.3c05019
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Tensor Encoding for Deep Learning

## Summary

Convert parsed molecular structures (SMILES, canonical molecule objects, or extracted descriptors) into fixed-size numerical tensor representations compatible with deep learning model input layers. This skill bridges chemical representation and neural network inference by standardizing feature dimensions and value ranges.

## When to use

When you have validated SMILES strings or RDKit molecule objects representing chemical structures and need to feed them into a pre-trained deep learning model (such as PS2MS, NEIMS, or DeepEI) that expects fixed-size numerical tensor inputs. Specifically, when the downstream task is mass spectrum prediction, chemical fingerprint generation, or similarity-based analyte matching that relies on encoded features rather than raw molecular graphs.

## When NOT to use

- Input is already a pre-computed feature matrix or fingerprint array ready for model inference — skip directly to model prediction.
- The downstream model accepts raw SMILES strings or molecule objects directly without requiring tensor encoding (rare; most deep learning architectures require numerical tensors).
- The chemical structures are too large, complex, or contain elements/bonds not supported by RDKit, leading to parsing failure or incompatible descriptor extraction.

## Inputs

- SMILES strings (text file or list)
- RDKit molecule objects
- Canonical molecular structure representations

## Outputs

- Encoded feature matrix (NumPy array)
- Encoded feature matrix (HDF5 file)
- Fixed-size numerical tensors compatible with model input layers

## How to apply

Parse and validate input SMILES strings using RDKit to generate canonical molecule objects. Extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) relevant to the target deep learning architecture. Encode these features into a fixed-size numerical array matching the model's input layer dimensions, typically by flattening or pooling molecular graphs into dense vectors. Normalize or standardize feature values (e.g., z-score, min-max scaling) according to the model's training specifications to ensure numerical stability. Serialize the resulting tensor into NumPy array or HDF5 format for batch processing. Validate output tensor shape against model input signature and verify value ranges fall within expected bounds.

## Related tools

- **RDKit** (Parse, validate, and extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) from SMILES strings into canonical molecule objects required by the tensor encoder) — https://www.rdkit.org/docs/Install.html

## Evaluation signals

- Output tensor shape exactly matches the model's input layer dimensions (e.g., if model expects [batch_size, 256] features, verify all encoded matrices conform to this shape).
- Feature values fall within expected normalized ranges (e.g., 0–1 for min-max scaling, mean ≈ 0 and std ≈ 1 for z-score normalization) after standardization.
- No NaN or infinite values present in the encoded tensor; all missing or invalid molecular features are handled consistently (e.g., masked, zero-filled, or rejected with clear error logging).
- Round-trip consistency: re-decoding or visualizing a subset of encoded tensors recovers recognizable molecular properties (atom counts, bond types, connectivity patterns) matching the input SMILES.
- Batch processing produces tensors with stable shape and value distributions across multiple SMILES inputs, with no rank mismatches or silent feature truncation.

## Limitations

- RDKit may fail to parse invalid, malformed, or non-standard SMILES strings, requiring validation and error handling upstream.
- Molecular descriptors extracted by RDKit are sensitive to tautomerization, stereochemistry, and aromaticity perception; canonical SMILES generation helps but does not eliminate all ambiguity.
- Fixed-size tensor encoding loses some information from large or structurally diverse molecules (e.g., if flattening a variable-length graph into a static vector); architecture choice (pooling strategy, dimensionality reduction) must balance expressiveness against computational cost.
- Normalization and standardization are data-dependent; parameters (min, max, mean, std) must be computed on the training set and applied consistently to test/inference data, or model performance degrades.
- The PS2MS system integrates this encoding with NEIMS (mass spectrum prediction) and DeepEI (chemical fingerprint generation); mismatch between encoder output and these downstream models' expected input formats will cause silent failures or poor predictions.

## Evidence

- [other] Load SMILES strings for candidate NPS structures from input file. Parse and validate SMILES using RDKit molecular toolkit to generate canonical molecule objects.: "Load SMILES strings for candidate NPS structures from input file. Parse and validate SMILES using RDKit molecular toolkit to generate canonical molecule objects."
- [other] Extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) required by PS2MS architecture.: "Extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) required by PS2MS architecture."
- [other] Encode features into fixed-size numerical tensor format matching the model's input layer dimensions.: "Encode features into fixed-size numerical tensor format matching the model's input layer dimensions."
- [other] Normalize or standardize feature values according to model training specifications.: "Normalize or standardize feature values according to model training specifications."
- [other] Output encoded feature matrix in NumPy array or HDF5 format.: "Output encoded feature matrix in NumPy array or HDF5 format."
- [readme] rdkit - build the c++ code from the source and install python package from conda: "rdkit - build the c++ code from the source and install python package from conda"
