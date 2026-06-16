---
name: rescore-training-data-augmentation
description: Use when when you have TCN-predicted candidate formulas with ranked scores and need to train a Siamese rescore model to re-rank those candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3936
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - msfiddle
  - FIDDLE
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- 'CLI and Python API: [msfiddle](https://github.com/josiehong/msfiddle)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
---

# rescore-training-data-augmentation

## Summary

Data augmentation pipeline for preparing balanced training and test sets for Siamese rescore models in MS/MS formula prediction. Applies positive example capping, cross-spectrum negative generation, and downsampling to enforce class balance before rescore model training.

## When to use

When you have TCN-predicted candidate formulas with ranked scores and need to train a Siamese rescore model to re-rank those candidates. Use this skill after TCN model inference has generated train and test sets with spectrum–formula pairs, and you need to create balanced positive/negative training data to avoid class imbalance during rescore training.

## When NOT to use

- Input spectra have already been augmented and balanced by another pipeline
- You are training only a TCN model (formula predictor), not a rescore (re-ranker) model
- Precursor m/z values or adduct annotations are missing or unreliable; cross-spectrum negative sampling depends on accurate m/z windowing

## Inputs

- TCN train set spectra (m/z and intensity arrays)
- TCN test set spectra (m/z and intensity arrays)
- Spectrum annotations (true molecular formulas, precursor m/z values, adduct types)

## Outputs

- Augmented train set with balanced positive and negative spectrum–formula pairs
- Augmented test set with balanced positive and negative spectrum–formula pairs
- Output files in rescore model training format

## How to apply

Load TCN train and test set spectra and their annotations (true formulas). Cap the number of positive examples (correct formula matches) per molecular formula to enforce class balance constraints. Generate negative examples by pairing spectra with incorrect formulas sampled from other spectra within a defined precursor m/z window (cross-spectrum negatives). Downsample the combined positive and negative example pools to achieve a target 1:1 positive:negative ratio. Write augmented train and test sets to output files in a format compatible with rescore model ingestion (expected by the Siamese network training pipeline).

## Related tools

- **msfiddle** (Python API and CLI for FIDDLE; used to run rescore model training and inference after augmented data preparation) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Research codebase containing prepare_augment_rescore.py and rescore model training scripts; orchestrates TCN and Siamese rescore training workflows) — https://github.com/JosieHong/FIDDLE

## Evaluation signals

- Positive:negative example ratio in augmented output is 1:1 or matches the target ratio specified
- No positive example (correct formula) is duplicated more than the specified per-formula cap
- All negative examples (incorrect formulas) are drawn from spectra within the defined precursor m/z window
- Output file format is readable by the Siamese rescore model training pipeline without schema errors
- Train and test set sizes are comparable and both contain balanced positive/negative pairs

## Limitations

- Class balance enforcement by capping positives and downsampling may discard rare molecular formulas or underrepresented spectra, reducing diversity in the training set
- Cross-spectrum negative generation depends on a predefined precursor m/z window; window size is a hyperparameter that may need tuning for different datasets or ionization modes
- Downsampling to 1:1 ratio discards training signal; if negatives are expensive to generate (e.g., sparse in the m/z window), the effective training set size may be small
- The article does not provide explicit details about the prepare_augment_rescore.py script's parameters, window sizes, or capping thresholds, limiting reproducibility

## Evidence

- [other] Cap positive examples per molecular formula to enforce class balance constraints. Generate cross-spectrum negatives by pairing spectra within a defined precursor m/z window. Downsample the combined positive and negative examples to achieve 1:1 positive:negative ratio.: "Cap positive examples per molecular formula to enforce class balance constraints. Generate cross-spectrum negatives by pairing spectra within a defined precursor m/z window. Downsample the combined"
- [readme] The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md.: "The rescore model has been redesigned (Siamese architecture), see details in CHANGELOG.md."
- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra.: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra."
- [other] Write augmented train and test sets to output files in format compatible with rescore model ingestion.: "Write augmented train and test sets to output files in format compatible with rescore model ingestion."
