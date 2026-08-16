---
name: binary-classification-model-training
description: Use when you have curated a labeled dataset of MS/MS spectra annotated as 'relevant' (compounds of interest obtained from reference standards) or 'other' (reference standards or non-target compounds), and you need to build a classifier to automatically distinguish these two classes on unknown.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Binary Classification Model Training for MS/MS Spectra

## Summary

Train a binary classifier to distinguish MS/MS spectra of compounds of interest from other compounds using labeled spectral datasets and ensemble methods. This skill is essential for building AnnoMe classifiers that enable rapid screening of complex natural product extracts.

## When to use

You have curated a labeled dataset of MS/MS spectra annotated as 'relevant' (compounds of interest obtained from reference standards) or 'other' (reference standards or non-target compounds), and you need to build a classifier to automatically distinguish these two classes on unknown spectra. This is particularly applicable when screening plant extracts or environmental samples for specific substance classes (e.g., flavonoids, prenylated compounds).

## When NOT to use

- The training dataset is severely imbalanced (e.g., >10:1 ratio of relevant to other spectra) without resampling or weighting strategies — the README explicitly warns that 'most often the classification will not be successful' in such cases.
- Input spectra are not annotated or you do not have a clear definition of 'relevant' vs 'other' compound classes for your use case.
- You require real-time inference on very large spectral databases without pre-computation of embeddings; the README notes embedding generation took 4 hours on a standard laptop and requires significant computing resources.

## Inputs

- Labeled MS/MS spectra dataset (MGF or repository format)
- Annotations mapping spectra to 'relevant' or 'other' compound classes
- Reference standard MS/MS spectra (for training positive and negative classes)

## Outputs

- Trained binary classifier model (serialized)
- Cached embeddings (MS2DeepScore representations)
- Classification performance metrics (accuracy, precision, recall, F1-score)
- Majority-vote ensemble predictions on validation set

## How to apply

Load the labeled MS/MS spectral dataset into AnnoMe and preprocess spectra using built-in normalization and feature extraction. Split the dataset into training and validation subsets (typically 70/30 or via cross-validation). Train multiple classifiers (LDA, Neural Network, SVM, etc.) on the training subset using cross-validation with different random seeds. Aggregate results via majority-vote to derive the final binary classification. Evaluate classifier performance on the validation subset using accuracy, precision, recall, and F1-score as metrics. Serialize and cache the trained model for reuse on new spectra. Exercise caution with imbalanced training datasets, as they may reduce classification success, and validate results against known compounds before deployment.

## Related tools

- **AnnoMe** (Classification framework for training binary classifiers on MS/MS spectra and managing cross-validation, model aggregation, and majority-vote ensemble prediction) — https://github.com/chrboku/AnnoMe

## Evaluation signals

- Classification performance metrics (accuracy, precision, recall, F1-score) on the validation subset meet acceptable thresholds (typically precision and recall >0.7 for balanced datasets)
- Cross-validation stability: classifiers trained with different random seeds produce consistent majority-vote results, indicating low variance across runs
- The trained model reproduces correct classifications on held-out test spectra from known reference compounds (ground truth validation)
- Cached embeddings persist on disk and significantly reduce subsequent classification runtime from hours to minutes, confirming successful caching
- Majority-vote predictions are consistent with expert manual annotations on a small set of ambiguous or borderline spectra

## Limitations

- Classification success is substantially reduced for highly imbalanced training datasets; the README warns 'most often the classification will not be successful, especially when the training dataset is highly imbalanced'.
- Classification of MS/MS spectra into substance classes is a non-trivial task with inherent failure modes; users must exercise caution with generated results and validate outputs before application.
- Embedding generation (MS2DeepScore) is the computational bottleneck, requiring 4+ hours on standard hardware and exceeding the capabilities of less powerful systems (e.g., MacBook Air M4 with passive cooling).
- Performance depends critically on the quality, diversity, and size of the training dataset; small or unrepresentative training sets will degrade classifier generalization.

## Evidence

- [readme] Classification task definition and data sources: "classifiers first need to be trained on a large set of MS/MS spectra of compounds of interest (e.g., obtained from reference standards) and others (e.g., obtained from reference standards of other"
- [readme] Ensemble methodology and aggregation strategy: "different classifiers (LDA, NN, SVM, etc.) are first trained using cross-validation and different random seeds. The results are then aggregated and a majority-vote is derived"
- [readme] Imbalanced dataset limitation: "most often the classification will not be successful, especially when the training dataset is highly imbalanced"
- [readme] Computational resource constraint: "The limiting step is the generation of the MS2DeepScore embeddings, which took 4 hours on a standard laptop (Intel Core Ultra 5 125U, 12 cores; 16GB main memory; SSD; Windows 11)"
- [other] Evaluation metrics and workflow stages: "Evaluate classifier performance on the validation subset and log accuracy, precision, recall, and F1-score. 6. Serialize and save the trained model."
