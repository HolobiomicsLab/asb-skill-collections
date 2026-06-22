---
name: metadata-structure-transformation
description: Use when you have raw tabular experimental metadata (mass spectrometry or NMR sample descriptions, sample-to-treatment mappings, instrument parameters, etc.) that needs to be deposited into a structured online repository like Metabolomics Workbench, but the raw format does not conform to the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3750
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - jsonschema
  - MESSES (Metadata from Experimental SpreadSheets Extraction System)
  techniques:
  - NMR
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

# metadata-structure-transformation

## Summary

Transform tabular experimental metadata (Excel/CSV) into clean, standardized JSONized intermediate format using a tagging system, then convert to repository-compliant output formats (e.g., mwTab for Metabolomics Workbench). This skill bridges raw data entry and repository submission by enforcing schema compliance and enabling format-agnostic validation.

## When to use

You have raw tabular experimental metadata (mass spectrometry or NMR sample descriptions, sample-to-treatment mappings, instrument parameters, etc.) that needs to be deposited into a structured online repository like Metabolomics Workbench, but the raw format does not conform to the repository's expected schema. Use this skill when you need to move from spreadsheet-based data entry to a standardized, validatable, and format-convertible representation.

## When NOT to use

- Input is already in the target repository format (e.g., already a valid mwTab file) — use direct validation instead.
- Data is already properly structured JSON conforming to Experiment Description Specification and your target format schema — skip directly to conversion.
- Tabular data is raw instrument output (e.g., raw mass spectrometry data files, unprocessed spectral data) rather than experimental metadata or sample annotations — use instrument-specific parsing tools instead.

## Inputs

- Tabular data file (Excel .xlsx or CSV format) with raw experimental metadata
- Tagging specification defining semantic markup for tabular columns
- Protocol Dependent Schema (JSON Schema) describing project-specific constraints
- Format-specific schema (e.g., mwTab schema) for target repository
- Conversion directives (JSON) specifying output transformations (e.g., collate, filter, rename operations)

## Outputs

- Intermediate JSON file conforming to Experiment Description Specification
- Validated intermediate JSON with error/warning report
- Repository-compliant output file (e.g., mwTab format for Metabolomics Workbench)

## How to apply

The workflow follows three steps: (1) Add a tagging layer to your tabular data (manual or automated) that marks columns with semantic meaning (e.g., sample ID, metabolite name, intensity value). (2) Run the `extract` command to parse the tagged tabular data into an intermediate JSON representation conforming to the Experiment Description Specification schema. (3) Validate the extracted JSON using the `validate` command against the Protocol Dependent Schema, custom project schemas, and format-specific schemas (e.g., mwTab schema) to catch errors. (4) Apply conversion directives (such as `collate='assignment'` for grouping records by metabolite assignment) using the `convert` command to transform the JSON into the final repository format. The rationale is that JSON serves as a format-agnostic interchange layer: once data is correctly extracted and validated in JSON form, it can be reliably converted to any supported output format without re-entering or re-validating the raw data.

## Related tools

- **MESSES (Metadata from Experimental SpreadSheets Extraction System)** (Core command-line tool for executing extract, validate, and convert commands on tabular and JSON data) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Validates intermediate and output JSON against Experiment Description Specification, Protocol Dependent Schema, and format-specific schemas) — https://pypi.org/project/jsonschema/
- **Python** (Runtime language for MESSES package and programmatic extension of conversion logic)

## Examples

```
messes extract your_data.csv --output your_data.json && messes validate json your_data.json --pds your_schema.json --format mwTab && messes convert mwTab your_data.json output_data
```

## Evaluation signals

- Extracted JSON file is valid against the Experiment Description Specification schema (confirmed by `validate` command with zero errors).
- When conversion directives are applied (e.g., `collate='assignment'`), measurement records are correctly grouped: verify that all records sharing the same metabolite assignment are merged into a single dictionary containing the metabolite name and a merged sample intensity dictionary, with no duplicates or lost records.
- Validation report from `validate` command shows zero errors against Protocol Dependent Schema and format-specific schema (e.g., mwTab schema).
- Final output file can be parsed by the target repository's ingestion tools without schema violations or format errors.
- Spot-check that sample intensity values, metabolite names, and assignment IDs are preserved (not truncated, corrupted, or reordered) during extraction and conversion steps.

## Limitations

- Requires manual or automatable tagging of raw tabular data before extraction; untagged or inconsistently tagged columns will be missed or cause extraction errors.
- The tagging system and conversion directives have a steep initial learning curve; proper understanding of the Experiment Description Specification and Protocol Dependent Schema is essential before use.
- Conversion to non-mwTab formats is not yet supported by the library (only mwTab is currently documented as a supported output format for Metabolomics Workbench).
- Complex data transformations beyond simple collation, filtering, and renaming may require custom JSON-to-JSON directives or programmatic extension of the MESSES library.
- File format support is limited to tabular input (Excel, CSV); other raw data formats (e.g., binary instrument files, HDF5) must be converted to tabular form before extraction.

## Evidence

- [readme] MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into other formats.: "MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into other formats."
- [readme] Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats.: "Simply add a layer of tags to any tabular data and MESSES can transform it into an intermediate JSON representation and then convert it to any of the supported formats."
- [readme] MESSES breaks up the process into 3 steps: extract, validate, and convert.: "MESSES breaks up the process into 3 steps: extract, validate, and convert."
- [readme] The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized.: "The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized."
- [readme] The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide, and a built in schema specific for the format you wish to convert to.: "The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide, and a"
- [other] The collate directive groups four measurement records into two dictionaries by assignment, with each dictionary containing the metabolite name and intensity values from all samples sharing that assignment.: "The collate directive groups four measurement records into two dictionaries by assignment, with each dictionary containing the metabolite name and intensity values from all samples sharing that"
- [intro] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
