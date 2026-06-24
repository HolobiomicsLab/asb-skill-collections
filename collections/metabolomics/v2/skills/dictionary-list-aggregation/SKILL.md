---
name: dictionary-list-aggregation
description: Use when after applying a matrix directive variant (fields_to_headers,
  headers, or collate) to extract and transform individual records into dictionaries
  with field filtering and type coercion applied.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MESSES
  - Python json module
  license_tier: open
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

# dictionary-list-aggregation

## Summary

Aggregate transformed dictionaries produced by matrix directive operations (fields_to_headers, headers, or collate variants) into a single JSON list and serialize to file. This skill converts record-by-record dictionary transformations into a final array-of-objects structure suitable for downstream format conversion or repository submission.

## When to use

After applying a matrix directive variant (fields_to_headers, headers, or collate) to extract and transform individual records into dictionaries with field filtering and type coercion applied. Use this skill when you have a sequence of transformed dictionaries in memory and need to collect them into a single JSON array for output to file or further processing in the MESSES convert pipeline.

## When NOT to use

- Input is already a single-level JSON object (not a list of records) — use str directive instead
- You need to filter or sort the aggregated list after collection — perform filtering before aggregation using the matrix directive's test field parameter
- Output format requires nested or hierarchical structures beyond flat array-of-objects — consider using the section value_type directive

## Inputs

- sequence of transformed dictionaries from matrix directive (fields_to_headers, headers, or collate variant)
- output file path for JSON serialization
- field transformation state (exclusions applied, values coerced to strings)

## Outputs

- JSON file containing array of objects (list of dictionaries)
- validated JSON structure ready for format-specific conversion

## How to apply

Iterate through all transformed dictionary objects produced by the preceding matrix directive step, collecting each into an ordered list in memory. After all records have been processed and aggregated, serialize the list to JSON format using Python's json module and write to the output file path specified in the conversion directive configuration. The aggregation preserves the order and structure of the transformed records and maintains the string type coercion and field exclusions applied during the matrix transformation step. Verify that the output JSON is valid and contains the expected number of dictionary objects (matching the input record count) before proceeding to format-specific validation.

## Related tools

- **MESSES** (orchestrates extraction, validation, and conversion pipeline; dictionary-list-aggregation is the output serialization step of the convert command) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python json module** (serializes aggregated list of dictionaries to JSON format and writes to output file)

## Evaluation signals

- Output file is valid JSON parseable by standard JSON parsers (e.g., python json.load())
- Output JSON structure is an array (list) containing one dictionary object per input record
- Number of dictionary objects in output array equals the number of input records processed by the matrix directive
- All field values in output dictionaries are strings (if values_to_str coercion was applied)
- Fields listed in exclusion_headers are absent from all dictionaries in the output array

## Limitations

- Aggregation occurs entirely in memory; very large record sets (>1 GB) may exhaust available RAM — process in chunks if needed
- Aggregation does not perform secondary filtering or sorting; all filtering must be done during the matrix directive phase using test, sort_by, and sort_order fields
- JSON serialization uses default Python encoding; if non-UTF-8 characters are present in field values, explicit encoding specification may be required

## Evidence

- [other] fields_to_headers variant allows selective field exclusion and type coercion by copying all fields from input records into output dictionaries: "The fields_to_headers matrix directive variant operates by: (1) copying all fields from input records into output dictionaries by default; (2) using exclusion_headers to remove specified fields; and"
- [other] Workflow step 6 explicitly describes list aggregation and JSON serialization: "Aggregate the transformed dictionaries into a list and write the output as JSON."
- [intro] matrix directive produces lists of dictionaries from table data: "The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON"
- [intro] convert command uses conversion directives to transform JSON data: "The convert command of MESSES supports converting JSON data to another JSON format or another supported format. This is done by using conversion directives"
