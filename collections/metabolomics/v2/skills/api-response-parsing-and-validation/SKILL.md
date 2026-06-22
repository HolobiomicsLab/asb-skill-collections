---
name: api-response-parsing-and-validation
description: Use when after submitting a POST request to the /api/smart3/search endpoint with peak data as a JSON payload, you receive an HTTP response and need to extract classification predictions and confidence scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - tensorflow serving
  - TensorFlow Serving
derived_from:
- doi: 10.1186/s13321-023-00738-4
  title: DeepSAT
evidence_spans:
- We pass through tensorflow serving at this url
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepsat
    doi: 10.1186/s13321-023-00738-4
    title: DeepSAT
  dedup_kept_from: coll_deepsat
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-023-00738-4
  all_source_dois:
  - 10.1186/s13321-023-00738-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# api-response-parsing-and-validation

## Summary

Parse and validate JSON responses from the DeepSAT SMART 3 classification API to extract predictions and confidence scores. This skill ensures that API responses conform to the expected schema and that prediction results are reliably captured for downstream analysis or logging.

## When to use

After submitting a POST request to the /api/smart3/search endpoint with peak data as a JSON payload, you receive an HTTP response and need to extract classification predictions and confidence scores. Use this skill when the response structure must be validated against the model's output schema before interpretation.

## When NOT to use

- The API request has not yet been submitted or no response has been received
- The response format is not JSON (e.g., plain text error or HTML error page)
- Model metadata from /model/metadata endpoint has not been retrieved to establish baseline schema expectations

## Inputs

- HTTP response object from POST request to /api/smart3/search
- Expected response schema from model metadata endpoint
- HTTP status code

## Outputs

- Parsed JSON structure containing classification predictions
- Confidence scores for each prediction
- Structured log file with request parameters, response timestamp, and results

## How to apply

Upon receipt of an HTTP response from /api/smart3/search, first validate the HTTP status code to confirm successful submission. Parse the returned JSON structure to identify the prediction results and associated confidence scores. Verify that the response contains the expected keys and data types as specified in the model metadata retrieved from /model/metadata. Extract classification predictions and confidence scores into structured fields. Log the request parameters, response timestamp, and parsed prediction results to a structured output file for auditability and debugging.

## Related tools

- **TensorFlow Serving** (Provides model metadata endpoint (/model/metadata) to verify current input/output schema and model version prior to response validation)

## Examples

```
import json; import requests; response = requests.post('http://api/api/smart3/search', json=peaks_payload); assert response.status_code == 200; predictions = response.json(); print(f'Predictions: {predictions["classifications"]}')
```

## Evaluation signals

- HTTP response status code is 200 or other expected success code (not 4xx or 5xx)
- Parsed JSON response contains all expected keys matching the schema from /model/metadata endpoint
- Classification predictions and confidence scores are present and of correct data type (string/float or as specified)
- Confidence scores fall within expected range (typically 0–1 for probability-based models)
- Structured log file is created and contains all request parameters, response timestamp, and prediction results with no missing fields

## Limitations

- Model input names and output schema may change between model versions; code updates may be required if the schema changes without backward compatibility
- No changelog is available to track schema changes across model versions, increasing risk of silent failure if response structure evolves
- HTTP status code validation alone does not guarantee the response JSON is valid or contains expected prediction fields; schema validation must be performed independently
- Confidence scores and prediction format depend on the specific model version; different versions may return different structures

## Evidence

- [intro] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
- [intro] Validate HTTP response status and parse returned JSON to extract predictions and confidence: "Validate the HTTP response status code and parse the returned JSON structure to extract classification predictions and confidence scores."
- [intro] Log request parameters and prediction results: "Log the request parameters, response timestamp, and prediction results to a structured output file."
- [intro] Check model metadata via TensorFlow Serving: "Retrieve model metadata from the /model/metadata endpoint via TensorFlow Serving to verify current input schema and model version."
