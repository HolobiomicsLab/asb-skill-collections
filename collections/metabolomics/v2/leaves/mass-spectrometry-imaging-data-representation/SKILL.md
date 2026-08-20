---
name: mass-spectrometry-imaging-data-representation
description: Use when you have raw mass spectrometry imaging data (2D or 3D spatial
  coordinates with full mass-to-charge spectra) and want to train a probabilistic
  deep learning classifier for tumor delineation or tissue classification.
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
  - scipy
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

# mass-spectrometry-imaging-data-representation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Represent raw mass spectrometry imaging (MSI) data as dense tensors suitable for direct input to deep learning classifiers without prior peak picking or feature extraction. This skill enables end-to-end learning on spatially resolved mass spectrometry data by preserving the full spectral and spatial dimensionality.

## When to use

You have raw mass spectrometry imaging data (2D or 3D spatial coordinates with full mass-to-charge spectra) and want to train a probabilistic deep learning classifier for tumor delineation or tissue classification. Use this skill when you want to avoid manual peak picking or when automated peak detection may lose diagnostic signal in the raw spectrum.

## When NOT to use

- Input MSI data is already peak-picked or reduced to a feature table (e.g., m/z intensity pairs only) — use direct feature input instead.
- Spatial resolution is extremely coarse (<<10 pixels per dimension) or temporal data dominates over spatial structure — consider alternative representations.
- Memory constraints prevent loading the full spectral dimension into memory — consider spectral binning or stratified sampling as a preprocessing step.

## Inputs

- raw mass spectrometry imaging data file (HDF5, NetCDF, or vendor MSI format)
- spatial coordinates (x, y, z pixel indices or continuous coordinates)
- full mass-to-charge spectrum per pixel (no prior peak picking)
- optional: spatial metadata (pixel size, mass calibration parameters)

## Outputs

- 4D tensor: [spatial_x, spatial_y, mass_channels, 1] or [spatial_x, spatial_y, spatial_z, mass_channels]
- serialized tensor in HDF5 format compatible with Keras input layer
- tensor shape and dtype specification for model input validation

## How to apply

Load raw MSI data (e.g., HDF5 or vendor format) and reshape it into a 4D tensor with dimensions [spatial_x, spatial_y, mass_channels, 1] or [spatial_x, spatial_y, spatial_z, mass_channels]. Normalize or standardize across the mass dimension to account for detector noise and intensity variations. Tile or pad the tensor to a fixed size matching the input layer specification of your Keras model (typically 64×64 or 128×128 spatial pixels and full mass range without binning). Use h5py or scipy.io to serialize the tensor in HDF5 format, preserving metadata (pixel size, mass calibration, spatial coordinates). Verify tensor dimensions match the model's input_shape before compilation. The rationale is that convolutional and dense layers can learn spatial and spectral patterns jointly from the raw data, enabling both feature discovery and probabilistic classification in a single differentiable pipeline.

## Related tools

- **h5py** (serialize and deserialize MSI tensors in HDF5 format for persistent storage and Keras model input)
- **numpy** (reshape, normalize, and pad raw MSI spectra into fixed-size tensors)
- **Keras** (define input layer accepting the 4D MSI tensor and compile model for end-to-end classification)
- **TensorFlow** (backend for Keras model execution and tensor operations during training)
- **scipy** (load vendor MSI file formats and normalize spectra across mass dimension)

## Examples

```
import h5py; import numpy as np; from keras.models import Sequential; raw_msi = h5py.File('msi_data.h5', 'r')['spectra']; tensor = np.reshape(raw_msi, (64, 64, -1, 1)); h5py.File('tensor_input.h5', 'w').create_dataset('input', data=tensor); model.predict(tensor.reshape(1, 64, 64, -1, 1))
```

## Evaluation signals

- Tensor shape matches model input_shape exactly; no shape mismatch errors on model.fit() or model.predict()
- Tensor dtype is float32 and values are normalized to a reasonable range (e.g., [0, 1] or z-scored) with no NaN or Inf values
- Spatial dimensions are contiguous and non-empty; mass channel dimension spans the full m/z range with no gaps or binning artifacts
- HDF5 serialization round-trip: tensor loaded from HDF5 file is byte-identical to in-memory tensor (verify via np.allclose after deserialization)
- Model can accept the tensor batch without out-of-memory errors and produces probability distributions across tumor/non-tumor classes with shape [batch_size, num_classes]

## Limitations

- No prior peak picking may retain instrumental noise and unrelated mass channels; preprocessing (e.g., median filtering or wavelet denoising) may improve downstream classification but is not enforced by this skill.
- Requires sufficient memory to load full spectral dimension into GPU/CPU; extremely large MSI datasets (>100 GB) may require streaming or mini-batch tensor generation.
- Spatial interpolation or resampling to fixed tensor size (e.g., 64×64 pixels) may lose high-resolution spatial detail if native MSI pixel count differs significantly.
- The skill assumes mass calibration is accurate; miscalibrated m/z values will cause spectral misalignment and degrade model performance.

## Evidence

- [readme] Deep learning based implementation for probabilistic classification of mass spectrometry imaging (MSI) data without prior peak picking.: "Deep Learning based implementation for probabilistic classification of mass spectrometry imaging (MSI) data without prior peak picking."
- [other] Define the massNet model architecture using Keras 2.2.0 with input layer accepting raw mass spectrometry imaging data (no pre-processing peaks required).: "Define the massNet model architecture using Keras 2.2.0 with input layer accepting raw mass spectrometry imaging data (no pre-processing peaks required)."
- [other] Verify the model can accept MSI data tensors and output probability distributions across tumor/non-tumor classes.: "Verify the model can accept MSI data tensors and output probability distributions across tumor/non-tumor classes."
- [other] Save the compiled model architecture to a serialized format (HDF5 or JSON) for downstream training and evaluation.: "Save the compiled model architecture to a serialized format (HDF5 or JSON) for downstream training and evaluation."
- [readme] Keras (2.2.0) with a Tensorflow(1.8.0) backend. Packages: numpy(1.15.4), sklearn(0.23.2), scipy(1.0.0), seaborn (0.9.0), Pandas(1.1.1.), and h5py(2.7.1): "Keras (2.2.0) with a Tensorflow(1.8.0) backend. Packages: numpy(1.15.4), sklearn(0.23.2), scipy(1.0.0), seaborn (0.9.0), Pandas(1.1.1.), and h5py(2.7.1)"
