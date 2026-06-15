---
name: molecular-descriptor-extraction
description: Use when when you have validated SMILES strings or canonical molecule objects from RDKit and need to convert them into the fixed-size numerical tensor format expected by a deep learning model (e.g., PS2MS).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0209
  - http://edamontology.org/topic_3372
  tools:
  - RDKit
derived_from:
- doi: 10.1021/acs.analchem.3c05019
  title: ps2ms
evidence_spans:
- jhhung/PS2MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ps2ms
    doi: 10.1021/acs.analchem.3c05019
    title: ps2ms
  dedup_kept_from: coll_ps2ms
schema_version: 0.2.0
---

# molecular-descriptor-extraction

## Summary

Extract atom types, bond connectivity, and graph topology features from canonical molecular structures to create fixed-size numerical tensors for deep learning input. This skill bridges chemical structure representation (SMILES) to machine-learning-ready feature matrices required by mass-spectrometry prediction models.

## When to use

When you have validated SMILES strings or canonical molecule objects from RDKit and need to convert them into the fixed-size numerical tensor format expected by a deep learning model (e.g., PS2MS). Apply this skill before feeding structures into neural network layers that expect pre-encoded molecular features rather than raw graph representations.

## When NOT to use

- Input is already a pre-computed feature matrix or tensor — skip directly to model inference.
- The deep learning model expects raw SMILES strings or graph adjacency matrices without prior encoding — consult the model's documentation on input format requirements.
- Molecular descriptors have already been extracted and normalized by an upstream pipeline — avoid redundant re-encoding.

## Inputs

- SMILES strings (text format)
- Canonical molecule objects (RDKit Mol objects)
- Input file containing candidate NPS structures

## Outputs

- Encoded feature matrix (NumPy array format)
- Encoded feature matrix (HDF5 format)
- Fixed-size numerical tensor matching model input dimensions

## How to apply

After parsing and validating SMILES using RDKit to generate canonical molecule objects, systematically extract structural features including atom types, bond connectivity patterns, and graph topology. Compute molecular descriptors that characterize the structure. Encode the extracted features into a fixed-size numerical tensor matching the model's input layer dimensions (e.g., a vector or matrix of specified shape). Normalize or standardize feature values according to the model's training specifications (e.g., zero-mean unit-variance scaling or min-max scaling to [0,1]). Output the encoded feature matrix in a machine-readable format such as NumPy arrays or HDF5 to ensure reproducibility and compatibility with downstream deep learning inference.

## Related tools

- **RDKit** (Parse and validate SMILES strings into canonical molecule objects; extract atom types, bond connectivity, and graph topology; compute molecular descriptors) — https://www.rdkit.org/docs/Install.html

## Evaluation signals

- Output tensor shape matches the model's expected input layer dimensions (e.g., [n_samples, n_features]).
- All feature values are within the expected normalized range (e.g., [0, 1] or zero-mean unit-variance) according to model training specifications.
- No NaN, infinity, or missing values present in the encoded feature matrix.
- Canonical SMILES input produces identical encoded features across multiple runs (deterministic behavior confirmed).
- Feature matrix is serializable to NumPy or HDF5 format without data loss or corruption.

## Limitations

- RDKit's canonical SMILES parser may fail or produce unexpected results for highly unusual or non-standard chemical structures; validation against reference databases is recommended.
- Feature normalization parameters (mean, std, min, max) must be derived from the same training dataset used to fit the deep learning model; mismatched statistics will degrade prediction accuracy.
- The fixed-size tensor format assumes a constant number of atoms or bonds; structures with highly variable size may require padding or masking strategies not detailed in the source material.
- No guidance provided in the source material on handling stereochemistry, tautomers, or salt forms; these may require explicit preprocessing before descriptor extraction.

## Evidence

- [other] Extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) required by PS2MS architecture.: "Extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) required by PS2MS architecture."
- [other] Encode features into fixed-size numerical tensor format matching the model's input layer dimensions.: "Encode features into fixed-size numerical tensor format matching the model's input layer dimensions."
- [other] Normalize or standardize feature values according to model training specifications.: "Normalize or standardize feature values according to model training specifications."
- [other] Output encoded feature matrix in NumPy array or HDF5 format.: "Output encoded feature matrix in NumPy array or HDF5 format."
- [other] Parse and validate SMILES using RDKit molecular toolkit to generate canonical molecule objects.: "Parse and validate SMILES using RDKit molecular toolkit to generate canonical molecule objects."
- [readme] [rdkit](https://www.rdkit.org/docs/Install.html) - build the c++ code from the source and install python package from conda: "[rdkit](https://www.rdkit.org/docs/Install.html) - build the c++ code from the source and install python package from conda"
