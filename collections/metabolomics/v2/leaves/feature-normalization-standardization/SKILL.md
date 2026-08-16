---
name: feature-normalization-standardization
description: Use when after extracting and encoding molecular descriptors and structural
  features (atom types, bond connectivity, graph topology) from SMILES strings into
  a fixed-size numerical tensor, before passing the feature matrix to the PS2MS deep
  learning model for NPS prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - RDKit
  - NumPy
  - HDF5
  license_tier: restricted
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

# feature-normalization-standardization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Normalize or standardize encoded molecular features to match the numerical scale and distribution expected by a deep learning model's input layer. This ensures feature values fall within the model's training range, preventing saturation or numerical instability during inference.

## When to use

After extracting and encoding molecular descriptors and structural features (atom types, bond connectivity, graph topology) from SMILES strings into a fixed-size numerical tensor, before passing the feature matrix to the PS2MS deep learning model for NPS prediction.

## When NOT to use

- Features are already in the model's native input range and distribution (e.g., pre-normalized by the training pipeline).
- The input is not yet encoded into numerical tensors (e.g., still in SMILES string or raw molecular graph form).
- The model architecture does not require fixed-size input tensors or does not expect normalized features (rare for deep learning models).

## Inputs

- Encoded feature matrix (NumPy array or HDF5 format)
- Molecular descriptors and structural features (atom types, bond connectivity, graph topology)
- Model training specification or reference statistics (mean, std, min, max values per feature)

## Outputs

- Normalized/standardized feature matrix (NumPy array or HDF5 format, same dimensions as input)
- Normalization parameter metadata (scaling factors, offsets, or statistics used)

## How to apply

Retrieve the normalization/standardization parameters (mean, std, min, max, or scaling factors) from the model training specification or a reference dataset. Apply the same transformation function—typically z-score standardization ((x − mean) / std) or min-max scaling ((x − min) / (max − min))—to every feature in the encoded tensor. Ensure the transformation is applied consistently across all samples and all features in the batch. Verify that output feature values fall within the expected range (e.g., mean ≈ 0 and std ≈ 1 for z-score, or [0, 1] for min-max). Document the parameters used so that the same normalization can be applied to new analyte features at inference time.

## Related tools

- **RDKit** (Parse and validate SMILES to generate canonical molecule objects and extract structural features that are then encoded and normalized) — https://www.rdkit.org/docs/Install.html
- **NumPy** (Perform vectorized normalization/standardization operations on the feature matrix)
- **HDF5** (Store and read normalized feature matrices in efficient binary format)

## Evaluation signals

- Output feature values match the expected distribution: mean ≈ 0 and standard deviation ≈ 1 for z-score normalization, or all values in [0, 1] for min-max scaling.
- Normalization parameters (mean, std, min, max) are identical to those used during model training—verify by comparing against stored training statistics.
- No NaN, inf, or out-of-range values appear in the normalized output (indicates division-by-zero or scale overflow errors).
- The normalized feature tensor has identical shape and dtype to the input, confirming element-wise transformation without data loss.
- When the same normalization is applied to a held-out reference dataset, output statistics match the training set's normalized distribution.

## Limitations

- Normalization parameters must be derived from the same training dataset or a representative reference; using mismatched statistics will degrade model performance.
- Features with zero variance (constant values across all samples) will cause division-by-zero in z-score standardization; such features should be identified and handled (e.g., dropped or assigned a fixed small value) before normalization.
- The paper does not explicitly specify which normalization method (z-score vs. min-max vs. other) is used in PS2MS; practitioners must consult the model code or training documentation.
- Normalization must be applied independently to training, validation, and test sets using statistics computed only from the training set to prevent data leakage.

## Evidence

- [other] Extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) required by PS2MS architecture.: "Extract molecular descriptors and structural features (atom types, bond connectivity, graph topology) required by PS2MS architecture."
- [other] Normalize or standardize feature values according to model training specifications.: "Normalize or standardize feature values according to model training specifications."
- [other] Encode features into fixed-size numerical tensor format matching the model's input layer dimensions.: "Encode features into fixed-size numerical tensor format matching the model's input layer dimensions."
