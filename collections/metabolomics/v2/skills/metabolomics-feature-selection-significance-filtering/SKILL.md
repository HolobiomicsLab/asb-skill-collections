---
name: metabolomics-feature-selection-significance-filtering
description: Use when you have fitted an MB-PLS model on multi-assay LC-MS intensity
  data (e.g., HPOS, LPOS, LNEG), computed MB-VIP scores for all features, and need
  to identify which features are statistically significant for your phenotypic outcome.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - mbpls
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
  - MAMSI
  - MamsiStructSearch
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- 'It is based on MB_PLS package: Baum et al., (2019). Multiblock PLS: Block dependent
  prediction modeling for Python.'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-feature-selection-significance-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Select statistically significant metabolomic features from multi-assay LC-MS datasets using Multi-Block Variable Importance in Projection (MB-VIP) scores combined with empirical permutation testing. This skill filters features to those with robust discriminatory power across assay blocks, reducing noise and enabling downstream structural annotation.

## When to use

You have fitted an MB-PLS model on multi-assay LC-MS intensity data (e.g., HPOS, LPOS, LNEG), computed MB-VIP scores for all features, and need to identify which features are statistically significant for your phenotypic outcome. Apply this skill when you want to control false positives in untargeted metabolomics by distinguishing signal from noise using a permutation null distribution, rather than accepting all features with high VIP scores.

## When NOT to use

- Input features are already pre-filtered or annotated by targeted assays; permutation testing is redundant if features are known metabolites.
- Sample size is very small (n < 30) or imbalanced across classes; empirical permutation testing may lack power to detect true signals.
- You have not fitted an MB-PLS model yet; feature selection must follow model fitting, not precede it.

## Inputs

- Fitted MamsiPls model object with training data
- Multi-assay LC-MS intensity matrix (m × n, where m = samples, n = features across blocks with assay-specific prefixes, e.g., 'HPOS_', 'LPOS_', 'LNEG_')
- Response vector y (numeric, e.g., binary class labels or quantitative phenotype)

## Outputs

- Feature significance table (DataFrame): feature names, MB-VIP scores, empirical p-values, and assay block membership
- Filtered feature set: subset of original intensity matrix containing only p < 0.01 features
- MB-VIP visualization (optional): bar plot or volcano-style plot showing VIP scores and p-values

## How to apply

First, compute Multi-Block Variable Importance in Projection (MB-VIP) scores for all features in the fitted MB-PLS model using the MamsiPls.mb_vip() method. Second, perform empirical permutation testing via MamsiPls.mb_vip_permtest() with Y-shuffling and ≥10,000 permutations to generate an empirical null distribution of VIP scores under the null hypothesis. Third, calculate empirical p-values for each feature by comparing its observed VIP score against the null distribution. Fourth, apply a stringent significance threshold (p < 0.01) to select features whose VIP scores are unlikely to arise by chance. Fifth, export the resulting feature importance table with p-values, VIP scores, and feature identifiers (including assay prefix) for downstream structural clustering and annotation. The p < 0.01 threshold balances discovery against false positive rate in typical metabolomics cohorts (n=50–300 samples).

## Related tools

- **mbpls** (Core Python package implementing Multi-Block PLS algorithm; provides MamsiPls class with mb_vip() and mb_vip_permtest() methods for feature importance scoring and empirical significance testing) — https://github.com/scikit-learn-contrib/scikit-learn
- **MAMSI** (High-level Python framework wrapping mbpls; provides MamsiPls class, estimate_lv() for latent variable optimization, and mb_vip_permtest() for permutation-based p-value computation on multi-assay MS data) — https://github.com/kopeckylukas/py-mamsi
- **scikit-learn** (Provides train_test_split() for data partitioning and cross-validation utilities used upstream of feature selection) — https://scikit-learn.org
- **pandas** (Data manipulation and export; used to construct and annotate feature importance tables with assay prefixes and p-values) — https://pandas.pydata.org
- **numpy** (Numerical operations for masking and filtering feature sets by p-value threshold) — https://numpy.org
- **MamsiStructSearch** (Downstream tool for linking selected significant features into structural clusters (isotopologues, adducts, cross-assay links) for metabolite annotation) — https://github.com/kopeckylukas/py-mamsi

## Examples

```
p_vals, null_vip = mamsipls.mb_vip_permtest([hpos, lpos, lneg], y, n_permutations=10000, return_scores=True); mask = np.where(p_vals < 0.01); selected = pd.concat([hpos, lpos, lneg], axis=1).iloc[:, mask[0]]
```

## Evaluation signals

- Empirical p-values are uniformly distributed under the null (visual check of histogram of null VIP scores and permutation-derived p-value distribution should show appropriate calibration)
- Selected features (p < 0.01) show higher absolute MB-VIP scores than rejected features; median VIP of selected features is >3σ above null median
- Feature count reduction is reasonable (e.g., 5–15% of original features retained); if >50% of features pass p < 0.01, threshold or permutation count may be inadequate
- Assay block representation is balanced among selected features (no single assay dominates; check count of features per assay prefix)
- Downstream structural clustering (isotopologues, adducts) yields interpretable metabolite groups; features in same cluster share consistent assay prefix patterns and m/z differences

## Limitations

- Permutation testing is computationally expensive (≥10,000 permutations); runtime scales with sample size and feature count. For datasets with >10,000 features, consider parallel execution (joblib) or HPC clusters (illustrated in MAMSI tutorials).
- p < 0.01 threshold is empirical and may require adjustment for different cohort sizes, outcome types (binary vs. quantitative), or domain knowledge. No universally optimal threshold is provided.
- Significance is relative to the fitted MB-PLS model; features selected depend on the chosen number of latent variables (LVs). If LV count is misspecified, feature rankings may be biased.
- Framework was tested on metabolomics phenotyping data (AddNeuroMed, MY Diabetes cohorts); applicability to other LC-MS data types (e.g., environmental, plant metabolomics) has not been formally validated.

## Evidence

- [methods] Calculate Multi-Block Variable Importance in Projection (MB-VIP) scores for all features via MamsiPls.mb_vip().: "Calculate Multi-Block Variable Importance in Projection (MB-VIP) scores for all features via MamsiPls.mb_vip()"
- [methods] Perform empirical permutation testing (n_permutations≥10,000) using MamsiPls.mb_vip_permtest() with Y shuffling to generate empirical p-values for each feature.: "Perform empirical permutation testing (n_permutations≥10,000) using MamsiPls.mb_vip_permtest() with Y shuffling to generate empirical p-values for each feature"
- [methods] Select statistically significant features at p<0.01 threshold and export feature importance table with p-values and VIP scores.: "Select statistically significant features at p<0.01 threshold and export feature importance table with p-values and VIP scores"
- [readme] Multi-Block Variable Importance in Projection (MB-VIP) and permutation testing. Estimation of statistically significant features (variables) using MB-VIP and permutation testing.: "Estimation of statistically significant features (variables) using MB-VIP and permutation testing"
- [readme] estimate empirical p-values for all features: p_vals, null_vip = mamsipls.mb_vip_permtest([hpos, lpos, lneg], y, n_permutations=10000, return_scores=True): "p_vals, null_vip = mamsipls.mb_vip_permtest([hpos, lpos, lneg], y, n_permutations=10000, return_scores=True)"
