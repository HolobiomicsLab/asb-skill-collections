---
name: release-branch-management
description: 'Use when you need to validate that a software project''s release branch is stable and ready for distribution. Specifically, use it when: (1) a release tag has been created or code pushed to a release branch; (2) you need to confirm that CI/CD pipelines execute without failures;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - GitHub Actions
  - SIRIUS
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-021-01045-9
  all_source_dois:
  - 10.1038/s41587-021-01045-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# release-branch-management

## Summary

Verify that a release branch's Build and Publish CI workflow executes successfully and produces passing artifacts. This skill is essential for confirming that code on a release branch is production-ready and that distribution pipelines (binaries, installers, SDKs) are correctly generated.

## When to use

Apply this skill when you need to validate that a software project's release branch is stable and ready for distribution. Specifically, use it when: (1) a release tag has been created or code pushed to a release branch; (2) you need to confirm that CI/CD pipelines execute without failures; (3) you want to verify that build artifacts (installers, binaries, archives) are successfully generated and published; or (4) you are validating the integrity of a release before announcing it to users.

## When NOT to use

- Do not use this skill for validating development or feature branches; it is specific to release branches where distribution and stability are critical.
- Do not apply this skill if the workflow configuration has not yet been reviewed or if trigger conditions are unknown—first inspect the workflow file to understand its behavior.
- Do not use this skill as a substitute for manual testing or functional validation of the released software; it confirms only that the CI pipeline ran successfully, not that the software itself works correctly.

## Inputs

- GitHub repository (e.g., sirius-ms/sirius)
- Workflow configuration file (.github/workflows/distribute.yaml or equivalent)
- Release tag or branch push trigger event
- Repository README containing status badge markup

## Outputs

- GitHub Actions workflow run log with exit status
- Workflow status badge indicating 'passing' or 'failed'
- Published build artifacts (installers, binaries, archives)
- Verification report confirming successful build and publish completion

## How to apply

First, navigate to the target repository's GitHub Actions tab and identify the workflow file (e.g., distribute.yaml in .github/workflows) that orchestrates the build and publish pipeline. Review the workflow's trigger conditions to understand whether it fires on release tags, pushes to the release branch, or both. Trigger the workflow by either creating a release tag (e.g., v6.3.7) or pushing to the designated release branch (e.g., release-4-pre), depending on the workflow configuration. Monitor the GitHub Actions run logs in real-time, checking for compilation errors, dependency failures, or test breakage. Once the run completes, verify that the workflow status badge in the repository README shows 'passing' or 'success' (typically indicated by green coloring), and inspect the Actions tab to confirm the overall run status displays 'passed'. For critical releases, download and spot-check the generated artifacts (e.g., .msi, .pkg, .zip installers) to ensure they are present and correctly named.

## Related tools

- **GitHub Actions** (CI/CD platform that executes the Build and Publish workflow, monitors logs, and reports pass/fail status via status badge.) — https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml
- **SIRIUS** (Target software project being tested; the build and publish workflow compiles, packages, and distributes SIRIUS binaries for Windows, macOS, and Linux.) — https://github.com/sirius-ms/sirius

## Evaluation signals

- Workflow run status in GitHub Actions tab is marked 'passed' (not 'failed' or 'cancelled').
- Status badge in repository README displays green 'passing' indicator and links to the correct branch (e.g., release-4-pre).
- Workflow logs show no compilation errors, failed tests, or critical warnings; all build steps complete successfully.
- Published artifacts are present on the releases page (e.g., .msi, .pkg, .zip files for SIRIUS v6.3.7) with correct naming and file sizes.
- Workflow execution time is within expected range (no unusual hangs or excessive delays indicative of infrastructure problems).

## Limitations

- GitHub Actions workflow status reflects only CI/CD pipeline success, not functional correctness of the released software; passing CI does not guarantee the application runs or behaves correctly.
- Workflow badge displays the status of the last run on the specified branch; if multiple commits are pushed rapidly, an older badge may temporarily reflect an outdated status until the latest run completes.
- External service dependencies (e.g., artifact repositories, code signing services, web endpoints) may fail intermittently, causing the workflow to fail even if the code is correct; transient failures require re-triggering.
- Status badge URL must reference the correct branch parameter (e.g., ?branch=release-4-pre); badges without explicit branch specification may show status from an unexpected branch, leading to misinterpretation.

## Evidence

- [other] Examine the distribute.yaml workflow file in the .github/workflows directory to understand the build and publish pipeline.: "Examine the distribute.yaml workflow file in the .github/workflows directory to understand the build and publish pipeline."
- [other] Monitor the GitHub Actions run until completion, tracking logs for any failures or warnings.: "Monitor the GitHub Actions run until completion, tracking logs for any failures or warnings."
- [other] Verify that the workflow run status shows 'passed' in the Actions tab.: "Verify that the workflow run status shows 'passed' in the Actions tab."
- [other] Inspect the repository README to confirm the build badge displays a passing status (typically indicated by 'passing' or 'success' label and green coloring).: "Inspect the repository README to confirm the build badge displays a passing status (typically indicated by 'passing' or 'success' label and green coloring)."
- [readme] [![Build and Publish](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml/badge.svg?branch=release-4-pre)](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml): "[![Build and Publish](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml/badge.svg?branch=release-4-pre)]"
- [readme] These installer packages are signed by Bright Giant to verify the package provider's identity, and should therefore trigger no or only mild security warnings from the operating system during installation.: "These installer packages are signed by Bright Giant to verify the package provider's identity"
