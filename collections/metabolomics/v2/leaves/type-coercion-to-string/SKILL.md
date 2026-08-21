---
name: type-coercion-to-string
description: Use when when converting intermediate JSON records to output dictionaries
  via matrix directives and all field values must be serialized as strings for downstream
  format compatibility (e.g., mwTab format or other repository-specific formats that
  expect string-typed metadata fields).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_3674
  tools:
  - Python
  - MESSES
  license_tier: open
  provenance_tier: literature
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

# type-coercion-to-string

## Summary

Uniformly convert all field values in extracted JSON records to string type during matrix directive transformation. This ensures consistent string representation of heterogeneous data types (numeric, boolean, null) when preparing metadata for repository deposition.

## When to use

When converting intermediate JSON records to output dictionaries via matrix directives and all field values must be serialized as strings for downstream format compatibility (e.g., mwTab format or other repository-specific formats that expect string-typed metadata fields). Particularly necessary when source data contains mixed types (integers, floats, booleans, nulls) that must be unified.

## When NOT to use

- When output format explicitly requires preservation of native types (e.g., numeric fields for statistical analysis or type-strict schemas); use only when repository or format specification mandates string serialization.
- When field values are already uniformly typed or type coercion would semantically corrupt the data (e.g., converting complex objects or nested structures).
- When downstream validation or conversion steps depend on type-level distinctions (e.g., JSON Schema validation expecting 'number' or 'boolean' type keywords).

## Inputs

- Intermediate JSON records (list of dictionaries) after fields_to_headers matrix directive applied
- Processed dictionaries with optional exclusion_headers already applied

## Outputs

- JSON records with all field values converted to string type
- Aggregated list of stringified dictionaries suitable for format-specific conversion or repository submission

## How to apply

After applying the fields_to_headers matrix directive variant to copy fields into output dictionaries, and after applying any exclusion_headers filters to remove unwanted fields, apply the values_to_str transformation to coerce every remaining field value to string type. This is performed as a post-copy, post-exclusion step in the conversion pipeline. The transformation should iterate through each field-value pair in the processed dictionary and invoke a string coercion function (e.g., Python's `str()` or equivalent) on the value. This ensures that numeric identifiers, floating-point measurements, boolean flags, and other non-string types are uniformly represented as text, making them compatible with downstream format specifications that mandate string-typed metadata.

## Related tools

- **MESSES** (Python package providing the matrix directive variant and values_to_str transformation function for type coercion during JSON-to-format conversion) — https://github.com/MoseleyBioinformaticsLab/messes
- **Python** (Runtime environment and standard library (str() function) for implementing field-value iteration and string coercion)

## Examples

```
messes convert mwTab intermediate_data.json output_data.mwTab --schema conversion_directives.json
```

## Evaluation signals

- All field values in output dictionaries are of Python type `str` or equivalent string representation (inspect via `type()` or JSON schema validation).
- No numeric, boolean, or null values remain unquoted in the JSON output; all values are enclosed in quotes.
- Round-trip validation: re-parsing output JSON and inspecting field types confirms string-only representation.
- Downstream format conversion (e.g., to mwTab) succeeds without type mismatch errors.
- Schema validation against repository-specific schemas (e.g., mwTab schema) passes without type errors on previously coerced fields.

## Limitations

- Type coercion to string is irreversible; original numeric precision, type semantics, or range information may be lost or require explicit schema documentation for recovery.
- Large numeric values may undergo precision loss or rounding during string representation, depending on JSON serializer behavior.
- String coercion of complex or nested objects (arrays, sub-dictionaries) may produce non-human-readable or non-parseable string representations; apply only to scalar field values.
- Downstream tools expecting type-level metadata (e.g., statistical software expecting numeric types) may require explicit type re-annotation after string coercion.

## Evidence

- [other] fields_to_headers matrix directive variant with values_to_str: "using values_to_str to convert all field values to strings"
- [intro] Matrix directive for list-of-dictionaries output: "The matrix directive assumes that you want to create a list of dictionaries (aka array of objects) from information in the input JSON"
- [intro] Conversion workflow includes coercion step: "Apply the values_to_str transformation to coerce all remaining field values to string type. Aggregate the transformed dictionaries into a list and write the output as JSON"
- [intro] Convert command applies directives during JSON transformation: "The convert command of MESSES supports converting JSON data to another JSON format or another supported format. This is done by using conversion directives"
