---
name: protocol-metadata-extraction
description: Use when you have experimental protocol information scattered across multiple rows in a spreadsheet or table (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - Python
  - MESSES
  - jsonschema
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into other formats
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

# Protocol Metadata Extraction

## Summary

Extract and aggregate protocol metadata from tabular experimental data into a unified, filtered JSON representation using tagging and iteration directives. This skill enables systematic transformation of dispersed protocol records into queryable metadata suitable for repository submission and quality control.

## When to use

Use this skill when you have experimental protocol information scattered across multiple rows in a spreadsheet or table (e.g., multiple sample preparation steps, assay procedures, or analysis methods), each with metadata fields like 'type', 'id', and 'description', and you need to selectively aggregate and sort them into a single structured JSON field for metadata submission or documentation.

## When NOT to use

- Protocol records are already pre-aggregated into a single field or summary text—extraction will be redundant.
- Tabular data lacks consistent field structure (e.g., 'type' and 'id' columns are missing or inconsistently named across rows)—filtering and sorting will fail or produce incorrect results.
- Protocol information is stored in free-text narrative format without row-level metadata—tagging overhead may outweigh extraction benefits; manual curation is more appropriate.

## Inputs

- Tagged tabular protocol data (CSV or Excel format with extraction markup)
- Intermediate JSON file with protocol table containing records with 'type', 'id', 'description', and other metadata fields
- Conversion directive specification in JSON, defining test filter, sort_by, and delimiter parameters

## Outputs

- Single aggregated protocol summary string value (e.g., SAMPLEPREP_SUMMARY)
- Converted JSON output with protocol metadata merged into flattened or nested structure
- Validated protocol metadata ready for repository deposition (mwTab or other format)

## How to apply

First, tag your tabular protocol data to identify table boundaries and field mappings. Extract the tagged data into an intermediate JSON representation where each protocol record becomes an object with standard fields (type, id, description, etc.). Define a conversion directive using the 'for_each' str-directive pattern, specifying a test filter (e.g., 'type=sample_prep') to select only relevant protocol records. Apply a sort_by field to order filtered records by id in ascending order (or descending if warranted by your analysis logic). Finally, concatenate the sorted records' description fields using a space or custom delimiter to produce a single aggregated string value. Validate the output string length, field coverage, and delimiter placement against the expected protocol summary to ensure no records were lost or duplicated during filtering and concatenation.

## Related tools

- **MESSES** (Provides extract, validate, and convert commands for transforming tagged tabular protocol data into JSON and applying for_each str-directives with test, sort_by, and delimiter filters to aggregate protocol records.) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Underlying runtime and scripting language for MESSES CLI and library-level protocol metadata extraction workflows.)
- **jsonschema** (Validates extracted and converted protocol JSON against the Experiment Description Specification and format-specific schemas to ensure metadata completeness and correctness.) — https://pypi.org/project/jsonschema/

## Examples

```
messes extract protocol_data.csv --output protocol.json && messes convert mwTab protocol.json output_metadata --pds protocol_schema.json
```

## Evaluation signals

- Output string contains all expected protocol records' descriptions concatenated in the order specified by sort_by (ascending or descending id); verify by comparing character count and substring presence of each record's description.
- Filtered records match the test condition exactly (e.g., count of 'type=sample_prep' records equals expected count from source data); spot-check test filter logic.
- Delimiter placement is consistent between all concatenated descriptions; inspect for stray or missing spaces/delimiters at record boundaries.
- Output JSON validates successfully against the Experiment Description Specification and the target format's schema (e.g., mwTab schema); run validate command with --format parameter.
- Protocol record order in output matches sort_by field and sort_order (ascending/descending); manually verify id sequence of included records.

## Limitations

- The for_each directive assumes all filtered records share a common string field (e.g., 'description'); missing or null values in that field will result in incomplete or malformed output strings.
- Filtering relies on exact field=value matching; partial string matching, regex, or range-based filtering is not supported by the test parameter.
- Concatenation produces a flat string; hierarchical or multi-valued protocol structures are lost; use matrix directives if you need to preserve record-level detail.
- Sort performance on large protocol tables (thousands of records) is not explicitly benchmarked; very large tables may require pre-sorting or chunking in preprocessing.
- Custom delimiters are supported but may conflict with or be misinterpreted by downstream parsing if they appear within description field values; sanitization of field content is user's responsibility.

## Evidence

- [other] for_each str directive with test, sort_by, and delimiter fields concatenate multiple records from a filtered and sorted table into a single string value: "The for_each directive iterates over records in the protocol table filtered by test=type=sample_prep, sorts them by id in ascending order, and concatenates their description fields with space"
- [intro] Apply str directives to produce single string values using override, code, record_id, or for_each patterns: "The str directive assumes that you want to create a string value from information in the input JSON, and that that information is contained within a single table."
- [intro] Filter records using 'test' field with field=value syntax before building string values: "**test** - a string of the form "field=value" where field is a field in the records being iterated over and value is what the field must be equal to in order to be used to build the string value."
- [intro] Sort records by specified fields before extraction using sort_by and sort_order fields: "**sort_by** - a list of fields to sort the input JSON records by before building the value from them. **sort_order** - a string value that is either "ascending" or "descending""
- [readme] Tagging system enables extraction of tabular data into JSON intermediate form for standardization and interoperability: "Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats."
- [readme] MESSES extract command turns tabular data into JSON using tags: "The expected workflow is to use the "extract" command to transform your tabular data into JSON, then use the "validate" command to validate the JSON"
