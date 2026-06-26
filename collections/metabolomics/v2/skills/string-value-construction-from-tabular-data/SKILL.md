---
name: string-value-construction-from-tabular-data
description: Use when you have a JSON table (e.g., protocol records with 'type', 'id',
  and 'description' fields) and need to create a single concatenated string value
  by selecting a subset of records matching a condition (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3673
  tools:
  - Python
  - MESSES
  - jsonschema
  license_tier: open
  provenance_tier: literature
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

# string-value-construction-from-tabular-data

## Summary

Construct single string values from filtered and sorted records in a tabular JSON table using the str conversion directive with test, sort_by, and delimiter fields. This skill enables aggregation of multiple protocol or metadata records into a human-readable summary field suitable for deposition into structured data repositories.

## When to use

You have a JSON table (e.g., protocol records with 'type', 'id', and 'description' fields) and need to create a single concatenated string value by selecting a subset of records matching a condition (e.g., type='sample_prep'), ordering them by a specified field, and joining their text fields with a delimiter. Common use case: summarizing all sample preparation steps into a SAMPLEPREP_SUMMARY field for metabolomics repository submission.

## When NOT to use

- Input records do not share a common schema or lack the fields specified in the test, sort_by, or extraction directives; the conversion will fail or produce incomplete output.
- You need to preserve record structure, field-level relationships, or hierarchical metadata; use matrix directives instead to output an array of objects.
- Records require complex conditional logic beyond simple field=value filtering; consider pre-processing the JSON or implementing custom code directives.

## Inputs

- JSON table with records containing at least: a field matching the test condition (e.g., 'type'), a sort key field (e.g., 'id'), and a text extraction field (e.g., 'description')

## Outputs

- Single concatenated string value with multiple record texts joined by the specified delimiter (e.g., 'Tissue is frozen in liquid nitrogen to stop metabolic processes. Frozen tissue is ground in a SPEX grinder...')

## How to apply

Define a str conversion directive with three key fields: (1) set the 'test' field to a filter condition in the form 'field=value' to select only records matching that criterion; (2) populate 'sort_by' with the field name(s) to order records (e.g., 'id') and set 'sort_order' to 'ascending' or 'descending' to ensure deterministic, consistent ordering; (3) specify a 'delimiter' (commonly a space) to join the concatenated text. The converter iterates over the filtered and sorted records, extracts the designated text field (e.g., 'description') from each, and joins them into a single string. This approach ensures reproducible, sortable aggregation of heterogeneous protocol or metadata records into a single normalized value suitable for validation and repository deposition.

## Related tools

- **MESSES** (Command-line tool and Python library that implements the convert command with str directives to transform filtered and sorted tabular JSON records into concatenated string values.) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validates the input JSON and the output string value against the Experiment Description Specification schema to ensure all required fields are present and properly formatted before and after conversion.) — https://pypi.org/project/jsonschema/

## Examples

```
messes convert mwtab your_data.json output_directory --conversion-directives conversion_spec.json
```

## Evaluation signals

- Output string contains all expected text fragments from filtered records in the correct sort order (ascending or descending by the sort_by field).
- Delimiter correctly separates each record's text field; no missing or extra delimiters between adjacent records.
- Records not matching the test filter (e.g., type != 'sample_prep') are excluded from the output string.
- Output string passes validation against the relevant JSON Schema (Experiment Description Specification or format-specific schema) for the target field.
- Repeated runs with the same input produce identical output strings (deterministic due to consistent sort_by ordering).

## Limitations

- The test field supports only simple equality conditions (field=value); more complex filtering (e.g., regex, range queries, OR logic) requires preprocessing or custom code directives.
- Sort order is limited to ascending or descending on a single field or list of fields; custom collation or multi-key sorting with varying directions per key is not directly supported.
- The skill assumes all records in the target table share the same schema; heterogeneous records may produce malformed or unexpected concatenation if the extraction field is missing in some records.
- Large tables with many records matching the filter may produce very long output strings; no built-in truncation or pagination is provided.

## Evidence

- [other] The for_each directive iterates over records in the protocol table filtered by test=type=sample_prep, sorts them by id in ascending order, and concatenates their description fields with space delimiters to produce: 'Tissue is frozen in liquid nitrogen to stop metabolic processes. Frozen tissue is ground in a SPEX grinder under liquid nitrogen to homogenize the sample. Before going into the IC-FTMS the frozen sample is reconstituted in water. acetone extraction of polar metabolites Lipid extraction from homogenate. Polar extraction from homogenate, lypholized, and frozen. Protein extraction and quantification.': "Apply the test filter to select only records where type='sample_prep'. 3. Sort the filtered records by the 'id' field in ascending order. 4. Join the selected records using the space delimiter"
- [intro] The str directive assumes that you want to create a string value from information in the input JSON, and that that information is contained within a single table.: "The str directive assumes that you want to create a string value from information in the input JSON, and that that information is contained within a single table."
- [intro] **test** - a string of the form "field=value" where field is a field in the records being iterated over and value is what the field must be equal to in order to be used to build the string value.: "**test** - a string of the form "field=value" where field is a field in the records being iterated over and value is what the field must be equal to"
- [intro] **sort_by** - a list of fields to sort the input JSON records by before building the value from them. **sort_order** - a string value that is either "ascending" or "descending": "**sort_by** - a list of fields to sort the input JSON records by before building the value from them. **sort_order** - a string value that is either "ascending" or "descending""
- [intro] The convert command was designed to transform the JSON format described in the :doc:`experiment_description_specification` to the JSON version of any of the supported formats and then to the final desired format using conversion directives: "The convert command was designed to transform the JSON format described in the :doc:`experiment_description_specification` to the JSON version of any"
- [readme] The conversion step converts the extracted data to the form that is accepted by the online repository. There is an initial steep learning curve. But once the extraction, validation, and conversion settings are worked out, this process can be easily added to your data generation and analysis workflows.: "The conversion step converts the extracted data to the form that is accepted by the online repository"
