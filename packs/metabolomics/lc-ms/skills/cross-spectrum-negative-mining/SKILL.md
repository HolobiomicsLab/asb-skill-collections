---
name: cross-spectrum-negative-mining
description: Use when when training a Siamese architecture rescore model for MS/MS-based molecular formula prediction and you have an imbalanced training set with far fewer negative than positive spectrum pairs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3520
  tools:
  - FIDDLE
  - msfiddle
  techniques:
  - LC-MS
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

# cross-spectrum-negative-mining

## Summary

A data augmentation technique that generates hard negative training examples for Siamese network training by selecting spectra with precursor m/z values within a defined window around query spectra. This addresses class imbalance in molecular formula prediction by creating diverse negative pairs that improve model discrimination.

## When to use

When training a Siamese architecture rescore model for MS/MS-based molecular formula prediction and you have an imbalanced training set with far fewer negative than positive spectrum pairs. Use this skill specifically during the data preparation phase before Siamese network training when you need to augment training negatives without modifying the test set.

## When NOT to use

- Test set is not meant to be augmented; this skill applies only to training data preparation.
- When precursor m/z range is too broad, generating negatives so similar in mass that they become false negatives or introduce data leakage.
- Input spectra do not have reliable precursor m/z annotations or chemical ground truth labels; the m/z window selection and diversity capping will fail.

## Inputs

- TCN training set (spectra with formula labels)
- TCN test set (spectra with formula labels)
- Pre-trained TCN model weights
- Precursor m/z window parameter (tolerance, e.g. 10 ppm or Da)
- Positive examples cap per formula (integer)

## Outputs

- Augmented training set with balanced 1:1 positive:negative ratio
- Unmodified test set
- Training pairs compatible with Siamese network input format

## How to apply

After loading TCN train/test splits and running TCN inference on the training set, cap the number of positive examples per molecular formula to enforce chemical diversity. Then, for each query spectrum, mine cross-spectrum negatives by selecting unrelated spectra (different precursor masses or formulas) whose precursor m/z values fall within a defined window (e.g., ±10 ppm or a fixed Da range) around the query's m/z. This window-based selection creates hard negatives—spectra similar in mass but chemically unrelated—which better challenge the model than random negatives. Finally, downsample the augmented training set to achieve a 1:1 positive-to-negative ratio before training. Leave the test set unaugmented to preserve evaluation integrity.

## Related tools

- **FIDDLE** (Hosts the rescore model training pipeline and data preparation code (prepare_augment_rescore.py) that implements cross-spectrum negative mining for Siamese network training.) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (Provides the PyPI package and CLI interface for FIDDLE model inference and prediction; users may apply negative mining as a preprocessing step before retraining or fine-tuning rescore models.) — https://github.com/josiehong/msfiddle

## Examples

```
# Within FIDDLE's prepare_augment_rescore.py workflow:
# 1. Load TCN train/test, run TCN inference
# 2. Cap positives per formula
# 3. For each query spectrum, mine negatives within precursor m/z window (e.g. ±10 ppm)
# 4. Downsample to 1:1 ratio
# 5. Save augmented training set for Siamese rescore model training
python prepare_augment_rescore.py --train_splits tcn_train.pkl --test_splits tcn_test.pkl --tcn_model fiddle_tcn_orbitrap.pt --mz_window 10 --output_dir augmented_data/
```

## Evaluation signals

- Output training set has exactly 1:1 positive:negative ratio; verify row count and label distribution.
- Each positive spectrum pair has matching molecular formula; each negative pair has different formulas.
- Negative spectra precursor m/z values all fall within the specified window (e.g., ±10 ppm) of the query spectrum's m/z.
- Test set row count and label distribution are unchanged from input (no augmentation applied).
- Siamese network training on the augmented set achieves improved rescore performance (e.g., higher rank-1 or rank-5 accuracy) compared to non-augmented or random-negative baselines.

## Limitations

- Quality depends heavily on the m/z window width: too narrow excludes valid negatives; too broad admits false negatives (chemically similar spectra).
- Requires accurate precursor m/z and molecular formula annotations; missing or mislabeled data propagates into training pairs.
- Does not account for instrumental or adduct variation; spectra from different instruments or adducts with overlapping m/z ranges may be misclassified as cross-spectrum negatives.
- The 1:1 downsampling ratio is fixed; datasets with extreme positive/negative imbalance may lose information or require further parameter tuning.

## Evidence

- [other] Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window of the query spectrum.: "Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window of the query spectrum."
- [other] The rescore data preparation pipeline augments the training split by capping positives per formula, generating cross-spectrum negatives within a precursor m/z window, and downsampling to 1:1 positive:negative ratio, while the test split is saved without augmentation.: "augments the training split by capping positives per formula, generating cross-spectrum negatives within a precursor m/z window, and downsampling to 1:1 positive:negative ratio, while the test split"
- [readme] The rescore model has been redesigned (Siamese architecture): "The rescore model has been redesigned (Siamese architecture)"
