---
name: api-request-response-handling
description: Use when you have nuclear magnetic resonance (NMR) peak data (proton 1H and carbon-13 13C measurements) that you need to classify using a deployed deep learning model, and you have access to a TensorFlow Serving instance running the SMART 3 classification model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - TensorFlow Serving
  - DeepSAT
derived_from:
- doi: 10.1186/s13321-023-00738-4
  title: DeepSAT
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepsat_cq
    doi: 10.1186/s13321-023-00738-4
    title: DeepSAT
  dedup_kept_from: coll_deepsat_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-023-00738-4
  all_source_dois:
  - 10.1186/s13321-023-00738-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# api-request-response-handling

## Summary

Construct and submit programmatic requests to a TensorFlow Serving classification endpoint, formatting NMR peak data as JSON and parsing the structured response. This skill bridges raw spectroscopic measurements to machine-learning-backed molecular classification by managing endpoint schema, request serialization, and response deserialization.

## When to use

Use this skill when you have nuclear magnetic resonance (NMR) peak data (proton 1H and carbon-13 13C measurements) that you need to classify using a deployed deep learning model, and you have access to a TensorFlow Serving instance running the SMART 3 classification model.

## When NOT to use

- The SMART 3 model service is offline or the /model/metadata endpoint is unreachable.
- Your NMR data lacks both proton (1H) and carbon-13 (13C) peak information; the endpoint expects both headers.
- You have already-classified molecules and do not need inference; this skill performs inference, not validation or re-ranking.

## Inputs

- NMR peak data as list of dictionaries with '1H' and '13C' keys
- TensorFlow Serving endpoint URL and model name

## Outputs

- JSON-structured classification response
- Molecular identifiers and scores from the SMART 3 model

## How to apply

First, query the TensorFlow Serving /model/metadata endpoint to retrieve the current model's input and output schema names, since model input names may change and require code updates. Second, format your NMR peaks as a JSON list of dictionaries with '1H' and '13C' keys representing proton and carbon-13 chemical shifts. Third, construct a POST request to the /api/smart3/search endpoint with the formatted peaks payload. Finally, parse the returned JSON classification response and extract the structured result (molecular identifiers, confidence scores, or other model outputs). The rationale is that programmatic access decouples data acquisition from model inference, allowing batch processing and integration into larger workflows without manual intervention.

## Related tools

- **TensorFlow Serving** (Hosts and serves the SMART 3 classification model; provides /model/metadata and /api/smart3/search endpoints for schema inspection and inference.)
- **DeepSAT** (Source repository containing model training and endpoint implementation logic for NMR-based molecular classification.) — https://github.com/mwang87/DeepSAT

## Examples

```
import json; import requests; metadata = requests.get('http://localhost:8501/v1/models/smart3:metadata').json(); peaks = [{'1H': 7.3, '13C': 128.5}, {'1H': 2.1, '13C': 20.3}]; response = requests.post('http://localhost:8501/v1/models/smart3:predict', json={'instances': [peaks]}); classification = response.json()
```

## Evaluation signals

- HTTP response status is 200; no connection or authentication errors are returned from the endpoint.
- Returned JSON response contains expected classification fields (e.g., molecular identifiers, scores); schema matches the /model/metadata output definition.
- Peak data is accepted without validation errors; JSON list of dicts with '1H' and '13C' keys passes the endpoint's input schema.
- Model input names in your code match those retrieved from /model/metadata; no mismatch errors occur on inference.
- Response latency and throughput are consistent; batch requests process without timeout or out-of-memory failures.

## Limitations

- Model input names may change in future model updates; the /model/metadata endpoint must be queried dynamically rather than hard-coded to remain forward-compatible.
- No official changelog is available, so breaking changes to the endpoint schema may not be advertised; monitoring the /model/metadata response is essential.
- The endpoint accepts only NMR peak data in the specified JSON format; other spectroscopic formats (e.g., mass spectrometry) or alternative NMR representations (e.g., raw binary spectra) are not supported.

## Evidence

- [other] Query the TensorFlow Serving /model/metadata endpoint to retrieve current model input/output names and schema: "Query the TensorFlow Serving /model/metadata endpoint to retrieve current model input/output names and schema."
- [intro] Accept peaks formatted as a list of dicts with '1H' and '13C' keys: "You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [intro] If the model input names change, code updates are required: "If the model input names change, then we need to change it in the code"
- [other] Request is sent to /api/smart3/search endpoint with formatted peaks payload: "Construct and send the classification request to the TensorFlow Serving /api/smart3/search endpoint with the formatted peaks payload."
- [other] Parse the classification response and return as structured JSON: "Parse the classification response and return the structured result as JSON."
