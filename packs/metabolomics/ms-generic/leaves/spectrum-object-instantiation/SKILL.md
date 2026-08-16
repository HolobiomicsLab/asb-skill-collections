---
name: spectrum-object-instantiation
description: Use when after successfully parsing raw spectral data from one of the supported file formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) into intermediate dictionaries containing m/z arrays, intensity arrays, and metadata key-value pairs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pytest
  - matchms
  techniques:
  - mass-spectrometry
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

# spectrum-object-instantiation

## Summary

Convert parsed mass spectrometry data (m/z arrays, intensity values, and metadata) into matchms Spectrum objects that serve as the standardized input format for downstream processing and similarity comparisons. This skill bridges file parsing and the matchms object model, ensuring spectral data is represented in a canonical, queryable form.

## When to use

After successfully parsing raw spectral data from one of the supported file formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) into intermediate dictionaries containing m/z arrays, intensity arrays, and metadata key-value pairs. Use this skill immediately before passing spectra to processing pipelines, cleaning workflows, or similarity comparison routines.

## When NOT to use

- If spectral data has not yet been parsed into intermediate dictionaries—use format-specific parsers first.
- If the input m/z and intensity arrays have mismatched lengths or contain non-numeric values—validate and clean the parsed data before instantiation.
- If you are working directly with a native matchms import function (e.g., from_msp, from_mzml) that handles both parsing and instantiation in one step.

## Inputs

- Parsed spectral data dictionary (containing m/z array, intensity array, metadata key-value pairs)
- File format identifier (mzML, mzXML, msp, metabolomics-USI, MGF, or JSON)
- Intermediate data structure from format-specific parser

## Outputs

- matchms Spectrum object(s)
- Collection of instantiated Spectrum objects ready for downstream processing

## How to apply

Create Spectrum objects by populating required fields (m/z arrays, intensity arrays, metadata) from the parsed intermediate data dictionary. Each Spectrum instance should have validated m/z and intensity arrays of matching length, and metadata fields that conform to matchms standards. Ensure the instantiated objects are compatible with downstream processing by verifying they expose the expected attributes (e.g., m/z, intensities, metadata dict) before passing them to cleaning, filtering, or comparison workflows. Use pytest to write unit tests that verify spectrum objects from each supported format retain their original m/z, intensity, and metadata values without loss or corruption.

## Related tools

- **matchms** (Python library providing the Spectrum class definition and object instantiation interface) — https://github.com/matchms/matchms
- **pytest** (Testing framework for writing unit tests that verify Spectrum objects are correctly instantiated with expected m/z, intensity, and metadata attributes)
- **Python** (Programming language for implementing format-specific parsers and Spectrum instantiation logic)

## Evaluation signals

- Instantiated Spectrum objects expose the required attributes: m/z array, intensity array, and metadata dictionary.
- m/z and intensity arrays are of equal length and contain numeric types (float or int).
- Metadata fields match the original values from the parsed intermediate dictionary (no silent omission or corruption).
- Unit test suite using pytest passes for each supported format, confirming round-trip fidelity (parse → instantiate → verify).
- Instantiated Spectrum objects integrate without errors into downstream matchms workflows (processing, filtering, similarity scoring).

## Limitations

- matchms supports only six file formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON); spectra from other formats require custom parsing before instantiation.
- Spectrum instantiation does not perform metadata cleaning or validation; raw metadata from parsed data is preserved as-is—use dedicated metadata cleaning steps afterward if needed.
- Large-scale instantiation of many Spectrum objects may require attention to memory usage, particularly when holding entire spectral libraries in memory before writing to persistent storage.
- The Spectrum object model assumes standard mass spectrometry attributes (m/z, intensity, precursor m/z, etc.); non-standard or missing fields must be handled by the parser before instantiation.

## Evidence

- [other] Instantiate matchms spectrum objects from the parsed data, populating required fields (m/z arrays, intensity arrays, metadata).: "Instantiate matchms spectrum objects from the parsed data, populating required fields (m/z arrays, intensity arrays, metadata)"
- [readme] transforming raw data from common mass spectra file formats into pre- and post-processed spectral data: "transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [other] Write unit tests using pytest to verify that spectra from each format are correctly imported with expected m/z, intensity, and metadata attributes.: "Write unit tests using pytest to verify that spectra from each format are correctly imported with expected m/z, intensity, and metadata attributes"
- [other] Validate that imported spectrum objects are compatible with downstream processing and comparison workflows in matchms.: "Validate that imported spectrum objects are compatible with downstream processing and comparison workflows in matchms"
- [other] Implement format-specific parsers for each file type, each extracting spectral peaks, metadata, and intensity values into intermediate data dictionaries.: "Implement format-specific parsers for each file type, each extracting spectral peaks, metadata, and intensity values into intermediate data dictionaries"
