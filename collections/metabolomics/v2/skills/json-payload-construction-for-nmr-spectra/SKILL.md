---
name: json-payload-construction-for-nmr-spectra
description: Use when when you have NMR peak assignments (1H and 13C chemical shift values) and need to submit them to the /api/smart3/search endpoint for automated structure classification. Use this skill before making API calls to ensure peak data conforms to the expected JSON schema.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0593
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

# json-payload-construction-for-nmr-spectra

## Summary

Construct a JSON payload containing NMR peak data (1H and 13C chemical shifts) formatted as a list of dictionaries for submission to the DeepSAT SMART 3 classification API. This skill enables programmatic classification of NMR spectra by encoding peak coordinates in the expected schema.

## When to use

When you have NMR peak assignments (1H and 13C chemical shift values) and need to submit them to the /api/smart3/search endpoint for automated structure classification. Use this skill before making API calls to ensure peak data conforms to the expected JSON schema.

## When NOT to use

- Peak data is already in a different API-accepted format (e.g., already serialized and validated by prior step)
- Chemical shift values are missing or incomplete for either 1H or 13C dimension
- Model input schema has changed and your local code references outdated field names without checking /model/metadata

## Inputs

- NMR peak chemical shift values (1H and 13C coordinates)
- Model metadata from /model/metadata endpoint (to verify schema)
- Structured peak data as Python list or equivalent in-memory structure

## Outputs

- JSON payload string (list of dictionaries with 1H and 13C keys)
- HTTP response with classification predictions and confidence scores
- Structured log file with request parameters, response timestamp, and results

## How to apply

Retrieve the current input schema from the /model/metadata endpoint via TensorFlow Serving to verify field names and structure. Organize your peak data into a list where each element is a dictionary with '1H' and '13C' keys mapped to corresponding chemical shift values (numeric). Construct the JSON payload by serializing this list structure. Validate that all required fields are present and values are numeric before submitting via POST request to /api/smart3/search. Parse the returned JSON response to extract classification predictions and confidence scores, logging request parameters and response timestamp for audit purposes.

## Related tools

- **TensorFlow Serving** (Serves model metadata endpoint to retrieve and verify current input schema and model version)
- **DeepSAT** (Hosts the /api/smart3/search endpoint that accepts and processes the JSON payload for NMR structure classification) — https://github.com/mwang87/DeepSAT

## Examples

```
import json; import requests; peaks = [{'1H': 7.32, '13C': 128.5}, {'1H': 3.82, '13C': 52.1}]; payload = json.dumps(peaks); response = requests.post('http://api.deepsat.org/api/smart3/search', data=payload, headers={'Content-Type': 'application/json'}); results = response.json(); print(results)
```

## Evaluation signals

- JSON payload is valid and parseable (no syntax errors)
- All peaks in the payload have both '1H' and '13C' keys with numeric values
- HTTP response status code is 200 or 201, indicating successful submission
- Returned JSON contains classification predictions and confidence scores (not error messages)
- Request/response timestamps and prediction results are correctly logged to output file with no missing entries

## Limitations

- If model input names change in TensorFlow Serving, code must be updated to match the new schema — no backward compatibility guarantee
- No changelog is available to track schema or API changes, requiring manual verification via /model/metadata on each deployment
- Payload construction assumes 1H and 13C are the only required peak dimensions; other isotopes or multi-dimensional data are not addressed

## Evidence

- [other] The /api/smart3/search endpoint accepts peaks as a JSON list of dictionaries with 1H and 13C as headers for programmatic classification requests.: "The /api/smart3/search endpoint accepts peaks as a JSON list of dictionaries with 1H and 13C as headers for programmatic classification requests."
- [intro] Classify programmatically. You can put in your peaks as a json list of dicts, with 1H,13C as headers: "Classify programmatically. You can put in your peaks as a json list of dicts, with 1H,13C as headers"
- [intro] We pass through tensorflow serving at this url: /model/metadata: "We pass through tensorflow serving at this url: /model/metadata"
- [intro] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
- [other] Construct a JSON payload as a list of dictionaries, each containing 1H and 13C peak keys and corresponding chemical shift values.: "Construct a JSON payload as a list of dictionaries, each containing 1H and 13C peak keys and corresponding chemical shift values."
