---
name: build-artifact-retrieval-and-validation
description: Use when when you need to verify that a GitHub Actions workflow (such as dev_build_release.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
  - GitHub Actions
  - gradle
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# build-artifact-retrieval-and-validation

## Summary

Retrieve and validate build artifacts produced by an automated CI/CD workflow (e.g., GitHub Actions), confirming successful compilation and integrity of generated packages (JAR, installers, portable bundles). This skill ensures that development builds complete without fatal errors and produce usable, uncorrupted distributable artifacts.

## When to use

When you need to verify that a GitHub Actions workflow (such as dev_build_release.yml) has successfully produced deployable artifacts for a Java application, or when you must confirm that compiled binaries, application bundles, or installer packages are present and uncorrupted after an automated build pipeline execution.

## When NOT to use

- Workflow has not been configured or is not present in the repository's .github/workflows directory.
- You are validating a local build performed with gradlew on your machine rather than a remote CI/CD artifact.
- The workflow run has already failed at an early stage (configuration or dependency resolution) before any artifacts could be generated.

## Inputs

- GitHub repository URL (e.g., github.com/mzmine/mzmine)
- Workflow file path (.github/workflows/dev_build_release.yml)
- Target branch name (e.g., 'dev', 'main', or 'master')

## Outputs

- Build log with compilation status and diagnostic messages
- Compiled JAR file(s)
- Platform-specific installer packages (.deb, .exe, .dmg, etc.)
- Portable application bundles
- Artifact checksum or hash for integrity verification
- Validation report confirming artifact completeness and extractability

## How to apply

Access the project's GitHub Actions interface and locate the target workflow file (e.g., dev_build_release.yml in .github/workflows/). Trigger the workflow via the GitHub web interface or API, specifying the desired branch (e.g., 'dev' or 'main'). Monitor execution by polling the GitHub Actions API for status updates until the run completes. Retrieve and inspect the build log to confirm all compilation steps completed without fatal errors. Download the generated artifacts (compiled JAR, application bundles, or platform-specific installers for Windows, macOS, Linux) from the workflow run page. Validate artifact integrity by verifying file size matches expectations, computing or comparing checksums, or attempting to extract and inspect the contents of archives to ensure all required components are present.

## Related tools

- **GitHub Actions** (Automated CI/CD platform that executes the dev_build_release.yml workflow and hosts build artifacts for download) — https://github.com/features/actions
- **gradle** (Build system invoked by the workflow to compile Java source code and package distributions (./gradlew invocation))
- **JDK 25** (Java Development Kit required by mzmine compilation to produce bytecode and packaged artifacts)
- **JavaFX 24** (GUI framework dependency bundled within mzmine artifacts for cross-platform UI functionality)
- **mzmine** (Target application whose automated build artifacts are being retrieved and validated) — https://github.com/mzmine/mzmine

## Evaluation signals

- GitHub Actions workflow run completes with a green 'success' status badge and no fatal error logs in the build output.
- All expected artifact files (JAR, platform-specific installers, portable versions) are present in the workflow run's artifact storage and are downloadable.
- File sizes of downloaded artifacts match expected ranges (e.g., installer ≥ 100 MB; portable ≥ 150 MB; JAR ≥ 50 MB) indicating no truncation or corruption during packaging.
- Computed SHA-256 or MD5 checksum of retrieved artifacts matches a reference checksum published alongside the workflow output.
- Archive extraction (e.g., unzip portable bundle, inspect .deb or .exe internal structure) succeeds without errors and confirms presence of required binaries, libraries, and configuration files (e.g., Java runtime, JavaFX modules, mzmine executable).

## Limitations

- Artifact retention policies on GitHub may cause older workflow runs' artifacts to be automatically deleted after a retention period (default 90 days); only recent development builds may be retrievable.
- The workflow's success status does not guarantee runtime correctness or functional testing of the application — only that compilation and packaging succeeded without fatal build errors.
- Validation via checksum or extraction is a file-integrity check only; it does not verify that the application will execute correctly on target platforms or that all runtime dependencies (e.g., system libraries on Linux) are installed.
- Cross-platform artifacts (Windows .exe, macOS .dmg, Linux .deb) produced by a single workflow may require platform-specific environment setup in the CI runner; artifacts for platforms not explicitly supported by the workflow may not be generated.

## Evidence

- [other] workflow_definition: "The mzmine repository includes a Development Build Release GitHub Actions workflow (dev_build_release.yml) accessible via badge link, indicating CI/CD automation is configured for the project."
- [other] workflow_steps: "1. Access the mzmine/mzmine GitHub repository and locate the 'dev_build_release.yml' workflow file in the .github/workflows directory. 2. Trigger the workflow via GitHub Actions API or web interface"
- [readme] build_output_format: "The final mzmine distribution will be placed in build/jpackage"
- [readme] platform_coverage: "Download options include portable versions and installers for the Window, macOS, and Linux."
- [readme] runtime_packaging: "There are **NO** further requirements as mzmine packages a specific Java Virtual Machine."
