---
name: mass-spectrometry-data-format-import
description: Use when you have raw mass spectrometry data in one of the supported spectral formats (mzML, mzXML, msp, MGF, JSON, or metabolomics-USI) and need to load it into a Python environment for cleaning, processing, or similarity comparison.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - matchms
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
evidence_spans:
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- matchms is a versatile open-source Python package
- A key feature of matchms is its ability to apply various pairwise similarity measures for comparing extensive amounts of spectra
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

# mass-spectrometry-data-format-import

## Summary

Import raw mass spectrometry data from standard spectral file formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) into a Python-based object representation suitable for downstream processing and comparison. This skill is foundational to any matchms workflow, as it standardizes disparate file formats into a unified spectral data model.

## When to use

You have raw mass spectrometry data in one of the supported spectral formats (mzML, mzXML, msp, MGF, JSON, or metabolomics-USI) and need to load it into a Python environment for cleaning, processing, or similarity comparison. Use this skill at the start of any matchms pipeline before any data cleaning, filtering, or scoring steps.

## When NOT to use

- Input data is already in matchms Spectrum object format in memory or serialized; use direct deserialization instead.
- Input file format is not one of the six supported formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI); custom conversion is required first.
- Data has already undergone cleaning and filtering in a prior workflow step; import step is not repeatable without data loss.

## Inputs

- Mass spectrometry data file in mzML format
- Mass spectrometry data file in mzXML format
- Mass spectrometry data file in msp format
- Mass spectrometry data file in MGF format
- Mass spectrometry data file in JSON format
- Mass spectrometry data file in metabolomics-USI format

## Outputs

- Spectrum collection object (list or iterable of Spectrum objects in matchms)
- Loaded spectra with parsed metadata and peak arrays

## How to apply

Use the matchms Python API to import spectral data files. The import process standardizes metadata and peak information from the chosen format into matchms' internal spectrum objects. Select the appropriate loader based on your input file extension (e.g., load_msp for .msp files, import_json for JSON files). The resulting spectrum collection is then ready for metadata cleaning, peak filtering, and similarity scoring. Verify that all spectra have loaded by checking the spectrum count and spot-checking metadata fields (e.g., precursor_mz, spectrum title) against the source file.

## Related tools

- **matchms** (Python package providing API and loader functions for importing mass spectrometry data from supported file formats) — https://github.com/matchms/matchms
- **Python** (Programming language in which matchms API and import workflows are written)

## Examples

```
from matchms.importing_utils import load_from_msp; spectra = list(load_from_msp('spectra_library.msp'))
```

## Evaluation signals

- All expected spectra are loaded without errors; spectrum count matches the source file or documented collection size.
- Metadata fields (precursor_mz, spectrum title, retention time, compound name, etc.) are correctly parsed and populated across spectra.
- Peak arrays (m/z and intensity pairs) are correctly extracted and stored in each Spectrum object.
- File format is correctly auto-detected or specified and no data corruption occurs during import.
- Spectrum objects are serializable and pass basic schema validation for downstream matchms operations (e.g., can be passed to similarity scoring functions).

## Limitations

- Matchms supports only the six documented spectral formats; vendor-specific or custom formats require prior conversion.
- Import does not perform data cleaning or validation; metadata may contain errors, inconsistencies, or missing fields that must be addressed in subsequent cleaning steps.
- Large spectral collections (hundreds of thousands of spectra) may consume significant memory during import; consider batch import strategies for very large files.
- Some metadata fields may be missing or non-standard depending on the originating instrument or software; downstream validation is recommended.

## Evidence

- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [readme] Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data: "Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data (MS/MS)"
- [other] Load cleaned spectral data (in supported formats: mzML, mzXML, msp, MGF, JSON) using matchms Python API: "Load cleaned spectral data (in supported formats: mzML, mzXML, msp, MGF, JSON) using matchms Python API"
- [readme] transforming raw data from common mass spectra file formats into pre- and post-processed spectral data: "transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
