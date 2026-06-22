---
name: ci-cd-pipeline-reproducibility-verification
description: Use when when a repository displays a GitHub Actions workflow badge (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ci-cd-pipeline-reproducibility-verification

## Summary

Verify that a GitHub Actions CI/CD workflow executes successfully locally and produces results matching the reported badge status. This skill validates the integrity and reproducibility of automated pipeline execution by comparing local test runs against the official CI logs.

## When to use

When a repository displays a GitHub Actions workflow badge (e.g. a passing status indicator) and you need to confirm that the claimed CI status is accurate, that the workflow steps are reproducible outside the GitHub environment, and that all dependencies and test commands are correctly specified in the workflow definition file.

## When NOT to use

- Workflow definition file is unavailable or repository is private without access credentials.
- The workflow requires secrets, external APIs, or hardware (e.g. GPU, specialized instruments) that cannot be replicated locally.
- The goal is to audit code quality or security rather than verify pipeline execution reproducibility.

## Inputs

- GitHub repository URL (pbjarterot/Met-ID or equivalent)
- Workflow definition file (.github/workflows/main.yml)
- Environment specification (OS, language version, dependencies)
- Test command(s) as defined in workflow YAML

## Outputs

- Local test execution log with exit status
- Pass/fail result summary
- Comparison report: local status vs. badge-reported status
- Error logs or test output (if failures occur)

## How to apply

Clone the repository and inspect the workflow definition file (main.yml) located in .github/workflows/ to identify CI steps, environment setup, dependency installation, and test commands. Execute the same test suite and dependency steps locally by running the commands defined in the workflow, capturing exit status and test output. Optionally, trigger the workflow via the GitHub Actions API and monitor its completion. Compare the local exit status and test results against the badge-reported status and any publicly visible CI logs. Document matches or discrepancies to confirm reproducibility.

## Related tools

- **git** (Clone the repository to obtain workflow definition and source code) — https://git-scm.com
- **GitHub Actions** (Define, monitor, and trigger CI/CD workflows; retrieve execution logs and badge status) — https://github.com/pbjarterot/Met-ID/actions
- **RDKit** (Execute chemistry-specific test steps defined in the workflow) — https://www.rdkit.org/

## Examples

```
git clone https://github.com/pbjarterot/Met-ID.git && cd Met-ID && cat .github/workflows/main.yml && npm install && npm test
```

## Evaluation signals

- Local test execution exit status (0 = success) matches badge-reported passing or failing state.
- All dependency installation and environment setup steps complete without errors.
- Test output and error logs are identical or semantically equivalent between local run and GitHub Actions run.
- Workflow YAML is syntactically valid and all referenced commands are executable in the specified environment.
- No file system, permission, or environment variable errors occur during local execution that would invalidate reproducibility.

## Limitations

- GitHub Actions may execute on hardware or configurations not available locally (e.g. multiple OS images, cached dependencies), making perfect reproducibility impossible in some cases.
- Workflow secrets (API keys, credentials) are not accessible outside GitHub Actions, requiring manual substitution or mocking.
- Time-dependent tests (e.g. rate limits, scheduled tasks) may produce different results when run outside the intended CI environment.
- The repository is noted as 'under development'; workflow stability and test coverage may be incomplete or subject to change without notice.

## Evidence

- [other] The Met-ID repository displays a GitHub Actions workflow badge linked to main.yml, indicating the presence of automated CI pipeline execution tracking.: "The Met-ID repository displays a GitHub Actions workflow badge linked to main.yml, indicating the presence of automated CI pipeline execution tracking."
- [other] Inspect the main.yml workflow file in .github/workflows/ to identify the CI steps, environment setup, and test commands.: "Inspect the main.yml workflow file in .github/workflows/ to identify the CI steps, environment setup, and test commands."
- [other] Execute the workflow locally by running the same test suite and dependency installation steps that the CI pipeline defines, or trigger the workflow via GitHub Actions API and monitor its completion.: "Execute the workflow locally by running the same test suite and dependency installation steps that the CI pipeline defines, or trigger the workflow via GitHub Actions API and monitor its completion."
- [other] Capture the final pass/fail exit status and any error logs or test output. Document whether the workflow completed successfully and matches the badge-reported passing status.: "Capture the final pass/fail exit status and any error logs or test output. Document whether the workflow completed successfully and matches the badge-reported passing status."
- [readme] Met-ID is under development. To help with debugging, a metid_log.log file on the desktop can be sent together with the steps to recreate the error.: "Met-ID is under development. To help with debugging, a metid_log.log file on the desktop can be sent together with the steps to recreate the error."
