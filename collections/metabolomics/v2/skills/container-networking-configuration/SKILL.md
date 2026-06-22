---
name: container-networking-configuration
description: Use when when deploying a multi-component research application (e.g., MAGMa's four subproject services) as containerized microservices that need to communicate internally—specifically when you have identified service interdependencies (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - MAGMa
  - Docker Compose
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# container-networking-configuration

## Summary

Configure inter-service networking and dependencies in Docker Compose to orchestrate multiple containerized microservices as a cohesive system. This skill ensures that services can discover and communicate with each other while respecting startup order and health constraints.

## When to use

When deploying a multi-component research application (e.g., MAGMa's four subproject services) as containerized microservices that need to communicate internally—specifically when you have identified service interdependencies (e.g., web application depends on joblauncher, joblauncher depends on job service, job depends on pubchem database) and need to define those relationships in an orchestration manifest.

## When NOT to use

- Input is a single monolithic application with no separate microservices—use standard containerization instead.
- Service dependencies are unknown or poorly documented—defer networking configuration until architecture is clarified.
- Deployment target requires advanced orchestration features (e.g., Kubernetes service mesh, multi-host networking, auto-scaling)—use a container orchestration platform instead of Docker Compose.

## Inputs

- GitHub repository structure of multi-service project (e.g., NLeSC/MAGMa)
- Existing Dockerfiles or build scripts for each component
- Project documentation describing service roles and dependencies
- Service configuration details (ports, environment variables, volume mounts)

## Outputs

- docker-compose.yml manifest with service definitions, networking configuration, and interdependencies
- Validated orchestration that successfully builds and runs all composed services with inter-service communication

## How to apply

Parse the repository structure and documentation to identify service interdependencies (e.g., which services call or depend on other services). Define each service's container specification in docker-compose.yml with explicit depends_on directives that capture startup ordering and optional health checks. Configure internal networking by specifying exposed ports and inter-service communication via service names (Docker's internal DNS resolves container names to IPs). For services with external interfaces (e.g., web application, joblauncher webservice), map container ports to host ports. Validate the docker-compose.yml syntax and test the orchestration workflow by building and running the composed services to confirm that service-to-service communication succeeds.

## Related tools

- **Docker Compose** (Define and orchestrate multi-container application services with networking and dependency configuration)
- **MAGMa** (Reference implementation of multi-service metabolomics research platform requiring container orchestration) — https://github.com/NLeSC/MAGMa

## Evaluation signals

- docker-compose.yml passes syntax validation (e.g., `docker-compose config` succeeds without errors)
- All four services (magmaweb, joblauncher, job, pubchem) start without crashing or hanging
- Service-to-service communication succeeds (e.g., joblauncher can reach job service via internal hostname, web app can reach joblauncher)
- Startup order respects dependencies (e.g., job service is healthy before joblauncher attempts to connect)
- External ports are accessible from the host and internal ports are not exposed unless required

## Limitations

- Docker Compose is designed for single-host development and testing; for production multi-host deployments, use Kubernetes or other orchestration platforms.
- Health checks are best-effort and may not catch transient network failures or slow service startup; additional monitoring and retry logic may be needed.
- Service interdependencies documented in README (e.g., 'web application starts job calculations via joblauncher webservice') must be manually translated into docker-compose.yml; no automated inference is performed.

## Evidence

- [readme] Service interdependency structure: "The `web` application starts `job` calculations via the `joblauncher` webservice."
- [readme] Identified architectural components: "Subprojects: emetabolomics_site - The http://www.emetabolomics.org website, job - Runs MAGMa calculation, joblauncher - Webservice to execute jobs, pubchem - Processing of PubChem database"
- [other] Multi-service deployment workflow: "Configure service interdependencies (e.g., joblauncher depends on job service, magmaweb depends on joblauncher) using depends_on and health checks."
- [other] Orchestration validation step: "Validate docker-compose.yml syntax and test orchestration workflow by building and running the composed services."
