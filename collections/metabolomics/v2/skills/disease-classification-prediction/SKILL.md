---
name: disease-classification-prediction
description: Use when you have raw LC-MS metabolomics data from multiple disease groups (in .npy or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3464
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2269
  tools:
  - DeepMSProfiler
  - TensorFlow
  - Keras
  - Python
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

# disease-classification-prediction

## Summary

Apply deep learning to raw LC-MS metabolomics data to generate per-sample disease-type classification labels. This skill leverages neural networks trained on preprocessed mass spectrometry features to distinguish between disease states (e.g., healthy, lung nodule, lung cancer) in a multi-class classification framework.

## When to use

You have raw LC-MS metabolomics data from multiple disease groups (in .npy or .mzML format) with annotated sample labels, and you need to: (1) train a predictive model to classify unknown samples into disease categories, (2) evaluate classification accuracy across a test set, or (3) generate disease-type probability scores for each sample. Use this skill when feature-level classification is the goal (not only biomarker discovery or network analysis).

## When NOT to use

- Input is already a classification label matrix or pre-computed prediction scores—skip directly to evaluation.
- Your goal is biomarker discovery (metabolite-disease correlation) or network inference rather than sample prediction—use the feature extraction or network plotting skill instead.
- You lack disease-annotated training data or have <3 disease categories and <10 samples per category—model will be underfitted and unreliable.

## Inputs

- raw LC-MS metabolomics data in .npy or .mzML format
- sample disease-type labels file (e.g., label.txt with FilePath, Label, Dataset columns)
- datalist mapping data files to labels and train/test partition

## Outputs

- per-sample disease-type classification labels
- confusion matrix (optionally plotted)
- trained deep learning model weights
- prediction confidence scores or probabilities per class

## How to apply

First, preprocess and normalize raw LC-MS spectra into feature matrices. Load raw metabolomics data from disease groups using Python (converting .mzML to .npy if needed). Instantiate a deep learning model (e.g., DenseNet121) with parameters including learning rate (default 1e-4), optimizer (e.g., 'adam'), batch size (default 8), and epochs (default 2). Train the model on the training partition with `-run_train` flag, specifying the datalist path and job directory. After training, invoke prediction on held-out test samples with `-run_pred` flag to generate per-sample disease-type labels and optional confusion matrices. Evaluate correctness by comparing predicted labels against ground-truth labels and computing metrics from the confusion matrix (accuracy, precision, recall per class).

## Related tools

- **DeepMSProfiler** (end-to-end Python package integrating preprocessing, model training, prediction, and feature extraction for LC-MS disease classification) — https://github.com/yjdeng9/DeepMSProfiler
- **TensorFlow** (deep learning backend for model architecture (DenseNet121) and gradient-based training)
- **Keras** (high-level API for model definition and layer specification)
- **Python** (primary language for data loading, preprocessing, and script execution)

## Examples

```
python mainRun.py -data ../example/data/ -label ../example/label.txt -out ../jobs -run_train -run_pred -plot_cm
```

## Evaluation signals

- Confusion matrix diagonal elements are high (>70%) relative to off-diagonal false positives/negatives, indicating accurate per-class predictions.
- Predicted labels match ground-truth test set labels with >80% overall accuracy; per-class precision, recall, and F1-score are balanced and acceptable for clinical/research use.
- AUC-ROC curve (if plotted) shows curves well above the diagonal (AUC > 0.8) for each disease class vs. rest, indicating discriminative model.
- Output files are generated in the job directory (`job_dir/predictions/` or similar) with one label per input sample in the same order as the input datalist.
- Model converges within the specified number of epochs; training and validation loss decrease monotonically or plateau without divergence.

## Limitations

- Requires adequate labeled training data; performance degrades significantly with <10 samples per disease class or highly imbalanced datasets.
- Model assumes input .npy files are already preprocessed (normalized metabolite intensities); raw unnormalized spectra may yield poor predictions.
- Deep learning model is a 'black box' for biomarker attribution; use the feature extraction step (run_feature) to generate RISE heatmaps for interpretability.
- Pretrained model based on serum metabolomics from 859 samples (210 healthy, 323 lung nodules, 326 lung cancer); transfer learning to other tissues, disease types, or LC-MS platforms may require fine-tuning or retraining.
- No automatic hyperparameter tuning; learning rate, batch size, architecture, and epoch count must be manually specified and validated via cross-validation or held-out test set.

## Evidence

- [readme] It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels.: "It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels."
- [intro] DeepMSProfiler harnesses deep learning to process complex LC-MS data from different diseases, taking raw metabolomics data from disease groups as input to generate sample disease type labels as one of its three main outputs.: "DeepMSProfiler harnesses deep learning to process complex LC-MS data from different diseases, taking raw metabolomics data from disease groups as input to generate sample disease type labels"
- [other] 1. Load raw LC-MS metabolomics data from disease groups using Python. 2. Preprocess and normalize the metabolomics features from the raw spectra. 3. Apply a deep learning model to extract disease-specific features from the normalized data. 4. Generate per-sample disease-type classification labels as output.: "Preprocess and normalize the metabolomics features from the raw spectra. 3. Apply a deep learning model to extract disease-specific features from the normalized data. 4. Generate per-sample"
- [readme] python mainRun.py -data ../example/data/ -label ../example/label.txt -out ../jobs -run_train -run_pred -run_feature: "python mainRun.py -data ../example/data/ -label ../example/label.txt -out ../jobs -run_train -run_pred -run_feature"
- [readme] -run_train: Initiates the training process (Boolean, default is False). -run_pred: Initiates the prediction process (Boolean, default is False).: "-run_train: Initiates the training process (Boolean, default is False). -run_pred: Initiates the prediction process (Boolean, default is False)."
- [readme] We provide a pre-trained model based on 859 serum metabolomics samples (210 healthy individuals, 323 lung nodules, 326 lung cancer) for academic use.: "We provide a pre-trained model based on 859 serum metabolomics samples (210 healthy individuals, 323 lung nodules, 326 lung cancer)"
