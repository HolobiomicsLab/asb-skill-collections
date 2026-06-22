---
name: mass-spectrometry-metadata-parsing
description: Use when you have a Thermo Fisher Orbitrap .raw file and need to programmatically inspect or validate its acquisition parameters (instrument type, total scan count, acquisition duration, file name) before extracting spectral data, or when you need to serialize metadata to JSON for data provenance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RawFileReader
  - rjson
  - rawrr
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific.
- invoke compiled `C#` wrapper methods using a system call. Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo
- rjson::toJSON
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_2_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.10.30.362533
  all_source_dois:
  - 10.1101/2020.10.30.362533
  - 10.1021/acs.jproteome.0c00866
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-metadata-parsing

## Summary

Extract and deserialize instrument metadata from proprietary Thermo Fisher Scientific .raw files into structured R objects (lists, data frames) using the RawFileReader API. This skill bridges the gap between binary mass spectrometry data storage and downstream R-based statistical analysis by exposing file-level metadata such as instrument model, acquisition time range, scan count, and control software version.

## When to use

You have a Thermo Fisher Orbitrap .raw file and need to programmatically inspect or validate its acquisition parameters (instrument type, total scan count, acquisition duration, file name) before extracting spectral data, or when you need to serialize metadata to JSON for data provenance, workflow documentation, or quality control dashboards.

## When NOT to use

- Input is a non-Thermo Fisher raw file (e.g., mzML, mzXML, Bruker, Waters) — use vendor-specific parsers or ProteoWizard converters instead.
- You need full spectral data (m/z, intensity arrays) rather than file-level metadata — use readSpectrum() or readIndex() instead.
- The .raw file was acquired on a non-Orbitrap Thermo instrument and RawFileReader support is unavailable — check RawFileReader compatibility matrix.

## Inputs

- Thermo Fisher Scientific .raw file (binary mass spectrometry data file)
- File path as character string

## Outputs

- R list object with instrument metadata (instrument model, acquisition time range, scan count, file name)
- JSON-serialized metadata file (optional)

## How to apply

Install the rawrr R package and its compiled RawFileReader executable using rawrr::installRawrrExe(). Load the target .raw file path and call readFileHeader() to invoke the compiled C# RawFileReader wrapper via a system call, which extracts binary metadata from the file header and writes it to a temporary location, then parses it back into an R list object. The returned list contains dynamically-generated items that vary by instrument model and control software version; common fields include instrument model name, file name, time range (start/end scan times), and total scan count. Validate that the list structure is non-empty and contains expected top-level keys (e.g., 'Instrument Model', 'Time range', 'Number of scans'). Optionally serialize the list to JSON using rjson::toJSON() and write to a .json file for downstream consumption or archival.

## Related tools

- **RawFileReader** (Vendor-provided .NET assembly that exposes the low-level API for reading binary Thermo Fisher .raw file headers and spectral data; invoked by rawrr via system calls.) — https://github.com/thermofisherlsms/RawFileReader
- **rawrr** (R package wrapper around RawFileReader; provides readFileHeader() function to extract and return metadata as an R list object.) — https://github.com/fgcz/rawrr
- **rjson** (R package for serializing R objects (e.g., metadata list) to JSON format for export and validation.)

## Examples

```
library(rawrr); rawrr::installRawrrExe(); header <- readFileHeader('20181113_010_autoQC01.raw'); cat('Instrument:', header$'Instrument Model', '\n', 'Scans:', header$'Number of scans', '\n')
```

## Evaluation signals

- readFileHeader() returns a non-null R list object with length > 0.
- Returned list contains expected top-level keys such as 'Instrument Model', 'File Name', 'Time range', and 'Number of scans'.
- If JSON serialization is performed, the output file exists at the specified path and parses successfully as valid JSON (e.g., using jsonlite::fromJSON() without error).
- Metadata values are consistent with file properties (e.g., 'Number of scans' is a positive integer; 'Time range' is a numeric vector of length 2 with start < end; 'Instrument Model' is a non-empty character string).
- If metadata is re-read from JSON, deserialized values match the original R list structure and values.

## Limitations

- readFileHeader() works only on Thermo Fisher Orbitrap .raw files; not compatible with other vendor formats or older Thermo instruments unless RawFileReader explicitly supports them.
- Metadata structure and available fields vary dynamically by instrument model and control software version, so downstream code must handle optional or version-specific fields gracefully.
- RawFileReader is a proprietary .NET assembly that requires Windows, Linux, or macOS runtime support and must be explicitly installed via rawrr::installRawrrExe(); availability and licensing may vary by institution.
- On non-Windows systems, RawFileReader relies on .NET runtime (Mono or .NET Core) and may have platform-specific bugs or performance limitations not present on Windows.
- File I/O overhead (writing to temporary disk location and reading back into R memory) can be slow for repeated calls on large .raw files; consider caching metadata when possible.

## Evidence

- [other] readFileHeader() retrieves metadata from binary raw files including instrument model, file name, time range of data acquisition, and number of scans, returning these items as a list object containing dynamically-generated data items that vary by instrument model and control software version.: "readFileHeader() retrieves metadata from binary raw files including instrument model, file name, time range of data acquisition, and number of scans, returning these items as a list object containing"
- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call.: "`R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call."
- [methods] Extracted information is written to temporary location on harddrive, read back into memory and parsed into R objects.: "the extracted information is written to a temporary location on the harddrive, read back into memory and"
- [intro] rawrr wraps the functionality of the RawFileReader .NET assembly.: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [results] The respective function is called readFileHeader() and returns a simple R object of type list.: "The respective function is called `readFileHeader()` and returns a simple `R` object of type `list`"
- [readme] The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package.: "The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend"
