---
name: tensorflow-serving-layer-inspection
description: Use when after deploying a TensorFlow model via TensorFlow Serving (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - TensorFlow Serving
  - Python
  - docker
  - docker-compose
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- We pass through tensorflow serving at this url
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

# tensorflow-serving-layer-inspection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate that a deployed TensorFlow Serving model exposes the correct input and output layer names by querying the /model/metadata HTTP endpoint and parsing the JSON response. This skill ensures model architecture conformance before programmatic use.

## When to use

After deploying a TensorFlow model via TensorFlow Serving (e.g., via docker-compose), verify that the model's input layer names match expected values ('input_2048' and 'input_4096') and output layer name is 'output', to catch layer-naming mismatches before they propagate to downstream classification or inference code.

## When NOT to use

- Model has not yet been deployed or TensorFlow Serving is not running—start the server first.
- The /model/metadata endpoint is not exposed or is behind authentication that has not been configured.
- Input/output layer naming is flexible or intentionally variable; use this skill only when strict layer-name conformance is a requirement.

## Inputs

- Running TensorFlow Serving instance (http://host:port)
- Expected input layer names (e.g., ['input_2048', 'input_4096'])
- Expected output layer name (e.g., 'output')

## Outputs

- JSON metadata response from /model/metadata endpoint
- Extracted input and output layer names
- Validation report (pass/fail, layer names found, comparison result)

## How to apply

Start the TensorFlow Serving instance using docker-compose (e.g., `make server-compose`). Send an HTTP GET request to the /model/metadata endpoint on the running server. Parse the returned JSON response to extract the names of all input and output layers. Cross-reference the extracted names against the expected schema: inputs should be exactly 'input_2048' and 'input_4096', and output should be 'output'. Document the layer names found, the comparison result, and pass/fail status in a validation report. If names do not match, the model conversion or serving configuration is misaligned and must be corrected before proceeding.

## Related tools

- **docker** (Container runtime for launching TensorFlow Serving instance)
- **docker-compose** (Orchestration tool to bring up NP Classifier server with `make server-compose`)
- **TensorFlow Serving** (Serving framework that exposes /model/metadata endpoint for layer name inspection)
- **Python** (Language for parsing JSON metadata response and generating validation report)

## Examples

```
curl -X GET http://localhost:8501/v1/models/NP_Classifier/metadata | python -m json.tool
```

## Evaluation signals

- HTTP 200 response received from /model/metadata endpoint with valid JSON payload
- Extracted input layers exactly match expected names 'input_2048' and 'input_4096'
- Extracted output layer exactly matches expected name 'output'
- Validation report documents all layer names found and final pass/fail status
- No layer-naming mismatches between model schema and downstream inference code (e.g., /classify endpoint)

## Limitations

- Requires TensorFlow Serving to be running and the /model/metadata endpoint to be network-accessible.
- Layer names are fixed at model conversion time; if incorrect names are embedded in the HDF5 TF2 model, this inspection will pass but the model remains misconfigured for the intended workflow.
- Does not validate layer shapes, data types, or tensor dimensions—only names are checked.

## Evidence

- [other] Does the deployed NP Classifier model expose input layers named 'input_2048' and 'input_4096' and an output layer named 'output' when queried through the TensorFlow Serving metadata endpoint?: "Does the deployed NP Classifier model expose input layers named 'input_2048' and 'input_4096' and an output layer named 'output' when queried through the TensorFlow Serving metadata endpoint?"
- [other] Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving instance.: "Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving instance."
- [other] Parse the JSON response to extract input and output layer names.: "Parse the JSON response to extract input and output layer names."
- [readme] We pass through tensorflow serving at this url: /model/metadata: "We pass through tensorflow serving at this url: /model/metadata"
- [readme] Input layers' names should be "input_2048" and "input_4096"; Output layer's name should be "output": "Input layers' names should be "input_2048" and "input_4096" and Output layer's name should be "output""
- [readme] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
