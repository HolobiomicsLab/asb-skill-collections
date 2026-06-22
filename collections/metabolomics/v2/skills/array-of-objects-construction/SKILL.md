---
name: array-of-objects-construction
description: Use when you have tabular experimental data (e.g., sample metadata, mass spectrometry parameters, NMR acquisition details) in JSON table format and need to produce a list of structured objects for submission to a data repository (e.g., Metabolomics Workbench) or downstream format conversion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - jsonschema
  - messes
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
- This is done largely through utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)
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
---

# array-of-objects-construction

## Summary

Construct a list of dictionaries (array of objects) from tabular JSON records by mapping columns to key–value pairs via headers specification, with optional filtering, sorting, and row-grouping (collation). This skill is essential when converting flat tabular experimental metadata into nested JSON structures suitable for REST API submission or format conversion.

## When to use

Apply this skill when you have tabular experimental data (e.g., sample metadata, mass spectrometry parameters, NMR acquisition details) in JSON table format and need to produce a list of structured objects for submission to a data repository (e.g., Metabolomics Workbench) or downstream format conversion. Trigger: the output schema requires an array of objects rather than a flat table, and records may need filtering (e.g., only 'positive' mode samples), ordering (e.g., by acquisition date), or grouping (e.g., all replicates of a sample into a single record).

## When NOT to use

- Input records are already in the desired array-of-objects format (avoid redundant re-structuring).
- Output should be a single flat string or scalar value (use str directive instead).
- Records contain nested structures that should be preserved as-is (collation may incorrectly flatten hierarchy).
- The mapping from table columns to output keys is not declarative via headers (requires custom scripting instead).

## Inputs

- JSON object containing a single table with records (array of row objects)
- matrix conversion directive (object specifying headers, sort_by, sort_order, test, collate, exclusion_headers fields)

## Outputs

- list of dictionaries (JSON array of objects)

## How to apply

Parse the matrix conversion directive to extract the headers key=value specification (mapping table columns to output dictionary keys), sort_by and sort_order fields (to reorder records), test filter expression (field=value syntax to select matching records), and collate field (to group multiple records by shared value). First, apply the test filter to select only records satisfying the condition (e.g., 'instrument_type=Orbitrap'). Next, sort the filtered records by the fields listed in sort_by in the specified sort_order (ascending or descending). Then, group records by the collate field value if specified, creating one output dictionary per group. For each record or group, iterate through the headers specification and extract table column values, mapping them to the corresponding dictionary key names; literal strings in the headers specification are preserved as-is. Finally, exclude any fields listed in exclusion_headers from the output, assemble all dictionaries into a single list, and return. The rationale is that collation and sorting normalize record order and structure before key–value extraction, ensuring deterministic, reproducible output suitable for validation and repository submission.

## Related tools

- **messes** (Python package providing the matrix directive and array-of-objects conversion as part of the convert command workflow) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validates the output list of dictionaries against JSON Schema to ensure correctness before repository submission) — https://pypi.org/project/jsonschema/

## Evaluation signals

- Output is a valid JSON array (not a single object or flat table).
- Each element in the output array is a dictionary with keys matching the headers specification (verify via schema validation).
- If a test filter was specified, all records in the output satisfy the filter condition (e.g., all records have instrument_type='Orbitrap').
- If sort_by was specified, records are ordered by the specified fields in the declared sort_order (ascending/descending); verify by spot-checking first and last records.
- If collate was specified, no two dictionaries share the same value for the collate field; verify cardinality matches the number of unique collate field values in the input.
- Fields listed in exclusion_headers do not appear as keys in any output dictionary.
- The output passes validation against the project's JSON Schema and the target format schema (e.g., mwTab format schema).

## Limitations

- The headers specification uses only key=value pairs referencing table columns or literal strings; complex computations or nested object construction are not supported by the matrix directive alone (would require chaining with str directive or post-processing).
- Collation groups records by exact match on a single field; more complex multi-field or conditional grouping logic requires pre-processing or custom scripting.
- The test filter supports only field=value equality conditions; range queries, regex matching, or boolean logic are not natively supported.
- If the collate field contains null or missing values, those records may be grouped unexpectedly or excluded; the article does not clarify handling of missing collate values.
- Sorting is applied globally before collation; within-group ordering is not preserved or user-controllable.

## Evidence

- [other] The matrix directive constructs a list of dictionaries by iterating over records in a table, building each dictionary using headers specified as key=value pairs where keys/values reference record fields or literal strings.: "The matrix directive constructs a list of dictionaries by iterating over records in a table, building each dictionary using headers specified as key=value pairs where keys/values reference record"
- [other] Records are preprocessed via sort_by/sort_order (to reorder), test field (to filter matching records), and the collate field groups multiple records into single dictionaries based on a shared field value.: "Records are preprocessed via sort_by/sort_order (to reorder), test field (to filter matching records), and the collate field groups multiple records into single dictionaries based on a shared field"
- [intro] The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table.: "The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table."
- [intro] Sort records by specified fields before extraction using sort_by and sort_order fields: "**sort_by** - a list of fields to sort the input JSON records by before building the value from them. **sort_order** - a string value that is either "ascending" or "descending""
- [intro] Filter records using 'test' field with field=value syntax before building string values: "**test** - a string of the form "field=value" where field is a field in the records being iterated over and value is what the field must be equal to in order to be used to build the string value."
- [intro] The "exclusion_headers" field can then be used to exclude fields from being added.: "The "exclusion_headers" field can then be used to exclude fields from being added."
- [readme] MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into other formats.: "MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into other formats."
