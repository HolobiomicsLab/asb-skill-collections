---
name: assembly-version-string-retrieval
description: Use when when you need to validate that a .NET assembly (such as ThermoFisher.CommonCore.RawFileReader) is correctly installed and accessible before attempting data reading operations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - RawFileReader
  - rawrr
derived_from:
- doi: 10.1021/acs.jproteome.0c00866
  title: rawrr
evidence_spans:
- The extracted information is written to a temporary location on the harddrive, read back into memory and parsed into `R` objects using RawFileReader API
- 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr
    doi: 10.1021/acs.jproteome.0c00866
    title: rawrr
  dedup_kept_from: coll_rawrr
schema_version: 0.2.0
---

# assembly-version-string-retrieval

## Summary

Retrieve the version string and file path of a precompiled .NET assembly bundled with an R package without requiring input data files. This skill verifies that internal R-to-C# dispatch mechanisms are functioning correctly and that managed code dependencies are properly deployed.

## When to use

When you need to validate that a .NET assembly (such as ThermoFisher.CommonCore.RawFileReader) is correctly installed and accessible before attempting data reading operations. Use this skill as a diagnostic check at the start of any workflow that relies on managed code interop, especially when troubleshooting failures in downstream functions like readSpectrum() or readFileHeader().

## When NOT to use

- Input is already a feature table or processed spectrum object; use this skill only to verify assembly availability, not to extract or transform spectral data.
- You have confirmed via system PATH or environment variables that the assembly is correctly deployed; this skill is a diagnostic, not a recovery mechanism.

## Inputs

- rawrr R package (installed and loaded)
- No raw data file required

## Outputs

- Assembly file path (string pointing to rawrr.exe directory)
- Assembly version string (non-empty semantic version)
- Validation status (success/failure of interop call)

## How to apply

Call the internal R package functions that expose assembly metadata without requiring raw data file inputs. In rawrr, invoke rawrr:::.rawrrAssembly() to obtain the filesystem path to the bundled .NET 8.0 executable, and rawrr:::.getRawrrAssemblyVersion() to retrieve the assembly version string. Verify that the returned path points to a valid directory containing the rawrr.exe executable, and confirm that the version string is non-empty and matches expected release tags. Both calls should execute successfully via the R-layer-to-C#-wrapper system call mechanism without errors, demonstrating that the two-layer architecture (R functions invoking compiled C# methods via system calls, with results written to temporary storage and read back) is operational.

## Related tools

- **rawrr** (R package wrapping RawFileReader .NET assembly; provides internal functions rawrr:::.rawrrAssembly() and rawrr:::.getRawrrAssemblyVersion() for assembly path and version retrieval) — https://github.com/fgcz/rawrr
- **RawFileReader** (Thermo Fisher Scientific .NET assembly read from by rawrr; version and path must be verified before invoking its wrapped functions) — https://github.com/thermofisherlsms/RawFileReader

## Examples

```
rawrr:::.rawrrAssembly(); rawrr:::.getRawrrAssemblyVersion()
```

## Evaluation signals

- rawrr:::.rawrrAssembly() returns a non-null, non-empty character string pointing to an existing directory
- Directory returned by .rawrrAssembly() contains a valid rawrr.exe executable file with accessible read permissions
- rawrr:::.getRawrrAssemblyVersion() returns a non-empty version string matching semantic versioning format (e.g., '1.0.0')
- Both function calls complete without R errors or system-level exceptions related to interop or file I/O
- Version string is consistent across repeated calls and matches the declared version in the installed package DESCRIPTION file

## Limitations

- This skill only validates assembly availability and basic metadata; it does not verify that the assembly can successfully read actual .raw files or that all wrapped C# methods are functional.
- On Windows systems, the decimal symbol must be configured as '.' for proper data extraction in downstream operations; this skill does not enforce or validate that configuration.
- The skill assumes the rawrr package is already installed and loaded into the R environment; it cannot diagnose installation failures or missing system dependencies (e.g., .NET 8.0 runtime).

## Evidence

- [other] Can the rawrr package's internal assembly dispatch functions (rawrr:::.rawrrAssembly() and rawrr:::.getRawrrAssemblyVersion()) successfully retrieve the assembly path and version string without requiring a raw data file as input?: "Can the rawrr package's internal assembly dispatch functions (rawrr:::.rawrrAssembly() and rawrr:::.getRawrrAssemblyVersion()) successfully retrieve the assembly path and version string without"
- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call: "R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call"
- [methods] the extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects: "the extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [other] Confirm that both functions execute successfully without requiring a raw data file input, demonstrating the internal dispatch mechanism between the R layer and the managed C# assembly layer.: "Confirm that both functions execute successfully without requiring a raw data file input, demonstrating the internal dispatch mechanism between the R layer and the managed C# assembly layer."
