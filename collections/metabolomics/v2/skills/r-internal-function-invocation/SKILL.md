---
name: r-internal-function-invocation
description: Use when when you need to verify or retrieve package-internal metadata
  about compiled .NET assembly location and version before processing raw mass spectrometry
  files, or when testing the R↔C# dispatch mechanism in isolation without loading
  actual Orbitrap .raw data files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RawFileReader
  - rawrr
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- The extracted information is written to a temporary location on the harddrive, read
  back into memory and parsed into `R` objects using RawFileReader API
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

# R Internal Function Invocation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Invoke unexported R package internal functions (prefixed with :::) to access low-level assembly dispatch and configuration metadata without requiring raw data file inputs. This skill enables direct querying of bundled .NET assembly paths and version information in the rawrr package's two-layer R/C# architecture.

## When to use

When you need to verify or retrieve package-internal metadata about compiled .NET assembly location and version before processing raw mass spectrometry files, or when testing the R↔C# dispatch mechanism in isolation without loading actual Orbitrap .raw data files.

## When NOT to use

- The rawrr package is not installed or not loaded in the R session.
- You need to read actual spectral or chromatographic data from .raw files (use exported functions like readSpectrum(), readChromatogram(), readFileHeader() instead).
- You are working with a different R proteomics package that does not use internal ::: functions for assembly dispatch.

## Inputs

- rawrr R package (loaded in R session)

## Outputs

- assembly directory path (character string pointing to .NET assembly location)
- assembly version string (character string with version metadata)

## How to apply

Use the ::: operator to call internal (non-exported) functions from the rawrr package: (1) invoke rawrr:::.rawrrAssembly() to retrieve the filesystem path to the precompiled .NET 8.0 assembly bundled with the package; (2) verify the returned path points to a valid directory containing the rawrr.exe executable; (3) invoke rawrr:::.getRawrrAssemblyVersion() to retrieve the version string of the .NET assembly; (4) verify a non-empty version string is returned. Both functions execute without requiring raw data file input, confirming successful internal dispatch between the R layer and managed C# layer. This demonstrates the two-layer architecture where R functions invoke compiled C# wrapper methods.

## Related tools

- **rawrr** (R package providing the internal functions .rawrrAssembly() and .getRawrrAssemblyVersion() for assembly path and version retrieval) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly wrapped by rawrr; contains the compiled C# code invoked through the two-layer architecture) — https://github.com/thermofisherlsms/RawFileReader

## Examples

```
rawrr:::.rawrrAssembly(); rawrr:::.getRawrrAssemblyVersion()
```

## Evaluation signals

- rawrr:::.rawrrAssembly() returns a non-empty character string pointing to an existing filesystem directory.
- The returned assembly path contains a rawrr.exe executable file readable by the R process.
- rawrr:::.getRawrrAssemblyVersion() returns a non-empty version string matching semantic versioning format (e.g., '1.0.0').
- Both function calls execute without raising errors or warnings, indicating the R↔C# dispatch mechanism is functional.
- The returned assembly version string is consistent across repeated invocations in the same R session.

## Limitations

- Internal functions (:::) are not part of the public API and may change between package versions without deprecation warnings.
- On Windows systems, the decimal symbol must be configured as '.' for proper data extraction in downstream operations, though this affects the broader package rather than internal function invocation alone.
- These internal functions do not provide access to actual spectral or chromatographic data; they only return metadata about the assembly itself.

## Evidence

- [methods] R functions invoke compiled C# wrapper methods using a system call: "Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call"
- [other] Assembly dispatch without raw data file input: "Can the rawrr package's internal assembly dispatch functions (rawrr:::.rawrrAssembly() and rawrr:::.getRawrrAssemblyVersion()) successfully retrieve the assembly path and version string without"
- [methods] Two-layer architecture with extracted information written to temporary storage: "In order to return extracted data back to the `R` layer we use file I/O. More specifically, the extracted information is written to a temporary location on the harddrive, read back into memory and"
- [readme] rawrr wraps RawFileReader .NET assembly functionality: "rawrr wraps the functionality of the [RawFileReader](https://github.com/thermofisherlsms/RawFileReader) [.NET assembly](https://www.mono-project.com/docs/advanced/assemblies-and-the-gac/)."
