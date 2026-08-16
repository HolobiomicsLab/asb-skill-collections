---
name: tensorflow-serving-deployment
description: 'Use when you have trained Keras models that need to be served as microservices
  for real-time inference. Specifically: (1) models have been converted to HDF5 TensorFlow
  2.3.0 format with properly named input layers (''input_2048'', ''input_4096'') and
  output layer (''output'');'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3474
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - TensorFlow
  - TensorFlow Serving
  - Docker
  - docker-compose
  - nginx
  - Python with TensorFlow 2.3.0 and Keras
  - NP Classifier
  license_tier: open
derived_from:
- doi: 10.1021/jacs.9b13786
  title: CSCS / deep CNN natural-product annotation
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

# tensorflow-serving-deployment

## Summary

Deploy trained TensorFlow/Keras models as containerized inference services using TensorFlow Serving behind an nginx reverse proxy, enabling scalable programmatic access to model predictions via REST APIs. This skill is essential when you need to expose trained models (converted to HDF5 TensorFlow 2.3.0 format) as production-ready web services with load balancing and caching capabilities.

## When to use

You have trained Keras models that need to be served as microservices for real-time inference. Specifically: (1) models have been converted to HDF5 TensorFlow 2.3.0 format with properly named input layers ('input_2048', 'input_4096') and output layer ('output'); (2) you need to expose predictions via HTTP endpoints (e.g., /classify?smiles=<>) with optional caching; (3) you are deploying locally or in a containerized environment where docker-compose orchestration is available.

## When NOT to use

- Models are not yet converted to HDF5 TensorFlow 2.3.0 format or have incorrectly named input/output layers—use model conversion and validation steps first.
- You require GPU acceleration or distributed multi-host serving beyond single-machine docker-compose orchestration—use Kubernetes or cloud-hosted TensorFlow Serving instead.
- Input data is not SMILES strings or the classification task is not molecular property prediction—this workflow is specifically tuned for the NP Classifier use case.

## Inputs

- Pre-trained Keras model files (converted to HDF5 TensorFlow 2.3.0 format)
- Model weights and architecture with input layers named 'input_2048' and 'input_4096' and output layer named 'output'
- docker-compose configuration file (make server-compose target)
- Query strings in SMILES format (e.g., /classify?smiles=CC(C)Cc1ccc(cc1)C(C)C(O)=O)

## Outputs

- Running TensorFlow Serving container exposing model inference on an internal port
- Running classification API container accepting HTTP requests at /classify and /model/metadata endpoints
- Running nginx reverse proxy container routing requests across nginx-net Docker network
- JSON classification results returned to /classify endpoint
- Model metadata (input/output layer names and shapes) returned at /model/metadata endpoint

## How to apply

First, ensure models are pre-trained and converted to HDF5 TensorFlow 2.3.0 format with correct input/output layer names, then download and organize models in the Classifier/models_folder/models directory. Create a Docker bridge network (nginx-net) to enable communication between TensorFlow Serving and the classification API containers. Use make server-compose to invoke docker-compose, which orchestrates simultaneous deployment of TensorFlow Serving (exposing the model metadata endpoint at /model/metadata) and the classification API (accepting SMILES strings as query parameters). The nginx reverse proxy routes requests to the appropriate backend service. Verify deployment by querying the metadata endpoint to confirm model input/output layer names match expectations, then test the /classify endpoint with sample SMILES strings, using the cached flag parameter when fast repeated lookups are needed.

## Related tools

- **Docker** (Containerization engine for building and running isolated TensorFlow Serving and API containers)
- **docker-compose** (Orchestrates multi-container deployment (TensorFlow Serving, classification API, nginx) via declarative YAML configuration)
- **TensorFlow Serving** (Inference server that loads HDF5 TensorFlow 2.3.0 models and exposes model metadata and prediction endpoints)
- **nginx** (Reverse proxy and load balancer routing HTTP requests from clients to TensorFlow Serving and classification API backends)
- **Python with TensorFlow 2.3.0 and Keras** (Pre-deployment tool for converting Keras models to HDF5 TensorFlow 2.3.0 format before containerization)
- **NP Classifier** (Reference implementation providing Makefile (make server-compose target) and docker-compose configuration) — https://github.com/mwang87/NP-Classifier

## Examples

```
make server-compose
```

## Evaluation signals

- Verify docker network creation: run `docker network ls | grep nginx-net` returns exactly one result with driver 'bridge'.
- Query metadata endpoint: `curl http://localhost/model/metadata` returns JSON with input layer names 'input_2048' and 'input_4096' and output layer name 'output'.
- Test classification endpoint: `curl 'http://localhost/classify?smiles=CC(C)Cc1ccc(cc1)C(C)C(O)=O'` returns valid JSON classification results without errors.
- Verify all three containers are running: `docker ps` shows containers for TensorFlow Serving, classification API, and nginx all in 'Up' state.
- Confirm caching works: query the /classify endpoint twice with the same SMILES string and `cached=true` parameter; second request should complete faster than first.

## Limitations

- Models must be pre-converted to HDF5 TensorFlow 2.3.0 format; the deployment workflow does not handle on-the-fly model conversion from other formats.
- Input/output layer names are hardcoded expectations ('input_2048', 'input_4096', 'output'); models with different layer naming conventions will fail validation.
- Single-machine docker-compose deployment is not suitable for high-throughput or distributed inference; horizontal scaling requires Kubernetes or similar orchestration.
- No changelog documented; version stability and backward compatibility of model formats across TensorFlow releases is not guaranteed.

## Evidence

- [readme] Model layer name requirements: "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [readme] TensorFlow Serving deployment via docker-compose: "We pass through tensorflow serving at this url:

```/model/metadata```

If the model input names change, then we need to change it in the code"
- [readme] Local deployment orchestration: "We typically will deploy this locally. To bring everything up, you need docker and docker-compose."
- [readme] Docker network creation step: "If you didn't do it already, you will need a network.

```shell
docker network create nginx-net
```

```shell
make server-compose
```"
- [readme] Classification API accepts SMILES input: "Classify programmatically 

```/classify?smiles=<>```

You can also provide cached flag to the params"
- [readme] TensorFlow 2.3.0 model conversion requirement: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
