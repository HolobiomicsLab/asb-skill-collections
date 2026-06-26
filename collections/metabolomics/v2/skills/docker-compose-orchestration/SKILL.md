---
name: docker-compose-orchestration
description: Use when when you need to deploy the NP Classifier locally with TensorFlow
  Serving backend and nginx frontend on the same host, and you want to avoid manual
  container lifecycle management and inter-container networking configuration.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - docker
  - docker-compose
  - Python
  - TensorFlow Serving
  - nginx
  - Make
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jacs.9b13786
  title: CSCS / deep CNN natural-product annotation
evidence_spans:
- you need docker and docker-compose
- To bring everything up, you need docker and docker-compose.
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

# docker-compose-orchestration

## Summary

Orchestrate multi-container deployments for the NP Classifier server using docker-compose, coordinating TensorFlow Serving and nginx reverse proxy through a shared Docker network. This skill ensures reproducible, containerized deployment of machine learning classification APIs.

## When to use

When you need to deploy the NP Classifier locally with TensorFlow Serving backend and nginx frontend on the same host, and you want to avoid manual container lifecycle management and inter-container networking configuration.

## When NOT to use

- Models have not been downloaded and converted to HDF5 TF2 format—docker-compose will fail at runtime when TensorFlow Serving attempts to load missing model files.
- Deploying to Kubernetes or cloud-native orchestration platforms—docker-compose is single-host only; use Helm charts or cloud deployment tools instead.
- Input layer or output layer names differ from the hardcoded specification (input_2048, input_4096, output)—the API code will not match the metadata endpoint responses.

## Inputs

- Cloned NP Classifier repository directory (github.com/mwang87/NP-Classifier)
- Pre-downloaded model files in Classifier/models_folder/models/
- HDF5-converted TensorFlow 2.3.0 model files
- docker-compose.yml configuration file
- Makefile with server-compose target

## Outputs

- Running TensorFlow Serving container exposing model metadata endpoint
- Running classification API container accessible via /classify?smiles=<> endpoint
- nginx reverse proxy forwarding requests to backend services
- Docker bridge network (nginx-net) with DNS resolution between containers
- Container logs documenting startup and model loading

## How to apply

First, create a persistent Docker bridge network (nginx-net) using docker network create to enable DNS-based service discovery between containers. Then invoke make server-compose, which reads docker-compose configuration to orchestrate pulling/building container images, mounting model volumes, exposing ports through nginx, and starting both the TensorFlow Serving container (listening on port 8501 internally) and the classification API container. The make target abstracts the underlying docker-compose up command and ensures models have been pre-downloaded via get_models.sh and converted to HDF5 TensorFlow 2.3.0 format beforehand. Verify correct orchestration by querying the /model/metadata endpoint (e.g., http://localhost:8501/v1/models/<model_name>/metadata) and confirming layer names match the specification (input_2048, input_4096, output).

## Related tools

- **docker** (Container runtime for isolating NP Classifier server and TensorFlow Serving)
- **docker-compose** (Multi-container orchestration declarative configuration and lifecycle management)
- **TensorFlow Serving** (Serves pre-trained NP Classifier models and exposes /model/metadata endpoint for layer name validation)
- **nginx** (Reverse proxy forwarding HTTP requests to backend classification API and TensorFlow Serving)
- **Make** (Build automation tool wrapping docker-compose commands in the server-compose target)

## Examples

```
docker network create nginx-net && make server-compose
```

## Evaluation signals

- docker ps confirms two containers are running (TensorFlow Serving and classification API) and both are connected to the nginx-net network.
- GET request to http://localhost:8501/v1/models/<model_name>/metadata returns JSON with input_spec fields containing 'input_2048' and 'input_4096', and output_spec containing 'output'.
- POST/GET request to /classify?smiles=CCO (or other valid SMILES) returns a classification result (not 404 or connection error), indicating nginx reverse proxy and API are responding.
- Container logs (docker logs <container_id>) show no model loading errors and confirm TensorFlow Serving started successfully.
- Docker network inspect nginx-net lists both containers under the Containers field, confirming network attachment.

## Limitations

- docker-compose deployment is single-host only; multi-host or cloud deployments require alternative orchestration (Kubernetes, Docker Swarm).
- Model input/output layer names are hardcoded in the code; if upstream Keras models are retrained with different layer names, the code must be manually updated and containers rebuilt.
- No persistent volume configuration mentioned in the README; restarting containers will lose any logged inference data unless volumes are explicitly configured in docker-compose.yml.
- TensorFlow 2.3.0 is pinned for model conversion; newer TensorFlow versions may have compatibility issues with HDF5 model format or TensorFlow Serving.

## Evidence

- [readme] We typically will deploy this locally. To bring everything up, you need docker and docker-compose.: "We typically will deploy this locally. To bring everything up, you need docker and docker-compose."
- [readme] Create Docker network and invoke make server-compose to orchestrate deployment: "docker network create nginx-net"
- [readme] Model metadata endpoint and layer name validation: "We pass through tensorflow serving at this url: /model/metadata"
- [readme] Layer name specifications for validation: "Input layers' names should be "input_2048" and "input_4096". Output layer's name should be "output""
