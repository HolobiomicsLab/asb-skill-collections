---
name: project-metadata-validation
description: Use when when a user uploads a JSON project document to the Pairing Omics Data Platform, before accepting it into the repository or indexing it for search. Use this skill to catch missing required fields, incorrect field types, and constraint violations early in the submission workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3364
  edam_topics:
  - http://edamontology.org/topic_3377
  - http://edamontology.org/topic_0091
  tools:
  - npm
  - ajv
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairedomicsdatapla
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_pairedomicsdatapla
schema_version: 0.2.0
---

# project-metadata-validation

## Summary

Validate uploaded JSON project documents against a formal JSON schema specification to ensure they conform to required structure and constraints for paired omics data storage. This skill enforces data quality and consistency before projects are persisted or indexed.

## When to use

When a user uploads a JSON project document to the Pairing Omics Data Platform, before accepting it into the repository or indexing it for search. Use this skill to catch missing required fields, incorrect field types, and constraint violations early in the submission workflow.

## When NOT to use

- Input is already known to be valid or has been validated by an earlier step
- The JSON schema file is missing, corrupted, or out of sync with the codebase

## Inputs

- JSON project document (uploaded file)
- JSON Schema definition (app/public/schema.json)

## Outputs

- Validation result (pass or fail)
- List of constraint violations (if any)
- List of missing required fields (if any)

## How to apply

Load the candidate JSON project file from the upload input and the JSON Schema definition from app/public/schema.json. Pass both to a JSON Schema validator library (such as ajv for Node.js environments). Run validation and report the pass/fail outcome. If validation fails, enumerate all constraint violations and identify which required fields are missing or malformed. This ensures only projects conforming to the platform's paired omics data model (linking MS/MS mass spectra with genome, sample preparation, extraction, and instrumentation metadata) are stored.

## Related tools

- **ajv** (JSON Schema validator used to perform schema validation of uploaded project documents)
- **npm** (Package manager and test runner for executing validation tests in the app/ and api/ directories)

## Evaluation signals

- Validation passes without errors for well-formed project documents containing all required fields
- Validation fails and reports specific field names and constraint types for malformed or incomplete documents
- Missing required fields (e.g., genome identifier, MS/MS spectra reference, sample preparation metadata) are explicitly identified
- Type mismatches (e.g., string instead of array, or incorrect enum values) are flagged with field path and expected type
- Existing test suite continues to pass after validation logic is integrated (verified by running `npm run test` in api/ and app/ directories)

## Limitations

- Schema validation alone cannot catch semantic inconsistencies (e.g., a valid NCBI accession that does not actually exist)
- Spaces in URLs are not properly handled by the platform, which may cause validation or downstream processing to fail (#75)
- The schema does not currently provide descriptive help text for all fields, limiting user-facing documentation (#76)
- Validation does not verify that linked public identifiers (genome accessions, GNPS task IDs) are resolvable or correct

## Evidence

- [other] A JSON schema file located at app/public/schema.json defines the required format for paired omics data projects in the platform.: "A JSON schema file located at app/public/schema.json defines the required format for paired omics data projects in the platform."
- [other] Load the candidate JSON project file from upload input. 2. Load the JSON Schema definition from app/public/schema.json. 3. Perform schema validation using a JSON Schema validator (e.g. ajv or similar library). 4. Report validation result (pass or fail) and enumerate any constraint violations or missing required fields.: "Load the candidate JSON project file from upload input. 2. Load the JSON Schema definition from app/public/schema.json. 3. Perform schema validation using a JSON Schema validator (e.g. ajv or similar"
- [readme] The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project.: "The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project."
- [other] make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory: "make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory"
- [intro] Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method: "Links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method"
