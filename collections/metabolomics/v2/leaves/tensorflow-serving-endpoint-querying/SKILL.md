---
name: tensorflow-serving-endpoint-querying
description: Use when you have deployed a TensorFlow model via TensorFlow Serving
  in a containerized environment (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - TensorFlow Serving
  - docker
  - docker-compose
  - curl or HTTP client library
  license_tier: open
derived_from:
- doi: 10.1021/acs.jnatprod.1c00399
  title: npclassifier
evidence_spans:
- We pass through tensorflow serving at this url
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

# tensorflow-serving-endpoint-querying

## Summary

Query a TensorFlow Serving endpoint to retrieve and validate model metadata, including input and output layer names. This skill is essential for verifying that a deployed model exposes the correct layer interface before performing inference requests.

## When to use

Use this skill when you have deployed a TensorFlow model via TensorFlow Serving in a containerized environment (e.g., Docker) and need to confirm that the /model/metadata endpoint correctly reports expected input layer names ('input_2048' and 'input_4096') and output layer name ('output'), or when integrating a TensorFlow Serving passthrough with an overlying API layer that requires validated layer metadata.

## When NOT to use

- The model has not yet been deployed or the TensorFlow Serving container is not running.
- You are testing model inference accuracy rather than metadata schema — use inference endpoints (/predict) instead.
- The model layer names are already known and validated in a prior integration step.

## Inputs

- running TensorFlow Serving container URL (e.g., http://localhost:8501)
- HTTP client or curl command-line tool
- expected layer name schema (input_2048, input_4096, output)

## Outputs

- JSON file containing the complete /model/metadata API response
- parsed input layer names and output layer name
- validation status (pass/fail)

## How to apply

Start the Dockerized TensorFlow Serving container using docker-compose. Send an HTTP GET request to the /model/metadata endpoint on the running container. Parse the JSON response to extract the input and output layer name fields. Validate that the parsed layer names match the expected schema (inputs: 'input_2048' and 'input_4096'; output: 'output'). If the validation passes, write the complete metadata response to a JSON file for reference; if layer names do not match, log the discrepancy and halt integration until the model or serving configuration is corrected, as mismatched layer names indicate that downstream inference code will fail.

## Related tools

- **TensorFlow Serving** (HTTP endpoint provider that exposes /model/metadata for layer introspection)
- **docker** (container runtime for executing the TensorFlow Serving environment)
- **docker-compose** (orchestration tool to start and manage the Dockerized NP-Classifier server)
- **curl or HTTP client library** (sends HTTP GET request to /model/metadata and retrieves JSON response)

## Examples

```
curl -X GET http://localhost:8501/v1/models/np_classifier/metadata | jq '.metadata.signature_def.serving_default.inputs | keys, .outputs | keys' && echo 'Layer names validated: input_2048, input_4096, output'
```

## Evaluation signals

- HTTP response status code is 200 OK and response body is valid JSON.
- Parsed response contains 'input_2048' and 'input_4096' as input layer names and 'output' as the output layer name.
- Metadata JSON file is successfully written to disk and contains all expected fields.
- No layer name mismatches are detected; all layer names conform to the expected schema.
- The /model/metadata endpoint response is consistent across multiple sequential queries (idempotency check).

## Limitations

- The skill assumes TensorFlow Serving is already built, configured, and running; it does not cover model conversion, Docker image build, or container startup troubleshooting.
- Layer names are fixed in the trained model artifact and cannot be changed via the metadata endpoint alone; if layer names do not match expectations, the model file or training pipeline must be corrected.
- The skill validates only metadata schema, not model weights, input shape validation, or inference correctness — a metadata validation pass does not guarantee downstream inference will succeed.

## Evidence

- [other] Does the TensorFlow Serving endpoint at /model/metadata successfully return model metadata including the correct input and output layer names when queried on the running Dockerized NP-Classifier server?: "Does the TensorFlow Serving endpoint at /model/metadata successfully return model metadata including the correct input and output layer names"
- [other] The expected model layer names that should be returned by the /model/metadata endpoint are input layers 'input_2048' and 'input_4096', and output layer 'output'.: "expected model layer names that should be returned by the /model/metadata endpoint are input layers 'input_2048' and 'input_4096', and output layer 'output'"
- [other] 1. Start the Dockerized NP-Classifier server using docker-compose. 2. Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving container. 3. Parse the JSON response and extract input/output layer name fields. 4. Validate that input layers are named 'input_2048' and 'input_4096' and output layer is named 'output'. 5. Write the complete metadata response to a JSON file.: "Start the Dockerized NP-Classifier server using docker-compose. Send an HTTP GET request to the /model/metadata endpoint on the running TensorFlow Serving container. Parse the JSON response and"
- [readme] We pass through tensorflow serving at this url: /model/metadata: "We pass through tensorflow serving at this url: /model/metadata"
- [readme] If the model input names change, then we need to change it in the code: "If the model input names change, then we need to change it in the code"
