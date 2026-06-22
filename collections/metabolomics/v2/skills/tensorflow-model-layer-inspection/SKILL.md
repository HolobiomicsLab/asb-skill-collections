---
name: tensorflow-model-layer-inspection
description: Use when after converting or downloading a pre-trained Keras model to HDF5 TensorFlow 2.3.0 format, particularly when integrating the model into a fixed-interface pipeline (e.g., NP Classifier) that expects specific named input/output layers.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3474
  tools:
  - get_models.sh
  - TensorFlow 2.3.0
  - Python
  - Docker
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- cd Classifier/models_folder/models sh ./get_models.sh
- tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.1c00399
  all_source_dois:
  - 10.1021/acs.jnatprod.1c00399
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tensorflow-model-layer-inspection

## Summary

Inspect and validate the layer architecture of a TensorFlow 2.3.0 HDF5 model to confirm the presence and names of input and output layers required for downstream pipeline integration. This skill ensures structural compliance before model deployment in containerized environments.

## When to use

After converting or downloading a pre-trained Keras model to HDF5 TensorFlow 2.3.0 format, particularly when integrating the model into a fixed-interface pipeline (e.g., NP Classifier) that expects specific named input/output layers. Use this skill as a validation checkpoint before building Docker containers or passing the model through TensorFlow Serving.

## When NOT to use

- Model is already deployed in production and layer names are no longer mutable; inspection should occur before containerization.
- Input is a SavedModel directory without an accompanying .h5 file; use TensorFlow's native inspect tools instead.
- Layer names are intentionally dynamic or user-configurable; this skill assumes a fixed specification.

## Inputs

- HDF5 TensorFlow 2.3.0 model file (*.h5 or SavedModel format)
- Expected layer name specification (input_2048, input_4096, output)

## Outputs

- Validated model object with confirmed layer names
- Log or report confirming presence and names of input/output layers
- Boolean pass/fail status for pipeline integration readiness

## How to apply

Load the HDF5 TF2 model using TensorFlow 2.3.0's model loading API (e.g., tf.keras.models.load_model). Programmatically inspect the model's layer architecture by iterating through model.layers or accessing layer metadata. Verify the presence of exactly two input layers with names 'input_2048' and 'input_4096' and one output layer named 'output'. Compare the observed layer names against the required specification and log or save the findings. Fail fast if layer names do not match; this indicates the model conversion step was incomplete or the wrong model was loaded.

## Related tools

- **TensorFlow 2.3.0** (Model loading and layer inspection via tf.keras.models.load_model and model.layers API)
- **Python** (Scripting language for programmatic model inspection and validation)
- **get_models.sh** (Script that downloads and converts pre-trained Keras models to HDF5 TF2 format prior to inspection) — https://github.com/mwang87/NP-Classifier
- **Docker** (Containerization context in which validated models are deployed downstream)

## Examples

```
import tensorflow as tf; model = tf.keras.models.load_model('model.h5'); layer_names = [layer.name for layer in model.layers]; print('Input layers:', [n for n in layer_names if 'input' in n]); print('Output layer:', layer_names[-1])
```

## Evaluation signals

- Model loads without error using tf.keras.models.load_model with TensorFlow 2.3.0.
- Exactly two input layers are present with names 'input_2048' and 'input_4096' (case-sensitive match).
- Exactly one output layer is present with name 'output' (case-sensitive match).
- Layer inspection completes without exceptions; model.layers is non-empty and iterable.
- Logged layer names match specification; no extra or missing layers in critical positions.

## Limitations

- Layer name inspection does not validate tensor shapes, data types, or numerical correctness—only name presence.
- If the model conversion step (get_models.sh) fails or uses an incompatible TensorFlow version, layer names may not be set as expected; pre-conversion validation is required.
- Layer names are case-sensitive; 'input_2048' is not equivalent to 'Input_2048' or 'INPUT_2048'.
- This skill validates structural compliance but does not test inference correctness or integration with downstream classifiers.

## Evidence

- [other] Load the converted HDF5 TF2 model using TensorFlow 2.3.0's model loading API. Inspect the model's layer architecture to confirm the presence of input layers named 'input_2048' and 'input_4096' and an output layer named 'output'.: "Load the converted HDF5 TF2 model using TensorFlow 2.3.0's model loading API. Inspect the model's layer architecture to confirm the presence of input layers named 'input_2048' and 'input_4096' and an"
- [readme] Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output": "Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output"."
- [readme] Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models.: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models."
- [readme] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
