---
name: spectral-feature-normalization
description: Use when when you have raw LC-MS metabolomics data in .mzML or .npy format
  from multiple disease groups with varying ionization efficiencies or detector sensitivities,
  and you need to train a deep learning model for disease classification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - DeepMSProfiler
  - TensorFlow / Keras
  - Python
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-feature-normalization

## Summary

Preprocessing step that normalizes metabolomics features extracted from raw LC-MS spectra to remove intensity scaling artifacts and enable comparable signal intensities across samples. Essential for preparing heterogeneous spectral data for deep learning classification.

## When to use

When you have raw LC-MS metabolomics data in .mzML or .npy format from multiple disease groups with varying ionization efficiencies or detector sensitivities, and you need to train a deep learning model for disease classification. Use this skill before feature extraction and model training to ensure that metabolite signal intensities are on comparable scales across all samples, preventing high-intensity samples from dominating model learning.

## When NOT to use

- Input is already a pre-normalized or log-transformed feature table from another analysis pipeline.
- You are working with MS/MS fragmentation spectra rather than intact LC-MS profiles, where intensity patterns encode structural information that may be altered by aggressive normalization.
- Sample-level metadata (e.g., acquisition batch, instrument configuration) indicates systematic differences that require batch-effect correction rather than simple feature normalization.

## Inputs

- raw LC-MS metabolomics data (.mzML or .npy format)
- spectral intensity matrix from disease groups
- per-sample disease-type labels (.txt file)

## Outputs

- normalized metabolomics feature matrix (.npy format)
- scaled spectral data ready for deep learning model input

## How to apply

Load raw LC-MS metabolomics data (provided as .mzML files converted to .npy format) and apply normalization to the spectral features extracted from the intensity matrix. The normalization step standardizes feature distributions across the dataset, removing instrument-dependent intensity variations while preserving disease-specific metabolite signals. This is performed as part of the preprocessing pipeline after raw spectrum loading but before deep learning model application. Use DeepMSProfiler's preprocessing module with default settings or with TensorFlow/Keras-compatible normalization (e.g., per-sample z-score or min-max scaling). Verify that output feature matrices have consistent statistical properties (mean ~0, std ~1 for z-score; range [0,1] for min-max) and that disease-group separation is preserved in the normalized feature space.

## Related tools

- **DeepMSProfiler** (End-to-end framework that integrates spectral normalization as part of its preprocessing pipeline before deep learning-based disease classification) — https://github.com/yjdeng9/DeepMSProfiler
- **TensorFlow / Keras** (Deep learning backend used after normalization for model training and feature extraction)
- **Python** (Programming environment and runtime for executing normalization workflows)

## Examples

```
python mainRun.py -data ../example/data/ -label ../example/label.txt -out ../jobs -run_train -run_pred -run_feature
```

## Evaluation signals

- Normalized feature matrix has consistent statistics across samples (e.g., per-feature mean ≈ 0 and std ≈ 1 for z-score normalization, or all values in [0,1] range for min-max scaling).
- Disease-group separation is preserved or improved in downstream visualizations (e.g., PCA plots, t-SNE, or heatmaps of metabolite-disease correlations).
- Deep learning model convergence is improved (lower training loss, better validation accuracy) compared to models trained on unnormalized raw spectra.
- Output .npy files contain no NaN, Inf, or out-of-range values that would cause model training failures.
- Heatmaps and confusion matrices produced by the downstream classification step show consistent disease labeling accuracy across all three disease classes (healthy, lung nodule, lung cancer in the example dataset).

## Limitations

- Normalization may obscure absolute intensity differences that carry diagnostic value if disease-specific metabolites have systematically different ionization efficiencies.
- The choice of normalization method (z-score, min-max, quantile, etc.) is not explicitly specified in the README and may require empirical validation for new disease cohorts or metabolite panels.
- Normalization assumes that the majority of spectral features represent background noise or confounding factors rather than true biological signal; highly skewed distributions (e.g., dominance of a single metabolite) may require robust or specialized scaling methods.
- Pre-trained models provided by the authors (trained on 859 serum metabolomics samples) may not transfer well to unnormalized or differently-normalized data from new cohorts.

## Evidence

- [other] Preprocess and normalize the metabolomics features from the raw spectra: "Preprocess and normalize the metabolomics features from the raw spectra."
- [readme] DeepMSProfiler is a tool for mining global features from raw metabolomics data. It takes raw metabolomics data from different disease groups as input and provides three main outputs: "Unlike traditional metabolomics data analysis tools, ``DeepMSProfiler`` is a tool for mining global features from raw metabolomics data. It takes raw metabolomics data from different disease groups"
- [readme] The demo files are in .npy format. If you upload a file in .mzML format, the script will automatically convert to .npy format automatically.: "The demo files are in. npy format. If you upload a file in. mzML format, and the script will automatically convert to. npy format automatically."
- [other] Apply a deep learning model to extract disease-specific features from the normalized data: "Apply a deep learning model to extract disease-specific features from the normalized data."
