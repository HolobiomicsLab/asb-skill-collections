---
name: structured-report-generation
description: Use when after applying jsonschema validation to a parsed mwTab file against MS or NMR schema definitions, when you have collected validation errors, warnings, and metadata column matching results and need to communicate findings to data curators or submitters in a structured, machine-readable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - jsonschema
  - Python
  - mwtab
  - NameMatcher
  - ValueMatcher
  - pandas
derived_from:
- doi: 10.3390/metabo11030163
  title: mwtab Python Library for RESTful Access
evidence_spans:
- jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema
- The ``mwtab`` package is a Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwtab_python_library_for_restful_access_cq
    doi: 10.3390/metabo11030163
    title: mwtab Python Library for RESTful Access
  dedup_kept_from: coll_mwtab_python_library_for_restful_access_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11030163
  all_source_dois:
  - 10.3390/metabo11030163
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Structured Report Generation

## Summary

Generate a categorized validation report documenting schema conformance results, violations, and remediation guidance for mwTab metabolomics data files. This skill transforms raw validation errors and metadata mismatches into a structured artifact that communicates pass/fail status and actionable recommendations for data curators and depositors.

## When to use

After applying jsonschema validation to a parsed mwTab file against MS or NMR schema definitions, when you have collected validation errors, warnings, and metadata column matching results and need to communicate findings to data curators or submitters in a structured, machine-readable format suitable for archival and curation workflows.

## When NOT to use

- The input mwTab file has not yet been parsed or loaded into memory — parse first using MWTabFile loader before generating the report.
- Validation has not been performed — run jsonschema validation and metadata column matching before collecting results for the report.
- The goal is to fix violations in-place rather than document them; use error correction or data transformation skills instead of report generation.

## Inputs

- Parsed mwTab file object (MWTabFile instance with metadata and data sections extracted)
- Validation errors from jsonschema validation run
- Metadata column matching results (NameMatcher and ValueMatcher outputs)
- MS or NMR schema definition (JSON schema used for validation)

## Outputs

- Structured validation report (JSON or dict format)
- Categorized violation list with severity and remediation guidance
- Pass/fail status per mwTab file section
- Machine-readable schema rule violations and column format mismatches

## How to apply

Collect and categorize all validation outputs from the jsonschema validation step, including schema violation errors, metadata column matching results (via NameMatcher.dict_match and ValueMatcher.series_match), and warnings generated during file parsing. Organize these results into logical sections: schema pass/fail status, violation details (grouped by metadata vs. data sections), column name and value format violations, and recommendations for remediation. Emit the report as a structured object (e.g., JSON or Python dict) with explicit categorization of error types, severity levels, and cross-references to the relevant mwTab file sections and schema rules that were violated. The report should enable downstream processes to programmatically identify which sections require resubmission or manual curation.

## Related tools

- **jsonschema** (Validates mwTab file content against MS and NMR JSON schema specifications; violations are collected and categorized into the report)
- **mwtab** (Parses mwTab files into structured MWTabFile objects; extracts metadata and data sections that are validated and reported on) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **NameMatcher** (Matches metadata column names against standard vocabularies; results are included in the report as column validation findings) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **ValueMatcher** (Validates metadata column values against format and vocabulary rules; violations are documented in the structured report) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **pandas** (Processes tabular data sections within the mwTab format for structured organization and serialization in the report)

## Examples

```
import mwtab; from jsonschema import validate; mwfile = mwtab.read_files('1')[0]; schema = mwfile.validate(verbose=True); print(schema)
```

## Evaluation signals

- Report contains explicit pass/fail status for each validation rule applied (schema conformance, column name matching, value format compliance).
- All violations collected during validation are present in the report and grouped by category (schema errors, metadata column mismatches, data section issues).
- Each violation entry includes a cross-reference to the affected mwTab section (metadata block or data table) and the schema rule or vocabulary standard violated.
- Remediation guidance or recommendation text is provided for each violation class, enabling curators to prioritize and address issues systematically.
- Report is machine-parseable (valid JSON or structured Python dict) and can be consumed by downstream curation workflows or archival systems without manual interpretation.

## Limitations

- Report generation assumes that validation has already been performed; if validation is incomplete or skipped, the report will be incomplete or misleading.
- Metadata column matching relies on NameMatcher and ValueMatcher rules; if those rules are not comprehensive or up-to-date, some violations may be missed or incorrectly categorized.
- The mwtab library does not include a built-in changelog or versioning mechanism for schema changes, making it difficult to track how validation rules have evolved over time.
- Report structure and remediation guidance are limited to the capabilities of the JSON schema definitions and NameMatcher/ValueMatcher rule sets; novel or domain-specific violations may not be detected or well-documented.

## Evidence

- [other] Collect and categorize all validation errors, warnings, and metadata column validation results (via metadata_column_matching rules for standard column names and value formats): "Collect and categorize all validation errors, warnings, and metadata column validation results (via metadata_column_matching rules for standard column names and value formats)."
- [other] Generate and return a structured validation report documenting pass/fail status, violation details, and recommendations: "Generate and return a structured validation report documenting pass/fail status, violation details, and recommendations."
- [other] The mwtab library uses jsonschema to validate mwTab files based on JSON schema definitions, enabling schema-based validation of MS and NMR experimental data files: "The mwtab library uses jsonschema to validate mwTab files based on JSON schema definitions, enabling schema-based validation of MS and NMR experimental data files."
- [other] Validate data based on schema definition: "Validate data stored in ``mwTab`` file based on schema definition."
- [other] jsonschema for validating functionality of mwTab files based on JSON schema: "jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema."
