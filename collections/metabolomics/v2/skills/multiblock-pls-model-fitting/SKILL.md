---
name: multiblock-pls-model-fitting
description: Use when you have split multi-assay LC-MS intensity data into training
  (90%) and test (10%) subsets with assay-specific column prefixes, and you need to
  fit a discriminant or regression model that respects the block structure (separate
  assays) while jointly predicting a phenotypic outcome (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3929
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - mbpls
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
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

# multiblock-pls-model-fitting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Fit a Multi-Block Partial Least Squares (MB-PLS) discriminant model to integrate and analyze multi-assay LC-MS metabolomics blocks (e.g., HPOS, LPOS, LNEG) for classification or regression tasks. MB-PLS leverages the NIPALS algorithm to model covariance structure across blocks while predicting a single response variable.

## When to use

You have split multi-assay LC-MS intensity data into training (90%) and test (10%) subsets with assay-specific column prefixes, and you need to fit a discriminant or regression model that respects the block structure (separate assays) while jointly predicting a phenotypic outcome (e.g., disease status, gender) encoded as numeric Y.

## When NOT to use

- Input is already a single aggregated feature table (not multi-block or multi-assay)
- Response variable is continuous and you require prediction intervals or heteroscedastic uncertainty quantification (use regression instead of discriminant model)
- Sample sizes are <50 per class (k-fold cross-validation with n_splits=5 becomes unstable)

## Inputs

- List of pandas DataFrames (one per assay block, e.g., [HPOS_train, LPOS_train, LNEG_train])
- Numeric response vector (y_train: encoded phenotype, e.g., 1 for female, 0 for male)
- Training data split fraction (default 90%)
- Assay-specific column name prefixes (e.g., 'HPOS_', 'LPOS_', 'LNEG_')

## Outputs

- Fitted MamsiPls model object with learned loadings and latent variable weights
- Optimal number of latent variables identified by cross-validation
- Model performance metrics on test set (accuracy, recall, specificity, F1-score, AUC)
- MB-PLS latent variable scores for downstream interpretation

## How to apply

Instantiate MamsiPls with n_components=1 (or a small integer), then call fit([block1, block2, block3], y) where each block is a pandas DataFrame with unit-variance standardization (standardize=True) applied. The NIPALS algorithm iteratively fits latent variables across blocks. After fitting, use estimate_lv() with k-fold cross-validation (n_splits=5) and AUC metric to identify the optimal number of latent variables, stopping when the plateau_threshold (e.g., 0.01) is reached. Refit the model with the optimal component count and evaluate on the held-out test set using evaluate_class_model() to record accuracy, recall, specificity, F1-score, and AUC.

## Related tools

- **mbpls** (Provides the MamsiPls class wrapping the MB_PLS NIPALS algorithm for multi-block PLS model fitting) — https://github.com/kopeckylukas/py-mamsi
- **scikit-learn** (train_test_split() for stratified train/test data partitioning; provides AUC metric for cross-validation)
- **pandas** (Loads and structures multi-assay LC-MS intensity data; applies column name prefixes; concatenates blocks)
- **numpy** (Numerical array operations for internal NIPALS iterations and latent variable computations)

## Examples

```
from mamsi.mamsi_pls import MamsiPls
mamsipls = MamsiPls(n_components=1)
mamsipls.fit([hpos_train, lpos_train, lneg_train], y_train)
mamsipls.estimate_lv([hpos_train, lpos_train, lneg_train], y_train, metric='auc')
metrics = mamsipls.evaluate_class_model([hpos_test, lpos_test, lneg_test], y_test)
```

## Evaluation signals

- Cross-validation AUC curve plateaus (change < plateau_threshold=0.01) and indicates a clear optimal number of latent variables
- Test set AUC, accuracy, and F1-score are within expected ranges for the phenotype (e.g., AUC > 0.70 for binary classification)
- Model loadings (weights) on each block are non-zero and interpretable in the context of known metabolic pathways
- Latent variable scores are orthogonal (zero correlation) across components
- MB-VIP scores computed from the fitted model show expected feature importance ranking (significant metabolites rank higher than background features)

## Limitations

- NIPALS is iterative and sensitive to initialization; reproducibility requires setting random_state or seed consistently
- Assumes block structures (assays) are balanced in sample size; severe imbalance may bias latent variable estimation toward larger blocks
- Unit-variance standardization (standardize=True) assumes all features on similar scales; highly skewed or long-tailed metabolite intensities may require prior log-transformation or robust scaling
- Model does not account for missing data; all blocks must have complete cases for each sample
- Optimal latent variable count is data-dependent and dataset-specific; no universal recommendation provided in the literature

## Evidence

- [methods] Fit MB-PLS discriminant model on training data using MamsiPls with NIPALS algorithm and unit-variance standardization (standardize=True): "Fit MB-PLS discriminant model on training data using MamsiPls with NIPALS algorithm and unit-variance standardization (standardize=True)."
- [methods] Estimate optimal number of latent variables using k-fold cross-validation (n_splits=5) with AUC metric via MamsiPls.estimate_lv(), identifying the model plateau threshold (plateau_threshold=0.01): "Estimate optimal number of latent variables using k-fold cross-validation (n_splits=5) with AUC metric via MamsiPls.estimate_lv(), identifying the model plateau threshold (plateau_threshold=0.01)."
- [methods] Refit MB-PLS with optimal latent variable count and evaluate on independent test set using MamsiPls.evaluate_class_model(), recording accuracy, recall, specificity, F1-score, and AUC: "Refit MB-PLS with optimal latent variable count and evaluate on independent test set using MamsiPls.evaluate_class_model(), recording accuracy, recall, specificity, F1-score, and AUC."
- [readme] MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets: "MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets."
- [readme] mamsipls = MamsiPls(n_components=1); mamsipls.fit([hpos, lpos, lneg], y): "mamsipls = MamsiPls(n_components=1)
mamsipls.fit([hpos, lpos, lneg], y)"
- [readme] Data integration analysis using the Multi-Block Partial Least Squares (MB-PLS) algorithm: "Data integration analysis using the Multi-Block Partial Least Squares (MB-PLS) algorithm."
