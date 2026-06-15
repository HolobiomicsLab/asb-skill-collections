---
name: mass-spectrometry-data-format-parsing
description: Use when you have raw mass spectrometry instrument output (mzML, vendor binary formats, or mzPeak archives) and need to load spectrum metadata, chromatogram data, or signal arrays into memory for quality control, format conversion, or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - OpenMS
  - Python
  - pyarrow
  - R
  - Rust mzPeak library and CLI converter
  - Python pyarrow implementation
  - R arrow implementation
  - Apache Arrow / PyArrow
  - mzPeak specification
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- There is a separate Python implementation in `python/`
- complete re-implementation for _reading_ mzPeak files using [`pyarrow`]
- There is also an R implementation in `R/`
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

# mass-spectrometry-data-format-parsing

## Summary

Parse and read mass spectrometry data files in multiple formats (mzML, mzPeak, vendor formats) into structured tabular representations using language-specific Arrow/Parquet libraries. This skill is essential for converting raw or legacy instrument output into interoperable, queryable data structures compatible with downstream proteomics analysis pipelines.

## When to use

You have raw mass spectrometry instrument output (mzML, vendor binary formats, or mzPeak archives) and need to load spectrum metadata, chromatogram data, or signal arrays into memory for quality control, format conversion, or statistical analysis. Use this skill when your input is a single file or batch of files and your goal is to construct in-memory or on-disk tabular representations (pandas DataFrames, Arrow Tables, or Parquet datasets) for downstream consumption.

## When NOT to use

- Your data is already in a parsed tabular format (DataFrame, Parquet, or Arrow Table) — skip directly to analysis or transformation.
- You require write access and are using Python or R implementations — use the Rust library or wait for future Python/R write support.
- Your workflow demands lossless preservation of all vendor-specific metadata not covered by the mzPeak schema — consider retaining the original file alongside the parsed output.

## Inputs

- mzML file (XML-based mass spectrometry data format)
- mzPeak archive (ZIP-based Parquet collection with JSON index)
- vendor binary spectrum files (Thermo .raw, Sciex .wiff, etc.)
- CSV or TSV spectrum metadata exports

## Outputs

- pandas DataFrame with spectrum metadata and/or signal data
- Arrow Table with spectrum or chromatogram records
- Parquet file(s) containing parsed spectra and metadata
- CSV export of parsed spectrum table
- mzPeak archive (ZIP of Parquet files with JSON index)

## How to apply

Identify which implementation matches your runtime environment and input format: use the Rust library (with CLI tools) if you need bidirectional read/write support and format conversion from mzML or vendor formats into mzPeak; use the Python/pyarrow implementation if you are working in a PyData stack (pandas, NumPy) and only require read access; use the R/arrow implementation if your analysis pipeline is in R. Load the mass spectrometry file using the language-specific reader function, which returns either an Arrow Table or pandas DataFrame containing spectrum or chromatogram metadata (scan number, precursor m/z, retention time, instrument parameters) and signal data arrays (m/z and intensity values, possibly with zero-run stripping or null-marking optimizations). Export the resulting table to Parquet or CSV format for downstream use. Verify parsing correctness by spot-checking row counts, field names, and data types against the mzPeak specification schema.

## Related tools

- **Rust mzPeak library and CLI converter** (Primary read/write implementation; converts mzML and vendor formats into mzPeak archives; available as a library and command-line tool) — https://github.com/HUPO-PSI/mzPeak
- **Python pyarrow implementation** (Read-only mzPeak parser for PyData stack integration; returns pandas DataFrames or Arrow Tables) — https://github.com/HUPO-PSI/mzPeak (python/ subdirectory)
- **R arrow implementation** (Read-only mzPeak parser for R workflows; compatible with tidyverse and Arrow ecosystems) — https://github.com/HUPO-PSI/mzPeak (R/ subdirectory)
- **OpenMS** (Reference proteomics toolkit; holds mzPeak trademark; provides mass spectrometry data processing context) — https://www.openms.de/
- **Apache Arrow / PyArrow** (Underlying columnar data structure and serialization engine for mzPeak Parquet files) — https://arrow.apache.org/
- **mzPeak specification** (Canonical schema definition for mzPeak files; defines Parquet layouts, metadata JSON, and controlled vocabularies) — https://github.com/HUPO-PSI/mzPeak-specification

## Evaluation signals

- Row count and column count match the expected counts from the source file's native headers or metadata sections (e.g., <spectrum> tags in mzML)
- Field names and data types conform to the mzPeak specification schemas in schema/ (e.g., spectrum_index is integer, mz is float64, intensity is float32 or float64)
- Numerical values (m/z, intensity, retention time) fall within plausible ranges for the instrument type and scan mode; no unexpected NaN, Inf, or negative intensity values in centroid data
- When the same input file is parsed by multiple implementations (Rust, Python, R), field-by-field CSV exports show exact agreement in row counts, field names, and numerical values (after accounting for floating-point rounding)
- For converted mzPeak outputs, verify that the resulting ZIP archive contains exactly the expected Parquet files (spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, etc.) and a valid JSON mzpeak_index.json

## Limitations

- Python and R implementations support reading only; write support is not yet available, requiring use of the Rust CLI for format conversion and output generation.
- mzPeak is a work-in-progress format with no stability guarantee; schema and API may change before 1.0 release.
- Zero-run stripping and null-marking optimizations introduce lossy compression for profile data; reconstructed m/z spacing for null-marked points relies on a fitted polynomial model (δmz ~ β₀ + β₁·mz + β₂·mz²) that may not be accurate for all m/z regions.
- Vendor-specific metadata not covered by controlled vocabularies (e.g., instrument calibration constants, proprietary scan parameters) may be lost or truncated during conversion to mzPeak.
- The .NET (C#) and JavaScript/TypeScript implementations are hosted separately and may lag behind the primary Rust implementation in feature completeness.

## Evidence

- [intro] Complete re-implementation for reading mzPeak files using pyarrow, and the PyData stack: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`](https://arrow.apache.org/docs/python/index.html), and the PyData stack"
- [intro] Rust library includes read/write and CLI conversion tools: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into"
- [intro] Python and R are read-only implementations: "The Python codebase does not support writing at this time although this is subject to change in the future"
- [readme] mzPeak format is a ZIP archive of Parquet files with JSON index: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP](<https://en.wikipedia.org/wiki/ZIP_(file_format)>) archive"
- [readme] Core mzPeak file structure includes metadata and data tables: "- `mzpeak_index.json`: Definition of the files present in the archive, encoded as JSON. This makes resolving files by controlled terms easier than matching file names.
- `spectra_metadata.parquet`:"
- [readme] Zero-run stripping and null-marking optimization technique: "When storing spectrum data, some vendors will produce arrays with lots of "empty" regions filled with zero intensity values along a semi-regularly spaced m/z axis. These regions hold little"
- [readme] Work-in-progress status with no stability guarantee: "**NOTE**: This is a **work in progress**, no stability is guaranteed at this point."
