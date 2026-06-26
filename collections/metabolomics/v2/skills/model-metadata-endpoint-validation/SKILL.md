---
name: model-metadata-endpoint-validation
description: Use when after starting a TensorFlow Serving instance (e.g., via docker-compose)
  and before attempting classification tasks, to confirm that input layers are named
  'input_2048' and 'input_4096' and the output layer is named 'output'.
license: CC-BY-4.0
metadata:
  edam_topics: []
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

# model-metadata-endpoint-validation

## Summary

Validate that a deployed TensorFlow Serving model exposes the correct input and output layer names by querying the /model/metadata HTTP endpoint. This skill ensures the model interface matches deployment expectations before executing inference workflows.

## When to use

Apply this skill after starting a TensorFlow Serving instance (e.g., via docker-compose) and before attempting classification tasks, to confirm that input layers are named 'input_2048' and 'input_4096' and the output layer is named 'output'. Use it as a prerequisite check when deploying a new NP Classifier model or when layer names may have changed.

## When NOT to use

- The model has not yet been converted to HDF5 TF2 format or downloaded via get_models.sh
- The TensorFlow Serving container is not running or the /model/metadata endpoint is not accessible
- You are validating a non-TensorFlow model or a model not served through TensorFlow Serving

## Inputs

- Running TensorFlow Serving container with NP Classifier model loaded
- HTTP endpoint URL: http://<host>:<port>/model/metadata

## Outputs

- JSON metadata object containing model signature with input and output layer definitions
- Validation report documenting layer names found and pass/fail status

## How to apply

Start the NP Classifier server using `make server-compose` to bring up the TensorFlow Serving container on the nginx-net Docker network. Send an HTTP GET request to the `/model/metadata` endpoint on the running TensorFlow Serving instance. Parse the returned JSON response to extract the names of all input and output layers. Verify that exactly two input layers exist with names 'input_2048' and 'input_4096', and that exactly one output layer exists named 'output'. Document any mismatches in a validation report; if layer names differ, the code consuming this model must be updated to match the actual layer names before inference can proceed.

## Related tools

- **TensorFlow Serving** (Exposes the model metadata endpoint for querying layer names and model signatures)
- **docker-compose** (Orchestrates the containerized NP Classifier server deployment via make server-compose)
- **Python** (Used to parse JSON response from metadata endpoint and generate validation report)

## Examples

```
curl -s http://localhost:8501/v1/models/np_classifier/metadata | python -m json.tool | grep -E '(name|input_|output)'
```

## Evaluation signals

- HTTP GET request to /model/metadata returns a 200 status code with valid JSON
- Parsed JSON contains exactly two input layers with names 'input_2048' and 'input_4096'
- Parsed JSON contains exactly one output layer with name 'output'
- Validation report explicitly documents pass/fail status for each layer name check
- No validation errors prevent downstream classification API calls to /classify?smiles=<>

## Limitations

- If model input or output layer names change, the code consuming this model must be updated in tandem; the metadata endpoint reflects only what the model exposes, not what the client code expects
- The metadata endpoint does not validate the shape or dtype of the tensors, only their names
- Querying metadata requires the TensorFlow Serving container to be running; it does not validate the model file itself before deployment

## Evidence

- [other] Does the deployed NP Classifier model expose input layers named 'input_2048' and 'input_4096' and an output layer named 'output' when queried through the TensorFlow Serving metadata endpoint?: "Does the deployed NP Classifier model expose input layers named 'input_2048' and 'input_4096' and an output layer named 'output' when queried through the TensorFlow Serving metadata endpoint?"
- [other] 1. Start the NP Classifier server using docker-compose (make server-compose). 2. Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving instance. 3. Parse the JSON response to extract input and output layer names.: "Start the NP Classifier server using docker-compose (make server-compose). 2. Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving instance. 3. Parse the JSON"
- [other] Verify that input layers are named 'input_2048' and 'input_4096' and the output layer is named 'output'. 5. Generate a validation report documenting layer names found and pass/fail status.: "Verify that input layers are named 'input_2048' and 'input_4096' and the output layer is named 'output'. 5. Generate a validation report documenting layer names found and pass/fail status."
- [readme] We pass through tensorflow serving at this url: ```/model/metadata```: "We pass through tensorflow serving at this url: ```/model/metadata```"
- [readme] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
