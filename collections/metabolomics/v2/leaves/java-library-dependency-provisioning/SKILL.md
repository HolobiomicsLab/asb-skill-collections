---
name: java-library-dependency-provisioning
description: Use when deploying a Java-based scientific application (such as CEU Mass
  Mediator) to an application server and the deployment documentation specifies required
  JAR libraries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3792
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - javax.faces-2.2.12.jar
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

# java-library-dependency-provisioning

## Summary

Identify, obtain, and configure Java library dependencies (JAR files) required by a Java application server to support deployed tools. This skill ensures that all compile-time and runtime JAR dependencies are located, validated, and properly installed in the application server's classpath or library path before deployment.

## When to use

Apply this skill when deploying a Java-based scientific application (such as CEU Mass Mediator) to an application server and the deployment documentation specifies required JAR libraries. Trigger on discovery of JAR file names in deployment instructions, dependency sections of READMEs, or error logs indicating missing classes or libraries at runtime.

## When NOT to use

- The application uses a dependency management tool (Maven, Gradle) that automatically resolves and downloads JAR files — use the build tool instead.
- The JAR file is already present and correctly configured in the application server's classpath — skip to deployment.
- The deployment is for a non-Java application or a fully containerized image where dependencies are already baked in.

## Inputs

- Application server deployment documentation (README or wiki)
- Application server configuration files or classpath specification
- Source code repository (to locate bundled or vendored JAR files)

## Outputs

- Installed JAR files in the application server library path
- Updated application server classpath configuration
- Deployment configuration manifest documenting JAR dependencies and locations

## How to apply

First, parse the deployment documentation (README, setup instructions, or pom.xml) to extract the exact name and version of required JAR files (e.g., javax.faces-2.2.12.jar). Second, verify availability of each JAR by checking the application server's existing library path, public Maven repositories, or the application's source repository. Third, obtain the JAR file through appropriate channels (download from Maven Central, extract from the source repository, or request from the development team). Fourth, place the JAR in the designated location on the application server (typically the lib/ or classpath directory specific to your application server type). Finally, document the JAR dependency location, version, and purpose in a configuration manifest to enable reproducibility and future maintenance.

## Related tools

- **javax.faces-2.2.12.jar** (Required Java Server Faces library providing web framework support for the CEU Mass Mediator application server deployment) — albertogilf/ceuMassMediator

## Evaluation signals

- JAR file is present at the documented location on the application server and is readable by the application server process.
- Application server startup logs do not report ClassNotFoundException or NoClassDefFoundError for classes expected to be in the JAR file.
- The deployed application (e.g., CEU Mass Mediator) loads and functions without runtime library resolution errors.
- Configuration manifest lists all required JARs with version numbers and paths; comparison between manifest and actual filesystem shows 100% match.
- Application server classpath configuration (via CLASSPATH environment variable, catalina.sh, or equivalent) includes the path to the provisioned JAR file.

## Limitations

- JAR version mismatch: provisioning the wrong version of a library can cause runtime failures or incompatibilities; exact version numbers must be verified.
- JAR availability: some proprietary or legacy JAR files may not be publicly available and must be requested from the development team (as in the case of CEU internal database credentials and library access).
- Application server specificity: the correct library path and classpath configuration varies by application server type (Tomcat, JBoss, WebLogic, etc.), requiring adaptation of deployment steps.
- No changelog or version documentation found in the repository, making it difficult to determine which JAR versions are compatible with specific application versions.

## Evidence

- [readme] The next library is needed in the app server: javax.faces-2.2.12.jar: "The next library is needed in the app server: javax.faces-2.2.12.jar"
- [other] Obtain or verify availability of javax.faces-2.2.12.jar library and prepare it for inclusion in the application server library path or classpath.: "Obtain or verify availability of javax.faces-2.2.12.jar library and prepare it for inclusion in the application server library path or classpath."
- [other] Document the deployment configuration (data-source name, JNDI binding, database URL, username, and JAR dependency location) in a configuration manifest or README.: "Document the deployment configuration (data-source name, JNDI binding, database URL, username, and JAR dependency location) in a configuration manifest or README."
