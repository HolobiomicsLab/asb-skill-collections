---
name: json-response-parsing
description: Use when when querying a TensorFlow Serving metadata endpoint or similar REST API that returns JSON-formatted model metadata, and you need to programmatically extract and validate input/output layer names against known specifications (e.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_3473
  tools:
  - Python
  - TensorFlow Serving
  - docker-compose
  - tensorflow serving
derived_from:
- doi: 10.1021/jacs.9b13786
  title: CSCS / deep CNN natural-product annotation
- doi: 10.1186/s13321-023-00738-4
  title: ''
evidence_spans:
- Make sure you have python installed
- We pass through tensorflow serving at this url
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_classyfire_cq
    doi: 10.1186/s13321-016-0174-y
    title: ClassyFire
  - build: coll_cscs_deep_cnn_natural_product_annotation_cq
    doi: 10.1021/jacs.9b13786
    title: CSCS / deep CNN natural-product annotation
  - build: coll_deepsat
    doi: 10.1186/s13321-023-00738-4
    title: DeepSAT
  dedup_kept_from: coll_cscs_deep_cnn_natural_product_annotation_cq
schema_version: 0.2.0
---

# JSON Response Parsing

## Summary

Extract and validate structured metadata from JSON responses returned by service endpoints (e.g., TensorFlow Serving /model/metadata). This skill is essential when deploying machine learning models through containerized services and need to verify that model layer names and signatures match expected specifications.

## When to use

When querying a TensorFlow Serving metadata endpoint or similar REST API that returns JSON-formatted model metadata, and you need to programmatically extract and validate input/output layer names against known specifications (e.g., confirming 'input_2048', 'input_4096', and 'output' layer names before sending inference requests).

## When NOT to use

- The service endpoint is not available or the network request fails before receiving a JSON response
- The response is not valid JSON (e.g., plain text error message, HTML error page, malformed XML)
- Layer names are already known and pre-validated from a prior successful query in the same deployment session

## Inputs

- JSON HTTP response body from TensorFlow Serving /model/metadata endpoint
- Expected layer name specifications (e.g., input_2048, input_4096, output)

## Outputs

- Parsed Python dictionary/object containing model metadata
- List of extracted input layer names
- Extracted output layer name
- Verification report documenting validation outcome (pass/fail)

## How to apply

Send a GET request to the service metadata endpoint (e.g., http://localhost:8501/v1/models/<model_name>/metadata via TensorFlow Serving). Parse the returned JSON response using a JSON parser (Python's json library or equivalent). Extract the input layer names and output layer name from the parsed object. Compare the extracted names against the expected specification ('input_2048', 'input_4096' for inputs, 'output' for output). Document any mismatches in a verification report. If names differ from specification, flag this as requiring code updates before inference can proceed.

## Related tools

- **TensorFlow Serving** (REST API service exposing /model/metadata endpoint that returns model metadata as JSON)
- **Python** (Language used to send HTTP GET requests and parse JSON response using standard library (json module, requests library))
- **docker-compose** (Brings up TensorFlow Serving container exposing the metadata endpoint)

## Examples

```
import requests, json; resp = requests.get('http://localhost:8501/v1/models/np_classifier/metadata'); metadata = resp.json(); inputs = metadata.get('inputs', []); outputs = metadata.get('outputs', []); print(f"Input layers: {inputs}, Output layers: {outputs}")
```

## Evaluation signals

- JSON response parses without error (no malformed JSON exception)
- Extracted input layer names match exactly the expected values 'input_2048' and 'input_4096'
- Extracted output layer name matches exactly the expected value 'output'
- Verification report is generated documenting the metadata query result and layer name validation outcome
- If layer names do not match specification, a warning or error flag is set indicating code updates are required

## Limitations

- The skill assumes the TensorFlow Serving endpoint is running and accessible at the specified URL; network timeouts or service unavailability will cause the query to fail
- The skill depends on the JSON response structure remaining consistent with TensorFlow Serving's metadata endpoint schema; changes to that schema would require adaptation
- Layer names must be validated exactly as strings; no fuzzy matching or partial name validation is performed

## Evidence

- [other] Send a GET request to the TensorFlow Serving /model/metadata endpoint (typically http://localhost:8501/v1/models/<model_name>/metadata). Parse the JSON response to extract input layer names and output layer name.: "Send a GET request to the TensorFlow Serving /model/metadata endpoint (typically http://localhost:8501/v1/models/<model_name>/metadata). Parse the JSON response to extract input layer names and"
- [other] Validate that the input layers are exactly 'input_2048' and 'input_4096' and output layer is exactly 'output'. Generate a verification report documenting the metadata query result and layer name validation outcome.: "Validate that the input layers are exactly 'input_2048' and 'input_4096' and output layer is exactly 'output'. Generate a verification report documenting the metadata query result and layer name"
- [readme] We pass through tensorflow serving at this url: /model/metadata. If the model input names change, then we need to change it in the code: "We pass through tensorflow serving at this url: /model/metadata. If the model input names change, then we need to change it in the code"
- [readme] Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output": "Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output""
