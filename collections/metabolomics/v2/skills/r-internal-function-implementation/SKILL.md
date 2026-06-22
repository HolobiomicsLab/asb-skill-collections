---
name: r-internal-function-implementation
description: Use when you need to expose capabilities of an external compiled dependency (e.g., a .NET assembly, C# wrapper, or executable) to R code, but direct R bindings do not exist.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - RawFileReader
  - rawrr
  - system2()
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

# R Internal Function Implementation

## Summary

Design and implement internal R functions (prefixed with `.`) that wrap external system calls or compiled dependencies, handling I/O serialization, parsing, and error validation to expose lower-level functionality through a stable R interface. This skill is essential when bridging R with .NET assemblies, command-line tools, or compiled libraries that require interprocess communication and result marshalling.

## When to use

You need to expose capabilities of an external compiled dependency (e.g., a .NET assembly, C# wrapper, or executable) to R code, but direct R bindings do not exist. The dependency must be invoked via system calls, and results must be serialized to disk (typically temporary files) and parsed back into R objects. Use this skill when a vendor-provided library (such as RawFileReader) has no native R API and you must design the bridge layer yourself.

## When NOT to use

- A native R package or Bioconductor package already wraps the dependency with a stable API—use the existing package instead.
- The external tool is not reliably installed or may not be available on the user's system—implement graceful fallbacks or dependency checks first.
- The external tool outputs binary data or very large datasets that cannot be efficiently serialized to disk and re-parsed—consider alternative marshalling strategies (e.g., memory-mapped files, direct C/C++ bindings via Rcpp).

## Inputs

- External executable or .NET assembly path (string)
- Query parameters or flags (strings, file paths, numeric ranges)
- Optional: input data files on disk (e.g., .raw files)

## Outputs

- Parsed R object (character vector, list, data frame, or S3/S4 object)
- Validated and schema-conformant result (e.g., version string, file metadata, scan index)

## How to apply

Implement internal functions (marked with `:::` prefix convention) that (1) construct a system call to the external tool or executable using parameters passed from the calling R function; (2) invoke the external process via `system2()`, capturing output to a text connection or temporary file; (3) parse the returned text or file content into R objects (vectors, lists, data frames) using string manipulation or parsing functions; (4) validate that outputs are non-empty and conform to expected schema (e.g., file paths exist, version strings match expected format); (5) return the parsed R object to the caller. The key design decision is whether to write intermediate results to disk (for large data) or capture output in memory (for metadata like version strings). Ground parameter passing in the external tool's own command-line flags and output format specifications.

## Related tools

- **RawFileReader** (External .NET assembly providing spectral data access; invoked via system calls from internal R functions) — https://github.com/thermofisherlsms/RawFileReader
- **rawrr** (R package that uses this skill to wrap RawFileReader .NET assembly; demonstrates system2() calls and output parsing) — https://github.com/fgcz/rawrr
- **system2()** (Base R function used to invoke external executables and capture output to text connections or files)

## Examples

```
.getRawrrAssemblyVersion() # calls system2() to invoke rawrr executable with version flag, parses output, returns semantic version string
```

## Evaluation signals

- The internal function returns a non-empty, typed R object matching the expected schema (e.g., character vector for version, data frame for scan index).
- External file dependencies (assembly paths, temporary files) are validated to exist before or after use; no dangling references or orphaned temp files.
- Parsing logic correctly handles the external tool's output format (e.g., version string extraction from help text, whitespace-delimited fields in tabular output).
- The function fails gracefully with informative error messages when the external tool is missing, returns malformed output, or the input is invalid.
- Round-trip testing: invoking the internal function with known inputs produces expected outputs (e.g., `rawrr:::.getRawrrAssemblyVersion()` returns a valid semantic version string).

## Limitations

- Performance: every call to an internal function triggers a system call, which is slower than in-process computation; batch queries where possible.
- Platform dependency: external executables may not be available on all platforms (Windows, Linux, macOS) or may require separate installation; document prerequisites.
- Parsing fragility: if the external tool changes its output format (e.g., version string format, column order in tabular output), parsing logic must be updated; maintain version-aware parsing if possible.
- Temporary file I/O: serializing large datasets to disk and re-reading introduces latency and temporary storage overhead; consider memory-mapped alternatives for big data.
- Error diagnostics: when the external tool fails silently or produces unexpected output, debugging is harder than native R code; log system call invocations and raw output.

## Evidence

- [other] The rawrr package provides internal functions rawrr:::.rawrrAssembly() to report the .NET assembly path and rawrr:::.getRawrrAssemblyVersion() to retrieve the assembly version: "The rawrr package provides internal functions rawrr:::.rawrrAssembly() to report the .NET assembly path and rawrr:::.getRawrrAssemblyVersion() to retrieve the assembly version"
- [other] Create the internal function rawrr:::.getRawrrAssemblyVersion() that invokes the rawrr executable with a version-query flag via system2() and parses the text connection output to extract and return the version string.: "Create the internal function rawrr:::.getRawrrAssemblyVersion() that invokes the rawrr executable with a version-query flag via system2() and parses the text connection output"
- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call.: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call."
- [methods] Extracted information is written to a temporary location on harddrive, read back into memory and parsed into R objects: "the extracted information is written to a temporary location on the harddrive, read back into memory and"
- [other] Validate that both functions return non-empty character vectors and that the assembly file path exists on disk.: "Validate that both functions return non-empty character vectors and that the assembly file path exists on disk."
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
