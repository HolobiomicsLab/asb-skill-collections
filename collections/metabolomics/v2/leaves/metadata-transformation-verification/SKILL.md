---
name: metadata-transformation-verification
description: Use when you have extracted raw tabular metadata into JSON form using
  the MESSES extract command and need to confirm the extraction is accurate before
  conversion to a repository-specific format. Specifically, use it when the conversion
  target format has strict schema requirements (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3377
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - MESSES
  - jsonschema
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

# metadata-transformation-verification

## Summary

Verify that tabular experimental metadata has been correctly extracted into an intermediate JSON representation and transformed to a target format (e.g., mwTab) by validating against schema constraints and comparing output against expected canonical results. This skill ensures data integrity across the extract–validate–convert pipeline used in metabolomics data deposition workflows.

## When to use

Apply this skill when you have extracted raw tabular metadata into JSON form using the MESSES extract command and need to confirm the extraction is accurate before conversion to a repository-specific format. Specifically, use it when the conversion target format has strict schema requirements (e.g., mwTab for Metabolomics Workbench submission) or when you are developing or testing a tagging scheme and need to verify that filtering, sorting, and concatenation directives (such as for_each with test, sort_by, and delimiter parameters) produce the expected canonical output strings.

## When NOT to use

- Input is already in a validated, repository-accepted format (e.g., mwTab already submitted to Metabolomics Workbench) — validation is redundant.
- Tabular source data has not yet been tagged or extracted to JSON — first run the extract command with appropriate tagging before validation.
- You have no schema documentation or reference output specification available — validation requires explicit schema constraints or known-good examples to compare against.

## Inputs

- Extracted JSON representation of tabular metadata (output from messes extract)
- Protocol Dependent Schema (PDS) JSON or JSON Schema file
- Format-specific schema (e.g., mwTab schema for Metabolomics Workbench)
- Experiment Description Specification constraints
- Expected reference output string or reference JSON for comparison

## Outputs

- Validation report indicating pass/fail status and listing schema violations, type errors, or missing required fields
- Verified JSON metadata ready for conversion to target format
- Corrected or flagged records requiring manual review or data source correction

## How to apply

Run the MESSES validate command against the extracted JSON, supplying both the Protocol Dependent Schema (PDS) specific to your experimental design and a format-specific schema for your target output format. The validator will check conformance against the Experiment Description Specification, your PDS constraints, and built-in format schemas. For directive-based transformations (e.g., str directive with for_each=True), verify the output by: (1) loading the documented example input JSON, (2) applying the directive engine with specified filter conditions (test parameter), sorting rules (sort_by and sort_order), and delimiter, (3) comparing the concatenated result string against the expected canonical output from documentation or reference implementations. Use JSON Schema validation and custom schema checks to catch mismatches in field names, value types, and required fields before proceeding to the convert step.

## Related tools

- **MESSES** (Extract, validate, and convert tabular metadata through its three-stage pipeline; provides the validate command used in this skill and the directive engine for filtering and concatenation) — https://github.com/MoseleyBioinformaticsLab/messes
- **jsonschema** (Underlying JSON Schema validation engine used by MESSES to check extracted JSON against PDS and format-specific schemas) — https://pypi.org/project/jsonschema/

## Examples

```
messes validate json your_data.json --pds your_schema.json --format desired_format
```

## Evaluation signals

- Validation report returns zero schema errors (all required fields present, all values match specified types and patterns)
- Concatenated output string from directive engine (e.g., SAMPLEPREP_SUMMARY) exactly matches the expected reference string character-for-character
- All filtered records (e.g., test='type=sample_prep') are correctly identified and sorted by the specified field (e.g., 'id') in the declared order (ascending/descending)
- No warnings for missing optional fields or ambiguous field names in the generated JSON
- Converted output (after passing validation) successfully imports or ingests into the target repository system without rejection

## Limitations

- Validation relies on having a complete and accurate PDS and format-specific schema; if the schema itself is incomplete or incorrect, validation may pass invalid data or reject valid data.
- Directive-based transformations (e.g., str directive with for_each) require careful specification of test, sort_by, sort_order, and delimiter parameters; errors in these parameters will produce incorrect output that may still pass structural validation.
- Manual tagging of tabular data can introduce human errors; automated tagging features reduce errors but may not catch all anomalies without human review.
- The validate command can identify structural and schema conformance issues but cannot verify semantic correctness (e.g., whether a sample ID actually refers to the intended biological sample).

## Evidence

- [readme] The extraction step adds a layer of tags to your raw tabular data, which may be automatable, and then extracts it into a JSONized form that it is more interoperable and more standardized. The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide, and a built in schema specific for the format you wish to convert to.: "The validation step ensures the data that was extracted is valid against the Experiment Description Specification, the Protocol Dependent Schema, any additional JSON schema you wish to provide, and a"
- [other] The for_each directive with test='type=sample_prep', sort_by=['id'], sort_order='ascending', and delimiter=' ' produces a SAMPLEPREP_SUMMARY concatenating six sample preparation descriptions: tissue quenching, tissue grinding, IC-FTMS preparation, acetone extraction, lipid extraction, and polar extraction.: "The for_each directive with test='type=sample_prep', sort_by=['id'], sort_order='ascending', and delimiter=' ' produces a SAMPLEPREP_SUMMARY concatenating six sample preparation descriptions"
- [other] 1. Load the documented example input JSON containing the protocol table. 2. Parse the protocol table entries and filter records matching test='type=sample_prep' using the str directive engine. 3. Sort filtered records by 'id' field in ascending order. 4. Concatenate the sorted records' values using the delimiter ' ' (space) to produce the SAMPLEPREP_SUMMARY string. 5. Verify the generated string matches the expected output shown in the For Each section of the documentation.: "Verify the generated string matches the expected output shown in the For Each section of the documentation."
- [intro] To support the JSON-to-JSON conversion a relatively simple set of directives were developed: "To support the JSON-to-JSON conversion a relatively simple set of directives were developed"
- [intro] The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format: "The convert command is used to convert extracted and validated data from it's intermediate JSON form to the final desired format"
