---
name: metadata-field-normalization
description: Use when immediately after importing raw mass spectrometry data from
  mzML, mzXML, msp, MGF, or JSON formats into matchms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pytest
  - matchms
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing,
  cleaning, and comparing mass spectrometry data
- matchms is a versatile open-source Python package
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_2_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
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

# metadata-field-normalization

## Summary

Normalize and standardize metadata field values in mass spectrometry spectral data after import to ensure consistent naming conventions, remove or flag invalid entries, and comply with matchms schema requirements. This prepares cleaned metadata for validation and downstream spectral comparison workflows.

## When to use

Apply this skill immediately after importing raw mass spectrometry data from mzML, mzXML, msp, MGF, or JSON formats into matchms. Use it when spectrum metadata fields contain inconsistent naming conventions, non-standard value representations, or entries that deviate from the expected matchms schema structure.

## When NOT to use

- Spectra already imported and validated by a certified matchms pipeline—re-normalizing clean data risks introducing inconsistencies.
- Raw peak intensity lists without accompanying metadata—this skill addresses field normalization, not spectral peak filtering or intensity calibration.
- When the goal is only to compare spectral similarity without requiring schema-validated metadata—though cleaning is recommended for reproducibility.

## Inputs

- Raw spectral data in mzML, mzXML, msp, MGF, or JSON format
- Imported spectra objects via matchms import utilities
- Metadata field definitions and schema specifications (implicit in matchms library)

## Outputs

- Normalized spectrum metadata with standardized field values and naming conventions
- Cleaned spectrum dataset with validated metadata conforming to matchms schema
- Validation report documenting metadata transformations and any flagged or invalid entries
- Optionally, spectra re-exported in original or preferred matchms format

## How to apply

Load imported spectra using matchms import utilities (e.g., from_mzml, from_json). Apply matchms metadata cleaning tools to normalize field values across all spectrum records—standardizing naming conventions to align with the matchms schema (e.g., consistent case, units, delimiter formats). Identify and either remove invalid entries or flag them for manual review. After normalization, validate the cleaned metadata fields against matchms schema requirements to ensure all records conform to expected data types and structure. Run pytest on any custom validation logic to verify that existing tests pass before outputting the cleaned dataset.

## Related tools

- **matchms** (Provides metadata cleaning and validation functions, schema definitions, and import/export utilities for normalized spectrum data) — https://github.com/matchms/matchms
- **pytest** (Runs test suites to verify that custom validation logic and existing tests pass after metadata normalization)
- **Python** (Core language for scripting metadata normalization workflows and invoking matchms APIs)

## Examples

```
from matchms import importing; spectra = list(importing.load_from_msp('raw_spectra.msp')); from matchms.cleaning import normalize_metadata; spectra = [normalize_metadata(s) for s in spectra]; import pytest; pytest.main(['-v', 'test_metadata_validation.py'])
```

## Evaluation signals

- All spectrum metadata field values conform to matchms schema data types and naming conventions (verified by schema validation pass).
- No spectrum records contain invalid, missing, or inconsistent field entries after cleaning (verified by validation report with zero flagged entries or by manual spot-check of output).
- pytest test suite passes without errors or warnings, confirming backward compatibility and correctness of custom validation logic.
- Metadata transformations are documented in the validation report, showing the number of records modified, fields normalized, and any entries removed or flagged.
- Re-imported cleaned spectra retain their normalized metadata structure when exported and re-imported in the same or alternative matchms format.

## Limitations

- matchms metadata cleaning tools are optimized for standard MS/MS fields (e.g., precursor_mz, retention_time, compound_name); custom or domain-specific metadata fields may require manual schema extension.
- Normalization does not infer missing metadata from raw spectral data—invalid or absent fields are flagged but not reconstructed; external reference databases may be needed for enrichment.
- The skill assumes import was successful and spectra are already in matchms Spectrum object format; import errors or malformed source files must be resolved upstream.
- Validation against the matchms schema does not guarantee scientific accuracy of metadata values (e.g., a normalized mass value may still be incorrect); domain expertise is required to judge value plausibility.

## Evidence

- [other] Apply matchms metadata cleaning tools to normalize field values, standardize naming conventions, and remove or flag invalid entries.: "Apply matchms metadata cleaning tools to normalize field values, standardize naming conventions, and remove or flag invalid entries."
- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity."
- [other] Validate cleaned metadata fields against matchms schema requirements to ensure data accuracy and integrity.: "Validate cleaned metadata fields against matchms schema requirements to ensure data accuracy and integrity."
- [other] Load imported spectra from matchms-compatible format (mzML, mzXML, msp, MGF, or JSON) using Python and matchms import utilities.: "Load imported spectra from matchms-compatible format (mzML, mzXML, msp, MGF, or JSON) using Python and matchms import utilities."
- [other] Document any metadata transformations and validation failures in a validation report.: "Document any metadata transformations and validation failures in a validation report."
