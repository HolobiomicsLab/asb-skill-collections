---
name: positive-negative-class-balancing
description: Use when when training a formula rescoring model on MS/MS spectra where positive examples (correct molecular formulas) are unevenly distributed across molecular formula groups or vastly outnumbered by negative examples (incorrect candidates), resulting in class imbalance that degrades model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - FIDDLE
  - msfiddle
  techniques:
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# positive-negative-class-balancing

## Summary

Balances training datasets by capping positive examples per class and downsampling negative examples to achieve a 1:1 positive-to-negative ratio, preventing model bias toward overrepresented classes in imbalanced molecular formula prediction tasks.

## When to use

When training a formula rescoring model on MS/MS spectra where positive examples (correct molecular formulas) are unevenly distributed across molecular formula groups or vastly outnumbered by negative examples (incorrect candidates), resulting in class imbalance that degrades model generalization.

## When NOT to use

- Input spectra already exhibit approximately 1:1 positive-to-negative ratio in raw form—balancing would discard representative negatives and artificially skew the dataset.
- Test set is being prepared for evaluation—test splits must remain unaugmented and unbalanced to reflect true class prevalence and enable realistic performance metrics.
- Cross-spectrum negative generation parameters (m/z window) are unknown or undefined—without clear precursor m/z thresholds, the skill cannot reliably select hard negatives.

## Inputs

- TCN model predictions on training set (predicted formulas and confidence scores)
- Initial training set (spectra with precursor m/z, true formulas, and spectrum identifiers)
- Test set (spectra with precursor m/z and true formulas)
- Positive-per-formula cap threshold (integer)
- Precursor m/z window width for cross-spectrum negatives (float, in Da or ppm)

## Outputs

- Augmented and balanced training set (1:1 positive:negative ratio, saved to file)
- Unmodified test set (saved to separate file)
- Metadata on capping, cross-spectrum negatives generated, and downsampling statistics

## How to apply

After running TCN model inference on the training set, apply the following pipeline: (1) Cap the number of positive examples per molecular formula to enforce diversity and prevent any single formula from dominating training; (2) Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window (typically ±window threshold) of the query spectrum to create hard negatives; (3) Downsample the augmented training set to achieve exactly 1:1 positive-to-negative ratio by randomly removing excess negative examples. This ensures the Siamese architecture receives balanced pairs without bias toward either class. Retain the test set unmodified to preserve realistic class distributions for unbiased evaluation.

## Related tools

- **FIDDLE** (Siamese rescore model trained on balanced positive-negative pairs to refine molecular formula candidates from MS/MS spectra) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (CLI and Python API packaging FIDDLE's rescore model (v2.0.0 with Siamese architecture) for inference on balanced training data) — https://github.com/josiehong/msfiddle

## Examples

```
# Within the FIDDLE workflow after TCN inference:
python prepare_augment_rescore.py --tcn_train_split ./splits/tcn_train.pkl --tcn_test_split ./splits/tcn_test.pkl --tcn_model_path ./check_point/fiddle_tcn_orbitrap.pt --positive_cap 100 --mz_window 0.01 --output_train ./splits/rescore_train_balanced.pkl --output_test ./splits/rescore_test.pkl
```

## Evaluation signals

- Verify that final training set has exactly equal counts of positive and negative examples (ratio = 1.0 ± tolerance).
- Confirm no molecular formula in the training set exceeds the specified positive cap threshold; check distribution histogram.
- Validate that all negative examples in training set have precursor m/z within the defined window of their paired positive spectra.
- Verify test set remains unchanged in size and class distribution compared to the input unmodified test set.
- Monitor model training curves: balanced sets should show stable loss convergence without divergence favoring one class over the other.

## Limitations

- Capping positives per formula may discard valuable spectral diversity if the cap is too aggressive, reducing model exposure to rare but valid formula variants.
- Cross-spectrum negatives within a narrow precursor m/z window may not capture chemically distant false candidates, potentially undertraining the model on hard false-positive rejection.
- Downsampling negatives to 1:1 ratio discards information; if original negative:positive ratio is very high (e.g., >10:1), significant data loss occurs and may bias the model away from legitimate low-confidence negatives.
- The skill assumes precursor m/z is a reliable proxy for spectral similarity; in noisy or chimeric spectra, window-based negative sampling may include poor hard negatives or miss suitable ones.

## Evidence

- [other] Cap the number of positive examples per molecular formula in the training set to enforce diversity.: "Cap the number of positive examples per molecular formula in the training set to enforce diversity."
- [other] Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window of the query spectrum.: "Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window of the query spectrum."
- [other] Downsample the augmented training set to achieve a 1:1 positive-to-negative ratio.: "Downsample the augmented training set to achieve a 1:1 positive-to-negative ratio."
- [other] the test split is saved without augmentation: "the test split is saved without augmentation"
- [readme] The rescore model has been redesigned (Siamese architecture): "The rescore model has been redesigned (Siamese architecture)"
