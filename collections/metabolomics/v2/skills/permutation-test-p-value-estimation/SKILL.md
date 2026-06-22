---
name: permutation-test-p-value-estimation
description: Use when after computing Multi-Block Variable Importance in Projection (MB-VIP) scores on a fitted MB-PLS discriminant model, when you need to distinguish signal features from noise by establishing empirical significance thresholds rather than relying on parametric assumptions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - mbpls
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
  - MamsiPls.mb_vip_permtest()
  - joblib
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# permutation-test-p-value-estimation

## Summary

Empirical permutation testing on shuffled response labels to generate null distributions and compute feature-level p-values for multi-block variable importance scores in discriminant LC-MS metabolomics models. This approach corrects for multiple testing and identifies statistically significant features after feature selection.

## When to use

After computing Multi-Block Variable Importance in Projection (MB-VIP) scores on a fitted MB-PLS discriminant model, when you need to distinguish signal features from noise by establishing empirical significance thresholds rather than relying on parametric assumptions. Particularly valuable when the feature space is high-dimensional (hundreds to thousands of LC-MS features) and you want to control false discovery in downstream metabolite annotation and structural clustering.

## When NOT to use

- When sample size is <30 per group or when rare class imbalance is extreme (<<5% minority class); permutation testing accuracy degrades with too few unique permutations.
- When response is continuous with complex error structure; parametric null models may be more appropriate than label-shuffling.
- When computational budget is severely constrained; 10,000+ permutations with MB-PLS fitting is computationally expensive for very large feature counts (>50k features).
- When you only need effect size or ranking without formal hypothesis testing; VIP scores alone may suffice for exploratory interpretation.

## Inputs

- Multi-assay LC-MS intensity data blocks (e.g., HPOS, LPOS, LNEG as pandas DataFrames with sample rows and feature columns)
- Binary or continuous response variable (y) aligned to sample indices
- Fitted MB-PLS model with computed baseline MB-VIP scores

## Outputs

- Empirical p-value array (one per feature, range [0, 1])
- Null VIP score distribution matrix (features × permutations)
- Boolean mask or feature index list for significant features (p < 0.01)
- Feature importance table with p-values and baseline VIP scores

## How to apply

Perform Y-shuffling permutation testing by randomly permuting the response variable (e.g., disease status or phenotype label), refitting the MB-PLS model on each permuted dataset, and recalculating MB-VIP scores. With ≥10,000 permutations, construct an empirical null distribution of VIP scores for each feature by pooling VIP values across all permutations. Calculate the one-tailed empirical p-value for each feature as the proportion of permuted VIP scores that exceed or equal the observed (non-permuted) VIP score. Features with p < 0.01 threshold are retained as statistically significant and used for downstream structural clustering and annotation.

## Related tools

- **mbpls** (MB-PLS model fitting and MB-VIP score calculation prior to permutation testing) — https://github.com/kopeckylukas/py-mamsi
- **MamsiPls.mb_vip_permtest()** (Core permutation testing and empirical p-value computation method) — https://github.com/kopeckylukas/py-mamsi
- **scikit-learn** (Provides utilities for label shuffling and cross-validation framework)
- **joblib** (Parallel permutation loop execution for computational efficiency)

## Examples

```
p_vals, null_vip = mamsipls.mb_vip_permtest([hpos, lpos, lneg], y, n_permutations=10000, return_scores=True)
mask = np.where(p_vals < 0.01)
selected = x.iloc[:, mask[0]]
```

## Evaluation signals

- Empirical p-value distribution should be approximately uniform on [0, 1] under the null hypothesis (features are noise); check histogram of all p-values for non-uniformity indicating model bias or insufficient permutations.
- Number of significant features (p < 0.01) should be substantially smaller than total feature count and inversely correlated with permutation count; increasing n_permutations should stabilize p-values (coefficient of variation < 10% for borderline features).
- Permuted null VIP distributions should have median ≈ 0 and maximum values well below observed VIP scores for true signal features; examine quantile-quantile plot of null vs. observed.
- Reproducibility check: repeating permutation test with same random_state should yield identical p-values; varying random_state should yield consistent feature ranks (Spearman ρ > 0.95 for top-ranked features).
- Selected significant features should show biological or chemical coherence in downstream structural clustering (isotopologue/adduct grouping, annotation to known metabolites); isolated features with high VIP may indicate overfitting.

## Limitations

- Empirical p-value resolution is limited by permutation count; minimum achievable p-value is 1/(n_permutations+1). With 10,000 permutations, smallest p-value is ~0.0001, so true p-values << 0.0001 cannot be distinguished.
- Assumes exchangeability of samples under the null; label shuffling is invalid if samples are paired, temporally ordered, or hierarchically clustered (e.g., family kinship, batch effects). No guidance provided in the article for such structures.
- Computational cost scales linearly with n_permutations and quadratically with sample count (due to MB-PLS refitting); 10,000 permutations on >1000 samples may exceed typical HPC time budgets. Article mentions a permutation testing guide for computer clusters but does not detail parallelization specifics within the main workflow.
- Permutation testing only controls false discovery rate under the selected null (response shuffling); it does not account for feature selection bias introduced by computing VIP on the full feature set before testing, potentially inflating false positives if features are highly correlated or if model selection (e.g., latent variable count) was tuned on the same data.
- Single p-value threshold (p < 0.01) is fixed in the workflow; no explicit guidance on threshold selection or multiple testing correction (e.g., FDR, Bonferroni) beyond the threshold stated.

## Evidence

- [other] Perform empirical permutation testing (n_permutations≥10,000) using MamsiPls.mb_vip_permtest() with Y shuffling to generate empirical p-values for each feature.: "Perform empirical permutation testing (n_permutations≥10,000) using MamsiPls.mb_vip_permtest() with Y shuffling to generate empirical p-values for each feature."
- [readme] or estimate empirical p-values for all features: p_vals, null_vip = mamsipls.mb_vip_permtest([hpos, lpos, lneg], y, n_permutations=10000, return_scores=True): "or estimate empirical p-values for all features: p_vals, null_vip = mamsipls.mb_vip_permtest([hpos, lpos, lneg], y, n_permutations=10000, return_scores=True)"
- [other] Select statistically significant features at p<0.01 threshold and export feature importance table with p-values and VIP scores.: "Select statistically significant features at p<0.01 threshold and export feature importance table with p-values and VIP scores."
- [readme] Estimation of statistically significant features (variables) using MB-VIP and permutation testing.: "Estimation of statistically significant features (variables) using MB-VIP and permutation testing."
- [readme] mask = np.where(p_vals < 0.01); selected = x.iloc[:, mask[0]]: "mask = np.where(p_vals < 0.01); selected = x.iloc[:, mask[0]]"
