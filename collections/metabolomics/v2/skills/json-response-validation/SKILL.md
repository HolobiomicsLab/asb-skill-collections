---
name: json-response-validation
description: Use when after sending HTTP requests to API endpoints (such as /classify
  or /model/metadata on an NP-Classifier server) to verify that the response is parseable
  JSON and contains the expected output fields and metadata before attempting to extract
  or process the data programmatically.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3674
  tools:
  - Python
  - TensorFlow Serving
  - docker-compose
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- Make sure you have python installed
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

# json-response-validation

## Summary

Validate that API endpoints return well-formed JSON responses with expected fields, correct HTTP status codes, and proper schema structure. This skill ensures that downstream programmatic consumers of the API can reliably parse and use the returned data.

## When to use

Apply this skill after sending HTTP requests to API endpoints (such as /classify or /model/metadata on an NP-Classifier server) to verify that the response is parseable JSON and contains the expected output fields and metadata before attempting to extract or process the data programmatically.

## When NOT to use

- The API endpoint is known to return non-JSON responses (e.g., plain text, HTML, binary data).
- You are validating against a different schema than what the API documentation specifies.
- The response has already been validated upstream by a trusted intermediary.

## Inputs

- HTTP response body (raw text)
- HTTP status code (integer)

## Outputs

- Parsed JSON object
- Validation report (pass/fail for status code, parseability, and field presence)
- JSON file containing the validated response

## How to apply

After sending an HTTP GET request to an API endpoint, capture the full response including the status code and body. Parse the response body as JSON and verify that the HTTP status code is 200. Extract and inspect key fields: for the /classify endpoint, confirm the presence of the 'output' field; for /model/metadata, validate that input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'. Write the parsed response to a JSON file for subsequent use. If parsing fails or expected fields are missing, the endpoint is not functioning correctly.

## Related tools

- **TensorFlow Serving** (Provides the /model/metadata endpoint whose response structure and layer names must be validated)
- **docker-compose** (Orchestrates the NP-Classifier server and TensorFlow Serving containers that expose the API endpoints being validated)
- **Python** (Programmatic language used to construct HTTP requests, parse JSON responses, and validate response structure)

## Examples

```
import requests; import json; response = requests.get('http://localhost:8500/model/metadata'); assert response.status_code == 200; metadata = response.json(); print(json.dumps(metadata, indent=2))
```

## Evaluation signals

- HTTP status code is 200 (not 4xx or 5xx).
- Response body is valid JSON (parses without throwing a JSONDecodeError).
- For /classify endpoint: 'output' field is present in the response object.
- For /model/metadata endpoint: input layer names 'input_2048' and 'input_4096' and output layer name 'output' are present in the metadata.
- Validated response can be successfully written to and re-read from a JSON file without data loss.

## Limitations

- This skill validates only structure and presence of expected fields; it does not validate the semantic correctness or accuracy of the classification output itself.
- The skill assumes the NP-Classifier Docker services (server and TensorFlow Serving) are already running; it does not diagnose service startup or connectivity issues.
- Validation success does not guarantee that the model weights are correct or that the classification results are scientifically valid; it only confirms that the API contract is being met.

## Evidence

- [other] Validate the response structure contains the expected output field 'output' and verify the presence of input layer names 'input_2048' and 'input_4096' in the response metadata or schema.: "Validate the response structure contains the expected output field 'output' and verify the presence of input layer names 'input_2048' and 'input_4096' in the response metadata or schema."
- [other] Confirm the HTTP status code is 200 and the response is well-formed JSON.: "Confirm the HTTP status code is 200 and the response is well-formed JSON."
- [other] Parse the JSON response and extract input/output layer name fields. Validate that input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'.: "Parse the JSON response and extract input/output layer name fields. Validate that input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'."
- [readme] Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output": "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
