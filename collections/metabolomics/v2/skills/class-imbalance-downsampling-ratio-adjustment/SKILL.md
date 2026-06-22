---
name: class-imbalance-downsampling-ratio-adjustment
description: Use when after generating cross-spectrum negative examples via precursor m/z windowing and before training a rescore model (e.g., Siamese architecture in FIDDLE v2.0.0).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle
schema_version: 0.2.0
---

# class-imbalance-downsampling-ratio-adjustment

## Summary

Downsample combined positive and negative training examples to enforce a 1:1 class ratio before training a rescore model. This prevents the model from learning a trivial majority-class classifier when negative examples substantially outnumber positives after data augmentation.

## When to use

After generating cross-spectrum negative examples via precursor m/z windowing and before training a rescore model (e.g., Siamese architecture in FIDDLE v2.0.0). Apply this skill when negative examples created during augmentation outnumber positive examples, risking severe class imbalance that would bias model learning toward the majority class.

## When NOT to use

- Input is already balanced (e.g., pre-filtered dataset with equal positive and negative counts).
- Rescore task does not involve binary classification or has custom class weighting strategies specified.
- Negative examples are not artificially generated but derive from genuine contaminants or biological negatives requiring preservation of their natural distribution.

## Inputs

- TCN train and test set spectra with MS/MS peaks and annotations
- Positive example set (capped per molecular formula)
- Cross-spectrum negative examples (generated within precursor m/z window)

## Outputs

- Balanced augmented train set with 1:1 positive:negative ratio
- Balanced augmented test set with 1:1 positive:negative ratio
- Downsampled example indices or filtered example lists ready for rescore model training

## How to apply

Pool all positive examples (capped per molecular formula to enforce balance constraints) with generated cross-spectrum negatives. Calculate the current positive:negative ratio. Randomly downsample the larger class (typically negatives) until the ratio reaches 1:1. This balanced dataset is then split into train and test sets compatible with rescore model ingestion. The 1:1 ratio ensures the model learns discriminative features rather than defaulting to the majority class; deviating from this threshold risks either underfitting (too few negatives) or overfitting to spurious negative patterns (too many negatives).

## Related tools

- **msfiddle** (Python API and CLI for rescore model training and inference; prepare_augment_rescore.py script applies class-balance downsampling before rescore model training) — https://github.com/josiehong/msfiddle
- **FIDDLE** (Research codebase containing full training pipeline; rescore model uses Siamese architecture (v2.0.0) trained on class-balanced augmented data) — https://github.com/JosieHong/FIDDLE

## Evaluation signals

- Final train and test sets have equal counts of positive and negative examples (ratio = 1.0).
- No examples are duplicated or lost during downsampling; only excess examples are removed.
- Rescore model convergence and validation loss stability indicate the balanced dataset prevents trivial majority-class overfitting.
- Confusion matrix on held-out test set shows balanced precision and recall across positive and negative classes (not skewed toward one class).
- Rank-1 accuracy and top-k candidate ranking scores on external benchmark datasets (CASMI, EMBL-MCF, NIST23) remain consistent with published FIDDLE results.

## Limitations

- Downsampling discards potentially informative negative examples; if negatives encode rare but important noise patterns, uniform random downsampling may lose them.
- 1:1 ratio is empirically chosen for FIDDLE rescore task and may not generalize to other rescore architectures or mass spectrometry instruments (Orbitrap vs. Q-TOF).
- Downsampling can increase variance in small datasets; cross-validation or stratified splitting is required to ensure train/test split preserves class balance.
- The skill assumes cross-spectrum negatives are already generated and capped per molecular formula; upstream steps (precursor m/z windowing, formula-level capping) are prerequisite.

## Evidence

- [other] Generate cross-spectrum negatives by pairing spectra within a defined precursor m/z window. 4. Downsample the combined positive and negative examples to achieve 1:1 positive:negative ratio.: "Generate cross-spectrum negatives by pairing spectra within a defined precursor m/z window. 4. Downsample the combined positive and negative examples to achieve 1:1 positive:negative ratio."
- [readme] The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md).: "The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md)."
- [other] 2. Cap positive examples per molecular formula to enforce class balance constraints.: "2. Cap positive examples per molecular formula to enforce class balance constraints."
