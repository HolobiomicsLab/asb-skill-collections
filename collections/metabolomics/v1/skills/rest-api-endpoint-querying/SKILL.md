---
name: rest-api-endpoint-querying
description: Use when you have a SMILES string or batch of SMILES strings representing chemical structures and need to obtain NP Classifier predictions programmatically.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3346
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  tools:
  - Python
  - Docker
  - Docker Compose
  - TensorFlow Serving
  - NP-Classifier
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- Make sure you have python installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepsat
    doi: 10.1186/s13321-023-00738-4
    title: DeepSAT
  - build: coll_npclassifier
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  dedup_kept_from: coll_npclassifier
schema_version: 0.2.0
---

# rest-api-endpoint-querying

## Summary

Query a deployed REST API endpoint to submit structured chemical data (SMILES strings) for programmatic classification and retrieve JSON-formatted predictions. This skill enables high-throughput molecular structure classification without manual web interface interaction.

## When to use

You have a SMILES string or batch of SMILES strings representing chemical structures and need to obtain NP Classifier predictions programmatically. Use this skill when you require reproducible, automatable access to the classifier's output rather than interactive web submission, or when integrating classification into a larger computational pipeline.

## When NOT to use

- You do not have a SMILES string or other structured chemical input; the endpoint requires valid molecular notation.
- The NP Classifier Docker services are not running or the network (nginx-net) has not been created and initialized.
- You need batch classification of many thousands of structures and require synchronous responses; consider asynchronous job submission if available.

## Inputs

- SMILES string (valid chemical structure notation)
- HTTP GET request parameters (smiles, optional: cached flag)

## Outputs

- JSON response object containing classification output
- HTTP status code (200 for success)
- Model layer metadata (input_2048, input_4096, output layer names)

## How to apply

First, ensure the NP Classifier Docker services (server and TensorFlow Serving) are running via docker-compose. Construct an HTTP GET request to the /classify endpoint, passing your SMILES string as a query parameter. Send the request and capture the returned JSON response. Validate that the HTTP status code is 200 and inspect the JSON structure to confirm the presence of the 'output' field and metadata indicating successful model invocation. Optionally, append a cached flag parameter to retrieve pre-cached results for faster repeated queries on the same structure.

## Related tools

- **Docker** (Container runtime for deploying and managing NP Classifier server and TensorFlow Serving services)
- **Docker Compose** (Orchestration tool for coordinating multi-container NP Classifier deployment (make server-compose))
- **TensorFlow Serving** (Model serving backend that handles inference requests and exposes /model/metadata endpoint for layer name verification)
- **NP-Classifier** (Core classification model and API server providing /classify and /model/metadata endpoints) — https://github.com/mwang87/NP-Classifier

## Examples

```
curl -X GET 'http://localhost:5000/classify?smiles=CC(=O)Oc1ccccc1C(=O)O' -H 'Content-Type: application/json'
```

## Evaluation signals

- HTTP response status code equals 200, indicating successful endpoint contact and request processing.
- Returned JSON is well-formed and contains the mandatory 'output' field with classification predictions.
- Response metadata or schema confirms the presence of expected input layer names 'input_2048' and 'input_4096' and output layer name 'output' (verifiable via /model/metadata endpoint).
- SMILES input is reflected or acknowledged in the response, confirming the correct structure was classified.
- Response time is reasonable (< 5 seconds for single queries, faster for cached queries indicated by cached flag parameter).

## Limitations

- The endpoint requires valid SMILES strings; malformed or invalid chemical notation will result in error or unexpected output.
- Input layer names are hardcoded in the NP Classifier codebase ('input_2048' and 'input_4096'); any model updates that change these names require code modifications.
- Privacy: the service logs queried structures but not user identity, so repeated large-scale queries may be recorded in server logs.
- Single synchronous requests block until the TensorFlow Serving backend completes inference; very high query rates may saturate the service.

## Evidence

- [other] Does the /classify API endpoint accept a SMILES string parameter and return a properly structured classification response?: "The NP Classifier provides a /classify API endpoint that accepts SMILES strings as query parameters for programmatic classification requests."
- [other] Workflow for REST endpoint querying: "Construct an HTTP GET request to the /classify endpoint with a valid SMILES string parameter. Send the request and capture the JSON response. Validate the response structure contains the expected"
- [readme] Required deployment infrastructure: "We typically will deploy this locally. To bring everything up, you need docker and docker-compose."
- [readme] Layer name specification: "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [readme] API endpoint syntax: "Classify programmatically 

```/classify?smiles=<>```

You can also provide cached flag to the params to get the cached version so make it faster"
- [readme] TensorFlow Serving routing: "We pass through tensorflow serving at this url:

```/model/metadata```"
