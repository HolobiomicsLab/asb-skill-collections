---
name: tensorflow-model-conversion
description: Use when you have downloaded pre-trained Keras models and need to prepare
  them for deployment in a TensorFlow Serving container. Use this skill when you must
  convert legacy or freshly downloaded Keras model files to HDF5 format for compatibility
  with TensorFlow 2.3.0 serving infrastructure.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3379
  tools:
  - Python
  - TensorFlow 2.3.0
  - TensorFlow Serving
  - TensorFlow
  - Keras
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- Make sure you have python installed
- tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models
- 'We pass through tensorflow serving at this url: ```/model/metadata```'
- We pass through tensorflow serving at this url
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npclassifier_cq
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  dedup_kept_from: coll_npclassifier_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.1c00399
  all_source_dois:
  - 10.1021/acs.jnatprod.1c00399
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tensorflow-model-conversion

## Summary

Convert pre-trained Keras models to HDF5 TensorFlow 2 format for deployment with TensorFlow Serving. This skill enables reproducible model serialization and ensures compatibility with containerized inference pipelines.

## When to use

You have downloaded pre-trained Keras models and need to prepare them for deployment in a TensorFlow Serving container. Use this skill when you must convert legacy or freshly downloaded Keras model files to HDF5 format for compatibility with TensorFlow 2.3.0 serving infrastructure.

## When NOT to use

- Models are already in HDF5 TensorFlow 2 format and do not need re-serialization.
- Your deployment target does not use TensorFlow Serving (e.g., ONNX Runtime, TensorFlow Lite).
- Layer names in the source Keras model cannot be verified or modified to match 'input_2048', 'input_4096', and 'output' conventions.

## Inputs

- Keras model files (downloaded via get_models.sh script)
- Python environment with TensorFlow 2.3.0 installed

## Outputs

- HDF5 TensorFlow 2 model files (.h5 format)
- Model layer name validation report

## How to apply

First, verify that Python and TensorFlow version 2.3.0 are installed in your environment. Use TensorFlow 2.3.0's Keras API to load each downloaded Keras model and inspect its layer architecture to confirm that input layers are named 'input_2048' and 'input_4096' and the output layer is named 'output'. If layer names do not match these conventions, the downstream API endpoint will fail. Then use TensorFlow 2.3.0's save_model or h5 serialization utility to convert each Keras model to HDF5 TensorFlow 2 format, producing .h5 files. These converted files are then compatible with TensorFlow Serving deployment and can be mounted into Docker containers for the classification API.

## Related tools

- **Python** (Execution environment for model loading and serialization scripts)
- **TensorFlow 2.3.0** (Provides Keras API for model loading and h5 serialization utilities for HDF5 format conversion)
- **Keras** (High-level API within TensorFlow for loading and inspecting pre-trained model architecture and layer metadata)
- **TensorFlow Serving** (Deployment runtime that consumes converted HDF5 models for inference via the /model/metadata endpoint)

## Examples

```
python -c "import tensorflow as tf; model = tf.keras.models.load_model('downloaded_model.h5'); print('Inputs:', [inp.name for inp in model.inputs]); print('Outputs:', [out.name for out in model.outputs]); model.save('converted_model.h5')"
```

## Evaluation signals

- Verify that input layer names in the converted model exactly match 'input_2048' and 'input_4096' by querying model.input_names or inspecting via /model/metadata endpoint.
- Confirm that output layer name is 'output' by examining model.output_names in the converted .h5 file.
- Check that the .h5 file is readable and loads successfully with tf.keras.models.load_model() without errors.
- Validate that the model can be mounted into a TensorFlow Serving container and responds correctly to /model/metadata requests.
- Test end-to-end classification by passing a SMILES string to the /classify endpoint and receiving valid predictions without layer name mismatch errors.

## Limitations

- Conversion requires exact TensorFlow version 2.3.0; newer or older versions may produce incompatible .h5 files or serialization errors.
- Layer names must be pre-defined in the source Keras model; if 'input_2048', 'input_4096', or 'output' are not present, model retraining or manual layer renaming is required.
- HDF5 format does not preserve certain TensorFlow-specific metadata; custom layers or post-training quantization may not serialize correctly.
- The get_models.sh script location (Classifier/models_folder/models) is environment-specific and must be verified before execution.

## Evidence

- [intro] Model preparation requirement: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [intro] Layer name validation: "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [intro] Model download workflow: "cd Classifier/models_folder/models
sh ./get_models.sh"
- [intro] Serialization format requirement: "We pass through tensorflow serving at this url"
- [readme] TensorFlow Serving integration: "Use TensorFlow 2.3.0's save_model or h5 serialization utility, outputting .h5 files compatible with TensorFlow Serving"
