---
name: matrix-directive-field-mapping
description: Use when you have extracted tabular data in intermediate JSON form and need to convert a table of records into a list of dictionaries (array of objects) where each row becomes a dictionary entry, optionally removing sensitive or irrelevant fields and normalizing all values to strings for downstream.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MESSES (Metadata from Experimental SpreadSheets Extraction System)
  - jsonschema
derived_from:
- doi: 10.3390/metabo13070842
  title: messes
- doi: 10.3390/metabo11030163
  title: ''
evidence_spans:
- MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package
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

# matrix-directive-field-mapping

## Summary

Apply the matrix directive's fields_to_headers variant to copy all fields from input table records into output dictionaries, with optional selective field exclusion and type coercion to strings. This skill transforms tabular data into arrays of objects suitable for JSON schema validation and format conversion.

## When to use

Use this skill when you have extracted tabular data in intermediate JSON form and need to convert a table of records into a list of dictionaries (array of objects) where each row becomes a dictionary entry, optionally removing sensitive or irrelevant fields and normalizing all values to strings for downstream schema validation or format deposition.

## When NOT to use

- When input records contain nested objects or arrays that should not be flattened to string representation — fields_to_headers assumes flat record structure.
- When you need to preserve original data types (integer, boolean, numeric) throughout the pipeline — values_to_str coercion is lossy.
- When your table is already in the desired output dictionary format and no field exclusion or normalization is needed — overhead of the directive is unjustified.

## Inputs

- Intermediate JSON representation containing table data (array of record objects)
- Exclusion headers list (optional; list of field names to remove)
- Type coercion flag (optional; boolean indicating whether to convert all values to strings)

## Outputs

- JSON array of dictionaries, where each dictionary represents a transformed table record with selected fields and coerced values
- Output JSON file ready for validation against JSON Schema or conversion to target format

## How to apply

Load the intermediate JSON data containing table records into memory. For each record in the input table, extract all fields and their values as key-value pairs. Apply the fields_to_headers transformation to copy all extracted fields into a new output dictionary for each record. Filter the resulting dictionaries using the exclusion_headers parameter to remove any fields whose names match entries in a user-supplied exclusion list. If value normalization is required (e.g., for compatibility with string-only downstream formats), apply the values_to_str transformation to coerce all remaining field values to string type. Aggregate the transformed dictionaries into a single list and serialize to JSON output. This approach preserves all field information by default while allowing fine-grained control over which fields are retained and how their types are normalized.

## Related tools

- **MESSES (Metadata from Experimental SpreadSheets Extraction System)** (Python package providing the convert command, which applies matrix directives (including fields_to_headers) to transform extracted JSON data) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Language used to implement the field extraction, dictionary construction, and value coercion logic within MESSES convert workflows)
- **jsonschema** (Validation library used to verify that the output dictionaries conform to the Experiment Description Specification and format-specific schemas) — https://pypi.org/project/jsonschema/

## Examples

```
messes convert mwTab your_data.json your_output.mwTab
```

## Evaluation signals

- Output JSON file parses without syntax errors and deserializes into a valid Python list of dictionaries.
- Each output dictionary contains exactly the expected fields (all original fields minus those in exclusion_headers list).
- If values_to_str was applied, all field values in output dictionaries are of type string; no numeric, boolean, or null types remain.
- Row count and record order are preserved: output array length equals input table row count (minus any filtered records).
- Output conforms to Experiment Description Specification schema and format-specific JSON Schema using jsonschema validation without errors.

## Limitations

- The fields_to_headers variant does not support nested field selection or dot-notation path expressions; it operates only on flat top-level fields in each record.
- Applying values_to_str coercion is irreversible; original numeric and boolean types cannot be recovered from the output without external metadata.
- Large tables with many fields may produce very large JSON output if exclusion_headers is not sufficiently restrictive.
- The directive assumes all input records have a homogeneous schema; records with heterogeneous field sets will result in dictionaries with different key sets in the output array.

## Evidence

- [other] The fields_to_headers matrix directive variant operates by: (1) copying all fields from input records into output dictionaries by default; (2) using exclusion_headers to remove specified fields; and (3) using values_to_str to convert all field values to strings.: "The fields_to_headers matrix directive variant operates by: (1) copying all fields from input records into output dictionaries by default; (2) using exclusion_headers to remove specified fields; and"
- [other] The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table.: "The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table."
- [other] The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
- [other] The "exclusion_headers" field can then be used to exclude fields from being added.: "The "exclusion_headers" field can then be used to exclude fields from being added."
- [readme] MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into other formats.: "MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into other formats."
