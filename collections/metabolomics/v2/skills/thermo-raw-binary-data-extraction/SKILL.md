---
name: thermo-raw-binary-data-extraction
description: Use when you have acquired .raw files from a Thermo mass spectrometer (e.g., Q Exactive, Orbitrap) and need to expose their contents—scan numbers, retention times, m/z values, intensities, and precursor information—for downstream nontargeted LCMS feature detection and alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - bmxp
  - Chroma
  - Eclipse
derived_from:
- doi: 10.1093/bioinformatics/btaf290/8128335
  title: Eclipse
evidence_spans:
- They are written in Python and C
- pip install bmxp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
  dedup_kept_from: coll_eclipse_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf290/8128335
  all_source_dois:
  - 10.1093/bioinformatics/btaf290/8128335
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# thermo-raw-binary-data-extraction

## Summary

Extract spectral metadata, scan information, and ion data from Thermo RAW binary files into a unified structured representation compatible with downstream LCMS processing. This skill transforms proprietary mass spectrometry instrument output into interoperable data structures suitable for alignment, clustering, and drift correction in metabolomics pipelines.

## When to use

You have acquired .raw files from a Thermo mass spectrometer (e.g., Q Exactive, Orbitrap) and need to expose their contents—scan numbers, retention times, m/z values, intensities, and precursor information—for downstream nontargeted LCMS feature detection and alignment. Use this skill as the first step in the BMXP metabolomics pipeline when ingesting raw instrument data.

## When NOT to use

- Input is already in mzML format; use the mzML parser instead.
- Data have already been converted to a feature table or abundance matrix; this skill targets raw instrument output.
- Targeted analysis with predefined compound lists; this skill is designed for nontargeted LCMS feature discovery.

## Inputs

- .raw files (Thermo RAW binary format)
- Reference .raw files for validation

## Outputs

- Structured spectral data object (Python dict or class)
- Unified representation exposing scan number, retention time, m/z values, intensities, precursor information

## How to apply

Implement a file format handler in Python that detects .raw files and routes them to a Thermo RAW parser capable of extracting binary spectral data. The parser must reconstruct spectral metadata (scan number, retention time, m/z array, intensity array) and precursor ion information into a unified data structure (dictionary or class) that abstracts format-specific details. Validate the parsed output by comparing key fields (scan count, RT range, m/z distribution, total ion current) against known reference .raw files to confirm fidelity. Handle file I/O errors and truncated files gracefully to ensure robustness in production workflows. The resulting structured object should expose common properties (scan number, retention time, m/z values, intensities, precursor information) that downstream modules like Eclipse and Gravity can consume directly.

## Related tools

- **bmxp** (Framework and shared schema for LCMS module integration; provides unified data structure abstractions and cloud-compatible execution environment) — https://github.com/broadinstitute/bmxp
- **Chroma** (Standalone BMXP module that orchestrates .raw and .mzml file parsing; routes data to format-specific parsers and exposes outputs for downstream processing) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/chroma/readme.md
- **Eclipse** (Consumes Chroma-parsed spectral data to align two or more same-method nontargeted LCMS datasets) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md

## Evaluation signals

- Scan count matches the original .raw file metadata.
- Retention time range (min, max) aligns with instrument acquisition window.
- m/z arrays are sorted and within expected instrument mass range (e.g., 50–2000 m/z for typical metabolomics).
- Intensities are non-negative and exhibit realistic dynamic range (no all-zero or saturated spectra).
- Precursor m/z and charge state are present for MS/MS scans; parent scan references are internally consistent.

## Limitations

- Thermo RAW format is proprietary and may require vendor libraries or reverse-engineered parsers; compatibility depends on Thermo RAW file version.
- Malformed or truncated .raw files may fail to parse; robust error handling is essential but cannot guarantee recovery of all data.
- Metadata extraction fidelity depends on correct interpretation of binary structures; validation against reference files is necessary to confirm correctness.
- Cloud deployment may require additional licensing or sandboxing for proprietary Thermo SDK components.

## Evidence

- [other] Chroma is a standalone module designed to read .raw and .mzml files, serving as the data input step that exposes mass spectrometry file contents for downstream processing in the BMXP pipeline.: "Chroma is a standalone module designed to read .raw and .mzml files, serving as the data input step that exposes mass spectrometry file contents for downstream processing"
- [other] Implement a parser for .raw files (Thermo RAW format) that extracts spectral metadata, scan information, and ion data into a structured object.: "Implement a parser for .raw files (Thermo RAW format) that extracts spectral metadata, scan information, and ion data into a structured object"
- [other] Define a unified data structure (class or dictionary schema) that abstracts both formats and exposes common properties (scan number, retention time, m/z values, intensities, precursor information).: "Define a unified data structure (class or dictionary schema) that abstracts both formats and exposes common properties (scan number, retention time, m/z values, intensities, precursor information)"
- [other] Implement file I/O and error handling to ensure robust reading of malformed or truncated files.: "Implement file I/O and error handling to ensure robust reading of malformed or truncated files"
- [other] Validate the structured output against known reference .raw and .mzml files to confirm fidelity of parsed data.: "Validate the structured output against known reference .raw and .mzml files to confirm fidelity of parsed data"
- [readme] Each tool is meant to be a standalone module that performs a step in our processing pipeline.: "Each tool is meant to be a standalone module that performs a step in our processing pipeline"
