---
name: dotnet-assembly-path-resolution
description: Use when your R package wraps a .NET assembly (e.g., RawFileReader) and you need to (1) report to users or logs which assembly file is actually being used, (2) verify that the assembly exists on disk before attempting to invoke it via system calls, or (3) enable diagnostic output showing the exact.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - RawFileReader
  - rawrr
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

# dotnet-assembly-path-resolution

## Summary

Locate and validate the file path to a cached .NET assembly at runtime, then retrieve and report its version string. This skill enables R packages wrapping compiled C# dependencies to inspect and confirm the presence and identity of the underlying managed code without requiring user-supplied paths.

## When to use

Your R package wraps a .NET assembly (e.g., RawFileReader) and you need to (1) report to users or logs which assembly file is actually being used, (2) verify that the assembly exists on disk before attempting to invoke it via system calls, or (3) enable diagnostic output showing the exact version of the wrapped managed code. Use this skill during package initialization, in diagnostic functions, or before invoking system2() to call the compiled executable.

## When NOT to use

- The .NET assembly is embedded within the R package binary and does not need runtime path resolution.
- You are distributing pre-compiled binaries where the assembly path is baked in at compile time and never changes.
- The wrapped tool does not support a version-query flag or does not return parseable version output.

## Inputs

- Cached assembly path (from rawrr::rawrrAssemblyPath() or similar)
- rawrr executable name or path
- System environment (Windows, Linux, or macOS)

## Outputs

- Normalized file path string to the .NET assembly (character vector)
- Version string of the assembly (character vector, e.g. '1.4.17')
- Logical validation that assembly file exists on disk

## How to apply

Create two internal functions: First, rawrr:::.rawrrAssembly() queries a cached assembly path (via rawrr::rawrrAssemblyPath()) and returns the normalized file path using normalizePath(), validating that the result is a non-empty character vector and the file exists on disk. Second, rawrr:::.getRawrrAssemblyVersion() invokes the rawrr executable with a version-query flag using system2(), pipes the output to a text connection, parses the returned string to extract the version number, and returns it as a character vector. Both functions should fail gracefully with informative errors if the assembly is missing or the version query returns unexpected output. Test that paths normalize correctly across Windows, Linux, and macOS, and that version strings follow a consistent format (e.g., semantic versioning).

## Related tools

- **RawFileReader** (The .NET assembly being wrapped; its path and version are resolved by this skill) — https://github.com/thermofisherlsms/RawFileReader
- **rawrr** (R package that implements this skill via internal functions rawrr:::.rawrrAssembly() and rawrr:::.getRawrrAssemblyVersion()) — https://github.com/fgcz/rawrr

## Examples

```
path <- rawrr:::.rawrrAssembly(); version <- rawrr:::.getRawrrAssemblyVersion(); cat('Assembly:', path, '\nVersion:', version, '\n')
```

## Evaluation signals

- rawrr:::.rawrrAssembly() returns a non-empty character vector matching the pattern of a valid file path (e.g. '/path/to/rawrr.exe' or 'C:\\path\\to\\rawrr.exe').
- file.exists() returns TRUE for the path returned by rawrr:::.rawrrAssembly().
- rawrr:::.getRawrrAssemblyVersion() returns a non-empty character vector containing only alphanumeric characters, dots, and hyphens (consistent with semantic versioning, e.g. '1.4.17').
- Both functions return consistent results across multiple invocations (idempotency).
- Both functions fail with a clear error message if the assembly is missing or the version query produces no parseable output.

## Limitations

- Assembly path caching assumes the compiled .NET executable is installed and stable at a known location; moving or deleting the assembly after installation will cause detection to fail.
- Version extraction depends on consistent output format from the executable's version-query flag; changes to the CLI interface will break parsing.
- Cross-platform path normalization requires testing on Windows, Linux, and macOS; absolute vs. relative path resolution may differ.
- The skill does not validate that the assembly version is compatible with the R package version; only that the assembly and its version string can be read.

## Evidence

- [other] internal functions rawrr:::.rawrrAssembly() to report the .NET assembly path: "The rawrr package provides internal functions rawrr:::.rawrrAssembly() to report the .NET assembly path and rawrr:::.getRawrrAssemblyVersion() to retrieve the assembly version, enabling runtime"
- [other] queries the cached assembly path by invoking rawrr::rawrrAssemblyPath() and returns the normalized file path: "Create the internal function rawrr:::.rawrrAssembly() that queries the cached assembly path by invoking rawrr::rawrrAssemblyPath() and returns the normalized file path to the precompiled .NET"
- [other] invokes the rawrr executable with a version-query flag via system2() and parses the text connection output: "Create the internal function rawrr:::.getRawrrAssemblyVersion() that invokes the rawrr executable with a version-query flag via system2() and parses the text connection output to extract and return"
- [methods] R functions requesting access to data invoke compiled C# wrapper methods using a system call: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call."
- [other] Validate that both functions return non-empty character vectors and that the assembly file path exists on disk: "Validate that both functions return non-empty character vectors and that the assembly file path exists on disk."
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
