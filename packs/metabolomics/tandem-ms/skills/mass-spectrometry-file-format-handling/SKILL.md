---
name: mass-spectrometry-file-format-handling
description: Use when when you have Thermo Fisher Scientific Orbitrap .raw files (e.g., from Q Exactive HF instruments) and need to extract spectral, chromatographic, or metadata directly into R for downstream statistical analysis, benchmarking, or integration with Bioconductor workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - rawrr
  - RawFileReader
  - .NET 8.0
  - MsBackendRawFileReader
  - .NET 8.0 runtime
  - Bioconductor Spectra
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime, in the `r BiocStyle::Biocpkg('rawrr')` executable file
- The extracted information is written to a temporary location on the harddrive, read back into memory and parsed into `R` objects using RawFileReader API
- 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'
- In case you prefer to compile `rawrr.exe` from C# source code, please install the .NET 8.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr
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

# Mass Spectrometry File Format Handling

## Summary

Direct programmatic access to proprietary Thermo Fisher Scientific .raw files (Orbitrap FTMS data) via the rawrr R package wrapping the RawFileReader .NET assembly. This skill enables end-to-end raw data reading in R without requiring GUI-based software, supporting modular proteomics pipelines.

## When to use

When you have Thermo Fisher Scientific Orbitrap .raw files (e.g., from Q Exactive HF instruments) and need to extract spectral, chromatographic, or metadata directly into R for downstream statistical analysis, benchmarking, or integration with Bioconductor workflows. Particularly useful when automated, reproducible access to raw instrument data is required rather than relying on proprietary software exports.

## When NOT to use

- Input is already converted to mzML, mzXML, or other open formats—use mzR or MS Data Import for those instead.
- You need write access or format conversion to other MS file types—rawrr is read-only and Thermo-specific.
- System lacks .NET 8.0 runtime or does not support RawFileReader on your OS (Windows, Linux, macOS support exists but .NET prerequisites vary).
- Real-time or streaming analysis of actively-acquiring instrument data—rawrr works on static .raw files only.

## Inputs

- Thermo Fisher Scientific .raw file (binary Orbitrap FTMS data)
- File path (character string) to .raw file
- Scan IDs or scan number ranges (integer vector, optional)
- Filter string specifying scan type or mass range (character, optional)
- Mass tolerance for XIC extraction (numeric, ppm, optional)

## Outputs

- File header metadata (list: run time, scan count, instrument info, acquisition settings)
- Spectrum object (data frame: m/z, intensity, scan metadata for selected scans)
- Chromatogram object (rawrrChromatogram: retention time, intensity traces, TIC or XIC)
- Scan index (data frame: all scans with type, filter string, and metadata)
- Parsed R objects (data frames, lists, or S4 objects compatible with Bioconductor Spectra)

## How to apply

Install the rawrr package and RawFileReader executable (via rawrr::installRawrrExe()), verify .NET 8.0 runtime availability on your system, then invoke reader functions (readFileHeader, readSpectrum, readChromatogram, readIndex) with the path to your .raw file. These functions invoke compiled C# wrapper methods via system2 calls to interact with the RawFileReader .NET assembly. Extracted data is written to a temporary location, read back into memory, and parsed into R objects (data frames, lists, or rawrrChromatogram objects). For filtered access, supply filter strings matching scan type (e.g., 'FTMS + c NSI Full ms2') or mass tolerance windows (e.g., tol = 10 ppm for XIC extraction). Validate output by checking data dimensionality, scan count, m/z ranges, and retention time linearity (R² > 0.99 indicates well-behaved data).

## Related tools

- **rawrr** (Primary R package wrapping RawFileReader; exports reader functions (readFileHeader, readSpectrum, readChromatogram, readIndex) and benchmark utilities) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly (C# compiled) that performs actual binary .raw file parsing; invoked via system2 calls from R) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Bioconductor backend adapter integrating rawrr with the Spectra package for on-disk spectrum access) — https://github.com/cpanse/MsBackendRawFileReader
- **.NET 8.0 runtime** (System dependency required to execute RawFileReader compiled assemblies)
- **Bioconductor Spectra** (Optional downstream consumer of rawrr-extracted data; rawrr serves as alternative MsBackend) — https://bioconductor.org/packages/Spectra/

## Examples

```
library(rawrr); H <- rawrr::readFileHeader('20181113_010_autoQC01.raw'); S <- rawrr::readSpectrum('20181113_010_autoQC01.raw', scan=c(1000,2000,5000)); C <- rawrr::readChromatogram('20181113_010_autoQC01.raw', type='tic')
```

## Evaluation signals

- Returned file header includes expected metadata fields (run time > 0, scan count ≥ 1, instrument model matches input file).
- Spectrum objects have matching m/z and intensity vector lengths with m/z sorted in ascending order and intensity ≥ 0.
- Retention time extraction from chromatograms shows linear behavior (linear regression R² > 0.99) when plotted against scan index.
- Scan index output has one row per scan with consistent filter strings matching declared MS level (e.g., 'ms' for MS1, 'ms2' for MS2).
- Round-trip test: readFileHeader() run time and readIndex() scan count match the file's internal metadata without gaps or duplicates.

## Limitations

- Windows systems require decimal symbol configured as '.' for proper numeric extraction.
- MsBackendRawFileReader integration is work-in-progress (WIP status); not yet a stable, public release.
- Read-only access—no export or format conversion functions provided.
- Requires .NET 8.0 runtime installation; dependency management can be complex across Linux/macOS.
- Performance scales with number of scans requested; benchmarking throughput (spectra/second) depends on scan complexity and temporary I/O.
- File I/O strategy (write to temp, read back, parse) may be slow for very large .raw files (>6 million scans).

## Evidence

- [intro] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [methods] Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call: "invoke compiled `C#` wrapper methods using a system call"
- [methods] extracted information is written to a temporary location on the harddrive, read back into memory and: "extracted information is written to a temporary location on the harddrive, read back into memory and"
- [methods] The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF: "Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF"
- [intro] The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package: "access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as MsRawFileReaderBackend for the Bioconductor Spectra package"
- [intro] Existing R libraries for proteomics mainly support high-level statistical analysis of preprocessed data rather than raw data reading: "mainly support high-level statistical analysis once the raw measurement data has"
- [discussion] On Windows, the decimal symbol has to be configured as a '.'!: "On Windows, the decimal symbol has to be configured as a '.'"
- [readme] RawFilelReader is a group of .Net Assemblies written in C# used to read Thermo Scientific RAW files. The assemblies can be used to read RAW files on Windows, Linux, and MacOS: "read RAW files on Windows, Linux, and MacOS using C# or other languages that can acces a .Net assembly"
