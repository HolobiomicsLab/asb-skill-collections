---
name: ci-workflow-reproduction
description: Use when you have access to a GitHub repository with a Maven-based CI workflow (e.g., defined in .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Git
  - Java
  - Apache Maven
  - GitHub Actions
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- git clone https://github.com/ipb-halle/MetFragRelaunched.git
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metfrag
    doi: 10.1186/s13321-016-0115-9
    title: MetFrag
  dedup_kept_from: coll_metfrag
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-016-0115-9
  all_source_dois:
  - 10.1186/s13321-016-0115-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# CI Workflow Reproduction

## Summary

Reproduce a software project's continuous integration (CI) build pipeline locally by cloning the source repository and executing the build automation steps defined in the project's CI configuration. This skill validates that the project's documented build dependencies and workflow are sufficient to successfully compile the software from source.

## When to use

You have access to a GitHub repository with a Maven-based CI workflow (e.g., defined in .github/actions/workflows/) and need to verify that the project can be built independently outside the CI environment, troubleshoot build failures, or validate that build dependencies are correctly documented and reproducible on a developer machine.

## When NOT to use

- The project uses a build system other than Maven (e.g., Gradle, Ant, CMake) — refer to the project's language-specific build documentation instead.
- You lack local network access to clone from GitHub or download Maven dependencies from remote repositories.
- The project requires platform-specific setup (e.g., native C++ compilation, Docker) that is not addressed in the README's core build section.

## Inputs

- GitHub repository URL (e.g., https://github.com/ipb-halle/MetFragRelaunched.git)
- System with Java 21 and Apache Maven 3.8 installed
- CI workflow file (.github/actions/workflows/maven.yml or equivalent)

## Outputs

- Compiled JAR artifact in target/ directory
- Build log confirming successful completion
- Validated build environment configuration

## How to apply

Clone the source repository using git to obtain the complete project source tree and CI configuration files. Verify that the required build tools (Java 21, Apache Maven 3.8) are installed and available in the system PATH. Examine the repository's README or GitHub Actions workflow file to identify the exact Maven command(s) executed during CI (e.g., `mvn clean install`). Execute the identified Maven command from the repository root directory. Verify successful completion by checking for the expected compiled artifact in the target/ directory with the correct naming convention and non-zero file size. If the build fails, compare your local environment (Java version, Maven version, PATH settings) against the README's stated requirements.

## Related tools

- **Java** (Compiler and runtime required to build and run the Maven-based project)
- **Apache Maven** (Build automation and dependency management tool that executes the CI workflow commands)
- **Git** (Version control system used to clone the source repository from GitHub)
- **GitHub Actions** (CI platform defining the reference workflow to reproduce locally) — https://github.com/ipb-halle/MetFragRelaunched/actions/workflows/maven.yml

## Examples

```
git clone https://github.com/ipb-halle/MetFragRelaunched.git && cd MetFragRelaunched && mvn clean install
```

## Evaluation signals

- Build completes with exit code 0 and no ERROR or FAILURE messages in the Maven log.
- Compiled JAR artifact exists at the expected path (e.g., MetFragRelaunched/target/*.jar) with non-zero file size.
- The artifact's naming convention matches the project's version scheme as specified in the README or pom.xml.
- All documented build dependencies (Java 21, Maven 3.8) are confirmed installed and accessible in the system PATH before build execution.
- Build output matches the expected behavior described in the README's Build and Run section (e.g., 'after the successful build Tomcat web server runs on port 8080').

## Limitations

- The skill reproduces the build environment but does not guarantee functional correctness of the compiled artifact — unit tests or integration tests may still fail.
- Local environment differences (OS, network firewall, proxy settings, disk space) may cause builds to fail even when dependencies are nominally installed.
- If a changelog is unavailable (as noted in the source cards), breaking changes between versions may not be detected until runtime.
- The skill assumes the CI workflow in the repository is current and compatible with the stated Java 21 and Maven 3.8 versions; older snapshots or branches may require different versions.

## Evidence

- [other] Java 21 and Apache Maven 3.8 as its core build dependencies.: "The MetFragRelaunched project requires Java 21 and Apache Maven 3.8 as its core build dependencies."
- [readme] Cloning and Maven command execution from repository root.: "download sources by cloning git repository
git clone https://github.com/ipb-halle/MetFragRelaunched.git"
- [readme] Maven build command definition.: "Execute `mvn clean install` or equivalent Maven build command (as defined in the GitHub Actions CI workflow) from the repository root directory."
- [other] Artifact verification criteria.: "Confirm successful build completion by verifying the compiled JAR artifact exists in the target/ directory with expected naming convention and non-zero file size."
- [readme] Requirements stated in README.: "##### Requirements
- Java 21
- Apache Maven 3.8"
