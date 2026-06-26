---
name: batch-construction-parameter-optimization
description: Use when preparing labeled LC-MS peak data for neural network training
  and you need to decide whether class imbalance in your dataset should be preserved
  or corrected in batch construction. Use it particularly when your annotated peak
  dataset has unequal class distributions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - NeatMS
  - Python
  - Keras
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create
  a `Neural network handler` object
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Batch Construction Parameter Optimization

## Summary

Optimize the creation of training, validation, and test batches for neural network training by systematically comparing class-normalized versus unnormalized batch creation strategies. This skill determines whether to balance class distributions within batches based on dataset characteristics and model training objectives.

## When to use

Apply this skill when preparing labeled LC-MS peak data for neural network training and you need to decide whether class imbalance in your dataset should be preserved or corrected in batch construction. Use it particularly when your annotated peak dataset has unequal class distributions (e.g., true peaks vs. false positives) and you must evaluate the trade-off between training on natural class proportions versus ensuring equal representation per class.

## When NOT to use

- Your annotated dataset already has balanced class counts — batch normalization will discard data unnecessarily
- You are using transfer learning with a pre-trained model rather than full model training — the pre-trained weights may already encode class-balanced assumptions
- Your dataset has fewer than 500 peaks in the smallest class and you intend full model training — normalization will further reduce per-class sample counts below recommended minimums

## Inputs

- Labeled NeatMS Experiment object (instantiated with raw_data_folder_path, feature_table_path, and input_data containing 10–20 pooled representative samples)
- NN_handler object (initialized with experiment, matrice_size, margin, and min_scan_num parameters)

## Outputs

- Training batch set (80% of normalized or unnormalized data)
- Validation batch set (10% of normalized or unnormalized data)
- Test batch set (10% of normalized or unnormalized data)
- Batch metadata (peak counts per class per batch for comparison)

## How to apply

Instantiate an NN_handler object with your labeled Experiment object and fixed parameters (matrice_size=120, margin=1, min_scan_num=5). Generate two parallel batch sets by calling nn_handler.create_batches(validation_split=0.1, normalise_class=False) and nn_handler.create_batches(validation_split=0.1, normalise_class=True). The first call preserves the original class distribution across 80% training, 10% test, and 10% validation splits; the second rebalances all three batches so each class contributes exactly N peaks, where N equals the smallest class count in the dataset. Compare the resulting peak count distributions per class per batch to assess which normalization strategy better suits your downstream model training and evaluation goals. When normalise_class=True is selected, verify that the constraint 'number of peaks for each class will be equal to the smallest class' is satisfied in all batches.

## Related tools

- **NeatMS** (Provides NN_handler class and create_batches() method to partition and optionally balance labeled LC-MS peak data into training, validation, and test cohorts) — https://github.com/bihealth/NeatMS
- **Python** (Language for scripting batch creation and comparison workflow)
- **Keras** (Neural network training framework that consumes the generated batches for model training)

## Examples

```
nn_handler.create_batches(validation_split=0.1, normalise_class=False)
nn_handler.create_batches(validation_split=0.1, normalise_class=True)
```

## Evaluation signals

- Verify that unnormalized batches reflect the original class distribution from the full labeled dataset (calculated as percentage of peaks per class in training, validation, and test sets)
- Confirm that normalized batches satisfy the invariant: all classes have identical peak counts within each batch, and that count equals min(class_counts) from the full dataset
- Compare total peak counts across both batch sets; unnormalized should preserve all peaks, while normalized should discard peaks from larger classes such that all classes are downsampled to the smallest class size
- Inspect batch metadata to verify validation_split=0.1 is honored (test + validation = 20% of total, validation = 10% of original data) in both normalization modes
- Run a preliminary model training step with both batch sets and track convergence speed and final validation accuracy to empirically assess which normalization choice improves generalization on held-out peaks

## Limitations

- Normalizing class distributions discards peaks from overrepresented classes, potentially losing information about natural class prevalence in real LC-MS data
- The method assumes you have labeled at least enough peaks to form meaningful batches after normalization; if the smallest class is very small, normalized batches may be too sparse for effective training
- Class normalization is applied uniformly across all three batches (training, validation, test); there is no option to normalize only training while preserving test/validation class distributions
- The choice between normalization modes must be made before training; switching strategies mid-training requires complete batch regeneration and model retraining

## Evidence

- [other] When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class equal to the smallest class count: "When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class"
- [methods] The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest: "The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest"
- [methods] NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object and call the batch creation method.: "NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object and call the batch creation method"
- [methods] For optimal training, we recommend to use a representative subset of the dataset that your are planning to analyse, or as similar as possible.: "For optimal training, we recommend to use a representative subset of the dataset that your are planning to analyse, or as similar as possible"
- [methods] When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class).: "When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class)"
