---
name: unit-test-development-for-spectral-loaders
description: Use when when you have implemented parser functions for one or more mass spectrometry file formats and need to verify that metadata and peak lists are correctly extracted and converted into matchms Spectrum objects before committing to a feature branch.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - pytest
  - matchms
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

# unit-test-development-for-spectral-loaders

## Summary

Write and validate pytest unit tests for mass spectrometry spectral file format parsers (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) to ensure correct metadata extraction and Spectrum object construction. This skill ensures parser correctness and prevents regression during development.

## When to use

When you have implemented parser functions for one or more mass spectrometry file formats and need to verify that metadata and peak lists are correctly extracted and converted into matchms Spectrum objects before committing to a feature branch.

## When NOT to use

- You have not yet implemented the parser functions themselves — test development follows implementation.
- Your file format is not among the six supported formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) — use integration testing instead.
- You are testing similarity scoring or spectral comparison logic — use separate similarity measure tests, not file parser tests.

## Inputs

- Parser function implementations for mzML, mzXML, msp, MGF, JSON, metabolomics-USI formats
- Representative sample spectra files in each supported file format
- Spectrum object schema definition

## Outputs

- pytest test suite validating parser correctness
- Test results confirming all parsing tests pass
- Verified Spectrum object instances with correctly extracted metadata and peak lists

## How to apply

Design test cases using pytest that cover representative samples from each supported file format (mzML, mzXML, msp, MGF, JSON, metabolomics-USI). For each parser, create unit tests that validate: (1) correct extraction of spectral metadata fields, (2) accurate peak list parsing into the Spectrum object schema, and (3) absence of data corruption or loss during import. Run `pytest` to confirm all parsing tests pass and that existing tests remain unbroken. Use assertion statements to verify that imported spectra match expected values for key fields (metadata, peak m/z values, intensities). This ensures the parser module is production-ready before code review.

## Related tools

- **pytest** (Framework for writing and executing unit tests to validate parser functions and Spectrum object construction)
- **Python** (Language for implementing parser functions and test code that manipulate Spectrum objects)
- **matchms** (Source package providing Spectrum object schema and parser module under test) — https://github.com/matchms/matchms

## Examples

```
pytest tests/test_spectral_parsers.py -v
```

## Evaluation signals

- All pytest tests pass with zero failures or errors when run on the parser module.
- Existing test suite continues to pass (no regression) after new parser tests are added.
- Assertions in each test confirm that metadata fields (e.g., precursor m/z, collision energy, compound name) are extracted with exact or expected-range values.
- Peak list assertions verify that m/z and intensity arrays in Spectrum objects match the source file values within acceptable numerical precision.
- Test coverage includes at least one representative sample file from each of the six supported formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI).

## Limitations

- Tests validate individual parsers in isolation; cross-format equivalence (e.g., identical spectra loaded from mzML vs. msp) requires integration tests.
- Unit tests do not capture downstream effects of parsing errors on similarity scoring or spectral comparison workflows.
- Numerical precision assertions must account for floating-point representation in each file format; tests may require tolerance thresholds (e.g., ±0.01 m/z).
- Tests assume sample spectra files are available and representative; malformed or edge-case files may not be caught by basic unit tests.

## Evidence

- [other] Implement individual parser functions that extract metadata and peak lists from each format and construct matchms Spectrum objects.: "Implement individual parser functions that extract metadata and peak lists from each format and construct matchms Spectrum objects"
- [other] Write unit tests using pytest to validate correct parsing and Spectrum object construction for representative samples in each format.: "Write unit tests using pytest to validate correct parsing and Spectrum object construction for representative samples in each format"
- [other] Run pytest to ensure all parsing tests pass and existing tests remain unbroken.: "Run pytest to ensure all parsing tests pass and existing tests remain unbroken"
- [other] Matchms supports loading mass spectrometry spectra from six file formats: mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "Matchms supports loading mass spectrometry spectra from six file formats: mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] make sure the existing tests still work by running ``pytest``: "make sure the existing tests still work by running ``pytest``"
