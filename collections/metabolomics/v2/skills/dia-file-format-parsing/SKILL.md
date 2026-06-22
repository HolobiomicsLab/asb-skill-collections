---
name: dia-file-format-parsing
description: Use when you have raw DIA mass spectrometry files in timsTOF (.d), TripleTOF (.wiff), or Orbitrap (.raw) format and need to extract precursor ion chromatogram (PIC) data as input for quality metric computation or machine learning-based file quality prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - msConvert
  - Python
derived_from:
- doi: 10.1038/s41467-024-54871-1
  title: iDIA-QC
evidence_spans:
- uses msConvert for file conversion to extracted precursor ion chromatogram (PIC)
- iDIA-QC is a Python Graphical User Interface (GUI)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idia_qc_cq
    doi: 10.1038/s41467-024-54871-1
    title: iDIA-QC
  dedup_kept_from: coll_idia_qc_cq
schema_version: 0.2.0
---

# dia-file-format-parsing

## Summary

Parse and extract precursor ion chromatogram (PIC) data from raw DIA mass spectrometry files (timsTOF, TripleTOF, Orbitrap formats) using msConvert, enabling downstream metric extraction and quality assessment. This skill converts instrument-native binary formats into a standardized chromatographic representation suitable for computational analysis.

## When to use

You have raw DIA mass spectrometry files in timsTOF (.d), TripleTOF (.wiff), or Orbitrap (.raw) format and need to extract precursor ion chromatogram (PIC) data as input for quality metric computation or machine learning-based file quality prediction. Use this skill when instrument-native file formats must be converted to a format that computational pipelines can load and process.

## When NOT to use

- PIC data has already been extracted or converted to an intermediate format (e.g., mzML, netCDF) — skip directly to metric extraction.
- Raw files are not from supported instruments (timsTOF, TripleTOF, Orbitrap) — msConvert may not support the native format.
- You only need to validate file integrity without computing quality metrics — file format validation alone does not require full PIC extraction.

## Inputs

- raw DIA mass spectrometry files (.raw, .d, .wiff formats)
- instrument type specification (timsTOF, TripleTOF, or Orbitrap)
- msConvert installation and configuration

## Outputs

- extracted precursor ion chromatogram (PIC) files in standardized format
- validated PIC files ready for metric extraction

## How to apply

Load raw DIA files in supported formats (timsTOF, TripleTOF, Orbitrap native formats) and apply msConvert with PIC extraction parameters to convert each file into extracted precursor ion chromatogram format. Validate converted PIC files for format integrity and completeness to ensure downstream analysis relies on well-formed input. The conversion standardizes heterogeneous instrument outputs into a uniform chromatographic representation that can then be loaded into Python for metric extraction. This preprocessing step is necessary because the iDIA-QC pipeline computes 15 quality-characterizing metrics from the converted PIC data, not directly from native binary files.

## Related tools

- **msConvert** (Converts raw DIA mass spectrometry files into extracted precursor ion chromatogram (PIC) format; applies PIC extraction parameters during conversion)
- **Python** (Used to load converted PIC data into computational environment for downstream processing and validation) — https://github.com/guomics-lab/iDIA-QC

## Evaluation signals

- Converted PIC files are generated in standardized format and are readable by downstream Python scripts without errors
- File format validation passes — PIC files contain expected precursor ion chromatogram data structure with no truncation or corruption
- PIC files from all three instrument types (timsTOF, TripleTOF, Orbitrap) convert successfully and contain non-empty chromatographic data
- Downstream metric extraction scripts can load PIC files and compute 15 metrics without raising format or schema errors
- Output file count matches input file count, indicating no silent failures during batch conversion

## Limitations

- msConvert supports only .raw, .d, and .wiff formats; other raw data formats will not convert successfully
- PIC extraction parameters must be correctly specified for each instrument type to ensure representative chromatographic data; incorrect parameters may produce incomplete or misleading PIC output
- Conversion is computationally intensive and may require substantial disk space for large batch conversions
- Format integrity validation depends on downstream loading and analysis; silent corruption may not be detected until metric extraction fails

## Evidence

- [intro] This preprocessing ensures raw files conform to a standard format amenable to metric computation: "raw DIA mass spectrometry files (supported formats: timsTOF, TripleTOF, Orbitrap native formats). 2. Apply msConvert with PIC extraction parameters to convert each raw file into extracted precursor"
- [intro] Conversion produces standardized PIC files ready for metric extraction: "uses msConvert for file conversion to extracted precursor ion chromatogram (PIC)"
- [readme] Input file formats and instrument types are clearly scoped: "This software supports the .raw, .d, and .wiff raw data formats. Choose the type of instrument that generated the file."
- [intro] PIC conversion is a discrete upstream step in the iDIA-QC workflow: "1. Load converted PIC data into Python environment. 2. Compute 15 quality-characterizing metrics from each DIA file"
