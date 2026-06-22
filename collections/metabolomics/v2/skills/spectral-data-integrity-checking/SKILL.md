---
name: spectral-data-integrity-checking
description: Use when after converting mass-spectrometry data from an existing format (mzML, mzXML, or vendor-specific formats) into mzPeak using command-line tools or API calls.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Rust mzPeak CLI
  - pyarrow
  - arrow (R package)
  - JSON Schema validator
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

# Spectral Data Integrity Checking

## Summary

Validate converted mass-spectrometry spectral data by verifying file format structure, schema compliance, and preservation of key spectral attributes (peaks, precursor masses, retention times) against the mzPeak specification. This skill ensures that data transformations into the mzPeak Parquet-based archive format have not corrupted or lost critical information.

## When to use

After converting mass-spectrometry data from an existing format (mzML, mzXML, or vendor-specific formats) into mzPeak using command-line tools or API calls. Apply this skill whenever you need confidence that spectral metadata, data arrays, and instrument parameters have survived the conversion pipeline intact and conform to the mzPeak schema.

## When NOT to use

- Input is already a trusted, validated mzPeak file from a known-reliable source.
- You only need to verify file existence, not data fidelity or schema compliance.
- The conversion tool is not from the HUPO-PSI/mzPeak implementation and you have no specification reference.

## Inputs

- mzPeak file (ZIP archive containing Parquet files)
- Original source mass-spectrometry file (mzML, mzXML, or vendor format)
- mzPeak JSON schema definitions (from schema/ directory)

## Outputs

- Validation report (pass/fail on file integrity, schema compliance, attribute preservation)
- Attribute comparison table (e.g., original vs. converted retention times, precursor masses)
- Error log or warnings (missing files, null values, schema violations, reconstruction errors)

## How to apply

First, verify that the output file exists and is a valid ZIP archive containing the expected Parquet files (mzpeak_index.json, spectra_metadata.parquet, spectra_data.parquet, and optionally spectra_peaks.parquet). Second, validate the file structure by checking that mzpeak_index.json correctly lists all present files and that each Parquet file adheres to its schema as defined in the mzPeak specification. Third, reconstruct or spot-check key spectral attributes from the converted data: load spectra_metadata.parquet to confirm precursor masses and retention times match the original input, and load spectra_data.parquet to verify that m/z and intensity arrays are present and non-empty for expected spectra. Fourth, if zero-run stripping or null marking has been applied, cross-reference a sample of reconstructed peaks against the original file to confirm that peak apexes and centroids remain unchanged. Use the JSON schemas in the mzPeak specification's schema/ directory as the authoritative format reference.

## Related tools

- **Rust mzPeak CLI** (Performs format conversion and writes mzPeak archive; output is the primary artifact for integrity checking) — https://github.com/HUPO-PSI/mzPeak
- **pyarrow** (Reads mzPeak Parquet tables into Python for programmatic validation and attribute extraction) — https://arrow.apache.org/docs/python/index.html
- **arrow (R package)** (Reads mzPeak Parquet tables in R for statistical validation and cross-file comparison) — https://arrow.apache.org/docs/r/
- **JSON Schema validator** (Validates mzpeak_index.json and file-level metadata JSON documents against schema definitions)

## Examples

```
import pyarrow.parquet as pq; meta = pq.read_table('spectra_metadata.parquet'); print(f'Spectra count: {len(meta)}'); data = pq.read_table('spectra_data.parquet'); print(f'Data points: {len(data)}'); assert all(col in data.column_names for col in ['mz', 'intensity']), 'Missing required columns'
```

## Evaluation signals

- Output ZIP archive structure is valid: mzpeak_index.json exists and lists all expected Parquet files with correct controlled vocabulary keys.
- Each Parquet file (spectra_metadata.parquet, spectra_data.parquet, spectra_peaks.parquet if present) conforms to its JSON schema and has no parsing errors when loaded with pyarrow or R arrow.
- Precursor masses, retention times, and spectrum count from spectra_metadata.parquet match the source file (within expected precision; e.g., retention time to 2 decimal places, m/z to 4 decimal places).
- Spectrum m/z and intensity arrays in spectra_data.parquet are non-null and contain the expected number of data points for profile or centroid data; no array should be empty for spectra marked as present in the index.
- If zero-run stripping or null marking was applied, reconstructed peak positions and centroids from the mzPeak data deviate by < 0.01 m/z units or < 5 ppm from the original source data, confirming lossless reconstruction.

## Limitations

- The mzPeak format is a work in progress with no stability guaranteed; schema definitions may change, invalidating previously validated files.
- Python and R implementations support reading only, not writing, so validation in those languages cannot verify round-trip fidelity for file creation.
- Null marking reconstruction accuracy depends on the fidelity of the fitted m/z spacing model; systematic bias in the model may introduce small but cumulative errors for spectra with large m/z ranges.
- Vendor-specific metadata or custom controlled vocabulary terms present in the original file may be lost or remapped during conversion if not explicitly handled by the conversion tool.
- Large files (> 1 GB) may require streaming or chunked validation to fit in memory; standard integrity checks assume the file can be fully loaded.

## Evidence

- [other] confirming the converted data preserves key spectral attributes (peaks, precursor masses, retention times) from the original input: "confirming the converted data preserves key spectral attributes (peaks, precursor masses, retention times) from the original input"
- [readme] The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into mzPeak: "command line tools for converting existing formats into mzPeak"
- [readme] mzPeak is a archive of multiple Parquet files, stored directly in an uncompressed ZIP archive.: "mzPeak is a archive of multiple Parquet files, stored directly in an uncompressed ZIP archive"
- [readme] mzpeak_index.json: Definition of the files present in the archive, encoded as JSON. This makes resolving files by controlled terms easier than matching file names.: "mzpeak_index.json: Definition of the files present in the archive, encoded as JSON"
- [readme] If the peak is composed of only three points including the two zero intensity spots, no meaningful peak model can be fit in any case so the minute angle change this would induce are still effectively lossless.: "reconstructed signal's peak apex or centroid should be unaffected"
- [readme] This repository contains prototype implementations of the mzPeak format initially described in https://pubs.acs.org/doi/10.1021/acs.jproteome.5c00435.: "This repository contains prototype implementations of the mzPeak format"
- [readme] **NOTE**: This is a **work in progress**, no stability is guaranteed at this point.: "This is a **work in progress**, no stability is guaranteed at this point"
