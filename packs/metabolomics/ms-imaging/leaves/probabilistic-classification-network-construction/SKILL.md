---
name: probabilistic-classification-network-construction
description: Use when when you have raw mass spectrometry imaging data tensors and need to build a trainable deep-learning classifier that outputs class probabilities (tumor vs. non-tumor) without preprocessing or manual peak detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3383
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - numpy
  - h5py
  - Keras
  - TensorFlow
  - Python
  - massNet
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1093/bioinformatics/btac032/6510930
  title: massNet
evidence_spans:
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

# probabilistic-classification-network-construction

## Summary

Construct and compile a Keras deep-learning network architecture for probabilistic classification of mass spectrometry imaging (MSI) data without requiring prior peak picking. This skill encapsulates the design, layer construction, and serialization of a neural network model that directly accepts raw MSI tensors and outputs probability distributions across tumor/non-tumor classes.

## When to use

When you have raw mass spectrometry imaging data tensors and need to build a trainable deep-learning classifier that outputs class probabilities (tumor vs. non-tumor) without preprocessing or manual peak detection. Apply this skill when you are setting up the model architecture before training or when reconstructing a published probabilistic MSI classifier for reproducibility or transfer learning.

## When NOT to use

- Input data is already a pre-computed feature table or peak-picked matrix — use feature-based classifiers instead
- You only need inference on an already-trained, pre-compiled model — load and use the saved weights directly
- Your MSI data requires specialized preprocessing (e.g., m/z recalibration, spatial smoothing) before classification — perform preprocessing first, then apply this skill

## Inputs

- Raw mass spectrometry imaging (MSI) data as 3D tensor (spatial_x, spatial_y, mass_channels)
- Model architecture specification (layer types, sizes, activation functions)
- Hyperparameter configuration (loss function, optimizer, learning rate)

## Outputs

- Compiled Keras model with trainable weights initialized
- Serialized model architecture (HDF5 or JSON)
- Model capable of outputting probability distributions across tumor/non-tumor classes

## How to apply

Define a Keras model using TensorFlow 1.8.0 backend that accepts raw MSI data tensors as input (no pre-processing peaks required). Construct the network using convolutional and dense layers according to the published massNet architecture. Compile the model with an appropriate loss function and optimizer compatible with TensorFlow 1.8.0 (e.g., categorical crossentropy for multi-class probability output). Verify that the model accepts MSI data tensors of the correct shape and outputs a probability distribution (softmax activations) across tumor/non-tumor classes. Finally, serialize the compiled model architecture to HDF5 or JSON format for downstream training and evaluation. The rationale is to ensure the network is correctly initialized, layers are properly connected, and the output layer produces calibrated probability estimates suitable for clinical or research-grade tumor delineation tasks.

## Related tools

- **Keras** (Neural network API for defining and compiling the probabilistic classification model architecture with layers and loss functions)
- **TensorFlow** (Backend computation engine (version 1.8.0) providing low-level tensor operations and optimization for model compilation)
- **Python** (Programming environment (3.6.12) for executing model construction, compilation, and serialization scripts)
- **h5py** (Serialization library for saving compiled model architecture and weights to HDF5 format)
- **numpy** (Tensor manipulation and data structure handling for MSI input arrays)
- **massNet** (Reference implementation and published architecture for probabilistic MSI classification) — github.com/wabdelmoula/massNet

## Evaluation signals

- Model input layer shape matches raw MSI tensor dimensions (no peak-picking artifacts); verify via model.input_shape
- Output layer uses softmax activation and produces probability distributions that sum to 1.0 across tumor/non-tumor classes
- Compiled model runs forward pass without shape mismatches or NaN outputs on sample MSI data
- Serialized model file (HDF5 or JSON) can be loaded and reconstructed without errors; verify architecture integrity by comparing layer counts and parameter counts
- Model accepts raw MSI tensors directly without requiring external feature extraction or peak detection preprocessing

## Limitations

- Keras 2.2.0 with TensorFlow 1.8.0 backend are legacy versions; modern deep-learning environments may have compatibility issues or performance regressions
- Model architecture does not include data augmentation, regularization (dropout, L2), or batch normalization details — these must be added separately if overfitting is observed
- No built-in validation or early stopping; compilation only ensures mathematical correctness, not generalization or clinical utility
- Raw MSI input requires careful memory management for high-resolution or large field-of-view datasets; tensor shape and batch size must be tuned to available GPU/CPU memory

## Evidence

- [other] Define the massNet model architecture using Keras 2.2.0 with input layer accepting raw mass spectrometry imaging data (no pre-processing peaks required).: "Define the massNet model architecture using Keras 2.2.0 with input layer accepting raw mass spectrometry imaging data (no pre-processing peaks required)."
- [other] Construct convolutional and dense layers as specified in the repository architecture for probabilistic classification.: "Construct convolutional and dense layers as specified in the repository architecture for probabilistic classification."
- [other] Compile the model with appropriate loss function and optimizer compatible with TensorFlow 1.8.0.: "Compile the model with appropriate loss function and optimizer compatible with TensorFlow 1.8.0."
- [other] Verify the model can accept MSI data tensors and output probability distributions across tumor/non-tumor classes.: "Verify the model can accept MSI data tensors and output probability distributions across tumor/non-tumor classes."
- [other] Save the compiled model architecture to a serialized format (HDF5 or JSON) for downstream training and evaluation.: "Save the compiled model architecture to a serialized format (HDF5 or JSON) for downstream training and evaluation."
- [readme] Deep learning based implementation for probabilistic classification of mass spectrometry imaging (MSI) data without prior peak picking.: "Deep learning based implementation for probabilistic classification of mass spectrometry imaging (MSI) data without prior peak picking."
- [readme] Keras (2.2.0) with a Tensorflow(1.8.0) backend. Packages: numpy(1.15.4), sklearn(0.23.2), scipy(1.0.0), seaborn (0.9.0), Pandas(1.1.1.), and h5py(2.7.1): "Keras (2.2.0) with a Tensorflow(1.8.0) backend. Packages: numpy(1.15.4), sklearn(0.23.2), scipy(1.0.0), seaborn (0.9.0), Pandas(1.1.1.), and h5py(2.7.1)"
