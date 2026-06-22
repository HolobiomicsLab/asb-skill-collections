---
name: training-validation-dataset-stratification
description: Use when when you have a complete labelled MS/MS spectral dataset annotated as 'relevant' (compounds of interest from reference standards) or 'other' (reference standards or non-target compounds from repositories), and you need to train and evaluate an AnnoMe binary classifier without data leakage.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - AnnoMe
  techniques:
  - LC-MS
derived_from:
- doi: 10.1093/bioadv/vbag111
  title: AnnoMe
evidence_spans:
- This is a package for the classification of MS/MS spectra of novel compounds
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_annome_cq
    doi: 10.1093/bioadv/vbag111
    title: AnnoMe
  dedup_kept_from: coll_annome_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbag111
  all_source_dois:
  - 10.1093/bioadv/vbag111
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# training-validation-dataset-stratification

## Summary

Split a labelled MS/MS spectral dataset into training and validation subsets to enable unbiased evaluation of binary classifiers that distinguish relevant compounds from other compounds. This skill ensures robust performance assessment by reserving held-out data for testing before model deployment.

## When to use

When you have a complete labelled MS/MS spectral dataset annotated as 'relevant' (compounds of interest from reference standards) or 'other' (reference standards or non-target compounds from repositories), and you need to train and evaluate an AnnoMe binary classifier without data leakage. Apply this skill before training to prevent overfitting and obtain honest performance estimates.

## When NOT to use

- Dataset is already split and balanced; this skill is redundant if train/validation partitions exist and class distribution is known.
- Unlabelled or partially labelled spectra; this skill requires complete annotation into 'relevant' or 'other' classes before splitting.
- Single-class dataset or severely imbalanced dataset (e.g., >95% one class); the README warns that 'most often the classification will not be successful, especially when the training dataset is highly imbalanced'.

## Inputs

- Labelled MS/MS spectral dataset (MGF or equivalent format) with annotations: 'relevant' or 'other' class labels
- Reference standards MS/MS spectra (for 'relevant' class)
- Other compounds MS/MS spectra from reference standards or repositories (for 'other' class)

## Outputs

- Training subset (70–80% of labelled spectra)
- Validation subset (20–30% of labelled spectra)
- Trained binary classifier model (serialized)
- Performance metrics (accuracy, precision, recall, F1-score on validation subset)

## How to apply

Load your labelled MS/MS spectral dataset into AnnoMe, ensuring spectra are annotated into two classes: 'relevant' for compounds of interest and 'other' for reference standards or non-target compounds. Preprocess the full dataset using AnnoMe's built-in normalization and feature extraction to ensure consistent representation. Stratify the dataset by splitting into training and validation subsets (typical ratio 70–80% training, 20–30% validation) while preserving class distribution to avoid imbalance bias. Train the binary classifier on the training subset using AnnoMe's default hyperparameters with cross-validation. Reserve the validation subset entirely for post-training evaluation, computing accuracy, precision, recall, and F1-score to assess classifier performance on unseen data before serializing the trained model.

## Related tools

- **AnnoMe** (Loads labelled MS/MS spectral dataset, preprocesses spectra via normalization and feature extraction, splits into training/validation subsets, trains binary classifier, evaluates on validation set, and serializes trained model) — https://github.com/chrboku/AnnoMe

## Examples

```
uv run annome_classificationgui  # Load labelled MGF, select 'Training/Validation Split' option, set ratio to 75/25, preprocess with normalization, train on training subset, evaluate on validation subset
```

## Evaluation signals

- Training and validation subset sizes sum to 100% of original labelled dataset; no spectra are duplicated across subsets.
- Class distribution (ratio of 'relevant' to 'other') is preserved or similar between training and validation subsets, indicating stratified split.
- Validation subset performance metrics (accuracy, precision, recall, F1-score) are computed only on data withheld from training; no training samples appear in validation results.
- Serialized model file is created and can be reloaded without error, confirming successful training completion.
- Performance metrics are reasonable and interpretable (values in [0, 1] range); extreme imbalance (e.g., F1-score << 0.1) signals dataset quality issues per README.

## Limitations

- Classification of MS/MS spectra into substance classes is non-trivial; the README notes 'most often the classification will not be successful, especially when the training dataset is highly imbalanced.' Users are warned to exercise caution with results.
- Validation subset size and class balance directly affect reliability of performance estimates; small or severely imbalanced validation sets may not reflect real-world classifier performance.
- Stratification alone does not address missing or mislabelled spectra in the source dataset; data quality issues upstream of this skill will propagate into both subsets.

## Evidence

- [other] Split dataset into training and validation subsets: "Split dataset into training and validation subsets."
- [other] Labelled MS/MS spectra annotated as 'relevant' or 'other': "Load labelled MS/MS spectral dataset containing spectra annotated as 'relevant' (compounds of interest) or 'other' (reference standards or non-target compounds)"
- [readme] Training data from reference standards and repositories: "the classifiers first need to be trained on a large set of MS/MS spectra of compounds of interest (e.g., obtained from reference standards) and others (e.g., obtained from reference standards of"
- [other] Evaluation on validation subset with performance metrics: "Evaluate classifier performance on the validation subset and log accuracy, precision, recall, and F1-score."
- [readme] Imbalance warning in README: "most often the classification will not be successful, especially when the training dataset is highly imbalanced."
