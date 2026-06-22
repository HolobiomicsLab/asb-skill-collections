---
name: multi-class-label-assignment
description: Use when you have raw LC-MS metabolomics data from multiple disease groups and need to classify new or existing samples into discrete disease categories.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3766
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - DeepMSProfiler
  - TensorFlow
  - Keras
  - Python
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

# multi-class-label-assignment

## Summary

Assign disease-type classification labels to LC-MS metabolomics samples using deep learning models trained on raw mass spectrometry data. This skill produces per-sample disease-type predictions (e.g., healthy, lung nodule, lung cancer) from complex metabolomics profiles.

## When to use

You have raw LC-MS metabolomics data from multiple disease groups and need to classify new or existing samples into discrete disease categories. Apply this skill when you want to move beyond univariate feature analysis to leverage global metabolite patterns via deep learning for multi-class discrimination.

## When NOT to use

- Input data is already a processed feature table without raw spectra — you would lose the benefit of global feature extraction from raw profiles.
- You have fewer than ~20 samples per disease group — ensemble deep learning requires sufficient labeled data to train stable models across multiple runs.
- Your goal is biomarker discovery rather than sample classification — use the feature extraction workflow instead to identify disease-specific metabolite-protein networks.

## Inputs

- Raw LC-MS metabolomics data in .mzML or .npy format
- Sample disease-type labels file (tab-delimited: FilePath, Label, Dataset)
- Training/test split specification

## Outputs

- Per-sample disease-type classification labels (ensemble predictions)
- Confusion matrix visualization
- AUC curve plots for each disease class

## How to apply

Preprocess and normalize raw LC-MS metabolomics features (automatically converting .mzML to .npy format if needed). Train a deep learning model (DenseNet121 or similar) on labeled training samples using the Adam optimizer at learning rate 1.0e-04 over 2+ epochs with batch size 8. Run multiple model instances (default 10 runs) and use ensemble mode to aggregate predictions across runs, producing consensus per-sample disease-type labels. Evaluate ensemble predictions using confusion matrix and AUC plots to verify classification accuracy across disease classes.

## Related tools

- **DeepMSProfiler** (End-to-end deep learning framework that ingests raw LC-MS data, trains ensemble models, and produces per-sample disease-type labels via mainRun.py with -run_train and -run_pred flags) — https://github.com/yjdeng9/DeepMSProfiler
- **TensorFlow** (Deep learning backend (version 2.2.0) for model training and inference)
- **Keras** (High-level neural network API (version 2.3.1) for DenseNet121 model architecture specification)
- **Python** (Scripting and data processing language for implementing preprocessing, model training, and prediction workflows)

## Examples

```
from DeepMSProfiler import *
run_train(datalist_path='DeepMSProfiler/example/datalist.txt',data_dir='DeepMSProfiler/example/data',job_dir='DeepMSProfiler/example/out/jobs007',epoch=2)
run_predict(job_dir='DeepMSProfiler/example/out/jobs007',plot_auc=True,plot_cm=True)
```

## Evaluation signals

- Confusion matrix shows balanced true positive rates across all disease classes (no single class dominates false negatives)
- AUC curves for each disease class exceed 0.85 on held-out test set, indicating discriminative ensemble predictions
- Per-sample label assignments are consistent across majority of the 10 ensemble model runs (>70% agreement threshold)
- Output label file follows format: FilePath, Label, Dataset with no missing or malformed entries
- Ensemble prediction probability distributions are well-calibrated (predicted probability ≈ empirical frequency of correct class)

## Limitations

- Pre-trained model provided is disease-specific (trained on 859 serum metabolomics samples from lung cancer cohort: 210 healthy, 323 lung nodules, 326 lung cancer); transfer to other diseases or sample types may require retraining.
- Requires CUDA-capable GPU (tested with CUDA 10.1) for acceptable training time; CPU-only execution is supported but substantially slower.
- Model architecture (DenseNet121) is fixed; no guidance provided in README for architecture selection or hyperparameter tuning beyond default learning rate, batch size, and epoch count.
- Ensemble approach (10 runs) increases computational cost; no ablation study provided on sensitivity to number of runs or batch size selection.

## Evidence

- [readme] It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels.: "It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels."
- [intro] DeepMSProfiler harnesses deep learning to process complex LC-MS data from different diseases, taking raw metabolomics data from disease groups as input to generate sample disease type labels.: "DeepMSProfiler harnesses deep learning to process complex data from different diseases and generate unique disease features."
- [readme] The demo data can be downloaded from `example` dir or **[Baidu Netdisk](https://pan.baidu.com/s/14v82CMsFZwcTI13iWaTWxA):** `https://pan.baidu.com/s/14v82CMsFZwcTI13iWaTWxA`, **Passward:** `acaa`. The demo files are in. npy format. If you upload a file in. mzML format, and the script will automatically convert to. npy format automatically.: "The demo files are in. npy format. If you upload a file in. mzML format, and the script will automatically convert to. npy format automatically."
- [other] Preprocess and normalize the metabolomics features from the raw spectra. 3. Apply a deep learning model to extract disease-specific features from the normalized data. 4. Generate per-sample disease-type classification labels as output.: "Apply a deep learning model to extract disease-specific features from the normalized data. 4. Generate per-sample disease-type classification labels as output."
- [readme] run_train(datalist_path='DeepMSProfiler/example/datalist.txt',data_dir='DeepMSProfiler/example/data', job_dir='DeepMSProfiler/example/out/jobs007',epoch=2) run_predict(job_dir = 'DeepMSProfiler/example/out/jobs007',plot_auc=True,plot_cm=True): "run_train(datalist_path='DeepMSProfiler/example/datalist.txt',data_dir='DeepMSProfiler/example/data', job_dir='DeepMSProfiler/example/out/jobs007',epoch=2) run_predict(job_dir ="
- [readme] We provide a pre-trained model based on 859 serum metabolomics samples (210 healthy individuals, 323 lung nodules, 326 lung cancer) for academic use.: "We provide a pre-trained model based on 859 serum metabolomics samples (210 healthy individuals, 323 lung nodules, 326 lung cancer) for academic use."
