---
name: keras-tensorflow-model-compilation
description: Use when you have defined a Keras model architecture (convolutional and
  dense layers) accepting raw mass spectrometry imaging data tensors and need to prepare
  it for training on tumor/non-tumor probabilistic classification without prior peak
  picking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0092
  tools:
  - Keras
  - TensorFlow
  - numpy
  - h5py
  - Python
  techniques:
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1093/bioinformatics/btac032/6510930
  title: massNet
evidence_spans:
- Keras (2.2.0)
- Tensorflow(1.8.0)
- 2- Keras (2.2.0) with a Tensorflow(1.8.0) backend.
- numpy(1.15.4)
- 'Packages: numpy(1.15.4)'
- h5py(2.7.1)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massnet_cq
    doi: 10.1093/bioinformatics/btac032/6510930
    title: massNet
  dedup_kept_from: coll_massnet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac032/6510930
  all_source_dois:
  - 10.1093/bioinformatics/btac032/6510930
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# keras-tensorflow-model-compilation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compile a Keras neural network model with TensorFlow backend, specifying loss function and optimizer compatible with the target framework version, to prepare the model for training on mass spectrometry imaging data. This skill ensures the model is properly configured before accepting raw MSI tensors and outputting probability distributions.

## When to use

You have defined a Keras model architecture (convolutional and dense layers) accepting raw mass spectrometry imaging data tensors and need to prepare it for training on tumor/non-tumor probabilistic classification without prior peak picking. The model must be compiled before training or evaluation can begin.

## When NOT to use

- Model architecture has not yet been defined (define layers first using Keras functional or sequential API)
- Input data has already been preprocessed into peak features (massNet accepts raw MSI data, not pre-picked peaks)
- You are using a different deep learning framework (e.g., PyTorch) — this skill is specific to Keras with TensorFlow backend

## Inputs

- Keras Sequential or Functional model with defined convolutional and dense layers
- Loss function specification (string or callable compatible with Keras 2.2.0)
- Optimizer specification (string or instance compatible with TensorFlow 1.8.0)
- Model input shape matching raw mass spectrometry imaging data tensor dimensions

## Outputs

- Compiled Keras model ready for training
- Serialized model architecture (HDF5 or JSON format)
- Model summary confirming layer structure and parameter counts

## How to apply

After defining the Keras model layers using Keras 2.2.0 with TensorFlow 1.8.0 backend, select a loss function appropriate for multi-class probabilistic classification (e.g., categorical cross-entropy for tumor/non-tumor classes) and choose an optimizer compatible with TensorFlow 1.8.0. Call the model.compile() method with the selected loss and optimizer. Verify the compiled model can accept MSI data tensors (raw spectra without peak picking) as input. Serialize the compiled model architecture to HDF5 or JSON format for reproducible downstream training and evaluation workflows.

## Related tools

- **Keras** (Model definition and compilation framework)
- **TensorFlow** (Computational backend for Keras model execution)
- **Python** (Programming language for model development and execution)
- **h5py** (Serialization of compiled model to HDF5 format)

## Evaluation signals

- model.compile() executes without errors and loss function is compatible with the number of target classes (tumor/non-tumor)
- model.summary() output confirms all layers are properly connected and total parameters are as expected
- Compiled model accepts a test batch of raw MSI data with correct input tensor shape and produces output probability distributions with shape matching number of classes
- Serialized model file (HDF5 or JSON) can be loaded and re-instantiated without loss of architecture information
- Model training step (one epoch) runs without shape mismatch or backend compatibility errors using TensorFlow 1.8.0

## Limitations

- Keras 2.2.0 and TensorFlow 1.8.0 are legacy versions; compilation syntax and optimizer availability differ from modern Keras/TensorFlow 2.x
- No explicit guidance in the article on loss function selection for imbalanced tumor/non-tumor classes or class weighting during compilation
- Compiled model performance depends critically on correct loss function choice; article does not detail hyperparameter tuning rationale

## Evidence

- [readme] We have implemented our machine learning model using the following software items: 1- Python(3.6.12) 2- Keras (2.2.0) with a Tensorflow(1.8.0) backend.: "Keras (2.2.0) with a Tensorflow(1.8.0) backend"
- [other] Compile the model with appropriate loss function and optimizer compatible with TensorFlow 1.8.0.: "Compile the model with appropriate loss function and optimizer compatible with TensorFlow 1.8.0"
- [other] Verify the model can accept MSI data tensors and output probability distributions across tumor/non-tumor classes.: "Verify the model can accept MSI data tensors and output probability distributions across tumor/non-tumor classes"
- [other] Save the compiled model architecture to a serialized format (HDF5 or JSON) for downstream training and evaluation.: "Save the compiled model architecture to a serialized format (HDF5 or JSON) for downstream training and evaluation"
- [other] Define the massNet model architecture using Keras 2.2.0 with input layer accepting raw mass spectrometry imaging data (no pre-processing peaks required).: "input layer accepting raw mass spectrometry imaging data (no pre-processing peaks required)"
