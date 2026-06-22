---
name: system-call-invocation-via-system2
description: Use when you need to query or extract data from Thermo Fisher Scientific .raw files or other proprietary binary formats accessible only through a compiled external executable (e.g., RawFileReader .NET assembly). The executable returns text or structured output (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - RawFileReader
  - rawrr
  - rawDiag
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# system-call-invocation-via-system2

## Summary

Invoke external compiled executables (e.g., .NET assemblies, C# wrappers) from R using the system2() function, capture their output via text connections, and parse results back into R objects. This is essential for accessing binary file formats and vendor-supplied APIs that lack native R bindings.

## When to use

You need to query or extract data from Thermo Fisher Scientific .raw files or other proprietary binary formats accessible only through a compiled external executable (e.g., RawFileReader .NET assembly). The executable returns text or structured output (e.g., CSV, JSON) that must be parsed into R data structures for downstream analysis.

## When NOT to use

- The desired functionality is already available as an R package or native function—use those instead to avoid subprocess overhead and platform-specific failures.
- The input file format is already supported by standard R libraries (e.g., mzML via MSnbase, or CSV via read.csv)—conversion to exchange formats or native R I/O is more robust.
- The executable is not reliably installed or its path is unknown—verify executable availability and register its path before invoking system2().

## Inputs

- executable path (character string)
- command-line arguments (character vector)
- raw binary file or resource identifier accessible to the external executable

## Outputs

- parsed R object (character vector, numeric vector, data.frame, or list)
- version string (e.g., assembly version number)
- structured data extracted from executable output

## How to apply

1. Identify the target external executable and its command-line interface (e.g., rawrr executable with version-query flag, or RawFileReader wrapper). 2. Use system2(command, args=c(...), stdout=TRUE) to invoke the executable with appropriate arguments, capturing output to a text connection. 3. Parse the returned text string using R's text parsing functions (e.g., read.csv(text=...), strsplit(), grep(), or regex extraction) to convert raw command output into typed R objects (numeric, character, data.frame, list). 4. Validate that the parsed result is non-empty and conforms to the expected schema before returning to the caller. 5. Handle file I/O overhead by reading temporary results from disk if the executable writes to a file rather than stdout.

## Related tools

- **RawFileReader** (External .NET assembly wrapping vendor-supplied Thermo Fisher API; invoked via system2() from R to read spectral data from proprietary .raw files) — https://github.com/thermofisherlsms/RawFileReader
- **rawrr** (R package that wraps RawFileReader and uses system2() to invoke the compiled executable; provides high-level R functions that internally call system2()) — https://github.com/fgcz/rawrr
- **rawDiag** (R package for LC-MS method optimization that also uses RawFileReader for fast multiplatform access to raw instrument data) — https://github.com/fgcz/rawDiag

## Examples

```
rawrr:::.getRawrrAssemblyVersion()
```

## Evaluation signals

- system2() call executes without error and returns exit code 0
- Parsed output is non-empty and matches the expected R class (character, numeric, data.frame, etc.)
- Returned values conform to expected schema (e.g., version string is non-empty; data.frame has expected column names and row count)
- File path or resource identifier passed to the executable is valid and accessible on the file system
- Temporary files created during file I/O round-trips are cleaned up and do not accumulate on disk

## Limitations

- system2() introduces subprocess overhead and cross-platform variability; command syntax may differ on Windows vs. Unix-like systems.
- The external executable must be installed and registered at a known path; missing or incompatible versions will cause silent or cryptic failures.
- Parsing logic is tightly coupled to the executable's output format; changes in executable version or output structure require rewriting the parser.
- Large outputs (e.g., thousands of spectra) require file I/O round-trips via temporary disk storage, which is slower than native R vectorized operations.
- Error handling is limited; subprocess failures may not produce informative R error messages.

## Evidence

- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call.: "R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call."
- [methods] The extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects: "the extracted information is written to a temporary location on the harddrive, read back into memory and [parsed into R objects]"
- [other] rawrr provides internal functions to query the cached assembly path and retrieve the assembly version by invoking the executable with a version-query flag: "rawrr:::.getRawrrAssemblyVersion() that invokes the rawrr executable with a version-query flag via system2() and parses the text connection output to extract and return the version string"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [readme] RawFileReader is a group of .Net Assemblies written in C# used to read Thermo Scientific RAW files on Windows, Linux, and MacOS: "RawFilelReader is a group of .Net Assemblies written in C# used to read Thermo Scientific RAW files.  The assemblies can be used to read RAW files on Windows, Linux, and MacOS"
