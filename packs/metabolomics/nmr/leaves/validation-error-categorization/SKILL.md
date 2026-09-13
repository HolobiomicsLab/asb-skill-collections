---
name: validation-error-categorization
description: Use when when a parsed mwTab file (MS or NMR experimental data) must
  be assessed for conformance to its corresponding JSON schema specification. Apply
  this skill after loading the mwTab file using the mwtab parser but before quality
  assurance sign-off or deposition to the Metabolomics Workbench.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3364
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - jsonschema
  - Python
  - mwtab
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo11030163
  title: mwtab Python Library for RESTful Access
evidence_spans:
- jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema
- The ``mwtab`` package is a Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwtab_python_library_for_restful_access_cq
    doi: 10.3390/metabo11030163
    title: mwtab Python Library for RESTful Access
  dedup_kept_from: coll_mwtab_python_library_for_restful_access_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11030163
  all_source_dois:
  - 10.3390/metabo11030163
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# validation-error-categorization

## Summary

Systematically collect, categorize, and report schema validation violations detected in mwTab files by applying jsonschema validation rules and metadata column matching against MS/NMR schema specifications. This skill produces structured validation reports that distinguish structural errors, content violations, and metadata inconsistencies to guide remediation.

## When to use

When a parsed mwTab file (MS or NMR experimental data) must be assessed for conformance to its corresponding JSON schema specification. Apply this skill after loading the mwTab file using the mwtab parser but before quality assurance sign-off or deposition to the Metabolomics Workbench. Use it when you need to report not just pass/fail status but also enumerate and classify the specific violations and violations by type (structural vs. metadata column format).

## When NOT to use

- Input file is not yet parsed; validation only works on mwtab.MWTabFile objects, not raw mwTab text files.
- JSON schema definitions (ms_schema or nmr_schema) are not available or match the mwTab file format version in use.
- The goal is to convert mwTab to JSON or vice versa; use format conversion workflows instead.

## Inputs

- parsed mwTab file object (mwtab.MWTabFile instance)
- JSON schema definition (ms_schema or nmr_schema)
- metadata_column_matching rules (NameMatcher and ValueMatcher specifications)

## Outputs

- structured validation report (categorized errors and warnings)
- pass/fail status per validation category
- violation details with remediation recommendations
- metadata column validation results

## How to apply

After loading the mwTab file with mwtab.MWTabFile parser, extract the study's experiment type (MS or NMR) to select the appropriate JSON schema (ms_schema or nmr_schema parameters). Apply jsonschema validation of the parsed mwTab data against the selected schema with verbose reporting enabled by default. Concurrently apply metadata_column_matching rules to validate standard column names and value formats in metadata sections. Aggregate all validation errors, warnings, and metadata column violations into separate categories. Generate and return a structured report documenting pass/fail status for each category, detailed violation descriptions, and recommendations for correction.

## Related tools

- **mwtab** (Parse and load mwTab files into MWTabFile objects and provide schema-based validation framework) — https://github.com/MoseleyBioinformaticsLab/mwtab
- **jsonschema** (Validate mwTab file content against MS and NMR JSON schema definitions and report violations)
- **Python** (Runtime environment for executing mwtab and jsonschema validation logic)

## Examples

```
from mwtab import MWTabFile; import jsonschema; mwfile = MWTabFile.from_file('study_001_analysis_123.txt'); schema = ms_schema if mwfile.study_type == 'MS' else nmr_schema; errors = list(jsonschema.Draft7Validator(schema).iter_errors(mwfile.to_dict())); print(f'Validation: {len(errors)} error(s) found')
```

## Evaluation signals

- All detected schema violations are recorded and categorized (structural errors vs. metadata column violations); no violations are silently dropped.
- Pass/fail status correctly reflects whether all validation rules passed (no violations) or at least one rule failed.
- Metadata column validation matches column names and value formats against metadata_column_matching rules (NameMatcher.dict_match and ValueMatcher.series_match).
- Violation details include sufficient context (field path, expected schema constraint, observed value) to enable practitioner remediation.
- Report structure is consistent across runs and experiment types (MS vs. NMR), enabling automated ingestion by downstream QC workflows.

## Limitations

- Validation accuracy depends on the completeness and correctness of the JSON schema definitions (ms_schema, nmr_schema); schema version mismatches will produce spurious violations or false negatives.
- The mwtab library's validation is schema-based and does not detect domain-specific metabolomics errors (e.g., biologically implausible m/z ranges or NMR field strengths) that fall outside JSON schema scope.
- Metadata column validation relies on predefined NameMatcher and ValueMatcher rules; non-standard or novel metadata columns will not be validated unless rules are extended.

## Evidence

- [other] Apply jsonschema validation to the parsed mwTab data against the appropriate schema based on experiment type, with verbose reporting enabled by default.: "Apply jsonschema validation to the parsed mwTab data against the appropriate schema based on experiment type, with verbose reporting enabled by default."
- [other] Collect and categorize all validation errors, warnings, and metadata column validation results (via metadata_column_matching rules for standard column names and value formats).: "Collect and categorize all validation errors, warnings, and metadata column validation results (via metadata_column_matching rules for standard column names and value formats)."
- [other] jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema.: "jsonschema_ for validating functionality of ``mwTab`` files based on ``JSON`` schema."
- [other] Generate and return a structured validation report documenting pass/fail status, violation details, and recommendations.: "Generate and return a structured validation report documenting pass/fail status, violation details, and recommendations."
- [readme] The ``mwtab`` package is a Python library that facilitates reading and writing files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear Magnetic Resonance (NMR) experimental data.: "files in ``mwTab`` format used by the `Metabolomics Workbench`_ for archival of Mass Spectrometry (MS) and Nuclear Magnetic Resonance (NMR) experimental data"
