---
name: metadata-field-verification
description: Use when you have located a workflow definition file (YAML or JSON) from
  a versioned release and need to confirm that all mandatory workflow metadata fields
  (name, version, inputs, outputs, steps) are declared, properly formatted, and cross-references
  are resolved before validation or execution.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_3365
  tools:
  - manual expert review
  - YAML/JSON schema validator
  license_tier: restricted
  provenance_tier: literature
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

# metadata-field-verification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate that all required metadata fields are present, correctly typed, and structurally consistent in workflow definition files for quality control systems. This skill ensures workflow components declare complete and schema-compliant metadata before deployment.

## When to use

Apply this skill when you have located a workflow definition file (YAML or JSON) from a versioned release and need to confirm that all mandatory workflow metadata fields (name, version, inputs, outputs, steps) are declared, properly formatted, and cross-references are resolved before validation or execution.

## When NOT to use

- Workflow definition file has already passed automated schema validation and no changes have been made since validation.
- Input is a compiled or binary workflow artifact rather than a source definition file.
- Goal is to execute the workflow rather than validate its declaration; use workflow execution tools instead.

## Inputs

- workflow definition file (YAML or JSON format)
- schema specification document for the target version
- qc_workflow_component declaration

## Outputs

- validation report documenting schema compliance
- list of detected metadata issues (missing fields, type errors, undefined references)

## How to apply

Parse the workflow definition file using a schema validator appropriate to the version specification (e.g., YAML or JSON schema for v1.0.0). Systematically check for presence of all required metadata fields: name, version, inputs, outputs, and steps. Verify that each field has the correct type and structure (e.g., inputs and outputs are arrays of objects with type, name, and description). Cross-check step references against declared input/output names to ensure no undefined references exist. Document any missing fields, type mismatches, or broken references in a validation report. This approach prevents runtime failures caused by incomplete or malformed workflow metadata.

## Related tools

- **YAML/JSON schema validator** (Parse and validate workflow definition against schema specification for structural and type compliance)
- **manual expert review** (Perform verification of workflow metadata field presence, consistency, and cross-reference integrity)

## Evaluation signals

- All required metadata fields (name, version, inputs, outputs, steps) are present in the definition file.
- Each metadata field has the correct data type (e.g., inputs/outputs are arrays, name is a string).
- No undefined references exist: all step inputs reference declared workflow inputs, and all step outputs are declared in the outputs section.
- Validation report indicates zero syntax errors and 100% schema compliance with the v1.0.0 specification.
- Type consistency is confirmed across all component definitions (e.g., input types match between workflow declaration and step usage).

## Limitations

- Validation is limited to structural and type checking; semantic correctness (e.g., whether a step can actually produce the declared outputs) requires additional testing.
- Manual expert review is recommended and may be necessary to catch domain-specific inconsistencies not caught by automated schema validation.
- This skill does not verify that referenced external tools or scripts actually exist or are compatible with the declared environment.

## Evidence

- [other] Validate all required workflow metadata fields (name, version, inputs, outputs, steps).: "Validate all required workflow metadata fields (name, version, inputs, outputs, steps)."
- [other] Check for syntax errors, undefined references, and type consistency across component definitions.: "Check for syntax errors, undefined references, and type consistency across component definitions."
- [other] Parse the workflow definition using a YAML or JSON schema validator appropriate to v1.0.0 specification.: "Parse the workflow definition using a YAML or JSON schema validator appropriate to v1.0.0 specification."
- [other] Generate a validation report documenting schema compliance and any detected issues.: "Generate a validation report documenting schema compliance and any detected issues."
