---
name: header-key-value-mapping
description: Use when when you have JSON table records (arrays of field-indexed objects)
  and need to restructure them into dictionaries where specific table columns are
  mapped to new key names, and you want to control which columns appear in the output
  and under what names.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - jsonschema
  - MESSES matrix directive
  license_tier: open
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

# header-key-value-mapping

## Summary

Maps table columns to dictionary key-value pairs using a headers specification (key=value syntax), enabling transformation of flat tabular records into structured key-value objects. This is a core operation within the MESSES matrix directive for converting JSON table data into lists of dictionaries.

## When to use

When you have JSON table records (arrays of field-indexed objects) and need to restructure them into dictionaries where specific table columns are mapped to new key names, and you want to control which columns appear in the output and under what names. Typical triggers: converting experimental metadata from row-indexed tables to column-mapped objects, normalizing field names during format conversion to mwTab or other structured formats, or preparing table data for downstream JSON schema validation.

## When NOT to use

- If input data is already in dictionary form and no key renaming or column selection is needed — the mapping step would be redundant.
- If the headers specification is unknown or undefined; the mapping requires an explicit declaration of which columns map to which output keys.
- If you need to preserve the original table structure exactly as-is; this skill necessarily transforms and selects columns.

## Inputs

- JSON table with records (array of objects with field keys)
- headers specification (list of key=value string pairs)
- optional exclusion_headers list
- optional collate field name (groups records before mapping)

## Outputs

- list of dictionaries (array of objects)
- each dictionary has keys and values mapped per headers specification

## How to apply

Within the matrix directive workflow, after filtering (via test field) and sorting (via sort_by and sort_order) have been applied to input records, extract the headers specification as a list of key=value mapping pairs. For each record or group of records (if using collate), iterate over the headers list and for each pair, parse the key (new field name) and value (table column reference or literal string). Retrieve the corresponding value from the record using the column reference, then add key:value to the output dictionary. If a column reference does not exist in the record, handle gracefully (skip or use null). Exclude any fields listed in the exclusion_headers parameter. The output is a list of dictionaries where each dictionary has been built according to the headers mapping specification.

## Related tools

- **Python** (implements the header mapping iteration and key-value dictionary construction logic)
- **jsonschema** (validates the resulting dictionary objects against the Experiment Description Specification schema) — https://pypi.org/project/jsonschema/
- **MESSES matrix directive** (orchestrates the full matrix conversion pipeline (filtering, sorting, collation, and header mapping)) — https://github.com/MoseleyBioinformaticsLab/messes

## Evaluation signals

- All output dictionaries have exactly the keys specified in the headers list (after exclusion_headers removal), no more, no fewer.
- Each key in the output dictionary maps to the correct value from the input table record, verifiable by spot-checking key-value pairs against source records.
- Fields listed in exclusion_headers do not appear in any output dictionary.
- If collate is used, all records sharing the same collate field value are grouped into a single dictionary, verifiable by checking group membership.
- Output passes validation against the Experiment Description Specification JSON schema and any format-specific schema (e.g. mwTab schema).

## Limitations

- The headers specification must be explicitly and completely defined; partial or ambiguous mappings will fail or produce incomplete output.
- If a column reference in the headers value does not exist in the input record, the behavior depends on error handling (may skip, null-fill, or raise exception) — the article does not specify default behavior, so downstream handling must account for this.
- The mapping is stateless — it does not support computed or derived fields; all output values must come directly from input record columns or be literal strings.
- Collation groups records by exact field value match only; more complex grouping logic (e.g. range-based, fuzzy matching) is not supported by this operation.
- The skill operates on a single table at a time; cross-table joins or hierarchical nesting require higher-level orchestration outside this mapping operation.

## Evidence

- [intro] headers specification extracts key=value pairs from table columns: "building each dictionary using headers specified as key=value pairs where keys/values reference record fields or literal strings"
- [intro] collate field groups records before mapping: "the collate field groups multiple records into single dictionaries based on a shared field value"
- [other] exclusion_headers removes specified fields from output: "The "exclusion_headers" field can then be used to exclude fields from being added."
- [intro] matrix directive produces lists of dictionaries from table data: "The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table."
- [intro] workflow step: extract and map table columns to dictionary key=value pairs: "For each group, extract and map table columns to dictionary key=value pairs using the headers specification."
