---
name: http-api-integration-testing
description: Use when you have deployed a microservice (e.g., TensorFlow Serving,
  REST API) and need to verify that specific endpoints (e.g., /model/metadata, /classify)
  return responses with correct schema, field names, and data types before consuming
  them in production workflows or downstream applications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - docker
  - docker-compose
  - TensorFlow Serving
  - curl / HTTP client library
  license_tier: open
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans: []
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

# HTTP API Integration Testing

## Summary

Validate that a running service's HTTP API endpoints return correctly structured responses with expected field values and metadata. This skill is essential for confirming that API contracts (input/output layer names, response schemas) match implementation before downstream integration.

## When to use

You have deployed a microservice (e.g., TensorFlow Serving, REST API) and need to verify that specific endpoints (e.g., /model/metadata, /classify) return responses with correct schema, field names, and data types before consuming them in production workflows or downstream applications.

## When NOT to use

- The API endpoint is already documented and tested in a CI/CD pipeline; this skill is redundant if integration tests already run on every commit.
- The service is a third-party, read-only API with no local deployment; use standard API client libraries and mocking instead.
- The response schema is unstable or intentionally versioned; in that case, use contract testing or API versioning strategies rather than hard-coded field validation.

## Inputs

- Running HTTP service endpoint URL (e.g., http://localhost:8080/model/metadata)
- Expected API response schema or specification (e.g., field names, data types)
- Service deployment configuration (e.g., docker-compose.yml)

## Outputs

- Parsed JSON response object
- Validation report (pass/fail per field)
- JSON response log file (for audit and debugging)
- Boolean success/failure signal for downstream workflow

## How to apply

Start the target service (e.g., via docker-compose), then send HTTP GET or POST requests to the endpoints under test. Parse the JSON response and extract key fields—in the NP-Classifier case, validate that /model/metadata returns input layers named 'input_2048' and 'input_4096' and output layer 'output'. Compare extracted field values against a known specification or schema. Write the full response to a file for logging and future audit. Fail fast if field names or structure do not match expectations, as misalignment indicates either misconfiguration or a breaking API change that must be resolved before proceeding.

## Related tools

- **docker** (Containerize and run the service (e.g., TensorFlow Serving) locally so the HTTP endpoint is accessible for testing.)
- **docker-compose** (Orchestrate multi-container services (NP-Classifier, TensorFlow Serving) and networking for end-to-end integration testing.)
- **TensorFlow Serving** (Serve the trained model and expose the /model/metadata endpoint whose response structure and field names are validated.) — https://github.com/tensorflow/serving
- **curl / HTTP client library** (Send GET/POST requests to the API endpoint and capture the JSON response.)

## Examples

```
curl -X GET http://localhost:8500/v1/models/np_classifier/metadata | jq '.config.input_config, .config.output_config' > metadata_response.json
```

## Evaluation signals

- HTTP response status code is 200 (or expected success code); non-2xx indicates endpoint failure.
- Response is valid JSON and parses without error.
- All required top-level fields are present in the response (schema completeness check).
- Input layer names extracted from response exactly match 'input_2048' and 'input_4096'; output layer name exactly matches 'output' (field value correctness).
- Response can be serialized to a JSON file without truncation or encoding errors (data integrity).

## Limitations

- This skill assumes the service is already running and accessible on the expected host:port; it does not diagnose deployment or network configuration issues.
- Field name validation is case-sensitive and exact-match; if the model or API is updated to rename layers, the test will fail and the validation spec must be updated manually.
- The skill validates response structure and explicit field values but does not test functional correctness (e.g., whether the model actually classifies compounds correctly); use end-to-end testing for that.
- No timeout or retry logic is specified; long-running or flaky endpoints may cause the test to hang or fail intermittently.

## Evidence

- [other] Does the TensorFlow Serving endpoint at /model/metadata successfully return model metadata including the correct input and output layer names when queried on the running Dockerized NP-Classifier server?: "Does the TensorFlow Serving endpoint at /model/metadata successfully return model metadata including the correct input and output layer names"
- [other] The expected model layer names that should be returned by the /model/metadata endpoint are input layers 'input_2048' and 'input_4096', and output layer 'output'.: "The expected model layer names that should be returned by the /model/metadata endpoint are input layers 'input_2048' and 'input_4096', and output layer 'output'."
- [other] Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving container. 3. Parse the JSON response and extract input/output layer name fields. 4. Validate that input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'.: "Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving container. Parse the JSON response and extract input/output layer name fields. Validate that input layers"
- [other] Write the complete metadata response to a JSON file.: "Write the complete metadata response to a JSON file."
- [readme] We pass through tensorflow serving at this url: /model/metadata. If the model input names change, then we need to change it in the code.: "We pass through tensorflow serving at this url: /model/metadata. If the model input names change, then we need to change it in the code."
- [readme] Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output".: "Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output"."
