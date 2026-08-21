---
name: keras-model-conversion-to-hdf5
description: Use when you have pre-trained Keras models from the NP-Classifier repository
  that must be deployed via TensorFlow Serving and need to expose standardized input/output
  layer names ('input_2048', 'input_4096', 'output') for integration with the classification
  API.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3173
  tools:
  - get_models.sh
  - Python
  - TensorFlow 2.3.0
  - Docker
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

# keras-model-conversion-to-hdf5

## Summary

Convert pre-trained Keras models to HDF5 TensorFlow 2.3.0 format with properly named input and output layers for deployment in the NP Classifier pipeline. This skill ensures structural compliance of the converted model with the pipeline's layer naming requirements.

## When to use

You have pre-trained Keras models from the NP-Classifier repository that must be deployed via TensorFlow Serving and need to expose standardized input/output layer names ('input_2048', 'input_4096', 'output') for integration with the classification API.

## When NOT to use

- The Keras model is already in HDF5 TensorFlow 2.3.0 format with correct layer names.
- You are deploying the model in a different pipeline that uses different layer naming conventions.
- TensorFlow version in your environment is not 2.3.0, as the conversion process may produce incompatible artifacts.

## Inputs

- Pre-trained Keras model files (typically .h5 or SavedModel format)
- get_models.sh script from NP-Classifier/Classifier/models_folder/models
- TensorFlow 2.3.0 installation with Python environment

## Outputs

- Converted HDF5 TensorFlow 2.3.0 model file
- Model layer name validation log
- Model metadata confirming input layer names 'input_2048' and 'input_4096' and output layer name 'output'

## How to apply

Clone the mwang87/NP-Classifier repository and navigate to Classifier/models_folder/models. Execute the get_models.sh script, which automates the Keras-to-HDF5 conversion process using TensorFlow 2.3.0. After conversion, load the resulting HDF5 model using TensorFlow's model loading API and inspect the layer architecture to confirm the presence of exactly two input layers named 'input_2048' and 'input_4096' and one output layer named 'output'. Log or persist the layer names as evidence of structural compliance. If layer names do not match the specification, the model will not integrate correctly with downstream API endpoints that expect these specific names.

## Related tools

- **TensorFlow 2.3.0** (Performs Keras model conversion to HDF5 format and provides model loading and layer inspection APIs)
- **get_models.sh** (Automates download and conversion of pre-trained Keras models to HDF5 TF2 format) — https://github.com/mwang87/NP-Classifier
- **Docker** (Provides reproducible environment with pinned TensorFlow 2.3.0 version for model conversion and deployment)
- **Python** (Runtime environment required to execute model conversion and validation scripts)

## Examples

```
cd Classifier/models_folder/models && sh ./get_models.sh
```

## Evaluation signals

- Model loads without error using TensorFlow 2.3.0's model loading API after conversion.
- Layer inspection confirms exactly two input layers named 'input_2048' and 'input_4096' are present in the model graph.
- Model output layer is unambiguously named 'output' in the converted HDF5 structure.
- Model metadata endpoint (/model/metadata) through TensorFlow Serving correctly reports the three required layer names.
- Downstream /classify API endpoint successfully accepts SMILES input and produces predictions without layer-name mismatch errors.

## Limitations

- Conversion requires TensorFlow 2.3.0 specifically; other versions may produce incompatible HDF5 artifacts or altered layer names.
- If upstream Keras models do not conform to the expected input/output structure, conversion will succeed but layer names will not match the pipeline specification, causing downstream API failures.
- The conversion process is one-way; reverting from HDF5 TF2 format back to native Keras format may result in loss of metadata.

## Evidence

- [readme] Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models.: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [readme] Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output": "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [readme] cd Classifier/models_folder/models; sh ./get_models.sh: "cd Classifier/models_folder/models
sh ./get_models.sh"
- [other] The NP Classifier model conversion process requires the resulting HDF5 TF2 model to expose three specific layer names: two input layers named 'input_2048' and 'input_4096', and one output layer named 'output'.: "The NP Classifier model conversion process requires the resulting HDF5 TF2 model to expose three specific layer names: two input layers named 'input_2048' and 'input_4096', and one output layer named"
