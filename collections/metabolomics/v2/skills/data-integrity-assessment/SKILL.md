---
name: data-integrity-assessment
description: Use when immediately after importing raw mass spectrometry data from supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) and before performing spectral similarity comparisons or statistical analysis.
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
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-integrity-assessment

## Summary

Systematic validation and cleaning of mass spectrometry metadata and spectral data to ensure accuracy and consistency before downstream analysis. This skill applies matchms tools to normalize spectral metadata fields, filter peaks, and verify data quality across imported MS/MS spectra in diverse formats.

## When to use

Apply this skill immediately after importing raw mass spectrometry data from supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) and before performing spectral similarity comparisons or statistical analysis. Use it when metadata fields are heterogeneous, missing, or non-standardized across imported spectra, or when peak intensity artifacts may compromise downstream scoring.

## When NOT to use

- Input spectra are already preprocessed and validated by upstream pipelines—skip this skill if metadata are already normalized and peak filtering has been applied.
- Analysis goal requires preservation of raw instrumental artifacts for diagnostic or forensic purposes—this skill removes noise that may be scientifically relevant.
- Data are static reference libraries from curated databases (e.g., GNPS, MassBank) where metadata are already harmonized; apply only to newly imported or heterogeneous user-generated spectral data.

## Inputs

- Raw spectra files in mzML, mzXML, msp, metabolomics-USI, MGF, or JSON format
- Unvalidated or heterogeneous spectral metadata (e.g., inconsistent compound names, missing retention times, non-normalized units)
- Peak lists with potential instrumental artifacts or low-intensity noise

## Outputs

- Cleaned and validated spectral data with harmonized metadata fields
- Filtered peak lists with instrumental artifacts removed
- Pytest validation report confirming data quality checks pass

## How to apply

Load raw spectra using matchms import functions that support multiple file formats. Apply matchms metadata cleaning operations to normalize and validate spectral metadata fields—removing duplicates, standardizing field names and units, and filling missing required fields. Run basic peak filtering to remove low-intensity noise or artifacts that could degrade similarity calculations. Execute pytest on the existing validation test suite to verify that cleaned data pass schema and invariant checks. Compare metadata before and after cleaning to confirm that normalization is complete and no data have been lost.

## Related tools

- **matchms** (Core library providing metadata cleaning operations, peak filtering, and validation functions for MS/MS spectra) — https://github.com/matchms/matchms
- **pytest** (Test framework used to verify that existing validation tests pass after cleaning operations)
- **poetry** (Dependency management tool for maintaining reproducible matchms environments during validation workflows)

## Examples

```
from matchms.importing_utils import load_from_msp; from matchms.filtering import default_filters; spectra = load_from_msp('raw_spectra.msp'); cleaned_spectra = [default_filters(s) for s in spectra]; import pytest; pytest.main(['-v', 'tests/test_validation.py'])
```

## Evaluation signals

- All metadata fields conform to a unified schema with consistent naming, units, and encoding (e.g., no mixed case in compound names, all m/z values in same units)
- Pytest validation test suite completes successfully with no schema violations or missing required fields
- Peak lists exhibit reduced noise: low-intensity artifacts below instrument threshold are removed; signal-to-noise ratio improves for downstream similarity scoring
- Metadata before/after comparison shows zero loss of high-quality data while removing only duplicates or malformed entries
- Cleaned spectra can be serialized and deserialized without error, and match expected counts and field cardinality

## Limitations

- Metadata cleaning relies on predefined matchms validators; edge-case or domain-specific metadata fields may not be recognized and could be incorrectly dropped or transformed.
- Basic peak filtering is applied uniformly; instrument-specific or experiment-specific filtering thresholds may not be optimal for all use cases (e.g., low-abundance metabolites in untargeted metabolomics).
- Cleaning operations are lossy for malformed or redundant entries; no recovery mechanism exists if valid data are inadvertently discarded due to overly strict schema constraints.
- Performance may degrade for very large spectral libraries (several hundred thousand spectra); matchms documentation emphasizes sparse data handling for efficiency but does not detail scaling limits for validation.

## Evidence

- [intro] Metadata cleaning and validation operations to ensure data accuracy and integrity: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [intro] Import and loading of supported spectral formats: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [intro] Workflow steps for importing, processing, and cleaning spectral data: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [other] pytest is used to verify validation tests pass: "make sure the existing tests still work by running ``pytest``"
- [other] Metadata normalization is a core step in the workflow: "Apply metadata cleaning operations to normalize and validate spectral metadata fields"
