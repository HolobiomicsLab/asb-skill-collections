---
name: spectral-data-quality-assurance
description: Use when when importing raw mass spectrometry data in formats like mzML,
  mzXML, msp, MGF, or JSON and you need to ensure spectral data quality before proceeding
  to similarity comparisons or other downstream analyses.
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
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing,
  cleaning, and comparing mass spectrometry data
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_2_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  dedup_kept_from: coll_matchms_2_cq
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

# spectral-data-quality-assurance

## Summary

Apply basic peak filtering and metadata validation to mass spectrometry spectral data to ensure data accuracy and integrity during pre-processing. This skill removes noise peaks, normalizes intensities, and validates cleaned peak lists against test suites before downstream analysis.

## When to use

When importing raw mass spectrometry data in formats like mzML, mzXML, msp, MGF, or JSON and you need to ensure spectral data quality before proceeding to similarity comparisons or other downstream analyses. Apply this skill when raw spectra contain low-intensity noise peaks or when metadata requires cleaning and validation.

## When NOT to use

- When spectral data has already been pre-processed and validated by upstream quality control (QC) pipelines
- When the analysis goal does not require peak-level filtering (e.g., metadata-only comparisons)
- When working with vendor-curated reference libraries already guaranteed to meet quality standards

## Inputs

- Raw mass spectrometry spectral data files (mzML, mzXML, msp, MGF, JSON formats)
- Spectral objects with peak lists and metadata
- Existing pytest test suite for validation

## Outputs

- Pre-processed spectral data with filtered peak lists
- Cleaned and validated metadata
- Spectral objects ready for similarity comparisons or further analysis
- Test results confirming filtering logic correctness

## How to apply

Load raw mass spectrometry spectral data using matchms import functionality for supported formats (mzML, mzXML, msp, MGF, JSON). Apply basic peak filtering operations including removal of low-intensity and noise peaks, followed by peak intensity normalization to standardize spectral representations. Perform metadata cleaning and validation in parallel. Validate that filtered peak lists pass the existing pytest test suite to confirm filtering logic correctness. Export pre-processed spectral data with cleaned peak lists in the original or compatible format for use in downstream workflow stages.

## Related tools

- **matchms** (Primary Python package providing peak filtering, metadata cleaning, and validation functionality for mass spectrometry data pre-processing) — https://github.com/matchms/matchms
- **pytest** (Testing framework for validating that filtered peak lists pass existing test suite to confirm filtering logic correctness)

## Examples

```
from matchms.importing_utils import load_from_msp; from matchms.filtering import default_filters; spectra = load_from_msp('raw_data.msp'); spectra = [default_filters(s) for s in spectra]; import pytest; pytest.main(['-v', 'test_filtering.py'])
```

## Evaluation signals

- Filtered peak lists contain no peaks below the configured intensity threshold and noise removal criteria are consistently applied across all spectra
- Peak intensity values are normalized to a consistent scale (e.g., 0–1 or 0–100 range) across all filtered spectra
- All pytest test cases pass without failure, confirming filtering logic is correct and no regressions were introduced
- Metadata fields are populated, validated, and free of inconsistencies (e.g., missing or conflicting values)
- Pre-processed spectral data can be successfully re-imported and re-exported in the same or compatible format without data loss

## Limitations

- Basic peak filtering does not account for instrument-specific artifacts or advanced denoising strategies; domain-specific tuning may be required for specialized analytical methods
- Metadata validation relies on matchms-defined schemas; custom or non-standard metadata fields may not be recognized or validated
- The skill is designed for pre-processing; it does not perform spectral alignment, deconvolution, or other advanced processing steps that may be necessary for certain MS/MS applications

## Evidence

- [readme] Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [other] Apply basic peak filtering operations including peak removal (e.g., low-intensity or noise peaks) and peak intensity normalization to ensure data accuracy and integrity.: "Apply basic peak filtering operations including peak removal (e.g., low-intensity or noise peaks) and peak intensity normalization to ensure data accuracy and integrity"
- [other] Load raw mass spectrometry spectral data in supported formats (mzML, mzXML, msp, MGF, JSON) using matchms import functionality.: "Load raw mass spectrometry spectral data in supported formats (mzML, mzXML, msp, MGF, JSON) using matchms import functionality"
- [other] Validate filtered peak lists pass existing pytest test suite to confirm filtering logic is correct.: "Validate filtered peak lists pass existing pytest test suite to confirm filtering logic is correct"
- [readme] It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
