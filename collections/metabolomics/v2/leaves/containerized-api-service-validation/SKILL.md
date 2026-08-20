---
name: containerized-api-service-validation
description: Use when after building and starting a Dockerized server via docker-compose
  orchestration, particularly when deploying machine learning inference services that
  depend on pre-trained models behind an API gateway.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Python
  - docker
  - docker-compose
  - TensorFlow Serving
  - nginx
  - NP Classifier API
  license_tier: open
derived_from:
- doi: 10.1021/jacs.9b13786
  title: CSCS / deep CNN natural-product annotation
evidence_spans:
- Make sure you have python installed
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cscs_deep_cnn_natural_product_annotation_cq
    doi: 10.1021/jacs.9b13786
    title: CSCS / deep CNN natural-product annotation
  dedup_kept_from: coll_cscs_deep_cnn_natural_product_annotation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jacs.9b13786
  all_source_dois:
  - 10.1021/jacs.9b13786
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# containerized-api-service-validation

## Summary

Validate a Dockerized API service by verifying correct deployment of containerized components (TensorFlow Serving, classification API, nginx), confirming model metadata accessibility, and testing inference endpoints with known input formats (SMILES strings). This skill ensures the NP Classifier server is correctly orchestrated and functional before downstream use.

## When to use

Apply this skill after building and starting a Dockerized server via docker-compose orchestration, particularly when deploying machine learning inference services that depend on pre-trained models behind an API gateway. Use it to confirm that the nginx-net Docker network, TensorFlow Serving, and classification API are all running and properly wired before querying the service in production or analysis workflows.

## When NOT to use

- Models have not yet been downloaded via sh ./get_models.sh or converted to HDF5 TF2 format — validation will fail due to missing or incompatible model artifacts.
- Docker daemon is not running or docker-compose has not been invoked via make server-compose — the containers do not exist to validate.
- Input/output layer names in the model do not conform to the expected schema ('input_2048', 'input_4096', 'output') — model metadata validation will flag a configuration error that must be resolved upstream.

## Inputs

- Running Docker containers (nginx, TensorFlow Serving, NP Classifier API)
- Docker network (nginx-net) with active container connectivity
- Pre-trained HDF5 TensorFlow 2.3.0 models with input/output layer metadata
- Test SMILES strings (chemical structure notation)

## Outputs

- Model metadata response confirming input/output layer names and tensor shapes
- Classification API response (structured predictions) for submitted SMILES input
- Docker container logs and network diagnostics
- Validation report indicating service readiness (pass/fail per endpoint)

## How to apply

First, verify that the Docker network (nginx-net) was created and all containers are running. Then, query the model metadata endpoint (/model/metadata) through TensorFlow Serving to confirm the model is loaded and accessible. Next, validate that input layer names match the expected schema ('input_2048' and 'input_4096') and the output layer is named 'output'. Finally, test the classification API endpoint (/classify?smiles=<>) by submitting a well-formed SMILES string and confirming that a structured classification response is returned without errors. If caching is enabled, test both cached and non-cached query paths to verify performance optimization.

## Related tools

- **docker** (Container runtime; verifies running containers and network connectivity)
- **docker-compose** (Orchestrates multi-container service deployment; invoked via make server-compose)
- **TensorFlow Serving** (Exposes model metadata and inference endpoints; /model/metadata queried to validate model load)
- **nginx** (Reverse proxy and API gateway; routes requests to TensorFlow Serving and classification API)
- **NP Classifier API** (Provides /classify?smiles=<> endpoint for chemical structure classification) — github.com/mwang87/NP-Classifier

## Examples

```
curl http://localhost/model/metadata && curl 'http://localhost/classify?smiles=CC(C)Cc1ccc(cc1)C(C)C(O)=O' && curl 'http://localhost/classify?smiles=CC(C)Cc1ccc(cc1)C(C)C(O)=O&cached=true'
```

## Evaluation signals

- Model metadata endpoint (/model/metadata) returns HTTP 200 with valid JSON containing model name, version, and input/output tensor specs.
- Input layer names in metadata response are exactly 'input_2048' and 'input_4096'; output layer name is exactly 'output'.
- Classification API endpoint (/classify?smiles=CC(C)Cc1ccc(cc1)C(C)C(O)=O) returns HTTP 200 with a JSON response containing predicted class labels and confidence scores.
- Docker containers for nginx, TensorFlow Serving, and NP Classifier API are all in 'running' state (docker ps shows all three active).
- Cached and non-cached query paths both return consistent predictions (same class/score regardless of cached flag), confirming API logic integrity.

## Limitations

- Model input layer names are hardcoded in the API code; if model architecture changes, the code must be updated to reflect new input layer names (as stated: 'If the model input names change, then we need to change it in the code').
- TensorFlow 2.3.0 is required for HDF5 model conversion; models converted with other TensorFlow versions may not load correctly in the Serving container.
- The skill assumes pre-trained models have been downloaded and converted to HDF5 format before docker-compose is invoked; missing or corrupted model files will cause TensorFlow Serving to fail silently or timeout.
- Validation via HTTP endpoints requires network connectivity to the nginx reverse proxy; firewall rules or port binding misconfiguration will block endpoint accessibility.

## Evidence

- [readme] Model metadata endpoint availability and expected structure: "We pass through tensorflow serving at this url: ```/model/metadata```"
- [readme] Expected input/output layer names in model schema: "Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output""
- [readme] Classification API endpoint format and input type: "Classify programmatically ```/classify?smiles=<>```"
- [readme] Docker network prerequisite and compose target invocation: "If you didn't do it already, you will need a network. ```shell docker network create nginx-net ``` ```shell make server-compose ```"
- [readme] Hardcoded input layer dependency in code: "If the model input names change, then we need to change it in the code"
- [readme] TensorFlow version constraint for model conversion: "Make sure you have python installed and tensorflow version 2.3.0 installed to convert the keras models into HDF5 TF2 models"
- [readme] Caching parameter availability: "You can also provide cached flag to the params to get the cached version so make it faster"
