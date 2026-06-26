---
name: formula-stratified-sampling
description: 'Use when when preparing MS/MS spectral training data where: (1) the
  initial TCN train/test split contains imbalanced positive and negative examples,
  (2) certain molecular formulas are over-represented in the positive class, (3) you
  are training a Siamese architecture rescore model that requires.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - FIDDLE
  - msfiddle
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# formula-stratified-sampling

## Summary

A data augmentation technique that caps positive examples per molecular formula and generates cross-spectrum negatives to create balanced training datasets for Siamese rescoring models. This ensures diversity in positive classes and prevents formula-specific bias in deep learning models trained on imbalanced MS/MS spectral data.

## When to use

When preparing MS/MS spectral training data where: (1) the initial TCN train/test split contains imbalanced positive and negative examples, (2) certain molecular formulas are over-represented in the positive class, (3) you are training a Siamese architecture rescore model that requires balanced pairwise comparisons, or (4) you need to prevent the model from learning formula-specific rather than spectrum-based features.

## When NOT to use

- Input is already balanced or contains only a few distinct molecular formulas (capping will be ineffective).
- You are not using a Siamese or contrastive learning architecture; standard supervised learning may not benefit from explicit negative generation.
- The MS/MS spectra lack reliable precursor m/z values or mass accuracy is poor (>10 ppm error), undermining precursor window-based negative selection.

## Inputs

- TCN train split (MS/MS spectra with formula labels and precursor m/z)
- TCN test split (MS/MS spectra with formula labels)
- Pre-trained TCN model checkpoint
- Precursor m/z window parameter (Da tolerance)

## Outputs

- Augmented training dataset (1:1 positive:negative ratio, capped per-formula, with cross-spectrum negatives)
- Unmodified test dataset for evaluation
- Metadata tracking positive cap thresholds and negative generation statistics

## How to apply

Load the TCN training set and run inference using a pre-trained TCN model to obtain base predictions. For each molecular formula in the training set, enforce diversity by capping the number of positive examples per formula. Generate cross-spectrum negatives by selecting spectra whose precursor m/z values fall within a defined window (typically within a few Da) of the query spectrum's precursor m/z, ensuring negatives are physically plausible but chemically distinct. Downsample the augmented training set to achieve a 1:1 positive-to-negative ratio. Save the augmented training set for Siamese model training and preserve the unmodified test set to maintain fair evaluation. The capping and negative generation enforce both diversity (preventing formula memorization) and class balance (enabling effective Siamese contrastive learning).

## Related tools

- **FIDDLE** (Provides pre-trained TCN model for inference and rescore model training framework that uses formula-stratified sampling for data preparation) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (CLI and Python API for deploying FIDDLE models; encapsulates the rescore model trained on formula-stratified augmented data) — https://github.com/josiehong/msfiddle

## Evaluation signals

- Positive-to-negative ratio in augmented training set equals 1:1 (verify class balance).
- Number of positive examples per formula does not exceed the specified cap threshold (verify diversity enforcement).
- Cross-spectrum negatives have precursor m/z values within the defined window of corresponding query spectra (verify negative plausibility).
- Test set remains unmodified and contains the same spectra and labels as input (verify evaluation integrity).
- Rescore model achieves higher ranking precision and lower false-positive rate on the test set compared to models trained on non-augmented or unbalanced data.

## Limitations

- Formula diversity depends on having sufficient spectra per formula; rare formulas may be under-represented even after capping.
- Precursor m/z window selection is critical but not data-driven in the article; suboptimal window size may generate implausible negatives or miss relevant cross-spectrum pairs.
- Downsampling to 1:1 ratio discards potentially informative negative examples, reducing total training data volume and may impact performance on data-rich scenarios.
- The technique assumes TCN predictions are reliable enough to filter training data; poor TCN model quality will propagate errors into augmented sets.
- Does not account for isomeric or isobaric spectra; two distinct formulas with identical precursor m/z will not be distinguished during negative generation.

## Evidence

- [other] Cap the number of positive examples per molecular formula in the training set to enforce diversity.: "Cap the number of positive examples per molecular formula in the training set to enforce diversity."
- [other] Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window of the query spectrum.: "Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window of the query spectrum."
- [other] Downsample the augmented training set to achieve a 1:1 positive-to-negative ratio.: "Downsample the augmented training set to achieve a 1:1 positive-to-negative ratio."
- [readme] The rescore model has been redesigned (Siamese architecture): "The rescore model has been redesigned (Siamese architecture)"
- [other] Run inference on the training set using the TCN model to obtain predictions.: "Run inference on the training set using the TCN model to obtain predictions."
