---
name: metabolite-metadata-column-matching
description: Use when validating mwTab files deposited to the Metabolomics Workbench
  and you need to verify that metadata columns match standard naming conventions and
  contain values in the expected format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - jsonschema
  - Python
  - mwtab
  techniques:
  - NMR
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-metadata-column-matching

## Summary

Validate mwTab metadata columns against standardized naming conventions and value formats using regex-based pattern matching. This skill ensures conformance of MS and NMR experimental metadata to expected column names and acceptable value ranges during file validation.

## When to use

Apply this skill when validating mwTab files deposited to the Metabolomics Workbench and you need to verify that metadata columns match standard naming conventions and contain values in the expected format. Specifically, use this when collecting validation errors, warnings, and metadata column validation results as part of structured quality control reporting for MS and NMR experimental data files.

## When NOT to use

- Input is already a pre-validated or curated metadata table from a trusted upstream system — re-matching is redundant.
- The mwTab file structure is malformed or unparseable — address parsing errors before attempting column-level matching.
- No schema definition is available for the experiment type — column matching requires reference rules.

## Inputs

- parsed mwTab file object (MWTabFile instance)
- MS or NMR schema definition (JSON schema)
- metadata section (key-value pairs or tabular data)

## Outputs

- structured metadata column validation report
- list of column name matches/mismatches
- list of column value conformance results
- categorized validation errors and warnings

## How to apply

Load the parsed mwTab file's metadata sections and apply the NameMatcher.dict_match method to verify that column names match the standardized schema-defined names for the experiment type (MS or NMR). Simultaneously, apply the ValueMatcher.series_match method to each column's values, using make_list_regex to construct regex patterns that enforce acceptable value formats and ranges. The NameMatcher attributes (lists of strings or lists of lists representing name alternatives and synonyms) and ValueMatcher attributes (regex patterns as strings) encode the conformance rules. Collect all column-level matches and mismatches, categorizing them as validation results. Return structured metadata column validation outcomes that document which columns conform, which are non-standard or missing, and which contain out-of-range or malformed values.

## Related tools

- **mwtab** (Provides MWTabFile parser and NameMatcher/ValueMatcher classes for metadata column validation) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **jsonschema** (Defines and enforces JSON schema rules for MS and NMR metadata column structure and content)
- **Python** (Execution environment for mwtab library and regex-based pattern matching)

## Examples

```
import mwtab; mwfile = mwtab.MWTabFile(open('study.mwtab')); validation_results = mwfile.validate(ms_schema, nmr_schema, verbose=True)
```

## Evaluation signals

- All expected metadata columns from the schema are matched (present and named correctly)
- All matched column values conform to their regex patterns and value constraints
- Validation report lists zero unmatched or missing standard columns for passing files
- Validation report documents specific column names and value patterns that failed, with clear distinction between name mismatches and value format violations
- Results can be traced back to the specific NameMatcher.dict_match and ValueMatcher.series_match rules applied

## Limitations

- Column matching relies on pre-defined schema rules; novel or experiment-type-specific columns not in the schema will be flagged as non-standard even if scientifically valid.
- Regex patterns for value matching are fixed at schema definition time and cannot adapt to emerging or context-dependent metadata conventions.
- No changelog is documented in the mwtab repository, so version-specific changes to NameMatcher or ValueMatcher behavior are not tracked.

## Evidence

- [other] All NameMatcher attributes are lists of strings or lists of lists of strings and all are used in its only method, dict_match.: "All NameMatcher attributes are lists of strings or lists of lists of strings and all are used in its only method, dict_match."
- [other] All ValueMatcher attributes are strings and all are used in its only method, series_match.: "All ValueMatcher attributes are strings and all are used in its only method, series_match."
- [other] make_list_regex function used in creating regex patterns for validation: "There is also a function used heavily in creating these regular expressions, make_list_regex."
- [other] Collect and categorize all validation errors, warnings, and metadata column validation results: "Collect and categorize all validation errors, warnings, and metadata column validation results (via metadata_column_matching rules for standard column names and value formats)."
- [other] jsonschema used for validating mwTab files based on JSON schema: "jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema."
