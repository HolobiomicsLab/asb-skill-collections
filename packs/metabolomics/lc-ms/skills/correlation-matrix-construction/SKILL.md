---
name: correlation-matrix-construction
description: Use when after obtaining per-sample model predictions and metabolite signal intensities from a trained deep learning model (e.g., DeepMSProfiler) on LC-MS data from multiple disease groups, and you need to identify and visualize metabolite–disease associations as correlation strengths.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - Python (scipy.stats, numpy)
  - DeepMSProfiler
  - matplotlib / seaborn
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-024-51433-3
  title: DeepMSProfiler
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepmsprofiler_cq
    doi: 10.1038/s41467-024-51433-3
    title: DeepMSProfiler
  dedup_kept_from: coll_deepmsprofiler_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-51433-3
  all_source_dois:
  - 10.1038/s41467-024-51433-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# correlation-matrix-construction

## Summary

Construct a matrix encoding correlation coefficients between metabolite signal intensities and disease class labels across all samples, forming the numerical foundation for metabolite-disease association heatmaps. This is essential for visualizing which metabolite features discriminate between disease phenotypes in LC-MS metabolomics data.

## When to use

After obtaining per-sample model predictions and metabolite signal intensities from a trained deep learning model (e.g., DeepMSProfiler) on LC-MS data from multiple disease groups, and you need to identify and visualize metabolite–disease associations as correlation strengths. Typical trigger: you have raw metabolomics samples grouped by disease class and want to rank metabolites by their association strength with each disease type.

## When NOT to use

- Input metabolite data is already a pre-computed correlation or distance matrix (e.g., already normalized or dimensionality-reduced); this skill requires raw intensity values.
- Sample disease labels are missing or ambiguous for a subset of samples; correlation requires complete label assignments.
- Metabolite intensities contain unhandled missing values (NaN); these must be imputed or filtered before correlation computation.

## Inputs

- Per-sample metabolite signal intensities (n_samples × n_metabolites array, numeric)
- Sample disease class labels (n_samples × 1 vector, categorical or binary-encoded)
- Per-sample model predictions or disease group assignments (n_samples × 1)

## Outputs

- Correlation matrix (n_metabolites × n_diseases, float array)
- Correlation metadata (min/max correlation, coefficient type used)

## How to apply

Load per-sample model outputs (predictions and metabolite signal intensities) for all samples grouped by disease class. For each metabolite feature (row), compute a correlation coefficient (Pearson or Spearman) between that metabolite's signal intensities across all samples and the corresponding disease class labels (encoded numerically or as binary indicators per disease). Organize results into a 2D matrix with metabolites as rows and diseases as columns, where each cell contains the computed correlation coefficient. The choice between Pearson and Spearman depends on signal distribution; Spearman is more robust to non-linear relationships and outliers in mass spectrometry intensity data. Validate that the matrix shape matches (n_metabolites, n_diseases) and that all correlation values lie in [−1, +1].

## Related tools

- **Python (scipy.stats, numpy)** (Compute Pearson or Spearman correlation coefficients between metabolite signals and disease labels; construct and manipulate the correlation matrix)
- **DeepMSProfiler** (Generate per-sample metabolite signal intensities and model outputs that serve as inputs to correlation matrix construction) — https://github.com/yjdeng9/DeepMSProfiler
- **matplotlib / seaborn** (Visualize the correlation matrix as a heatmap after construction)

## Examples

```
import numpy as np; from scipy.stats import pearsonr; metabolite_signals = np.load('model_outputs.npy'); disease_labels = np.loadtxt('label.txt', dtype=int); corr_matrix = np.array([[pearsonr(metabolite_signals[:, i], disease_labels)[0] for j in np.unique(disease_labels)] for i in range(metabolite_signals.shape[1])]); np.save('correlation_matrix.npy', corr_matrix)
```

## Evaluation signals

- Correlation matrix shape is (n_metabolites, n_diseases) with no NaN or inf values.
- All correlation coefficients fall within [−1.0, +1.0]; values outside this range indicate computation error.
- Correlation values are symmetric or anti-symmetric with expected disease phenotypes (e.g., higher |r| for metabolites known to be disease biomarkers).
- Row and column labels correctly correspond to metabolite IDs and disease class names.
- Heatmap visualization displays interpretable color gradients (e.g., red for positive correlation, blue for negative) without rendering artifacts.

## Limitations

- Correlation strength depends on sample size; small cohorts (< 30 samples per group) yield unstable estimates. DeepMSProfiler's demonstration used 859 serum samples (210 healthy, 323 lung nodules, 326 lung cancer).
- Pearson correlation assumes linearity; non-linear metabolite–disease relationships may be missed. Spearman is more robust but discards intensity magnitude information.
- Outlier metabolite intensities or mislabeled samples can bias correlation coefficients; input data quality control is assumed.
- The matrix does not infer causal relationships or mechanistic associations, only linear/monotonic statistical associations.

## Evidence

- [other] Compute correlation coefficients (e.g., Pearson or Spearman) between each metabolite signal and disease class labels for all samples.: "Compute correlation coefficients (e.g., Pearson or Spearman) between each metabolite signal and disease class labels for all samples."
- [other] Construct a correlation matrix with metabolites as rows and diseases as columns.: "Construct a correlation matrix with metabolites as rows and diseases as columns."
- [other] Load the per-sample model outputs (sample predictions and metabolite signal intensities) from the trained DeepMSProfiler model.: "Load the per-sample model outputs (sample predictions and metabolite signal intensities) from the trained DeepMSProfiler model."
- [readme] It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite: "It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite"
