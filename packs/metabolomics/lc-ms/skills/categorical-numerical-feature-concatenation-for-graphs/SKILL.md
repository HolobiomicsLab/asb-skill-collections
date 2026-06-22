---
name: categorical-numerical-feature-concatenation-for-graphs
description: 'Use when when preparing heterogeneous column-metadata inputs for a graph transformer model that operates on molecular graphs. Specifically: (1) you have both categorical metadata (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  tools:
  - Graphormer
  - DGL
  - RDKit
  - PyTorch
  - NumPy
  - Graphormer-RT
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
- Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github
- import dgl
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# categorical-numerical-feature-concatenation-for-graphs

## Summary

Encode mixed categorical and numerical HPLC column parameters into a unified feature vector for input to graph transformer models by one-hot encoding categorical attributes (company, USP, solvents, HPLC type) and normalizing numerical features (length, temperature, pH, particle size, dead time, physicochemical parameters) before concatenation. This skill bridges domain-specific chromatographic metadata and graph neural network architectures for retention-time prediction.

## When to use

When preparing heterogeneous column-metadata inputs for a graph transformer model that operates on molecular graphs. Specifically: (1) you have both categorical metadata (e.g., column brand, USP classification, solvent identity) and continuous instrumental parameters (diameter, temperature, pH, flow rate, Tanaka/HSMB descriptors); (2) your model expects a single concatenated feature tensor alongside molecular graph embeddings; (3) you need to train on multiple chromatographic methods (e.g., reverse-phase and HILIC) with method-invariant feature representation.

## When NOT to use

- Input column metadata is already a single pre-computed embedding (e.g., from a separate encoder model); skip concatenation and use directly.
- Model architecture does not accept separate column-parameter tensors (i.e., it only takes a single graph input); instead, featurize columns as additional graph nodes or edges.
- Categorical features are already ordinal or continuous (e.g., solvent polarity index, pKa); do not one-hot encode; normalize and concatenate directly.
- Gradient information is unavailable or undefined for some samples; imputation or removal of gradient-slope features may be required before concatenation.

## Inputs

- column metadata table (e.g., pickle, CSV) with headers: company_name, usp_code, col_length, col_innerdiam, col_part_size, temp, col_fl, col_dead, HPLC_type, A_solv, B_solv, time1–time4, grad1–grad4, A_pH, B_pH, A_start, A_end, B_start, B_end, eluent additives and units
- categorical feature names (string list of column names to one-hot encode)
- numerical feature names and their normalization divisors (dict or table)
- gradient parameters table with B and t values for slope calculation

## Outputs

- composite feature vector (numpy ndarray or torch tensor) of shape (batch_size, feature_dim) ready for concatenation with molecular graph embeddings
- mapping of feature indices to feature names (for interpretability and debugging)
- normalized/encoded feature arrays saved in .npz, .npy, .pkl, or .csv formats as specified

## How to apply

First, identify categorical columns (company, USP, solvent A/B, HPLC type) and apply one-hot encoding to each, storing each as a separate binary vector. Second, normalize numerical features by domain-specific divisors: length ÷ 250, temperature ÷ 100, pH ÷ 14 (these normalizations center features around unit scale). Third, extract gradient-slope features (s1, s2, s3) by computing (B_next − B_prev)/(t_next − t_prev) for each segment of the elution gradient. Fourth, convert additive-concentration indicators (e.g., formic acid, acetic acid) to binary flags (0 or 1) by checking non-zero values. Fifth, concatenate all vectors in a consistent order: one-hot encodings (company, USP, solvent_A, solvent_B, additives_A, additives_B, HPLC_type), followed by normalized scalars (diameter, particle_size, temperature, pH_A, pH_B, flow_rate, dead_time, Tanaka_params, HSMB_params), then gradient slopes. Finally, validate tensor shape consistency by passing sample batches through the model's forward pass to ensure no shape mismatches occur at the concatenation step.

## Related tools

- **RDKit** (Encodes molecular structure as graph nodes and edges (atom types, bond orders, chirality) that are concatenated with column-parameter features in the forward pass)
- **DGL** (Constructs and manages heterogeneous molecular graphs with node/edge attributes; receives concatenated column embeddings alongside graph tensors) — https://github.com/dmlc/dgl
- **PyTorch** (Implements one-hot encoding, normalization, and concatenation operations; provides tensor manipulation and gradient computation for model training) — https://github.com/pytorch/pytorch
- **NumPy** (Performs array operations (normalization, concatenation, slicing); handles .npz/.npy file I/O for feature storage and loading)
- **Graphormer** (Graph Transformer backbone that consumes concatenated column-parameter embeddings combined with molecular graph representations to predict retention time) — https://github.com/microsoft/Graphormer
- **Graphormer-RT** (Application-specific extension implementing the full featurization, concatenation, and training pipeline for retention-time prediction across chromatographic methods) — https://github.com/HopkinsLaboratory/Graphormer-RT

