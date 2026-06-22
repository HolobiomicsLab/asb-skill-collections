---
name: rest-api-endpoint-querying
description: Use when when you need to verify that a deployed model service (such as TensorFlow Serving) is running and exposing the correct input and output layer names before sending classification requests.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_3361
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  tools:
  - Python
  - docker
  - docker-compose
  - TensorFlow Serving
  - tensorflow serving
  - Docker
  - Docker Compose
  - NP-Classifier
derived_from:
- doi: 10.1021/jacs.9b13786
  title: CSCS / deep CNN natural-product annotation
- doi: 10.1186/s13321-023-00738-4
  title: ''
- doi: 10.1021/acs.jnatprod.1c00399
  title: ''
evidence_spans:
- Make sure you have python installed
- We pass through tensorflow serving at this url
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cscs_deep_cnn_natural_product_annotation_cq
    doi: 10.1021/jacs.9b13786
    title: CSCS / deep CNN natural-product annotation
  - build: coll_deepsat
    doi: 10.1186/s13321-023-00738-4
    title: DeepSAT
  - build: coll_npclassifier
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  dedup_kept_from: coll_cscs_deep_cnn_natural_product_annotation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jacs.9b13786
  all_source_dois:
  - 10.1021/jacs.9b13786
  - 10.1186/s13321-023-00738-4
  - 10.1021/acs.jnatprod.1c00399
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# rest-api-endpoint-querying

## Summary

Query a REST API endpoint to retrieve and validate structured metadata from a running service instance. This skill is essential for confirming that deployed models or services expose the correct interface specifications before downstream processing or integration.

## When to use

When you need to verify that a deployed model service (such as TensorFlow Serving) is running and exposing the correct input and output layer names before sending classification requests. Apply this skill after starting a containerized service and before attempting to call inference endpoints.

## When NOT to use

- The service is not yet running or the endpoint is not accessible — start the container first.
- You only need to retrieve inference results without validating layer specifications — use the /classify endpoint instead.
- The model input/output layer names are already known and have not changed from the previous deployment.

## Inputs

- Running TensorFlow Serving instance (via Docker container)
- Service endpoint URL (e.g., http://localhost:8501/v1/models/<model_name>/metadata)
- Expected input and output layer name specifications

## Outputs

- JSON metadata response from the /model/metadata endpoint
- Verification report with extracted layer names and validation outcome (pass/fail)

## How to apply

Start the NP Classifier Docker container using docker-compose, then send a GET request to the TensorFlow Serving /model/metadata endpoint (typically http://localhost:8501/v1/models/<model_name>/metadata). Parse the returned JSON response to extract the 'inputs' and 'outputs' fields. Validate that input layer names are exactly 'input_2048' and 'input_4096' and that the output layer name is exactly 'output'. If any names deviate from these specifications, the inference code must be updated to match the actual layer names exposed by the service. Generate a verification report documenting the metadata query result and the validation outcome (pass/fail).

## Related tools

- **docker** (Start and manage the NP Classifier container)
- **docker-compose** (Orchestrate multi-container deployment of NP Classifier and its dependencies)
- **TensorFlow Serving** (Expose the /model/metadata endpoint that provides input and output layer name specifications)
- **Python** (Parse and validate the JSON metadata response from the endpoint)

## Evaluation signals

- HTTP GET request succeeds with 200 status code and valid JSON response
- Parsed JSON response contains 'inputs' array with exactly two entries: 'input_2048' and 'input_4096'
- Parsed JSON response contains 'outputs' entry with value exactly 'output'
- Verification report is generated and documents match/mismatch against expected layer name specifications
- If any layer names differ from specifications, verification report explicitly flags the discrepancy

## Limitations

- The endpoint returns metadata only; it does not validate that the model will actually process data correctly until inference is tested.
- If model input names change after initial deployment, the discovery process must be re-run; there is no automatic alerting mechanism documented.
- The metadata endpoint is specific to TensorFlow Serving; other model serving frameworks may use different endpoints and response formats.

## Evidence

- [other] Send a GET request to the TensorFlow Serving /model/metadata endpoint (typically http://localhost:8501/v1/models/<model_name>/metadata): "Send a GET request to the TensorFlow Serving /model/metadata endpoint (typically http://localhost:8501/v1/models/<model_name>/metadata)"
- [other] Parse the JSON response to extract input layer names and output layer name: "Parse the JSON response to extract input layer names and output layer name"
- [other] Validate that the input layers are exactly 'input_2048' and 'input_4096' and output layer is exactly 'output': "Validate that the input layers are exactly 'input_2048' and 'input_4096' and output layer is exactly 'output'"
- [other] Generate a verification report documenting the metadata query result and layer name validation outcome: "Generate a verification report documenting the metadata query result and layer name validation outcome"
- [readme] We pass through tensorflow serving at this url: /model/metadata. If the model input names change, then we need to change it in the code: "We pass through tensorflow serving at this url: /model/metadata. If the model input names change, then we need to change it in the code"
- [readme] Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output": "Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output""
