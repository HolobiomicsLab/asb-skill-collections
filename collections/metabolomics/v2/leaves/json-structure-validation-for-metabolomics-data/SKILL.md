---
name: json-structure-validation-for-metabolomics-data
description: Use when after serializing empirical compound collections to JSON format
  via khipu's build_empCpds command, or before ingesting empCpd.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0336
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - ThermoRawFileParser
  - khipu
  - Python
  - metDataModel
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- pre-annotation to group featues to empirical compounds (khipu)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# JSON Structure Validation for Metabolomics Data

## Summary

Validate the structural integrity and completeness of empirical compound JSON files produced by khipu's build_empCpds command, ensuring all required fields (list_of_features, median m/z, median rt, pre-annotation) are present and properly formatted before downstream annotation or statistical analysis.

## When to use

After serializing empirical compound collections to JSON format via khipu's build_empCpds command, or before ingesting empCpd.json files into MS1 annotation, MS2 matching, or statistical workflows to detect schema drift, missing fields, or malformed records that could cause downstream failures.

## When NOT to use

- Input is not yet serialized to JSON (e.g., empirical compounds are still in-memory Python objects or intermediate formats)
- The downstream tool natively handles schema validation and repair (check tool documentation first)
- You are validating a different data model (e.g., MS2 spectral library JSON, sample metadata JSON) — use tool-specific validators instead

## Inputs

- empCpd.json file (output from khipu build_empCpds command)
- Feature table TSV (asari preferred_Feature_table.tsv, for row count cross-check)

## Outputs

- Validation report (pass/fail, schema conformance summary)
- Error log (records with missing/malformed fields, if any)
- Summary statistics (count of empirical compounds, median m/z range, median rt range)

## How to apply

Load the empCpd.json file and verify that each empirical compound record contains the required fields: list_of_features (array of feature identifiers), median m/z (numeric, typically 100–1000 Da range), median rt (numeric, in seconds), and pre-annotation (string or null). Confirm that list_of_features is non-empty (grouped features, not singletons unless configured otherwise), that m/z and rt values are numeric and within expected instrument ranges, and that the JSON is valid UTF-8 and parses without syntax errors. Validate counts: the total number of grouped features across all records should match or be less than the input feature table row count (accounting for ungrouped singletons). Report any records with missing fields, null values in mandatory positions, or type mismatches, and log the count of valid vs. invalid records.

## Related tools

- **khipu** (Constructs empirical compound groups and serializes to JSON; validation confirms correctness of serialization output) — https://github.com/shuzhao-li-lab/khipu
- **metDataModel** (Defines standardized data model schemas for metabolomics JSON structures, including empirical compound JSON schema) — https://github.com/shuzhao-li-lab/metDataModel
- **Python** (Language for writing validation scripts (json module, schema validators))

## Examples

```
python -c "import json; data = json.load(open('empCpd.json')); assert isinstance(data, list); records = sum(1 for rec in data if all(k in rec for k in ['list_of_features', 'median_mz', 'median_rt', 'pre_annotation'])); print(f'Valid records: {records}/{len(data)}')"
```

## Evaluation signals

- JSON parses without syntax errors (valid UTF-8, well-formed key–value pairs)
- Every empirical compound record contains all required fields: list_of_features, median_mz, median_rt, pre_annotation
- list_of_features is a non-empty array of feature identifiers; median_mz and median_rt are numeric values within plausible ranges (e.g., m/z > 0, rt > 0)
- Sum of feature counts across all empirical compounds equals or is less than input feature table row count
- No null values in mandatory fields; pre_annotation may be null or empty string if no prior assignment

## Limitations

- Validation checks structural conformance only; does not verify chemical correctness or whether grouped features are truly related isotopes/adducts
- Does not detect semantic errors (e.g., features grouped with implausible m/z or rt differences relative to khipu tolerance parameters)
- Khipu's output may vary if mz tolerance (default 5 ppm) and rt tolerance (default 2 seconds) parameters differ; validation does not account for parameter choices
- Validation assumes UTF-8 encoding; files with other encodings will fail to parse

## Evidence

- [other] Serialize the empirical compound collection to JSON format, including list_of_features, median m/z, median rt, and pre-annotation fields for each group.: "Serialize the empirical compound collection to JSON format, including list_of_features, median m/z, median rt, and pre-annotation fields for each group."
- [other] Validate JSON structure and confirm all required fields are present.: "Validate JSON structure and confirm all required fields are present."
- [other] The build_empCpds command groups features into empirical compounds by matching isotopes and adducts with configurable mz tolerance (default 5 ppm) and rt tolerance (default 2 seconds), producing a JSON file containing grouped features with their mz and rt values.: "The build_empCpds command groups features into empirical compounds by matching isotopes and adducts with configurable mz tolerance (default 5 ppm) and rt tolerance (default 2 seconds), producing a"
- [readme] empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards: "empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards"
