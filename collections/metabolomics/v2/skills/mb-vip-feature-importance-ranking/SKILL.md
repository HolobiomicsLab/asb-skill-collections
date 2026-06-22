---
name: mb-vip-feature-importance-ranking
description: Use when after fitting a Multi-Block PLS (MB-PLS) discriminant or regression model on multi-assay LC-MS intensity data (e.g., HPOS, LPOS, LNEG blocks), and you need to identify which features drive model performance and warrant further statistical validation or biological interpretation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - mbpls
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
  - MAMSI
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- 'It is based on MB_PLS package: Baum et al., (2019). Multiblock PLS: Block dependent prediction modeling for Python.'
- import pandas as pd
- import numpy as np
- from sklearn.model_selection import train_test_split
- from matplotlib import pyplot as plt
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
schema_version: 0.2.0
---

# mb-vip-feature-importance-ranking

## Summary

Calculate Multi-Block Variable Importance in Projection (MB-VIP) scores to rank and identify statistically significant features across multiple assay blocks in multi-assay LC-MS metabolomics datasets. MB-VIP quantifies each feature's contribution to discriminant or predictive model performance while accounting for block-level structure.

## When to use

After fitting a Multi-Block PLS (MB-PLS) discriminant or regression model on multi-assay LC-MS intensity data (e.g., HPOS, LPOS, LNEG blocks), and you need to identify which features drive model performance and warrant further statistical validation or biological interpretation. Use this skill when you want to prioritize features for downstream structural annotation or when assessing feature importance across heterogeneous assay platforms.

## When NOT to use

- When you have only a single assay block (use standard univariate feature selection or single-block PLS-VIP instead).
- When the MB-PLS model has not converged or shows poor cross-validation performance (validate model fit quality first).
- When input feature matrices are not unit-variance standardized (standardize=True must be set during model fitting).

## Inputs

- Fitted MamsiPls model object (trained on multi-block LC-MS intensity data)
- Multi-block input data (list of pandas DataFrames, one per assay block, with assay-specific prefixes on feature column names)
- Response variable (y, numeric vector of phenotype labels or continuous outcomes)

## Outputs

- MB-VIP scores (numeric vector, one value per feature, ranked by importance)
- Empirical p-values for each feature (from permutation testing)
- Feature importance table (pandas DataFrame with columns: feature name, assay block, VIP score, p-value)
- Optional: MB-VIP visualization plot (matplotlib figure)

## How to apply

Invoke the MamsiPls.mb_vip() method on a fitted MB-PLS model to compute Variable Importance in Projection scores for all features across all blocks. The VIP score for each feature reflects its weighted contribution to model latent variable space, scaled by the explained variance in the response variable. Features with higher VIP scores have greater impact on model discrimination or prediction. Optionally, visualize the ranked VIP scores. To establish statistical significance, perform empirical permutation testing (n_permutations ≥ 10,000) using MamsiPls.mb_vip_permtest() with Y-shuffling to generate null-distribution p-values. Select features at p < 0.01 threshold to control false discovery rate. Export the final feature importance table containing VIP scores and empirical p-values for each feature, preserving assay-specific prefixes in column names to enable cross-assay interpretation.

## Related tools

- **mbpls** (Core multi-block PLS package providing MamsiPls class and mb_vip() method for VIP score computation) — https://github.com/kopeckylukas/py-mamsi
- **pandas** (Data frame manipulation for preparing multi-assay intensity matrices with assay-specific prefixes and exporting feature importance tables)
- **numpy** (Numerical array operations for VIP score computation and permutation test array handling)
- **scikit-learn** (Provides train_test_split for generating independent validation sets prior to VIP calculation)
- **matplotlib** (Visualization of ranked MB-VIP scores across assay blocks)
- **MAMSI** (Complete Python framework integrating MB-PLS model fitting, MB-VIP computation, and permutation testing for multi-assay LC-MS feature selection) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
mb_vip = mamsipls.mb_vip(plot=True); p_vals, null_vip = mamsipls.mb_vip_permtest([hpos, lpos, lneg], y, n_permutations=10000); mask = np.where(p_vals < 0.01); selected = pd.concat([hpos, lpos, lneg], axis=1).iloc[:, mask[0]]
```

## Evaluation signals

- VIP scores are strictly positive, non-zero, and sum to a predictable value (typically proportional to the number of model latent variables and explained variance in Y).
- Top-ranked features (p < 0.01) show consistent direction of effect (positive or negative loading) in the MB-PLS latent variable space and are interpretable in terms of known metabolomic pathways or disease biology.
- Permutation test p-values are distributed as expected under the null (uniform distribution between 0 and 1 for truly non-significant features) and show a left-skewed tail for truly significant features.
- Assay-specific prefixes (e.g., 'HPOS_', 'LPOS_', 'LNEG_') are preserved in the feature importance table output, enabling cross-assay traceability.
- Feature importance rankings are stable across repeated cross-validation folds (if model was cross-validated during latent variable estimation).

## Limitations

- VIP scores depend heavily on the quality and convergence of the underlying MB-PLS model; poor model fit will yield unreliable importance rankings.
- Permutation testing is computationally intensive (n_permutations ≥ 10,000 required for stable p-values); runtime scales linearly with number of features and permutations.
- The method assumes unit-variance standardization during model training (standardize=True); violation of this assumption will bias VIP scores.
- MB-VIP reflects model contribution, not biological effect size or clinical relevance; high VIP does not guarantee biological importance or reproducibility in independent cohorts.
- The threshold p < 0.01 is arbitrary; practitioners should justify threshold choice based on downstream validation (e.g., structural annotation success rate, pathway enrichment) or control for multiple testing stringency.
- Framework was tested on metabolomics phenotyping data but applicability to other LC-MS data types (e.g., non-targeted proteomics, lipidomics-only assays) has not been formally validated.

## Evidence

- [methods] Calculate Multi-Block Variable Importance in Projection (MB-VIP) scores for all features via MamsiPls.mb_vip(): "Calculate Multi-Block Variable Importance in Projection (MB-VIP) scores for all features via MamsiPls.mb_vip()."
- [methods] Perform empirical permutation testing (n_permutations≥10,000) using MamsiPls.mb_vip_permtest() with Y shuffling to generate empirical p-values for each feature.: "Perform empirical permutation testing (n_permutations≥10,000) using MamsiPls.mb_vip_permtest() with Y shuffling to generate empirical p-values for each feature."
- [methods] Select statistically significant features at p<0.01 threshold and export feature importance table with p-values and VIP scores.: "Select statistically significant features at p<0.01 threshold and export feature importance table with p-values and VIP scores."
- [readme] Multi-Block Variable Importance in Projection (MB-VIP): "Multi-Block Variable Importance in Projection (MB-VIP)."
- [readme] You can visualise the MB-VIP: mb_vip = mamsipls.mb_vip(plot=True) or estimate empirical p-values for all features: p_vals, null_vip = mamsipls.mb_vip_permtest([hpos, lpos, lneg], y, n_permutations=10000, return_scores=True): "You can visualise the MB-VIP: mb_vip = mamsipls.mb_vip(plot=True) or estimate empirical p-values for all features: p_vals, null_vip = mamsipls.mb_vip_permtest([hpos, lpos, lneg], y,"
- [intro] MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets and enables statistical feature selection from LC-MS metabolomics data.: "MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets and enables statistical feature selection from LC-MS metabolomics data."
