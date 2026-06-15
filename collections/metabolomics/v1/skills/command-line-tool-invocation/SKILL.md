---
name: command-line-tool-invocation
description: Use when you have an existing mass spectrometry data file in a vendor or standard format (mzML, NetCDF, etc.) and need to convert it to mzPeak format for downstream analysis, visualization, or archival.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - OpenMS
  - Rust (cargo)
  - mzpeak_prototyping
  - Apache Parquet
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzpeak
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_mzpeak
schema_version: 0.2.0
---

# command-line-tool-invocation

## Summary

Invoke a compiled command-line tool to convert mass spectrometry data from one format (e.g., mzML) to another (e.g., mzPeak binary). This skill bridges file format interoperability by executing a pre-built converter executable with specified input and output paths.

## When to use

You have an existing mass spectrometry data file in a vendor or standard format (mzML, NetCDF, etc.) and need to convert it to mzPeak format for downstream analysis, visualization, or archival. The source format is supported by the converter tool's input pipeline, and you have local filesystem access to both the source data and the destination directory.

## When NOT to use

- Input file format is not supported by the converter (e.g., a proprietary binary format without a documented parser in the mzpeak_prototyping repository).
- Output mzPeak format is not required; the source format already meets your analysis requirements.
- You only need to read mzPeak files; use the Python (pyarrow-based) or R (arrow-based) read-only implementations instead.

## Inputs

- mzML file (XML-based mass spectrometry data format)
- NetCDF file or other vendor-supported mass spectrometry format
- File path to source mass spectrometry data

## Outputs

- mzPeak archive (ZIP file containing Parquet tables and JSON index)
- spectra_metadata.parquet (spectrum-level metadata and file-level metadata)
- spectra_data.parquet (spectrum signal data in point or chunked layout)
- mzpeak_index.json (archive file definition)
- spectra_peaks.parquet (optional; explicit centroids separate from signal)

## How to apply

First, clone or obtain the mzpeak_prototyping repository from the reference source and build the Rust command-line tools using `cargo build`. Execute the converter with the source mzML (or other supported format) file as the primary input argument and specify the desired mzPeak output file path as the destination. The tool will parse the input format, apply zero-run stripping and optional null-marking compression for profile data, and write the result as an uncompressed ZIP archive containing Parquet tables (spectra_metadata.parquet, spectra_data.parquet, mzpeak_index.json, and optional spectra_peaks.parquet). Verify the output by checking for valid ZIP structure, presence of required Parquet files, and metadata correctness in mzpeak_index.json.

## Related tools

- **Rust (cargo)** (Build system and compiler for the mzPeak converter tool.) — https://github.com/HUPO-PSI/mzPeak
- **mzpeak_prototyping** (Repository containing the Rust implementation of the mzPeak converter library and command-line tools.) — https://github.com/HUPO-PSI/mzPeak
- **OpenMS** (Referenced as holder of the mzPeak trademark and related mass spectrometry processing framework.)
- **Apache Parquet** (Columnar storage format used internally by mzPeak for spectra_metadata.parquet and spectra_data.parquet.) — https://parquet.apache.org/

## Examples

```
cargo build --release && ./target/release/mzpeak_convert --input data.mzML --output data.mzpeak
```

## Evaluation signals

- Output file is a valid ZIP archive readable by standard ZIP utilities.
- Archive contains required Parquet files: spectra_metadata.parquet and spectra_data.parquet, plus mzpeak_index.json.
- mzpeak_index.json is valid JSON and correctly references all stored Parquet tables.
- Parquet files conform to mzPeak schema (validate using JSONSchema in schema/ directory of specification repository).
- Spectrum metadata (scan count, precursors, selected ions) matches input file; data arrays are not truncated or corrupted (spot-check peak apex positions and intensity ranges).

## Limitations

- The Rust implementation is work-in-progress with no stability guarantee; API and output format may change.
- Input format support depends on parsers available in the mzpeak_prototyping repository; not all vendor formats may be implemented.
- Zero-run stripping and null-marking are applied only to profile data; centroid data is stored as-is. Peak reconstruction accuracy using null-marked m/z spacing relies on fitted polynomial models (δmz ~ β₀ + β₁·mz + β₂·mz²) and may degrade for sparse or irregularly-spaced data.
- Numpress compression methods require the chunked layout and incur small lossy transformations; lossless storage uses point layout with larger file size.

## Evidence

- [intro] command line tools for converting existing formats into mzPeak: "command line tools for converting existing formats into mzPeak"
- [readme] Build and execute the converter with mzML input: "1. Clone or obtain the mzpeak_prototyping Rust repository from github.com/mobiusklein/mzpeak_prototyping at the repository root. 2. Build the command-line converter tool using Rust's cargo build"
- [readme] mzPeak format structure and contents: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP] archive. Each Parquet file describes a different facet of the stored mass"
- [readme] Archive component files: "- `mzpeak_index.json`: Definition of the files present in the archive, encoded as JSON. - `spectra_metadata.parquet`: Spectrum level metadata and file-level metadata. - `spectra_data.parquet`:"
- [readme] Verification of output validity: "Verify that the output file is produced in valid mzPeak binary format with correct structure and metadata."
- [readme] Work-in-progress stability statement: "**NOTE**: This is a **work in progress**, no stability is guaranteed at this point."
- [readme] Zero-run stripping and null-marking mechanism: "all but the first and last zero intensity points are removed. This is only meaningful for profile data... replace the flanking zero intensity points with `null` m/z and intensity values"
