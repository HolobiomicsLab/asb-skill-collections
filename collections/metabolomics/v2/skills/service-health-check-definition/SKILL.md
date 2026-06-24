---
name: service-health-check-definition
description: 'Use when when deploying a multi-service microarchitecture (such as MAGMa''s
  four distinct subprojects: magmaweb, joblauncher, job, and pubchem) via Docker Compose
  and you need to ensure that service startup order respects true readiness rather
  than container existence—particularly when services have.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0361
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - MAGMa
  - Docker Compose
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

# service-health-check-definition

## Summary

Define and configure health checks for containerized microservices in a Docker Compose orchestration to monitor service readiness and inter-service dependencies. Health checks enable the orchestrator to validate that dependent services are running correctly before allowing downstream services to start or retry communication.

## When to use

When deploying a multi-service microarchitecture (such as MAGMa's four distinct subprojects: magmaweb, joblauncher, job, and pubchem) via Docker Compose and you need to ensure that service startup order respects true readiness rather than container existence—particularly when services have initialization overhead (e.g., database population, webservice binding) or when one service depends on another's API availability.

## When NOT to use

- Services are stateless and have no initialization overhead—simple container existence checks may suffice.
- Health checks would create circular dependencies or deadlock conditions (e.g., service A checks service B, which checks service A).
- The deployment target does not support Docker Compose health checks (very old Docker Engine versions < 1.12).

## Inputs

- MAGMa GitHub repository structure and Dockerfiles
- Service dependency graph (e.g., joblauncher→job, magmaweb→joblauncher, job→pubchem lookup database)
- Existing docker-compose.yml template or configuration fragments
- Service startup logs and initialization behavior documentation

## Outputs

- docker-compose.yml with healthcheck directives for all services
- Validated orchestration configuration with depends_on conditions
- Service health status verification log (from docker-compose up)

## How to apply

Extract service interdependencies from the project documentation and codebase (e.g., joblauncher depends on job service, magmaweb depends on joblauncher). For each service, identify its startup completion signal: port binding readiness, HTTP endpoint responsiveness, database initialization, or file presence. Define health check commands in docker-compose.yml using the `healthcheck` directive with an interval (e.g., 10s), timeout (e.g., 5s), and retry threshold (e.g., 3 failures before marking unhealthy). Configure the `depends_on` clause to use `condition: service_healthy` for critical paths. Validate the composed configuration by building and running services in order, observing container logs and health status via `docker-compose ps` to confirm that downstream services wait for upstream readiness before initialization.

## Related tools

- **Docker Compose** (Orchestration and service dependency management; defines healthcheck directives and depends_on conditions for service startup sequencing)
- **MAGMa** (Target multi-service project with four containerized subprojects (emetabolomics_site, job, joblauncher, pubchem) requiring health-check-driven orchestration) — https://github.com/NLeSC/MAGMa

## Evaluation signals

- docker-compose.yml syntax validates without errors (docker-compose config succeeds)
- Each service's healthcheck command is executable and responsive within the defined timeout; `docker-compose ps` shows (healthy) status for all services
- Dependent services (e.g., joblauncher) do not attempt to start until their dependencies (e.g., job service) report healthy status
- Service startup logs confirm that downstream services wait for upstream readiness; no connection-refused or timeout errors from joblauncher→job or magmaweb→joblauncher communication
- Full orchestration workflow (build and run) completes successfully; all services reach healthy state and inter-service networking is functional

## Limitations

- Health checks are service-level and cannot directly verify end-to-end application logic correctness; a service may report healthy but still fail at higher layers (e.g., calculation logic errors in the job service).
- PubChem data service initialization may be slow or data-dependent; health checks must account for variable initialization duration and may require tuning of retry counts and intervals.
- Docker Compose health checks do not cover orchestration scenarios beyond container readiness (e.g., resource exhaustion, network partitions, or gradual performance degradation); monitoring and alerting require additional tools.
- No changelog documentation found for the MAGMa project; health check configurations may become stale as service APIs and startup behaviors evolve.

## Evidence

- [readme] Service interdependencies and configuration: "The `emetabolomics_site` website can be used as starting pages for the `web` application. The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application."
- [readme] Four distinct containerizable subprojects: "Subprojects: emetabolomics_site - The http://www.emetabolomics.org website, job - Runs MAGMa calculation, joblauncher - Webservice to execute jobs, pubchem - Processing of PubChem database"
- [other] Orchestration configuration workflow from task: "Configure service interdependencies (e.g., joblauncher depends on job service, magmaweb depends on joblauncher) using depends_on and health checks."
- [other] Validation via orchestration execution: "Validate docker-compose.yml syntax and test orchestration workflow by building and running the composed services."
