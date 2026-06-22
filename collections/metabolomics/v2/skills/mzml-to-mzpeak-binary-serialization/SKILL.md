---
name: mzml-to-mzpeak-binary-serialization
description: Use when you have one or more mzML files (XML-based mass spectrometry data) and need to convert them into mzPeak format for downstream analysis, archival, or integration with tools that consume Parquet-based spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - OpenMS
  - Rust (cargo)
  - pyarrow
  - Apache Arrow (R)
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzpeak
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_mzpeak
schema_version: 0.2.0
---

# mzml-to-mzpeak-binary-serialization

## Summary

Convert mass spectrometry data from mzML format into the mzPeak binary Parquet-based archive format using the Rust command-line converter tool. This skill enables transformation of vendor-neutral XML-based spectra into a scalable, interoperable columnar storage format optimized for random access and compression.

## When to use

You have one or more mzML files (XML-based mass spectrometry data) and need to convert them into mzPeak format for downstream analysis, archival, or integration with tools that consume Parquet-based spectra. This is the entry point when beginning a mzPeak-centric workflow or migrating legacy mzML datasets.

## When NOT to use

- Input is already in mzPeak format or another Parquet-based columnar format.
- Workflow requires real-time streaming conversion; mzPeak conversion requires buffering the entire spectrum set into Parquet tables.
- Python or R read-only implementations are sufficient for your use case; the Rust implementation is required for format conversion and writing.

## Inputs

- mzML file (XML-formatted mass spectrometry spectrum data)

## Outputs

- mzPeak file (uncompressed ZIP archive containing Parquet tables: mzpeak_index.json, spectra_metadata.parquet, spectra_data.parquet, and optionally spectra_peaks.parquet)

## How to apply

Clone the mzpeak_prototyping Rust repository and build the command-line converter tool using Rust's cargo build system. Execute the converter tool with an mzML input file, specifying the desired mzPeak output file path. The converter reads spectrum metadata (descriptions, scans, precursors, selected ions), spectrum signal data (profile or centroid), and optional centroid peaks, then serializes them into a ZIP archive containing Parquet files: mzpeak_index.json, spectra_metadata.parquet, spectra_data.parquet, and optionally spectra_peaks.parquet. Verify the output by checking that the resulting .mzpeak file is a valid ZIP archive containing the expected Parquet files and that metadata (instrumentation, software, data transformation pipeline) are preserved in the Parquet metadata segment as JSON documents.

## Related tools

- **Rust (cargo)** (Build and execution environment for the mzpeak_prototyping command-line converter tool) — https://github.com/mobiusklein/mzpeak_prototyping
- **OpenMS** (Trademark holder and reference implementation ecosystem for mzPeak format standardization)
- **pyarrow** (Python implementation for reading mzPeak files post-conversion (read-only support)) — https://arrow.apache.org/docs/python/index.html
- **Apache Arrow (R)** (R implementation for reading mzPeak files post-conversion (read-only support)) — https://arrow.apache.org/docs/r/

## Examples

```
cargo build --release && ./target/release/mzpeak_converter --input sample.mzML --output sample.mzpeak
```

## Evaluation signals

- Output file is a valid uncompressed ZIP archive containing mzpeak_index.json and at least spectra_metadata.parquet and spectra_data.parquet files.
- mzpeak_index.json is valid JSON and correctly enumerates the Parquet files present in the archive.
- spectra_metadata.parquet contains expected columns for spectrum index, spectrum ID, scan number, retention time, precursor m/z, and other metadata; spectra_data.parquet contains m/z and intensity arrays with correct data types (float32 or float64).
- File-level metadata (instrumentation, software, data transformation) are preserved in the Parquet metadata segment as valid JSON documents conformable to the mzPeak JSON Schema.
- Output can be successfully read by the mzPeak Python or R implementations using pyarrow or arrow libraries without schema errors.

## Limitations

- Project is in work-in-progress status with no stability guarantee; the specification and implementation may change.
- Python and R implementations support read-only access to converted mzPeak files; only the Rust implementation supports both reading and writing.
- Conversion requires the entire spectrum set to fit in memory or be buffered, limiting scalability for extremely large mzML files.
- mzML files with nested or vendor-specific metadata structures may lose fidelity if those structures do not map directly to mzPeak's schema for controlled vocabularies and arbitrary metadata JSON.
- The converter does not perform quality filtering, denoising, or spectral feature extraction; it is a direct structural transformation.

## Evidence

- [other] The Rust implementation at the repository root includes command-line tools capable of converting existing mass spectrometry data formats into the mzPeak format, operating as a library for both reading and writing mzPeak files.: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into"
- [readme] mzPeak is a ZIP-based archive of Parquet files containing structured spectrum metadata and signal data.: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP](<https://en.wikipedia.org/wiki/ZIP_(file_format)>) archive. Each Parquet file"
- [readme] File-level metadata including instrumentation, software, and data transformation pipeline are stored in the Parquet metadata segment as JSON documents.: "mzPeak file-level metadata, including descriptions of the file's contents, the instrumentation, software, and data transformation pipeline are stored in the Parquet metadata segment as JSON documents."
- [other] The converter tool accepts mzML as input format and produces mzPeak output with correct structure and metadata.: "Execute the converter tool with an mzML input file as the source format, specifying the desired mzPeak output file path. Verify that the output file is produced in valid mzPeak binary format with"
- [readme] Spectrum metadata is stored in spectra_metadata.parquet; signal data in spectra_data.parquet; optional centroid peaks in spectra_peaks.parquet.: "- `spectra_metadata.parquet`: Spectrum level metadata and file-level metadata. Includes spectrum descriptions, scans, precursors, and selected ions using packed parallel tables.
-"
