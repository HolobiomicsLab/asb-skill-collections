---
name: github-actions-api-integration
description: Use when when you need to verify that a GitHub Actions workflow (such as a development build or release pipeline) executes without fatal errors and produces expected artifacts. Use this skill when the workflow is already configured in a repository (e.g., a .yml file in .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
  - GitHub Actions
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
---

# github-actions-api-integration

## Summary

Programmatically trigger and monitor GitHub Actions workflows via the GitHub Actions API to validate CI/CD pipelines and retrieve build artifacts. This skill enables automated verification that a project's build and release workflows complete successfully and produce usable artifacts.

## When to use

When you need to verify that a GitHub Actions workflow (such as a development build or release pipeline) executes without fatal errors and produces expected artifacts. Use this skill when the workflow is already configured in a repository (e.g., a .yml file in .github/workflows/) and you need to programmatically trigger it, poll its status, and validate the resulting build outputs.

## When NOT to use

- The GitHub Actions workflow has not yet been configured or does not exist in the repository's .github/workflows directory.
- You do not have API access credentials or sufficient permissions to trigger workflows or access artifacts in the target repository.
- The workflow is expected to fail (e.g., testing a known bug), and you need to analyze why it failed rather than verify a passing build.

## Inputs

- GitHub repository URL (e.g., github.com/mzmine/mzmine)
- Workflow file name (e.g., dev_build_release.yml)
- Target branch name (e.g., dev, main)
- GitHub API token or credentials

## Outputs

- Workflow execution status (success/failure/in_progress)
- Build log (compilation output and error messages)
- Artifact metadata (list of generated files, download URLs, file sizes, checksums)
- Artifact integrity validation report

## How to apply

First, identify the target workflow file (e.g., 'dev_build_release.yml') in the repository's .github/workflows directory. Trigger the workflow via the GitHub Actions API with the desired branch (e.g., 'dev' or 'main'). Poll the GitHub Actions API for status updates until the workflow reaches a terminal state (success or failure). Once complete, retrieve and parse the build log to confirm all compilation steps executed without fatal errors. Finally, validate artifact integrity by checking artifact availability, file size, checksums, or by extracting and inspecting contents to confirm the expected deliverables (e.g., compiled JAR files, application bundles, or installer packages) were generated.

## Related tools

- **GitHub Actions** (CI/CD automation platform that executes workflows; API provides endpoints to trigger runs, poll status, and retrieve logs and artifacts) — https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml
- **mzmine** (Target build artifact—the software package whose compilation is validated by the GitHub Actions workflow) — https://github.com/mzmine/mzmine
- **JDK 25** (Java compiler and runtime required to build mzmine; must be available in the GitHub Actions runner environment)
- **JavaFX 24** (GUI framework dependency required for mzmine compilation and packaging into application bundles)

## Evaluation signals

- Workflow execution completes without timing out and transitions to a terminal state (success or failure).
- Build log shows zero fatal compilation errors and confirms all required build steps completed (e.g., JAR compilation, JavaFX packaging).
- Artifacts are present and downloadable from the workflow run; file listing includes expected types (e.g., .jar, .deb, .exe, .dmg, .tar.gz).
- Artifact integrity checks pass: file sizes are non-zero and reasonable for a mass spectrometry data processing suite; checksums (if provided) are valid.
- Artifact extraction/inspection succeeds (e.g., JAR can be opened, installer packages contain expected binaries and resources).

## Limitations

- API rate limits may apply; frequent polling may require exponential backoff or GitHub App authentication to avoid throttling.
- Workflow execution time and artifact availability depend on GitHub Actions infrastructure availability and runner queue depth; transient failures may occur.
- Artifacts are typically retained for a limited time (default 90 days on GitHub); long-term validation requires separate artifact storage.
- Validation confirms that artifacts were generated but does not verify functional correctness or runtime behavior of the compiled software (e.g., whether mzmine actually processes mass spectrometry data correctly).

## Evidence

- [other] Trigger the workflow via GitHub Actions API or web interface with the desired branch (e.g., 'dev' or 'main'). Monitor the workflow execution until completion, polling the GitHub Actions API for status updates.: "Trigger the workflow via GitHub Actions API or web interface with the desired branch (e.g., 'dev' or 'main'). Monitor the workflow execution until completion, polling the GitHub Actions API for"
- [other] Retrieve the build log and verify that all compilation steps completed without fatal errors. Confirm that build artifacts (compiled JAR, application bundles, or installer packages) were generated and are available for download from the workflow run.: "Retrieve the build log and verify that all compilation steps completed without fatal errors. Confirm that build artifacts (compiled JAR, application bundles, or installer packages) were generated and"
- [other] Validate artifact integrity by checking file size, checksum, or attempting to extract/inspect contents.: "Validate artifact integrity by checking file size, checksum, or attempting to extract/inspect contents."
- [other] Access the mzmine/mzmine GitHub repository and locate the 'dev_build_release.yml' workflow file in the .github/workflows directory.: "Access the mzmine/mzmine GitHub repository and locate the 'dev_build_release.yml' workflow file in the .github/workflows directory."
- [other] The mzmine repository includes a Development Build Release GitHub Actions workflow (dev_build_release.yml) accessible via badge link, indicating CI/CD automation is configured for the project.: "The mzmine repository includes a Development Build Release GitHub Actions workflow (dev_build_release.yml) accessible via badge link, indicating CI/CD automation is configured for the project."
