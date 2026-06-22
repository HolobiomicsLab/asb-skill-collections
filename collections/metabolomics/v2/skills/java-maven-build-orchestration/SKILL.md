---
name: java-maven-build-orchestration
description: Use when when you have access to a Java project with a Maven pom.xml defining multiple interdependent modules (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Java 21
  - Apache Maven 3.8
  - Git
  - Java
  - Apache Maven
  - Tomcat
derived_from:
- doi: 10.1186/s13321-016-0115-9
  title: MetFrag
evidence_spans:
- Java 21
- Apache Maven 3.8
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# java-maven-build-orchestration

## Summary

Orchestrate multi-module Maven builds for Java projects with explicit dependency resolution and selective compilation. This skill applies when you need to compile a modular Java project (like MetFragRelaunched) that exposes library, command-line, R, and web interface variants from a single source tree.

## When to use

When you have access to a Java project with a Maven pom.xml defining multiple interdependent modules (e.g., MetFragLib as a core dependency for MetFragCommandLine, MetFragR, and MetFragWeb), and you need to build one or more specific modules without compiling the entire repository or want to skip expensive test suites during development cycles.

## When NOT to use

- You only need to run a pre-compiled application (e.g., the ipbhalle/metfragweb Docker image); use Docker instead.
- Your project uses a non-Maven build system (Gradle, Ant, sbt, Bazel); apply the appropriate orchestration skill for that tool.
- You need to develop and iteratively test a single small Java file without module dependencies; use javac or an IDE directly.

## Inputs

- Git repository URL or local clone (ipb-halle/MetFragRelaunched or equivalent multi-module Maven project)
- Java 21 runtime (installed and on PATH)
- Apache Maven 3.8+ (installed and on PATH)
- Maven POM files defining module structure and dependencies

## Outputs

- Compiled JAR artifacts in module-specific target/ directories (e.g., MetFragLib/target/metfrag-lib.jar)
- WAR artifacts for web modules (e.g., MetFragWeb/target/MetFragWeb.war)
- Build logs and console output indicating successful compilation or failure reason

## How to apply

Verify that Java 21 and Apache Maven 3.8+ are installed and on the system PATH. Clone the source repository using git. From the repository root, use Maven's `-pl` (project list) flag to specify target modules and `-am` (also-make) to automatically resolve and compile upstream dependencies. For example, build MetFragLib standalone with `mvn clean install -pl MetFragLib -am`, or build MetFragCommandLine and its dependencies with `mvn clean install -pl MetFragCommandLine -am`. Append `-DskipTests` if you want to skip unit/integration tests to accelerate the build cycle. Monitor the build console for compilation errors and verify that the target JAR artifacts are created in the respective module's `target/` directory with expected naming and non-zero file size. For web modules, use `mvn clean package` instead of `install` if you only need the WAR artifact for deployment to an external Tomcat container.

## Related tools

- **Java** (Runtime and compilation target; MetFragRelaunched requires Java 21 for source compatibility and runtime execution)
- **Apache Maven** (Multi-module build orchestrator; resolves dependencies, compiles modules in dependency order, executes tests, and packages artifacts)
- **Git** (Version control and source acquisition; clone the repository to obtain the full pom.xml hierarchy and source code)
- **Tomcat** (Deployment runtime for MetFragWeb WAR artifacts; the Maven build can also run an embedded Tomcat instance for local testing) — https://hub.docker.com/r/ipbhalle/metfragweb

## Examples

```
mvn clean install -pl MetFragCommandLine -am -DskipTests
```

## Evaluation signals

- Maven build exits with code 0 (success) and displays '[INFO] BUILD SUCCESS' in console output
- Expected JAR/WAR artifacts exist in target/ directories with non-zero file size (e.g., `ls -lh MetFragLib/target/metfrag-lib*.jar` shows size > 1 MB)
- No compilation errors or unresolved dependency errors in the build log; all upstream modules (indicated by `-am`) compiled before their dependents
- If `-DskipTests` was used, verify that tests were skipped without error; if tests were run, all test suites pass or you inspect and accept test failures as non-blocking
- For web modules, the generated WAR can be deployed to Tomcat or the embedded Tomcat test server starts without ClassNotFoundException or NoClassDefFoundError

## Limitations

- Requires Java 21 specifically; earlier or later JDK versions may have compatibility issues with the project's language features or dependencies.
- Maven requires network access to download dependencies from remote repositories; if behind a corporate proxy, proxy settings must be configured in ~/.m2/settings.xml.
- Large test suites (especially integration tests connecting to external databases) can make builds slow; `-DskipTests` trades test confidence for speed and is only safe during rapid development cycles.
- The README indicates that MetFragR module requires additional R-specific build steps (`R CMD check` and `R CMD build`) after the Maven JAR is generated; Maven alone does not produce a fully installable R package.

## Evidence

- [readme] Requirements: Java 21, Apache Maven 3.8: "##### Requirements
- Java 21
- Apache Maven 3.8"
- [readme] Clone repository from GitHub and run mvn clean install: "download sources by cloning git repository
```bash
git clone https://github.com/ipb-halle/MetFragRelaunched.git
```"
- [readme] Build MetFragLib with -pl and -am flags to resolve dependencies: "mvn clean install -pl MetFragLib -am"
- [readme] Skip tests during build with -DskipTests flag: "mvn clean install -pl MetFragLib -am -DskipTests"
- [readme] Build MetFragCommandLine depends on MetFragLib: "MetFrag commandline version depends on MetFragLib"
- [other] Execute mvn clean install or equivalent Maven build command from repository root: "Execute `mvn clean install` or equivalent Maven build command (as defined in the GitHub Actions CI workflow) from the repository root directory."
- [other] Verify successful build by checking JAR artifact in target/ directory: "Confirm successful build completion by verifying the compiled JAR artifact exists in the target/ directory with expected naming convention and non-zero file size."
- [readme] For web modules use mvn clean package to produce WAR file: "if you just want to build the war file to transfer it to another Tomcat instance, run:

```bash
mvn clean package -pl MetFragWeb -am
```"
