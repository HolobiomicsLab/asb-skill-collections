---
name: keras-model-format-conversion
description: Use when you have downloaded Keras-format pre-trained models (e.g., via
  get_models.sh) and need to deploy them locally via TensorFlow Serving within a Dockerized
  classification API.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3474
  tools:
  - Python
  - Keras
  - TensorFlow
  - TensorFlow Serving
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jacs.9b13786
  title: CSCS / deep CNN natural-product annotation
evidence_spans:
- Make sure you have python installed
- convert the keras models into HDF5 TF2 models
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cscs_deep_cnn_natural_product_annotation_cq
    doi: 10.1021/jacs.9b13786
    title: CSCS / deep CNN natural-product annotation
  dedup_kept_from: coll_cscs_deep_cnn_natural_product_annotation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jacs.9b13786
  all_source_dois:
  - 10.1021/jacs.9b13786
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# keras-model-format-conversion

## Summary

Convert Keras deep learning models to HDF5 TensorFlow 2.0+ format for compatibility with TensorFlow Serving and containerized deployment pipelines. This skill ensures pre-trained neural network models meet layer naming and format requirements for production inference servers.

## When to use

You have downloaded Keras-format pre-trained models (e.g., via get_models.sh) and need to deploy them locally via TensorFlow Serving within a Dockerized classification API. The conversion is required when input and output layer names must conform to a specific naming scheme ('input_2048', 'input_4096', 'output') and the deployment target is TensorFlow Serving behind nginx.

## When NOT to use

- Models are already in HDF5 TensorFlow 2.0+ format and have been validated for correct layer naming.
- You are deploying models directly via a framework that natively consumes Keras SavedModel or frozen graph formats without requiring HDF5 conversion.
- Layer naming requirements differ from the standard ('input_2048', 'input_4096', 'output') and model renaming is not feasible in your pipeline.

## Inputs

- Downloaded Keras model files (pre-trained NP Classifier models from get_models.sh)
- Python 3.x runtime
- TensorFlow 2.3.0 library

## Outputs

- HDF5-format TensorFlow 2.0+ models (.h5 or .hdf5 files)
- Converted models with validated layer names for TensorFlow Serving

## How to apply

Ensure Python and TensorFlow 2.3.0 are installed in your environment. Load the downloaded Keras model files using TensorFlow/Keras model loading utilities and convert them to HDF5 format using Keras model conversion functions. After conversion, validate that input layers are named 'input_2048' and 'input_4096', and the output layer is named 'output'—these names are critical for TensorFlow Serving compatibility and downstream API routing. Verify the converted files are written in HDF5 format (.h5 or .hdf5 extension) before proceeding to Docker network and deployment steps.

## Related tools

- **TensorFlow** (Deep learning framework for loading and converting Keras models to HDF5 format)
- **Keras** (High-level API for building and loading neural network models prior to format conversion)
- **Python** (Runtime environment for executing conversion scripts and TensorFlow utilities)
- **TensorFlow Serving** (Production inference server that consumes converted HDF5 models for classification requests)

## Evaluation signals

- Output files exist in HDF5 format (.h5 or .hdf5) and are readable by TensorFlow 2.3.0+
- Converted model metadata (retrieved via /model/metadata endpoint in TensorFlow Serving) confirms input layer names are 'input_2048' and 'input_4096'
- Converted model metadata confirms output layer name is 'output'
- Model can be successfully loaded and queried without errors in a TensorFlow Serving container
- Input tensor shapes and data types match the original Keras model and are compatible with downstream classification API (/classify?smiles=<> endpoint)

## Limitations

- Conversion requires TensorFlow version 2.3.0 specifically; newer or older versions may produce incompatible outputs.
- Layer names are fixed at conversion time; if downstream requirements change, re-conversion is necessary.
- No changelog is documented, making it difficult to track breaking changes between model versions or conversion tool updates.

## Evidence

- [readme] tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [readme] Input and output layer names must match specific naming scheme for TensorFlow Serving: "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [readme] Conversion is prerequisite for Dockerized deployment via TensorFlow Serving: "We pass through tensorflow serving at this url"
- [other] Models must be in HDF5 TensorFlow 2.0+ format after conversion: "Convert the downloaded Keras models to HDF5 TensorFlow 2.0+ format using Keras model conversion utilities, verifying that input layers are named 'input_2048' and 'input_4096', and output layer is"
