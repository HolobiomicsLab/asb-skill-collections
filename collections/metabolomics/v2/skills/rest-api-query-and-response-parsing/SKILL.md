---
name: rest-api-query-and-response-parsing
description: Use when you have deployed a TensorFlow Serving instance (via docker-compose or equivalent) and need to verify that the model's input layer names ('input_2048' and 'input_4096') and output layer name ('output') match the expected schema before integrating the model into a classification pipeline or.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Python
  - docker-compose
  - TensorFlow Serving
  - docker
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
  - build: coll_npclassifier_cq
    doi: 10.1021/acs.jnatprod.1c00399
    title: npclassifier
  dedup_kept_from: coll_npclassifier_cq
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

# REST API Query and Response Parsing

## Summary

Query a deployed TensorFlow Serving metadata endpoint via HTTP GET and parse the JSON response to extract and validate model layer names. This skill is essential for verifying that a containerized model server exposes the correct input and output layer architecture before downstream classification or inference tasks.

## When to use

You have deployed a TensorFlow Serving instance (via docker-compose or equivalent) and need to verify that the model's input layer names ('input_2048' and 'input_4096') and output layer name ('output') match the expected schema before integrating the model into a classification pipeline or before running inference queries.

## When NOT to use

- The TensorFlow Serving instance is not yet running or not accessible via HTTP
- The model has already been validated in a prior deployment and you are reusing the same container image without code changes
- You need to query the classification API itself (e.g., /classify?smiles=<>) rather than inspect model metadata

## Inputs

- Running TensorFlow Serving instance with NP Classifier model deployed
- HTTP endpoint URL (e.g., http://localhost:8501/model/metadata)
- Expected layer name specification (input_2048, input_4096, output)

## Outputs

- JSON metadata response from TensorFlow Serving
- Extracted input layer names list
- Extracted output layer name
- Validation report (pass/fail status and layer names found)

## How to apply

Start the NP Classifier server using `make server-compose`, which launches TensorFlow Serving in a Docker container. Send an HTTP GET request to the `/model/metadata` endpoint on the running service. Parse the returned JSON response to extract the 'inputs' and 'outputs' fields. Cross-check that the input layer names are exactly 'input_2048' and 'input_4048' and the output layer is named 'output'. If any layer name does not match the expected values, the model configuration must be corrected (e.g., in the code that references layer names) before proceeding to inference. Document the validation outcome (pass/fail) and layer names found in a report.

## Related tools

- **docker-compose** (Orchestrate and start the TensorFlow Serving container)
- **TensorFlow Serving** (Host the NP Classifier model and expose metadata and inference endpoints)
- **Python** (Parse and validate JSON response from the metadata endpoint)
- **docker** (Container runtime for TensorFlow Serving instance)

## Examples

```
curl -X GET http://localhost:8501/model/metadata | python -m json.tool | grep -E '(input_2048|input_4096|output)'
```

## Evaluation signals

- HTTP response status code is 200 (OK) and response body is valid JSON
- Parsed JSON contains 'inputs' key with exactly two entries named 'input_2048' and 'input_4096'
- Parsed JSON contains 'outputs' key with exactly one entry named 'output'
- No HTTP errors (4xx, 5xx) or connection timeouts occur during endpoint query
- Validation report explicitly states 'pass' when all layer names match expected values, 'fail' otherwise

## Limitations

- The skill assumes TensorFlow Serving is correctly configured and the model is already loaded; misconfigured or missing models will not return valid metadata
- If model input or output layer names are changed in the source code or model file, the hardcoded layer name checks must be updated to match
- The metadata endpoint does not validate model behavior or inference correctness—only the layer naming schema

## Evidence

- [other] Does the deployed NP Classifier model expose input layers named 'input_2048' and 'input_4096' and an output layer named 'output' when queried through the TensorFlow Serving metadata endpoint?: "input layers named 'input_2048' and 'input_4096' and an output layer named 'output' when queried through the TensorFlow Serving metadata endpoint"
- [other] Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving instance. Parse the JSON response to extract input and output layer names.: "Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving instance. Parse the JSON response to extract input and output layer names."
- [other] Verify that input layers are named 'input_2048' and 'input_4096' and the output layer is named 'output'. Generate a validation report documenting layer names found and pass/fail status.: "Verify that input layers are named 'input_2048' and 'input_4096' and the output layer is named 'output'. Generate a validation report documenting layer names found and pass/fail status."
- [readme] We pass through tensorflow serving at this url: ```/model/metadata```: "We pass through tensorflow serving at this url: ```/model/metadata```"
- [readme] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
- [readme] Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output": "Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output""
