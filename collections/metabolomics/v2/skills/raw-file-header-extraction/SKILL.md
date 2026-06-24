---
name: raw-file-header-extraction
description: Use when beginning an LC-MS data analysis pipeline and you need to rapidly
  inspect instrument metadata, acquisition parameters, or scan statistics from proprietary
  Thermo .raw files without the I/O overhead of loading full spectra.
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
  - MsBackendRawFileReader
  - jsonlite
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Calling a wrapper method typically results in the execution of methods defined in
  the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific.
- invoke compiled `C#` wrapper methods using a system call. Calling a wrapper method
  typically results in the execution of methods defined in the `RawFileReader` dynamic
  link library provided by Thermo
- rjson::toJSON
- Calling a wrapper method typically results in the execution of methods defined in
  the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific
- methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher
  Scientific
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_2_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  - build: coll_rawrr_cq
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# raw-file-header-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and deserialize metadata from Thermo Fisher Scientific binary .raw files into R list objects using the readFileHeader() function, retrieving instrument configuration, acquisition time range, and scan counts without loading full spectral data.

## When to use

Apply this skill when beginning an LC-MS data analysis pipeline and you need to rapidly inspect instrument metadata, acquisition parameters, or scan statistics from proprietary Thermo .raw files without the I/O overhead of loading full spectra. Use it as a preliminary diagnostic step before deciding whether to read specific scans or chromatograms, or to construct reproducible analysis summaries that document instrument state and file structure.

## When NOT to use

- Do not use this skill if you need spectral m/z and intensity data—readFileHeader() returns only metadata, not peak lists.
- Do not use this skill if your input is already in an open exchange format (mzML, mzXML, NetCDF)—conversion and header parsing should use format-specific tools.
- Do not use this skill for non-Thermo proprietary formats (e.g., Bruker, Waters, Sciex .raw files)—RawFileReader is specific to Thermo Fisher Scientific instruments.

## Inputs

- Thermo Fisher Scientific .raw file (binary mass spectrometry data file)
- File system path (character string)

## Outputs

- R list object with named fields (instrument model, file name, time range, number of scans)
- JSON serialization of extracted metadata

## How to apply

Call the readFileHeader() function from the rawrr package on a Thermo Fisher .raw file path. The function invokes a compiled C# wrapper via system call to access the binary file header without requiring external conversion tools. The function returns a dynamically-structured R list object containing instrument model, file name, acquisition time range (in minutes), and total number of scans—the exact fields vary by instrument model and control software version. Serialize the returned list to JSON format using rjson::toJSON() for downstream documentation, validation, or integration with external metadata repositories. Verify JSON validity and non-empty structure to confirm successful extraction.

## Related tools

- **rawrr** (R package wrapper around RawFileReader .NET assembly; provides readFileHeader() function and JSON serialization utilities) — https://github.com/fgcz/rawrr
- **RawFileReader** (Thermo Fisher Scientific .NET assembly (C#) that performs low-level binary file parsing and header extraction) — https://github.com/thermofisherlsms/RawFileReader
- **rjson** (R package for JSON serialization of extracted metadata lists)
- **MsBackendRawFileReader** (Integration layer for rawrr into Bioconductor Spectra ecosystem; enables header and spectral data access via unified interface) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
H <- rawrr::readFileHeader('autoQC01.raw'); json_str <- rjson::toJSON(H); writeLines(json_str, 'autoQC01_header.json')
```

## Evaluation signals

- Returned object is an R list (not NULL, not an error); verify with is.list() and length() > 0.
- List contains expected named fields: 'Instrument model', 'File name', 'Time range', 'Number of scans' (fields vary by instrument; check for at least one numeric and one character field).
- JSON serialization is valid JSON syntax; test by parsing with fromJSON() or external JSON validator without parse errors.
- File header extraction completes without system error or warning; rawrr executable is installed and functional (verify via rawrr::installRawrrExe() if needed).
- Time range is numeric and non-negative; number of scans is a positive integer; file name matches the input .raw file basename.

## Limitations

- readFileHeader() returns only static metadata; dynamic scan properties require separate readSpectrum() or readIndex() calls.
- Header structure and available fields are instrument-model and software-version dependent; code must not assume a fixed set of list elements.
- RawFileReader .NET assembly requires Mono or .NET runtime on Linux/macOS; Windows users benefit from native .NET Framework support.
- File I/O overhead exists due to C# wrapper communication via temporary files; for batch processing of many files, consider caching or parallelization.
- readFileHeader() cannot extract data from corrupted or truncated .raw files; error handling should check for file integrity before calling the function.

## Evidence

- [other] readFileHeader() retrieves metadata from binary raw files including instrument model, file name, time range of data acquisition, and number of scans, returning these items as a list object containing dynamically-generated data items that vary by instrument model and control software version.: "readFileHeader() retrieves metadata from binary raw files including instrument model, file name, time range of data acquisition, and number of scans, returning these items as a list object containing"
- [methods] R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call.: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call."
- [methods] The extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects: "the extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects"
- [results] The respective function is called readFileHeader() and returns a simple R object of type list: "The respective function is called readFileHeader() and returns a simple R object of type list"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [results] The C-trap collected 100,000 charges within 2.8 ms, corresponding to only ~5.1% of the maximum injection time of 55 ms: "The C-trap managed to collect the defined 100,000 charges within 2.8 ms, corresponding to only ~5.1% of the maximum injection time of 55 ms"
- [results] The example LC-MS run resulted in 24,221 scans over 55 minutes: "The example LC-MS run resulted in 24,221 scans over 55 minutes"
