---
name: model-metadata-schema-verification
description: Use when before submitting peak data or other inputs to a machine learning classification API for the first time, after a model update, or if you encounter unexpected prediction errors. It is essential when the underlying model's input names or structure may change and require code updates.
license: CC-BY-4.0
metadata:
  edam_topics: []
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
---

# model-metadata-schema-verification

## Summary

Verify the input schema and model version of a deployed machine learning model by querying its metadata endpoint before constructing and submitting prediction requests. This skill ensures that your request payload matches the model's current input specification, preventing schema mismatch errors and outdated code.

## When to use

Apply this skill before submitting peak data or other inputs to a machine learning classification API for the first time, after a model update, or if you encounter unexpected prediction errors. It is essential when the underlying model's input names or structure may change and require code updates.

## When NOT to use

- The model schema is already documented and confirmed to be static in your deployment.
- You are working with a local, non-updated model artifact where the schema is hardcoded and never changes.

## Inputs

- Model metadata endpoint URL (typically /model/metadata on TensorFlow Serving)
- HTTP client or SDK configured to query the TensorFlow Serving instance

## Outputs

- Parsed JSON metadata object containing model name, version, and input schema
- Validated field names and data types (e.g., '1H', '13C' as keys for peak dictionaries)

## How to apply

Query the /model/metadata endpoint via TensorFlow Serving to retrieve the current model version and input schema (e.g., expected field names such as '1H' and '13C' for NMR peak data). Parse the returned JSON metadata to confirm that the field names and data types match your intended request payload. If discrepancies are found, update your payload construction logic before submitting any classification requests. This prevalidation step prevents silent failures and ensures compatibility with the deployed model version.

## Related tools

- **TensorFlow Serving** (Provides the /model/metadata endpoint to retrieve and verify current model input schema and version before classification requests)

## Evaluation signals

- HTTP response status code is 200 and returns valid JSON metadata.
- Returned metadata contains 'model_spec' and input schema information with expected field names (e.g., '1H', '13C').
- Model version in metadata matches the version you intend to use for downstream predictions.
- Field names and data types in metadata align with the keys and value types in your planned JSON payload.
- Subsequent POST requests to /api/smart3/search execute without schema validation errors.

## Limitations

- Metadata endpoint availability depends on TensorFlow Serving uptime; if unavailable, you cannot verify the schema before submission.
- The metadata endpoint may not return human-readable documentation of the expected value ranges or units for each field.
- Metadata verification does not guarantee that the model's predictions will be accurate or meaningful for your specific data; it only confirms structural compatibility.

## Evidence

- [intro] Model input names may change and require code updates: "If the model input names change, then we need to change it in the code"
- [intro] Check model metadata via /model/metadata endpoint: "We pass through tensorflow serving at this url: /model/metadata"
- [intro] Expected peak data format with 1H and 13C headers: "You can put in your peaks as a json list of dicts, with 1H,13C as headers"
