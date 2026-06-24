---
name: keras-model-serialization
description: Use when you have downloaded pre-trained Keras model files (via get_models.sh
  or similar) and need to prepare them for deployment in a TensorFlow Serving environment,
  particularly when the downstream inference system expects .h5 serialized models
  with explicit input/output layer naming conventions.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Python
  - Keras
  - TensorFlow 2.3.0
  - TensorFlow Serving
  license_tier: open
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- Make sure you have python installed
- convert the keras models into HDF5 TF2 models
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

# keras-model-serialization

## Summary

Convert pre-trained Keras neural network models to HDF5 TensorFlow 2 format for deployment in TensorFlow Serving. This serialization step is essential for packaging trained models into a format compatible with containerized inference pipelines.

## When to use

You have downloaded pre-trained Keras model files (via get_models.sh or similar) and need to prepare them for deployment in a TensorFlow Serving environment, particularly when the downstream inference system expects .h5 serialized models with explicit input/output layer naming conventions.

## When NOT to use

- Models are already serialized in .h5 format or other production-ready serialization (e.g., SavedModel format).
- Your environment cannot support TensorFlow 2.3.0 specifically—version mismatch will cause layer naming and API compatibility failures.
- Input/output layer names in your Keras models do not or cannot be renamed to 'input_2048', 'input_4096', and 'output'—the NP Classifier expects these exact conventions.

## Inputs

- Pre-trained Keras model files (downloaded via get_models.sh script)
- Python environment with TensorFlow 2.3.0 installed

## Outputs

- .h5 serialized models (HDF5 TensorFlow 2 format)
- Models compatible with TensorFlow Serving deployment

## How to apply

First, verify that Python and TensorFlow version 2.3.0 are installed in your environment. Navigate to the directory containing the downloaded Keras model files. Load each Keras model using TensorFlow 2.3.0's Keras API and inspect layer names to confirm input layers are named 'input_2048' and 'input_4096' and the output layer is named 'output'—if layer names do not match these conventions, the downstream classifier will fail. Convert each validated Keras model to HDF5 TensorFlow 2 format using TensorFlow 2.3.0's save_model or h5 serialization utility, outputting .h5 files that are compatible with TensorFlow Serving. Verify the resulting .h5 files can be loaded and interrogated via the TensorFlow Serving metadata endpoint (/model/metadata) before deploying into the Docker container.

## Related tools

- **Python** (Runtime environment for executing model conversion scripts)
- **TensorFlow 2.3.0** (Provides Keras API for loading, inspecting, and serializing models to HDF5 format)
- **Keras** (High-level API (via TensorFlow 2.3.0) for loading and converting pre-trained neural network models)
- **TensorFlow Serving** (Target inference platform that consumes the .h5 serialized models and exposes metadata endpoint for layer name validation)

## Evaluation signals

- Resulting .h5 files can be successfully loaded by TensorFlow 2.3.0 without errors.
- Layer inspection via TensorFlow Serving's /model/metadata endpoint confirms input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'.
- Model input/output dimensions and data types are preserved after serialization (verify via layer shape inspection).
- .h5 files are readable by downstream Docker-deployed NP Classifier inference service without layer naming errors.
- File size and modification timestamp of .h5 output files confirm conversion completed successfully.

## Limitations

- Conversion is specific to TensorFlow 2.3.0; other versions may introduce incompatibilities in serialization format or Keras API behavior.
- Layer names must exactly match the expected convention ('input_2048', 'input_4096', 'output'); if the original Keras models use different layer names, they must be renamed before serialization or the downstream classifier will fail.
- HDF5 serialization via TensorFlow 2.3.0 may not preserve custom layers or loss functions; models must use only standard Keras layer types.
- No changelog or version history provided in the NP-Classifier repository; reproducibility across future updates of the codebase is not guaranteed.

## Evidence

- [other] Model preparation requires Python and TensorFlow version 2.3.0 to be installed to convert Keras models into HDF5 TF2 format: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [readme] Input layer names must be 'input_2048' and 'input_4096'; output layer must be 'output': "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [other] Conversion uses TensorFlow 2.3.0's h5 serialization to produce HDF5 format compatible with TensorFlow Serving: "Convert each Keras model to HDF5 TensorFlow 2 format using TensorFlow 2.3.0's save_model or h5 serialization utility, outputting .h5 files compatible with TensorFlow Serving"
- [readme] Validation occurs through TensorFlow Serving's metadata endpoint after conversion: "We pass through tensorflow serving at this url: ```/model/metadata``` If the model input names change, then we need to change it in the code"
- [readme] Models are downloaded via get_models.sh script prior to conversion: "cd Classifier/models_folder/models
sh ./get_models.sh"
