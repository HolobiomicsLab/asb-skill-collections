---
name: data-integrity-verification
description: Use when after applying matchms metadata cleaning tools to normalize field values and standardize naming conventions on imported spectra (mzML, mzXML, msp, MGF, or JSON formats).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pytest
  - matchms
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- matchms is a versatile open-source Python package
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-integrity-verification

## Summary

Validate cleaned mass spectrometry metadata against matchms schema requirements and test custom validation logic to ensure spectral dataset accuracy and integrity. This skill confirms that normalized metadata fields conform to expected types, ranges, and naming conventions before downstream analysis.

## When to use

After applying matchms metadata cleaning tools to normalize field values and standardize naming conventions on imported spectra (mzML, mzXML, msp, MGF, or JSON formats). Use this skill when you need formal verification that metadata transformations have not introduced errors and that all required fields meet matchms schema specifications before proceeding to similarity comparisons or publication.

## When NOT to use

- Input spectral data has not yet been cleaned or imported into matchms format
- No custom validation logic or schema requirements have been defined for your metadata fields
- Validation is intended only as ad hoc spot-checking rather than systematic, repeatable verification

## Inputs

- cleaned spectrum dataset with normalized metadata (mzML, mzXML, msp, MGF, or JSON format)
- matchms schema specification or validation rules
- custom validation test suite (pytest)

## Outputs

- validated spectrum dataset with metadata conforming to matchms schema
- validation report documenting transformations, failures, and schema violations
- pytest pass/fail log confirming regression testing

## How to apply

Load the cleaned spectrum dataset and systematically validate each metadata field against matchms schema requirements using built-in or custom validation logic. Run pytest on custom validation functions to verify that existing test suites pass and that no regressions have occurred. Document all validation failures and metadata transformations in a structured validation report, noting which spectra passed or failed and the specific schema violations encountered. This ensures reproducibility and traceability of the cleaning process.

## Related tools

- **matchms** (provides metadata cleaning tools, schema validation framework, and spectrum import/export utilities for normalized spectral data) — https://github.com/matchms/matchms
- **pytest** (executes unit and integration tests on custom validation logic to verify existing tests pass and confirm data integrity)
- **Python** (language for implementing custom validation functions and orchestrating schema verification workflows)

## Examples

```
from matchms import Spectrum; import pytest; spectra = [load cleaned spectra]; [assert spectrum.metadata.get('mz') is not None for spectrum in spectra]; pytest.main(['-v', 'test_metadata_validation.py'])
```

## Evaluation signals

- All metadata fields conform to matchms schema type and range specifications with no violations reported
- pytest test suite executes successfully with 100% pass rate on validation logic
- Validation report systematically enumerates metadata transformations applied and any spectra that failed validation with specific schema violation reasons
- Spot-check of validated metadata shows consistent normalization (e.g., standardized field names, no orphaned or malformed entries)
- Validated spectrum dataset can be successfully re-exported to original or alternate matchms format without schema errors

## Limitations

- Validation accuracy depends on completeness and correctness of the schema specification; incomplete schemas may miss real data quality issues
- Custom validation logic must be manually implemented per project; matchms provides the framework but not project-specific rules
- Large spectral datasets may require batched or parallelized validation to avoid memory or performance bottlenecks
- Validation can confirm structural conformance but cannot detect all logical or semantic inconsistencies in metadata (e.g., biologically impossible compound masses)

## Evidence

- [other] Validate cleaned metadata fields against matchms schema requirements to ensure data accuracy and integrity: "Validate cleaned metadata fields against matchms schema requirements to ensure data accuracy and integrity."
- [other] Apply matchms metadata cleaning tools to normalize field values, standardize naming conventions, and remove or flag invalid entries: "Apply matchms metadata cleaning tools to normalize field values, standardize naming conventions, and remove or flag invalid entries."
- [other] Run pytest on custom validation logic to verify existing tests pass: "Run pytest on custom validation logic to verify existing tests pass."
- [other] Document any metadata transformations and validation failures in a validation report: "Document any metadata transformations and validation failures in a validation report."
- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity."
- [other] make sure the existing tests still work by running ``pytest``: "make sure the existing tests still work by running ``pytest``"
