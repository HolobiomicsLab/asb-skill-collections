---
name: mass-spectrometry-format-conversion
description: Use when when you have mass spectrometry spectra in one of the six supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) and need to convert them to a different format for compatibility with downstream tools, or when importing raw spectra into matchms for the first time and need to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pytest
  - matchms
  - poetry
  - Rust mzPeak CLI
  - Cargo (Rust package manager)
  - Parquet
  - ZIP
derived_from:
- doi: 10.1186/s13321-024-00878-1
  title: matchms
- doi: 10.1021/acs.jproteome.5c00435
  title: ''
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
  - build: coll_mzpeak_cq
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_matchms_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-024-00878-1
  all_source_dois:
  - 10.1186/s13321-024-00878-1
  - 10.1021/acs.jproteome.5c00435
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-format-conversion

## Summary

Convert mass spectrometry spectral data between supported file formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) while preserving metadata and peak list integrity. This skill enables standardization of heterogeneous spectral datasets for downstream processing and comparison workflows in matchms.

## When to use

When you have mass spectrometry spectra in one of the six supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) and need to convert them to a different format for compatibility with downstream tools, or when importing raw spectra into matchms for the first time and need to ensure correct parsing of both metadata and peak intensity data.

## When NOT to use

- When spectra are already in a standardized intermediate format (e.g., already loaded as matchms Spectrum objects in memory) and no serialization to disk is needed.
- When the source or target format is not among the six supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON).
- When preservation of all vendor-specific metadata is required and the target format does not support the full metadata schema of the source format.

## Inputs

- Raw mass spectrometry spectra in mzML format
- Raw mass spectrometry spectra in mzXML format
- Raw mass spectrometry spectra in msp format
- Raw mass spectrometry spectra in MGF format
- Raw mass spectrometry spectra in JSON format
- Raw mass spectrometry spectra in metabolomics-USI format

## Outputs

- Converted mass spectrometry spectra in target format
- matchms Spectrum objects with harmonized metadata
- Peak lists with validated m/z and intensity values

## How to apply

Load raw spectra using matchms import functions that parse the source format (mzML, mzXML, msp, MGF, JSON, or metabolomics-USI) and construct matchms Spectrum objects with normalized metadata and peak lists. The parser extracts metadata fields and peak intensity data from each format according to its specification. Run pytest to validate that parsing produces correct Spectrum objects with expected metadata and peak counts. Convert to the target format by serializing the Spectrum objects using the corresponding matchms export function. Verify conversion integrity by spot-checking metadata harmonization and comparing input/output peak counts to detect truncation or loss.

## Related tools

- **matchms** (Python package providing Spectrum object schema, parser functions for six file formats, and serialization methods for format conversion) — https://github.com/matchms/matchms
- **pytest** (Unit testing framework used to validate correct parsing of each format and Spectrum object construction for representative samples)
- **poetry** (Dependency and version management tool for the matchms package)

## Evaluation signals

- All pytest unit tests for format-specific parsers pass without errors or warnings.
- Peak count in converted output matches peak count in input source (no truncation or loss).
- Metadata fields in converted spectra match expected schema (e.g., parent_mass, precursor_mz, spectrum_type are present and non-null where expected).
- Spot-check: manually inspect 3–5 randomly selected spectra from converted dataset and confirm metadata consistency and m/z ordering (monotonically increasing within tolerance).
- Round-trip test: convert spectra A→B→A and verify that critical fields (parent_mass, peak lists, metadata) are identical or within expected tolerance before/after.

## Limitations

- Matchms supports only six file formats; spectra in other mass spectrometry formats (e.g., .raw, .d, .wiff) must be pre-converted using vendor software or external tools.
- Metadata normalization may result in loss of vendor-specific fields not defined in the matchms Spectrum schema; conversion is lossy in this respect.
- Large spectral datasets (hundreds of thousands of spectra) may require significant memory and disk I/O during format conversion; performance is not optimized for single-pass streaming.

## Evidence

- [intro] File format support claim: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [other] Parser implementation workflow: "Implement individual parser functions that extract metadata and peak lists from each format and construct matchms Spectrum objects"
- [other] Validation approach: "Write unit tests using pytest to validate correct parsing and Spectrum object construction for representative samples in each format"
- [other] Import workflow step: "Load raw spectra data in supported formats (mzML, mzXML, msp, metabolomics-USI, MGF, JSON) using matchms import functions"
- [intro] Data transformation purpose: "transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
