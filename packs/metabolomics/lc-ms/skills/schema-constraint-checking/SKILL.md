---
name: schema-constraint-checking
description: Use when a user uploads a JSON project file to the platform and you need to verify it matches the required format defined in app/public/schema.json before accepting it into the database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - npm
  - ajv
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-020-00724-z
  all_source_dois:
  - 10.1038/s41589-020-00724-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# schema-constraint-checking

## Summary

Validate uploaded JSON project documents against a formal JSON Schema specification to enforce structural and semantic constraints before ingestion into the Pairing Omics Data Platform. This skill ensures that paired omics data (linking MS/MS spectra with genome, sample preparation, extraction method, and instrumentation metadata) conform to required field definitions, data types, and cardinality rules.

## When to use

Apply this skill when a user uploads a JSON project file to the platform and you need to verify it matches the required format defined in app/public/schema.json before accepting it into the database. Use it as a gating step before persistence or indexing, particularly when users submit programmatically via the OpenAPI web service or through the web application submission form.

## When NOT to use

- Input is already known to be a valid project already stored in the platform database.
- The schema definition file itself is corrupted or not available — this skill requires a valid reference schema.
- User is performing bulk re-validation of the entire platform database; use a batch schema-validation job instead.

## Inputs

- JSON project file (user-uploaded candidate document)
- JSON Schema definition file (app/public/schema.json)

## Outputs

- Validation result (pass/fail boolean)
- List of constraint violations (if any)
- List of missing required fields (if any)
- List of type or cardinality errors (if any)

## How to apply

Load the candidate JSON project file from the upload input and the JSON Schema definition from app/public/schema.json. Perform schema validation using a JSON Schema validator library (e.g., ajv). The validator will check that all required fields are present, that field values match their declared types (e.g., strings, numbers, arrays), and that any cardinality or enum constraints are satisfied. Report the validation result (pass or fail) and enumerate any constraint violations, missing required fields, or type mismatches to the user. Reject the upload if validation fails; proceed to storage only on success.

## Related tools

- **ajv** (JSON Schema validator library used to perform constraint validation)
- **npm** (Package manager and test runner for executing validation in api/ and app/ directories)

## Evaluation signals

- Validation passes (returns true/success) only when all required fields are present in the JSON.
- Validation fails (returns false/error) and reports specific field names and types when a field is missing or has wrong type.
- Validation correctly enforces any enum constraints or cardinality rules defined in the schema (e.g., required arrays, mutually required fields).
- Error messages enumerate all violations in a single pass, not stopping at the first error.
- The schema file app/public/schema.json is loaded from the expected path and its version matches the platform release.

## Limitations

- Validation checks only structural and type constraints; it does not verify semantic validity of field values (e.g., that a GenBank genome identifier actually exists or is publicly accessible).
- Schema validation does not catch spaces in URLs or other character-level issues; see issue #75 on the repository for known URL formatting problems.
- No built-in guidance is provided to the user on what each field means or why it is required; see issue #76 for discussion of missing field documentation.
- If the schema definition itself is malformed or not accessible, validation will fail regardless of input quality.

## Evidence

- [other] A JSON schema file located at app/public/schema.json defines the required format for paired omics data projects in the platform.: "A JSON schema file located at app/public/schema.json defines the required format for paired omics data projects in the platform."
- [other] The workflow for validating an uploaded project includes loading the candidate file, loading the schema, performing validation with a library like ajv, and reporting results with enumerated violations.: "1. Load the candidate JSON project file from upload input. 2. Load the JSON Schema definition from app/public/schema.json. 3. Perform schema validation using a JSON Schema validator (e.g. ajv or"
- [readme] The JSON schema describes the format of a project in the Pairing Omics Data Platform.: "The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project."
- [readme] The platform stores each project as a file on disk and uses a web service with OpenAPI specification for programmatic submission and retrieval.: "The web service stores each project as a file on disk. The web service has an OpenAPI (v3.0.3) specification"
