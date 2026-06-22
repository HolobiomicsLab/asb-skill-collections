---
name: deep-learning-layer-inspection
description: Use when when you have downloaded pre-trained Keras models and need to confirm their layer naming and structure conform to requirements for TensorFlow Serving or other deployment pipelines—specifically before converting to HDF5 format or integrating into a production API that expects fixed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3474
  tools:
  - Python
  - TensorFlow 2.3.0
  - Keras
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- Make sure you have python installed
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-layer-inspection

## Summary

Inspect and validate layer names and architecture of pre-trained deep learning models (Keras/TensorFlow) to ensure conformance with downstream serving requirements. This skill verifies that input and output layer names match expected conventions before model deployment or format conversion.

## When to use

When you have downloaded pre-trained Keras models and need to confirm their layer naming and structure conform to requirements for TensorFlow Serving or other deployment pipelines—specifically before converting to HDF5 format or integrating into a production API that expects fixed input/output layer names.

## When NOT to use

- Model is already in HDF5 TF2 format—skip layer inspection and proceed directly to serving configuration
- Model layer names have been documented as already validated in a prior workflow step
- You are working with a custom model architecture where layer naming conventions differ from the NP Classifier standard

## Inputs

- Pre-trained Keras model files (.h5 or SavedModel format)
- TensorFlow 2.3.0 runtime environment with Keras API

## Outputs

- Validated layer name report (confirming 'input_2048', 'input_4096', 'output' presence and position)
- Go/no-go decision for proceeding to model conversion or deployment

## How to apply

Load each downloaded Keras model using TensorFlow 2.3.0's Keras API and programmatically inspect all layer names in the model graph. Validate that the model contains exactly two input layers named 'input_2048' and 'input_4096' and one output layer named 'output'. If layer names do not match these conventions, flag the model and do not proceed with conversion or deployment. This validation step ensures compatibility with downstream TensorFlow Serving configuration and API contracts that depend on these specific layer name bindings.

## Related tools

- **TensorFlow 2.3.0** (Keras API for loading and introspecting model layer structure and names)
- **Keras** (High-level API for model inspection and layer attribute access)
- **Python** (Scripting language for programmatic model loading and layer iteration)

## Examples

```
import tensorflow as tf; model = tf.keras.models.load_model('path/to/model.h5'); print([layer.name for layer in model.layers])
```

## Evaluation signals

- Model loads without error using TensorFlow 2.3.0 Keras API (model.load_model or similar)
- Layer name audit confirms exactly two input layers with names 'input_2048' and 'input_4096'
- Layer name audit confirms exactly one output layer with name 'output'
- No warnings or deprecations from TensorFlow regarding layer naming or structure
- Downstream TensorFlow Serving metadata endpoint (/model/metadata) correctly reflects inspected layer names

## Limitations

- Layer inspection is specific to TensorFlow 2.3.0; models trained or saved in other TensorFlow versions may have different layer naming conventions or structure
- Inspection does not validate layer input/output shapes, only names; shape mismatches will be detected only at inference time
- Models with dynamic or conditional layer structures may not be fully inspectable using static layer enumeration

## Evidence

- [other] Use TensorFlow 2.3.0 Keras API to load each downloaded Keras model and inspect layer names to confirm input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'.: "Use TensorFlow 2.3.0 Keras API to load each downloaded Keras model and inspect layer names to confirm input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'."
- [readme] Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output".: "Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output"."
- [readme] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
