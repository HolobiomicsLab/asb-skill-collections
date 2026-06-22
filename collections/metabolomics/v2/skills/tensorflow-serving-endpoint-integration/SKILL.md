---
name: tensorflow-serving-endpoint-integration
description: Use when you have nuclear magnetic resonance (NMR) peak data (1H and 13C measurements) that you need to classify using a deployed SMART 3 model, and you want to submit peaks programmatically rather than through a web UI.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - TensorFlow Serving
  - DeepSAT
derived_from:
- doi: 10.1186/s13321-023-00738-4
  title: DeepSAT
evidence_spans:
- We pass through tensorflow serving at this url
- 'We pass through tensorflow serving at this url:'
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

# tensorflow-serving-endpoint-integration

## Summary

Integrate with a TensorFlow Serving inference endpoint to programmatically submit nuclear magnetic resonance peak data for molecular classification. This skill enables automated classification workflows by querying model metadata and invoking the classification API with properly formatted NMR peak payloads.

## When to use

You have nuclear magnetic resonance (NMR) peak data (1H and 13C measurements) that you need to classify using a deployed SMART 3 model, and you want to submit peaks programmatically rather than through a web UI. Use this skill when integrating NMR classification into an automated pipeline or batch processing workflow.

## When NOT to use

- Your NMR peak data is not yet structured or validated—preprocess and validate peaks before submitting.
- The model input/output schema names are hardcoded in your application—use this skill only if you can dynamically query and adapt to schema changes.
- You are working with a different spectroscopy format (e.g., mass spectrometry, IR) that does not conform to 1H/13C NMR peak dictionaries.

## Inputs

- NMR peak data as JSON list of dictionaries with '1H' and '13C' keys
- TensorFlow Serving model metadata endpoint URL
- SMART 3 classification endpoint URL (/api/smart3/search)

## Outputs

- Structured JSON classification response containing molecular classification results
- Model input/output schema metadata (from /model/metadata)

## How to apply

First, query the TensorFlow Serving /model/metadata endpoint to retrieve the current model's input and output schema names, since these may change across model versions and require code updates. Next, format your NMR peak data as a JSON list of dictionaries with '1H' and '13C' keys representing the respective peak measurements. Construct a POST request to the /api/smart3/search endpoint with this formatted peaks payload. Send the request through the TensorFlow Serving gateway and parse the returned JSON classification response. Verify that the response structure matches the schema retrieved from metadata to confirm successful integration.

## Related tools

- **TensorFlow Serving** (Serves the SMART 3 deep learning model and exposes /model/metadata and /api/smart3/search endpoints for programmatic inference)
- **DeepSAT** (Source repository containing the SMART 3 classification model and NMR analysis framework) — https://github.com/mwang87/DeepSAT

## Examples

```
import json; import requests; metadata = requests.get('http://tensorflow-serving:8501/v1/models/smart3:metadata').json(); peaks = [{'1H': [7.2, 6.8], '13C': [130.5, 128.3]}]; result = requests.post('http://tensorflow-serving:8501/api/smart3/search', json={'peaks': peaks}).json()
```

## Evaluation signals

- The /model/metadata endpoint returns a valid JSON schema with input and output field names
- The peaks JSON list is accepted without parsing errors by the /api/smart3/search endpoint
- The classification response JSON structure matches the schema fields retrieved from /model/metadata
- Classification results are returned within expected latency and contain non-null molecular identifiers or scores
- Repeated submissions of the same peak data produce deterministic (identical) classification results

## Limitations

- Model input names may change between model versions; code must dynamically query /model/metadata to remain robust
- No versioning or changelog is documented, making it difficult to track breaking changes to the API schema
- The skill assumes peaks are properly formatted as 1H and 13C measurements; malformed or missing keys will cause request failures
- Network latency and TensorFlow Serving availability directly impact integration reliability

## Evidence

- [intro] We pass through tensorflow serving at this url: /model/metadata: "We pass through tensorflow serving at this url: /model/metadata"
- [intro] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
- [intro] You can put in your peaks as a json list of dicts, with 1H,13C as headers: "You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [discussion] Source: github:mwang87__DeepSAT: "Source: github:mwang87__DeepSAT"
- [discussion] No changelog found: "_No changelog found._"
