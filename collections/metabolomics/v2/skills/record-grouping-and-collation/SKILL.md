---
name: record-grouping-and-collation
description: Use when you have multiple rows in a table that describe the same logical entity (e.g., multiple measurements from the same sample, or repeated attributes under a common identifier) and need to merge them into a single dictionary entry keyed by that shared field.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - jsonschema
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

# Record Grouping and Collation

## Summary

This skill groups multiple table records into single dictionary entries by collating on a shared field value, enabling consolidation of repetitive experimental metadata into hierarchical structures suitable for repository submission.

## When to use

Use this skill when you have multiple rows in a table that describe the same logical entity (e.g., multiple measurements from the same sample, or repeated attributes under a common identifier) and need to merge them into a single dictionary entry keyed by that shared field. This is particularly relevant when converting tabular experimental metadata (MS, NMR runs; sample properties) into JSONized format for deposition into repositories like Metabolomics Workbench.

## When NOT to use

- Input records do not share a common field or the grouping semantics are unclear—collation requires all records in a group to relate to the same logical entity.
- Records within a group conflict on key values (i.e., the same header key would map to different values from different records in the group)—collation does not handle merging conflicts.
- The input is already a feature table or pre-aggregated matrix—collation is a reduction operation, not applicable to data already in the target format.

## Inputs

- JSON table containing records with a shared field to collate on
- Matrix conversion directive specifying collate field, headers (key=value mappings), sort_by field list, sort_order, optional test filter, and optional exclusion_headers

## Outputs

- List of dictionaries (JSON array of objects), one dictionary per collate group, with records merged and mapped according to headers specification

## How to apply

Apply the matrix directive with the collate field parameter set to the name of the column whose values define grouping boundaries. First filter records using the test field (field=value syntax) if only a subset should be collated. Next, sort filtered records by fields listed in sort_by according to sort_order ('ascending' or 'descending') to establish a deterministic order within each group. Then iterate over groups—each group shares the same collate field value—and for each group, construct a dictionary by mapping table columns to key=value pairs using the headers specification (key=value pairs where keys/values reference record fields or literal strings). Finally, exclude any fields listed in exclusion_headers from the output. The result is a list of dictionaries, one per collate group, with all records in that group merged into single key=value mappings.

## Related tools

- **Python** (Language for implementing record iteration, grouping, filtering, and dictionary construction logic in MESSES convert command) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validates the output JSON dictionaries and the input conversion directive specification against the Experiment Description Specification schema) — https://pypi.org/project/jsonschema/

## Examples

```
messes convert mwtab your_data.json output_data --conversion-directive '{"collate": "sample_id", "headers": {"sample": "sample_name", "instrument": "instrument_type"}, "sort_by": ["run_order"], "sort_order": "ascending"}'
```

## Evaluation signals

- Each output dictionary corresponds to exactly one unique value of the collate field; no collate value appears in more than one output dictionary.
- All records sharing the same collate field value are present in the corresponding output dictionary (group is complete and no records are dropped).
- Output dictionaries conform to the headers key=value mapping specification—no extra or missing keys, and values match expected record field references or literal strings.
- Records excluded by the test filter do not appear in any output dictionary.
- Records within each group are ordered according to sort_by and sort_order before collation (verifiable by inspecting intermediate group composition).
- Fields listed in exclusion_headers do not appear in any output dictionary key.

## Limitations

- Collation assumes no conflicting values for the same key within a group; behavior is undefined if two records in the same group map the same header key to different values.
- Grouping is deterministic only if sort_by and sort_order are specified; without sorting, the order of records within a group (and thus the order of merging) may vary.
- Large tables with many records per collate group may produce very large dictionaries, potentially exceeding memory or serialization limits.
- The collate operation does not handle nested or hierarchical table structures; it works on flat record sets.
- If the collate field contains NULL or missing values, behavior depends on the implementation; records with missing collate keys may be grouped together or excluded.

## Evidence

- [other] Core collation mechanism and purpose: "the collate field groups multiple records into single dictionaries based on a shared field value"
- [other] Workflow step: grouping and dictionary construction: "Group records by the collate field value, creating a dictionary per group. For each group, extract and map table columns to dictionary key=value pairs using the headers specification."
- [other] Preprocessing with filtering and sorting: "Apply the test filter to select only records matching the specified field=value condition. Sort the filtered records by the fields listed in sort_by according to sort_order."
- [other] Exclusion of specified headers: "The "exclusion_headers" field can then be used to exclude fields from being added."
- [intro] Matrix directive use case in tabular-to-JSON conversion: "The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON, and that that information is contained within a single table."
- [readme] MESSES workflow context for metadata conversion: "MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into other formats"
