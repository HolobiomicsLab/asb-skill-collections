---
name: spectrum-metadata-validation
description: Use when after importing raw mass spectrometry data from mzML, mzXML, msp, MGF, or JSON formats using matchms, when you need to ensure that metadata fields (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pytest
  - matchms
  - poetry
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
---

# spectrum-metadata-validation

## Summary

Validate and normalize mass spectrometry spectrum metadata fields against schema requirements to ensure data accuracy and integrity after importing raw spectral data. This skill applies matchms metadata cleaning and validation tools to normalize field values, standardize naming conventions, and flag or remove invalid entries before downstream analysis.

## When to use

After importing raw mass spectrometry data from mzML, mzXML, msp, MGF, or JSON formats using matchms, when you need to ensure that metadata fields (e.g., precursor m/z, compound name, ionization mode) conform to expected schema requirements and are free of inconsistencies, missing values, or malformed entries that could corrupt similarity comparisons or library searches.

## When NOT to use

- Spectra that have already undergone metadata validation and cleaning in an upstream pipeline—re-validating may introduce redundant computation.
- Use cases where raw, unvalidated metadata must be preserved exactly as recorded for audit or regulatory compliance (prefer data flagging over transformation).
- When metadata is intentionally sparse or schema-agnostic (e.g., exploratory mass spectrometry studies with heterogeneous instrument outputs).

## Inputs

- Raw mass spectrometry spectra in mzML, mzXML, msp, MGF, or JSON format
- Imported Spectrum objects with unvalidated metadata fields
- Schema specification or validation rules for expected metadata structure

## Outputs

- Validated and normalized Spectrum objects with cleaned metadata
- Cleaned spectrum dataset in original or preferred matchms format
- Validation report documenting metadata transformations and failures

## How to apply

Load imported spectra using matchms import utilities, then apply matchms metadata cleaning functions to normalize field values and standardize naming conventions across the dataset. Next, validate cleaned metadata fields against matchms schema requirements using the library's validation logic. Run pytest on any custom validation code to confirm that existing tests pass and validation logic is sound. Document all metadata transformations, null values, and validation failures in a structured validation report. Finally, output the cleaned spectrum dataset with validated metadata in the original or preferred matchms format (mzML, mzXML, msp, MGF, or JSON), ensuring data integrity for downstream spectral similarity measures and comparisons.

## Related tools

- **matchms** (Primary library providing metadata cleaning functions, validation schema, and import utilities for mass spectrometry data) — https://github.com/matchms/matchms
- **pytest** (Testing framework for verifying that custom validation logic and existing tests pass)
- **poetry** (Dependency and version management for matchms development and contribution workflows)

## Examples

```
from matchms.importing_utils import load_from_mgf; from matchms import Spectrum; spectra = load_from_mgf('raw_spectra.mgf'); import pytest; pytest.main(['-v', 'test_metadata_validation.py'])
```

## Evaluation signals

- All spectrum metadata fields conform to matchms schema requirements with no schema violations reported
- Pytest test suite runs without errors and all existing validation tests pass
- Validation report shows zero or documented number of invalid entries (e.g., null precursor m/z, malformed compound names, out-of-range retention times)
- Metadata normalization is traceable: field transformations and flagged entries are recorded in the validation report
- Output spectra retain or improve data integrity when used in downstream spectral similarity computations (e.g., no crashes or unexpected null scores due to malformed metadata)

## Limitations

- Metadata validation is schema-dependent; if the schema is incomplete or does not match the user's data model, valid spectra may be incorrectly flagged or rejected.
- Normalization and transformation of metadata values (e.g., standardizing compound name capitalization or ionization mode labels) may discard or alter original provenance information if not carefully logged.
- Sparse or highly heterogeneous metadata across large spectral libraries may require custom validation rules beyond matchms' built-in tools, requiring extension via custom code.
- Validation performance may degrade on very large spectral libraries (hundreds of thousands of spectra) if schema checks are computationally expensive.

## Evidence

- [other] matchms provides metadata cleaning and validation tools: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [readme] Supported spectral data formats: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] Workflow includes schema validation after cleaning: "Validate cleaned metadata fields against matchms schema requirements to ensure data accuracy and integrity"
- [other] pytest is used to verify validation logic: "Run pytest on custom validation logic to verify existing tests pass"
- [other] Documentation and reporting of transformations: "Document any metadata transformations and validation failures in a validation report"
