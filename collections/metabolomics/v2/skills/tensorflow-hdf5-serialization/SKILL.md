---
name: tensorflow-hdf5-serialization
description: Use when when you have acquired Keras models (via get_models.sh or similar download) and need to deploy them locally through TensorFlow Serving within a Docker/docker-compose stack.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
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
- tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models
- 'We pass through tensorflow serving at this url: ```/model/metadata```'
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

# Convert Keras Models to HDF5 TensorFlow 2.0 Format

## Summary

This skill converts downloaded Keras models to HDF5 TensorFlow 2.0 format for deployment in containerized serving pipelines. It is essential for preparing NP Classifier models for local TensorFlow Serving integration, ensuring compatibility with downstream inference and model metadata operations.

## When to use

When you have acquired Keras models (via get_models.sh or similar download) and need to deploy them locally through TensorFlow Serving within a Docker/docker-compose stack. Apply this skill before building the Dockerized server to guarantee that model layer names conform to the expected schema (input_2048, input_4096, output) and the model format is readable by TensorFlow Serving.

## When NOT to use

- Models are already in HDF5 format and layer names are pre-validated.
- You are using TensorFlow version < 2.0 or a version other than 2.3.0, as the conversion utilities and serialization format may differ.
- Input layers do not correspond to 2048 or 4096-dimensional embeddings, or output layer structure is non-standard; conversion alone will not fix architectural mismatches.

## Inputs

- Keras model files (downloaded via get_models.sh)
- Python environment with TensorFlow 2.3.0
- Layer naming specification (input_2048, input_4096, output)

## Outputs

- HDF5-serialized TensorFlow 2.0 models (.h5 files)
- Model metadata (layer names and tensor shapes)

## How to apply

First, ensure Python and TensorFlow 2.3.0 are installed in your environment. Download the NP Classifier models by navigating to Classifier/models_folder/models and executing get_models.sh. Then use Keras model conversion utilities (available in TensorFlow 2.3.0) to convert each Keras model to HDF5 format. During or after conversion, validate that the input layers are named exactly 'input_2048' and 'input_4096', and the output layer is named 'output'; these layer names are required for TensorFlow Serving compatibility and downstream classification API integration. After conversion, verify the resulting .h5 files are readable and queryable via the /model/metadata endpoint to confirm layer schema is correct before proceeding to Docker deployment.

## Related tools

- **TensorFlow** (Provides Keras model conversion utilities and HDF5 serialization for TF2 models)
- **Keras** (Source model format; conversion target is HDF5 TensorFlow 2.0 serialization)
- **Python** (Execution environment for running conversion scripts)
- **TensorFlow Serving** (Downstream deployment target; requires HDF5 models with specific layer naming)

## Examples

```
cd Classifier/models_folder/models && sh ./get_models.sh && python -c "import tensorflow as tf; model = tf.keras.models.load_model('model.h5'); model.save('model_converted.h5', save_format='tf')"
```

## Evaluation signals

- Converted model files are readable and parse without errors as valid HDF5 archives.
- Model metadata endpoint (/model/metadata) returns input layer names as 'input_2048' and 'input_4096' and output layer name as 'output'.
- Model accepts SMILES string queries through the /classify?smiles=<> API without shape mismatch or layer lookup errors.
- File format verification: output files have .h5 extension and can be inspected with HDF5 tools (h5dump, h5py) to confirm layer structure.
- Successful integration into Docker Serving pipeline using 'make server-compose' after model conversion.

## Limitations

- Conversion is specific to TensorFlow 2.3.0; other versions may produce incompatible serializations or fail to validate layer names.
- Layer renaming must be performed during or immediately after conversion; the script does not provide post-hoc layer relabeling utilities.
- No changelog or version history documented for model format changes or breaking updates to the NP Classifier model schema.
- Conversion does not validate downstream model behavior (e.g., correctness of predictions); it only ensures format and layer name compliance.

## Evidence

- [readme] Model acquisition and format conversion step: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models."
- [readme] Download workflow prerequisite: "cd Classifier/models_folder/models
sh ./get_models.sh"
- [readme] Layer naming requirement for TensorFlow Serving: "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [readme] Metadata validation step post-conversion: "We pass through tensorflow serving at this url:

```/model/metadata```"
- [intro] Purpose of conversion in deployment context: "Model acquisition requires downloading NP Classifier models via get_models.sh script, then converting Keras models to HDF5 TensorFlow 2.0 models using Python and TensorFlow version 2.3.0."
