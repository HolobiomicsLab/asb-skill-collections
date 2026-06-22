---
name: r-data-object-serialization
description: Use when you have mzPeak files (Parquet-based archives containing mass spectrometry spectra and chromatogram data) that you want to analyze in R, and you need to convert the Arrow columnar representation into native R objects that can be passed to downstream analysis functions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - arrow
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- There is also an R implementation in `R/`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzpeak_cq
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_mzpeak_cq
schema_version: 0.2.0
---

# R data object serialization

## Summary

Convert Apache Arrow columnar data structures (Parquet files) into native R data objects (lists or S3 objects) suitable for downstream statistical analysis and visualization. This skill enables read-only access to mzPeak mass spectrometry files by deserializing Arrow-encoded metadata and peak data into R-compatible formats.

## When to use

You have mzPeak files (Parquet-based archives containing mass spectrometry spectra and chromatogram data) that you want to analyze in R, and you need to convert the Arrow columnar representation into native R objects that can be passed to downstream analysis functions (e.g., peak detection, chromatogram visualization, statistical modeling).

## When NOT to use

- Writing or modifying mzPeak files — the R implementation supports read-only access; use the Rust implementation for write operations
- Real-time streaming access to very large archives — Parquet random access is efficient but full deserialization to R objects may exceed memory for multi-gigabyte files
- Analyzing data already in native R format (e.g., MSnbase, xcms objects) — serialization is unnecessary; use format conversion tools instead

## Inputs

- mzPeak archive (ZIP file containing Parquet files: mzpeak_index.json, spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, chromatograms_data.parquet)
- Apache Arrow Parquet schema definition (implicit from mzPeak specification)

## Outputs

- R list or S3 object containing deserialized spectrum metadata (spectrum descriptions, scans, precursors, selected ions)
- R list or S3 object containing deserialized spectrum signal data (m/z and intensity arrays in point or chunked layout)
- R list or S3 object containing deserialized chromatogram metadata and signal data
- Reconstructed m/z arrays for null-marked regions (via delta encoding model or local median spacing)

## How to apply

Load the mzPeak archive (an uncompressed ZIP containing Parquet files) using the Apache Arrow R package. Parse the JSON index file (mzpeak_index.json) to locate the relevant Parquet tables (spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, chromatograms_data.parquet). Read each Parquet file using arrow::read_parquet() or arrow::open_dataset(), then deserialize the packed parallel table structures (struct/group columns containing spectrum descriptions, scans, precursors, and selected ions) into corresponding R list or S3 object hierarchies. Handle null-marked m/z and intensity values by reconstructing missing positions using the stored delta encoding model or local median spacing. Return the fully deserialized object as an R data structure that preserves the hierarchical metadata and allows element-wise access to spectral signals.

## Related tools

- **arrow** (R package for reading Apache Arrow Parquet files and deserializing columnar data structures into R objects) — https://arrow.apache.org/docs/r/
- **R** (Host language for implementing the mzPeak deserialization workflow and downstream analysis)

## Examples

```
library(arrow); idx <- jsonlite::read_json('mzpeak_index.json'); spectra_meta <- read_parquet('spectra_metadata.parquet'); spectra_data <- read_parquet('spectra_data.parquet'); mzpeak_obj <- list(metadata = spectra_meta, signals = spectra_data); str(mzpeak_obj)
```

## Evaluation signals

- Returned R object preserves all fields from the Parquet schema without loss or corruption of metadata or signal data
- Null-marked m/z values are correctly reconstructed using the delta encoding model or local median spacing, with reconstruction error < 1 ppm relative to true m/z
- Spectrum and chromatogram indices are consistent across metadata and data tables (no orphaned or duplicate records)
- S3 object methods (summary, plot, extraction operators) work without error on deserialized data
- Round-trip test: write Parquet → deserialize to R → compare to reference object structure

## Limitations

- Read-only access only — the R implementation does not support writing mzPeak files; write operations require the Rust implementation
- Full object deserialization may exhaust R memory for multi-gigabyte mzPeak archives; consider lazy evaluation or chunked reading for very large files
- Null-marked m/z reconstruction accuracy depends on the fit quality of the stored delta encoding model; highly irregular spacing patterns may produce artifacts
- The mzPeak format is currently a work in progress with no stability guarantee; breaking changes to Parquet schema or JSON metadata structure are possible

## Evidence

- [intro] The R implementation uses the arrow package to read and decode mzPeak files, supporting read-only access: "There is also an R implementation in `R/`, which is also a complete re-implementation using the [`arrow`](https://arrow.apache.org/docs/r/) for _reading_ only"
- [other] Workflow for R deserialization: load file, parse metadata and peak data structures, return as R data structure: "1. Load the mzPeak file using the arrow package in R to read the Apache Arrow columnar format. 2. Parse and decode the mzPeak-specific metadata and peak data structures from the Arrow tables. 3."
- [readme] mzPeak archive contains multiple Parquet files indexed by JSON: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP](<https://en.wikipedia.org/wiki/ZIP_(file_format)>) archive. ... Components of"
- [readme] Packed parallel tables store spectrum and chromatogram metadata with hierarchical structure: "The `spectra_metadata.parquet` and `chromatograms_metadata.parquet` store multiple schemas in parallel. In these Parquet files, the root schema is made up of several branched "group" or "struct""
- [readme] Null-marked m/z reconstruction via delta encoding model: "Then when reading the the null-marked data, use either the local median δ mz or the learned model for that spectrum to compute the m/z spacing for singleton points to achieve an very accurate"
- [readme] R implementation currently supports read-only access, not writing: "The Python codebase does not support writing at this time although this is subject to change in the future. ... There is also an R implementation in `R/`, which is also a complete re-implementation"
