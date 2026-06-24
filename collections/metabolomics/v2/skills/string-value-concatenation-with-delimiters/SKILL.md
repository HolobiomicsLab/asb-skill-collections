---
name: string-value-concatenation-with-delimiters
description: Use when converting intermediate JSON to a target format (e.g., mwTab)
  and a single string field must be populated from multiple source records—for example,
  combining author names separated by semicolons, or concatenating a list of instrument
  names or experimental conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3281
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - jsonschema
  - MESSES convert command
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

# string-value-concatenation-with-delimiters

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Build a single string value from multiple records in JSON by iterating over filtered and sorted records, concatenating their values with a specified delimiter. This skill is essential in the MESSES conversion pipeline when a target metadata field requires aggregation of repeated or multi-value fields from a source table.

## When to use

Apply this skill when converting intermediate JSON to a target format (e.g., mwTab) and a single string field must be populated from multiple source records—for example, combining author names separated by semicolons, or concatenating a list of instrument names or experimental conditions. Use when the source data is organized as a table with repeating rows that must be collapsed into one delimited string in the output.

## When NOT to use

- When the target field should contain a list or array rather than a single string—use the matrix directive instead.
- When source records are already in the desired single-field format and no concatenation or filtering is needed.
- When the delimiter choice or record selection logic is ambiguous and has not been documented in the conversion specification.

## Inputs

- intermediate JSON object containing a table (array of records) with fields to be converted
- conversion directive specifying value_type='str' with for_each, test, sort_by, and sort_order parameters
- source field references (override, code expression, or record_id path)

## Outputs

- single string value formed by delimiter-separated concatenation of selected record values
- converted JSON record with the constructed string field ready for final format output

## How to apply

Within a MESSES conversion directive with value_type='str', use the for_each pattern to iterate over records in the source table. First, filter records using the 'test' field with field=value syntax to select only relevant records (e.g., test='field_type=author'). Then sort filtered records by specified fields using sort_by and sort_order (ascending or descending). For each selected and sorted record, extract the value using override (direct specification), code (Python evaluation), or table/fields/record_id (nested JSON path lookup). Finally, concatenate all extracted values using the delimiter specified in the for_each structure. This approach ensures deterministic, reproducible string assembly even when source data contains multiple entries.

## Related tools

- **Python** (Evaluation engine for code-based value extraction within for_each loops; interprets code directives to extract or transform field values before concatenation)
- **jsonschema** (Validation of the output JSON and the conversion directive schema to ensure compliance with the Experiment Description Specification and format-specific schemas) — https://pypi.org/project/jsonschema/
- **MESSES convert command** (Orchestrates the application of all conversion directives (including str with for_each) to transform intermediate JSON to target format) — https://github.com/MoseleyBioinformaticsLab/messes

## Examples

```
In a conversion specification JSON, define a str directive with for_each pattern: {"value_type": "str", "for_each": {"table": "authors", "test": "role=corresponding", "sort_by": ["order"], "sort_order": "ascending", "fields": "name", "delimiter": "; "}}
```

## Evaluation signals

- Output string matches expected delimiter-separated concatenation of selected record values in the correct sort order.
- Filter criteria (test field) correctly exclude or include records; verify by spot-checking the source JSON table against the output string.
- Sort order is correct (ascending or descending by specified field) by checking the sequence of values in the final string.
- No extra whitespace or delimiter artifacts; validate against the target schema (e.g., mwTab schema) using jsonschema.
- Round-trip validation: re-parse the output record as JSON and confirm the string field is present, non-empty, and well-formed.

## Limitations

- The for_each pattern assumes all selected records contribute a single value per iteration; records with missing or null values in the extraction path may introduce empty strings or require explicit null handling in the code directive.
- Sorting is performed only on fields present in the source records; if sort_by references a field not in all records, behavior depends on the JSON library's null handling and may not be deterministic across implementations.
- The delimiter is applied verbatim between all concatenated values; no automatic escaping or quoting is performed, so if delimiter characters appear in source values, they will not be escaped in the output string.
- The test filter uses strict field=value equality matching; regex or range-based filtering is not supported by the test directive alone and requires code-based extraction as a workaround.

## Evidence

- [intro] for_each iteration pattern for string concatenation: "for_each iteration with delimiter concatenation across filtered/sorted records"
- [intro] test field filtering mechanism: "**test** - a string of the form "field=value" where field is a field in the records being iterated over and value is what the field must be equal to"
- [intro] sort_by and sort_order parameters: "**sort_by** - a list of fields to sort the input JSON records by before building the value from them. **sort_order** - a string value that is either "ascending" or "descending""
- [intro] str directive value extraction methods: "The str directive assumes that you want to create a string value from information in the input JSON, and that that information is contained within a single table."
- [intro] conversion directive application in MESSES workflow: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
- [readme] CLI invocation of convert command: "messes convert desired_format your_data.json your_format_data"
