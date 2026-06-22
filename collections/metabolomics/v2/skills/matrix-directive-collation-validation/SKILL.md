---
name: matrix-directive-collation-validation
description: Use when you have IC-FTMS measurement records in JSON format with multiple samples per metabolite assignment and you need to verify that a matrix directive with collate='assignment' correctly groups records by assignment identifier and merges sample intensity values into a single dictionary per.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_3172
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

# matrix-directive-collation-validation

## Summary

Apply a matrix conversion directive with collate='assignment' to group IC-FTMS measurement records by metabolite assignment and merge their sample intensity data into unified dictionaries. This skill validates that the directive correctly consolidates multiple records sharing the same metabolite assignment into single output objects.

## When to use

Use this skill when you have IC-FTMS measurement records in JSON format with multiple samples per metabolite assignment and you need to verify that a matrix directive with collate='assignment' correctly groups records by assignment identifier and merges sample intensity values into a single dictionary per unique assignment.

## When NOT to use

- Input records are not yet in the MESSES intermediate JSON format — use the extract command first to convert tabular data to JSON
- You need to collate records by a different field (e.g., sample identifier or compound name) — the collate='assignment' directive is specific to assignment-based grouping
- Records contain hierarchical or nested sample structures where intensity merging logic differs from simple dictionary aggregation — validate the directive behavior against your specific data schema first

## Inputs

- IC-FTMS measurement records in JSON format with multiple samples per metabolite assignment
- matrix conversion directive specification with collate='assignment' parameter
- experiment metadata in MESSES Experiment Description Specification format

## Outputs

- list of dictionaries grouped by metabolite assignment
- each dictionary containing metabolite name and merged sample intensity data
- validation report confirming correct collation of records by assignment

## How to apply

Load the IC-FTMS measurement dataset from MESSES documentation in JSON format. Define a matrix conversion directive specifying collate='assignment' to group measurement records by their metabolite assignment field. Execute the MESSES convert command with this directive to transform the JSON structure into a list of dictionaries. For each unique assignment value in the input, verify that exactly one output dictionary exists containing the metabolite name and a merged collection of intensity values from all input samples sharing that assignment. Compare the resulting output structure against the expected JSON documented in the Collate section of the MESSES specification, checking that the number of output dictionaries matches the number of unique assignments and that no sample intensity data is lost or duplicated.

## Related tools

- **MESSES** (command-line tool and Python library that executes the convert command to apply matrix directives and transform JSON data according to collation specifications) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (validates the JSON structure of measurement records and the output of the collation directive against the Experiment Description Specification schema) — https://pypi.org/project/jsonschema/
- **Python** (runtime environment for MESSES package and JSON manipulation)

## Examples

```
messes convert matrix your_data.json your_output.json --directive '{"collate": "assignment"}'
```

## Evaluation signals

- Number of output dictionaries equals the number of unique metabolite assignments in the input records
- Each output dictionary contains exactly one metabolite name corresponding to its assignment group
- All sample intensity values from input records with the same assignment are present in the merged output dictionary with no data loss
- No duplicate intensity entries or sample data across output dictionaries
- Output JSON structure validates against the Collate section schema in the MESSES documentation

## Limitations

- The collate='assignment' directive assumes a one-to-one mapping between assignment identifiers and metabolite names; conflicting metabolite names for the same assignment will not be detected or reported
- Intensity value merging uses simple dictionary aggregation; complex or conditional merge logic (e.g., averaging, filtering by quality threshold) is not supported by this basic directive
- The directive does not validate or reconcile differences in sample metadata or provenance across records being merged under the same assignment

## Evidence

- [other] When a matrix directive with collate='assignment' is applied to measurement records containing multiple samples for the same metabolite assignment, does the directive correctly group records by assignment and merge their sample intensity data into a single dictionary?: "When a matrix directive with collate='assignment' is applied to measurement records containing multiple samples for the same metabolite assignment, does the directive correctly group records by"
- [other] The collate directive groups four measurement records into two dictionaries by assignment, with each dictionary containing the metabolite name and intensity values from all samples sharing that assignment: (S)-2-Acetolactate with two samples and (S)-3-Sulfonatolactate with two samples.: "The collate directive groups four measurement records into two dictionaries by assignment, with each dictionary containing the metabolite name and intensity values from all samples sharing that"
- [other] Load the IC-FTMS measurement example dataset from the MESSES documentation in JSON format. Parse and apply a matrix conversion directive specifying collate='assignment' to transform the JSON structure. Execute the convert command with the matrix directive to produce a list of dictionaries.: "Load the IC-FTMS measurement example dataset from the MESSES documentation in JSON format. Parse and apply a matrix conversion directive specifying collate='assignment'"
- [intro] The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
- [intro] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
- [other] utilizing `JSON Schema <https://json-schema.org/understanding-json-schema/>`_ (`jsonschema <https://pypi.org/project/jsonschema/>`_): "utilizing `JSON Schema` (`jsonschema <https://pypi.org/project/jsonschema/>`_)"
