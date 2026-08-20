---
name: tabular-record-filtering-and-sorting
description: Use when you have extracted tabular data (e.g., protocol descriptions,
  sample preparation steps) into an intermediate JSON representation and need to subset
  records by type or property (e.g., test='type=sample_prep'), then order them consistently
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tabular-record-filtering-and-sorting

## Summary

Apply filtering and sorting operations to tabular records using directive engines to select and order subsets of data by field values and comparison criteria. This skill is essential when extracting structured metadata from experimental tables into JSON, particularly for concatenating or selecting protocol-dependent records that meet specific type or content criteria.

## When to use

You have extracted tabular data (e.g., protocol descriptions, sample preparation steps) into an intermediate JSON representation and need to subset records by type or property (e.g., test='type=sample_prep'), then order them consistently (e.g., by 'id' field in ascending order) before concatenating or aggregating their values into a summary field or downstream output.

## When NOT to use

- Input data is already in final output format (e.g., already a validated mwTab file); filtering and sorting are extract/validate/convert pipeline steps, not post-conversion cleanup.
- Records are untyped or lack consistent sort keys (e.g., 'id' field is missing or non-numeric); sorting will fail or produce unpredictable order.
- You need to preserve all records without loss; filtering by type or property will exclude non-matching records and cannot be reversed without the original input.

## Inputs

- Intermediate JSON representation containing tabular records with typed fields (e.g., protocol table with 'id', 'type', and 'description' fields)
- Directive specification with filter criteria, sort keys, sort order, and delimiter parameters

## Outputs

- Filtered and sorted subset of records (as JSON array or object)
- Concatenated summary string (when using str directive with for_each and delimiter)

## How to apply

Within the MESSES conversion directive engine, specify a str directive with a for_each=True parameter to iterate over multiple records. Define a test filter (e.g., test='type=sample_prep') to select only records matching a target property or type. Chain a sort_by parameter (e.g., sort_by=['id']) with sort_order='ascending' to impose a stable, reproducible order on the filtered subset. Finally, apply a delimiter (e.g., delimiter=' ') to concatenate the sorted field values into a single output string. This approach ensures deterministic output when merging protocol metadata across multiple experiment records, avoiding order-dependent artifacts in downstream schema validation or repository submission.

## Related tools

- **MESSES** (Directive engine providing str directive with for_each, test filter, sort_by, sort_order, and delimiter parameters for filtering and concatenating tabular records) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Runtime environment for executing MESSES extract, validate, and convert commands on tabular data)
- **jsonschema** (Validation library used by MESSES to ensure filtered and sorted JSON records conform to Experiment Description Specification and Protocol Dependent Schema) — https://pypi.org/project/jsonschema/

## Examples

```
messes convert desired_format your_data.json your_format_data
```

## Evaluation signals

- Filtered record count matches expected number of records matching the test criterion (e.g., six records with type='sample_prep').
- Sorted records appear in the specified order by the sort_by field (e.g., 'id' values in ascending order: 1, 2, 3, ... without gaps or reversals).
- Concatenated output string matches the expected summary format with correct delimiter placement (e.g., space-separated descriptions with no leading/trailing delimiters).
- Output JSON validates against the Experiment Description Specification and Protocol Dependent Schema without errors.
- Repeated application of the same filter and sort parameters on the same input produces identical output (determinism check).

## Limitations

- Sorting requires consistent, comparable values in the sort_by field; missing or heterogeneous data types (e.g., mixing numeric and string IDs) may cause undefined sort order or runtime errors.
- The test filter syntax is directive-engine specific and does not support complex boolean logic (e.g., AND/OR combinations); multiple simple filters may require nested directives or post-processing.
- Delimiter-based concatenation is lossy; the original record structure is collapsed into a string, preventing recovery of individual field values or record boundaries without re-parsing.
- Large record sets may exhibit performance degradation in the directive engine; the for_each loop processes each record sequentially without parallelization.

## Evidence

- [other] When applying a str directive with for_each=True, test filtering, sorting, and space delimiter to concatenate multiple protocol records, does the output match the expected concatenated summary string?: "When applying a str directive with for_each=True, test filtering, sorting, and space delimiter to concatenate multiple protocol records, does the output match the expected concatenated summary string?"
- [other] Parse the protocol table entries and filter records matching test='type=sample_prep' using the str directive engine. 3. Sort filtered records by 'id' field in ascending order. 4. Concatenate the sorted records' values using the delimiter ' ' (space): "Parse the protocol table entries and filter records matching test='type=sample_prep' using the str directive engine. 3. Sort filtered records by 'id' field in ascending order. 4. Concatenate the"
- [intro] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
- [intro] The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
- [readme] The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide: "The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide"
