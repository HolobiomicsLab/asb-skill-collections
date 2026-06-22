---
name: restful-api-endpoint-invocation
description: Use when you have NMR peak data (1H and 13C chemical shift values) and need to obtain SMART 3 classification predictions from the DeepSAT service.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - tensorflow serving
  - TensorFlow Serving
  - DeepSAT
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
---

# RESTful API endpoint invocation

## Summary

Submit structured peak data (chemical shifts) to a remote classification API endpoint and parse the returned predictions and confidence scores. This skill enables programmatic access to machine-learning-based spectral classification without local model deployment.

## When to use

You have NMR peak data (1H and 13C chemical shift values) and need to obtain SMART 3 classification predictions from the DeepSAT service. Use this skill when you want to avoid local TensorFlow model management and instead leverage a deployed API endpoint that handles versioning and model updates transparently.

## When NOT to use

- Input peaks are not in 1H and 13C format or lack required chemical shift headers
- The DeepSAT API endpoint is unavailable or unresponsive
- You require real-time, ultra-low-latency predictions (API calls incur network overhead)

## Inputs

- JSON list of dictionaries with 1H and 13C peak keys and chemical shift values
- Model metadata retrieved from /model/metadata endpoint

## Outputs

- JSON response containing classification predictions
- Confidence scores for each prediction
- Structured log file with request parameters, timestamp, and results

## How to apply

First, query the /model/metadata endpoint via TensorFlow Serving to confirm the current input schema and model version, since model input names may change and require code updates. Construct a JSON payload as a list of dictionaries, where each dictionary contains 1H and 13C as keys with corresponding chemical shift values. Execute a POST request to the /api/smart3/search endpoint with this JSON payload as the request body. Validate the HTTP response status code and parse the returned JSON structure to extract classification predictions and their associated confidence scores. Log the request parameters, response timestamp, and prediction results to a structured output file for audit and reproducibility.

## Related tools

- **TensorFlow Serving** (Hosts the /model/metadata endpoint to retrieve current input schema and model version; serves the underlying SMART 3 classification model)
- **DeepSAT** (Provides the /api/smart3/search REST endpoint for programmatic spectral classification via peak submission) — https://github.com/mwang87/DeepSAT

## Examples

```
import requests; peaks = [{'1H': 7.25, '13C': 128.5}, {'1H': 3.45, '13C': 65.3}]; response = requests.post('http://api.deepsat.example.com/api/smart3/search', json=peaks); print(response.json())
```

## Evaluation signals

- HTTP response status code is 200 (or other expected success code) and response body is valid JSON
- Returned JSON contains expected classification prediction keys and confidence score values within valid numeric ranges (e.g., 0–1 for probabilities)
- Request payload matches the schema confirmed by /model/metadata (1H and 13C keys present)
- Structured log file is created and contains non-empty request parameters, ISO-formatted timestamp, and prediction results
- Model version in /model/metadata response matches the expected version documented for this analysis

## Limitations

- Model input names may change; code must be updated if /model/metadata schema changes
- No changelog is maintained, making it difficult to track model version updates and breaking changes
- API endpoint availability and latency depend on remote service uptime
- Requires network connectivity; offline classification is not possible with this approach

## Evidence

- [intro] We pass through tensorflow serving at this url: /model/metadata: "We pass through tensorflow serving at this url: /model/metadata"
- [intro] You can put in your peaks as a json list of dicts, with 1H,13C as headers: "You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [intro] Classify programmatically. You can put in your peaks as a json list of dicts: "Classify programmatically. You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [intro] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
- [discussion] Source: github:mwang87__DeepSAT: "github:mwang87__DeepSAT"
