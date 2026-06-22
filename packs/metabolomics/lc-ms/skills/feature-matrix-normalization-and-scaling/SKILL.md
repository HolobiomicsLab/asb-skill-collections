---
name: feature-matrix-normalization-and-scaling
description: Use when you have a heterogeneous feature matrix combining molecular descriptors (from RDKit/mordred) and chromatographic metadata (column length, temperature, pH, flow rate, particle size) with different physical units, ranges, and scales.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
  tools:
  - mordred
  - NumPy
  - pandas
  - RDKit
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
- import mordred from mordred import Calculator, descriptors
- import numpy as np
- import pandas as pd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphormer_rt_cq
    doi: 10.1021/acs.analchem.4c05859
    title: Graphormer-RT
  dedup_kept_from: coll_graphormer_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05859
  all_source_dois:
  - 10.1021/acs.analchem.4c05859
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-matrix-normalization-and-scaling

## Summary

Normalize and scale numerical descriptor and chromatographic parameter features to standardized ranges (e.g., division by domain-specific factors) before machine learning model training. This preprocessing step improves model convergence and enables fair comparison of features with different physical units and magnitudes.

## When to use

Apply this skill when you have a heterogeneous feature matrix combining molecular descriptors (from RDKit/mordred) and chromatographic metadata (column length, temperature, pH, flow rate, particle size) with different physical units, ranges, and scales. Use it before feeding features into graph transformer or other neural network models for retention time prediction or molecular property modeling.

## When NOT to use

- Input features are already normalized or standardized (e.g., z-score or min-max scaling already applied).
- Feature matrix is entirely categorical or binary; scaling divisors are domain-specific and not applicable to new feature spaces without revalidation.
- Model architecture expects raw, unscaled feature magnitudes (rare for neural networks, but possible for tree-based models or domain-specific physical simulators).

## Inputs

- Raw chromatographic metadata (column parameters: diameter, particle size, temperature, flow rate, dead time, solvent composition, pH, Tanaka/HSMB physicochemical parameters)
- Molecular descriptor arrays (RDKit and mordred descriptors combined, deduplicated)
- Categorical metadata (company name, USP code, solvent identifiers, HPLC type, column length in original units)

## Outputs

- Normalized numerical feature matrix (length, temperature, pH scaled by domain-specific divisors)
- One-hot encoded categorical feature matrix (company, USP, solvents, HPLC type)
- Concatenated feature matrix ready for model training
- Compressed feature file (.npz, optionally .npy, .csv, .pkl)

## How to apply

Identify numerical feature columns and their physical meaning (e.g., column length in mm, temperature in °C, pH in 0–14 scale). Apply domain-specific divisors to normalize each feature to a standardized range: divide column length by 250 (reference length), temperature by 100 (reference temperature), pH by 14 (max pH), and gradient slopes (s1, s2, s3) by their respective time and concentration deltas. One-hot encode categorical features (company, USP code, solvent identities, HPLC type) separately to avoid scaling. Concatenate normalized numerical features with one-hot categorical features into a single feature matrix. Optionally apply per-descriptor tolerance filtering to remove descriptors with excessive broken or missing values before or after normalization. Save the resulting normalized feature matrix in compressed NumPy format (.npz) for reproducibility and downstream model ingestion.

## Related tools

- **NumPy** (Vectorized normalization via element-wise division and concatenation of feature arrays)
- **pandas** (Loading, reshaping, and saving tabular feature data; handling missing values during preprocessing)
- **RDKit** (Source of molecular descriptor values prior to normalization)
- **mordred** (Source of mordred descriptor values prior to normalization and deduplication)

## Examples

```
length = float(column_params[2]) / 250; temp = float(column_params[5]) / 100; pH_A = float(column_params[19]) / 14; np.savez_compressed('normalized_features.npz', features=np.concatenate([rdkit_descriptors, normalized_column_params, one_hot_encoded_categories], axis=1))
```

## Evaluation signals

- Normalized feature values fall within expected ranges (e.g., length ≤ 1.0 after division by 250, temperature ≤ 1.0 after division by 100, pH ≤ 1.0 after division by 14).
- One-hot encoded categorical features contain only 0 and 1 values; exactly one 1 per row for single-valued categories.
- Feature matrix shape matches expected dimensions: (n_samples, n_descriptors + n_encoded_categories).
- No NaN or infinite values remain in the normalized matrix after division; missing values (empty strings) are replaced with 0 before normalization.
- Concatenated matrix can be loaded from .npz file and has identical shape and values to in-memory array before serialization.

## Limitations

- Domain-specific divisors (250 for length, 100 for temperature, 14 for pH) are fixed based on the Stienstra et al. study; transferring these normalizations to datasets with different experimental ranges (e.g., ultra-high-pressure LC with different flow rates or pH extremes) may require revalidation or adaptive scaling.
- Additive feature handling converts non-zero values to binary (1) via thresholding; this loses information about additive concentration or molarity and may not be appropriate for datasets where additive magnitude is predictive.
- Tanaka parameter handling involves replacement of '2.7 spp' and '2.6 spp' string values with numeric 2.7; other non-numeric artifacts in the raw metadata may cause failures if not explicitly handled in preprocessing.
- One-hot encoding produces sparse, high-dimensional categorical features; datasets with many unique categorical values (e.g., hundreds of solvent types or column brands) may suffer from curse of dimensionality in downstream models.

## Evidence

- [results] length = float(column_params[2]) / 250
temp = float(column_params[5]) / 100
pH_A = float(column_params[19]) / 14: "Normalization of numerical features (length divided by 250, temperature divided by 100, pH divided by 14)"
- [results] s1 = (B2 - B1) / (t2 - t1)
s2 = (B3 - B2) / (t3 - t2)
s3 = (B3 - B1) / (t3 - t1): "Calculation of gradient slope features (s1, s2, s3) from B and t parameters"
- [results] def one_hot_company(company):
    one_hot = [0] * len(companies)
    one_hot[companies.index(company)] = 1: "One-hot encoding of categorical features (company, USP, solvents, HPLC type, column lengths)"
- [results] add_A_vals = np.where(add_A_vals != 0, 1, add_A_vals)
add_B_vals = np.where(add_B_vals != 0, 1, add_B_vals): "Conversion of additive values to binary (0 or 1) by checking if non-zero"
- [results] def save_features(path: str, features: List[np.ndarray]):
    np.savez_compressed(path, features=features): "Loading and saving features in multiple formats (.npz compressed, .npy, .csv/.txt, .pkl/.pickle)"
- [readme] The pickle files (/home/cmkstien/RT_pub/Graphormer_RT/sample_data/HILIC_metadata.pickle, /home/cmkstien/RT_pub/Graphormer_RT/sample_data/RP_metadata.pickle) contain processed column metada generated from RepoRT: "processed column metadata containing chromatographic parameters for normalization and encoding"
