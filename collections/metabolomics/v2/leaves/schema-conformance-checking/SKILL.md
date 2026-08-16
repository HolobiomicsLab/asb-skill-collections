---
name: schema-conformance-checking
description: Use when you have a collection of records in a standardized format (e.g.,
  MassBank plain-text or structured records) that must be validated before commit
  or publication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - MassBank-web Validator
  - GitHub Actions
  - MassBank-cli-tools
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1002/jms.1777
  title: MassBank
evidence_spans: []
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# schema-conformance-checking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automated validation of structured scientific records (e.g., mass spectrometry data) against a formal schema to detect field presence, data type, value range, and format violations. This skill ensures that records conform to defined standards before integration into a shared repository.

## When to use

Apply this skill when you have a collection of records in a standardized format (e.g., MassBank plain-text or structured records) that must be validated before commit or publication. Triggers include: new records added to a version-controlled repository, pull requests requiring automated quality gates, or periodic validation runs to detect schema drift in existing data.

## When NOT to use

- Records are already validated and certified by an upstream authority; re-running the full schema check is redundant.
- Input format is unstructured text or image data that cannot be parsed into named fields.
- The schema specification is unknown, unstable, or not machine-readable.

## Inputs

- MassBank record files (plain-text or structured format)
- Record metadata fields (accession, name, formula, mass, spectrum peaks)
- Schema or format specification defining valid field names, types, ranges, and patterns

## Outputs

- Validation report listing passed and failed checks
- Per-record error messages with field names and constraint violations
- Pass/fail status suitable for CI workflow gate decisions

## How to apply

Load individual records from input files or strings and parse their metadata fields (accession, name, formula, mass, spectrum peaks, etc.) according to the declared format specification. Apply a rule engine (implemented in the schema validator) that checks field presence, data type constraints, value ranges, and format patterns. Collect and report all violations as validation errors or warnings, organized by record and rule. The validation is typically invoked automatically in a CI/CD workflow (e.g., GitHub Actions) on every commit or pull request, allowing failures to block merges until records are corrected.

## Related tools

- **MassBank-web Validator** (Implements validation rules (field presence, data type, value range, format constraints) and generates the conformance report) — https://github.com/MassBank/MassBank-web/blob/main/MassBank-Project/MassBank-lib/src/main/java/massbank/cli/Validator.java
- **GitHub Actions** (Orchestrates automated validation on every commit/PR to the record repository, blocking merges on validation failure) — https://github.com/MassBank/MassBank-data
- **MassBank-cli-tools** (Successor repository maintaining the validator and other command-line tools for schema conformance checking) — https://github.com/MassBank/MassBank-cli-tools

## Evaluation signals

- All required metadata fields are present in each record.
- Field values conform to declared types (e.g., mass is numeric, accession is string with correct prefix).
- Numeric fields fall within specified ranges; spectrum peaks have valid m/z and intensity values.
- String fields match required format patterns (e.g., accession format, chemical formula syntax).
- CI workflow validation badge shows 'passing' status for the target branch; failed checks are reported as actionable error messages.

## Limitations

- The validator enforces schema rules but cannot detect semantic errors (e.g., a chemically invalid formula that is syntactically correct).
- Validation is defined by the schema specification; updates to schema rules require coordination across the repository and CI configuration.
- Performance may degrade with very large record collections; the article does not specify validation runtime or scalability thresholds.

## Evidence

- [other] Schema conformance via field, type, range, and format checks: "Apply the validation rules implemented in MassBank-web Validator.java (field presence, data type, value range, format constraints)."
- [readme] CI-based automation on record repository: "This repo contains all MassBank records and uses GitHub Actions to validate the content of all records with the Validator from MassBank-web."
- [other] Record parsing and field extraction: "Parse the record's metadata fields (accession, name, formula, mass, spectrum peaks, etc.) according to MassBank format specification."
- [other] Structured validation report output: "Generate a validation report listing passed and failed checks with specific error messages."
