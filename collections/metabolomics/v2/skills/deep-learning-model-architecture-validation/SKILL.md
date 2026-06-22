---
name: deep-learning-model-architecture-validation
description: Use when after converting or loading a Keras model to HDF5 TensorFlow 2.3.0 format, especially when the model will be served through a pipeline (e.g., NP Classifier) that expects specific input/output layer names.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3474
  tools:
  - get_models.sh
  - Python
  - TensorFlow 2.3.0
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- cd Classifier/models_folder/models sh ./get_models.sh
- Make sure you have python installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npclassifier
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  dedup_kept_from: coll_npclassifier
schema_version: 0.2.0
---

# deep-learning-model-architecture-validation

## Summary

Validate that a converted Keras deep learning model exposes the correct input and output layer names required by a downstream inference pipeline. This skill ensures structural compliance before deployment, preventing runtime failures due to layer naming mismatches.

## When to use

Apply this skill after converting or loading a Keras model to HDF5 TensorFlow 2.3.0 format, especially when the model will be served through a pipeline (e.g., NP Classifier) that expects specific input/output layer names. Use it as a pre-deployment validation step before feeding the model to inference APIs or TensorFlow Serving.

## When NOT to use

- The model has not yet been converted to HDF5 format or is still in native Keras format.
- The downstream pipeline does not have fixed layer name requirements and can accept any valid input/output interface.
- You are only interested in model accuracy or inference performance, not structural metadata.

## Inputs

- HDF5 TensorFlow 2.3.0 model file (converted from Keras)
- specification document or pipeline configuration defining expected input/output layer names

## Outputs

- validated model object with confirmed layer names
- audit log or report documenting input and output layer names

## How to apply

Load the converted HDF5 TF2 model using TensorFlow 2.3.0's model loading API. Inspect the model's layer architecture by iterating through the model's layers or using the model's layer name property accessor. Cross-reference the discovered input layer names against the expected names ('input_2048' and 'input_4096' for NP Classifier) and the output layer name against the expected output name ('output'). Log or save the layer names for audit. If any mismatch is found, the model conversion step failed or used incorrect parameters and must be repeated. Confirm structural compliance before proceeding to deployment or API integration.

## Related tools

- **TensorFlow 2.3.0** (loads and introspects the converted HDF5 model to access layer metadata and names) — https://github.com/tensorflow/tensorflow
- **Python** (scripting language used to programmatically load the model and inspect layers)
- **get_models.sh** (shell script that downloads and converts pre-trained Keras models to HDF5 TF2 format prior to validation) — https://github.com/mwang87/NP-Classifier

## Examples

```
import tensorflow as tf
model = tf.keras.models.load_model('model.h5')
input_names = [layer.name for layer in model.layers if 'input' in layer.name]
output_name = model.layers[-1].name
print(f'Inputs: {input_names}, Output: {output_name}')
```

## Evaluation signals

- Input layer names match the expected set: 'input_2048' and 'input_4096'
- Output layer name exactly equals 'output'
- Model loads without errors using TensorFlow 2.3.0's model loading API
- Layer introspection returns all expected layer objects with no missing or extra named layers
- Audit log or saved metadata confirms layer names and can be compared against specification

## Limitations

- This skill validates only layer naming conventions; it does not check model weights, numerical stability, inference correctness, or performance.
- The skill is specific to HDF5 TensorFlow 2.3.0 format; models in other serialization formats or TensorFlow versions may require different inspection methods.
- If the model was incorrectly converted during the Keras-to-HDF5 process (e.g., layer names were not preserved), validation will fail but will not automatically repair the conversion.

## Evidence

- [readme] Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output": "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [other] Load the converted HDF5 TF2 model using TensorFlow 2.3.0's model loading API. Inspect the model's layer architecture to confirm the presence of input layers named 'input_2048' and 'input_4096' and an output layer named 'output'.: "Load the converted HDF5 TF2 model using TensorFlow 2.3.0's model loading API. Inspect the model's layer architecture to confirm the presence of input layers named 'input_2048' and 'input_4096' and an"
- [readme] tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models: "tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [readme] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
