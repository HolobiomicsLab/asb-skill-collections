---
name: model-metadata-schema-inspection
description: Use when when preparing to send peak data (1H and 13C NMR measurements) to a machine learning classification endpoint and you need to verify the current model's input/output names and schema, especially before implementing or updating code that constructs JSON payloads for the /api/smart3/search.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - TensorFlow Serving
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

# model-metadata-schema-inspection

## Summary

Retrieve and inspect the input/output schema and model metadata from a TensorFlow Serving instance to understand required data formats and structure before sending classification requests. This skill ensures programmatic requests are aligned with the current model's expected input signatures.

## When to use

When preparing to send peak data (1H and 13C NMR measurements) to a machine learning classification endpoint and you need to verify the current model's input/output names and schema, especially before implementing or updating code that constructs JSON payloads for the /api/smart3/search endpoint.

## When NOT to use

- The model endpoint is not deployed on TensorFlow Serving (e.g., a native REST API that does not expose /model/metadata).
- You have already verified the schema within the same session and the model has not been redeployed.
- Peak data is already formatted and validated against a frozen, versioned schema specification that is guaranteed not to change.

## Inputs

- TensorFlow Serving instance URL
- Model name (e.g. 'smart3')
- Model version (optional; defaults to latest)

## Outputs

- Model metadata JSON object containing input/output tensor names, data types, and shapes
- Schema validation report (pass/fail confirmation against planned peak data format)

## How to apply

Query the TensorFlow Serving /model/metadata endpoint to retrieve the current model's input and output names, data types, and tensor shapes. Parse the returned metadata JSON to extract the exact field names and structure required by the model. Compare the metadata against your planned JSON request payload (a list of dictionaries with 1H and 13C NMR peak headers) to ensure field names and formats match. If model input names differ from your code, update the request handler to map your peak data to the correct tensor names. This step guards against silent failures caused by schema drift between model versions.

## Related tools

- **TensorFlow Serving** (Exposes the /model/metadata endpoint to retrieve and inspect current model input/output schema; serves the /api/smart3/search classification endpoint)

## Examples

```
curl -X GET http://localhost:8501/v1/models/smart3/metadata | jq '.model_spec, .metadata.signature_def'
```

## Evaluation signals

- HTTP 200 response received from /model/metadata endpoint with valid JSON structure
- Returned metadata contains 'inputs' and 'outputs' fields with tensor names, shapes, and data types
- Input tensor names match the expected field names in your JSON peak payload (e.g., '1H' and '13C' keys)
- Schema validation confirms that your peak data list-of-dicts format maps to the required input tensor structure without field name mismatches
- No code modifications are needed, or required changes to field mapping are identified and documented before sending requests

## Limitations

- Model input names may change between model versions or redeployments, requiring code updates to maintain compatibility.
- No changelog is available to track when schema changes occur, so schema drift may only be detected at runtime.
- The /model/metadata endpoint may not be enabled or accessible on all TensorFlow Serving deployments depending on configuration.

## Evidence

- [intro] Query the TensorFlow Serving /model/metadata endpoint to retrieve current model input/output names and schema.: "Query the TensorFlow Serving /model/metadata endpoint to retrieve current model input/output names and schema."
- [intro] If the model input names change, then we need to change it in the code.: "If the model input names change, then we need to change it in the code"
- [intro] We pass through tensorflow serving at this url: /model/metadata: "We pass through tensorflow serving at this url: /model/metadata"
- [intro] You can put in your peaks as a json list of dicts, with 1H,13C as headers.: "You can put in your peaks as a json list of dicts, with 1H,13C as headers"
