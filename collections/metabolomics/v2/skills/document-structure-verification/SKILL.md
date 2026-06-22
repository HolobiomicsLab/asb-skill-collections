---
name: document-structure-verification
description: Use when when uploading or ingesting paired omics project documents into the Pairing Omics Data Platform, or when you need to verify that a JSON project file conforms to the expected schema structure before processing MS/MS mass spectra linkages, genome associations, or submission to external.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0121
  tools:
  - npm
  - Github
  - JSON schema file (app/public/schema.json)
  - GitHub
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory
- pull request (https://help.github.com/articles/about-pull-requests/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairedomicsdatapla_cq
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_pairedomicsdatapla_cq
schema_version: 0.2.0
---

# document-structure-verification

## Summary

Validate paired omics project documents against a JSON schema to ensure structural compliance and data integrity before storage or downstream analysis. This skill detects format violations and missing required fields that would compromise data interoperability.

## When to use

When uploading or ingesting paired omics project documents into the Pairing Omics Data Platform, or when you need to verify that a JSON project file conforms to the expected schema structure before processing MS/MS mass spectra linkages, genome associations, or submission to external repositories like Zenodo.

## When NOT to use

- Document has already been validated and stored in the platform data directory
- Input is not JSON or is severely malformed (use a JSON parser/repair tool first)
- You are performing semantic validation of omics values (e.g., organism taxonomy or instrument calibration) rather than structural validation

## Inputs

- JSON project document (paired omics data structure)
- JSON schema file (app/public/schema.json)

## Outputs

- Validation pass/fail status
- Structured validation report with compliance details
- Schema violation list with error messages and field locations

## How to apply

Load the paired omics project JSON document and the canonical JSON schema from app/public/schema.json. Apply JSON schema validation using the npm test framework (via `npm run test`) to systematically check the document against all structural and format constraints defined in the schema. Capture the validation output including pass/fail status, enumerated schema violations, and specific error messages identifying which fields or nested structures failed validation. Generate a structured validation report that itemizes compliance status and flags any violations with their locations in the document hierarchy. Use this report to either approve the document for storage or return remediation guidance to the user.

## Related tools

- **npm** (Execute JSON schema validation tests and generate validation reports via `npm run test` command) — https://www.npmjs.com
- **JSON schema file (app/public/schema.json)** (Define structural and format requirements against which paired omics project documents are validated) — https://github.com/iomega/paired-data-form
- **GitHub** (Version control and CI/CD pipeline for managing schema updates and validating changes via pull requests) — https://github.com/iomega/paired-data-form

## Examples

```
npm run test
```

## Evaluation signals

- Validation report explicitly returns pass status for all schema constraints
- No schema violations are reported; violation list is empty
- All required fields are present and populated with values of correct type
- Nested structures (e.g., sample preparation, instrumentation methods) conform to defined schema hierarchy
- Error messages, if any, precisely identify field names and violation types (e.g., 'type mismatch', 'missing required property', 'value not in enum')

## Limitations

- Schema validation confirms structural and format compliance only; it does not verify semantic correctness (e.g., whether organism identifiers are valid GenBank accessions or whether MS/MS spectra IDs are resolvable)
- Validation occurs at document upload time; post-upload modifications to the JSON schema require re-validation of previously stored documents
- The schema is maintained in app/public/schema.json and must be kept in sync with the platform's data model; schema drift is not automatically detected

## Evidence

- [other] The application uses a JSON schema file located at app/public/schema.json that defines the structural and format requirements for paired omics data projects.: "The application uses a JSON schema file located at app/public/schema.json that defines the structural and format requirements for paired omics data projects."
- [other] Load the paired omics project JSON document and the JSON schema from app/public/schema.json. Apply JSON schema validation using npm test framework to check the document against all schema constraints.: "Apply JSON schema validation using npm test framework to check the document against all schema constraints."
- [other] Capture validation results including pass/fail status, any schema violations, and error messages.: "Capture validation results including pass/fail status, any schema violations, and error messages."
- [readme] The JSON schema (app/public/schema.json) describes the format of an project.: "The JSON schema (app/public/schema.json) describes the format of an project."
- [readme] make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory: "make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory"
