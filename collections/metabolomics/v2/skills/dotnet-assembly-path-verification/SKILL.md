---
name: dotnet-assembly-path-verification
description: Use when when you have just loaded the rawrr R package and need to confirm that the bundled .NET 8.0 assembly (rawrr.exe) is present and functional before performing any mass spectrometry data extraction operations.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - RawFileReader
  - rawrr
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dotnet-assembly-path-verification

## Summary

Verify that a .NET assembly bundled with an R package is correctly deployed and accessible by calling internal dispatch functions to retrieve the assembly path and version string without requiring raw data input. This validates the two-layer R/C# architecture before attempting data processing.

## When to use

When you have just loaded the rawrr R package and need to confirm that the bundled .NET 8.0 assembly (rawrr.exe) is present and functional before performing any mass spectrometry data extraction operations. Use this as a diagnostic step if data reading functions fail or return unexpected results.

## When NOT to use

- You have already successfully read spectra or chromatogram data using rawrr::readSpectrum() or rawrr::readChromatogram() — the assembly is already verified to be working.
- Your R environment does not have the rawrr package installed; install the package first before calling internal assembly dispatch functions.

## Inputs

- rawrr R package (loaded in memory)

## Outputs

- Assembly filesystem path (character string)
- Assembly version string (character string)
- Validation status (logical: path exists and version is non-empty)

## How to apply

Call rawrr:::.rawrrAssembly() to retrieve the filesystem path to the precompiled .NET assembly and verify it points to a valid directory containing the rawrr.exe executable. Then call rawrr:::.getRawrrAssemblyVersion() to retrieve the version string of the assembly. Both functions should execute without requiring a raw data file input; if either returns an empty result or an invalid path, the two-layer dispatch mechanism between the R layer and the managed C# assembly layer is broken and data extraction will fail. Document the returned assembly path and version for troubleshooting and reproducibility.

## Related tools

- **rawrr** (R package that wraps RawFileReader .NET assembly and exposes internal dispatch functions (.rawrrAssembly, .getRawrrAssemblyVersion) for assembly path and version verification) — https://github.com/fgcz/rawrr
- **RawFileReader** (Thermo Fisher Scientific .NET assembly for reading proprietary Orbitrap .raw files; bundled within rawrr as a compiled C# wrapper) — https://github.com/thermofisherlsms/RawFileReader

## Examples

```
path <- rawrr:::.rawrrAssembly(); version <- rawrr:::.getRawrrAssemblyVersion(); cat("Assembly:", path, "Version:", version, "\n")
```

## Evaluation signals

- rawrr:::.rawrrAssembly() returns a non-empty, valid filesystem path that resolves to an existing directory
- The returned path contains or points to a rawrr.exe executable file
- rawrr:::.getRawrrAssemblyVersion() returns a non-empty version string matching the expected .NET 8.0 assembly version
- Both functions execute without raising exceptions or warnings about missing assemblies or dispatch failures
- Subsequent calls to rawrr::readFileHeader() or rawrr::readSpectrum() on valid .raw files succeed without assembly-related errors

## Limitations

- On Windows systems, the decimal symbol must be configured as '.' for proper extraction and parsing of assembly metadata; regional locale settings can cause silent failures.
- The internal dispatch functions (.rawrrAssembly, .getRawrrAssemblyVersion) are private R functions (prefixed with '.') and are not guaranteed to remain stable across rawrr package versions.
- This skill only verifies assembly presence and accessibility; it does not validate that the assembly can actually read .raw files or that all RawFileReader dependencies are satisfied.

## Evidence

- [other] Can the rawrr package's internal assembly dispatch functions (rawrr:::.rawrrAssembly() and rawrr:::.getRawrrAssemblyVersion()) successfully retrieve the assembly path and version string without requiring a raw data file as input?: "Can the rawrr package's internal assembly dispatch functions (rawrr:::.rawrrAssembly() and rawrr:::.getRawrrAssemblyVersion()) successfully retrieve the assembly path and version string without"
- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call"
- [other] The rawrr package implements a two-layer architecture where R functions invoke compiled C# wrapper methods using system calls, with extracted information written to temporary storage and read back into R objects for parsing.: "The rawrr package implements a two-layer architecture where R functions invoke compiled C# wrapper methods using system calls, with extracted information written to temporary storage and read back"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [discussion] On Windows, the decimal symbol has to be configured as a '.'!: "On Windows, the decimal symbol has to be configured as a '.'!"
