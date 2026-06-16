---
name: volume-mount-and-persistence-design
description: Use when you are composing multiple containerized services that have data dependencies—e.g., a web application that launches calculation jobs, a calculation engine that consumes a pre-built lookup database, and a data-processing service that generates that lookup.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3173
  tools:
  - MAGMa
  - Docker Compose
  - MAGMa job service
  - MAGMa pubchem service
  - MAGMa joblauncher webservice
  - MAGMa web application
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma
schema_version: 0.2.0
---

# volume-mount-and-persistence-design

## Summary

Design and configure Docker volume mounts and data persistence strategies for multi-service containerized systems where stateful components (databases, lookup tables, calculation outputs) must survive container restarts and be shared across interdependent services. This skill is essential when orchestrating microservices that depend on shared data artifacts or long-lived state.

## When to use

You are composing multiple containerized services that have data dependencies—e.g., a web application that launches calculation jobs, a calculation engine that consumes a pre-built lookup database, and a data-processing service that generates that lookup. You need to define which data must persist across container lifecycle events, where it should be stored, and how services will access it.

## When NOT to use

- All application state is ephemeral and services are stateless (no database, no shared lookup tables)—use simple container networking without volume mounts.
- Services are deployed in a Kubernetes cluster where StatefulSets and PersistentVolumeClaims are the correct abstraction, not Docker Compose.
- Data is managed by an external service (managed database, S3, etc.) so local persistence is not required.

## Inputs

- docker-compose.yml template or service specifications
- MAGMa subproject source code (emetabolomics_site, job, joblauncher, pubchem, web) with documented data paths and dependencies
- Existing Dockerfiles or build configurations indicating data directories and environment variables
- PubChem dataset or initialization script (for the pubchem service)

## Outputs

- docker-compose.yml with volume mount definitions, named volumes, and service interdependencies
- Verified service orchestration where data persists across container lifecycle events
- Documentation or inline comments specifying which volumes are read-only vs. read-write for each service

## How to apply

First, identify stateful components in your service architecture by tracing data flow: the MAGMa `job` calculation engine requires a PubChem lookup database (produced by the `pubchem` service), the `web` application stores and retrieves job results, and the `joblauncher` webservice coordinates job execution across services. Second, define volume mount points in docker-compose.yml for each stateful service: mount a named volume or bind mount for the PubChem database that both `pubchem` (writes) and `job` (reads) can access, and mount volumes for job results that persist across container restarts. Third, configure volume initialization and health checks: use service dependencies and health checks to ensure the `pubchem` service completes data processing before `job` attempts to use the lookup database. Fourth, validate that mounted paths are consistent across service definitions and match internal application paths (e.g., if the MAGMa job engine expects the database at `/data/pubchem`, mount it there). Test the orchestration by running docker-compose up, verifying that data persists when services are stopped and restarted, and confirming that inter-service data access works correctly.

## Related tools

- **Docker Compose** (Orchestration and volume mount specification for multi-service deployments; defines service interdependencies, volume mounts, networking, and health checks)
- **MAGMa job service** (Calculation engine that reads from PubChem lookup database; requires read access to mounted pubchem volume) — https://github.com/NLeSC/MAGMa
- **MAGMa pubchem service** (Processes PubChem database and writes lookup artifacts; requires write access to shared pubchem volume that job service consumes) — https://github.com/NLeSC/MAGMa
- **MAGMa joblauncher webservice** (Coordinates job execution and result retrieval; depends on job service and may need read/write access to job results volume) — https://github.com/NLeSC/MAGMa
- **MAGMa web application** (Frontend for launching jobs and viewing results; requires read/write access to job results and configuration volumes) — https://github.com/NLeSC/MAGMa

## Examples

```
docker-compose -f docker-compose.yml up --build; sleep 30; docker-compose exec job curl http://pubchem:5000/data/pubchem.db; docker-compose stop; docker-compose start; docker-compose exec job curl http://pubchem:5000/data/pubchem.db
```

## Evaluation signals

- docker-compose.yml syntax is valid (confirmed via `docker-compose config` or `docker-compose up --validate`)
- Named volumes and bind mounts are declared in the top-level `volumes:` section and referenced consistently in service definitions
- Service interdependencies are defined via `depends_on` with health checks ensuring the pubchem service has completed data initialization before job service starts
- Data persists after stopping and restarting services: verify by docker-compose stop, docker-compose start, then confirm job results and lookup database are still accessible
- Inter-service data access works: verify that the job service can read the PubChem lookup database and that results are written to and read from shared volumes across web, joblauncher, and job services

## Limitations

- Docker Compose volume mounts are local to the Docker host; distributed or multi-host persistence requires additional infrastructure (network file systems, cloud storage).
- Named volumes created by docker-compose are not automatically cleaned up and may consume disk space if prune operations are not performed.
- Health checks and depends_on do not guarantee data readiness—if the pubchem service initializes slowly, a simple health check may pass before data is fully written; add explicit wait scripts or data validation in application code.
- No changelog documentation found in the MAGMa repository, so exact data format and API changes across versions are not tracked—persistence schema must be validated manually across upgrades.

## Evidence

- [readme] The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application.: "The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application."
- [readme] The `web` application starts `job` calculations via the `joblauncher` webservice.: "The `web` application starts `job` calculations via the `joblauncher` webservice."
- [other] Configure service interdependencies (e.g., joblauncher depends on job service, magmaweb depends on joblauncher) using depends_on and health checks.: "Configure service interdependencies (e.g., joblauncher depends on job service, magmaweb depends on joblauncher) using depends_on and health checks."
- [other] Add PubChem data service with appropriate initialization and persistence configuration.: "Add PubChem data service with appropriate initialization and persistence configuration."
- [readme] Subproject interdependencies: The `emetabolomics_site` website can be used as starting pages for the `web` application.: "The `emetabolomics_site` website can be used as starting pages for the `web` application."
