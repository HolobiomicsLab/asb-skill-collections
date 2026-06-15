---
name: rest-api-endpoint-querying
description: Use when you need to programmatically retrieve model metadata or submit data to a service endpoint when direct file-based access is unavailable or when the service exposes a published HTTP API contract. This is particularly relevant when model input specifications (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3361
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepsat
    doi: 10.1186/s13321-023-00738-4
    title: DeepSAT
  dedup_kept_from: coll_deepsat
schema_version: 0.2.0
---

# REST API endpoint querying

## Summary

Query a REST API endpoint to retrieve and validate structured metadata or classification results, typically by constructing HTTP requests, parsing JSON responses, and verifying response schema compliance.

## When to use

You need to programmatically retrieve model metadata or submit data to a service endpoint when direct file-based access is unavailable or when the service exposes a published HTTP API contract. This is particularly relevant when model input specifications (e.g., expected spectroscopic headers) may change and must be validated before use.

## When NOT to use

- Model metadata is embedded in local configuration files or code comments and does not require live service validation.
- The endpoint is unavailable or unreliable; use cached or hardcoded metadata instead.
- Input schema is guaranteed static by design and does not require runtime verification.

## Inputs

- HTTP endpoint URL (e.g., TensorFlow Serving instance with /model/metadata or /api/smart3/search paths)
- Model instance identifier or name
- Optional: JSON payload (for POST/classification requests; e.g., peaks as list of dicts with 1H,13C headers)

## Outputs

- Parsed JSON response containing model metadata (signature, input names, output schema)
- Validation report (boolean or structured status indicating schema compliance)
- Extracted input/output field names suitable for code generation or runtime binding

## How to apply

Construct an HTTP GET request to the target endpoint (e.g., /model/metadata for TensorFlow Serving instances). Execute the request and retrieve the JSON response. Parse the JSON to extract required fields (e.g., signature, inputs, outputs) that define the API contract. Validate that the response structure matches expectations—for SMART 3, this means confirming the presence of model input names such as '1H' and '13C' headers. Write extracted metadata and validation status to structured output (e.g., JSON) for downstream use or code generation.

## Related tools

- **TensorFlow Serving** (HTTP service providing model metadata and inference endpoints; queried via GET to /model/metadata to retrieve input/output schema)

## Evaluation signals

- HTTP response status code is 200 (success) and response is valid JSON.
- Parsed JSON contains all required top-level fields: 'signature', 'inputs', 'outputs' matching the API contract.
- Extracted input field names (e.g., '1H', '13C') are non-empty and match expected spectroscopic conventions for the SMART 3 model.
- Validation report is generated and written to output JSON without exceptions.
- Changes to model input names are detected and flagged for code update review.

## Limitations

- Model input names may change and require corresponding code updates; this skill detects the change but does not automate code generation.
- No changelog is available in the source repository to track historical changes to the API contract.
- Network availability and endpoint stability are prerequisites; transient service outages will cause validation to fail.
- The skill assumes the endpoint returns well-formed JSON; malformed or non-JSON responses will cause parsing to fail.

## Evidence

- [intro] HTTP GET call to the /model/metadata endpoint on a TensorFlow Serving instance: "queries model metadata via an HTTP GET call to the /model/metadata endpoint on a TensorFlow Serving instance"
- [intro] Model input names must be extracted and verified; changes require code updates: "model input names must be extracted and verified, as changes to these input names require corresponding code updates"
- [intro] Expected input headers are '1H' and '13C': "Classify programmatically. You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [intro] Response must contain required fields (signature, inputs, outputs): "Validate that the response contains required fields (signature, inputs, outputs) matching the expected API contract"
- [intro] TensorFlow Serving instance location mentioned in intro: "We pass through tensorflow serving at this url: /model/metadata"
