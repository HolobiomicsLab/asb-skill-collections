---
name: c-sharp-wrapper-method-validation
description: Use when when integrating an R package that wraps a compiled .NET assembly (such as rawrr), you need to verify that the internal dispatch mechanism between the R layer and the C# layer is operational before attempting to read actual raw data files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0121
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

# C# Wrapper Method Validation

## Summary

Validate that R functions can successfully invoke compiled C# wrapper methods through system calls and retrieve assembly metadata without requiring input data files. This skill confirms the two-layer R/C# architecture is functioning correctly and that the managed .NET assembly is properly dispatched.

## When to use

When integrating an R package that wraps a compiled .NET assembly (such as rawrr), you need to verify that the internal dispatch mechanism between the R layer and the C# layer is operational before attempting to read actual raw data files. Use this skill after package installation or when troubleshooting data access failures.

## When NOT to use

- Input is a raw mass spectrometry data file (.raw) — use readFileHeader() or readSpectrum() instead to access actual spectral data.
- You are testing end-to-end data extraction — this skill only validates the interop layer, not data parsing correctness.
- The .NET assembly has not been installed or bundled with the package — check installation logs first.

## Inputs

- Installed rawrr R package with bundled .NET 8.0 assembly

## Outputs

- Assembly path string (directory containing rawrr.exe)
- Assembly version string
- Confirmation that dispatch mechanism is operational

## How to apply

Load the rawrr package and call its internal assembly dispatch functions: rawrr:::.rawrrAssembly() to retrieve the precompiled .NET assembly path, and rawrr:::.getRawrrAssemblyVersion() to retrieve the version string. Both functions must execute without error and without requiring a raw data file as input. Verify that .rawrrAssembly() returns a non-empty path pointing to a valid directory containing the rawrr.exe executable, and that .getRawrrAssemblyVersion() returns a non-empty version string. This validates the two-layer architecture where R functions invoke C# wrapper methods using system calls to extract information, write it to temporary storage, and read it back into R objects.

## Related tools

- **rawrr** (R package that wraps RawFileReader .NET assembly and provides the dispatch functions being validated) — https://github.com/fgcz/rawrr
- **RawFileReader** (Thermo Fisher Scientific .NET assembly providing compiled C# wrapper methods for reading Orbitrap raw files) — https://github.com/thermofisherlsms/RawFileReader

## Examples

```
rawrr:::.rawrrAssembly(); rawrr:::.getRawrrAssemblyVersion()
```

## Evaluation signals

- rawrr:::.rawrrAssembly() returns a non-empty path string without error
- Returned assembly path points to a valid directory containing rawrr.exe executable
- rawrr:::.getRawrrAssemblyVersion() returns a non-empty version string without error
- Both functions execute successfully without requiring any raw data file as input parameter
- Returned version string follows expected semantic versioning format (e.g., '1.0.0' or similar)

## Limitations

- On Windows systems, the decimal symbol must be configured as '.' for proper data extraction downstream, though this validation step itself is platform-agnostic.
- These internal functions (.rawrrAssembly() and .getRawrrAssemblyVersion()) are undocumented/private API methods (prefixed with .), so their availability or behavior may change across package versions.
- Successful validation of the dispatch mechanism does not guarantee that actual raw data files will be readable; it only confirms the R-to-C# interop layer is operational.

## Evidence

- [other] The rawrr package implements a two-layer architecture where R functions invoke compiled C# wrapper methods using system calls, with extracted information written to temporary storage and read back into R objects for parsing.: "The rawrr package implements a two-layer architecture where R functions invoke compiled C# wrapper methods using system calls, with extracted information written to temporary storage and read back"
- [other] Call rawrr:::.rawrrAssembly() to retrieve the path to the precompiled .NET 8.0 assembly bundled with the package and verify that the returned path points to a valid directory containing the rawrr.exe executable.: "Call rawrr:::.rawrrAssembly() to retrieve the path to the precompiled .NET 8.0 assembly bundled with the package. 3. Verify that the returned path points to a valid directory containing the rawrr.exe"
- [other] Confirm that both functions execute successfully without requiring a raw data file input, demonstrating the internal dispatch mechanism between the R layer and the managed C# assembly layer.: "Confirm that both functions execute successfully without requiring a raw data file input, demonstrating the internal dispatch mechanism between the R layer and the managed C# assembly layer."
- [methods] Specifically, R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call, with extracted information written to temporary locations on harddrive, read back into memory and parsed into R objects.: "Specifically, `R` functions requesting access to data stored in binary raw files invoke compiled `C#` wrapper methods using a system call... the extracted information is written to a temporary"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly, which is a group of assemblies written in C# used to read Thermo Scientific RAW files on Windows, Linux, and MacOS.: "rawrr wraps the functionality of the RawFileReader .NET assembly"
