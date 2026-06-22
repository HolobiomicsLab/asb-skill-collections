---
name: executable-version-string-parsing
description: Use when your R package wraps a compiled .NET assembly or binary executable and you need to expose the version of that dependency to users at runtime for troubleshooting, validation, or documentation purposes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3168
  - http://edamontology.org/topic_0092
  tools:
  - RawFileReader
  - rawrr
  - system2
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
---

# executable-version-string-parsing

## Summary

Parse version strings returned by a compiled executable (invoked via system call) to enable runtime inspection of wrapped binary dependencies. This skill bridges R and external compiled assemblies by extracting version metadata that documents the underlying implementation.

## When to use

Your R package wraps a compiled .NET assembly or binary executable and you need to expose the version of that dependency to users at runtime for troubleshooting, validation, or documentation purposes. Specifically, when the assembly version is not easily queryable from within R and must be retrieved by spawning a subprocess that reports version information as text output.

## When NOT to use

- The wrapped binary already exposes version metadata via an R API or environment variable — use direct API queries instead.
- The assembly version is static and baked into your R package metadata at install time — use DESCRIPTION or package-level constants.
- The underlying executable is not guaranteed to be available or installed on the user's system — version querying will fail; provide a fallback or graceful degradation.

## Inputs

- Compiled .NET assembly or executable (on disk)
- Executable name or path (string)
- Version-query CLI flag or command (string, e.g. '--version')

## Outputs

- Version string (character vector)
- Normalized file path to assembly (character vector)
- Validated assembly metadata (list or named character)

## How to apply

Create an internal R function that invokes the wrapped executable with a version-query flag using system2(), capturing stdout to a text connection. Parse the raw text output using string matching or regular expressions to extract the version string, validate it is non-empty, and return it as a character vector. The article demonstrates this pattern: rawrr:::.getRawrrAssemblyVersion() calls the rawrr executable, captures its version output, and parses the resulting text. Combine this with a path-locating function (e.g., rawrr:::.rawrrAssembly()) that returns the normalized file path to the precompiled executable, allowing users to verify both the location and version of the dependency in a single workflow.

## Related tools

- **RawFileReader** (Compiled .NET assembly being wrapped; version is queried via subprocess invocation) — https://github.com/thermofisherlsms/RawFileReader
- **rawrr** (R package that implements the version-parsing functions and wraps RawFileReader) — https://github.com/fgcz/rawrr
- **system2** (R base function used to invoke the executable and capture text output)

## Examples

```
rawrr:::.getRawrrAssemblyVersion()
```

## Evaluation signals

- rawrr:::.getRawrrAssemblyVersion() returns a non-empty character vector matching semantic versioning pattern (e.g., '2.0.0' or '1.5.123')
- rawrr:::.rawrrAssembly() returns a normalized file path that exists on disk (file.exists() returns TRUE)
- Calling both functions in sequence produces consistent results across multiple invocations (idempotency)
- Text parsing correctly handles whitespace, newlines, and common version prefix patterns (e.g., 'v1.0', 'version 1.0')
- Subprocess call does not hang or raise errors when executable is present and in PATH or explicitly located

## Limitations

- Subprocess invocation is platform-dependent; executable must be in PATH or explicitly located, and system2() behavior may differ on Windows, macOS, and Linux.
- Version string format is fragile: parsing logic must be updated if the executable's version output format changes between releases.
- If the executable is not installed or not found, the function will raise an error; no graceful fallback is provided for missing binaries.
- Temporary file handles and text connections must be properly closed to avoid resource leaks in long-running applications.
- Version metadata reflects only the executable version, not the internal state or schema version of binary data files (e.g., raw files may be newer or older than the reader).

## Evidence

- [other] The rawrr package provides internal functions rawrr:::.rawrrAssembly() to report the .NET assembly path and rawrr:::.getRawrrAssemblyVersion() to retrieve the assembly version, enabling runtime inspection of the wrapped RawFileReader dependency.: "internal functions rawrr:::.rawrrAssembly() to report the .NET assembly path and rawrr:::.getRawrrAssemblyVersion() to retrieve the assembly version, enabling runtime inspection"
- [other] Create the internal function rawrr:::.getRawrrAssemblyVersion() that invokes the rawrr executable with a version-query flag via system2() and parses the text connection output to extract and return the version string.: "invokes the rawrr executable with a version-query flag via system2() and parses the text connection output to extract and return the version string"
- [other] Validate that both functions return non-empty character vectors and that the assembly file path exists on disk.: "Validate that both functions return non-empty character vectors and that the assembly file path exists on disk"
- [methods] R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call.: "R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call"
- [methods] In order to return extracted data back to the R layer we use file I/O. More specifically, the extracted information is written to a temporary location on the harddrive, read back into memory and: "extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects"
