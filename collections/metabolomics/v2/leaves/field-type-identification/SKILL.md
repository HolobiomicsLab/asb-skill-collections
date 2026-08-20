---
name: field-type-identification
description: Use when when working with JSON project documents that must conform to
  a schema-defined structure, and you need to apply type-specific validation, sanitization,
  or transformation rules (e.g., URL whitespace detection, numeric range checking,
  mandatory field enforcement).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3071
  tools:
  - npm
  - paired-data-form repository
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or
  `app/` directory
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Field-type identification

## Summary

Identify and classify fields in JSON project documents according to their designated types (e.g., URL, string, number) as defined in a JSON schema, enabling downstream validation and processing rules specific to each field category.

## When to use

When working with JSON project documents that must conform to a schema-defined structure, and you need to apply type-specific validation, sanitization, or transformation rules (e.g., URL whitespace detection, numeric range checking, mandatory field enforcement).

## When NOT to use

- Input is a non-JSON or unstructured document (e.g., CSV, plain text)
- The project JSON does not declare which schema version it conforms to
- No schema file is available or schema is incomplete/malformed

## Inputs

- Project JSON document
- JSON schema definition file (app/public/schema.json)

## Outputs

- Field-type mapping (field name → type classification)
- Categorized field list (URLs, strings, numbers, etc.)
- Validation rule assignments per field type

## How to apply

Load the project JSON schema (e.g., app/public/schema.json) and parse its field type definitions. Iterate through each field in a project JSON document and cross-reference its name against the schema to determine its declared type. For fields with URL type, flag them for URL-specific validation (whitespace detection); for string fields, apply text constraints; for numeric fields, apply range checks. This classification step is prerequisite to any schema-aware validation workflow and ensures validation rules are applied only to relevant field categories.

## Related tools

- **npm** (Runtime environment for loading, parsing, and iterating JSON schema and project documents) — https://www.npmjs.com/
- **paired-data-form repository** (Source of the JSON schema definition and project structure documentation) — https://github.com/iomega/paired-data-form

## Evaluation signals

- All fields in the project JSON are successfully mapped to a type declared in the schema
- Fields classified as URL type match the schema's URL field list (e.g., project URLs, reference links, data repository links)
- No fields are left unclassified or assigned an unknown type
- Type-specific validation rules (e.g., whitespace checks for URLs) can be applied to the correct field subset
- Schema conformance check passes without type mismatch errors

## Limitations

- Requires the schema file to be present and valid; breaks silently if schema is missing or malformed
- Does not validate field values themselves, only identifies their types; whitespace or format errors are caught by downstream validation, not this step
- Schema version mismatch between document and schema definition may lead to incorrect type assignments
- Platform historically had issues with spaces in URLs not being properly handled, suggesting field-type identification alone is insufficient without downstream whitespace validation

## Evidence

- [other] The platform stores paired omics data projects using a JSON schema format (app/public/schema.json) that defines project structure: "The platform stores paired omics data projects using a JSON schema format (app/public/schema.json) that defines project structure, which serves as the basis for implementing field-level validation"
- [other] Identify all fields designated as URL type in the schema (e.g., project URLs, reference links, data repository links): "Identify all fields designated as URL type in the schema (e.g., project URLs, reference links, data repository links). Iterate through each URL field and check for the presence of whitespace"
- [readme] The JSON schema (app/public/schema.json) describes the format of an project: "The JSON schema (app/public/schema.json) describes the format of an project."
- [discussion] Warning to not include spaces in urls: "Spaces in URLs not properly handled  [section=discussion; evidence='Warning to not include spaces in urls ([#75]'"
