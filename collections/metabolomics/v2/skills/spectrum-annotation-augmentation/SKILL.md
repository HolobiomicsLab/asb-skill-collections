---
name: spectrum-annotation-augmentation
description: Use when you have a TCN-predicted training set of MS/MS spectra with formula annotations and need to prepare it for Siamese rescore model training.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - FIDDLE
  - msfiddle
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
schema_version: 0.2.0
---

# spectrum-annotation-augmentation

## Summary

Augment tandem mass spectra training sets by capping positive examples per molecular formula, generating cross-spectrum negatives within precursor m/z windows, and downsampling to balanced positive:negative ratios. This prepares diverse, balanced datasets suitable for training Siamese architecture rescore models in formula prediction workflows.

## When to use

You have a TCN-predicted training set of MS/MS spectra with formula annotations and need to prepare it for Siamese rescore model training. The training set exhibits class imbalance (more negatives than positives) or lacks sufficient negative diversity across precursor m/z ranges, and you want to enforce both formula-level diversity and balanced 1:1 positive:negative ratios without modifying the test set.

## When NOT to use

- Test set is being prepared for model evaluation — test data should remain unaugmented to preserve unbiased performance metrics.
- Training set already exhibits balanced positive:negative ratios and sufficient negative diversity — augmentation may introduce unnecessary redundancy.
- Precursor m/z window parameter is unknown or undefined — cross-spectrum negatives require a biologically or instrumentally justified window width.

## Inputs

- TCN train split (MGF or spectrum object format with formula annotations)
- TCN test split (MGF or spectrum object format)
- Pre-trained TCN model checkpoint
- Precursor m/z window tolerance (numeric, e.g., ±50 Da)
- Positive examples cap per formula (numeric threshold)

## Outputs

- Augmented training dataset with balanced 1:1 positive:negative ratio
- Unmodified test dataset (saved separately)
- Metadata on augmentation statistics (formulas capped, negatives generated, downsample ratio)

## How to apply

Load the TCN train/test splits and run inference on the training set using the pre-trained TCN model to obtain initial predictions. Cap the number of positive examples per molecular formula to enforce diversity and reduce redundancy within each formula class. Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window (e.g., ±tolerance) of each query spectrum, ensuring negatives span different chemical formulas. Downsample the augmented training set to achieve a 1:1 positive-to-negative ratio, randomly selecting negatives if necessary. Save the augmented training set and leave the test set unmodified to preserve unbiased evaluation.

## Related tools

- **FIDDLE** (Provides pre-trained TCN model for inference on training set to obtain initial predictions before augmentation; v2.0.0 rescore model uses Siamese architecture trained on augmented data) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (CLI and Python API for FIDDLE model inference; supports batch prediction on training spectra) — https://github.com/josiehong/msfiddle

## Examples

```
# From FIDDLE workflow: Load TCN, augment train split, save augmented data
# Pseudocode snippet:
prepare_augment_rescore(tcn_model, train_split, test_split, precursor_mz_window=50, pos_cap_per_formula=100, output_train_path='train_augmented.pkl', output_test_path='test.pkl')
```

## Evaluation signals

- Verify 1:1 positive:negative ratio in augmented training set output.
- Confirm that no molecular formula in the augmented training set exceeds the specified positive examples cap.
- Check that all generated cross-spectrum negatives have precursor m/z values within the defined window of their respective query spectra.
- Validate that test set remains unmodified (identical record count and annotations before and after augmentation pipeline).
- Inspect augmentation statistics log for anomalies: zero negatives generated, formulas with no positives remaining, or downsample failure.

## Limitations

- Augmentation quality depends on TCN model accuracy; poor TCN predictions will propagate errors into the training set.
- Cross-spectrum negatives are selected by m/z window only; no chemical structure similarity or spectral cosine similarity filtering is applied, so some negatives may be close structural analogs.
- Capping positives per formula may discard valid training examples, reducing signal for rare or underrepresented formulas.
- Downsampling negatives to 1:1 ratio discards information; if true negative:positive ratio in data is higher, the imbalance reduction may hurt generalization to imbalanced real-world queries.
- Pipeline assumes precursor m/z window parameter is fixed; dynamic or data-driven window selection is not described.

## Evidence

- [other] Cap the number of positive examples per molecular formula in the training set to enforce diversity.: "Cap the number of positive examples per molecular formula in the training set to enforce diversity."
- [other] Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window of the query spectrum.: "Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window of the query spectrum."
- [other] Downsample the augmented training set to achieve a 1:1 positive-to-negative ratio.: "Downsample the augmented training set to achieve a 1:1 positive-to-negative ratio."
- [readme] The rescore model has been redesigned (Siamese architecture): "The rescore model has been redesigned (Siamese architecture)"
- [other] Run inference on the training set using the TCN model to obtain predictions.: "Run inference on the training set using the TCN model to obtain predictions."
