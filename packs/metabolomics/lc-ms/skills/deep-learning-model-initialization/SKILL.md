---
name: deep-learning-model-initialization
description: Use when you have downloaded the LC-MS spectral peak dataset (DOI 10.25345/C5FD2F) and need to train a DNN model from scratch rather than using a pre-trained checkpoint.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3172
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

# deep-learning-model-initialization

## Summary

Initialize and train a deep neural network classifier from scratch on LC-MS spectral peak data using the EDML_deep_learning2.py script. This skill prepares the model architecture and parameters for binary classification of real versus noise peaks in liquid chromatography–mass spectrometry data.

## When to use

Use this skill when you have downloaded the LC-MS spectral peak dataset (DOI 10.25345/C5FD2F) and need to train a DNN model from scratch rather than using a pre-trained checkpoint. Apply it at the start of a modeling pipeline when you want to establish baseline performance or retrain on a specific subset of LC-MS peaks.

## When NOT to use

- Input dataset has not been downloaded from the official repository; use download utilities first.
- You already have a trained model checkpoint and only need inference; use model loading instead.
- Peak data is in a non-standard format not compatible with EDML_deep_learning2.py's data loaders; preprocess or convert first.

## Inputs

- LC-MS spectral peak dataset (from DOI 10.25345/C5FD2F)
- EDML_deep_learning2.py script
- Data loading configuration (if required by script)

## Outputs

- Trained DNN model weights
- Model architecture definition
- Model artifact file (saved checkpoint)

## How to apply

First, download the LC-MS datasets from the deposited repository (DOI 10.25345/C5FD2F) and load them into memory using the data loading utilities provided in EDML_deep_learning2.py. Initialize the deep neural network model by executing EDML_deep_learning2.py, which sets up the architecture and trains on the peak classification task. Monitor training progress to ensure convergence on the spectral peak classification objective. Upon completion, save the trained model weights and architecture to a model artifact file for subsequent inference or transfer learning tasks.

## Related tools

- **EDML_deep_learning2.py** (Main training script that initializes the DNN architecture, loads LC-MS peak data, and executes the training loop for spectral peak classification) — https://github.com/JainLab/Manuscript-DNNs-for-Classification-of-LCMS-Peaks
- **TensorFlow** (Deep learning framework underlying model initialization and gradient-based training)
- **Keras** (High-level API used to define and compile the neural network model architecture)

## Examples

```
python EDML_deep_learning2.py --dataset_path /path/to/10.25345/C5FD2F --output_model model_checkpoint.h5
```

## Evaluation signals

- Model artifact file is created and contains both weights and architecture metadata.
- Training loss decreases monotonically or shows expected convergence behavior over epochs.
- Model can successfully generate predictions on held-out spectral peak validation data.
- Saved model can be reloaded and produces identical predictions on the same input peaks.
- Memory consumption and training time align with dataset size and hardware specifications (GPU/CPU).

## Limitations

- Training requires the full LC-MS peak dataset to be downloaded; network connectivity and storage space are prerequisites.
- Hyperparameters and network architecture are fixed within EDML_deep_learning2.py; custom modifications require script editing.
- No guidance provided in README or article on resuming interrupted training or checkpoint recovery.
- Reproducibility depends on fixed random seeds; results may vary across hardware platforms or library versions.

## Evidence

- [other] Training the neural network model from scratch requires two sequential steps: first downloading the LC-MS datasets from the specified repository, then executing the EDML_deep_learning2.py script on those datasets.: "first downloading the LC-MS datasets from the specified repository, then executing the EDML_deep_learning2.py script on those datasets"
- [readme] Workflow step from README describing the initialization procedure.: "first download the datasets from https://doi.org/doi:10.25345/C5FD2F. Then use the script EDML_deep_learning2.py"
- [other] Detailed workflow describing data loading and model saving.: "Load the LC-MS Peaks Dataset (from DOI 10.25345/C5FD2F) into memory using the data loading utilities provided in EDML_deep_learning2.py. 2. Execute EDML_deep_learning2.py to initialize and train the"
- [other] Output specification from the task card.: "Save the trained model weights and architecture to a model artifact file upon completion of training"
