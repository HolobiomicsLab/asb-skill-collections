---
name: model-serving-artifact-preparation
description: Use when you have trained Keras models that need to be deployed in a TensorFlow Serving container, and the serving infrastructure requires HDF5 TensorFlow 2.0+ format with specific input/output layer naming conventions (e.g., 'input_2048', 'input_4096', 'output').
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - TensorFlow
  - Keras
  - TensorFlow Serving
derived_from:
- doi: 10.1021/jacs.9b13786
  title: CSCS / deep CNN natural-product annotation
evidence_spans:
- Make sure you have python installed
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

# model-serving-artifact-preparation

## Summary

Convert trained Keras models to HDF5 TensorFlow 2.0+ format and validate layer naming conventions to prepare models for deployment via TensorFlow Serving. This skill ensures compatibility with containerized inference pipelines and remote model metadata inspection.

## When to use

You have trained Keras models that need to be deployed in a TensorFlow Serving container, and the serving infrastructure requires HDF5 TensorFlow 2.0+ format with specific input/output layer naming conventions (e.g., 'input_2048', 'input_4096', 'output').

## When NOT to use

- Your models are already in HDF5 TensorFlow 2.0+ format with correct layer naming.
- You are using TensorFlow Serving version < 2.0 or a different model server that does not require HDF5 format.
- Input models use layer names that cannot be changed or are incompatible with the required 'input_2048', 'input_4096', 'output' convention.

## Inputs

- Keras model files (in native Keras format)
- TensorFlow 2.3.0 environment
- Python installation

## Outputs

- HDF5 TensorFlow 2.0+ model files (.h5)
- Model metadata (layer names and structure)
- Validation report confirming layer naming conventions

## How to apply

First, ensure Python and TensorFlow 2.3.0 are installed in your environment. Acquire the pre-trained models by navigating to the models directory and executing the get_models.sh download script. Next, use Keras model conversion utilities (available in TensorFlow 2.3.0) to convert each downloaded Keras model to HDF5 TensorFlow 2.0+ format. Critically, validate that the converted model's input layers are named exactly 'input_2048' and 'input_4096', and the output layer is named 'output'—these names are required for TensorFlow Serving compatibility and must match the inference API's expectations. Finally, verify the output files are valid HDF5 models by loading them and inspecting their layer structure before deploying to the containerized server.

## Related tools

- **TensorFlow** (Model conversion and validation (version 2.3.0 required for Keras-to-HDF5 conversion))
- **Keras** (Source model format and conversion utilities)
- **Python** (Runtime environment for executing conversion scripts)
- **TensorFlow Serving** (Target deployment infrastructure requiring HDF5 format and specific layer naming)

## Examples

```
cd Classifier/models_folder/models && sh ./get_models.sh && python -c "import tensorflow as tf; model = tf.keras.models.load_model('classifier.h5'); print([layer.name for layer in model.layers])"
```

## Evaluation signals

- Converted output file is readable as valid HDF5 format and loads without I/O errors in TensorFlow.
- Input layer names exactly match 'input_2048' and 'input_4096' when inspected via model.layers or tf.saved_model.inspect_signature().
- Output layer name is exactly 'output' and produces expected tensor shape for downstream inference.
- Model metadata endpoint (/model/metadata) returns correct layer names without requiring code changes.
- Model successfully accepts SMILES string input through the /classify?smiles=<> API endpoint after deployment.

## Limitations

- Conversion is specific to TensorFlow 2.3.0; other TensorFlow versions may produce incompatible HDF5 formats.
- Layer names must be exactly 'input_2048', 'input_4096', and 'output'—any deviation requires code modifications in the serving infrastructure.
- Keras models with custom layers or non-standard architectures may not convert cleanly to HDF5 format.
- Model conversion does not optimize for inference latency; converted models retain original architecture and computational complexity.

## Evidence

- [readme] Model conversion requirement: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [readme] Required input layer naming: "Input layers' names should be "input_2048" and "input_4096""
- [readme] Required output layer naming: "Output layer's name should be "output""
- [readme] Model acquisition workflow: "cd Classifier/models_folder/models
sh ./get_models.sh"
- [readme] TensorFlow Serving compatibility rationale: "If the model input names change, then we need to change it in the code"
