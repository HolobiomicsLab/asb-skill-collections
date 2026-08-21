---
name: application-server-datasource-configuration
description: Use when when deploying a Java web application (such as CEU Mass Mediator)
  that requires access to a database managed outside the application server, and you
  have obtained database credentials from the maintainers.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - javax.faces-2.2.12.jar
  - CEU Mass Mediator (ceuMassMediator)
  license_tier: open
  provenance_tier: literature
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

# application-server-datasource-configuration

## Summary

Configure a data-source on an application server to enable runtime database connectivity for a deployed Java application. This skill bridges authentication credentials and JNDI binding to allow the application to access an external or internal database without embedding credentials in code.

## When to use

When deploying a Java web application (such as CEU Mass Mediator) that requires access to a database managed outside the application server, and you have obtained database credentials from the maintainers. The trigger is the presence of deployment documentation that specifies a required data-source configuration and the availability of database connection parameters (host, port, username, password, connection URL).

## When NOT to use

- The application uses embedded or hard-coded database credentials—use this skill only when credentials are externalized and managed by the server.
- The application connects directly via JDBC without a data-source layer—this skill is for server-managed connection pooling and JNDI binding.
- Database access is already configured and the application is running successfully—use this skill only during initial deployment or reconfiguration.

## Inputs

- Database credentials (username, password, host, port)
- Database connection URL or connection parameters
- Application server configuration directory or deployment descriptor location
- JNDI binding name (application-specific identifier)

## Outputs

- Data-source configuration file (e.g., datasource XML)
- Verified JNDI binding accessible to the deployed application
- Configuration manifest or deployment documentation

## How to apply

Obtain database credentials by contacting the maintainer (e.g., [redacted-email] for CEU Mass Mediator). Create a data-source configuration file appropriate to your application server (typically an XML file for application servers like JBoss or Tomcat) that specifies the JNDI binding name, database URL, username, password, and driver class. Deploy or reload the configuration file to the application server. Verify that the application can retrieve and use the data-source via JNDI lookup at runtime. Document the data-source name, JNDI binding, and database URL for future maintenance or redeployment.

## Related tools

- **javax.faces-2.2.12.jar** (Required JSF library dependency that must be installed on the application server alongside data-source configuration to support the CEU Mass Mediator web interface.)
- **CEU Mass Mediator (ceuMassMediator)** (The metabolite annotation tool that consumes the configured data-source to access the CEU internal database at runtime.) — https://github.com/albertogilf/ceuMassMediator

## Evaluation signals

- Data-source configuration file is present in the application server's configuration directory and is valid XML (or equivalent format).
- The application server logs show successful data-source binding at startup (e.g., 'data-source X deployed successfully').
- A test query executed via the application (e.g., metabolite search in CEU Mass Mediator) successfully retrieves results, confirming database connectivity.
- JNDI lookup of the configured data-source name from within the application returns a valid connection pool object without null-pointer or naming exceptions.
- Connection pooling metrics (active connections, idle connections) are visible in the application server's admin console and show non-zero activity during application use.

## Limitations

- Credentials must be obtained separately by contacting the database maintainer; this skill does not provision access itself.
- Data-source configuration syntax and location vary by application server type (JBoss, Tomcat, WebLogic, etc.), requiring adaptation of the configuration file format.
- Changes to database credentials (password rotation, host migration) require manual reconfiguration and application server restart, risking downtime.
- No automated testing or changelog mechanism is documented to verify or track configuration changes over time.

## Evidence

- [readme] Request access to CEU internal database: "It is necessary to access an internal database of CEU. Request access to [redacted-email]."
- [readme] Configure data-source with provided credentials: "it is needed a data-source from the app server used with the credentials provided"
- [readme] Install required JSF library: "The next library is needed in the app server: javax.faces-2.2.12.jar"
- [other] Document deployment configuration: "Document the deployment configuration (data-source name, JNDI binding, database URL, username, and JAR dependency location) in a configuration manifest or README."
