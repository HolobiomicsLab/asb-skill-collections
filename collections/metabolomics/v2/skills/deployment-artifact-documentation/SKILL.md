---
name: deployment-artifact-documentation
description: Use when preparing a scientific application (such as a metabolite annotation tool) for deployment to a shared or production app server, particularly when the deployment requires external database access, Java library dependencies, and credential management.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - javax.faces-2.2.12.jar
  - CEU Mass Mediator
derived_from:
- doi: 10.1021/acs.jproteome.8b00720
  title: CEU Mass Mediator 3.0
evidence_spans:
- 'The next library is needed in the app server: javax.faces-2.2.12.jar'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ceu_mass_mediator_3_0_cq
    doi: 10.1021/acs.jproteome.8b00720
    title: CEU Mass Mediator 3.0
  dedup_kept_from: coll_ceu_mass_mediator_3_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00720
  all_source_dois:
  - 10.1021/acs.jproteome.8b00720
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deployment-artifact-documentation

## Summary

Document deployment configuration artifacts (data sources, library dependencies, credentials, JNDI bindings) for reproducible app-server deployment of metabolomics tools. This skill ensures future operators and collaborators can reconstruct the exact runtime environment without trial-and-error.

## When to use

Apply this skill when preparing a scientific application (such as a metabolite annotation tool) for deployment to a shared or production app server, particularly when the deployment requires external database access, Java library dependencies, and credential management. Trigger on: (1) need to hand off deployment to another team member or institution, (2) app requires JDBC data-source configuration, (3) specific JAR library versions are non-standard, or (4) database access is gated behind a contact procedure.

## When NOT to use

- Application has no external database dependency or all credentials are embedded in code (use secrets management instead).
- Deployment target is a containerized environment (e.g., Docker) where configuration is already captured in a Dockerfile or compose file.
- App is a standalone CLI tool with no app-server runtime or shared library requirements.

## Inputs

- app-server type and version identifier
- database connection parameters (URL, credentials, JDBC driver)
- required library list with version numbers and file names
- JNDI or data-source configuration schema for target app server

## Outputs

- deployment configuration manifest or README
- data-source configuration template (XML or app-server format)
- documented list of prerequisite contacts and procedures
- JAR dependency inventory with installation paths

## How to apply

Document the deployment configuration in a structured README or manifest that captures: (1) prerequisite steps (e.g., contact person and email for database access), (2) data-source configuration syntax and required credentials (database URL, username placeholder), (3) library dependencies with exact version numbers and installation location (app-server lib path or classpath), and (4) JNDI binding name and connection parameters. Ground each step in the application's actual architecture: for CEU Mass Mediator, this means explicitly naming the javax.faces library version, specifying that a data-source XML must be created on the app server, and providing [redacted-email] as the contact for CEU database access. Validate completeness by ensuring a new operator could follow the steps without needing to reverse-engineer the original deployment.

## Related tools

- **javax.faces-2.2.12.jar** (JSF (Java Server Faces) library required on app-server classpath for CEU Mass Mediator runtime)
- **CEU Mass Mediator** (metabolite annotation tool requiring documented deployment configuration) — https://github.com/albertogilf/ceuMassMediator

## Evaluation signals

- README explicitly names the database contact person and email ([redacted-email]) so a new operator does not have to search the codebase.
- Data-source configuration template includes all required parameters: database URL, username, password placeholder, and JNDI binding name.
- Library inventory lists exact version numbers (e.g., javax.faces-2.2.12.jar, not just 'javax.faces') and specifies installation location (app-server lib path).
- Deployment steps are in execution order: access request → credential receipt → data-source creation → library installation → validation.
- A practitioner unfamiliar with the project can follow the README and deploy the tool without modifying code or contacting original authors.

## Limitations

- Documentation is only as current as its maintenance; credentials, contact emails, and library URLs may become stale if not kept in sync with actual deployment.
- No changelog was found in the source repository, making it difficult to track deployment changes across versions.
- JDBC data-source configuration syntax varies by app-server type (JBoss, Tomcat, WebSphere, etc.); a single generic template may not cover all targets.
- This skill documents static configuration but does not cover runtime environment validation (e.g., confirming database connectivity, JAR version compatibility at startup).

## Evidence

- [readme] It is necessary to access an internal database of CEU. Request access to [redacted-email].: "It is necessary to access an internal database of CEU. Request access to [redacted-email]."
- [readme] Once you have access to the database, it is needed a data-source from the app server used with the credentials provided.: "Once you have access to the database, it is needed a data-source from the app server used with the credentials provided."
- [readme] The next library is needed in the app server: javax.faces-2.2.12.jar: "The next library is needed in the app server: javax.faces-2.2.12.jar"
- [other] Obtain or verify availability of javax.faces-2.2.12.jar library and prepare it for inclusion in the application server library path or classpath.: "Obtain or verify availability of javax.faces-2.2.12.jar library and prepare it for inclusion in the application server library path or classpath."
- [other] Document the deployment configuration (data-source name, JNDI binding, database URL, username, and JAR dependency location) in a configuration manifest or README.: "Document the deployment configuration (data-source name, JNDI binding, database URL, username, and JAR dependency location) in a configuration manifest or README."
