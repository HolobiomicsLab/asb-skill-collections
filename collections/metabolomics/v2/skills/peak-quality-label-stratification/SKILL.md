---
name: peak-quality-label-stratification
description: Use when when you have manually labeled LC-MS peaks as 'High quality' or 'Low quality' using NeatMS's annotation tool and need to create training/validation/test batches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - NeatMS
  - Python
  - scikit-learn
  - Keras / TensorFlow
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neatms
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  dedup_kept_from: coll_neatms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02220
  all_source_dois:
  - 10.1021/acs.analchem.1c02220
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-quality-label-stratification

## Summary

This skill involves stratifying MS1 peaks by quality labels (High/Low quality) during batch creation for neural network training, ensuring balanced or representative class distributions to avoid bias in model training. It is essential when preparing labeled LC-MS datasets for supervised learning where peak quality classification affects model generalization.

## When to use

When you have manually labeled LC-MS peaks as 'High quality' or 'Low quality' using NeatMS's annotation tool and need to create training/validation/test batches. Use this skill whenever class imbalance in peak quality labels could skew model training—particularly when the smallest class has fewer than 500 peaks (the recommended minimum per class for full model training), or when you want to enforce equal representation across quality classes.

## When NOT to use

- When you have fewer than ~300–500 peaks total or severely imbalanced quality labels (e.g., one class has <50 peaks); normalisation would discard too much data or create trivially small batches.
- When you have unlabeled peaks or heterogeneous labeling schemes (mixing 'High/Low' with multi-class or continuous quality scores); ensure a single, consistent label vocabulary first.
- When the input data is already a pre-made batch artifact or feature matrix rather than a fresh Experiment object; batching is a one-time preprocessing step, not idempotent.

## Inputs

- Labeled NeatMS Experiment object (with raw LCMS data and feature table)
- NN_handler instance with configured matrix_size, margin, and min_scan_num
- Peak-level quality labels (High/Low) from manual annotation

## Outputs

- Stratified training batch (80% of peaks, class-normalized or original distribution)
- Stratified validation batch (10% of peaks, same class distribution as training)
- Stratified test batch (10% of peaks, same class distribution as training)
- Batch metadata (peak counts per quality class per batch)

## How to apply

After loading a labeled experiment object and instantiating an NN_handler with your desired matrix size (typically 120) and filtering parameters (e.g., min_scan_num=5), call nn_handler.create_batches() with the normalise_class parameter set according to your strategy: set normalise_class=True to ensure every quality class receives equal peak counts (set to the smallest class count) and avoid training bias toward over-represented quality labels; set normalise_class=False to preserve the original class distribution if you want to study label imbalance effects or have naturally balanced data. Record the peak counts per quality class in each resulting batch (training 80%, test 10%, validation 10% by default with validation_split=0.1) and verify that stratification matches your chosen constraint—equal class sizes or original proportions. This ensures the model is not inadvertently trained to recognize dataset-specific class imbalances rather than true peak quality patterns.

## Related tools

- **NeatMS** (Provides NN_handler object and create_batches() method for class-stratified batch creation and peak-quality label management) — https://github.com/bihealth/NeatMS
- **Python** (Scripting environment for instantiating NN_handler and calling batch creation with normalise_class parameters)
- **scikit-learn** (Imported for model evaluation metrics (auc) after stratified batch training)
- **Keras / TensorFlow** (Backend neural network framework used by NeatMS for training on stratified batches)

## Examples

```
nn_handler.create_batches(validation_split=0.1, normalise_class=True)
```

## Evaluation signals

- Verify that when normalise_class=True, all quality classes in each batch have exactly equal peak counts, and that count equals the smallest class size from the original dataset.
- Verify that when normalise_class=False, class distributions in training/validation/test batches match (or closely reflect) the original labeled dataset's proportions.
- Confirm that the union of training + validation + test batches accounts for all (or a documented fraction of) labeled peaks, and no peaks are duplicated across batches.
- Check that the validation_split parameter correctly allocates batches: training ≈ 80%, validation ≈ 10%, test ≈ 10% by count of peaks.
- After model training on stratified batches, inspect confusion matrices or per-class recall/precision to confirm the model does not overfit to class imbalance or artifact distribution biases.

## Limitations

- Normalising class distributions requires discarding peaks from over-represented quality classes; this reduces effective training set size and may sacrifice information about natural class prevalence.
- NeatMS does not automatically recommend whether to use normalise_class=True or False; the choice is user-dependent and should reflect your downstream analysis goal (e.g., balanced classifier vs. prevalence-aware classifier).
- If quality labels are subjective or inconsistent (e.g., annotation drift where 'High quality' definition changes mid-labeling), stratification cannot correct label noise; review mode and re-annotation may be required first.
- Stratified batches assume sufficient labeled data (≥500 peaks per class recommended); smaller datasets may yield batches too small for effective neural network training regardless of stratification strategy.

## Evidence

- [other] When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class equal to the smallest class count: "When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class"
- [other] when set to False, class counts remain unequal, reflecting the original distribution in the dataset.: "when set to False, class counts remain unequal, reflecting the original distribution in the dataset."
- [methods] The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest: "The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest"
- [methods] We recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class).: "We recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class)."
- [methods] A type of peak that was considered `High quality` can slowly change into a `Low quality` as we go along, even with careful attention, it will most certainly happen.: "A type of peak that was considered `High quality` can slowly change into a `Low quality` as we go along, even with careful attention, it will most certainly happen."
