---
name: mass-spectrometry-data-quality-assessment
description: Use when when raw mass spectrometry spectral data has been imported into matchms from common file formats (mzML, mzXML, msp, MGF, JSON) and you need to assess whether metadata fields are correctly normalized, validated against schema requirements, and peaks are appropriately filtered before.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pytest
  - matchms
  - Paramounter
  - XCMS CentWave
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
- doi: 10.1021/acs.analchem.1c04758
  title: ''
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- matchms is a versatile open-source Python package
- make sure the existing tests still work by running ``pytest``
- github.com/HuanLab/Paramounter
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  - build: coll_paramounter_cq
    doi: 10.1021/acs.analchem.1c04758
    title: Paramounter
  dedup_kept_from: coll_matchms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  - 10.1021/acs.analchem.1c04758
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-quality-assessment

## Summary

Assessment of mass spectrometry data quality through systematic metadata cleaning, validation, and peak filtering to ensure data accuracy and integrity before downstream analysis. This skill applies matchms tools to normalize spectrum metadata fields, standardize naming conventions, and remove or flag invalid entries across imported spectral datasets in mzML, mzXML, msp, MGF, or JSON formats.

## When to use

When raw mass spectrometry spectral data has been imported into matchms from common file formats (mzML, mzXML, msp, MGF, JSON) and you need to assess whether metadata fields are correctly normalized, validated against schema requirements, and peaks are appropriately filtered before proceeding to similarity comparisons or statistical analysis.

## When NOT to use

- Input spectra are already pre-processed and validated by an upstream trusted pipeline; performing redundant cleaning may introduce artifacts.
- The analysis requires raw, unfiltered peak data where lossy cleaning operations are not acceptable.
- Metadata schema or cleaning rules are domain-specific and not covered by matchms default validators; custom validation logic must be developed first.

## Inputs

- Raw spectral data in mzML, mzXML, msp, MGF, or JSON format
- Imported spectra objects loaded via matchms import utilities
- Spectrum metadata fields requiring normalization and validation
- Peak intensity and mass-to-charge ratio arrays

## Outputs

- Cleaned spectrum dataset with validated metadata
- Validation report documenting metadata transformations and failures
- Spectra annotated with quality flags or filtered entries
- Standardized spectrum objects conforming to matchms schema

## How to apply

Load imported spectra using matchms import utilities, then systematically apply matchms metadata cleaning tools to normalize field values and standardize naming conventions. Validate cleaned metadata fields against matchms schema requirements to flag or remove invalid entries. Apply basic peak filtering to ensure spectral data integrity. Run pytest on any custom validation logic to verify tests pass. Document all metadata transformations, validation failures, and filtering decisions in a validation report. Output the cleaned spectrum dataset with validated metadata in the original or preferred matchms format, recording which spectra passed or failed validation.

## Related tools

- **matchms** (Provides metadata cleaning, validation, and peak filtering tools; imports and normalizes spectrum data across mzML, mzXML, msp, MGF, and JSON formats) — https://github.com/matchms/matchms
- **Python** (Execution environment for loading spectra and applying matchms cleaning utilities programmatically)
- **pytest** (Framework for running automated tests on custom validation logic to ensure cleaning and filtering rules work as intended)

## Examples

```
from matchms.importing_utils import load_from_msp; from matchms.data_processing import normalize_intensities; spectra = load_from_msp('raw_spectra.msp'); cleaned_spectra = [normalize_intensities(s) for s in spectra]; import pytest; pytest.main(['tests/validation_test.py', '-v'])
```

## Evaluation signals

- All spectrum metadata fields conform to matchms schema requirements with no validation errors or unresolved flags.
- Metadata transformations are documented in the validation report with counts of entries removed, normalized, or flagged per field.
- pytest test suite passes without errors, confirming custom validation logic is correct.
- Peak filtering reduces noise or invalid peaks while preserving expected spectral features (compare peak counts before/after filtering).
- Output spectrum dataset is readable by downstream matchms operations (e.g., similarity scoring) without import or schema errors.

## Limitations

- Matchms metadata cleaning applies general normalization rules; domain-specific validation rules must be implemented as custom pytest logic.
- Basic peak filtering may not be optimal for all mass spectrometry modalities; additional filtering parameters may need tuning per dataset.
- The validation report documents failures but does not automatically resolve them; human review is needed to decide whether to remove or attempt recovery of invalid spectra.
- Metadata schema requirements are defined by matchms; schemas not explicitly supported by matchms may require custom extensions.

## Evidence

- [intro] Matchms provides an array of tools for metadata cleaning and validation alongside basic peak filtering to ensure data accuracy and integrity of imported spectra.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [other] The workflow applies cleaning and validation steps to normalize and standardize metadata after import, then validates against schema before output.: "Apply matchms metadata cleaning tools to normalize field values, standardize naming conventions, and remove or flag invalid entries. 3. Validate cleaned metadata fields against matchms schema"
- [other] Imported spectra from matchms-compatible formats must be cleaned, validated, and tested before output as a standardized dataset.: "Load imported spectra from matchms-compatible format (mzML, mzXML, msp, MGF, or JSON) using Python and matchms import utilities. 2. Apply matchms metadata cleaning tools to normalize field values,"
- [readme] The software supports mzML, mzXML, msp, metabolomics-USI, MGF, and JSON formats for spectral data.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] Test validation logic using pytest to verify existing tests pass before documenting transformations in a validation report.: "Run pytest on custom validation logic to verify existing tests pass. 5. Document any metadata transformations and validation failures in a validation report."
