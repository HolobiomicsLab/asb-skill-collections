---
name: data-type-constraint-verification
description: Use when when ingesting or updating MassBank records in plain-text or
  structured format, and you need to verify that metadata fields (accession, name,
  formula, mass, spectrum peaks) comply with type definitions, presence requirements,
  and allowed value ranges.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - MassBank-web Validator
  - GitHub Actions
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
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

# data-type-constraint-verification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Automated validation of MassBank record content against defined data-type and value-range constraints to ensure conformance to the MassBank format specification. This skill applies the MassBank Validator's rule engine to individual records during CI/CD workflows, catching schema violations, missing fields, and out-of-range values before data publication.

## When to use

When ingesting or updating MassBank records in plain-text or structured format, and you need to verify that metadata fields (accession, name, formula, mass, spectrum peaks) comply with type definitions, presence requirements, and allowed value ranges. Trigger this skill as part of automated record submission or continuous integration pipelines to catch conformance errors early.

## When NOT to use

- Records that have already been validated and archived in a stable release (use only for new submissions or updates)
- When performing semantic validation (e.g., checking chemical formula plausibility or spectrum-to-mass consistency); this skill validates syntax and type conformance only
- If you need to validate records not in MassBank format or against alternative schemas

## Inputs

- MassBank record file (plain-text or structured format)
- Record metadata fields (accession, name, formula, mass, spectrum peaks)

## Outputs

- Validation report listing passed checks
- Validation report listing failed checks with specific error messages
- Workflow status badge (pass/fail) for GitHub Actions

## How to apply

Load the MassBank record from the input file or string, then parse its metadata fields according to the MassBank format specification. Invoke the MassBank-web Validator.java component, which applies a ruleset checking field presence, data type (e.g., numeric vs. string), value ranges, and format constraints (e.g., valid accession patterns). Collect all validation errors or warnings for each failed rule and generate a validation report listing passed and failed checks with specific error messages. The GitHub Actions workflow automatically runs this validation on all pull requests and commits to the main and dev branches.

## Related tools

- **MassBank-web Validator** (Implements and executes the validation rules for field presence, data type, value range, and format constraints on individual records) — https://github.com/MassBank/MassBank-web/blob/main/MassBank-Project/MassBank-lib/src/main/java/massbank/cli/Validator.java
- **GitHub Actions** (Orchestrates automated invocation of the Validator on all records with each commit/pull request to the main and dev branches) — https://github.com/MassBank/MassBank-data

## Evaluation signals

- Validation report indicates 100% of checked fields pass their respective data-type and format constraints
- No validation errors or warnings are reported for a given record
- GitHub Actions workflow badge shows 'passing' status for both main and dev branches
- All mandatory fields (accession, name, formula, mass) are present and conform to their declared types
- Numeric fields (e.g., mass, m/z values in spectrum peaks) are parseable as numbers and fall within expected ranges

## Limitations

- The Validator checks syntax and type conformance only; it does not validate semantic correctness (e.g., chemical formula plausibility or spectrum-to-mass agreement)
- Validation rules are defined by the MassBank format specification; if the specification is incomplete or ambiguous, some errors may not be caught
- The skill relies on GitHub Actions infrastructure; validation will not run without a configured workflow file in the repository

## Evidence

- [other] Parse the record's metadata fields (accession, name, formula, mass, spectrum peaks, etc.) according to MassBank format specification.: "Parse the record's metadata fields (accession, name, formula, mass, spectrum peaks, etc.) according to MassBank format specification."
- [other] Apply the validation rules implemented in MassBank-web Validator.java (field presence, data type, value range, format constraints).: "Apply the validation rules implemented in MassBank-web Validator.java (field presence, data type, value range, format constraints)."
- [other] Collect validation errors or warnings for each failed rule.: "Collect validation errors or warnings for each failed rule."
- [other] Generate a validation report listing passed and failed checks with specific error messages.: "Generate a validation report listing passed and failed checks with specific error messages."
- [readme] uses GitHub Actions to validate the content of all records with the Validator from MassBank-web: "uses GitHub Actions to validate the content of all records with the Validator from MassBank-web"
