---
name: docker-container-orchestration-for-ml-services
description: Use when you have trained or pre-trained ML models (Keras, TensorFlow)
  that need to be exposed as HTTP endpoints for programmatic classification or inference,
  require reproducible deployment across environments, or need to coordinate multiple
  services (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3676
  - http://edamontology.org/topic_0091
  tools:
  - docker
  - docker-compose
  - Python
  - TensorFlow Serving
  - TensorFlow / Keras
  license_tier: open
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- you need docker and docker-compose
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# docker-container-orchestration-for-ml-services

## Summary

Deploy containerized machine learning inference services (e.g., TensorFlow Serving models) using Docker and docker-compose to expose REST APIs for real-time predictions. This skill bundles model preparation, network configuration, and container orchestration to enable scalable, reproducible ML service delivery.

## When to use

You have trained or pre-trained ML models (Keras, TensorFlow) that need to be exposed as HTTP endpoints for programmatic classification or inference, require reproducible deployment across environments, or need to coordinate multiple services (e.g., inference engine + web server) with shared networking.

## When NOT to use

- Model is still in active development or requires frequent retraining within the same service lifecycle — use local development/notebook environments instead.
- Input data is already hosted in a managed cloud ML service (e.g., AWS SageMaker, Google Vertex AI) — orchestrating containers adds unnecessary overhead.
- Inference latency requirements are sub-millisecond and demand GPU/TPU co-location not easily achieved via containerization.

## Inputs

- Pre-trained ML model files (Keras .h5, TensorFlow SavedModel format)
- Model metadata (input/output layer names, expected tensor shapes)
- docker-compose.yml configuration file
- API endpoint specification (HTTP query parameters, request schema)
- Test data samples (e.g., SMILES strings, feature vectors)

## Outputs

- Deployed Docker network with running inference service
- HTTP API endpoints returning model predictions (JSON-serialized outputs)
- Service metadata endpoint (/model/metadata) exposing model signature
- Optional: cached prediction store (in-memory or persistent)

## How to apply

First, prepare models by verifying their input/output layer names match the service's expectations (e.g., 'input_2048', 'input_4096' for inputs; 'output' for predictions) and convert to the target format (HDF5 TensorFlow 2.3.0). Create a dedicated Docker network (e.g., docker network create nginx-net) to enable secure inter-container communication. Write a docker-compose configuration that defines services for the inference engine (TensorFlow Serving), API handler, and optional reverse proxy, binding model endpoints and REST routes. Build and start all services via make server-compose or docker-compose up, then validate by querying model metadata (/model/metadata) and test endpoints with representative inputs (e.g., SMILES strings for chemistry classifiers). Implement optional performance optimizations such as caching logic in the endpoint handler to retrieve prior results.

## Related tools

- **docker** (Container runtime for packaging and isolating the inference service and its dependencies) — https://www.docker.com
- **docker-compose** (Orchestration tool for defining and running multi-container applications (inference engine + API server)) — https://docs.docker.com/compose
- **TensorFlow Serving** (Inference serving system that loads and exposes TensorFlow models via REST API)
- **TensorFlow / Keras** (Framework for model training, format conversion (Keras to HDF5 TF2), and verification of layer signatures)
- **Python** (Language for model format conversion scripts and optional caching/endpoint logic)

## Examples

```
docker network create nginx-net && make server-compose && curl 'http://localhost:8080/classify?smiles=CC(C)Cc1ccc(cc1)C(C)C(O)=O&cached=true'
```

## Evaluation signals

- Model metadata endpoint (/model/metadata) successfully responds with layer names matching specification ('input_2048', 'input_4096', 'output').
- Classification API endpoint (/classify?smiles=<>) returns predictions with correct JSON schema and plausible confidence scores for test SMILES strings.
- Repeated queries to the same input return cached results, reducing response latency and verifying caching logic is functional.
- All services remain healthy and restart automatically on container failure (inspect via docker ps and service logs).
- Network traffic between containers flows only through the declared Docker network (nginx-net); verify with docker network inspect.

## Limitations

- Model input/output layer names must be hardcoded or discovered at service startup; dynamic layer renaming is not supported and requires model retraining or export with canonical names.
- Performance depends on TensorFlow Serving version and batch size configuration; single-input requests may not fully utilize GPU/CPU and benefit from request batching or model quantization.
- Caching does not account for model version updates; stale cached results will persist until cache is manually cleared or the service is restarted.
- Privacy logging retains structure/SMILES classification history but omits user identity; full anonymization is not guaranteed if logs are publicly exposed.

## Evidence

- [readme] Model layer names verification: "Input layers' names should be "input_2048" and "input_4096" Output layer's name should be "output""
- [readme] Docker and docker-compose requirement: "We typically will deploy this locally. To bring everything up, you need docker and docker-compose."
- [readme] Model format conversion prerequisite: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [readme] Docker network creation step: "If you didn't do it already, you will need a network. docker network create nginx-net"
- [readme] TensorFlow Serving integration: "We pass through tensorflow serving at this url: /model/metadata"
- [readme] REST API classification endpoint with SMILES input: "/classify?smiles=<> You can also provide cached flag to the params to get the cached version so make it faster"
