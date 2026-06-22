---
name: git-repository-cloning-and-version-control
description: Use when when you need to reproduce a computational workflow described in a GitHub repository, validate CI/CD pipeline definitions (e.g., GitHub Actions workflows), inspect source code structure, or execute local versions of automated tests.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - git
  - RDKit
  - GitHub Actions
derived_from:
- doi: 10.1021/acs.analchem.5c00633
  title: metid
evidence_spans:
- Clone the Met-ID repository
- Powered by RDKit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metfrag
    doi: 10.1186/s13321-016-0115-9
    title: MetFrag
  - build: coll_metid
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  dedup_kept_from: coll_metid
schema_version: 0.2.0
---

# git-repository-cloning-and-version-control

## Summary

Clone a remote Git repository to a local development environment and inspect version-controlled artifacts (e.g., workflow files, source code) to understand project structure, CI/CD configuration, and reproducibility prerequisites. This skill is essential for reproducing computational workflows and validating automated checks defined in repository metadata.

## When to use

When you need to reproduce a computational workflow described in a GitHub repository, validate CI/CD pipeline definitions (e.g., GitHub Actions workflows), inspect source code structure, or execute local versions of automated tests. Specifically applicable when a repository displays a CI badge (e.g., GitHub Actions status badge) and you must clone the repository and examine the workflow file (e.g., .github/workflows/main.yml) to understand what the badge claims to monitor.

## When NOT to use

- Repository does not use Git version control or is not publicly accessible on GitHub
- You only need to download a single release artifact (e.g., .msi, .dmg, or .deb installer); use direct release download instead
- The repository has no CI/CD workflow defined or does not expose a workflow badge; focus on source code inspection alone

## Inputs

- Remote Git repository URL (e.g., https://github.com/pbjarterot/Met-ID.git)
- GitHub repository name and owner (pbjarterot/Met-ID)
- Workflow file path (.github/workflows/main.yml)
- Git version control system (local or remote)

## Outputs

- Local repository directory with full commit history and all branches
- Parsed workflow YAML file defining CI pipeline steps
- CI/CD execution logs (stdout/stderr from workflow runs)
- Pass/fail exit status from workflow execution
- Reproducibility assessment document (workflow status matches badge claim or not)

## How to apply

Use `git clone` to copy the remote repository (pbjarterot/Met-ID) to your local machine, preserving the full commit history and branch structure. Navigate to the `.github/workflows/` directory to locate workflow definition files (e.g., main.yml) that define the CI pipeline steps, environment setup, and test commands. Inspect the workflow YAML to identify the sequence of steps (install dependencies, run tests, build artifacts) that the automated CI system executes. If reproducing the workflow locally, execute the same dependency installation and test commands in your environment, or trigger the workflow via the GitHub Actions API and monitor its completion status. Document the exit status and any error logs to verify whether the workflow completes successfully and matches the CI badge-reported status.

## Related tools

- **git** (Version control system for cloning the remote repository and inspecting commit history and branch structure) — https://git-scm.com/
- **GitHub Actions** (CI/CD platform used by Met-ID (main.yml workflow) to execute automated checks; workflow definitions are inspected and optionally triggered via API) — https://github.com/pbjarterot/Met-ID/actions

## Examples

```
git clone https://github.com/pbjarterot/Met-ID.git && cd Met-ID && cat .github/workflows/main.yml
```

## Evaluation signals

- Repository cloned successfully and local directory contains all source files and .git metadata
- Workflow file (main.yml) is located in .github/workflows/ and contains valid YAML syntax with defined CI steps
- Workflow execution (local or via GitHub Actions API) completes without fatal errors and produces an exit code 0 (success) or documented non-zero code (failure)
- CI badge displayed in repository README matches the reported workflow completion status (passing/failing)
- Dependency installation and test commands extracted from workflow YAML are reproducible and produce consistent results in a clean environment

## Limitations

- Repository access requires network connectivity and GitHub authentication if the repository is private; public repositories like pbjarterot/Met-ID do not require credentials
- Workflow reproduction depends on availability of the same runtime environment (OS, language versions, system libraries); differences in OS, Python version, Rust version, or Node.js version may cause the workflow to fail locally even if it passes in the CI environment
- GitHub Actions workflows may depend on secrets (API keys, credentials) not available in the repository; such steps may fail or be skipped during local reproduction
- The workflow badge reflects only the most recent commit status on a specific branch (typically main); historical or branch-specific CI failures are not captured by the badge display

## Evidence

- [other] Clone the pbjarterot/Met-ID repository from GitHub using git. Inspect the main.yml workflow file in .github/workflows/ to identify the CI steps, environment setup, and test commands.: "Clone the pbjarterot/Met-ID repository from GitHub using git. Inspect the main.yml workflow file in .github/workflows/ to identify the CI steps, environment setup, and test commands."
- [other] Execute the workflow locally by running the same test suite and dependency installation steps that the CI pipeline defines, or trigger the workflow via GitHub Actions API and monitor its completion.: "Execute the workflow locally by running the same test suite and dependency installation steps that the CI pipeline defines, or trigger the workflow via GitHub Actions API and monitor its completion."
- [other] The Met-ID repository displays a GitHub Actions workflow badge linked to main.yml, indicating the presence of automated CI pipeline execution tracking.: "The Met-ID repository displays a GitHub Actions workflow badge linked to main.yml, indicating the presence of automated CI pipeline execution tracking."
- [readme] ![example workflow](https://github.com/pbjarterot/Met-ID/actions/workflows/main.yml/badge.svg): "![example workflow](https://github.com/pbjarterot/Met-ID/actions/workflows/main.yml/badge.svg)"
