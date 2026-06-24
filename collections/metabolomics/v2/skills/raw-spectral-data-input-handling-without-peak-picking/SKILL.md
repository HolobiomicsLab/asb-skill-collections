---
name: raw-spectral-data-input-handling-without-peak-picking
description: Use when when you have raw mass spectrometry imaging data (full m/z profiles
  with intensity arrays) and want to classify spatial regions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - numpy
  - h5py
  - Keras
  - TensorFlow
  - NumPy
  - massNet
  techniques:
  - MS-imaging
  license_tier: restricted
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

# raw-spectral-data-input-handling-without-peak-picking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Skill to accept and preprocess raw mass spectrometry imaging (MSI) data directly into a deep learning classifier without performing prior peak picking or feature extraction. This avoids information loss from peak detection thresholding and enables probabilistic end-to-end learning on full spectral tensors.

## When to use

When you have raw mass spectrometry imaging data (full m/z profiles with intensity arrays) and want to classify spatial regions (e.g., tumor vs. non-tumor tissue) directly using a convolutional neural network, without manual or automated peak picking that would discard spectral intensity detail or introduce detection bias.

## When NOT to use

- Input data is already a reduced feature matrix or peak list (peaks have already been extracted and picked).
- Analysis goal is to identify specific m/z peaks or perform targeted metabolite quantitation at known m/z values.
- Spectral resolution or m/z range is incompatible with the model input layer dimensionality.

## Inputs

- raw mass spectrometry imaging data tensor (spatial dimensions × m/z bins × intensity values)
- HDF5 or NumPy array format containing full spectral profiles
- spatial class labels (e.g., tumor/non-tumor annotations per pixel or region)

## Outputs

- compiled Keras neural network model accepting raw spectral tensors
- probabilistic classification output (per-class probability distribution for each spatial location)
- serialized model architecture (HDF5 or JSON format) ready for training and evaluation

## How to apply

Load raw MSI data into tensor format (e.g., HDF5 via h5py) with dimensions [spatial_x, spatial_y, m/z_bins] representing the full spectral profile at each pixel. Pass this raw tensor directly to the Keras input layer without preprocessing steps like peak normalization, feature selection, or dimensionality reduction. The network learns to identify discriminative m/z patterns automatically during training. Compile the model with a loss function suitable for multi-class probability output (e.g., categorical cross-entropy) and train on raw spectral tensors paired with spatial class labels (tumor/non-tumor). Verify that the input layer shape matches the raw data dimensions and that the model outputs probability distributions summing to 1.0 across classes.

## Related tools

- **Keras** (defines and compiles the convolutional neural network model architecture accepting raw spectral tensors as input)
- **TensorFlow** (backend engine for Keras model compilation and automatic differentiation during training on raw MSI tensors)
- **h5py** (loads and serializes raw mass spectrometry imaging data in HDF5 format to/from Keras-compatible tensor format)
- **NumPy** (constructs and manipulates raw spectral data arrays with correct shape [spatial_x, spatial_y, m/z_bins])
- **massNet** (reference implementation demonstrating end-to-end raw MSI data input and probabilistic tumor classification) — github.com/wabdelmoula/massNet

## Evaluation signals

- Raw spectral tensor input shape matches model input layer dimensionality exactly (no shape mismatch errors).
- Model output layer produces probability distributions: output values in [0, 1] and per-sample class probabilities sum to 1.0 ± 1e-6.
- Model accepts and processes batches of raw MSI data without triggering peak-picking or feature extraction preprocessing steps.
- Serialized model (HDF5/JSON) can be loaded and passes raw test spectral tensors through forward pass without errors.
- Training loss converges and validation accuracy on held-out raw MSI regions matches expected tumor/non-tumor classification performance.

## Limitations

- Raw spectral tensor dimensionality must match the fixed input layer size; variable-length or heterogeneous m/z ranges require resampling or padding.
- No explicit peak picking means the model must learn spectral patterns from raw intensity data; performance depends on network depth and training data size.
- The approach omits interpretability: which specific m/z values or peak patterns drive classification decisions is not directly extracted from the raw input handling.
- Memory footprint is larger than peak-picked features because full spectral resolution is retained; large-scale MSI datasets may require batching or downsampling.

## Evidence

- [readme] Deep learning based implementation for probabilistic classification of mass spectrometry imaging (MSI) data without prior peak picking.: "Deep Learning based implementation for probabilistic classification of mass spectrometry imaging (MSI) data without prior peak picking."
- [intro] Input layer accepting raw mass spectrometry imaging data without preprocessing.: "input layer accepting raw mass spectrometry imaging data (no pre-processing peaks required)"
- [intro] Model accepts MSI data tensors and outputs probability distributions.: "Verify the model can accept MSI data tensors and output probability distributions across tumor/non-tumor classes."
- [intro] Serialization of compiled model to HDF5 or JSON format.: "Save the compiled model architecture to a serialized format (HDF5 or JSON) for downstream training and evaluation."
