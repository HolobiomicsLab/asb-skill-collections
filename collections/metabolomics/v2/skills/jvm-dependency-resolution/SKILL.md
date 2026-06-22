---
name: jvm-dependency-resolution
description: Use when when you have obtained source code for a Maven-based Java project and need to determine whether your local build environment can successfully compile it, or when preparing to reproduce a published CI/CD build workflow from a GitHub Actions or similar pipeline configuration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3346
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Git
  - Java 21
  - Apache Maven 3.8
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
---

# Resolve and verify JVM build dependencies for Maven projects

## Summary

Identify, verify, and confirm the availability of Java Runtime Environment and Apache Maven versions required to successfully compile a Maven-based JVM project from source. This skill ensures that the build environment meets explicit version requirements before attempting compilation.

## When to use

When you have obtained source code for a Maven-based Java project and need to determine whether your local build environment can successfully compile it, or when preparing to reproduce a published CI/CD build workflow from a GitHub Actions or similar pipeline configuration.

## When NOT to use

- Project uses a non-Maven build system (Gradle, Ant, sbt, Bazel, etc.) — consult tool-specific documentation instead.
- You are building a pre-compiled binary or Docker image; dependency resolution may be handled automatically by the container.
- JVM version is already fixed in a locked dependency file (e.g., gradle.lock, pom.lock); direct version verification may be less relevant than dependency constraint checking.

## Inputs

- Maven project source code (local repository or cloned from GitHub)
- Project README or pom.xml file
- GitHub Actions workflow configuration (e.g., .github/workflows/maven.yml)

## Outputs

- Verified Java version string (e.g., 'java version "21"')
- Verified Apache Maven version string (e.g., 'Apache Maven 3.8.x')
- Boolean confirmation that build environment is ready

## How to apply

Consult the project's README, pom.xml, or GitHub Actions CI workflow files to extract the declared Java and Maven version requirements. For the MetFragRelaunched project, the requirements are Java 21 and Apache Maven 3.8. Verify each tool is installed and available in the system PATH by invoking `java -version` and `mvn -v` from the command line. Compare the output version strings against the declared requirements—both must match or exceed the minimum versions stated in the project documentation. Only after confirming both tools meet the requirements should you proceed to execute `mvn clean install` or the equivalent build command specified in the project's CI workflow.

## Related tools

- **Java 21** (Runtime environment required to compile and run the MetFragRelaunched project)
- **Apache Maven 3.8** (Build automation and dependency management tool for executing mvn clean install and resolving transitive dependencies)
- **Git** (Version control tool used to clone the source repository from GitHub) — https://github.com/ipb-halle/MetFragRelaunched.git

## Examples

```
java -version && mvn -v && git clone https://github.com/ipb-halle/MetFragRelaunched.git && cd MetFragRelaunched && mvn clean install
```

## Evaluation signals

- Command `java -version` returns a version string matching or exceeding Java 21 (e.g., '21.0.x' or later).
- Command `mvn -v` returns a version string matching or exceeding Apache Maven 3.8 (e.g., 'Apache Maven 3.8.x' or later).
- Both tools are located in the system PATH and executable from any working directory without full path qualification.
- Subsequent `mvn clean install` from the project root directory completes without JVM version-related or Maven configuration errors.
- Compiled JAR artifact appears in the target/ directory with the expected naming convention and non-zero file size.

## Limitations

- This skill verifies only the declared minimum versions and does not detect incompatibilities between Java 21 and Maven 3.8 on specific operating systems or architectures.
- Version strings returned by `java -version` and `mvn -v` may vary across distributions and packaging methods (e.g., OpenJDK vs. Oracle JDK); manual inspection is required to confirm semantic version equivalence.
- If the project's README is missing or outdated, version requirements may be inferred only from the pom.xml or GitHub Actions workflow, which may not be immediately accessible without cloning the repository.
- Some projects declare version ranges (e.g., Java 21+) rather than exact versions; the skill cannot determine whether a higher version (e.g., Java 22 or 23) will be compatible without attempting a build.

## Evidence

- [other] Java 21 and Apache Maven 3.8 as its core build dependencies: "The MetFragRelaunched project requires Java 21 and Apache Maven 3.8 as its core build dependencies."
- [other] Verify Java 21 and Maven 3.8 availability in system PATH: "Verify Java 21 is installed and available in the system PATH. 3. Verify Apache Maven 3.8 is installed and available in the system PATH."
- [readme] README requirements statement: "##### Requirements
- Java 21
- Apache Maven 3.8"
- [readme] Clone the repository as first workflow step: "download sources by cloning git repository
```bash
git clone https://github.com/ipb-halle/MetFragRelaunched.git
```"
- [other] Artifact verification in target directory: "Confirm successful build completion by verifying the compiled JAR artifact exists in the target/ directory with expected naming convention and non-zero file size."
