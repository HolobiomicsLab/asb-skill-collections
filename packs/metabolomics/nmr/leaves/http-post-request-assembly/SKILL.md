---
name: http-post-request-assembly
description: Use when you have NMR peak data (1H and 13C chemical shift values) that must be submitted to a remote DeepSAT SMART 3 classification API for structural prediction, and you need to format the data correctly, validate the endpoint schema, and parse the response to extract predictions and confidence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - tensorflow serving
  - TensorFlow Serving
  - DeepSAT
  techniques:
  - NMR
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

# http-post-request-assembly

## Summary

Construct and execute HTTP POST requests with structured JSON payloads to communicate peak data to a remote classification API endpoint. This skill enables programmatic submission of NMR spectroscopy data (1H and 13C chemical shifts) to obtain machine learning predictions.

## When to use

You have NMR peak data (1H and 13C chemical shift values) that must be submitted to a remote DeepSAT SMART 3 classification API for structural prediction, and you need to format the data correctly, validate the endpoint schema, and parse the response to extract predictions and confidence scores.

## When NOT to use

- Peak data is already in a proprietary binary or compressed format that cannot be serialized to JSON without loss of precision.
- The remote API endpoint is unavailable or does not expose /model/metadata or /api/smart3/search routes.
- Your workflow requires batch processing of millions of peaks and the API does not support streaming or vectorized requests.

## Inputs

- NMR peak data: list of chemical shift measurements (1H and 13C values)
- Model metadata endpoint URL (TensorFlow Serving)
- API endpoint URL (/api/smart3/search)

## Outputs

- HTTP POST request with JSON payload
- Parsed JSON response containing classification predictions
- Confidence scores for each prediction
- Structured log file with request parameters, timestamps, and results

## How to apply

First, retrieve the current model input schema and version from the /model/metadata endpoint via TensorFlow Serving to verify field names and structure have not changed. Then construct a JSON payload as a list of dictionaries, where each dictionary contains 1H and 13C as keys mapped to their corresponding chemical shift values. Execute a POST request to the /api/smart3/search endpoint with this JSON payload as the request body. Validate the HTTP response status code (typically 200 for success) and parse the returned JSON structure to extract classification predictions and associated confidence scores. Log the request parameters, response timestamp, and prediction results to a structured output file for audit and reproducibility.

## Related tools

- **TensorFlow Serving** (Serves the SMART 3 model and exposes /model/metadata endpoint to verify input schema and model version before constructing POST requests)
- **DeepSAT** (Source repository and framework containing the SMART 3 classification API and endpoint implementation) — https://github.com/mwang87__DeepSAT

## Examples

```
import json; import requests; peaks = [{"1H": 7.32, "13C": 128.5}, {"1H": 3.87, "13C": 55.2}]; response = requests.post('http://api.example.com/api/smart3/search', json=peaks); predictions = response.json(); print(predictions)
```

## Evaluation signals

- HTTP response status code is 200 (or other success code defined by the API documentation).
- Returned JSON contains expected keys for predictions and confidence scores; no parsing errors occur.
- Peak data round-trip: 1H and 13C values in the request match the values acknowledged in the response metadata.
- Response timestamp is recorded and is later than the request timestamp by a reasonable margin (< 10 seconds for typical requests).
- Prediction results are non-null and confidence scores fall within the expected range (e.g., 0–1 or 0–100) for the model.

## Limitations

- Model input field names (1H, 13C) may change in future model versions and require code updates to the payload construction logic.
- No changelog is available to track API breaking changes, so version mismatches between the client and deployed model may cause silent failures or schema mismatches.
- The skill assumes peaks can be represented as simple dictionaries; complex peak metadata (e.g., integration, multiplicity, coupling constants) are not supported by the current /api/smart3/search schema.

## Evidence

- [intro] We pass through tensorflow serving at this url: /model/metadata: "We pass through tensorflow serving at this url: /model/metadata"
- [intro] You can put in your peaks as a json list of dicts, with 1H,13C as headers: "You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [intro] Classify programmatically via /api/smart3/search endpoint: "Classify programmatically. You can put in your peaks as a json list of dicts"
- [intro] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
- [discussion] No changelog found for API version tracking: "_No changelog found._"
