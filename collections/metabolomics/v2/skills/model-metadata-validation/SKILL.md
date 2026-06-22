---
name: model-metadata-validation
description: Use when after deploying a TensorFlow Serving container (especially within a Dockerized stack like NP-Classifier), before running classification or inference pipelines, to confirm that input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - docker
  - docker-compose
  - TensorFlow Serving
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans: []
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

# Model Metadata Validation

## Summary

Validate that a TensorFlow Serving endpoint correctly exposes model metadata including input and output layer names. This skill confirms that a deployed neural network model's schema matches expected specifications before downstream inference.

## When to use

After deploying a TensorFlow Serving container (especially within a Dockerized stack like NP-Classifier), before running classification or inference pipelines, to confirm that input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'. Use this skill to catch layer name mismatches early, which would otherwise cause API calls to fail.

## When NOT to use

- Model has not yet been containerized or TensorFlow Serving is not running.
- Layer names are custom or project-specific and do not follow the NP-Classifier convention (input_2048, input_4096, output).
- Only offline metadata inspection is needed without testing the live endpoint.

## Inputs

- Running TensorFlow Serving container (via docker-compose)
- HTTP endpoint URL: /model/metadata

## Outputs

- JSON metadata response object (containing input/output layer schema)
- Persisted metadata JSON file (for audit trail)

## How to apply

Start the Dockerized NP-Classifier server via `docker-compose` or `make server-compose`. Send an HTTP GET request to the `/model/metadata` endpoint on the TensorFlow Serving container. Parse the returned JSON response and extract the input and output layer name fields. Validate that the two input layers are exactly named 'input_2048' and 'input_4096', and the single output layer is named 'output'. Record the complete metadata response to a JSON file for audit and debugging. If layer names do not match, the model configuration in the served artifact must be corrected before the inference API can be reliably used.

## Related tools

- **docker** (Container runtime for launching the TensorFlow Serving instance)
- **docker-compose** (Orchestration tool to bring up the complete NP-Classifier stack (TensorFlow Serving + nginx) in one command)
- **TensorFlow Serving** (REST/gRPC server exposing the /model/metadata endpoint and serving inference requests) — https://github.com/tensorflow/serving

## Examples

```
curl -X GET http://localhost:8501/v1/models/npc/metadata | jq '.inputs[].name, .outputs[].name'
```

## Evaluation signals

- HTTP 200 response received from /model/metadata endpoint.
- Parsed JSON contains 'inputs' array with exactly two entries named 'input_2048' and 'input_4096'.
- Parsed JSON contains 'outputs' array with exactly one entry named 'output'.
- Persisted metadata JSON file is valid JSON and contains all layer definitions.
- Layer names match expected schema; if they differ, the validation fails and model artifact must be redeployed.

## Limitations

- Metadata validation only confirms layer names; it does not verify layer shapes, data types, or functional correctness of the model.
- Requires TensorFlow Serving to be running; intermittent container failures will cause the skill to fail.
- Layer names are hard-coded expectations specific to NP-Classifier; other models with different layer naming schemes require this skill to be re-parameterized.
- The /model/metadata endpoint availability depends on TensorFlow Serving configuration; some deployments may disable it for security reasons.

## Evidence

- [other] Does the TensorFlow Serving endpoint at /model/metadata successfully return model metadata including the correct input and output layer names when queried on the running Dockerized NP-Classifier server?: "Does the TensorFlow Serving endpoint at /model/metadata successfully return model metadata including the correct input and output layer names when queried on the running Dockerized NP-Classifier"
- [other] The expected model layer names that should be returned by the /model/metadata endpoint are input layers 'input_2048' and 'input_4096', and output layer 'output'.: "The expected model layer names that should be returned by the /model/metadata endpoint are input layers 'input_2048' and 'input_4096', and output layer 'output'."
- [other] 1. Start the Dockerized NP-Classifier server using docker-compose. 2. Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving container. 3. Parse the JSON response and extract input/output layer name fields. 4. Validate that input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'. 5. Write the complete metadata response to a JSON file.: "1. Start the Dockerized NP-Classifier server using docker-compose. 2. Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving container. 3. Parse the JSON response"
- [readme] We pass through tensorflow serving at this url: /model/metadata: "We pass through tensorflow serving at this url: /model/metadata"
- [readme] Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output": "Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output""
- [readme] To bring everything up, you need docker and docker-compose: "To bring everything up, you need docker and docker-compose"
