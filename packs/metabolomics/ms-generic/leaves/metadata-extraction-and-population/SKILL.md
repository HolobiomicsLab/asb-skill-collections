---
name: metadata-extraction-and-population
description: Use when when importing raw mass spectrometry data from files in supported formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) and you need to extract and standardize metadata fields so that spectra are ready for metadata cleaning, validation, and comparative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
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

# metadata-extraction-and-population

## Summary

Extract metadata fields (compound name, molecular weight, precursor m/z, ionization mode, etc.) from raw mass spectrometry file formats and populate them into matchms spectrum objects for downstream processing and similarity comparisons. This skill ensures that spectral records are enriched with standardized, validated metadata alongside their m/z and intensity arrays.

## When to use

When importing raw mass spectrometry data from files in supported formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) and you need to extract and standardize metadata fields so that spectra are ready for metadata cleaning, validation, and comparative analysis. Use this skill as part of the initial data ingestion pipeline before processing or similarity scoring.

## When NOT to use

- Input spectra are already instantiated as matchms Spectrum objects with validated metadata — use metadata cleaning or filtering skills instead.
- Metadata is not available in the input file (e.g., centroided MGF with only m/z and intensity) — skip metadata population and focus on spectral array extraction.
- File format is not one of the six supported formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) — this skill will fail; use custom parser or convert file format first.

## Inputs

- Raw mass spectrometry data files in one of: mzML, mzXML, msp, MGF, JSON, or metabolomics-USI format
- File path(s) pointing to mass spectrometry spectral data
- Format specification or schema describing expected metadata fields

## Outputs

- matchms Spectrum objects populated with m/z arrays, intensity arrays, and metadata fields
- Validated metadata dictionaries (intermediate representation before Spectrum instantiation)
- Unit test results confirming metadata extraction fidelity per format

## How to apply

Design format-specific parsers for each supported file type (mzML, mzXML, msp, MGF, JSON, metabolomics-USI), each extracting spectral peaks, metadata fields, and intensity values into intermediate data dictionaries. Map raw metadata keys to matchms spectrum object fields (e.g., compound identifiers, molecular weights, precursor m/z values, ionization mode, collision energy). Instantiate matchms spectrum objects by populating required fields (m/z arrays, intensity arrays) alongside extracted metadata. Validate that all populated metadata conform to expected data types and are not malformed. Unit test each format parser using pytest to confirm metadata extraction accuracy and that spectrum objects are compatible with downstream processing workflows.

## Related tools

- **matchms** (Core library providing Spectrum class, parser interface, and metadata validation for multi-format spectral data import) — https://github.com/matchms/matchms
- **pytest** (Unit testing framework for verifying metadata extraction correctness and schema compliance per file format)
- **Python** (Programming language for implementing format-specific parsers and Spectrum object instantiation)

## Examples

```
from matchms.importing import load_from_msp; spectra = load_from_msp('library.msp'); print(f'Loaded {len(spectra)} spectra with metadata: {spectra[0].metadata.keys()}')
```

## Evaluation signals

- Metadata dictionaries from each file format contain expected keys (e.g., 'compound_name', 'precursor_mz', 'ionization_mode') with non-null values matching raw file content.
- Instantiated Spectrum objects populate all required fields (m/z array, intensity array, metadata) without raising AttributeError or validation exceptions.
- Unit tests pass for all six supported formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI), confirming round-trip fidelity: raw file → parsed metadata → Spectrum object.
- Spectrum objects are compatible with downstream matchms workflows (processing, cleaning, similarity scoring) — no schema mismatches or missing field errors during pipeline execution.
- Metadata values conform to expected data types (e.g., precursor_mz as float, compound_name as string, ionization_mode as controlled vocabulary) and fall within plausible ranges.

## Limitations

- Metadata extraction fidelity depends on file format compliance; malformed or non-standard metadata in the input file may be skipped, truncated, or misinterpreted.
- Not all metadata fields present in raw files are extracted; only fields recognized by format-specific parsers are populated into Spectrum objects.
- Conflicting or redundant metadata fields from different file formats may require reconciliation or prioritization rules during parser design.
- Large-scale metadata extraction may exhibit I/O bottlenecks when reading many large spectral files; consider batching or streaming strategies for very large datasets.

## Evidence

- [other] Implement format-specific parsers for each file type, each extracting spectral peaks, metadata, and intensity values into intermediate data dictionaries.: "Implement format-specific parsers for each file type, each extracting spectral peaks, metadata, and intensity values into intermediate data dictionaries"
- [other] Instantiate matchms spectrum objects from the parsed data, populating required fields (m/z arrays, intensity arrays, metadata).: "Instantiate matchms spectrum objects from the parsed data, populating required fields (m/z arrays, intensity arrays, metadata)"
- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [readme] transforming raw data from common mass spectra file formats into pre- and post-processed spectral data: "transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [other] Write unit tests using pytest to verify that spectra from each format are correctly imported with expected m/z, intensity, and metadata attributes.: "Write unit tests using pytest to verify that spectra from each format are correctly imported with expected m/z, intensity, and metadata attributes"
