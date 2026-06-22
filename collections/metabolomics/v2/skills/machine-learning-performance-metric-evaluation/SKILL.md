---
name: machine-learning-performance-metric-evaluation
description: Use when after training a binary MS/MS spectral classifier on labeled data, apply this skill to quantify classifier performance before deployment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0602
  tools:
  - AnnoMe
  techniques:
  - tandem-MS
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

# machine-learning-performance-metric-evaluation

## Summary

Evaluate trained binary classifiers for MS/MS spectral discrimination by computing standard performance metrics (accuracy, precision, recall, F1-score) on held-out validation data. This skill assesses whether a classifier reliably distinguishes MS/MS spectra of compounds of interest from other compounds.

## When to use

After training a binary MS/MS spectral classifier on labeled data, apply this skill to quantify classifier performance before deployment. Use this when you have a trained AnnoMe model and a validation subset of labeled MS/MS spectra (annotated as 'relevant' or 'other') that were held out from training.

## When NOT to use

- Input validation set is not held-out from training; using training data to evaluate leads to inflated metrics and overfitting bias.
- MS/MS spectra are not preprocessed (normalized, features extracted) in the same manner as training data; metric values will not reflect true generalization.
- Dataset is extremely imbalanced (e.g., >95% one class) and only accuracy is reported; use F1-score, precision, or recall instead to avoid misleading conclusions.

## Inputs

- Trained MS/MS binary classifier model (AnnoMe format)
- Validation subset of labeled MS/MS spectra (annotated as 'relevant' or 'other')
- Preprocessed MS/MS spectra (normalized, features extracted)

## Outputs

- Classification metrics: accuracy, precision, recall, F1-score
- Confusion matrix (true positives, false positives, true negatives, false negatives)
- Serialized trained model with performance metadata

## How to apply

Split your labeled MS/MS spectral dataset into non-overlapping training and validation subsets (typical 70/30 or 80/20). Train the binary classifier on the training subset using AnnoMe with default hyperparameters. After training converges, run inference on the validation subset to generate predictions for each spectrum. Compute accuracy (overall fraction of correct predictions), precision (true positives / predicted positives), recall (true positives / actual positives), and F1-score (harmonic mean of precision and recall) by comparing predicted labels to ground-truth labels. Log and serialize these metrics alongside the trained model. The F1-score is particularly useful when the validation dataset is imbalanced between 'relevant' and 'other' classes, as it penalizes both false positives and false negatives.

## Related tools

- **AnnoMe** (Trains binary classifiers on MS/MS spectra and computes performance metrics on validation data during model evaluation.) — https://github.com/chrboku/AnnoMe

## Examples

```
uv run annome_classificationgui
```

## Evaluation signals

- Accuracy, precision, recall, and F1-score are all in the range [0, 1] or [0, 100%] with no NaN or infinite values.
- Precision + false positive rate sum approximately to 1 (verify internal consistency of the confusion matrix).
- F1-score is ≤ min(precision, recall), confirming it is the harmonic mean and not inflated by class imbalance.
- Metrics are computed on the held-out validation set only, never on the training set (confirmed by data split logging).
- Model serialization succeeds and the saved model can be deserialized and used for new predictions without error.

## Limitations

- Classification of MS/MS spectra into substance classes is a non-trivial task and the classifier will often fail, especially when the training dataset is highly imbalanced (see README limitations).
- Performance metrics computed on a single validation split may be optimistic or pessimistic; consider k-fold cross-validation for more robust estimates.
- High F1-score on validation data does not guarantee performance on truly novel, out-of-distribution MS/MS spectra from new plant extracts or chemical sources not represented in training.
- AnnoMe uses ensemble methods (LDA, NN, SVM, majority-vote aggregation) which can mask underlying classifier disagreement; examine per-classifier predictions to assess model consensus.

## Evidence

- [other] Split dataset into training and validation subsets. Train the binary classifier in AnnoMe using the training subset with default hyperparameters. Evaluate classifier performance on the validation subset and log accuracy, precision, recall, and F1-score.: "Split dataset into training and validation subsets. Train the binary classifier in AnnoMe using the training subset with default hyperparameters. Evaluate classifier performance on the validation"
- [readme] Classification of MS/MS spectra into substance classes is a non-trivial task and most often the classification will not be successful, especially when the training dataset is highly imbalanced.: "Classification of MS/MS spectra into substance classes is a non-trivial task and most often the classification will not be successful, especially when the training dataset is highly imbalanced."
- [readme] Using training data consisting of annotated and labeled MS/MS spectra of compounds of interest and others, different classifiers (LDA, NN, SVM, etc.) are first trained using cross-validation and different random seeds. The results are then aggregated and a majority-vote is derived which indicates the final classification of the input MS/MS spectra to either "relevant" or "other".: "Using training data consisting of annotated and labeled MS/MS spectra of compounds of interest and others, different classifiers (LDA, NN, SVM, etc.) are first trained using cross-validation and"
