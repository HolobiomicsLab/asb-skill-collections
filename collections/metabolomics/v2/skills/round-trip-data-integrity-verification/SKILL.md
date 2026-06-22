---
name: round-trip-data-integrity-verification
description: Use when you have implemented or are validating a reader/writer library for a mass spectrometry file format (such as mzPeak, mzML, or similar), and need to confirm that data parsed from disk can be written back without loss of information.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Rust mzPeak library
  - Parquet reader/writer (e.g., pyarrow, arrow R package)
  - ZIP utility
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

# round-trip-data-integrity-verification

## Summary

Verify that mass spectrometry data can be read from a file format, written back to disk, and compared for structural and data equivalence to confirm lossless serialization. This ensures that file format implementations correctly preserve all spectrum metadata, signal arrays, and instrument information through encode–decode cycles.

## When to use

Apply this skill when you have implemented or are validating a reader/writer library for a mass spectrometry file format (such as mzPeak, mzML, or similar), and need to confirm that data parsed from disk can be written back without loss of information. Use it after any changes to the format specification, after porting the implementation to a new language or platform, or as a regression test before release.

## When NOT to use

- The reader/writer implementations are incomplete or do not yet support writing (e.g., Python and R mzPeak implementations currently support reading only, not writing).
- The file format is still in active development with no stability guarantee, and the specification may change between test runs, invalidating previous reference files.
- The original file was created with a lossy transformation (e.g., Numpress compression) and you require bit-exact equality rather than reconstruction-accuracy validation.

## Inputs

- mass spectrometry data file in target format (mzPeak archive, mzML, or similar)
- reader implementation (library or command-line tool)
- writer implementation (library or command-line tool)

## Outputs

- round-tripped data file written to disk
- structural comparison report (schema, metadata structure, file inventory match)
- data equivalence report (spectrum counts, array values, metadata field-by-field comparison)
- integrity assessment (pass/fail, with documented tolerances and any discrepancies)

## How to apply

Obtain a sample mass spectrometry file in the target format (e.g., an mzPeak archive). Load the file using the reader functionality of the implementation under test, capturing all spectrum metadata (scan indices, precursors, selected ions), chromatogram metadata, and signal data arrays (m/z and intensity values, potentially with null markers or zero-run stripping applied). Write the loaded data back to a new file on disk using the writer functionality. Compare the original and round-tripped files by verifying structural equivalence (same Parquet schemas, same JSON metadata in file-level metadata segments, same archive index), then verify data equivalence by checking that spectrum counts, metadata fields, and signal arrays match within expected tolerances. For compressed or transformed data (e.g., Numpress-encoded signals or null-marked m/z arrays), account for lossy transformations by validating reconstruction accuracy rather than bit-exact equality. Document the tolerance used (e.g., floating-point precision, peak apex shift, centroid error) to establish what 'equivalence' means for the specific format and compression mode.

## Related tools

- **Rust mzPeak library** (read and write mzPeak archives; provide the reference implementation for round-trip testing) — https://github.com/HUPO-PSI/mzPeak
- **Parquet reader/writer (e.g., pyarrow, arrow R package)** (parse and serialize Parquet tables within mzPeak archives for data equivalence comparison) — https://arrow.apache.org/
- **ZIP utility** (extract and list contents of mzPeak archive files for structural comparison)

## Examples

```
cargo run --release --bin round_trip_test -- --input sample.mzpeak --output round_trip.mzpeak && diff <(unzip -Z1 sample.mzpeak | sort) <(unzip -Z1 round_trip.mzpeak | sort)
```

## Evaluation signals

- Original and round-tripped files contain identical counts of spectra, chromatograms, and metadata entries.
- Parquet schema definitions (column names, types, nullable flags) are identical between original and round-tripped files.
- File-level metadata JSON documents (instrument, software, data transformation pipeline) match exactly or within documented schema version tolerance.
- m/z and intensity signal arrays are equal within the tolerance specified for the compression mode (lossless: exact match; Numpress-encoded: reconstruction error < vendor-specified threshold; null-marked: peak apex shift < 0.1 ppm or centroid error < 1 mDa).
- Optional files (e.g., spectra_peaks.parquet) are present in both versions or absent in both, and archive index (mzpeak_index.json) lists the same file inventory.

## Limitations

- The mzPeak format is a work in progress with no stability guaranteed; round-trip test fixtures may become invalid if the specification changes.
- The Python and R implementations support reading only, not writing, so round-trip verification is not possible for those languages in their current state.
- Lossy transformations such as Numpress compression introduce intentional information loss; round-trip verification for compressed data requires reconstruction-accuracy benchmarking rather than bit-exact comparison.
- Zero-run stripping and null-marked m/z reconstruction introduce small floating-point errors in the m/z axis; tolerance thresholds must be set per dataset and compression mode to avoid false failures.
- File-level metadata encoded as JSON within Parquet metadata segments may vary in serialization order or whitespace; comparison must be schema-aware rather than string-literal.

## Evidence

- [other] round-trip integrity verification rationale: "Load a sample mzPeak input file using the Rust library's read functionality. Write the loaded data back to disk as a new mzPeak file using the library's write functionality. Verify round-trip"
- [other] Rust library implements read/write capability: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into"
- [readme] format components and archive structure: "mzPeak is a archive of multiple [Parquet] files, stored directly in an _uncompressed_ [ZIP] archive. Each Parquet file describes a different facet of the stored mass spectrometry run."
- [readme] data preservation through transformations: "Because the non-zero m/z points remain unchanged, the reconstructed signal's peak apex or centroid should be unaffected. If the peak is composed of only three points including the two zero intensity"
- [other] Python/R read-only implementation limitation: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`] ... The Python codebase does not support writing at this time ... using the [`arrow`] ... for _reading_ only at this time"
