---
name: two-layer-architecture-dispatch-testing
description: Use when when you need to verify that a wrapper package (e.g., rawrr) correctly bridges R and a managed .NET assembly (such as RawFileReader), specifically to confirm that internal dispatch functions can retrieve assembly location and version string before attempting actual spectral data extraction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0361
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - RawFileReader
  - rawrr
  - MsBackendRawFileReader
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- The extracted information is written to a temporary location on the harddrive, read back into memory and parsed into `R` objects using RawFileReader API
- 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'
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

# Two-Layer Architecture Dispatch Testing

## Summary

Validate that an R package's internal assembly dispatch mechanism successfully invokes compiled C# wrapper methods and retrieves assembly metadata (path and version) without requiring raw data file input. This tests the R↔.NET interop layer that underpins cross-platform mass spectrometry data access.

## When to use

When you need to verify that a wrapper package (e.g., rawrr) correctly bridges R and a managed .NET assembly (such as RawFileReader), specifically to confirm that internal dispatch functions can retrieve assembly location and version string before attempting actual spectral data extraction. Apply this skill early in integration validation or when troubleshooting assembly loading failures.

## When NOT to use

- When the R package has not yet been installed or loaded into the R environment.
- When testing full end-to-end spectral data extraction; use this skill for architecture validation only, not for functional data extraction tests.
- When the .NET assembly is already known to be missing or corrupt; this skill assumes the assembly exists and is addressable by the package.

## Inputs

- R package namespace (rawrr or equivalent)
- Access to package-bundled .NET assembly

## Outputs

- Assembly directory path (string)
- Assembly version string (non-empty string)
- Validation report (boolean or exception)

## How to apply

Load the R package (e.g., rawrr) and call its internal assembly dispatch functions directly: first invoke rawrr:::.rawrrAssembly() to retrieve the filesystem path to the precompiled .NET 8.0 assembly bundled with the package, then verify the returned path points to an existing directory containing the executable (rawrr.exe). Next, call rawrr:::.getRawrrAssemblyVersion() to fetch the version string of the .NET assembly and confirm a non-empty string is returned. Both calls should execute without requiring a raw data file as input, demonstrating that the R layer can successfully construct system calls to the C# wrapper and parse responses back into R objects. Success indicates the interop mechanism is functional before attempting full spectral data reads.

## Related tools

- **rawrr** (R package providing internal dispatch functions (.rawrrAssembly, .getRawrrAssemblyVersion) and system call abstraction to .NET assembly) — https://github.com/fgcz/rawrr
- **RawFileReader** (Thermo Fisher Scientific .NET assembly (C#) wrapped by rawrr; contains core mass spectrometry data reading logic) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Bioconductor integration layer that validates rawrr dispatch before serving as backend to Spectra package) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
rawrr:::.rawrrAssembly() |> normalizePath(); rawrr:::.getRawrrAssemblyVersion()
```

## Evaluation signals

- rawrr:::.rawrrAssembly() returns a non-empty string matching a valid filesystem path
- Directory at returned path contains the rawrr.exe executable file
- rawrr:::.getRawrrAssemblyVersion() returns a non-empty version string (not NA or empty)
- Both function calls complete without throwing exceptions or requiring raw data file input
- Subsequent calls to higher-level rawrr functions (e.g., readFileHeader) succeed, confirming interop is operationally sound

## Limitations

- Windows systems require decimal symbol configuration as '.' for proper data extraction downstream; this does not affect assembly dispatch but may break subsequent data operations if misconfigured.
- The skill validates only the dispatch mechanism and metadata retrieval; it does not confirm the assembly can actually read spectral data or handle binary raw files.
- Assembly dispatch may succeed but version string parsing could fail if the RawFileReader .NET assembly version format changes unexpectedly.

## Evidence

- [other] invoke rawrr:::.rawrrAssembly() to retrieve the path to the precompiled .NET 8.0 assembly bundled with the package: "Call rawrr:::.rawrrAssembly() to retrieve the path to the precompiled .NET 8.0 assembly bundled with the package."
- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call: "Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call"
- [methods] extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects: "the extracted information is written to a temporary location on the harddrive, read back into memory and"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the [RawFileReader](https://github.com/thermofisherlsms/RawFileReader) [.NET assembly]"
- [other] both functions execute successfully without requiring a raw data file input, demonstrating the internal dispatch mechanism between the R layer and the managed C# assembly layer: "Confirm that both functions execute successfully without requiring a raw data file input, demonstrating the internal dispatch mechanism between the R layer and the managed C# assembly layer."
