---
name: mzpeak-file-io-operations
description: 'Use when you have raw mass spectrometry data (vendor formats, mzML, or existing mzPeak files) and need to: (1) convert to mzPeak format for long-term storage and interoperability across languages and tools; (2) load mzPeak spectrum or chromatogram data into memory as structured tables for analysis;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3999
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - OpenMS
  - Python
  - pyarrow
  - Rust mzPeak library and CLI
  - Python pyarrow implementation
  - R arrow implementation
  - .NET (C#) implementation
  - TypeScript/JavaScript implementation
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- There is a separate Python implementation in `python/`
- complete re-implementation for _reading_ mzPeak files using [`pyarrow`]
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.5c00435
  all_source_dois:
  - 10.1021/acs.jproteome.5c00435
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzpeak-file-io-operations

## Summary

Reading and writing mass spectrometry spectra and chromatogram data in the mzPeak format, a Parquet-based archive standard that stores spectrum metadata, signal data, and instrument information in structured tabular form. Use this skill to convert between vendor formats (e.g., mzML, vendor binary) and the interoperable mzPeak format, or to load mzPeak files into PyData-compatible structures (pandas DataFrame, Arrow Table) for downstream analysis.

## When to use

You have raw mass spectrometry data (vendor formats, mzML, or existing mzPeak files) and need to: (1) convert to mzPeak format for long-term storage and interoperability across languages and tools; (2) load mzPeak spectrum or chromatogram data into memory as structured tables for analysis; or (3) integrate mass spectrometry data with the broader PyData ecosystem (pandas, polars, dask). Apply this skill when your input is a recognized MS format and your output target is either an mzPeak archive or an in-memory tabular representation.

## When NOT to use

- Input is already a validated mzPeak archive and you only need to query or filter specific spectra — use direct parquet read/filter operations instead of round-trip conversion.
- You require writing capability with Python or R — the current implementations support reading only; use the Rust implementation or .NET/JS variants for write operations.
- Your workflow demands lossless, uncompressed signal recovery and you have applied Numpress compression — mzPeak's null-marking reconstruction is approximate and unsuitable for applications (e.g., exact peak shape modeling) requiring sub-ppm m/z accuracy after sparse encoding.

## Inputs

- mzML file or vendor binary MS data (e.g., Thermo .raw, Sciex .wiff)
- existing mzPeak archive (ZIP of Parquet files)
- spectrum metadata table (JSON, CSV, or Parquet with scan, precursor, ion information)
- spectrum signal arrays (m/z and intensity paired columns, profile or centroid mode)

## Outputs

- mzPeak archive (uncompressed ZIP containing mzpeak_index.json, spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, chromatograms_data.parquet)
- pandas DataFrame or pyarrow Table with spectrum metadata and signal data columns
- parquet file or CSV export of spectrum or chromatogram tables

## How to apply

For writing/conversion: use the Rust command-line tools or library from the repository root to read source format and emit an uncompressed ZIP archive containing mzpeak_index.json (file listing), spectra_metadata.parquet and spectra_data.parquet (spectrum tables), and chromatograms_metadata.parquet and chromatograms_data.parquet (chromatogram tables). For reading: invoke the language-specific reader (Python pyarrow implementation, R arrow implementation, or Rust library) to deserialize the Parquet tables within the ZIP, optionally applying zero-run stripping or null-marking reconstruction if the source used sparse encoding. Extract spectrum-level metadata (scans, precursors, selected ions) from *_metadata.parquet and signal arrays (m/z, intensity) from *_data.parquet. Validate schema conformance using the JSON Schema files in the schema/ directory. Rationale: mzPeak's Parquet foundation enables efficient compression, columnar access, and language-agnostic interoperability, while packed parallel table layout and sparse encoding (zero-run stripping, null marking with m/z model fitting) reduce storage footprint for profile data without lossy compression.

## Related tools

- **Rust mzPeak library and CLI** (Read and write mzPeak archives; convert vendor and mzML formats to mzPeak; command-line interface for format conversion and file inspection) — https://github.com/HUPO-PSI/mzPeak
- **Python pyarrow implementation** (Read-only deserialization of mzPeak archives into pyarrow Tables and pandas DataFrames; integration with PyData stack) — https://github.com/HUPO-PSI/mzPeak (python/ subdirectory)
- **R arrow implementation** (Read-only deserialization of mzPeak Parquet tables into R data structures) — https://github.com/HUPO-PSI/mzPeak (R/ subdirectory)
- **.NET (C#) implementation** (Read and write mzPeak files in .NET/C# environments) — https://github.com/HUPO-PSI/mzPeak.NET
- **TypeScript/JavaScript implementation** (Browser-based mzPeak file reading and visualization) — https://github.com/HUPO-PSI/mzpeakts
- **OpenMS** (Potential downstream tool for mass spectrometry data processing; mzPeak format specification held in trust by OpenMS Inc.)

## Examples

```
from mobiusklein.mzpeak_prototyping import mzpeak_reader; import pyarrow.parquet as pq; archive = mzpeak_reader.read('sample.mzpeak'); spectra_meta = pq.read_table(archive['spectra_metadata.parquet']).to_pandas(); print(spectra_meta.head())
```

## Evaluation signals

- Output mzPeak archive contains all six required Parquet files (mzpeak_index.json, spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, chromatograms_data.parquet, and optional spectra_peaks.parquet) and conforms to schema definitions in schema/ directory.
- Loaded spectrum metadata includes non-null scan, precursor, and selected ion fields following packed parallel table layout; verify no data loss in nested struct columns.
- Spectrum signal data arrays (m/z, intensity) round-trip without lossy compression artifacts; if null-marking was applied, reconstructed m/z values from fitted model match original within local median δmz tolerance (typically <0.1 Da for Orbitrap data).
- Exported pandas DataFrame or pyarrow Table has correct column dtypes (float32/float64 for m/z/intensity, int64 for spectrum_index) and row count matches input spectrum count; verify no duplicate or missing spectra.
- Zero-run stripping and null-marking reduction significantly decrease file size compared to raw input (typically 50–80% smaller); validate via ZIP archive inspection and parquet file metadata.

## Limitations

- Python and R implementations support reading only; writing requires Rust or .NET/JS implementations. Python write support is subject to change in future versions.
- mzPeak is a work-in-progress specification with no stability guarantee; schema and archive layout may change between versions.
- Null-marking m/z reconstruction via weighted least-squares model is approximate and induces minute peak-centroid angle shifts; unsuitable for applications requiring sub-ppm precision or exact peak shape recovery after sparse encoding.
- The weighted least-squares m/z model (δmz ~ β₀ + β₁·mz + β₂·mz²) assumes semi-regular m/z spacing; may poorly fit data with irregular gaps or highly non-linear calibration.
- Numpress compression methods (if used in source data) are lossy and incompatible with null-marking reconstruction; users must choose one encoding strategy.

## Evidence

- [readme] The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into mzPeak.: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into"
- [readme] There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`](https://arrow.apache.org/docs/python/index.html), and the PyData stack.: "There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`], and the PyData stack"
- [readme] mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP] archive. Each Parquet file describes a different facet of the stored mass spectrometry run.: "mzPeak is a archive of multiple Parquet files, stored directly in an uncompressed ZIP archive. Each Parquet file describes a different facet of the stored mass spectrometry run"
- [readme] The Python codebase does not support writing at this time although this is subject to change in the future.: "The Python codebase does not support writing at this time although this is subject to change in the future"
- [readme] When reading the the null-marked data, use either the local median δ mz or the learned model for that spectrum to compute the m/z spacing for singleton points to achieve an very accurate reconstruction.: "When reading the null-marked data, use either the local median δ mz or the learned model for that spectrum to compute the m/z spacing for singleton points to achieve an very accurate reconstruction"
- [readme] **NOTE**: This is a **work in progress**, no stability is guaranteed at this point.: "This is a **work in progress**, no stability is guaranteed at this point"
