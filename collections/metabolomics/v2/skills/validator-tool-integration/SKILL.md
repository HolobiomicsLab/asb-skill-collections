---
name: validator-tool-integration
description: Use when you have a repository of structured records (e.g., mass spectrometry data, metadata, or domain-specific formats) and need to enforce validation rules systematically across all records.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - MassBank-web Validator
  - GitHub Actions
  - MassBank-cli-tools
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1002/jms.1777
  title: MassBank
evidence_spans:
- Validator from MassBank-web
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massbank_cq
    doi: 10.1002/jms.1777
    title: MassBank
  dedup_kept_from: coll_massbank_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/jms.1777
  all_source_dois:
  - 10.1002/jms.1777
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# validator-tool-integration

## Summary

Integrate a dedicated validator tool into a continuous integration (CI) workflow to automatically validate all records in a repository against a defined schema or specification. This skill ensures data quality and consistency are checked on every commit or pull request without manual intervention.

## When to use

You have a repository of structured records (e.g., mass spectrometry data, metadata, or domain-specific formats) and need to enforce validation rules systematically across all records. Use this skill when manual validation is impractical, when records are frequently updated or contributed by multiple authors, and when you want validation results to be visible and traceable (e.g., via status badges).

## When NOT to use

- Records are already validated upstream and immutable before repository ingestion — integration here is redundant.
- Validation rules are ad-hoc, undocumented, or change frequently without formal specification — the overhead of maintaining a CI validator exceeds its benefit.
- Validator tool does not exist or cannot be reliably invoked in a CI environment (e.g., requires interactive UI, large external dependencies, or unreliable network calls).

## Inputs

- Repository containing all records (MassBank record files or equivalent structured data)
- Validator tool (Java CLI, Python module, or containerized executable)
- GitHub Actions workflow definition (YAML) or equivalent CI configuration
- Schema or validation specification (implicit in the Validator implementation)

## Outputs

- Validation status report (JSON or CSV format)
- Pass/fail outcome per record and record set
- CI status badge (displayed in README or branch view)
- Pipeline success/failure signal (blocks or permits merge)

## How to apply

Set up a GitHub Actions workflow (or equivalent CI system) that triggers on commits to your main and dev branches. Configure the workflow to invoke a dedicated Validator tool (either embedded in your codebase or retrieved from a companion library/repository) against all records in the repository. The Validator should parse each record, check conformance to a schema or specification, and output results in a machine-readable format (JSON or CSV) that itemizes pass/fail outcomes per record or record set. Generate a validation status report and optionally expose the results via CI status badges so that branch health is immediately visible. Use exit codes to fail the CI pipeline if validation fails, blocking merges of non-conformant records.

## Related tools

- **GitHub Actions** (CI/CD orchestration engine that schedules and executes the validator workflow on every commit or pull request) — https://github.com/features/actions
- **MassBank-web Validator** (Dedicated validator tool that checks MassBank records for schema conformance and structural correctness) — https://github.com/MassBank/MassBank-web
- **MassBank-cli-tools** (Command-line interface containing validator and other tools for MassBank record validation) — https://github.com/MassBank/MassBank-cli-tools

## Evaluation signals

- All records in the repository pass validation; the validation status badge shows 'passing' for both main and dev branches.
- When an invalid record is committed, the GitHub Actions workflow fails immediately, blocking merge until the record is corrected.
- Validation report (JSON or CSV) is generated and contains one entry per record with explicit pass/fail status and error messages.
- Validator exit code is 0 on success and non-zero on failure, allowing CI pipeline to make merge decisions based on validation outcome.
- Validation results are reproducible: running the validator locally on the same records produces identical pass/fail outcomes as the CI pipeline.

## Limitations

- Validator tool must be compatible with the CI environment (GitHub Actions, GitLab CI, etc.) and not require interactive input or graphical display.
- Schema or validation rules must be formally defined and stable; ad-hoc or frequently changing rules undermine the reliability of automated validation.
- Large repositories may experience CI timeout or resource constraints if the validator is slow; performance tuning may be required.
- The validator's error messages and diagnostic output depend on the tool's implementation; unclear or verbose errors can reduce usability for contributors.

## Evidence

- [intro] The MassBank-data repository uses GitHub Actions to validate the content of all records with the Validator from MassBank-web: "uses GitHub Actions to validate the content of all records with the Validator from MassBank-web"
- [readme] Validation status badges are displayed for main and dev branches: "main branch [![Main Validation Status](https://github.com/MassBank/MassBank-data/actions/workflows/validate-records.yml/badge.svg?branch=main)] ... dev branch [![Dev Validation"
- [other] Validation workflow outputs results in machine-readable format per record set: "Output the validation report in a machine-readable format (JSON or CSV)"
- [readme] The validator is invoked via GitHub Actions validate-records.yml workflow: "Trigger the GitHub Actions validate-records.yml workflow in the MassBank-data repository"
