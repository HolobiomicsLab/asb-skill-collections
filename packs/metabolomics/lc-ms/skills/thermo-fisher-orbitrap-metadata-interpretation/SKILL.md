---
name: thermo-fisher-orbitrap-metadata-interpretation
description: Use when when you have a Thermo Fisher Scientific .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RawFileReader
  - rawrr
  - jsonlite
  - MsBackendRawFileReader
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific
- methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr_cq
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

# Thermo Fisher Orbitrap metadata interpretation

## Summary

Extract, parse, and serialize instrument metadata from proprietary Thermo Fisher Scientific .raw file headers into interpretable R objects and JSON format. This skill bridges access to raw binary Orbitrap data—including instrument model, scan counts, time ranges, and acquisition parameters—without requiring conversion to exchange formats.

## When to use

When you have a Thermo Fisher Scientific .raw file from an Orbitrap instrument and need to programmatically extract and interpret header-level metadata (instrument configuration, acquisition time span, total scan count, dynamic instrument parameters) prior to spectral data processing or to document instrument state and run parameters in a machine-readable format.

## When NOT to use

- Input is already converted to an open exchange format (mzML, mzXML, netCDF); use those parsers instead
- You only need spectral data (m/z, intensity arrays) or chromatogram traces; use readSpectrum() or readChromatogram() functions instead
- Analysis is on non-Thermo raw files (e.g., Bruker, Waters, Sciex); RawFileReader and rawrr are Thermo-specific

## Inputs

- Thermo Fisher Scientific .raw file (binary file path)
- RawFileReader .NET assembly (compiled executable)

## Outputs

- R list object containing header metadata (instrument model, file name, time range, scan count)
- JSON-serialized header metadata file (.json)

## How to apply

Install the rawrr R package and its compiled RawFileReader executable via rawrr::installRawrrExe(). Call rawrr::readFileHeader() on the .raw file path to retrieve a list object containing metadata items dynamically extracted from the binary file header via the RawFileReader .NET API. Inspect the returned list for key fields such as instrument model, file name, time range (acquisition start/end), and number of scans. Serialize the list to JSON using standard R JSON libraries (e.g., jsonlite::toJSON()) and write to a named .json output file. This workflow preserves the instrument's native metadata representation without format conversion, facilitating downstream integration with modular R-based proteomics pipelines.

## Related tools

- **rawrr** (R package wrapping RawFileReader .NET assembly; provides readFileHeader() and JSON serialization interface) — https://github.com/fgcz/rawrr
- **RawFileReader** (Vendor-provided .NET assembly (C# library) that directly reads binary .raw file structures and exposes header metadata via compiled API) — https://github.com/thermofisherlsms/RawFileReader
- **jsonlite** (R package for serializing list objects to JSON format)
- **MsBackendRawFileReader** (Bioconductor backend integrating rawrr into the Spectra ecosystem for unified spectral data access) — https://github.com/fgcz/MsBackendRawFileReader

## Examples

```
H <- rawrr::readFileHeader('sample.raw'); json_output <- jsonlite::toJSON(H); write(json_output, 'sample_header.json')
```

## Evaluation signals

- Returned R list object contains non-empty, type-consistent fields for instrument model, file name, time range, and number of scans
- JSON output file is valid JSON and parseable by standard JSON parsers without schema errors
- Metadata values (e.g., number of scans, time range) match independent verification (e.g., rawrr::readIndex() scan count or manual inspection)
- File I/O workflow completes without errors; temporary files are cleaned up and final JSON file is written to specified path
- Returned time range and scan count are consistent with instrument capabilities (e.g., realistic scan counts for 50–60 min LC run; retention times within 0–500 min range)

## Limitations

- readFileHeader() works only on Thermo Fisher Scientific .raw files; does not support other vendor formats
- Metadata extraction relies on the RawFileReader .NET assembly, which must be installed and available on the system; not a pure R implementation
- File I/O workflow (write to disk, read back, parse) introduces latency and temporary disk usage; inefficient for high-throughput batch processing of many files
- Dynamic metadata fields may vary across instrument models and Thermo software versions; no guarantee of consistent field presence or naming across all .raw file versions
- readFileHeader() returns only header-level metadata; does not include spectral or chromatographic data; separate readSpectrum() and readChromatogram() calls required for those

## Evidence

- [other] readFileHeader() reads meta information from a raw file header and returns a list object containing dynamic data items such as instrument model, file name, time range, and number of scans: "reads meta information from a raw file header and returns a list object containing dynamic data items such as instrument model, file name, time range, and number of scans"
- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call"
- [methods] Extracted information is written to temporary location, read back into memory and parsed into R objects: "the extracted information is written to a temporary location on the harddrive, read back into memory and"
- [results] readFileHeader() returns a simple R object of type list: "The respective function is called `readFileHeader()` and returns a simple `R` object of type `list`"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [discussion] provides direct access to spectral data stored in Thermo Fisher Scientific raw-formatted binary files, thereby eliminating the need for unfavorable conversion to exchange formats: "provides direct access to spectral data stored in Thermo Fisher Scientific raw-formatted binary files, thereby eliminating the need for unfavorable conversion to exchange formats"
- [intro] We strongly believe that a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R: "a library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R"
- [results] The example LC-MS run resulted in 24,221 scans over 55 minutes: "The `r H$"Time range"[2]` min run resulted in `r format(H$"Number of scans")` scans"
