---
name: precursor-mz-window-filtering
description: Use when when preparing augmented training data for Siamese or contrastive learning architectures in mass spectrometry, specifically when you need to generate hard negative examples that are spectrally distinct but mass-similar to positive examples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-mz-window-filtering

## Summary

Filter mass spectrometry spectra by precursor m/z proximity to generate negative training examples within a defined mass window. This skill enforces spectral diversity in training datasets for machine learning models by selecting spectra whose precursor m/z values fall within a specified tolerance of a query spectrum's precursor m/z.

## When to use

When preparing augmented training data for Siamese or contrastive learning architectures in mass spectrometry, specifically when you need to generate hard negative examples that are spectrally distinct but mass-similar to positive examples. Apply this when your training set shows imbalanced positive-to-negative ratios or lacks sufficient within-mass-range negative diversity.

## When NOT to use

- Input dataset already has sufficient negative examples with balanced positive:negative ratios (e.g., 1:1 or better)—direct training is more efficient.
- Query spectra lack reliable precursor m/z values or m/z calibration is poor—window-based filtering will produce unreliable negatives.
- Training objective is mass-independent formula prediction (e.g., fragment-only models); precursor m/z filtering introduces mass bias that contradicts the goal.

## Inputs

- TCN training dataset (spectra with precursor m/z and molecular formula labels)
- Query spectrum (precursor_mz, molecular_formula)
- m/z window tolerance parameter (Da or ppm)

## Outputs

- Augmented training dataset with cross-spectrum negatives
- Balanced positive:negative ratio dataset suitable for Siamese training
- Downsample configuration (ratio applied)

## How to apply

During the rescore data preparation stage, after capping positive examples per molecular formula, iterate over the training set and for each query spectrum, select spectra with precursor m/z values within a defined window (typically ± a small m/z tolerance in Da or ppm) as candidate negatives. This generates 'cross-spectrum' negatives—spectra from different molecular formulas but similar precursor masses—which enforces the model to discriminate molecular formulas at similar mass, not just on spectral similarity alone. Combine these generated negatives with positive examples and downsample to achieve a target positive:negative ratio (e.g., 1:1). The window size is a hyperparameter: smaller windows increase difficulty (harder negatives) but reduce candidate pool; larger windows may include too-distant formulas. Record the window bounds and downsample ratio as part of the training configuration for reproducibility.

## Related tools

- **FIDDLE** (deep learning framework for molecular formula prediction from MS/MS spectra; rescore model training uses this augmented dataset with precursor m/z-windowed negatives) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (CLI and Python API for FIDDLE inference; data preparation scripts are part of the research codebase) — https://github.com/josiehong/msfiddle

## Examples

```
# Pseudo-code for m/z-window negative generation during data preparation
# (as part of prepare_augment_rescore.py workflow)
window_mz = 0.5  # ±0.5 Da tolerance
for query_spectrum in train_set:
    query_mz = query_spectrum['precursor_mz']
    negatives = [s for s in all_spectra 
                 if abs(s['precursor_mz'] - query_mz) <= window_mz 
                 and s['formula'] != query_spectrum['formula']]
    # Combine with positives and downsample to 1:1 ratio
```

## Evaluation signals

- Verify that all selected negative examples have precursor m/z values within the specified window of the query spectrum (e.g., ±0.1 Da or ±10 ppm).
- Confirm that negative examples have different molecular formula labels from the positive example but overlap in precursor mass range, demonstrating spectral-mass confusion.
- Check that the final training dataset achieves the target positive:negative ratio (e.g., exactly 1:1 after downsampling, with no class imbalance > 5%).
- Validate that test set is kept unmodified and separate, to prevent data leakage and ensure unbiased evaluation of Siamese model generalization.
- Inspect that cross-spectrum negatives span multiple spectra per query (not just single closest matches), confirming diverse negative sampling.

## Limitations

- Window size is a critical hyperparameter with no universal optimal value; values too small exhaust the negative candidate pool, while too large introduce uninformative negatives far from the query mass. The article does not explicitly quantify the window size used, so practitioners must tune empirically.
- Assumes precursor m/z values are accurately calibrated and reliable; poor calibration or missing values render the entire filtering approach invalid.
- Does not account for in-source fragmentation, neutral loss, or adduct variation—all spectra in the window are treated equally regardless of chemical relationship beyond mass.
- Downsampling to 1:1 positive:negative may discard valuable information if the original negative pool is small; applications with sparse negative diversity may require alternative augmentation (e.g., data synthesis or semi-supervised learning).

## Evidence

- [other] Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window of the query spectrum.: "Generate cross-spectrum negative examples by selecting spectra with precursor m/z values within a defined window of the query spectrum."
- [other] Downsample the augmented training set to achieve a 1:1 positive-to-negative ratio.: "Downsample the augmented training set to achieve a 1:1 positive-to-negative ratio."
- [readme] The rescore model has been redesigned with a Siamese architecture in v2.0.0.: "The rescore model has been redesigned (Siamese architecture)"
- [other] Cap the number of positive examples per molecular formula in the training set to enforce diversity.: "Cap the number of positive examples per molecular formula in the training set to enforce diversity."
