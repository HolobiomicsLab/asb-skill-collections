---
name: thermo-raw-format-parsing
description: Use when when you have LC-MS data in Thermo .raw format (a proprietary
  binary output from Thermo mass spectrometers) and need to load it into a 3D LC-MS
  viewer or extract structured spectral metadata (retention time, m/z values, intensities,
  scan number, MS level) for visualization or quantitative.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - lcmsWorld
  - RawFileReader
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.0c00618
  title: lcmsWorld
evidence_spans:
- lcmsWorld is a 3d viewer for LC-MS data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lcmsworld_cq
    doi: 10.1021/acs.jproteome.0c00618
    title: lcmsWorld
  dedup_kept_from: coll_lcmsworld_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00618
  all_source_dois:
  - 10.1021/acs.jproteome.0c00618
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# thermo-raw-format-parsing

## Summary

Parse Thermo .raw binary files to extract LC-MS spectral metadata and ion intensity data for visualization and downstream analysis. This skill converts proprietary Thermo RAW format into an in-memory spectral data structure indexed by scan number.

## When to use

When you have LC-MS data in Thermo .raw format (a proprietary binary output from Thermo mass spectrometers) and need to load it into a 3D LC-MS viewer or extract structured spectral metadata (retention time, m/z values, intensities, scan number, MS level) for visualization or quantitative analysis.

## When NOT to use

- Input is already in mzML or other open XML-based spectral format (use mzML parser instead).
- Input file extension is not .raw or file is not from a Thermo instrument (use format-detection before attempting RAW parsing).
- System does not have .NET Framework 4.7+ installed or is not 64-bit Windows (prerequisite for RawFileReader).

## Inputs

- Thermo .raw file (proprietary binary format from Thermo mass spectrometers)

## Outputs

- Indexed in-memory spectral data structure with extracted scans
- Spectral metadata (retention time, m/z values, intensities, scan number, MS level per scan)

## How to apply

Detect that the input file has a .raw extension, then invoke the Thermo RawFileReader .NET library to parse the proprietary binary format. Extract key spectral metadata including retention time, m/z values, intensities, scan number, and MS level from each scan. Construct an indexed in-memory spectral data structure that allows random access to scans. Validate that parsing is complete by confirming all scans have been read and metadata fields are populated. Return the structured data object to the viewer renderer or downstream analysis module. Note: RawFileReader is a 64-bit only .NET application and requires .NET Framework 4.7 or later on Windows.

## Related tools

- **lcmsWorld** (3D viewer that consumes parsed Thermo .raw spectral data structures for interactive LC-MS visualization) — https://github.com/PGB-LIV/lcmsWorld
- **RawFileReader** (Thermo proprietary .NET library that performs binary parsing of .raw files)

## Evaluation signals

- All scans in the input .raw file are successfully read; scan count matches Thermo software enumeration.
- Extracted metadata fields (retention time, m/z, intensities, scan number, MS level) are non-null and within expected ranges (e.g., m/z > 0, retention time ≥ 0, intensities ≥ 0).
- Indexed access to scans is functional; random retrieval of arbitrary scan numbers completes without error.
- The generated .lcms output file can be loaded by lcmsWorld for visualization without parse errors.
- Spectral metadata round-trips correctly: re-parsing the same .raw file produces identical metadata.

## Limitations

- RawFileReader is 64-bit only and requires .NET Framework 4.7+ on Windows; not natively available on Linux or macOS.
- Large .raw files require proportional hard disk space for the converted .lcms output file; file conversion time scales with file size.
- Little error checking is performed during parsing; malformed or corrupted .raw files may cause silent data loss or incomplete extraction.
- The .raw format is proprietary to Thermo; parsing depends on Thermo's RawFileReader library, which may not support all instrument variants or firmware versions.

## Evidence

- [other] Thermo RAW parser for proprietary binary format: "mzML parser for XML-based spectral data; Thermo RAW parser for proprietary binary format"
- [readme] RawFileReader from Thermo is used for .raw loading: "RawFileReader from Thermo is used to load .raw files. This is a 64-bit only .NET application."
- [readme] .NET Framework prerequisite for Windows: "You may need to install .NET Framework 4.7 on Windows to use this."
- [other] Extraction of key spectral metadata from scans: "Extract key spectral metadata (retention time, m/z values, intensities, scan number, MS level)"
- [readme] .raw files are converted to .lcms indexed format: "The first time you load a file, lcmsWorld automatically converts this file and creates a corresponding .lcms file."
