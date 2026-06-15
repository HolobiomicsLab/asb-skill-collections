---
name: chemical-structure-featurization
description: Use when you have SMILES strings or molecular structure files (e.g., from a synthetic drug database) and need to feed them into a deep learning model like PS2MS, NEIMS, or DeepEI that expects numerical feature vectors.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
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

# chemical-structure-featurization

## Summary

Convert SMILES strings and molecular structures into fixed-size numerical feature tensors compatible with deep learning models for chemical property prediction. This skill encodes atomic, topological, and structural information from organic molecules into standardized input formats required by neural networks.

## When to use

You have SMILES strings or molecular structure files (e.g., from a synthetic drug database) and need to feed them into a deep learning model like PS2MS, NEIMS, or DeepEI that expects numerical feature vectors. Specifically, when your downstream task is mass spectrum prediction, chemical fingerprint generation, or structural similarity matching.

## When NOT to use

- Input is already a pre-computed chemical fingerprint or feature matrix—proceed directly to model inference.
- SMILES strings are invalid or unparseable by RDKit; validate and repair the input data first.
- The target model requires different input modalities (e.g., raw mass spectra, image data, or pre-trained embeddings) rather than molecular feature vectors.

## Inputs

- SMILES strings (text file or Python iterable)
- Canonical or non-canonical molecular structure representations
- Core drug structure (SMILES) used for synthetic database enumeration

## Outputs

- Fixed-size numerical feature tensor (NumPy ndarray or HDF5 matrix)
- Encoded feature matrix with shape compatible to deep learning model input layer
- Normalized/standardized numerical features ready for neural network inference

## How to apply

Parse and validate SMILES strings using RDKit to construct canonical molecule objects, ensuring consistent representation. Extract molecular descriptors and structural features including atom types, bond connectivity, and graph topology. Encode these features into a fixed-size numerical tensor format matching the model's input layer dimensions (e.g., adjacency matrices, atom feature matrices, or concatenated descriptor vectors). Normalize or standardize feature values according to the model's training specifications (e.g., z-score, min-max scaling). Output the encoded features as a NumPy array or HDF5 file for batch processing. Validation should confirm that feature vector dimensions match model input shape and that normalized values fall within expected ranges (typically [-1, 1] or [0, 1] after scaling).

## Related tools

- **RDKit** (Parse, validate, and canonicalize SMILES strings; extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) required for featurization) — https://www.rdkit.org/docs/Install.html

## Evaluation signals

- All input SMILES strings parse successfully without RDKit exceptions; canonical SMILES are deterministic across re-runs.
- Feature tensor dimensions exactly match the downstream model's input layer shape (e.g., 64 atoms × 14 atom features for PS2MS).
- Feature values fall within expected normalized ranges (e.g., [−1, 1] or [0, 1]) after standardization; no NaN or infinite values are present.
- Model inference produces predictions without shape-mismatch errors; loss and accuracy metrics improve or remain stable compared to baseline featurization.
- Structurally similar compounds (measured by Tanimoto similarity or RMSD) cluster closely in the encoded feature space; dissimilar compounds separate appropriately.

## Limitations

- SMILES parsing and feature extraction depend on RDKit compatibility and correctness; invalid or unusual chemical structures may fail or produce inconsistent encodings.
- Fixed-size feature tensors may lose important information for very large or complex molecules with more atoms than the model's maximum supported dimension.
- Feature normalization and standardization parameters must match those used during model training; mismatched preprocessing will degrade prediction accuracy.
- The skill does not validate chemical feasibility or biological plausibility of encoded structures; invalid or non-existent compounds will still produce numerical features.

## Evidence

- [other] Load SMILES strings for candidate NPS structures from input file. Parse and validate SMILES using RDKit molecular toolkit to generate canonical molecule objects.: "Load SMILES strings for candidate NPS structures from input file. 2. Parse and validate SMILES using RDKit molecular toolkit to generate canonical molecule objects."
- [other] Extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) required by PS2MS architecture. Encode features into fixed-size numerical tensor format matching the model's input layer dimensions.: "Extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) required by PS2MS architecture. 4. Encode features into fixed-size numerical tensor format"
- [other] Normalize or standardize feature values according to model training specifications. Output encoded feature matrix in NumPy array or HDF5 format.: "Normalize or standardize feature values according to model training specifications. 6. Output encoded feature matrix in NumPy array or HDF5 format."
- [readme] rdkit - build the c++ code from the source and install python package from conda: "[rdkit](https://www.rdkit.org/docs/Install.html)
  - build the c++ code from the source and install python package from conda"
