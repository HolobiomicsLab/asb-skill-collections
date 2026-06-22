---
name: lcms-spectral-peak-classification
description: Use when you have raw LC-MS spectral peak data (in the format provided by DOI 10.25345/C5FD2F) and need to build a classifier that can distinguish valid peaks from false positives or background noise without manual feature engineering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - TensorFlow
  - Keras
  - EDML_deep_learning2.py
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.9b02983
  title: DNN peak classifier
- doi: 10.25345/C5FD2F
  title: ''
evidence_spans:
- Deep Neural Networks for Classification of LC-MS Spectral Peaks
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dnn_peak_classifier_cq
    doi: 10.1021/acs.analchem.9b02983
    title: DNN peak classifier
  dedup_kept_from: coll_dnn_peak_classifier_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b02983
  all_source_dois:
  - 10.1021/acs.analchem.9b02983
  - 10.25345/C5FD2F
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lcms-spectral-peak-classification

## Summary

Train a deep neural network from scratch to classify LC-MS spectral peaks using TensorFlow/Keras on a curated peak dataset. This skill enables automated discrimination of true spectral signals from noise or artifacts in liquid chromatography–mass spectrometry data.

## When to use

You have raw LC-MS spectral peak data (in the format provided by DOI 10.25345/C5FD2F) and need to build a classifier that can distinguish valid peaks from false positives or background noise without manual feature engineering. Use this when you want to leverage deep learning to learn peak morphology and intensity patterns directly from labeled examples.

## When NOT to use

- You already have a pre-trained peak classifier model and only need inference.
- Your LC-MS data are in a different format or from a substantially different instrument/method (model may not generalize).
- You have fewer than ~100 labeled peak examples; insufficient data will lead to severe overfitting.

## Inputs

- LC-MS spectral peak dataset (DOI 10.25345/C5FD2F format)
- EDML_deep_learning2.py script with data loaders
- TensorFlow/Keras configuration or hyperparameter specification

## Outputs

- Trained deep neural network model weights and architecture
- Model artifact file (e.g., .h5, .pb, or checkpoint directory)
- Training/validation loss and accuracy metrics

## How to apply

First, download the LC-MS datasets from the official repository (DOI 10.25345/C5FD2F) and load them into memory using the data loading utilities embedded in EDML_deep_learning2.py. Execute the EDML_deep_learning2.py script, which initializes a deep neural network architecture (built in TensorFlow/Keras) and trains it end-to-end on the peak classification task. The script handles data batching, gradient descent optimization, and convergence. Upon completion, save the trained model weights and architecture to a model artifact file (e.g., .h5 or .pb format). Validation performance on held-out peak data confirms whether the model has learned discriminative features.

## Related tools

- **TensorFlow** (Deep learning framework for building and training the neural network architecture)
- **Keras** (High-level API (integrated with TensorFlow) for model definition, training loop, and checkpoint management)
- **EDML_deep_learning2.py** (Main training script that loads LC-MS peak data, initializes the DNN, executes training, and saves model artifacts) — https://github.com/JainLab/Manuscript-DNNs-for-Classification-of-LCMS-Peaks

## Examples

```
python EDML_deep_learning2.py --data_path /path/to/lcms_peaks_doi_10.25345_C5FD2F --epochs 100 --batch_size 32 --output_model ./trained_peak_classifier.h5
```

## Evaluation signals

- Training loss decreases monotonically and plateaus after a reasonable number of epochs (no divergence).
- Validation accuracy on held-out peak examples is substantially higher than random guessing (>60% for binary classification, >50% for multi-class).
- Model artifact file is created with non-zero size and can be loaded and used for inference without errors.
- Confusion matrix on test peaks shows low false-positive and false-negative rates relative to ground truth labels.
- Model generalizes across different LC-MS runs or peak intensity ranges without dramatic accuracy drop.

## Limitations

- Model performance depends critically on the quality and representativeness of the training dataset; peaks from novel instruments or methods may be misclassified.
- Deep learning requires substantial computational resources (GPU recommended) and can be slow on CPU-only systems.
- The trained model is a black box; feature importance and decision logic are not directly interpretable.
- No changelog or detailed discussion of failure modes is available in the published record.

## Evidence

- [readme] For training the neural net model from scratch using the data sets that we used, first download the datasets from https://doi.org/doi:10.25345/C5FD2F. Then use the script EDML_deep_learning2.py.: "For training the neural net model from scratch using the data sets that we used, first download the datasets from https://doi.org/doi:10.25345/C5FD2F. Then use the script EDML_deep_learning2.py."
- [other] Training the neural network model from scratch requires two sequential steps: first downloading the LC-MS datasets from the specified repository, then executing the EDML_deep_learning2.py script on those datasets.: "Training the neural network model from scratch requires two sequential steps: first downloading the LC-MS datasets from the specified repository, then executing the EDML_deep_learning2.py script on"
- [other] Load the LC-MS Peaks Dataset (from DOI 10.25345/C5FD2F) into memory using the data loading utilities provided in EDML_deep_learning2.py.: "Load the LC-MS Peaks Dataset (from DOI 10.25345/C5FD2F) into memory using the data loading utilities provided in EDML_deep_learning2.py."
- [other] Execute EDML_deep_learning2.py to initialize and train the deep neural network model from scratch on the peak classification task.: "Execute EDML_deep_learning2.py to initialize and train the deep neural network model from scratch on the peak classification task."
- [other] Save the trained model weights and architecture to a model artifact file upon completion of training.: "Save the trained model weights and architecture to a model artifact file upon completion of training."
- [intro] Deep neural networks can be applied to classification of LC-MS spectral peaks: "Deep neural networks can be applied to classification of LC-MS spectral peaks"
