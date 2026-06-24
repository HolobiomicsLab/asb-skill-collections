---
name: json-table-to-matrix-conversion
description: Use when you have extracted tabular data (e.g., from experimental spreadsheets)
  in intermediate JSON form with a single table of records, and you need to produce
  a list of dictionaries (array of objects) for deposition into a data repository
  such as the Metabolomics Workbench, or when you need to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3750
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - jsonschema
  - MESSES
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
- This is done largely through utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_
  (`jsonschema <https://pypi.org/project/jsonschema/>`_)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_messes_cq
    doi: 10.3390/metabo13070842
    title: messes
  dedup_kept_from: coll_messes_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo13070842
  all_source_dois:
  - 10.3390/metabo13070842
  - 10.3390/metabo11030163
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# json-table-to-matrix-conversion

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Transforms a JSON table (array of records) into a list of dictionaries by mapping table columns to key–value pairs using a headers specification, with optional filtering, sorting, and record grouping. This skill is essential when converting semi-structured tabular metadata into clean, nested JSON objects suitable for repository submission or downstream processing.

## When to use

Apply this skill when you have extracted tabular data (e.g., from experimental spreadsheets) in intermediate JSON form with a single table of records, and you need to produce a list of dictionaries (array of objects) for deposition into a data repository such as the Metabolomics Workbench, or when you need to restructure table records by mapping specific columns to named keys, filtering subsets of rows, reordering them, and optionally collating multiple records into single grouped objects.

## When NOT to use

- Input data is already in the target dictionary/object format — no transformation needed
- Multiple input tables need to be merged or joined — this skill operates on a single table only
- You need to apply complex conditional logic or code-based transformations beyond field mapping — use the str directive or custom code patterns instead

## Inputs

- JSON object containing a single table (array of records with field/column structure)
- Matrix conversion directive (JSON object specifying headers, sort_by, sort_order, test filter, collate field, exclusion_headers)

## Outputs

- List of dictionaries (JSON array of objects) with keys and values mapped from input table records according to the headers specification

## How to apply

First, parse the matrix conversion directive to extract the headers mapping (key=value pairs where values reference record fields or literal strings), sort_by field list, sort_order (ascending or descending), test filter expression (field=value syntax), collate grouping field, and exclusion_headers list. Apply the test filter to select only records matching the specified field=value condition. Sort the filtered records by the fields listed in sort_by according to sort_order. Group records by the collate field value if present, creating one dictionary per group. For each group (or record if no collation), extract and map table columns to dictionary key=value pairs using the headers specification. Exclude any fields listed in exclusion_headers. Finally, assemble the grouped dictionaries into a single list and validate the output structure against the schema for your target format (e.g., mwTab).

## Related tools

- **MESSES** (Python package providing the convert command and matrix directive for JSON table-to-dictionary conversion) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validation library used to verify output dictionary structure conforms to target format schema) — https://pypi.org/project/jsonschema/

## Examples

```
messes convert mwTab your_data.json output_data.mwTab
```

## Evaluation signals

- Output is a valid JSON array of objects (list of dictionaries) with no parse errors
- Every key in each output dictionary corresponds to a key in the headers mapping and matches the expected target schema (e.g., mwTab format)
- Records filtered by test condition are exactly those matching field=value; records outside the condition are absent from output
- Records are sorted in the specified order (ascending/descending) by the sort_by fields; verify by inspecting sort_by field values in output
- If collate field is specified, multiple input records with identical collate field values are grouped into a single output dictionary; verify grouping cardinality matches expected collation
- All fields listed in exclusion_headers are absent from output dictionaries
- Output validates without errors against the target format schema (jsonschema validate)

## Limitations

- This skill operates on a single input table only; it cannot merge or join multiple tables
- The headers mapping uses simple field-to-key correspondence (field names or literal strings); complex transformations, arithmetic, or conditional field values require the str directive or external code patterns
- Collation groups records only by exact equality of a single field value; more sophisticated grouping logic is not supported
- The test filter only supports simple field=value equality; complex boolean filters or range conditions are not built into the matrix directive

## Evidence

- [other] Matrix directive core function: "The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table."
- [other] Headers key-value mapping mechanism: "The matrix directive constructs a list of dictionaries by iterating over records in a table, building each dictionary using headers specified as key=value pairs where keys/values reference record"
- [other] Filtering with test field: "**test** - a string of the form "field=value" where field is a field in the records being iterated over and value is what the field must be equal to in order to be used to build the string value."
- [other] Sorting mechanism: "**sort_by** - a list of fields to sort the input JSON records by before building the value from them. **sort_order** - a string value that is either "ascending" or "descending""
- [other] Collation grouping process: "Records are preprocessed via sort_by/sort_order (to reorder), test field (to filter matching records), and the collate field groups multiple records into single dictionaries based on a shared field"
- [other] Exclusion headers feature: "The "exclusion_headers" field can then be used to exclude fields from being added."
- [readme] MESSES convert command workflow: "The convert command of MESSES supports converting JSON data to another JSON format or another supported format. This is done by using conversion directives"
- [readme] Use case context: tabular metadata extraction: "The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized."
