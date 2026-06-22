---
name: spectrum-relevance-classification
description: Use when you have a collection of MS/MS spectra from reference standards representing your compounds of interest (e.g., flavonoids, prenylated chalcones) and a set of MS/MS spectra from non-target or other compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3659
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

# spectrum-relevance-classification

## Summary

Train binary classifiers on annotated MS/MS spectra to distinguish compounds of interest (relevant) from other compounds using AnnoMe's ensemble approach. This skill enables automated filtering and prioritization of unknown MS/MS spectra in metabolomics and natural products discovery workflows.

## When to use

You have a collection of MS/MS spectra from reference standards representing your compounds of interest (e.g., flavonoids, prenylated chalcones) and a set of MS/MS spectra from non-target or other compounds. You want to automatically classify unknown spectra from complex biological extracts into these two categories so that follow-up structural elucidation effort focuses on relevant compounds.

## When NOT to use

- Your training dataset is highly imbalanced (e.g., vastly more 'other' than 'relevant' spectra) — AnnoMe documentation explicitly cautions that imbalanced datasets often result in unsuccessful classification
- You have fewer than ~50–100 high-quality reference spectra per class — classifier ensemble training requires sufficient labeled data to learn robust decision boundaries
- Your unknown spectra come from a substantially different ionization source, mass analyzer, or collision energy regime than your training spectra — domain shift will degrade generalization

## Inputs

- Labeled MS/MS spectral dataset in MGF format with annotations ('relevant' or 'other')
- Reference standards MS/MS spectra from compounds of interest
- Reference standards MS/MS spectra from other compounds or public repositories

## Outputs

- Trained binary classifier model (serialized)
- Validation performance metrics (accuracy, precision, recall, F1-score)
- Classification predictions ('relevant' or 'other') on unknown spectra

## How to apply

Load your labeled MS/MS spectral dataset into AnnoMe, divided into two categories: 'relevant' (reference spectra of compounds of interest) and 'other' (reference spectra from MS/MS repositories or non-target standards). Preprocess spectra using AnnoMe's normalization and feature extraction, then split data into training and validation subsets. Train multiple classifiers (LDA, NN, SVM, etc.) using cross-validation with different random seeds; AnnoMe aggregates results via majority-vote to produce the final classification. Evaluate performance on the validation subset using accuracy, precision, recall, and F1-score. Once performance is acceptable, serialize the trained model for inference on unknown spectra. Note that highly imbalanced training datasets will degrade performance, and the majority-vote aggregation strategy helps mitigate individual classifier errors.

## Related tools

- **AnnoMe** (Primary tool for training binary classifiers on MS/MS spectra and performing majority-vote ensemble classification of relevant vs. other compounds) — https://github.com/chrboku/AnnoMe

## Examples

```
uv run annome_classificationgui
```

## Evaluation signals

- Validation set F1-score, precision, and recall are all ≥0.75 (or domain-appropriate threshold), indicating balanced classification performance
- Cross-validation results across different random seeds show low variance in performance metrics, confirming model stability
- Confusion matrix on validation data shows minimal false-positive and false-negative rates for the 'relevant' class
- When applied to inference spectra from known producer organisms (e.g., Paulownia tomentosa for prenylated flavonoids), the classifier identifies expected compounds with high confidence
- Class distribution in predicted labels on unknown spectra is consistent with prior knowledge (e.g., if 'relevant' compounds are known to be rare, <5% 'relevant' predictions is expected)

## Limitations

- Classification of MS/MS spectra into substance classes is non-trivial and success is not guaranteed, especially with highly imbalanced training datasets
- Performance depends critically on the quality, diversity, and representativeness of the reference standard MS/MS spectra used for training
- Majority-vote ensemble aggregation requires sufficient compute resources to train multiple classifiers; embedding generation (MS2DeepScore) is the most time-consuming step and may require 4+ hours on standard hardware
- Model generalization to spectra from novel ionization methods, instruments, or collision energies not represented in training data is not guaranteed

## Evidence

- [readme] Classification of MS/MS spectra into substance classes is a non-trivial task and most often the classification will not be successful, especially when the training dataset is highly imbalanced.: "Classification of MS/MS spectra into substance classes is a non-trivial task and most often the classification will not be successful, especially when the training dataset is highly imbalanced."
- [readme] Different classifiers (LDA, NN, SVM, etc.) are first trained using cross-validation and different random seeds. The results are then aggregated and a majority-vote is derived which indicates the final classification.: "different classifiers (LDA, NN, SVM, etc.) are first trained using cross-validation and different random seeds. The results are then aggregated and a majority-vote is derived which indicates the"
- [readme] The classifiers first need to be trained on a large set of MS/MS spectra of compounds of interest (e.g., obtained from reference standards) and others (e.g., obtained from reference standards of other compounds and from large MS/MS spectra repositories).: "the classifiers first need to be trained on a large set of MS/MS spectra of compounds of interest (e.g., obtained from reference standards) and others (e.g., obtained from reference standards of"
- [readme] The generation of the MS2DeepScore embeddings, which took 4 hours on a standard laptop (Intel Core Ultra 5 125U, 12 cores; 16GB main memory; SSD; Windows 11).: "The generation of the MS2DeepScore embeddings, which took 4 hours on a standard laptop (Intel Core Ultra 5 125U, 12 cores; 16GB main memory; SSD; Windows 11)"
- [readme] Binary classification into 'relevant' or 'other' compounds. In this respect, the classification result 'relevant' refers to specific substance classes of interest to the user, while the classification result 'other' refer to structures not of interest.: "classification of MS/MS spectra of novel compounds into either "relevant" or "other" compounds. In this respect, the classification result "relevant" refers to specific substance classes of interest"
