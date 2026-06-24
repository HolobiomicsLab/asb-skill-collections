---
name: docker-container-health-verification
description: Use when when you have deployed NP Classifier using Docker Compose and
  need to confirm that both the server and TensorFlow Serving containers are running
  and healthy before sending SMILES strings to the /classify endpoint.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_2258
  - http://edamontology.org/topic_0154
  tools:
  - docker
  - docker-compose
  - Python
  - Docker
  - Docker Compose
  - TensorFlow Serving
  - mwang87/NP-Classifier
  license_tier: open
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

# docker-container-health-verification

## Summary

Verify that Docker containers running NP Classifier services (server and TensorFlow Serving) are operational and responding correctly before executing classification requests. This skill ensures the API is ready to accept SMILES queries and return properly structured responses.

## When to use

When you have deployed NP Classifier using Docker Compose and need to confirm that both the server and TensorFlow Serving containers are running and healthy before sending SMILES strings to the /classify endpoint. Apply this skill after executing `make server-compose` and before querying the classification API.

## When NOT to use

- Containers have not yet been built—run `make server-compose` first
- You only need to verify model metadata structure without testing the full classification pipeline—use `/model/metadata` endpoint instead
- Input is an already-classified molecular structure and you need to validate classification results, not container health

## Inputs

- Docker container identifiers (service names from docker-compose.yml)
- Valid SMILES string (e.g., 'CC(=O)Oc1ccccc1C(=O)O')
- HTTP client or curl command

## Outputs

- HTTP status code (200 for healthy)
- JSON response object containing 'output' field
- Response metadata with input layer names 'input_2048' and 'input_4096'

## How to apply

After bringing up the Docker services with `make server-compose`, verify container status using docker ps or docker-compose ps commands. Check that both the server container and TensorFlow Serving container are in the 'running' state. Send a test HTTP GET request to the /classify endpoint with a valid SMILES string parameter and validate that the response returns HTTP status 200 with well-formed JSON containing the 'output' field and expected input layer names 'input_2048' and 'input_4096' in the response metadata. If the response is successful and properly structured, the container health check is complete.

## Related tools

- **Docker** (Container runtime for running NP Classifier server and TensorFlow Serving)
- **Docker Compose** (Orchestration tool to bring up and manage multi-container NP Classifier deployment)
- **TensorFlow Serving** (Backend service that handles model inference requests and metadata exposure at /model/metadata endpoint)
- **mwang87/NP-Classifier** (The complete NP Classifier application containing the server, models, and Docker configuration) — https://github.com/mwang87/NP-Classifier

## Examples

```
curl -X GET 'http://localhost:8080/classify?smiles=CC(=O)Oc1ccccc1C(=O)O' -w '\nStatus: %{http_code}\n'
```

## Evaluation signals

- HTTP GET request to /classify endpoint with a valid SMILES parameter returns HTTP status code 200
- Response body is valid JSON containing an 'output' field with classification result
- Response metadata or schema includes both input layer names 'input_2048' and 'input_4096'
- Both server and TensorFlow Serving containers appear in `docker ps` output with status 'running' or 'up'
- Consecutive requests to /classify return consistent responses without errors or timeouts

## Limitations

- Health verification only confirms that containers are running and responding; it does not validate the correctness of classification results themselves
- The skill assumes the Docker network (nginx-net) was created beforehand with `docker network create nginx-net`
- Model accuracy and performance characteristics are not evaluated by container health checks; see model metadata at /model/metadata for layer configuration details
- If models were not downloaded via `sh ./get_models.sh` in Classifier/models_folder/models, the TensorFlow Serving container may fail even if Docker containers appear healthy

## Evidence

- [readme] We typically will deploy this locally. To bring everything up, you need docker and docker-compose: "We typically will deploy this locally. To bring everything up, you need docker and docker-compose"
- [other] Ensure NP-Classifier Docker services are running (server and TensorFlow Serving): "Ensure NP-Classifier Docker services are running (server and TensorFlow Serving)"
- [other] Send the request and capture the JSON response. Validate the response structure contains the expected output field 'output' and verify the presence of input layer names 'input_2048' and 'input_4096': "Validate the response structure contains the expected output field 'output' and verify the presence of input layer names 'input_2048' and 'input_4096'"
- [other] Confirm the HTTP status code is 200 and the response is well-formed JSON: "Confirm the HTTP status code is 200 and the response is well-formed JSON"
