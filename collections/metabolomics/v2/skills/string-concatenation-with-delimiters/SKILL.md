---
name: string-concatenation-with-delimiters
description: Use when when you need to aggregate values from multiple records in a JSON input document into a single concatenated string field (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3908
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - Python
  - jsonschema
  - MESSES
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
- utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_messes
    doi: 10.3390/metabo13070842
    title: messes
  dedup_kept_from: coll_messes
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo13070842
  all_source_dois:
  - 10.3390/metabo13070842
  - 10.3390/metabo11030163
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# String Concatenation with Delimiters

## Summary

Apply str directives with for_each iteration, optional filtering, and delimiter-based field concatenation to combine values from multiple records into a single summary string. Used in JSON-to-JSON conversion workflows to aggregate protocol descriptions, metadata fields, or enumerated values across filtered record sets.

## When to use

When you need to aggregate values from multiple records in a JSON input document into a single concatenated string field (e.g., combining protocol step descriptions, sample preparation methods, or enumerated codes) using a specified delimiter, with optional test-based filtering and sort ordering applied before concatenation.

## When NOT to use

- Input records are already in the desired concatenated format (no aggregation needed).
- Individual field values must be transformed or computed independently rather than combined via delimiter.
- The order of concatenation is semantically irrelevant and sorting overhead is not justified.

## Inputs

- conversion directives JSON file (containing str-type directive with for_each, test, sort_by, sort_order, delimiter, fields sub-fields)
- input JSON document (containing array or object collection to iterate over)
- optional sort keys and filter conditions

## Outputs

- resolved JSON document with concatenated str field populated
- validated output JSON matching input schema

## How to apply

Define a str directive in the conversion directives JSON file with for_each=True to iterate over a designated array or object collection in the input JSON. If filtering is needed, specify a test sub-directive (e.g., test='type=sample_prep') to select only records matching that condition. Use sort_by and sort_order sub-directives to order the filtered records before concatenation. Specify the delimiter (e.g., ' ' for space, ',' for comma) and the field names to extract and concatenate. The directive engine iterates over the matching records, extracts the specified fields, sorts them if required, and joins them using the delimiter, writing the result to the output JSON field. Validate the output string against the expected format to confirm correct record selection, ordering, and delimiter application.

## Related tools

- **Python** (Runtime for evaluating str directive logic and executing concatenation and iteration)
- **jsonschema** (Validation of resolved output JSON against the input specification and format-specific schemas) — https://pypi.org/project/jsonschema/
- **MESSES** (Extract, validate, and convert framework that implements the str directive resolver for JSON-to-JSON and JSON-to-format conversion) — https://github.com/MoseleyBioinformaticsLab/messes

## Examples

```
messes convert desired_format data_with_str_directives.json output_data
```

## Evaluation signals

- Output concatenated string contains all expected field values from filtered records in the specified sort order.
- Delimiter appears correctly between each concatenated field value (no missing or extra delimiters).
- Records selected for concatenation match the test filter condition (e.g., only type='sample_prep' records included).
- Records appear in the output in the order specified by sort_by and sort_order (e.g., ascending by id field).
- Output JSON validates against the schema without errors or warnings using jsonschema.

## Limitations

- The for_each directive requires the target field or collection to exist in the input JSON; missing collections will skip concatenation.
- The test sub-directive uses simple equality matching; complex conditional logic is limited and may require code sub-directive as fallback.
- Sort ordering applies only to the records themselves before concatenation; individual field values within a record are not reordered.
- The delimiter is applied uniformly between all concatenated values; conditional or context-dependent delimiters are not supported.

## Evidence

- [other] for_each iterates over all records with optional test filtering and delimiter-separated concatenation: "for_each iterates over all records with optional test filtering and delimiter-separated concatenation"
- [other] When applying a str directive with for_each=True, test filtering, sorting, and space delimiter to concatenate multiple protocol records: "When applying a str directive with for_each=True, test filtering, sorting, and space delimiter to concatenate multiple protocol records"
- [other] for_each directive with test='type=sample_prep', sort_by=['id'], sort_order='ascending', and delimiter=' ' produces a SAMPLEPREP_SUMMARY concatenating six sample preparation descriptions: "for_each directive with test='type=sample_prep', sort_by=['id'], sort_order='ascending', and delimiter=' ' produces a SAMPLEPREP_SUMMARY concatenating six sample preparation descriptions"
- [other] Parse conversion directives JSON file to extract str-type directive definition with all sub-fields (override, code, record_id, for_each, test, sort_by, sort_order, delimiter, fields).: "Parse conversion directives JSON file to extract str-type directive definition with all sub-fields (override, code, record_id, for_each, test, sort_by, sort_order, delimiter, fields)."
- [other] If for_each is specified, iterate over the designated array or object collection in the input JSON; otherwise apply directive once to the root or specified record_id target.: "If for_each is specified, iterate over the designated array or object collection in the input JSON; otherwise apply directive once to the root or specified record_id target."
- [intro] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
