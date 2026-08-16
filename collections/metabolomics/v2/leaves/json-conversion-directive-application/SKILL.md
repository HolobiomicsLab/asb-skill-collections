---
name: json-conversion-directive-application
description: Use when you have validated intermediate JSON data conforming to the
  Experiment Description Specification and need to convert it to a target format (e.g.,
  mwTab for Metabolomics Workbench deposition).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MESSES
  - jsonschema
  license_tier: open
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
  that facilitates the conversion of tabular data into other formats
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

# json-conversion-directive-application

## Summary

Apply conversion directives (str, matrix, or section value_type patterns) to transform intermediate JSON metadata into target format representations, using filtering, sorting, and field selection to aggregate or restructure tabular records. This skill is essential when converting structured experimental metadata from MESSES's standardized JSON schema into domain-specific formats like mwTab for repository deposition.

## When to use

You have validated intermediate JSON data conforming to the Experiment Description Specification and need to convert it to a target format (e.g., mwTab for Metabolomics Workbench deposition). The conversion requires selective extraction, concatenation, or restructuring of records from JSON tables using field filtering, sorting, and aggregation rules defined in conversion directives.

## When NOT to use

- Input JSON has not been validated against the Experiment Description Specification and Protocol Dependent Schema — validate first to avoid malformed directive application.
- Target format is not supported by MESSES (currently only mwTab is fully supported); attempting to apply directives to unsupported formats will fail.
- Intermediate JSON data are already in the target format and no transformation is needed; conversion directives are unnecessary.

## Inputs

- Intermediate JSON file conforming to Experiment Description Specification
- Conversion directives specification (JSON with value_type, test, sort_by, sort_order, delimiter, headers, collate, fields_to_headers, exclusion_headers fields)
- Target format schema definition

## Outputs

- Converted JSON or target format file (e.g., mwTab)
- Single string value (str directive output)
- List of dictionaries / array of objects (matrix directive output)
- Nested section structure (section directive output)

## How to apply

For each conversion directive in your conversion specification, identify the value_type field (str, matrix, or section) and apply the corresponding transformation pattern. For str directives: apply a test filter (field=value syntax) to select records, sort them using sort_by and sort_order fields, and concatenate the specified fields using the delimiter. For matrix directives: extract headers from the table, optionally collate or use fields_to_headers to reshape data, and exclude unwanted fields via exclusion_headers. For section directives: recursively apply conversion rules to nested table structures. Validate that the output schema matches the target format specification before deposition.

## Related tools

- **MESSES** (Python package that implements the convert command to apply conversion directives and transform intermediate JSON to target formats) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validates intermediate JSON against conversion directive specifications and target format schemas before and after directive application) — https://pypi.org/project/jsonschema/

## Examples

```
messes convert mwTab your_data.json your_mwtab_output --directives conversion_spec.json
```

## Evaluation signals

- Output string (str directive) correctly concatenates filtered and sorted records using the specified delimiter; verify by comparing against expected SAMPLEPREP_SUMMARY or equivalent reference output.
- Matrix directive output is a valid list of dictionaries with expected headers and no excluded fields; check schema compliance and row/column counts against source table.
- Records are filtered by test condition (e.g., type=sample_prep) before aggregation; inspect output to confirm only matching records are included.
- Records are sorted in the specified order (ascending/descending by sort_by fields); verify record sequence matches sort specification.
- Output JSON or target format file validates against the target format schema (mwTab schema for Metabolomics Workbench) with zero errors.

## Limitations

- Conversion directives require precise field names and test conditions; mismatched field names or typos in test filters will silently fail or produce empty results.
- The for_each str directive concatenates only records from a single table; cross-table joins or complex nested aggregations require multiple directive passes or custom code.
- sort_by field list is applied as a multi-key sort in the order specified; unexpected record ordering can result if sort key priority is misunderstood.
- Currently only mwTab format is fully supported for conversion; other domain formats require custom directive schemas.
- Large JSON datasets with many records may produce very long concatenated strings or large matrix outputs; memory and performance constraints apply at scale.

## Evidence

- [intro] str directive with test, sort_by, and delimiter concatenation: "The for_each directive iterates over records in the protocol table filtered by test=type=sample_prep, sorts them by id in ascending order, and concatenates their description fields with space"
- [other] conversion directive value_type specification: "Every record must have a "value_type" field, and the value of this field determines the other required and meaningful fields the record can have. The allowed values for the "value_type" field are"
- [intro] str directive pattern definition: "The str directive assumes that you want to create a string value from information in the input JSON, and that that information is contained within a single table."
- [intro] matrix directive pattern definition: "The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table."
- [intro] test filter field=value syntax: "**test** - a string of the form "field=value" where field is a field in the records being iterated over and value is what the field must be equal to"
- [intro] sort_by and sort_order parameters: "**sort_by** - a list of fields to sort the input JSON records by before building the value from them. **sort_order** - a string value that is either "ascending" or "descending""
- [intro] exclusion_headers for matrix output: "The "exclusion_headers" field can then be used to exclude fields from being added."
- [intro] convert command workflow step: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
- [readme] README convert command usage: "messes convert desired_format your_data.json your_format_data"
