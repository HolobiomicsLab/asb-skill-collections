---
name: batch-document-verification
description: Use when when you have deposited a collection of JSON project documents in a platform and need to verify that all conform to the published schema before public release or after schema updates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - npm
derived_from:
- doi: 10.1038/s41589-020-00724-z
  title: pairedomicsdatapla
evidence_spans:
- make sure the existing tests still work by running ``npm run test`` in `api/` and/or `app/` directory
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pairedomicsdatapla
    doi: 10.1038/s41589-020-00724-z
    title: pairedomicsdatapla
  dedup_kept_from: coll_pairedomicsdatapla
schema_version: 0.2.0
---

# batch-document-verification

## Summary

Validate a collection of JSON documents against a published JSON Schema specification to identify structural and type violations across all records. This skill detects non-conforming documents in a repository to flag remediation targets.

## When to use

When you have deposited a collection of JSON project documents in a platform and need to verify that all conform to the published schema before public release or after schema updates. Particularly useful when discovering whether legacy or newly ingested records violate the canonical format specification.

## When NOT to use

- Schema definition itself has not been published or agreed upon by the community
- Individual documents are already known to conform and testing is not required for quality assurance
- JSON documents use format extensions that intentionally deviate from the canonical schema

## Inputs

- Complete set of project JSON documents from a platform repository
- Canonical JSON Schema definition (e.g., app/public/schema.json)

## Outputs

- Validation report listing project identifiers with pass/fail status
- Detailed schema violation log for non-conforming documents

## How to apply

Retrieve the complete set of project JSON documents from the platform API or web interface. Load the canonical JSON Schema definition (e.g., from app/public/schema.json in the paired-data-form repository). Use a JSON Schema validator to iterate over each document and validate its structure and field types against the schema. Generate a validation report listing project identifier, pass/fail status, and specific schema violations. Aggregate results to identify which documents conform and which require remediation, focusing on type mismatches, missing required fields, and invalid field values.

## Related tools

- **npm** (package manager and test runner for executing validation workflows in the paired-data-form repository) — https://github.com/iomega/paired-data-form

## Evaluation signals

- All project identifiers appear in the validation report with explicit pass or fail status
- Non-conforming documents are flagged with specific field names and violation types (e.g., type mismatch, missing required field)
- Aggregated results show 100% of documents have been checked (no missing identifiers)
- Violations can be cross-referenced against the canonical schema definition to confirm accuracy
- Report can be used to prioritize remediation work for projects with the most violations

## Limitations

- Validation only checks structural conformance to schema; it does not verify semantic correctness or data accuracy (e.g., valid genome identifiers, real instrument names)
- Large document collections may require optimized batch processing or pagination to avoid memory or API limits
- Newly discovered schema violations may require updates to the canonical schema definition itself if many documents share the same deviation

## Evidence

- [other] Do all project JSON documents currently deposited in the Paired Omics Data Platform conform to the published JSON Schema specification?: "Do all project JSON documents currently deposited in the Paired Omics Data Platform conform to the published JSON Schema specification?"
- [other] A JSON schema (app/public/schema.json) has been published to formally describe the required format of paired omics data projects stored in the platform.: "A JSON schema (app/public/schema.json) has been published to formally describe the required format of paired omics data projects stored in the platform."
- [other] Query the Paired Omics Data Platform API or web interface to retrieve the complete set of project JSON documents currently published. Load the canonical JSON Schema definition from app/public/schema.json in the iomega/paired-data-form repository. Iterate over each retrieved project JSON document and validate its structure and field types against the schema using a JSON Schema validator. Generate a validation report listing each project identifier, validation status (pass/fail), and any schema violations encountered. Aggregate results to confirm all documents conform or flag non-conforming projects for remediation.: "Query the Paired Omics Data Platform API or web interface to retrieve the complete set of project JSON documents currently published. Load the canonical JSON Schema definition from"
- [readme] The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project.: "The [JSON schema (app/public/schema.json)](app/public/schema.json) describes the format of an project."
