---
name: spectral-data-import-and-parsing
description: Use when you have raw mass spectrometry data in one or more supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, or JSON) and need to convert it into a standardized in-memory representation that can be processed, validated, and compared using matchms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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
---

# spectral-data-import-and-parsing

## Summary

Import and parse raw mass spectrometry spectral data from multiple file formats (mzML, mzXML, msp, MGF, JSON) into a unified matchms spectrum object representation. This is the essential first step before any downstream processing, cleaning, or similarity scoring workflows.

## When to use

You have raw mass spectrometry data in one or more supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, or JSON) and need to convert it into a standardized in-memory representation that can be processed, validated, and compared using matchms. This skill is required whenever beginning a new matchms workflow.

## When NOT to use

- Your input data is already in matchms Spectrum object format (e.g., cached or pickled from a prior import).
- Your data is in an unsupported format not listed above — first convert to MGF, mzML, msp, or JSON.
- You need to compare spectral similarity across sources without first cleaning or filtering — parse data, but plan to apply basic peak filtering and metadata validation before similarity scoring.

## Inputs

- mzML spectral data file
- mzXML spectral data file
- msp (NIST MS Search) spectral data file
- MGF (Mascot Generic Format) spectral data file
- JSON spectral data file
- metabolomics-USI spectral reference

## Outputs

- matchms Spectrum object collection (in-memory list or iterator)
- parsed peak lists with m/z and intensity pairs
- validated spectrum metadata (compound name, molecular weight, precursor m/z, etc.)

## How to apply

Use matchms import utilities to load spectral data from your input file format into spectrum objects. The import process automatically parses mass-to-charge ratio (m/z) and intensity peak data, as well as associated metadata fields. After import, verify data integrity by checking that peak lists are non-empty and metadata fields are populated. This establishes a reproducible baseline before applying any filtering, normalization, or similarity scoring steps downstream. The structured spectrum objects enable consistent handling of heterogeneous data sources in downstream analyses.

## Related tools

- **matchms** (Python package providing import utilities and Spectrum object model for parsing and standardizing spectral data across multiple file formats) — https://github.com/matchms/matchms
- **pytest** (Testing framework for validating that parsed data meets schema and integrity expectations) — https://github.com/pytest-dev/pytest

## Examples

```
from matchms import importing; spectra = list(importing.load_from_mgf('data/spectra.mgf'))
```

## Evaluation signals

- All input files are successfully parsed without IOError or format mismatch exceptions.
- Each imported Spectrum object contains non-empty peaks (m/z and intensity arrays of equal length) and populated metadata fields (e.g., precursor_mz, compound_name).
- Row count of imported spectra matches the expected number from source file metadata (e.g., SCAN lines in mzML, COUNT field in msp).
- Peak m/z values are strictly increasing within each spectrum; intensities are non-negative.
- Metadata fields are consistent with the source file schema (no truncation, encoding errors, or missing critical fields).

## Limitations

- Import supports only the listed file formats; other mass spectrometry formats (e.g., raw Bruker .d, Waters .raw) require external conversion tools.
- Large spectral datasets (several hundred thousand spectra) may require significant memory; consider streaming import or batch processing.
- Metadata extraction depends on the completeness of the source file; missing fields (e.g., SMILES, InChI) in input files will result in empty metadata in the Spectrum object.
- Some file formats (e.g., MGF) store minimal metadata; matchms import cannot infer missing data fields — downstream metadata cleaning steps may be needed.

## Evidence

- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [readme] Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data.: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS)"
- [readme] It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data.: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [other] Load spectral data from supported formats (mzML, mzXML, msp, MGF, JSON) using matchms import utilities.: "Load spectral data from supported formats (mzML, mzXML, msp, MGF, JSON) using matchms import utilities"
- [intro] Importing mass spectrometry data is a key workflow step before processing and cleaning.: "importing, processing, cleaning, and comparing mass spectrometry data (MS/MS)"
