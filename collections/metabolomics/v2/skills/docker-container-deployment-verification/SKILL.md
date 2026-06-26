---
name: docker-container-deployment-verification
description: Use when after building and starting a Dockerized TensorFlow Serving
  instance (via `make server-compose` or equivalent) to validate that the model has
  the expected input layer names ('input_2048' and 'input_4096') and output layer
  name ('output') before routing live inference traffic through the.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - docker
  - docker-compose
  - Python
  - TensorFlow Serving
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- you need docker and docker-compose
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

# docker-container-deployment-verification

## Summary

Verify that a Dockerized model server (specifically TensorFlow Serving) is running and exposes the correct input/output layer metadata through its HTTP metadata endpoint. This skill ensures the deployed model conforms to expected interface specifications before classification queries are issued.

## When to use

After building and starting a Dockerized TensorFlow Serving instance (via `make server-compose` or equivalent) to validate that the model has the expected input layer names ('input_2048' and 'input_4096') and output layer name ('output') before routing live inference traffic through the classification API.

## When NOT to use

- The model has already been validated in a prior deployment cycle and layer names are known to be stable.
- Input/output layer names are expected to change dynamically or differ from the documented specification.

## Inputs

- Running TensorFlow Serving Docker container (via docker-compose)
- HTTP endpoint URL (e.g. http://localhost:8500/model/metadata or equivalent)

## Outputs

- JSON metadata response from TensorFlow Serving
- Validation report documenting layer names and pass/fail status

## How to apply

Start the NP Classifier server using the docker-compose orchestration (make server-compose), then send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving instance at localhost or its configured hostname. Parse the JSON response and extract the 'inputs' and 'outputs' fields. Compare the layer names in the response against the expected specification: input layers must be named exactly 'input_2048' and 'input_4096', and the output layer must be named 'output'. Document any discrepancies in a validation report; if layer names differ, the model configuration in the code must be updated before proceeding with classification requests.

## Related tools

- **docker** (Container runtime for launching and managing the TensorFlow Serving instance)
- **docker-compose** (Orchestration tool for building and starting the Dockerized NP Classifier server stack)
- **TensorFlow Serving** (Inference server that exposes the model metadata endpoint and handles model queries)
- **Python** (Language for parsing JSON metadata response and generating validation report)

## Examples

```
curl -s http://localhost:8500/v1/models/np-classifier/metadata | python -c "import sys, json; meta = json.load(sys.stdin); print('Inputs:', [i['name'] for i in meta.get('inputs', [])]); print('Outputs:', [o['name'] for o in meta.get('outputs', [])])"
```

## Evaluation signals

- HTTP GET request to /model/metadata returns HTTP 200 status with valid JSON payload.
- JSON response contains 'inputs' array with exactly two entries named 'input_2048' and 'input_4096'.
- JSON response contains 'outputs' array with exactly one entry named 'output'.
- Layer names match specification exactly; validation report shows pass status.
- Subsequent /classify API calls with SMILES strings execute without layer-name mismatch errors.

## Limitations

- This skill validates only the layer names exposed via metadata; it does not verify model weights, inference correctness, or numerical output ranges.
- If model input/output names change upstream (e.g., during model retraining or conversion), the code consuming these layer names must be updated manually—the skill does not auto-correct mismatches.
- The metadata endpoint is TensorFlow Serving–specific; other inference servers (e.g., TorchServe, KServe) use different metadata protocols.

## Evidence

- [intro] research_question from task_002 / finding: "Does the deployed NP Classifier model expose input layers named 'input_2048' and 'input_4096' and an output layer named 'output' when queried through the TensorFlow Serving metadata endpoint?"
- [intro] task workflow step: "Start the NP Classifier server using docker-compose (make server-compose). Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving instance. Parse the JSON response"
- [readme] README section on checking model metadata: "We pass through tensorflow serving at this url: /model/metadata"
- [readme] README specification of layer names: "Input layers' names should be "input_2048" and "input_4096"

Output layer's name should be "output""
- [readme] README on code update requirement: "If the model input names change, then we need to change it in the code"
