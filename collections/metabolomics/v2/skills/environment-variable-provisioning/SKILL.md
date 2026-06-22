---
name: environment-variable-provisioning
description: Use when when extending a multi-service project (like MAGMa with its four subproject components) to container orchestration, and you need to ensure each microservice (magmaweb, joblauncher, job, pubchem) receives the correct configuration—such as port mappings, service URLs, and data paths—without.
license: CC-BY-4.0
metadata:
  edam_topics: []
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# environment-variable-provisioning

## Summary

Configure environment variables for containerized microservices in a multi-component orchestration system. This skill defines service-specific variables (ports, database connections, inter-service dependencies) that enable correct communication and resource allocation across containerized components.

## When to use

When extending a multi-service project (like MAGMa with its four subproject components) to container orchestration, and you need to ensure each microservice (magmaweb, joblauncher, job, pubchem) receives the correct configuration—such as port mappings, service URLs, and data paths—without hardcoding values into container images.

## When NOT to use

- Single monolithic application without inter-service dependencies—use simple environment files or hardcoded defaults instead.
- Services already deployed in a managed cloud platform (e.g., Kubernetes with ConfigMaps)—use platform-native configuration instead.
- Legacy components that cannot be containerized or do not support environment variable injection.

## Inputs

- GitHub repository structure (NLeSC/MAGMa)
- Existing Dockerfiles and build scripts
- Service documentation and dependency specifications
- Service configuration files (build configs, environment examples)

## Outputs

- docker-compose.yml with service specifications
- Validated service environment variable mappings
- Inter-service networking and health check configuration
- Running orchestrated microservices with correct variable injection

## How to apply

Extract service dependencies and configuration requirements from existing build scripts, Dockerfiles, and documentation (e.g., joblauncher depends on job service; magmaweb depends on joblauncher). Define environment variables in the docker-compose.yml specification for each service, mapping ports (e.g., magmaweb on port 80/443, joblauncher on service port), database/data paths, and inter-service URLs. Configure depends_on and health checks to establish service startup order and readiness signals. Validate syntax and test the orchestration workflow by building and running the composed services to confirm that environment variables are correctly injected and services can communicate. Check container logs and service health endpoints to verify that each microservice resolved its dependencies correctly.

## Related tools

- **Docker Compose** (Orchestration format and runtime for defining service specifications, environment variables, port mappings, volumes, and inter-service networking.)
- **MAGMa** (Source system being containerized; comprises four subproject services (magmaweb, joblauncher, job, pubchem) whose interdependencies and configurations must be provisioned.) — https://github.com/NLeSC/MAGMa

## Evaluation signals

- docker-compose.yml passes syntax validation and composes without errors.
- Container logs show successful startup and no unresolved environment variable references (e.g., no 'key not found' errors).
- Inter-service communication tests pass: joblauncher successfully resolves the job service endpoint, magmaweb successfully resolves joblauncher, and pubchem data is accessible to the job service.
- Service health checks return healthy status after startup; depends_on ordering ensures dependent services are ready before dependents start.
- Comparison of provisioned variables against documentation confirms port assignments, data paths, and database URLs match intended architecture.

## Limitations

- Docker Compose is single-host orchestration; for distributed deployments, Kubernetes or other multi-node systems require ConfigMaps, Secrets, or other platform-specific mechanisms.
- Secrets (API keys, passwords) should not be stored in docker-compose.yml; use .env files or Secrets management instead.
- The MAGMa project README does not document all required environment variables—extraction may require inference from source code or experimental validation.
- Health checks and service readiness depend on correct port and endpoint configuration; mismatched ports will cause failed dependency resolution even if environment variables are correctly set.

## Evidence

- [readme] The MAGMa project comprises four distinct subproject components with interdependencies.: "The MAGMa project is organized into four distinct subprojects: emetabolomics_site (website), job (calculation engine), joblauncher (webservice), and pubchem (data processing)"
- [readme] Service interdependencies require correct environment configuration for startup and communication.: "The `emetabolomics_site` website can be used as starting pages for the `web` application. The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application."
- [other] Define service specifications including ports, environment variables, volume mounts, and inter-service networking in docker-compose.yml.: "Define service specifications in docker-compose.yml including image names, ports, environment variables, volume mounts, and inter-service networking."
- [other] Configure service interdependencies and health checks to establish startup order.: "Configure service interdependencies (e.g., joblauncher depends on job service, magmaweb depends on joblauncher) using depends_on and health checks."
- [other] Validate docker-compose through syntax and runtime orchestration testing.: "Validate docker-compose.yml syntax and test orchestration workflow by building and running the composed services."
