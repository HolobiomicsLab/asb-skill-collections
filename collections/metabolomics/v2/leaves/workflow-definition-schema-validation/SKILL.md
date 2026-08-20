---
name: workflow-definition-schema-validation
description: Use when you have located a workflow definition file (YAML or JSON) in
  a versioned release or commit and need to verify that it conforms to the schema
  specification for that release version (e.g., v1.0.0).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_0091
  tools:
  - manual expert review
  - YAML schema validator (e.g., yamllint, jsonschema)
  - QC4metabolomics repository
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.4c07078
  title: qc4metabolomics
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qc4metabolomics
    doi: 10.1021/acs.analchem.4c07078
    title: qc4metabolomics
  dedup_kept_from: coll_qc4metabolomics
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c07078
  all_source_dois:
  - 10.1021/acs.analchem.4c07078
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# workflow-definition-schema-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate the structural integrity and schema compliance of a workflow definition file (YAML or JSON) against a formal specification, ensuring all required metadata fields are present, type-consistent, and free of syntax errors or undefined references. This skill is essential when reconstructing or auditing released workflow components to confirm they match their declared specification version.

## When to use

Apply this skill when you have located a workflow definition file (YAML or JSON) in a versioned release or commit and need to verify that it conforms to the schema specification for that release version (e.g., v1.0.0). This is especially important when reconstructing bundled workflow components whose integrity has not yet been manually verified, or when validating workflow definitions across multiple commits or releases.

## When NOT to use

- The workflow definition file has already been validated by automated CI/CD tests in the source repository and a validation report is already available.
- You are checking runtime behavior or execution correctness rather than static schema compliance—use a workflow execution trace or integration test instead.
- The workflow file format or version is unknown and no schema specification is available for the target version.

## Inputs

- workflow definition file (YAML or JSON format)
- workflow schema specification document for the target version
- commit hash or release tag identifier

## Outputs

- validation report documenting schema compliance status
- list of detected errors (syntax, undefined references, type inconsistencies, missing fields)
- confirmation of qc_workflow_component structural integrity

## How to apply

First, identify the workflow definition file and the specification version it declares (e.g., commit d441874 for QC4metabolomics v1.0.0). Obtain or construct a schema validator appropriate to that version and format (YAML or JSON schema). Parse the workflow definition file using the validator. Check for presence of all required workflow metadata fields: name, version, inputs, outputs, and steps. Validate type consistency and referential integrity across all component definitions—specifically, ensure that all step inputs reference defined workflow inputs or outputs from prior steps, and that all declared outputs are actually produced by the workflow steps. Document any syntax errors, undefined variable references, type mismatches, or missing required fields in a validation report. Use the report to confirm schema compliance or flag issues for remediation.

## Related tools

- **YAML schema validator (e.g., yamllint, jsonschema)** (Parse and validate YAML/JSON workflow definition syntax and structural compliance against schema specification)
- **QC4metabolomics repository** (Source of workflow definition file and release asset bundles for validation) — https://github.com/stanstrup/QC4Metabolomics

## Evaluation signals

- All required workflow metadata fields (name, version, inputs, outputs, steps) are present and non-empty.
- No syntax errors reported by the YAML/JSON parser; file is well-formed.
- All step input references resolve to either declared workflow inputs or outputs from prior steps; no undefined variable references.
- All declared outputs are produced by at least one workflow step; no orphaned or unreachable outputs.
- Type consistency is maintained across all input/output declarations and step bindings (e.g., file type, data type, cardinality).

## Limitations

- Schema validation confirms static structural correctness but does not verify runtime behavior, data flow correctness, or tool availability.
- Validation is specific to the schema version for the target release; schemas may differ across versions, requiring version-specific validators.
- The approach relies on availability of a formal schema specification document for the target version; if the specification is missing or ambiguous, validation effectiveness is reduced.

## Evidence

- [other] Locate the workflow definition file in the QC4metabolomics repository (commit d441874). Parse the workflow definition using a YAML or JSON schema validator appropriate to v1.0.0 specification.: "Locate the workflow definition file in the QC4metabolomics repository (commit d441874). Parse the workflow definition using a YAML or JSON schema validator appropriate to v1.0.0 specification."
- [other] Validate all required workflow metadata fields (name, version, inputs, outputs, steps). Check for syntax errors, undefined references, and type consistency across component definitions.: "Validate all required workflow metadata fields (name, version, inputs, outputs, steps). Check for syntax errors, undefined references, and type consistency across component definitions."
- [readme] QC systems for metabolomics studies: "QC systems for metabolomics studies"
