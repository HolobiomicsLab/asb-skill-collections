---
name: one-hot-encoding-categorical-chromatography-features
description: Use when you have raw HPLC column metadata containing categorical fields (e.g., column manufacturer 'Waters', USP type 'L1', solvent identities 'H2O'/'MeOH'/'ACN') that must be converted into numerical representations before featurization for a machine learning pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3553
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - NumPy
  - pandas
  - Graphormer-RT
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.4c05859
  title: Graphormer-RT
evidence_spans:
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# one-hot-encoding-categorical-chromatography-features

## Summary

Converts categorical HPLC column metadata (company, USP designation, solvent identities) into binary feature vectors suitable for machine learning. This preprocessing step is essential for method-independent retention time prediction, enabling graph transformer models to ingest heterogeneous categorical and continuous column parameters as a unified feature array.

## When to use

Apply this skill when you have raw HPLC column metadata containing categorical fields (e.g., column manufacturer 'Waters', USP type 'L1', solvent identities 'H2O'/'MeOH'/'ACN') that must be converted into numerical representations before featurization for a machine learning pipeline. Specifically use it in the first stage of the featurize_column function when building HSM parameter blocks that will be concatenated with Tanaka physicochemical vectors.

## When NOT to use

- Input columns are already pre-encoded as numerical indices or one-hot vectors — skip re-encoding to avoid data corruption.
- Categorical values are not from a predefined, finite set — one-hot encoding assumes exhaustive enumeration; for open-ended or unseen categories, use hashing or embedding approaches instead.
- Feature vector is being used in a model that natively handles categorical data (e.g., tree-based ensemble) — one-hot encoding may waste dimensionality and reduce interpretability.

## Inputs

- column_params array (raw HPLC metadata including company name string, USP code string, solvent A identity string, solvent B identity string, additive A flag, additive B flag)
- predefined category lists: companies list, USP codes list, solvents list (e.g., ['h2o', 'meoh', 'acn', 'Other'])

## Outputs

- integer_encodings: concatenated one-hot and binary vectors as NumPy array (dtype int or float)
- feature vector component (to be concatenated with normalized numericals and Tanaka parameters into final HSM feature vector)

## How to apply

For each categorical column metadata field (company name, USP designation, solvent A, solvent B, additive presence flags), create a binary vector of length equal to the number of unique categories in a predefined category list. Set the index corresponding to the observed category value to 1 and all others to 0. For example, if company list is ['Waters', 'Agilent', 'Phenomenex'] and the input is 'Agilent', produce [0, 1, 0]. Use np.where to convert additive flags (non-zero/zero) to binary (1/0). Concatenate all resulting one-hot vectors in a fixed order (company, then USP, then solvent A, then solvent B, then additives A and B) to form the integer encoding block (indices 0–91 of the final feature array). This ordering ensures reproducible feature alignment across all samples.

## Related tools

- **NumPy** (Implements one-hot encoding logic and np.where for binary conversion of additive flags; used for concatenating encoded vectors into final feature array)
- **pandas** (Optional: loading and organizing column metadata tables for batch encoding of multiple column records)
- **Graphormer-RT** (Downstream graph transformer model that accepts the encoded feature vectors as part of the column featurization input) — https://github.com/HopkinsLaboratory/Graphormer-RT

## Examples

```
companies = ['Waters', 'Agilent']; one_hot = [0] * len(companies); one_hot[companies.index('Waters')] = 1; add_A = np.where(0.5 != 0, 1, 0)
```

## Evaluation signals

- Each one-hot vector sums to exactly 1 (i.e., sum(encoded_category) == 1) — verifies exactly one category is selected.
- Total length of concatenated integer encodings equals sum of lengths of all category lists (e.g., 10 companies + 5 USP codes + 4 solvents × 2 + 1 additive A + 1 additive B = 26 dimensions for integer block) — ensures no fields are missing or duplicated.
- Additive flags are binary (only 0 or 1 values present) after np.where conversion — verifies binary conversion succeeded.
- Feature vector indices 0–91 contain only integer values (0 or 1); indices 92+ contain float Tanaka parameters — confirms proper demarcation between integer and float encoding blocks.
- Repeated encoding of the same input produces identical output vector — verifies deterministic, reproducible encoding.

## Limitations

- One-hot encoding is inflexible to unseen categories at inference time; if a new company or solvent identity appears in test data, it will not match any predefined category and must be manually handled (e.g., mapped to 'Other' or excluded).
- Predefined category lists must be complete and consistent across training and inference; any inconsistency in spelling or ordering breaks reproducibility.
- One-hot encoding increases dimensionality linearly with the number of categories; with many categorical fields (e.g., >100 unique companies), the resulting feature space may become sparse and high-dimensional, potentially hurting model generalization.
- Additive presence flags are assumed to be non-zero/zero indicators; if additives are encoded as continuous concentrations or multiple presence states, np.where binary conversion will lose information.

## Evidence

- [other] Apply one-hot encoding to company name using predefined company list, producing binary vector.: "Apply one-hot encoding to company name using predefined company list, producing binary vector."
- [results] def one_hot_company(company):
    one_hot = [0] * len(companies)
    one_hot[companies.index(company)] = 1: "def one_hot_company(company):
    one_hot = [0] * len(companies)
    one_hot[companies.index(company)] = 1"
- [other] Conversion of additive values to binary (0 or 1) by checking if non-zero: "Conversion of additive values to binary (0 or 1) by checking if non-zero"
- [results] add_A_vals = np.where(add_A_vals != 0, 1, add_A_vals)
add_B_vals = np.where(add_B_vals != 0, 1, add_B_vals): "add_A_vals = np.where(add_A_vals != 0, 1, add_A_vals)
add_B_vals = np.where(add_B_vals != 0, 1, add_B_vals)"
- [other] Concatenate all encoded features (company, USP, solvents, additives, normalized numericals) into HSM parameter block (indices 0–91): "Concatenate all encoded features (company, USP, solvents, additives, normalized numericals) into HSM parameter block (indices 0–91)"
- [results] int_encodings = np.concatenate([[-2],company, USP, solv_A, solv_B, add_A_vals,: "int_encodings = np.concatenate([[-2],company, USP, solv_A, solv_B, add_A_vals,"
