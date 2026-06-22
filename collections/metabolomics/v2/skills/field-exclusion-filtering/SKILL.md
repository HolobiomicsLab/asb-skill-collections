---
name: field-exclusion-filtering
description: Use when when transforming tabular data via the matrix directive and you need to copy most or all fields from input records into output dictionaries, but must explicitly exclude certain named fields (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3375
  tools:
  - Python
  - MESSES
  - messes convert command
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
---

# field-exclusion-filtering

## Summary

Selectively remove specified fields from tabular records during matrix directive transformation, allowing practitioners to copy all fields from input records into output dictionaries while excluding unwanted columns by name. This is essential when converting intermediate JSON table data to final formats where certain fields must be omitted.

## When to use

When transforming tabular data via the matrix directive and you need to copy most or all fields from input records into output dictionaries, but must explicitly exclude certain named fields (e.g., internal identifiers, staging columns, or redundant headers) from appearing in the final output.

## When NOT to use

- If you need to include all fields from input records without any exclusions — use the base fields_to_headers variant without exclusion_headers parameter.
- If fields to remove are conditional on record content or dynamic values — exclusion_headers operates on static field name matching only, not on value-based conditions.
- If the field names to exclude are not known in advance or differ per-record — the exclusion list must be fixed and pre-defined in the conversion directive.

## Inputs

- intermediate JSON data containing table records (from MESSES extract command)
- list of field names to exclude (exclusion_headers parameter)
- conversion directive specifying value_type='matrix' and fields_to_headers variant

## Outputs

- list of dictionaries with specified fields removed
- JSON output file or in-memory dictionary collection

## How to apply

Within a matrix directive conversion specification, populate the 'exclusion_headers' field with a list of field names to remove from each output dictionary. The transformation operates by first copying all fields from input records into new dictionaries, then filtering out any fields whose names match entries in the exclusion list before final aggregation. This is typically applied after extraction and validation steps, as part of the convert command workflow that transforms intermediate JSON to a target format like mwTab. The exclusion happens at the per-record level, so each record is processed independently, ensuring consistent field removal across all records in the output.

## Related tools

- **MESSES** (Python package that implements the matrix directive and exclusion_headers filtering during JSON-to-format conversion) — https://github.com/MoseleyBioinformaticsLab/messes
- **messes convert command** (CLI command that applies conversion directives (including exclusion_headers) to transform intermediate JSON to target formats) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Runtime language for executing the field-exclusion filtering logic within MESSES)

## Examples

```
messes convert mwtab intermediate_data.json output_data --conversion-directive '{"fields_to_headers": {"exclusion_headers": ["internal_id", "staging_flag"]}}'
```

## Evaluation signals

- Verify that all fields named in exclusion_headers are absent from every record in the output dictionary list.
- Confirm that all other fields present in the input records (those NOT in exclusion_headers) appear in the output dictionaries.
- Check that the number of fields in each output record equals (input field count - exclusion_headers list length).
- Validate output JSON against the target format schema (e.g., mwTab schema) to ensure excluded fields do not cause schema violations.
- Compare output record structure across multiple records to ensure exclusion is consistent and no field names are partially or conditionally removed.

## Limitations

- Exclusion operates only on exact field name matches; partial matches or regex patterns are not supported.
- The exclusion_headers list is static and cannot adapt based on record-level metadata or conditional logic.
- If a required field for the target format is accidentally included in exclusion_headers, validation will fail and must be corrected manually in the conversion directive.
- Field exclusion happens after all fields are copied; for large records with many fields, memory overhead may occur before filtering.

## Evidence

- [intro] Exclusion_headers usage in matrix directive: "The "exclusion_headers" field can then be used to exclude fields from being added."
- [intro] Matrix directive copies all fields by default: "The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON"
- [intro] Conversion directive workflow context: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
- [other] Task card finding on exclusion mechanism: "using exclusion_headers to remove specified fields; and (3) using values_to_str to convert all field values to strings"
