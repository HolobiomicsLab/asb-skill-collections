---
name: ci-cd-workflow-triggering
description: Use when you need to verify that a GitHub Actions workflow (such as dev_build_release.yml) successfully completes end-to-end, especially after code changes or to confirm that automated build infrastructure is functioning correctly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
  - GitHub Actions
  techniques:
  - MS-imaging
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

# CI/CD Workflow Triggering

## Summary

Trigger and monitor automated build and release workflows in GitHub Actions to validate that development branches produce passing build artifacts without manual intervention. This skill verifies CI/CD pipeline completeness and artifact generation for mass spectrometry software distributions.

## When to use

Use this skill when you need to verify that a GitHub Actions workflow (such as dev_build_release.yml) successfully completes end-to-end, especially after code changes or to confirm that automated build infrastructure is functioning correctly. Apply it when you must validate that compiled artifacts (JAR files, application bundles, installers) are generated and ready for distribution across target platforms (Windows, macOS, Linux).

## When NOT to use

- When you only need to inspect the workflow definition itself without executing it; use static code review instead.
- When the repository does not expose a GitHub Actions workflow or does not use GitHub as its CI/CD platform.
- When local or offline testing of the build is required without triggering remote CI pipelines.

## Inputs

- GitHub repository URL (e.g., mzmine/mzmine)
- Target branch name (e.g., 'dev', 'main')
- Workflow file name (e.g., dev_build_release.yml)

## Outputs

- Workflow execution status (pass/fail)
- Build log output
- Compiled artifacts (JAR, installer packages, application bundles)
- Artifact checksums and metadata
- Workflow run ID and timestamp

## How to apply

Locate the target workflow file in the .github/workflows directory of the repository (e.g., dev_build_release.yml in mzmine/mzmine). Trigger the workflow by calling the GitHub Actions API or web interface, specifying the desired branch (e.g., 'dev' or 'main'). Poll the GitHub Actions API for status updates until the workflow completes. Retrieve the build log and scan for fatal compilation errors or warnings that would prevent artifact generation. Confirm that build artifacts (compiled JAR, application bundles, or platform-specific installers for Windows, macOS, and Linux) were generated and are available for download from the workflow run details. Validate artifact integrity by inspecting file size, checksums, or attempting to extract and inspect contents to ensure the build is complete and uncorrupted.

## Related tools

- **GitHub Actions** (CI/CD platform used to define and execute automated build and release workflows) — https://github.com/mzmine/mzmine/actions/workflows/dev_build_release.yml
- **JDK 25** (Java Development Kit required to compile mzmine source code during workflow execution)
- **JavaFX 24** (Graphics toolkit required for mzmine GUI compilation and packaging)
- **mzmine** (Target application being built and released via the workflow) — https://github.com/mzmine/mzmine

## Evaluation signals

- Workflow execution completes without timeout or cancellation; GitHub Actions API status field returns 'completed' with conclusion 'success'.
- Build log contains no fatal errors (ERROR-level messages in compilation steps); all compilation tasks report success.
- At least one artifact file is present in the workflow run's artifacts section with a file size consistent with a full application bundle (not zero or suspiciously small).
- Artifact integrity check passes: checksums match expected values, or compressed archives can be successfully extracted and contain expected directory/file structure.
- Platform-specific installers or portable versions are generated for the intended targets (Windows .exe or .msi, macOS .dmg, Linux .deb packages mentioned in README).

## Limitations

- Workflow triggering and monitoring are only possible if the GitHub repository is public or the user has appropriate access permissions to the Actions API.
- GitHub Actions API rate limits may apply for high-frequency polling of workflow status.
- Artifact retention policies on GitHub may expire old build artifacts, making historical validation unavailable after a retention period.
- Workflow success does not guarantee runtime correctness on all target platforms; integration or functional testing must be performed separately.

## Evidence

- [other] Trigger the workflow via GitHub Actions API or web interface with the desired branch (e.g., 'dev' or 'main'). 3. Monitor the workflow execution until completion, polling the GitHub Actions API for status updates.: "Trigger the workflow via GitHub Actions API or web interface with the desired branch (e.g., 'dev' or 'main'). 3. Monitor the workflow execution until completion, polling the GitHub Actions API for"
- [other] Retrieve the build log and verify that all compilation steps completed without fatal errors. 5. Confirm that build artifacts (compiled JAR, application bundles, or installer packages) were generated and are available for download from the workflow run.: "Retrieve the build log and verify that all compilation steps completed without fatal errors. 5. Confirm that build artifacts (compiled JAR, application bundles, or installer packages) were generated"
- [other] The mzmine repository includes a Development Build Release GitHub Actions workflow (dev_build_release.yml) accessible via badge link, indicating CI/CD automation is configured for the project.: "The mzmine repository includes a Development Build Release GitHub Actions workflow (dev_build_release.yml) accessible via badge link, indicating CI/CD automation is configured for the project."
- [readme] mzmine should work on Windows, macOS, and Linux using either the installers or the portable versions. There are **NO** further requirements as mzmine packages a specific Java Virtual Machine.: "mzmine should work on Windows, macOS, and Linux using either the installers or the portable versions. There are **NO** further requirements as mzmine packages a specific Java Virtual Machine."
- [readme] The final mzmine distribution will be placed in build/jpackage: "The final mzmine distribution will be placed in build/jpackage"
