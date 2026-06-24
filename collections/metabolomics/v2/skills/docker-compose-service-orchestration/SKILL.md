---
name: docker-compose-service-orchestration
description: Use when when a research software project is decomposed into distinct
  subproject components (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MAGMa
  - Docker
  - docker-compose
  license_tier: open
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# docker-compose-service-orchestration

## Summary

Orchestrate multi-service containerized applications using docker-compose.yml to define and manage interdependent microservices (web frontend, calculation engine, job launcher, data processing) with shared networking, volume mounts, and health checks. This skill is essential when a research platform comprises multiple loosely coupled components that must be deployed, networked, and scaled together.

## When to use

When a research software project is decomposed into distinct subproject components (e.g., website, calculation engine, webservice, data processing) that are already containerized or have Dockerfiles, and you need to define how these services discover each other, share data, and initialize in the correct dependency order for reproducible multi-environment deployment.

## When NOT to use

- Input is a monolithic single-container application; use docker build/run directly instead.
- Services require complex Kubernetes-level features (e.g., rolling updates, multi-node scheduling, auto-scaling); use Kubernetes manifests instead.
- Project components do not have well-defined service boundaries or unclear interdependencies that have not been documented.

## Inputs

- GitHub repository structure (subproject directories)
- Existing Dockerfiles for each subproject component
- Build scripts and build configuration files
- Project documentation (README, architecture descriptions)
- Environment requirements and service interdependency specifications

## Outputs

- docker-compose.yml manifest
- Validated service orchestration configuration
- Functional multi-service deployment ready for development or production

## How to apply

First, parse the project repository structure to identify distinct subproject services and their roles (e.g., MAGMa's emetabolomics_site, job, joblauncher, pubchem, and web). Extract or infer service configurations from existing Dockerfiles, build scripts, and README documentation, including image names, exposed ports, environment variables, and data volume requirements. Define each service in docker-compose.yml with image references, port mappings, environment variable definitions, and volume mounts; configure inter-service dependencies using the 'depends_on' directive and health checks to ensure correct initialization order. For data-dependent services (e.g., pubchem lookup database), configure initialization and persistence volumes. Finally, validate the composed manifest syntax and test the orchestration by building and running all composed services together to verify inter-service networking and workflow.

## Related tools

- **Docker** (Container runtime engine that executes individual service images defined in the compose manifest)
- **docker-compose** (Command-line tool that parses docker-compose.yml and orchestrates service lifecycle (build, start, stop, health checks))
- **MAGMa** (Multi-component chemo-informatics platform whose four subproject services (emetabolomics_site, job, joblauncher, pubchem, web) are defined and networked via docker-compose) — https://github.com/NLeSC/MAGMa

## Examples

```
docker-compose up --build
```

## Evaluation signals

- docker-compose.yml passes validation without syntax errors (docker-compose config succeeds)
- All four service images build successfully without errors (docker-compose build exits 0)
- Services start in dependency order: pubchem initializes before job, job before joblauncher, joblauncher before web (inspect docker-compose logs for startup sequence)
- Inter-service DNS resolution works: joblauncher resolves 'job' hostname and pubchem lookup service is accessible to job service (test with docker exec)
- Health checks pass for all services within defined timeout windows (docker ps shows 'healthy' status); data volumes persist across restart cycles (verify with docker volume inspect)

## Limitations

- docker-compose is optimized for single-host development/testing deployments; production multi-host orchestration requires Kubernetes or Docker Swarm.
- Service interdependency ordering via 'depends_on' does not guarantee true readiness—only container startup order; explicit health checks must be defined to wait for service initialization.
- Environment variable substitution in docker-compose.yml requires careful management of .env files; secrets should not be hardcoded in the manifest.
- The MAGMa pubchem data processing service requires initialization and a populated lookup database; the compose configuration must include explicit volume persistence and init logic to ensure data consistency across restarts.

## Evidence

- [other] The MAGMa project is organized into four distinct subprojects: emetabolomics_site (website), job (calculation engine), joblauncher (webservice), and pubchem (data processing), which can be deployed as separate containerized services.: "The MAGMa project is organized into four distinct subprojects: emetabolomics_site (website), job (calculation engine), joblauncher (webservice), and pubchem (data processing), which can be deployed"
- [other] Define service specifications in docker-compose.yml including image names, ports, environment variables, volume mounts, and inter-service networking. Configure service interdependencies (e.g., joblauncher depends on job service, magmaweb depends on joblauncher) using depends_on and health checks.: "Define service specifications in docker-compose.yml including image names, ports, environment variables, volume mounts, and inter-service networking. Configure service interdependencies (e.g.,"
- [readme] The `web` application starts `job` calculations via the `joblauncher` webservice.: "The `web` application starts `job` calculations via the `joblauncher` webservice."
- [readme] The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application.: "The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application."
- [other] Validate docker-compose.yml syntax and test orchestration workflow by building and running the composed services.: "Validate docker-compose.yml syntax and test orchestration workflow by building and running the composed services."
