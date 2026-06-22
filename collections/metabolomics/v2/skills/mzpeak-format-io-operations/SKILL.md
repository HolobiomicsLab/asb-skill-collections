---
name: mzpeak-format-io-operations
description: Use when you have mass spectrometry run data (spectra, chromatograms, instrument metadata) that must be stored in or recovered from the mzPeak format, or when you need to validate that a mzPeak implementation correctly supports both read and write paths for round-trip fidelity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Rust mzPeak library
  - PyArrow
  - Arrow (R)
  - mzPeak specification
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans: []
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

# mzPeak format I/O operations

## Summary

Read, write, and round-trip mass spectrometry spectra and chromatogram data using the mzPeak Parquet-based format, which stores spectrum metadata, signal arrays, and instrument configuration in an uncompressed ZIP archive. This skill validates interoperability of mzPeak implementations and enables lossless serialization of complex MS data structures.

## When to use

Use this skill when you have mass spectrometry run data (spectra, chromatograms, instrument metadata) that must be stored in or recovered from the mzPeak format, or when you need to validate that a mzPeak implementation correctly supports both read and write paths for round-trip fidelity. Apply this skill if you are prototyping or evaluating mzPeak tooling across Rust, Python, R, or other language implementations.

## When NOT to use

- If your MS data is already stored in a different open format (mzML, mzXML, netCDF) and you do not need to convert to mzPeak—use existing readers for those formats instead.
- If you require write support and are using Python or R implementations—currently only read operations are supported; use the Rust implementation for full read/write capability.
- If you need guaranteed backward compatibility or stable API—the mzPeak format and implementations are work-in-progress with no stability guaranteed.

## Inputs

- mzPeak file (uncompressed ZIP archive containing Parquet tables and JSON index)
- Mass spectrometry run metadata (spectrum descriptions, scans, precursors, selected ions)
- Spectrum signal data arrays (m/z and intensity in profile or centroid mode)
- Chromatogram metadata and signal data (optional)
- File-level metadata (instrumentation, software, transformation pipeline)
- Controlled vocabulary terms for spectrum and chromatogram annotations

## Outputs

- Deserialized spectrum and chromatogram objects in application memory
- Round-tripped mzPeak file (new ZIP archive with Parquet tables)
- Comparison report (structural/data equivalence metrics, diff summary)
- Validation logs (schema compliance, row counts, null-marking reconstruction fidelity)
- Error or warning messages if zero-run stripping or null-marked m/z reconstruction diverges from original

## How to apply

Obtain the mzPeak library implementation for your language (Rust at the repository root supports both read and write; Python and R implementations currently support read-only operations via PyArrow and Arrow respectively). Compile or install the library and its dependencies. Load a reference mzPeak file (an uncompressed ZIP archive containing Parquet files: mzpeak_index.json, spectra_metadata.parquet, spectra_data.parquet, and optionally spectra_peaks.parquet and chromatogram files). Deserialize the archive into in-memory MS data structures using the library's read API. Serialize the loaded data back to disk as a new mzPeak file using the write API. Verify round-trip integrity by comparing the original and re-written files for structural equivalence (JSON index match, Parquet schema preservation, row counts), data equivalence (m/z and intensity array values, metadata fields), and byte-level differences if lossless round-tripping is claimed.

## Related tools

- **Rust mzPeak library** (Primary implementation providing both read and write I/O for mzPeak files, including command-line tools for format conversion) — https://github.com/HUPO-PSI/mzPeak
- **PyArrow** (Underlying Arrow library used by the Python mzPeak implementation to deserialize Parquet tables for reading) — https://arrow.apache.org/docs/python/index.html
- **Arrow (R)** (R language binding to Apache Arrow, used by the R mzPeak implementation for read-only access to Parquet files) — https://arrow.apache.org/docs/r/
- **mzPeak specification** (Normative schema and format definition including Parquet table layouts, JSON metadata structure, zero-run stripping and null-marking algorithms) — https://github.com/HUPO-PSI/mzPeak-specification

## Examples

```
# Load and round-trip mzPeak file using Rust library
cargo run --bin mzpeak -- read input.mzpeak write output.mzpeak && diff <(unzip -c input.mzpeak mzpeak_index.json) <(unzip -c output.mzpeak mzpeak_index.json)
```

## Evaluation signals

- mzpeak_index.json present in round-tripped file and field definitions match original (file list, controlled vocabulary references)
- Parquet table schema preserved: spectra_metadata.parquet and spectra_data.parquet row counts and column types identical to original
- m/z and intensity array values match original within measurement precision after reconstruction from null-marked or zero-run-stripped representations
- Spectrum-level metadata (scan identifiers, precursor m/z, retention time, centroid/profile mode flag) byte-identical or semantically equivalent after round-trip
- If null-marking or m/z spacing models were used during write, reconstructed m/z values for null-marked points fall within 5 ppm tolerance of original peak apexes and centroids

## Limitations

- Python and R implementations do not support write operations; round-trip validation is only possible with the Rust implementation.
- The mzPeak format is a work-in-progress with no API or file format stability guaranteed; breaking changes may occur in future versions.
- Zero-run stripping and null-marking introduce lossy compression for profile data; lossless round-tripping is only guaranteed when no zero-run stripping is applied.
- Numpress compression methods (if applied) incur additional lossiness beyond null-marking; the reconstructed peak apexes and centroids may diverge from originals by sub-peak-width angles.
- Round-trip comparison logic must account for Parquet's internal compression and metadata reordering; byte-level file comparison will fail even for semantically equivalent data.

## Evidence

- [intro] Rust library round-trip capability: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files"
- [intro] Read-only support in Python and R: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`] ... The Python codebase does not support writing at this time ... using the [`arrow`] ... for _reading_ only at this time"
- [readme] mzPeak archive structure and components: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP] archive. Each Parquet file describes a different facet of the stored mass"
- [readme] Zero-run stripping and null-marking algorithms: "all but the first and last zero intensity points are removed. This is only meaningful for profile data. ... replace the flanking zero intensity points with `null` m/z and intensity values"
- [readme] Work-in-progress status and stability caveat: "**NOTE**: This is a **work in progress**, no stability is guaranteed at this point."
- [other] Round-trip integrity verification task: "Verify round-trip integrity by comparing the original and round-tripped files for structural and data equivalence."
