---
name: rest-api-endpoint-construction
description: Use when you have pre-trained neural network models (e.g., Keras/TensorFlow) for chemical classification and need to expose them as a queryable HTTP service.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3664
  edam_topics:
  - http://edamontology.org/topic_3372
  tools:
  - Python
  - docker
  - docker-compose
  - TensorFlow Serving
  - TensorFlow 2.3.0
  - Keras
  - mwang87/NP-Classifier
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
---

# rest-api-endpoint-construction

## Summary

Design and implement a REST API endpoint that accepts structured chemical input (SMILES strings) and routes predictions through a containerized machine learning service, optionally with caching for repeated queries. This skill applies when you need to operationalize trained neural network models as web services with query parameter parsing and performance optimization.

## When to use

You have pre-trained neural network models (e.g., Keras/TensorFlow) for chemical classification and need to expose them as a queryable HTTP service. The trigger is typically: (1) you have SMILES strings or other serialized chemical structures to classify in bulk or on-demand, (2) you want to serve predictions from a containerized environment, and (3) you want to optimize repeated queries via caching rather than re-computing identical predictions.

## When NOT to use

- Model input/output layer names do not conform to the expected schema ('input_2048', 'input_4096', 'output') — first rename or retrain.
- You are not using Keras or TensorFlow 2.3.0 — model conversion will fail or produce incompatible HDF5 files.
- Input is already a pre-computed feature table or embedding — skip endpoint construction and serve table lookups instead.

## Inputs

- Pre-trained Keras neural network model files (HDF5 format)
- SMILES strings (query parameter: ?smiles=<structure>)
- Optional cached flag parameter (?cached=true)

## Outputs

- Natural product classification predictions (from 'output' layer)
- HTTP response with classification result
- Cached classification result (on repeat query with cached flag)

## How to apply

First, verify your model's input and output layer names match the service expectation ('input_2048' and 'input_4096' for inputs, 'output' for the classification output). Convert Keras models to HDF5 TensorFlow 2.3.0 format using Python and TensorFlow. Set up a Docker network (e.g., nginx-net) to isolate containerized services. Build the API server via docker-compose, configuring the /classify endpoint to parse the SMILES query parameter and optional cached flag parameter. Route parsed SMILES strings through TensorFlow Serving at the /model/metadata endpoint to retrieve predictions. Implement caching logic in the endpoint handler to store prior classification results and return them on repeat queries. Test by issuing repeated requests with identical SMILES and verifying cached responses are returned without re-inference.

## Related tools

- **docker** (Containerize the API server and isolate service dependencies)
- **docker-compose** (Orchestrate multi-container deployment of API and TensorFlow Serving)
- **TensorFlow Serving** (Serve model inference via /model/metadata endpoint and route predictions)
- **TensorFlow 2.3.0** (Convert Keras models to HDF5 TF2 format for compatibility with Serving)
- **Keras** (Define and load pre-trained neural network models for classification)
- **Python** (Implement endpoint handler logic, caching, and model conversion scripts)
- **mwang87/NP-Classifier** (Reference implementation of /classify endpoint for natural product SMILES classification) — https://github.com/mwang87/NP-Classifier

## Examples

```
curl 'http://localhost:8080/classify?smiles=CC(=O)Oc1ccccc1C(=O)O&cached=true'
```

## Evaluation signals

- Endpoint accepts SMILES query parameter and returns a JSON response with classification output without error
- TensorFlow Serving /model/metadata endpoint is accessible and returns layer names matching 'input_2048', 'input_4096', 'output'
- Repeated queries with identical SMILES strings return identical cached results when cached flag is set, faster than initial inference
- Docker network (nginx-net) is created and running, and containers communicate without network errors
- Sample SMILES strings (e.g., from the NP Classifier repo) produce consistent, human-interpretable natural product classifications

## Limitations

- Model conversion to HDF5 TF2 requires TensorFlow 2.3.0 exactly; other versions may produce incompatible serializations.
- Input and output layer names must be manually verified and aligned; mismatches will cause prediction routing to fail silently or raise runtime errors.
- Caching is in-memory or requires external persistence (not specified in the README); cache invalidation policy is not documented.
- Privacy implications: the service logs classified SMILES structures (but not user identity per the README privacy statement), which may be sensitive for confidential chemical discovery workflows.
- No changelog or versioning found; endpoint contract stability across repository updates is unclear.

## Evidence

- [readme] Input layer names and output layer verification: "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [readme] Endpoint accepts SMILES strings and optional cached parameter: "/classify?smiles=<>

You can also provide cached flag to the params to get the cached version so make it faster"
- [readme] Docker containerization requirement: "To bring everything up, you need docker and docker-compose."
- [readme] TensorFlow model conversion step: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [readme] TensorFlow Serving routing for predictions: "We pass through tensorflow serving at this url:

```/model/metadata```"
- [readme] Docker network setup for service communication: "docker network create nginx-net"
