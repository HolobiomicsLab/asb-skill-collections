---
name: mass-spectrometry-scan-indexing
description: Use when you have a Thermo Fisher Scientific .raw file and need to (1) enumerate all scans and their metadata, (2) identify which scans are MS1 vs. MSn to enable level-specific filtering, (3) retrieve scan ranges or specific scan numbers for targeted spectral extraction, or (4) plan.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - R
  - RawFileReader
  - MsBackendRawFileReader
  - Spectra
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- The `rawrr` executable will run out of the box
- '`R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods'
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

# mass-spectrometry-scan-indexing

## Summary

Generate a tabular index of all scans in a Thermo Fisher Scientific raw file, enabling programmatic filtering and selective extraction of spectral data by MS level, scan type, or scan number. This foundational operation bridges raw binary data and downstream analysis by providing scan metadata (retention time, MS level, scan type) without loading all spectral arrays into memory.

## When to use

You have a Thermo Fisher Scientific .raw file and need to (1) enumerate all scans and their metadata, (2) identify which scans are MS1 vs. MSn to enable level-specific filtering, (3) retrieve scan ranges or specific scan numbers for targeted spectral extraction, or (4) plan memory-efficient access to large LC-MS runs by iterating over a lightweight index rather than loading the entire file.

## When NOT to use

- Input is already a scan index or feature table—re-indexing wastes I/O and computation.
- You have already converted the raw file to an exchange format (mzML, mzXML) and loaded it via ProteoWizard or ThermoRawFileParser; use existing in-memory indices instead.
- Your analysis requires only aggregate statistics (e.g., total scan count, retention time range) without individual scan metadata—use readFileHeader() to query file-level properties more efficiently.

## Inputs

- Thermo Fisher Scientific .raw file (binary proprietary format)
- File path to raw file (character string)

## Outputs

- data.frame with scan index (columns: scan number, ms_level, scan_type, retention_time, and other metadata)
- Subset index data.frame (after filtering by MS level, scan type, or other criteria)

## How to apply

Use the rawrr::readIndex() function to generate a data.frame that indexes all scans in the raw file, returning columns such as scan number, MS level (ms_level), scan type, and retention time. Subset this index by logical conditions—e.g., ms_level==1 to retain only MS1-level scans, or scan type matching a specific experiment (e.g., 'FTMS + c NSI Full ms2 487.2567@hcd27.00' for PRM)—to identify the scan numbers of interest. This filtered index then serves as input to iterative readSpectrum() calls or as metadata for downstream analyses. The rationale is that the index is lightweight and fast to generate, allowing you to make filtering decisions before invoking expensive spectral reading operations on binary data via the RawFileReader .NET assembly.

## Related tools

- **rawrr** (Primary R package providing readIndex() function to generate scan indices from Thermo raw files; wraps RawFileReader .NET assembly) — https://github.com/fgcz/rawrr
- **RawFileReader** (Vendor-provided .NET assembly (Thermo Fisher Scientific) that rawrr invokes via system calls to parse binary raw file structure and extract metadata) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Alternative Bioconductor backend integrating rawrr into the Spectra ecosystem; builds on scan indexing for on-disk spectral access) — https://github.com/fgcz/MsBackendRawFileReader
- **Spectra** (Bioconductor package defining MsBackend interface; uses scan indices from MsBackendRawFileReader to enable lazy-loading and filtering of spectral data)

## Examples

```
index <- readIndex("20181113_010_autoQC01.raw"); ms1_index <- subset(index, ms_level == 1); head(ms1_index)
```

## Evaluation signals

- The returned data.frame contains exactly one row per scan in the raw file, with no missing or duplicate scan numbers.
- Filtering by ms_level==1 returns a subset of rows consistent with the raw file's acquisition protocol (e.g., expected ratio of MS1 to MS2 scans in a data-dependent acquisition experiment).
- Retention time values are monotonically increasing (or non-decreasing) across rows, reflecting the temporal order of scans during the LC run.
- When passed to readSpectrum() with scan numbers from the index, spectral arrays are successfully retrieved and match the ms_level and scan_type metadata recorded in the index.
- Index generation completes in seconds to minutes even for large files (e.g., 24,221 scans over 55 minutes), confirming the lightweight nature of metadata-only indexing.

## Limitations

- Indexing requires the RawFileReader .NET assembly to be installed (via rawrr::installRawrrExe()) and is platform-dependent; while supported on Windows, Linux, and macOS via Mono/.NET Core, performance and compatibility may vary.
- The index is a static snapshot of the raw file at the time of readIndex() invocation; if the raw file is being actively written by an instrument, index contents will not reflect in-flight scans.
- Index generation incurs I/O and system-call overhead; for repeated analyses on the same raw file, caching the index result (e.g., serializing to RDS) is recommended to avoid redundant parsing.
- Filter steps are applied in-memory on the data.frame after indexing; very large indices (millions of scans) may require chunked or external filtering to manage memory overhead.

## Evidence

- [results] Generate scan index using readIndex(): "By using the `readIndex()` function a `data.frame` that indexes all scans found in a raw file is returned"
- [results] Filter MS scans using ms level: "using only MS1-level scans"
- [results] Specific scan type filtering for targeted experiments: "subset(scanType == "FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]")"
- [intro] rawrr wraps RawFileReader .NET assembly for binary access: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [discussion] Direct raw file access eliminates conversion step: "provides direct access to spectral data stored in Thermo Fisher Scientific raw-formatted binary files, thereby eliminating the need for unfavorable conversion to exchange formats"
- [other] Workflow for scan extraction and aggregation: "Generate a scan index using readIndex() to retrieve all scans. Filter the index to retain only MS1-level scans by subsetting on ms_level==1. Iterate through filtered scans and call readSpectrum() on"
- [results] Example LC-MS run scale: "The `r H$"Time range"[2]` min run resulted in `r format(H$"Number of scans")` scans"
- [methods] Lightweight indexing approach: "`R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call."
