---
name: file-path-normalization-and-validation
description: Use when when preparing to read Thermo Fisher Scientific .raw files using rawrr functions (readFileHeader, readSpectrum, readChromatogram, readIndex), or when retrieving cached assembly paths for the wrapped RawFileReader dependency.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RawFileReader
  - rawrr
  - tartare
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

# file-path-normalization-and-validation

## Summary

Normalize and validate file paths to binary raw mass spectrometry files before passing them to external executables or APIs. This skill ensures consistent path representation across platforms and verifies file existence, preventing runtime failures when rawrr functions invoke the RawFileReader .NET assembly.

## When to use

When preparing to read Thermo Fisher Scientific .raw files using rawrr functions (readFileHeader, readSpectrum, readChromatogram, readIndex), or when retrieving cached assembly paths for the wrapped RawFileReader dependency. Apply this skill before invoking system calls to the rawrr executable or querying assembly metadata.

## When NOT to use

- Input is already a validated in-memory spectral object (mass spectrum or mass chromatogram) — normalization applies only to file paths, not to R data structures
- Working with exchange format files (mzML, mzXML) converted by ProteoWizard or ThermoRawFileParser — those do not require rawrr assembly path validation
- Performing statistical post-processing of LC-MS data after raw spectra have already been aggregated into feature tables — assembly path validation is irrelevant at downstream analysis stages

## Inputs

- character string: relative or absolute file path to a .raw file
- character string: cached or uncached assembly path reference
- ExperimentHub object or file path reference from tartare package

## Outputs

- character vector: normalized absolute file path to .raw file
- character vector: normalized absolute file path to RawFileReader .NET assembly
- logical: TRUE if file exists and is accessible, FALSE otherwise

## How to apply

Invoke normalizePath() on the input file path to standardize path separators and resolve relative or symbolic references into absolute canonical form. Pass the normalized path to the data-reading function or system call. For assembly paths, call rawrr:::.rawrrAssembly() which internally queries rawrr::rawrrAssemblyPath() and returns the normalized file path to the precompiled .NET executable. Validate that the returned path is a non-empty character vector and that the file exists on disk using file.exists(). This normalization ensures consistent behavior across Windows, Linux, and macOS file system conventions and prevents path-related failures when invoking C# wrapper methods via system calls.

## Related tools

- **rawrr** (R package that wraps RawFileReader .NET assembly; provides internal functions to retrieve and normalize assembly paths) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly whose path must be normalized and validated before invoking via system calls from rawrr) — https://github.com/thermofisherlsms/RawFileReader
- **tartare** (ExperimentData package providing test .raw files; file paths from this source require normalization before use)

## Examples

```
rawrr_path <- normalizePath(system.file('extdata', 'sample.raw', package='tartare')); if (file.exists(rawrr_path)) { H <- rawrr::readFileHeader(rawrr_path) }
```

## Evaluation signals

- Returned path is a non-empty character vector of length ≥ 1
- file.exists() returns TRUE for the normalized path on the current platform
- Path uses forward slashes (/) or appropriate platform-specific separators consistently
- Subsequent readFileHeader(), readSpectrum(), or readChromatogram() calls complete without path-related errors
- Assembly version retrieval via rawrr:::.getRawrrAssemblyVersion() succeeds and returns a non-empty version string

## Limitations

- normalizePath() requires the file to exist before normalization; pre-flight file existence checks should precede path normalization
- Assembly path caching assumes rawrr::rawrrAssemblyPath() has already been called during package initialization; if assembly installation has failed, path retrieval will return an empty or invalid path
- Cross-platform path handling relies on R's native normalizePath() function; unusual mount points, network shares, or permission-restricted paths may not normalize as expected
- The rawrr executable must be installed via rawrr::installRawrrExe() before assembly path queries will succeed; the skill assumes successful prior installation

## Evidence

- [other] Validate that both functions return non-empty character vectors and that the assembly file path exists on disk.: "Validate that both functions return non-empty character vectors and that the assembly file path exists on disk."
- [other] The rawrr package provides internal functions rawrr:::.rawrrAssembly() to report the .NET assembly path: "The rawrr package provides internal functions rawrr:::.rawrrAssembly() to report the .NET assembly path and rawrr:::.getRawrrAssemblyVersion() to retrieve the assembly version"
- [other] Create the internal function rawrr:::.rawrrAssembly() that queries the cached assembly path by invoking rawrr::rawrrAssemblyPath() and returns the normalized file path to the precompiled .NET executable.: "Create the internal function rawrr:::.rawrrAssembly() that queries the cached assembly path by invoking rawrr::rawrrAssemblyPath() and returns the normalized file path to the precompiled .NET"
- [methods] R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call.: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call."
- [methods] the extracted information is written to a temporary location on the harddrive, read back into memory: "the extracted information is written to a temporary location on the harddrive, read back into memory and parsed into R objects"
