---
name: docker-network-creation
description: Use when when deploying a multi-container application stack using docker-compose
  where containers need reliable hostname-based service discovery and isolation from
  the host network.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - docker
  - docker-compose
  - Python
  - nginx
  - TensorFlow Serving
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

# docker-network-creation

## Summary

Create an isolated Docker network bridge to enable multi-container communication for microservice deployments. This skill is essential when orchestrating interdependent containers (e.g., TensorFlow Serving + API + nginx) that must communicate on a shared virtual network rather than through host ports.

## When to use

When deploying a multi-container application stack using docker-compose where containers need reliable hostname-based service discovery and isolation from the host network. Specifically, when you have TensorFlow Serving, classification APIs, and reverse proxies (nginx) that must communicate internally without exposing each service individually to the host.

## When NOT to use

- Single-container deployments where the container runs in host or default bridge network mode.
- Deployments already using Docker Swarm or Kubernetes, which manage networking automatically.
- When containers only need to communicate via published ports on localhost (though this is less resilient and not recommended for multi-service stacks).

## Inputs

- Docker daemon running on host
- Network name (string identifier, e.g. 'nginx-net')

## Outputs

- User-defined bridge network (Docker network object)
- Network available for container attachment via docker-compose or docker run --network flag

## How to apply

Before invoking docker-compose or make server-compose targets, explicitly create a user-defined bridge network using `docker network create <network-name>`. In the NP Classifier deployment, the network is named 'nginx-net' and is created once as a prerequisite. The docker-compose configuration then references this network by name in its `networks` section, ensuring all orchestrated containers join the same bridge and can resolve each other by service name. This decouples network setup from compose orchestration and prevents network name collisions across deployments.

## Related tools

- **docker** (CLI tool used to create and inspect user-defined bridge networks via `docker network create` and `docker network inspect` commands)
- **docker-compose** (Orchestration tool that references the pre-created network in compose configuration to attach containers on startup)
- **nginx** (Reverse proxy container that joins the network to route traffic to downstream services (TensorFlow Serving, API) by service hostname)
- **TensorFlow Serving** (Model serving container that joins the network to be discoverable by the classification API at a stable hostname)

## Examples

```
docker network create nginx-net
```

## Evaluation signals

- Network exists and is visible via `docker network ls` and `docker network inspect nginx-net`
- docker-compose services can resolve each other by hostname (e.g. from API container, `curl http://tensorflow-serving:8501/v1/models` succeeds)
- No port conflicts or 'network already exists' errors when re-running docker-compose
- Containers are listed under the network's 'Containers' field when inspected, confirming they are attached
- Inter-container communication works without publishing ports to the host (services communicate via bridge, not localhost:port)

## Limitations

- Network must be created before docker-compose is invoked; failure to do so will cause compose to fail or create a default network instead.
- The network persists after containers stop and must be manually cleaned up with `docker network rm` if no longer needed, otherwise it can clutter the Docker environment.
- User-defined bridge networks do not support link aliases or legacy --link flag; service discovery relies on container names and docker-compose service names only.
- Network creation requires Docker daemon to be running and the user to have sufficient privileges (typically membership in the docker group).

## Evidence

- [readme] If you didn't do it already, you will need a network. docker network create nginx-net: "If you didn't do it already, you will need a network.

```shell
docker network create nginx-net
```"
- [intro] Local deployment of NP Classifier requires creating an nginx-net Docker network and invoking the make server-compose target to build and start the Dockerized server.: "Local deployment of NP Classifier requires creating an nginx-net Docker network and invoking the make server-compose target"
