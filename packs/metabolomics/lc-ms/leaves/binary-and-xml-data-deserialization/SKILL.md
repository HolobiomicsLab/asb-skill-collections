---
name: binary-and-xml-data-deserialization
description: Use when you have raw LC-MS data in .mzML (XML-based) or Thermo .raw
  (proprietary binary) format and need to load it into memory for visualization, querying,
  or downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - lcmsWorld
  - RawFileReader (Thermo)
  - XML parser (mzML)
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

# binary-and-xml-data-deserialization

## Summary

Parse and deserialize proprietary binary (Thermo .raw) and XML-based (.mzML) LC-MS data files into structured in-memory spectral objects with indexed access to scans, retention times, m/z values, and intensities. This skill is essential for ingesting heterogeneous mass spectrometry file formats into visualization and analysis pipelines.

## When to use

Use this skill when you have raw LC-MS data in .mzML (XML-based) or Thermo .raw (proprietary binary) format and need to load it into memory for visualization, querying, or downstream analysis. Specifically, apply it when lcmsWorld or similar viewers must support multiple file format inputs, or when you need to extract and validate spectral metadata (retention time, m/z, intensity, scan number, MS level) from heterogeneous sources before 3D rendering or identification annotation.

## When NOT to use

- Input data is already in a parsed, memory-resident format (e.g., already loaded spectral data object or feature table).
- File format is neither .raw nor .mzML (e.g., NetCDF, .h5ad, or proprietary vendor formats not supported by RawFileReader or mzML schema).
- Storage is constrained such that an in-memory copy of the entire spectral dataset cannot fit; streaming or chunked parsing is required instead.

## Inputs

- Thermo .raw file (binary proprietary format)
- mzML file (XML-based spectral data format)

## Outputs

- In-memory indexed spectral data structure with scan-level access
- .lcms cache file (optional; created on first load for fast subsequent access)
- Structured metadata object (retention time, m/z values, intensities, scan number, MS level per scan)

## How to apply

Detect the input file format by checking the file extension (.mzML or .raw). Route to the appropriate format-specific parser: use an XML parser for .mzML files to extract spectral data from the structured XML hierarchy, and use the Thermo RawFileReader (a .NET library) for .raw files to decode the proprietary binary format. Extract key spectral metadata—retention time, m/z values, intensities, scan number, and MS level—from each parsed record. Construct an in-memory spectral data structure with indexed access to scans (e.g., by scan number or retention time) to enable efficient random access during rendering. Validate that all expected fields are present and scan counts match file metadata before returning the structured object to the downstream viewer or analysis component.

## Related tools

- **lcmsWorld** (3D LC-MS viewer that invokes file deserialization during 'Load LC-MS file' workflow; calls format-specific parsers and renders the resulting structured spectral object) — https://github.com/PGB-LIV/lcmsWorld
- **RawFileReader (Thermo)** (64-bit .NET library used to deserialize Thermo .raw binary files into accessible spectral records)
- **XML parser (mzML)** (Deserializes XML-structured .mzML spectral data into hierarchical objects for metadata extraction)

## Evaluation signals

- File parsing completes without exception and produces a non-empty in-memory spectral data structure.
- Extracted metadata (retention time, m/z, intensity, scan number, MS level) matches expected ranges and cardinality (e.g., MS1 scans contain valid m/z and intensity arrays; retention times are in ascending or valid order).
- Indexed access by scan number or retention time returns the correct spectral record with no missing fields.
- Downstream renderer successfully consumes the structured object and displays 3D visualization without crashes or warnings.
- Optional: .lcms cache file is generated and a subsequent load of the same file from the cache completes in substantially less time than the initial parse.

## Limitations

- RawFileReader is a 64-bit only .NET application; may require .NET Framework 4.7+ on Windows and is untested or unsupported on Linux/MacOS.
- For large .raw or .mzML files, parsing can be slow and memory-intensive; the README recommends loading from fast hard disk and warns that disk space and RAM should be at least as large as the input file size.
- MacOS support is noted as untested for a long time and unlikely to work without changes; minimal error checking is performed during parsing.
- Identification file loading (.csv or tab-separated text) is supported but noted in the README as 'better loading of identifications' is a future feature, implying current parsing may have limitations.

## Evidence

- [intro] lcmsWorld loads .mzml or Thermo .raw format files for LC-MS data visualization: "lcmsWorld is a 3d viewer for LC-MS data (it can load ```.mzml``` or Thermo ```.raw``` format files)"
- [other] Format detection and routing to format-specific parsers: "1. Detect the input file format based on file extension (.mzML or .raw). 2. Parse the file using format-specific parsers (mzML parser for XML-based spectral data; Thermo RAW parser for proprietary"
- [other] Metadata extraction and indexing workflow: "3. Extract key spectral metadata (retention time, m/z values, intensities, scan number, MS level). 4. Construct an in-memory spectral data structure with indexed access to scans. 5. Validate parsing"
- [readme] RawFileReader for .raw deserialization: "RawFileReader from Thermo is used to load .raw files.  This is a 64-bit only .NET application."
- [readme] Resource requirements and caching workflow: "The first time you load a file, lcmsWorld automatically converts this file and creates a corresponding .lcms file. In future, you can load this .lcms file to start viewing instantly."
- [readme] Platform and .NET dependency constraint: "You may need to install .NET Framework 4.7 on Windows to use this."
