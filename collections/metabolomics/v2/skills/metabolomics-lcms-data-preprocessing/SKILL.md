---
name: metabolomics-lcms-data-preprocessing
description: Use when when you have raw LC-MS metabolomics data from multiple disease groups (e.g., .mzML or .npy format files) that must be converted into a uniform, normalized feature representation before training a deep learning classifier to distinguish disease states.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - DeepMSProfiler
  - Python
  - TensorFlow
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
---

# metabolomics-lcms-data-preprocessing

## Summary

Preprocessing and normalization of raw LC-MS metabolomics spectra to extract disease-specific features for downstream deep-learning classification. This skill transforms raw mass spectrometry data into normalized feature matrices suitable for neural network ingestion.

## When to use

When you have raw LC-MS metabolomics data from multiple disease groups (e.g., .mzML or .npy format files) that must be converted into a uniform, normalized feature representation before training a deep learning classifier to distinguish disease states. Use this skill as the mandatory preprocessing step between raw spectral data acquisition and model training.

## When NOT to use

- Input is already a normalized feature table or pre-extracted metabolite abundance matrix (preprocessing would be redundant).
- Raw data originates from a single disease group without comparative disease labels (normalization requires multi-group context).
- Spectra have been preprocessed by a prior tool and you need only to apply model inference, not train from raw data.

## Inputs

- Raw LC-MS metabolomics data files (.mzML or .npy format)
- Directory path containing spectra from multiple disease groups
- Sample metadata mapping filenames to disease labels

## Outputs

- Normalized metabolomics feature matrix (numpy array in .npy format)
- Preprocessed spectra ready for deep learning model input
- Normalized signal intensity values suitable for classification

## How to apply

Load raw LC-MS metabolomics data files (in .mzML or .npy format) from disease group directories using Python. Preprocess and normalize the metabolomics features from the raw spectra to remove batch effects and standardize intensity distributions. The preprocessing pipeline automatically converts .mzML format files to .npy format if needed. Apply feature normalization to ensure all metabolite signals are on a comparable scale before passing the normalized feature matrix to the deep learning model for disease-specific feature extraction. Validation occurs by confirming that output feature vectors have consistent dimensionality across all samples and that intensity distributions are appropriately scaled (e.g., zero mean or bounded ranges depending on the normalization method chosen).

## Related tools

- **DeepMSProfiler** (Orchestrates raw LC-MS data loading, preprocessing, normalization, and deep learning inference within a unified pipeline) — https://github.com/yjdeng9/DeepMSProfiler
- **Python** (Execution environment for data loading, array manipulation, and feature normalization operations)
- **TensorFlow** (Backend deep learning framework that consumes preprocessed normalized feature matrices)

## Examples

```
python mainRun.py -data ../example/data/ -label ../example/label.txt -out ../jobs -run_train -run_pred -run_feature
```

## Evaluation signals

- Output feature matrix dimensions match expected sample count and spectral feature count (e.g., rows = samples, columns = m/z bins or metabolite signals).
- Normalized intensities fall within expected ranges (e.g., [0,1] for min-max scaling or approximately zero-centered for z-score normalization).
- No NaN or infinite values remain in the normalized matrix after preprocessing.
- Distribution of normalized values across samples shows reduced batch effects compared to raw data (visualizable via density plots or PCA).
- Preprocessed data successfully ingests into the deep learning model without shape or dtype errors.

## Limitations

- Preprocessing pipeline assumes .mzML or .npy input formats; other mass spectrometry data formats (e.g., .raw, .mzXML) require external conversion before use.
- Automatic .mzML-to-.npy conversion may fail or produce unexpected results if input files are corrupted or use non-standard encoding; manual validation of converted files is advised.
- Normalization strategy is fixed within the DeepMSProfiler pipeline and cannot be easily customized without modifying source code; users cannot swap normalization methods (e.g., quantile normalization vs. z-score) via command-line arguments.
- Preprocessing does not include peak-picking, m/z alignment, or chromatographic retention-time correction—these steps must be completed before raw data is input to this skill.

## Evidence

- [readme] It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite: "It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels."
- [intro] DeepMSProfiler harnesses deep learning to process complex LC-MS data from different diseases and generate unique disease features: "DeepMSProfiler harnesses deep learning to process complex LC-MS data from different diseases and generate unique disease features"
- [other] Preprocess and normalize the metabolomics features from the raw spectra.: "Preprocess and normalize the metabolomics features from the raw spectra."
- [readme] The demo files are in. npy format. If you upload a file in. mzML format, and the script will automatically convert to. npy format automatically.: "If you upload a file in. mzML format, and the script will automatically convert to. npy format automatically."
- [other] Load raw LC-MS metabolomics data from disease groups using Python.: "Load raw LC-MS metabolomics data from disease groups using Python."
