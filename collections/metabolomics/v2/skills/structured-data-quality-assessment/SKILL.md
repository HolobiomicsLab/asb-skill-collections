---
name: structured-data-quality-assessment
description: Use when when you have deposited a collection of JSON project documents in a platform or repository and need to verify that all conform to a published JSON Schema specification before publication, distribution, or integration with downstream systems.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3071
  tools:
  - npm
  - JSON Schema validator
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

# structured-data-quality-assessment

## Summary

Validate that all JSON documents in a structured data repository conform to a published JSON Schema specification, identifying non-conforming projects for remediation. This skill ensures data integrity and consistency across a platform by systematically checking document structure and field types.

## When to use

When you have deposited a collection of JSON project documents in a platform or repository and need to verify that all conform to a published JSON Schema specification before publication, distribution, or integration with downstream systems. Use this skill when you suspect schema drift or when onboarding new data sources to an existing platform.

## When NOT to use

- Input documents are not JSON or do not have a formal schema specification available
- Schema itself is not yet finalized or is still in development — wait until the canonical schema is published
- Documents are already known to conform because they were generated directly from the schema (e.g., via validated form submission)

## Inputs

- Complete set of JSON project documents from a platform or repository
- Published JSON Schema definition file (e.g., app/public/schema.json)
- Platform API endpoint or file system path to retrieve projects

## Outputs

- Validation report listing each project identifier, validation status (pass/fail), and schema violations
- Aggregated summary indicating whether all documents conform or non-conforming projects flagged for remediation

## How to apply

First, retrieve the complete set of project JSON documents from the platform API or web interface (e.g., via HTTP GET or file listing). Load the canonical JSON Schema definition from the designated schema file (e.g., app/public/schema.json in the iomega/paired-data-form repository). Iterate over each retrieved JSON document and validate its structure and field types against the schema using a JSON Schema validator (available in most programming languages). For each validation, record the project identifier, pass/fail status, and any schema violations (missing required fields, type mismatches, constraint violations). Aggregate the results into a validation report to determine if all documents conform or to flag non-conforming projects for remediation. The rationale is to catch structural errors early before they propagate to dependent systems and to maintain a single source of truth for data format.

## Related tools

- **JSON Schema validator** (Validate JSON document structure and field types against the published schema specification)
- **npm** (Run test suite to ensure validation logic works correctly (e.g., npm run test in api/ and/or app/ directories)) — https://github.com/iomega/paired-data-form

## Evaluation signals

- All project identifiers are present in the validation report with a documented status
- No documents in the repository fail validation due to missing required fields or incorrect field types
- Schema violations, if present, are accurately reported with the violating field name and expected/actual type or constraint
- The validation report can be compared against a previous validation run to detect schema drift over time
- Non-conforming projects are successfully remediated and re-validation confirms they now pass

## Limitations

- The validation assumes the published JSON Schema specification is itself correct and up-to-date; if the schema contains errors, false positives or false negatives may occur
- Validation checks structural and type conformance but may not catch semantic or logical errors (e.g., values that are syntactically valid but scientifically implausible)
- Performance may degrade if the number of project documents is very large; batch processing or pagination may be needed

## Evidence

- [other] Research question and workflow from task_003: "Do all project JSON documents currently deposited in the Paired Omics Data Platform conform to the published JSON Schema specification?"
- [other] Workflow steps from task_003: "Query the Paired Omics Data Platform API or web interface to retrieve the complete set of project JSON documents currently published. Load the canonical JSON Schema definition from"
- [readme] Schema specification location from README: "The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project."
- [readme] Platform architecture and data format from README: "The web application renders the submission form from the JSON schema. The web service stores each project as a file on disk."
