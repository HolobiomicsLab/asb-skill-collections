---
name: model-deployment-preparation
description: Use when you have a pre-trained Keras model and need to deploy it via
  a Docker-based TensorFlow Serving API (e.g., for molecular classification via SMILES),
  but the model's layer naming or format does not yet match the target runtime's expectations
  (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - get_models.sh
  - Python
  - TensorFlow 2.3.0
  - Docker
  - Keras
  - TensorFlow Serving
  - Docker and docker-compose
  license_tier: open
  provenance_tier: literature
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
  - build: coll_npclassifier_cq
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  dedup_kept_from: coll_npclassifier
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

# model-deployment-preparation

## Summary

Prepare a pre-trained Keras model for deployment in a TensorFlow Serving pipeline by converting it to HDF5 TF2 format and validating that input/output layer names match the expected schema. This skill ensures structural compliance before containerization and API exposure.

## When to use

You have a pre-trained Keras model and need to deploy it via a Docker-based TensorFlow Serving API (e.g., for molecular classification via SMILES), but the model's layer naming or format does not yet match the target runtime's expectations (e.g., 'input_2048', 'input_4096', 'output' in HDF5 TF2 format for NP Classifier).

## When NOT to use

- The model is already in HDF5 TF2 format with correct layer names and you are only tuning hyperparameters or retraining.
- You are deploying a model that does not require fixed layer names (e.g., a model served via a custom Python wrapper that remaps inputs dynamically).
- The target deployment system uses SavedModel format or ONNX instead of HDF5 TF2.

## Inputs

- pre-trained Keras model file (or model directory)
- target framework specification (TensorFlow 2.3.0, HDF5 format)
- expected layer name schema (input_2048, input_4096, output)

## Outputs

- HDF5 TF2 model file with validated layer names
- layer name inspection report (JSON or plaintext log)
- confirmation of structural compliance

## How to apply

First, clone the target repository and execute its model conversion script (e.g., get_models.sh) with TensorFlow 2.3.0 installed to transform Keras models into HDF5 TF2 format. Then load the converted model using TensorFlow's model loading API and programmatically inspect the layer architecture to confirm the presence of exactly two input layers named 'input_2048' and 'input_4096' and one output layer named 'output'. Log or save the validated layer names. If any layer names differ, adjust the model conversion pipeline or the API routing code before proceeding to Dockerization. This ensures the model will correctly accept SMILES strings and other inputs through the /classify endpoint without runtime layer-binding errors.

## Related tools

- **TensorFlow 2.3.0** (Convert Keras models to HDF5 TF2 format and load/inspect model layer architecture)
- **get_models.sh** (Automate download and conversion of pre-trained Keras models to HDF5 TF2 format) — https://github.com/mwang87/NP-Classifier
- **Docker** (Containerize the validated model for deployment in TensorFlow Serving)
- **Python** (Execute model loading, layer inspection, and validation scripts)

## Examples

```
cd Classifier/models_folder/models && sh ./get_models.sh
```

## Evaluation signals

- Model loads without errors using TensorFlow 2.3.0's model loading API.
- Layer inspection confirms presence of exactly two input layers named 'input_2048' and 'input_4096'.
- Layer inspection confirms presence of exactly one output layer named 'output'.
- Model metadata endpoint (/model/metadata) returns layer names matching the schema.
- Classify API endpoint (/classify?smiles=<>) accepts and processes test SMILES strings without layer-binding errors.

## Limitations

- Requires TensorFlow 2.3.0 specifically; compatibility with other TF versions is not addressed.
- Layer names are hardcoded and cannot be dynamically remapped after conversion without retraining or post-hoc model surgery.
- The conversion process is specific to Keras → HDF5 TF2; other source formats (SavedModel, ONNX, PyTorch) are not supported by the get_models.sh script.
- Privacy logging captures which structures were classified but not user identity, which may still pose privacy concerns in sensitive domains.

## Evidence

- [readme] tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [readme] Input and output layer names are explicitly specified: "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [readme] Model conversion script location and invocation: "cd Classifier/models_folder/models
sh ./get_models.sh"
- [readme] Layer name validation is a deployment prerequisite: "If the model input names change, then we need to change it in the code"
- [readme] The converted model is passed through TensorFlow Serving: "We pass through tensorflow serving at this url:

```/model/metadata```"
