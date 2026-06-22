---
name: spectral-data-import-validation
description: Use when when you have raw mass spectrometry data in one or more of the six supported file formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) and need to transform it into matchms spectrum objects for processing, cleaning, or similarity comparisons.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pytest
  - matchms
  techniques:
  - LC-MS
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

# spectral-data-import-validation

## Summary

Import mass spectrometry data from multiple file formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) into matchms spectrum objects and validate that spectral peaks, metadata, and intensity values are correctly parsed and compatible with downstream processing workflows.

## When to use

When you have raw mass spectrometry data in one or more of the six supported file formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) and need to transform it into matchms spectrum objects for processing, cleaning, or similarity comparisons. Use this skill at the entry point of any matchms workflow to ensure data integrity before applying downstream processing or comparison operations.

## When NOT to use

- Input data is already in the form of instantiated matchms spectrum objects
- Input file format is not among the six supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON)
- Raw spectral data is embedded in a custom binary or proprietary format without conversion to a supported format first

## Inputs

- mzML file
- mzXML file
- msp file
- MGF file
- JSON file
- metabolomics-USI reference

## Outputs

- matchms spectrum objects
- parsed spectral peaks (m/z arrays)
- parsed intensity arrays
- parsed metadata dictionaries

## How to apply

Design an import interface that accepts file paths in supported formats as input to the matchms library. Implement or invoke format-specific parsers for each file type to extract spectral peaks (m/z arrays), intensity values, and metadata into intermediate data dictionaries. Instantiate matchms spectrum objects from the parsed data, populating required fields (m/z arrays, intensity arrays, metadata). Write unit tests using pytest to verify that spectra from each format are correctly imported with expected m/z, intensity, and metadata attributes. Finally, validate that imported spectrum objects are compatible with downstream processing and comparison workflows by checking that required fields are populated and object types conform to matchms specifications.

## Related tools

- **matchms** (Core library for importing, parsing, and instantiating spectrum objects from multiple file formats) — https://github.com/matchms/matchms
- **pytest** (Framework for writing and running unit tests to verify correct import of spectra with expected m/z, intensity, and metadata attributes)
- **Python** (Programming language for implementing format-specific parsers and instantiating spectrum objects)

## Evaluation signals

- All spectra imported from each supported format contain non-empty m/z arrays and intensity arrays with matching lengths
- Metadata fields are correctly extracted and populated in spectrum objects (e.g., compound name, precursor m/z, ionization mode)
- Unit tests pass for each file format using pytest, confirming expected attributes match actual parsed values
- Spectrum objects can be successfully passed to downstream matchms processing functions (e.g., cleaning, normalization, similarity scoring) without type or schema errors
- Round-trip validation: re-exporting imported spectra to the same format and re-importing yields identical or semantically equivalent spectrum objects

## Limitations

- Import is limited to six file formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON); other MS/MS file formats require external conversion or parser implementation
- Format-specific parsers may handle optional or non-standard metadata fields inconsistently; validation should confirm that critical metadata for the downstream workflow is present
- Large files (several hundred thousands of spectra) may require memory optimization or batch processing strategies not covered by basic import alone
- Metabolomics-USI imports depend on external network/database access and may fail if the reference service is unavailable

## Evidence

- [other] supported file formats (mzML, mzXML, msp, metabolomics-USI, MGF, and JSON): "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] import raw spectral data into spectrum objects: "transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [intro] format-specific parsers extract spectral peaks, metadata, and intensity values: "Implement format-specific parsers for each file type, each extracting spectral peaks, metadata, and intensity values into intermediate data dictionaries"
- [intro] pytest unit tests verify correct import of m/z, intensity, and metadata attributes: "Write unit tests using pytest to verify that spectra from each format are correctly imported with expected m/z, intensity, and metadata attributes"
- [intro] validate imported spectrum objects are compatible with downstream processing: "Validate that imported spectrum objects are compatible with downstream processing and comparison workflows in matchms"
