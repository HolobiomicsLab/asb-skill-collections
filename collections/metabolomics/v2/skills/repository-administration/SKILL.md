---
name: repository-administration
description: Use when you need to validate that a scientific software project's continuous integration pipeline is functional and producing reproducible builds—particularly before releasing new versions, after merging changes to release branches, or when troubleshooting build failures that block distribution of.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - GitHub Actions
  - SIRIUS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# repository-administration

## Summary

Verify and monitor the build and publish CI/CD pipeline for a scientific software repository to ensure successful compilation, testing, and artifact distribution across multiple platforms. This skill confirms that automated workflows execute correctly and produce passing build status on designated release branches.

## When to use

Apply this skill when you need to validate that a scientific software project's continuous integration pipeline is functional and producing reproducible builds—particularly before releasing new versions, after merging changes to release branches, or when troubleshooting build failures that block distribution of compiled artifacts.

## When NOT to use

- The repository does not use GitHub Actions or has no CI/CD pipeline configured.
- You are testing local compilation without artifact distribution requirements.
- The workflow is designed for internal development only and does not target multiple platforms or release channels.

## Inputs

- GitHub repository with configured GitHub Actions workflows
- distribute.yaml or equivalent CI/CD workflow file
- Release branch or version tag identifier
- README with workflow status badge URL

## Outputs

- GitHub Actions workflow run log (passed/failed status)
- Compiled distribution artifacts (installers, archives)
- Workflow status badge displaying pass/fail state
- Build summary report (job durations, step results)

## How to apply

Navigate to the GitHub repository and locate the distributed workflow configuration file (e.g., distribute.yaml in .github/workflows/) to understand the trigger conditions and build stages. Trigger the workflow by pushing to the designated release branch or creating a release tag, depending on the trigger specification in the workflow file. Monitor the GitHub Actions run log in real time, examining build output and test results for errors or warnings. Upon completion, verify that the workflow status badge (typically displayed in the repository README) shows a passing state. Cross-reference the Actions tab to confirm all job steps executed successfully and that artifacts were generated for all target platforms (Windows, macOS, Linux; both x86-64 and ARM architectures if applicable).

## Related tools

- **GitHub Actions** (Continuous integration and workflow orchestration service used to execute automated build and publish pipelines) — https://github.com/sirius-ms/sirius
- **SIRIUS** (Java-based software framework being built and distributed via the CI/CD pipeline) — https://github.com/sirius-ms/sirius

## Evaluation signals

- GitHub Actions 'Build and Publish' workflow run status is marked as 'passed' or 'success' in the Actions tab
- Repository README displays a workflow status badge with green coloring indicating successful build
- Build log shows no unresolved errors or critical warnings during compilation and packaging stages
- Compiled distribution artifacts are present and accessible for all declared target platforms (Windows x86-64, macOS x86-64, macOS ARM64, Linux x86-64, Linux ARM64)
- Workflow execution completes within expected time bounds and no job timeouts or cancellations are logged

## Limitations

- GitHub Actions execution depends on repository secrets and external service availability (e.g., package repositories, signing services); network failures or credential expiration can cause false negatives.
- Build status badges reflect only the most recent workflow run; historical runs or branch-specific results require navigation to the Actions tab.
- Some workflow failures may originate from upstream dependencies or third-party service outages rather than repository code; log inspection is required to distinguish root causes.

## Evidence

- [other] Examine the distribute.yaml workflow file in the .github/workflows directory to understand the build and publish pipeline.: "Examine the distribute.yaml workflow file in the .github/workflows directory to understand the build and publish pipeline."
- [other] Trigger the 'Build and Publish' workflow by creating a release tag or pushing to the release branch, depending on the workflow trigger conditions specified in distribute.yaml.: "Trigger the 'Build and Publish' workflow by creating a release tag or pushing to the release branch, depending on the workflow trigger conditions specified in distribute.yaml."
- [other] Monitor the GitHub Actions run until completion, tracking logs for any failures or warnings.: "Monitor the GitHub Actions run until completion, tracking logs for any failures or warnings."
- [other] Verify that the workflow run status shows 'passed' in the Actions tab.: "Verify that the workflow run status shows 'passed' in the Actions tab."
- [other] Inspect the repository README to confirm the build badge displays a passing status (typically indicated by 'passing' or 'success' label and green coloring).: "Inspect the repository README to confirm the build badge displays a passing status (typically indicated by 'passing' or 'success' label and green coloring)."
- [readme] [![Build and Publish](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml/badge.svg?branch=release-4-pre)](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml): "[![Build and Publish](https://github.com/sirius-ms/sirius/actions/workflows/distribute.yaml/badge.svg?branch=release-4-pre)]"
- [readme] These versions include the Java Runtime Environment, so there is no need to install Java separately! Just download, install/unpack and execute.: "These versions include the Java Runtime Environment, so there is no need to install Java separately!"
- [readme] for Windows (x86-64/amd64/x64), Mac (x86-64/amd64/x64), Mac (arm64/aarch64/apple silicon), Linux (x86-64/amd64/x64), Linux (arm64/aarch64): "for Windows (x86-64/amd64/x64): [msi] / [zip]; for Mac (x86-64/amd64/x64); for Mac (arm64/aarch64/apple silicon); for Linux (x86-64/amd64/x64); for Linux (arm64/aarch64)"
