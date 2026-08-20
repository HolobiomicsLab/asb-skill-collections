---
name: java-application-build-verification
description: Use when when you need to confirm that a Java project's GitHub Actions
  workflow (e.g., 'dev_build_release.yml') has completed successfully and generated
  usable build artifacts;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
  - GitHub Actions
  license_tier: open
derived_from:
- doi: 10.1038/s41467-021-23953-9
  title: iimn
evidence_spans:
- mzmine is an open-source software for mass spectrometry data processing
- JDK version-25-blue
- JavaFX version-24
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iimn
    doi: 10.1038/s41467-021-23953-9
    title: iimn
  dedup_kept_from: coll_iimn
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-021-23953-9
  all_source_dois:
  - 10.1038/s41467-021-23953-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# java-application-build-verification

## Summary

Verify that a Java application's automated build workflow (GitHub Actions CI/CD) successfully compiles, produces valid artifacts, and passes integrity checks. This skill validates that development builds are reproducible and deployable without fatal compilation errors.

## When to use

When you need to confirm that a Java project's GitHub Actions workflow (e.g., 'dev_build_release.yml') has completed successfully and generated usable build artifacts; typically after code is pushed to a development or release branch, or when assessing the health of a project's CI/CD pipeline.

## When NOT to use

- The workflow definition itself is malformed or missing; focus first on fixing the .yml file syntax and structure.
- The repository lacks GitHub Actions configured or the workflow file does not exist in .github/workflows.
- Your goal is to modify the Java source code or dependencies; this skill only verifies the build output, not code quality or functionality.

## Inputs

- GitHub repository URL (e.g., github.com/mzmine/mzmine)
- Target branch name (e.g., 'dev', 'main')
- GitHub Actions workflow file path (e.g., .github/workflows/dev_build_release.yml)

## Outputs

- Workflow execution status (success/failure)
- Build log with compilation step details
- Build artifacts (JAR, application bundles, installer packages)
- Artifact integrity validation result (checksum, file size, content inspection)

## How to apply

Access the GitHub Actions workflow file in the .github/workflows directory of the target repository (e.g., mzmine/mzmine). Trigger the workflow via the GitHub Actions web interface or API, targeting the desired branch (e.g., 'dev' or 'main'). Poll the GitHub Actions API or web interface to monitor execution status until completion. Retrieve and inspect the workflow run log to verify that all Java compilation steps completed without fatal errors. Confirm that build artifacts (compiled JAR files, application bundles, or installer packages) were generated and are available for download from the workflow run details. Validate artifact integrity by checking file size, computing checksums, or attempting to extract and inspect the contents of generated files.

## Related tools

- **GitHub Actions** (CI/CD platform that executes the automated build workflow and hosts build artifacts) — https://github.com/mzmine/mzmine
- **JDK 25** (Java Development Kit used by the build process to compile Java source code)
- **JavaFX 24** (Graphics library dependency required for compilation of GUI components in mzmine)
- **mzmine** (Target Java application subject to build verification) — https://github.com/mzmine/mzmine

## Evaluation signals

- Workflow badge status is green/passing (linked from README badge)
- Build log contains no fatal compilation errors, only successful step outputs
- Artifact file exists and has a non-zero size consistent with expected application bundles
- Artifact checksum matches expected value or artifact can be extracted/inspected without corruption
- Build completion timestamp is recent and matches the intentional trigger time

## Limitations

- Workflow execution time may be long; monitor via GitHub API polling or web interface rather than blocking.
- Artifacts are typically retained for only 90 days by GitHub; older workflow runs may not have downloadable artifacts.
- Build success does not imply functional correctness or runtime behavior; it only confirms compilation and packaging completed.
- Repository must have GitHub Actions enabled and the workflow YAML must be syntactically valid; misconfigured workflows will fail before generating artifacts.

## Evidence

- [other] The mzmine repository includes a Development Build Release GitHub Actions workflow (dev_build_release.yml) accessible via badge link, indicating CI/CD automation is configured for the project.: "Development Build Release GitHub Actions workflow (dev_build_release.yml) accessible via badge link, indicating CI/CD automation is configured"
- [other] Trigger the workflow via GitHub Actions API or web interface with the desired branch (e.g., 'dev' or 'main'). Monitor the workflow execution until completion, polling the GitHub Actions API for status updates. Retrieve the build log and verify that all compilation steps completed without fatal errors. Confirm that build artifacts (compiled JAR, application bundles, or installer packages) were generated and are available for download from the workflow run. Validate artifact integrity by checking file size, checksum, or attempting to extract/inspect contents.: "Trigger the workflow via GitHub Actions API or web interface with the desired branch (e.g., 'dev' or 'main'). Monitor the workflow execution until completion, polling the GitHub Actions API for"
- [readme] mzmine should work on Windows, macOS, and Linux using either the installers or the portable versions. There are NO further requirements as mzmine packages a specific Java Virtual Machine.: "mzmine packages a specific Java Virtual Machine. This means the local Java installation has no impact on mzmine."
- [readme] mzmine development requires Java Development Kit (JDK) version 23 or newer: "mzmine development requires Java Development Kit (JDK) version 23 or newer"
