---
name: unit-test-design-for-file-parsing
description: Use when when implementing or extending file format parsers in a spectral data pipeline, you need unit tests to ensure that format-specific parsers correctly instantiate spectrum objects with expected m/z arrays, intensity arrays, and metadata attributes before releasing to users or integrating.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
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

# unit-test-design-for-file-parsing

## Summary

Design and implement pytest-based unit tests to verify that file parsers correctly extract spectral peaks, metadata, and intensity values from raw mass spectrometry data files in multiple formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI), and that parsed spectra are compatible with downstream processing workflows.

## When to use

When implementing or extending file format parsers in a spectral data pipeline, you need unit tests to ensure that format-specific parsers correctly instantiate spectrum objects with expected m/z arrays, intensity arrays, and metadata attributes before releasing to users or integrating into production data workflows.

## When NOT to use

- The parser is already fully validated in production and you are only performing a routine import with no code changes.
- You are comparing pre-existing spectrum objects and do not need to verify the import step itself.
- The input is already a matchms Spectrum object or pre-processed spectral data, not raw file data.

## Inputs

- raw mass spectrometry data files in one or more supported formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI)
- file path or file handle to raw spectral data
- format-specific parser module or function
- expected schema or data dictionary specification for intermediate parsed data

## Outputs

- pytest test suite with test functions for each file format
- test report indicating pass/fail status for each parser and format
- validated matchms Spectrum objects instantiated from parsed data
- code coverage report for parser implementation

## How to apply

For each supported file format (mzML, mzXML, msp, MGF, JSON, metabolomics-USI), write pytest test cases that (1) load a representative raw file via the format-specific parser, (2) validate that parsed m/z and intensity arrays have correct length, type, and numeric ranges, (3) verify metadata fields are populated and conform to expected schema, (4) instantiate a matchms Spectrum object from the parsed data, and (5) confirm the resulting spectrum object is compatible with downstream similarity comparison and processing functions. Use parametrized pytest fixtures to test multiple files per format, and include edge cases such as empty spectra, missing metadata fields, and malformed entries. Ground assertions in the specific data types and field names that matchms.Spectrum expects.

## Related tools

- **pytest** (Unit testing framework for writing and executing test cases that verify parser correctness and spectrum object instantiation)
- **matchms** (Mass spectrometry data processing library providing Spectrum class, format-specific parsers, and downstream processing functions for validating parser output) — https://github.com/matchms/matchms
- **Python** (Programming language for implementing test cases and format-specific parser logic)

## Examples

```
pytest tests/test_importers.py -v --cov=matchms.importing --cov-report=html
```

## Evaluation signals

- All pytest tests pass with 100% pass rate for each supported file format (mzML, mzXML, msp, MGF, JSON, metabolomics-USI).
- Parsed m/z and intensity arrays have consistent length, non-empty values, and numeric types matching matchms.Spectrum expectations.
- Metadata fields from raw files are correctly extracted and present in the Spectrum object's metadata dictionary with expected keys and value types.
- Instantiated Spectrum objects are compatible with downstream matchms processing workflows (e.g., similarity comparison functions) without errors.
- Code coverage for parser implementation reaches ≥90%, with edge cases (empty spectra, malformed entries, missing fields) explicitly tested.

## Limitations

- Tests are format-specific; adding a new supported file format requires writing new parser code and corresponding test cases.
- Unit tests verify that parsers correctly instantiate Spectrum objects but do not validate scientific accuracy or chemical correctness of imported metadata.
- Edge cases such as extremely large files or corrupted file headers may not be thoroughly covered by standard unit tests; integration tests or stress tests may be required.
- The test suite depends on representative example files for each format; test coverage quality is only as good as the diversity and completeness of those example files.

## Evidence

- [other] Implement format-specific parsers for each file type, each extracting spectral peaks, metadata, and intensity values into intermediate data dictionaries.: "Implement format-specific parsers for each file type, each extracting spectral peaks, metadata, and intensity values into intermediate data dictionaries"
- [other] Write unit tests using pytest to verify that spectra from each format are correctly imported with expected m/z, intensity, and metadata attributes.: "Write unit tests using pytest to verify that spectra from each format are correctly imported with expected m/z, intensity, and metadata attributes"
- [other] Validate that imported spectrum objects are compatible with downstream processing and comparison workflows in matchms.: "Validate that imported spectrum objects are compatible with downstream processing and comparison workflows in matchms"
- [other] make sure the existing tests still work by running ``pytest``: "make sure the existing tests still work by running ``pytest``"
- [readme] transforming raw data from common mass spectra file formats into pre- and post-processed spectral data: "transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
