---
name: java-build-artifact-validation
description: Use when when you need to verify that a Java project's automated build pipeline (GitHub Actions workflow) executes without errors and generates distributable artifacts (e.g., .deb installers, portable binaries, or .jar files).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
  - GitHub Actions
derived_from:
- doi: 10.1038/s41587-023-01690-2
  title: mzmine3
evidence_spans:
- mzmine is an open-source software for mass spectrometry data processing
- JDK version-25-blue
- JavaFX version-24
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzmine3
    doi: 10.1038/s41587-023-01690-2
    title: mzmine3
  dedup_kept_from: coll_mzmine3
schema_version: 0.2.0
---

# java-build-artifact-validation

## Summary

Validate that a Java application build workflow completes successfully and produces expected executable artifacts. This skill monitors GitHub Actions CI/CD pipelines, retrieves build logs and artifacts, and documents pass/fail outcomes to verify reproducibility of development releases.

## When to use

When you need to verify that a Java project's automated build pipeline (GitHub Actions workflow) executes without errors and generates distributable artifacts (e.g., .deb installers, portable binaries, or .jar files). Use this skill when assessing whether a development build release workflow for a multi-platform Java application (Windows, macOS, Linux) completes successfully and produces platform-specific installers or artifacts.

## When NOT to use

- Input is a pre-built binary or already-packaged release (not a CI/CD workflow run)
- Workflow is private or access credentials are not available to retrieve logs and artifacts
- The Java project does not use GitHub Actions or does not expose workflow runs publicly

## Inputs

- GitHub Actions workflow URL (e.g., https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml)
- Repository commit hash or branch reference (default: master/main branch state)
- Build environment specification (JDK version, JavaFX version, OS targets)

## Outputs

- Workflow execution status (pass/fail/error)
- Build artifact manifest (file names, sizes, download links for portable and installer distributions)
- Structured report file (timestamp, workflow status, artifact links, error logs if applicable)
- Build log excerpts documenting dependency resolution and compilation steps

## How to apply

Access the GitHub Actions workflow page for the target repository (e.g., https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml). Retrieve the most recent workflow run and examine the execution logs to identify pass/fail status. For mzmine specifically, verify that JDK 25 and JavaFX 24 dependencies are correctly resolved during the build. Document the workflow status, timestamp, any error messages, and links to produced artifacts (portable versions, installers for Windows/macOS/Linux). Compare artifact checksums or metadata against expected outputs to confirm build reproducibility. Record all findings in a structured report file with workflow URL, status badge, execution logs excerpt, and artifact inventory.

## Related tools

- **mzmine** (Java application whose build workflow is validated; requires JDK 25 and JavaFX 24 to build successfully) — https://github.com/mzmine/mzmine
- **JDK 25** (Java Development Kit version required to compile mzmine source code) — http://jdk.java.net
- **JavaFX 24** (Graphics toolkit dependency required for mzmine GUI; must be resolved during build)
- **GitHub Actions** (CI/CD platform that executes the dev_build_release.yml workflow and produces platform-specific installers) — https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml

## Evaluation signals

- Workflow badge status at https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml shows 'passing' or 'failing' clearly
- Build log contains no fatal compilation errors; all dependencies (JDK 25, JavaFX 24) resolved successfully
- Artifact inventory includes all expected platform-specific files: .deb installer for Linux, .dmg or .pkg for macOS, .msi or .exe for Windows
- Final build output directory (build/jpackage for mzmine) contains executable artifacts with non-zero file sizes
- Workflow execution timestamp and artifact links are populated in the structured report; report matches most recent run on master branch

## Limitations

- Workflow access and artifact visibility depend on repository permissions; private repositories or restricted artifacts cannot be validated externally
- Build success does not guarantee runtime correctness or functional testing; only confirms compilation and packaging steps completed
- JDK and JavaFX version requirements are version-specific (mzmine currently requires JDK 25+ and JavaFX 24); builds may fail if workflow uses incompatible versions
- No changelog is currently available in the mzmine repository, limiting ability to correlate build artifacts with specific code changes or fixes

## Evidence

- [other] Access the GitHub Actions workflow page at https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml. Retrieve the most recent workflow run status and execution logs.: "Access the GitHub Actions workflow page at https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml. Retrieve the most recent workflow run status and execution logs."
- [readme] mzmine development requires Java Development Kit (JDK) version 23 or newer: "mzmine development requires Java Development Kit (JDK) version 23 or newer (http://jdk.java.net)."
- [readme] To build the mzmine package from the sources, run the following command: ./gradlew. The final mzmine distribution will be placed in build/jpackage: "To build the mzmine package from the sources, run the following command: ./gradlew […] The final mzmine distribution will be placed in build/jpackage"
- [readme] Download options include portable versions and installers for the Window, macOS, and Linux.: "Download options include portable versions and installers for the Window, macOS, and Linux."
- [readme] [![Development Build Release](https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml/badge.svg)](https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml): "[![Development Build Release](https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml/badge.svg)](https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml)"
