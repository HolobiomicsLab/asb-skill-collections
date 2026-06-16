---
name: batch-preparation-class-imbalance-handling
description: Use when when you have raw mzML files and a feature table (CSV from mzMine or XCMS) with labeled peaks of unequal class sizes (e.g., fewer false positives than true positives) and plan to train a CNN classifier on the LCMS data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - NeatMS
  - Python
  - TensorFlow
  - Keras
  - scikit-learn
  - pandas
  - NumPy
  - Jupyter Notebook
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
- calling the training method (1000 by default). NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training
- from keras.optimizers import SGD, Adam
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neatms
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  dedup_kept_from: coll_neatms
schema_version: 0.2.0
---

# batch-preparation-class-imbalance-handling

## Summary

Prepare training, validation, and test batches from LCMS peak data while addressing class imbalance through normalization. This skill ensures balanced representation of true and false positive peaks during neural network training to prevent bias toward the majority class.

## When to use

When you have raw mzML files and a feature table (CSV from mzMine or XCMS) with labeled peaks of unequal class sizes (e.g., fewer false positives than true positives) and plan to train a CNN classifier on the LCMS data. Use this skill before model training when your smallest class has <500 peaks, or when you observe the model learning spurious correlations favoring the majority class.

## When NOT to use

- Your training dataset already contains ≥500 peaks per class and classes are approximately balanced; normalization may discard useful data.
- You are performing transfer learning with a pre-trained model; rebalancing may conflict with the model's learned feature distributions.
- Input data is already in batched or tensor format; re-batching introduces data leakage risks.

## Inputs

- raw mzML files (LCMS data)
- feature table in CSV format (mzMine or XCMS output)
- labeled peak annotations with class assignments (true positive or false positive)

## Outputs

- training batch (80% of normalized data)
- validation batch (10% of normalized data)
- test batch (10% of normalized data)
- batch metadata including peak counts per class

## How to apply

Load raw mzML files and the feature table into a NeatMS Experiment object, specifying the input type (mzmine or xcms). Create a Neural Network Handler with parameters matrice_size=120, margin=1, min_scan_num=5 to filter out low-quality peaks. Call create_batches(validation_split=0.1, normalise_class=True) to generate training, test, and validation batches in 80:10:10 split; set normalise_class=True to equalize the number of peaks per class to match the smallest class size. This prevents the optimizer from learning to classify by class frequency rather than signal quality. Inspect the returned batch counts to confirm both classes are equally represented before proceeding to model training.

## Related tools

- **NeatMS** (Provides the Experiment object and Neural Network Handler for loading mzML/CSV data, defining batch creation parameters, and normalizing class representation) — https://github.com/bihealth/NeatMS
- **Python** (Host language for NeatMS API calls and batch inspection)
- **pandas** (Inspect and validate batch composition and class counts in returned DataFrames)
- **NumPy** (Compute batch statistics and verify class distribution across splits)

## Examples

```
from neatms import Experiment, NeuralNetworkHandler
exp = Experiment(path_to_raw_data='./data', path_to_feature_table='./features.csv', input_type='mzmine')
nn_handler = NeuralNetworkHandler(experiment=exp, matrice_size=120, margin=1, min_scan_num=5)
nn_handler.create_batches(validation_split=0.1, normalise_class=True)
```

## Evaluation signals

- Batch creation completes without errors and returns non-empty training, validation, and test DataFrames
- Class distribution in training batch is exactly 1:1 (equal count of true and false positive peaks) when normalise_class=True
- Total peaks in batches equals the normalized class count × 2 (both classes represented equally)
- Validation and test batches preserve the original class ratio (not normalized) for realistic performance estimation
- min_scan_num filtering removes peaks with <5 scans; verify by comparing feature table row count before/after batch creation

## Limitations

- normalise_class=True discards peaks from the majority class, reducing effective dataset size; not suitable for very small datasets (<1000 total peaks).
- The fixed 80:10:10 split ratio may not be optimal for all domains; the article does not discuss stratification by sample or temporal/batch effects.
- Normalization to the smallest class may amplify overfitting risk if the minority class is sparse (<100 peaks); the article recommends ≥500 peaks per class for full training.
- No automatic detection of mislabeled or ambiguous peaks; class imbalance handling assumes labels are correct.

## Evidence

- [other] Create a Neural Network Handler with default parameters (matrice_size=120, margin=1, min_scan_num=5) and call create_batches(validation_split=0.1, normalise_class=False) to generate training, test, and validation batches (80:10:10 split).: "Create a Neural Network Handler with default parameters (matrice_size=120, margin=1, min_scan_num=5) and call create_batches(validation_split=0.1, normalise_class=False) to generate training, test,"
- [methods] The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest: "The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest"
- [methods] `min_scan_number` argument will filter out all peaks that have a number of point (scan) lower than this value. `5` is the default value: "`min_scan_number` argument will filter out all peaks that have a number of point (scan) lower than this value. `5` is the default value"
- [methods] When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class).: "When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class)."
- [methods] NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object and call the batch creation method.: "NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object and call the batch creation method."