## Examples

```
company = one_hot_company('Agilent'); length_norm = float(col_params[2]) / 250; s1 = (B2 - B1) / (t2 - t1); concat_features = np.concatenate([company, usp_vec, solv_A, solv_B, add_A_binary, add_B_binary, [length_norm, temp_norm, pH_norm, diameter, particle_size, tanaka_param], [s1, s2, s3]])
```

## Evaluation signals

- One-hot encoded vectors have exactly one entry equal to 1 per categorical feature, all others 0; vector length matches the number of unique categories.
- Normalized numerical features fall in reasonable ranges (e.g., length/250 typically 0.2–0.8, temperature/100 typically 0.2–0.5, pH/14 typically 0.2–0.9).
- Gradient-slope features (s1, s2, s3) are computed without division-by-zero errors and values are finite (no NaN or Inf).
- Concatenated tensor shape matches expected (batch_size, 1 + num_companies + num_USP + num_solvents_A + num_solvents_B + num_additives_A + num_additives_B + 1 + scalar_features + 3_slopes), and forward pass through Graphormer backbone succeeds without shape mismatch errors.
- Additive binary flags are exactly 0 or 1, with 1 indicating presence of that additive in the sample.

## Limitations

- One-hot encoding does not capture similarity or hierarchy among categorical levels (e.g., different column brands with similar properties); ordinal or learned embeddings may be more informative but require additional model complexity.
- Normalization divisors (250, 100, 14) are heuristic and may not be optimal for all datasets; divisors should be validated against the min/max range of each feature in your dataset to avoid pathological normalization (e.g., division by a feature's natural range).
- Missing or invalid values (empty strings for diameter, '2.7 spp' or '2.6 spp' for Tanaka parameters) require ad-hoc imputation (replacing with 0 or 2.7); systematic missing-data handling or domain-based imputation may improve model robustness.
- Gradient-slope calculation assumes exactly 3 time-points with defined B values; samples with fewer than 2 time-steps or undefined gradients will produce NaN or Inf slopes and require filtering or removal.
- Concatenation order is critical for reproducibility and model interpretation; any deviation in concatenation order between training and inference will misalign features and degrade predictions.

## Evidence

- [full_text] Column parameters are featurized through one-hot encoding of categorical features (company, USP, solvents), normalization of numerical features (length/250, temperature/100, pH/14), and concatenation of integer and float encodings including diameter, particle size, pH, dead time, gradient slopes, Tanaka parameters, and HSMB parameters into a composite feature vector.: "Column parameters are featurized through one-hot encoding of categorical features (company, USP, solvents), normalization of numerical features (length/250, temperature/100, pH/14), and concatenation"
- [full_text] Create column-parameter embedding layer that accepts one-hot encoded categorical features (company, USP, solvent composition) and normalized numerical features (length/250, temperature/100, pH/14).: "Create column-parameter embedding layer that accepts one-hot encoded categorical features (company, USP, solvent composition) and normalized numerical features (length/250, temperature/100, pH/14)."
- [results] def one_hot_company(company):
    one_hot = [0] * len(companies)
    one_hot[companies.index(company)] = 1: "def one_hot_company(company):
    one_hot = [0] * len(companies)
    one_hot[companies.index(company)] = 1"
- [results] length = float(column_params[2]) / 250
temp = float(column_params[5]) / 100
pH_A = float(column_params[19]) / 14: "length = float(column_params[2]) / 250
temp = float(column_params[5]) / 100
pH_A = float(column_params[19]) / 14"
- [results] s1 = (B2 - B1) / (t2 - t1)
s2 = (B3 - B2) / (t3 - t2)
s3 = (B3 - B1) / (t3 - t1): "s1 = (B2 - B1) / (t2 - t1)
s2 = (B3 - B2) / (t3 - t2)
s3 = (B3 - B1) / (t3 - t1)"
- [full_text] Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to final dense output layer for continuous retention-time prediction.: "Assemble forward pass that concatenates molecular graph embeddings from DGL encoder, column embeddings, and gradient slopes, passing combined representation through Graphormer transformer backbone to"
- [results] add_A_vals = np.where(add_A_vals != 0, 1, add_A_vals)
add_B_vals = np.where(add_B_vals != 0, 1, add_B_vals): "add_A_vals = np.where(add_A_vals != 0, 1, add_A_vals)
add_B_vals = np.where(add_B_vals != 0, 1, add_B_vals)"
- [full_text] Handling missing values by converting empty strings to 0 for diameter and pH_B: "Handling missing values by converting empty strings to 0 for diameter and pH_B"
- [readme] Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github: "Graphormer-RT is an extension to the Graphormer package, with documentation, and the original code on Github"
