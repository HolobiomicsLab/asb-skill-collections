---
name: r-package-installation-and-runtime-verification
description: Use when before running any R function that wraps compiled C# methods or system executables (e.g., rawrr::readSpectrum), especially when the package depends on language runtimes (.NET, Mono) or proprietary third-party assemblies that must be downloaded and configured separately.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3693
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - rawrr
  - RawFileReader
  - .NET 8.0
  - .NET 8.0 runtime
  - MsBackendRawFileReader
  techniques:
  - mass-spectrometry
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# R Package Installation and Runtime Verification

## Summary

Install an R package and verify that all required external dependencies (compiled executables, .NET runtimes, system libraries) are correctly configured before attempting data access operations. This skill ensures that downstream analysis workflows can invoke system-level tools without runtime failures.

## When to use

Before running any R function that wraps compiled C# methods or system executables (e.g., rawrr::readSpectrum), especially when the package depends on language runtimes (.NET, Mono) or proprietary third-party assemblies that must be downloaded and configured separately. Use this skill as a pre-flight check when setting up new proteomics data pipelines on a fresh machine or when switching operating systems (Windows, Linux, macOS).

## When NOT to use

- Package has no external compiled dependencies or system executables (use standard install.packages() only)
- You are in a containerized environment where all dependencies are pre-installed and verified at image build time
- You are only importing the R package for use as a dependency of another package, not calling its data-reading functions directly

## Inputs

- R package source or binary (installable via install.packages() or BiocManager::install())
- Example data file(s) shipped with or referenced by the package (e.g., 20181113_010_autoQC01.raw)
- System runtime availability (e.g., .NET 8.0 SDK or runtime)

## Outputs

- Confirmed R package loaded in memory with all functions available
- Executable binary(ies) downloaded and placed in package library directory
- System runtime confirmed present and compatible
- Verification log or test output confirming successful data read from sample file

## How to apply

Install the R package using standard Bioconductor or CRAN methods. Then invoke the package's explicit installation/verification function (e.g., rawrr::installRawrrExe()) to download and configure external binaries. This function will attempt to install the compiled C# wrapper executable and check for required runtime availability (e.g., .NET 8.0). Capture and inspect the return status and any error messages. Verify that system calls from R can successfully invoke the compiled executable; a common validation is to run a minimal data-reading operation (e.g., readFileHeader on a sample .raw file) and confirm it completes without crashes or missing-assembly errors. On Windows systems, also verify that the decimal symbol is configured as '.' rather than a locale-specific alternative, as this affects parsing of extracted data.

## Related tools

- **rawrr** (R package that wraps RawFileReader .NET assembly and provides readSpectrum, readFileHeader, readChromatogram functions; installRawrrExe() performs verification) — https://github.com/fgcz/rawrr
- **RawFileReader** (Thermo Fisher Scientific .NET assembly that rawrr wraps; must be downloaded and configured as external dependency) — https://github.com/thermofisherlsms/RawFileReader
- **.NET 8.0 runtime** (Required system runtime for executing C# compiled wrapper methods invoked by rawrr via system2 call)
- **MsBackendRawFileReader** (Bioconductor package that serves as an MsBackend for Spectra package, built on rawrr; shares same installation/verification requirements) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
rawrr::installRawrrExe(); rawrr::readFileHeader(rawfile = system.file('extdata', '20181113_010_autoQC01.raw', package = 'rawrr'))
```

## Evaluation signals

- rawrr::installRawrrExe() completes without error and reports executable installed successfully
- System call to compiled C# wrapper executable via system2() returns exit code 0
- rawrr::readFileHeader(rawfile = sample_raw_file) returns a named list with 119 or more data items (e.g., 'Number of scans', 'Time range', etc.)
- rawrr::readSpectrum(rawfile = sample_raw_file, scan = valid_scan_id) returns a list of spectra objects with expected schema (e.g., mz, intensity, retention time fields)
- No warnings or errors related to missing assemblies, incorrect decimal symbol, or incompatible .NET version appear in R console or stderr

## Limitations

- Windows systems require decimal symbol configured as '.' not locale-dependent alternatives; this must be verified separately
- RawFileReader .NET assemblies are proprietary to Thermo Fisher Scientific and must be downloaded from their GitHub repository; license terms may restrict redistribution
- .NET 8.0 runtime must be installed system-wide; rawrr::installRawrrExe() does not automatically install the .NET runtime itself, only the RawFileReader wrapper
- The skill assumes network access to download external binaries during verification; offline environments may fail the check
- Package verification uses the example .raw file provided by tartare ExperimentData package; verification may not catch data-reading failures on real user files with different metadata or scan types

## Evidence

- [other] Install the rawrr executable and verify .NET 8.0 runtime availability via rawrr::installRawrrExe().: "Install the rawrr executable and verify .NET 8.0 runtime availability via rawrr::installRawrrExe()."
- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call: "Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the [RawFileReader](https://github.com/thermofisherlsms/RawFileReader) [.NET assembly]"
- [discussion] On Windows, the decimal symbol has to be configured as a '.'!: "On Windows, the decimal symbol has to be configured as a '.'!"
- [methods] The example file contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF: "The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF"
