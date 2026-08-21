---
name: shell-environment-setup-and-dependency-management
description: Use when when you need to verify that a GitHub Actions workflow (e.g.,
  main.yml) executes successfully on your local machine, reproduce a reported passing
  or failing CI build status, or debug why a workflow badge reports success/failure.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - git
  - RDKit
  - GitHub Actions
  - Rust (cargo)
  - Python
  - npm/Node.js
  license_tier: open
  provenance_tier: literature
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
  - build: coll_metid
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  dedup_kept_from: coll_metid
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00633
  all_source_dois:
  - 10.1021/acs.analchem.5c00633
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# shell-environment-setup-and-dependency-management

## Summary

Set up a local shell environment and install all dependencies required to execute a project's CI/CD pipeline locally, mirroring the configuration and test commands defined in the workflow file. This skill is essential for reproducing automated build status, debugging workflow failures, and validating that local execution matches CI badge-reported results.

## When to use

When you need to verify that a GitHub Actions workflow (e.g., main.yml) executes successfully on your local machine, reproduce a reported passing or failing CI build status, or debug why a workflow badge reports success/failure. Apply this skill before running integration tests or attempting to replicate the CI pipeline's automated checks outside the GitHub Actions environment.

## When NOT to use

- The GitHub Actions workflow status is already passing on the remote repository and you have no reason to suspect local environment issues.
- Your goal is to understand the workflow definition syntax rather than reproduce its execution; inspect the YAML file directly instead.
- The repository does not provide a workflow file or CI configuration; there is no CI pipeline to reproduce locally.

## Inputs

- GitHub repository URL or local clone (e.g., pbjarterot/Met-ID)
- Workflow definition file (.github/workflows/main.yml or equivalent)
- System environment (Linux, macOS, Windows) matching or compatible with CI runner specification

## Outputs

- Exit status code (0 for pass, non-zero for failure)
- Test output and logs from local test suite execution
- Validation report comparing local execution result to CI badge status
- Captured error logs or stderr/stdout streams if workflow fails

## How to apply

Clone the target repository using git, then inspect the workflow file (e.g., .github/workflows/main.yml) to extract the environment setup commands, dependency installation steps, and test suite invocations. Identify the language runtime(s) required (Rust, Python, TypeScript, etc.) and any build tools (cargo, npm, pip, etc.) referenced. Execute each dependency installation and setup step in sequence on your local machine, capturing any error output. Then run the same test suite commands the CI pipeline defines. Compare the final exit status and test output to the badge-reported status; a match indicates successful reproduction of the CI environment and behavior.

## Related tools

- **git** (Clone the repository from GitHub to obtain the workflow file and source code to execute locally.) — https://git-scm.com/
- **GitHub Actions** (Define and document the CI workflow steps, environment variables, dependency commands, and test invocations that are reproduced locally; can also be used to trigger and monitor workflow execution remotely via API.) — https://github.com/pbjarterot/Met-ID/actions
- **Rust (cargo)** (Build and test system for the Met-ID Tauri/Rust codebase; executes cargo build and test commands extracted from main.yml.) — https://www.rust-lang.org/
- **Python** (Execute Python-based tests or utility scripts defined in the CI workflow, if present in the project.) — https://www.python.org/
- **npm/Node.js** (Install and execute TypeScript/JavaScript dependencies and test commands for the frontend components of Met-ID.) — https://nodejs.org/

## Examples

```
git clone https://github.com/pbjarterot/Met-ID.git && cd Met-ID && cat .github/workflows/main.yml && cargo build && cargo test
```

## Evaluation signals

- Exit code from local test suite matches the CI badge status (0 for passing, non-zero for failing).
- No unresolved dependency errors or missing environment variables during setup and test execution.
- Test output and stderr logs from local execution are identical or semantically equivalent to those produced by the remote CI runner.
- All commands extracted from main.yml (e.g., cargo build, npm test, pytest) execute without modification on the local environment.
- Workflow completion time and resource usage (CPU, memory) are consistent with expectations for the declared runner OS and Rust/TypeScript/Python versions.

## Limitations

- Local OS (Linux, macOS, Windows) and runtime versions (Rust, Python, Node.js) must match or be compatible with those specified in the workflow; mismatches can cause false negatives even if the CI pipeline passes.
- Platform-specific issues may arise (e.g., the README notes 'some issues with adding functional groups on MacOS' for Met-ID); reproducibility may require the exact runner OS used in CI.
- Network-dependent steps (e.g., downloading databases, fetching external resources) may fail or behave differently in isolated local environments; cached artifacts in CI may not be available locally.
- Met-ID is noted as 'under development' in the README; workflow stability and database file synchronization issues may affect reproducibility across version updates.

## Evidence

- [other] Does the Met-ID GitHub repository's CI workflow (main.yml) execute successfully and pass all automated checks as indicated by the badge?: "Does the Met-ID GitHub repository's CI workflow (main.yml) execute successfully and pass all automated checks as indicated by the badge?"
- [other] Inspect the main.yml workflow file in .github/workflows/ to identify the CI steps, environment setup, and test commands.: "Inspect the main.yml workflow file in .github/workflows/ to identify the CI steps, environment setup, and test commands."
- [other] Execute the workflow locally by running the same test suite and dependency installation steps that the CI pipeline defines, or trigger the workflow via GitHub Actions API and monitor its completion.: "Execute the workflow locally by running the same test suite and dependency installation steps that the CI pipeline defines"
- [other] Capture the final pass/fail exit status and any error logs or test output.: "Capture the final pass/fail exit status and any error logs or test output."
- [readme] Met-ID is under development. To help with debugging, a metid_log.log file on the desktop can be sent together with the steps to recreate the error.: "Met-ID is under development. To help with debugging, a metid_log.log file"
- [readme] ![example workflow](https://github.com/pbjarterot/Met-ID/actions/workflows/main.yml/badge.svg): "example workflow badge linked to main.yml"
