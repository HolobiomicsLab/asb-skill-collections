---
name: c-sharp-wrapper-invocation-from-r
description: Use when when you need to read proprietary or binary data formats (e.g.,
  Thermo Fisher .raw files) from R but the native implementation is in .NET/C#, and
  direct language bindings are unavailable or impractical. Use this when the target
  assembly requires Windows/.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - .NET 8.0
  - .NET Framework / .NET 8.0
  - Spectra (Bioconductor)
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime,
  in the `r BiocStyle::Biocpkg('rawrr')` executable file
- The extracted information is written to a temporary location on the harddrive, read
  back into memory and parsed into `R` objects using RawFileReader API
- 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'
- In case you prefer to compile `rawrr.exe` from C# source code, please install the
  .NET 8.0
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

# C# Wrapper Invocation from R

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Invoke compiled C# wrapper methods from R via system calls to access functionality of .NET assemblies (such as the RawFileReader for Thermo Fisher Orbitrap data). This technique enables R to read proprietary binary file formats and extract structured data by delegating to managed code and serializing results back through temporary file I/O.

## When to use

When you need to read proprietary or binary data formats (e.g., Thermo Fisher .raw files) from R but the native implementation is in .NET/C#, and direct language bindings are unavailable or impractical. Use this when the target assembly requires Windows/.NET runtime support and performance is acceptable for file I/O round-trips.

## When NOT to use

- Input data is already in an open format (mzML, mzXML) with existing R parsers available
- .NET runtime or compiled wrapper executable cannot be installed on the target system
- Latency is critical and repeated file I/O round-trips through temporary files is unacceptable

## Inputs

- Thermo Fisher .raw file path (character string)
- Scan ID selection vector (integer or character)
- Filter string specifying scan type/range (e.g., 'FTMS + c NSI Full ms2 487.2567@hcd27.00')
- Query parameters (mass-to-charge ratio, tolerance, chromatogram type)

## Outputs

- Spectral data frames (scan index, m/z, intensity, metadata)
- File header metadata (instrument, scan count, time range)
- Chromatogram data (total ion current or extracted ion chromatogram)
- Raw index with scan type and filter annotations

## How to apply

First, verify that the compiled C# wrapper executable and required .NET runtime (e.g., .NET 8.0) are installed via a dedicated installation function (e.g., rawrr::installRawrrExe()). Second, define R functions that construct command-line invocations matching the wrapper's interface, passing input parameters (file paths, scan IDs, filter strings) as arguments. Third, invoke the wrapper using system2() calls, capturing the command exit status and output. Fourth, write results to a temporary file location from the C# layer and read that serialized output back into R memory using standard R I/O functions. Finally, parse the returned data into native R objects (vectors, data frames, or lists) for downstream analysis. The rationale: this indirect approach avoids tight language coupling while leveraging the RawFileReader .NET assembly's direct access to binary file structures.

## Related tools

- **RawFileReader** (Thermo Fisher .NET assembly providing low-level binary reader API for Orbitrap raw files; invoked indirectly via C# wrapper) — https://github.com/thermofisherlsms/RawFileReader
- **rawrr** (R package wrapping RawFileReader via C# compiled methods; exports readSpectrum(), readFileHeader(), readChromatogram(), readIndex() functions) — https://github.com/fgcz/rawrr
- **.NET Framework / .NET 8.0** (Runtime environment required to execute compiled C# wrapper assemblies)
- **Spectra (Bioconductor)** (Optional downstream R package that can use MsBackendRawFileReader backend powered by rawrr C# wrappers)

## Examples

```
S <- rawrr::readSpectrum(rawfile = "20181113_010_autoQC01.raw", scan = c(1000, 2000, 3000))
```

## Evaluation signals

- C# wrapper executable is present and confirmed accessible via system PATH or absolute path
- .NET runtime version (≥8.0) is installed and functional; verify via dotnet --version or wrapper --version invocation
- readSpectrum() call on 20181113_010_autoQC01.raw returns spectrum object with 119 data items per scan as documented
- Benchmark throughput (spectra per second) output from rawrr:::.benchmark is captured and numerically consistent across multiple runs
- Temporary file output from C# wrapper is valid JSON/CSV/text; parsed R object schema matches documented API (e.g., colnames for spectrum data frames)

## Limitations

- File I/O round-trip via temporary files incurs latency overhead; not suitable for real-time or streaming use cases
- Windows requires decimal symbol to be configured as '.' for proper data extraction; locale settings may cause silent parsing failures
- Dependent on external .NET runtime; deployment requires runtime pre-installation and platform-specific setup
- C# wrapper must be explicitly installed via installRawrrExe(); no automatic fallback if binary is missing or corrupted
- Limited to data structures that can be serialized/deserialized through file I/O; complex nested objects or large matrices may suffer performance degradation

## Evidence

- [methods] invoke compiled C# wrapper methods using a system call: "Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call"
- [methods] write extracted information to temporary location, read back into memory and parse into R objects: "In order to return extracted data back to the `R` layer we use file I/O. More specifically, the extracted information is written to a temporary location on the harddrive, read back into memory and"
- [intro] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [results] readSpectrum provides 119 data items per scan: "In total, the API provides `r length(S[[1]])` data items for this particular scan"
- [other] Installation of RawFileReader executable and .NET 8.0 runtime verification: "Install the rawrr executable and verify .NET 8.0 runtime availability via rawrr::installRawrrExe()"
- [discussion] Decimal symbol configuration requirement on Windows: "On Windows, the decimal symbol has to be configured as a '.'!"
