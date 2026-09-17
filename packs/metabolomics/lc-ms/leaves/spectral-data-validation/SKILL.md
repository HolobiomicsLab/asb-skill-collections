---
name: spectral-data-validation
description: Use when when raw spectra have been imported from common MS/MS file formats
  but contain inconsistent, missing, or malformed metadata fields that could compromise
  spectral similarity comparisons or cause downstream pipeline failures.
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

# spectral-data-validation

## Summary

Apply metadata cleaning and validation operations to imported mass spectrometry spectra to ensure data accuracy and integrity before downstream analysis. This skill normalizes spectral metadata fields and enforces validation constraints across supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON).

## When to use

When raw spectra have been imported from common MS/MS file formats but contain inconsistent, missing, or malformed metadata fields that could compromise spectral similarity comparisons or cause downstream pipeline failures. Apply this skill as the immediate post-import step before processing or comparison workflows.

## When NOT to use

- Spectra are already pre-processed and validated (e.g., from a trusted curated library); validation is redundant.
- Input format is not one of the supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON).
- The workflow goal is exploratory and metadata accuracy is not a constraint (not recommended, but possible).

## Inputs

- raw spectra in mzML, mzXML, msp, metabolomics-USI, MGF, or JSON format
- spectral metadata fields (compound name, precursor m/z, instrument, collision energy, etc.)
- existing pytest validation tests (optional, for baseline regression)

## Outputs

- cleaned and validated spectral data
- harmonized metadata fields
- pytest validation report confirming no regression

## How to apply

Load raw spectra using matchms import functions for the relevant format (mzML, mzXML, msp, metabolomics-USI, MGF, or JSON). Apply matchms metadata cleaning operations to normalize and validate spectral metadata fields—for example, standardizing compound names, resolving missing precursor m/z values, or correcting malformed instrument metadata. Run pytest on the validation suite to verify that existing validation tests pass and that no spectra were inadvertently corrupted. Output the cleaned and validated spectral dataset with harmonized metadata fields ready for downstream processing. The rationale is that consistent, accurate metadata is essential for reliable spectral similarity computations and reproducible workflows.

## Related tools

- **matchms** (Python package that provides metadata cleaning operations, import functions for supported MS/MS formats, and validation infrastructure) — https://github.com/matchms/matchms
- **pytest** (Test framework to verify that validation operations pass existing tests and do not regress)

## Examples

```
from matchms import Spectrum
from matchms.importing import load_from_msp
spectra = load_from_msp('raw_spectra.msp')
cleaned_spectra = [s for s in spectra if s.metadata is not None]
# Run validation suite: pytest tests/test_metadata_validation.py
```

## Evaluation signals

- All spectra successfully round-trip through the cleaning pipeline without data loss or corruption.
- Pytest validation suite passes with no new failures after cleaning is applied.
- Metadata fields are uniform in format and type across all spectra (e.g., precursor m/z is numeric, compound names are strings).
- No spectra are dropped during validation unless explicitly flagged as invalid; retention rate ≥ 95% or as specified by project requirements.
- A diff or comparison of before/after metadata shows only expected normalizations (e.g., whitespace trimming, case standardization, missing-value imputation) with no unintended alterations.

## Limitations

- Validation cannot recover completely missing critical metadata (e.g., precursor m/z for MS/MS spectra); such records may need to be flagged or removed.
- Cleaning operations are format-specific; the behavior and strictness of validation may differ across mzML, mzXML, msp, MGF, and JSON imports.
- Validation relies on predefined schemas and rules; non-standard or proprietary metadata extensions may not be recognized or validated.
- Performance may degrade on very large spectral datasets (hundreds of thousands of spectra); consider batch processing or sampling for preliminary validation.

## Evidence

- [intro] Matchms provides an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity of imported spectra.: "Matchms offers an array of tools for metadata cleaning and validation, alongside basic peak filtering, to ensure data accuracy and integrity"
- [other] Load raw spectra data in supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) using matchms import functions, then apply metadata cleaning operations to normalize and validate spectral metadata fields.: "Load raw spectra data in supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) using matchms import functions. 2. Apply metadata cleaning operations to normalize and validate spectral"
- [other] Run pytest to verify that existing validation tests pass, confirming no regression in the cleaned dataset.: "Run pytest to verify that existing validation tests pass. 4. Output cleaned and validated spectral data with harmonized metadata fields."
- [readme] Matchms facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data.: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [other] Make sure the existing tests still work by running pytest after applying cleaning operations.: "make sure the existing tests still work by running ``pytest``"
