---
name: mzpeak-format-file-parsing
description: Use when you have an mzPeak file (uncompressed ZIP archive containing Parquet files) and need to extract and work with spectrum metadata (scan descriptions, precursors, selected ions), spectrum signal data (profile or centroid m/z and intensity arrays), or chromatogram data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - OpenMS
  - R
  - arrow
  - pyarrow
  - Rust mzPeak library
  techniques:
  - mass-spectrometry
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

# mzpeak-format-file-parsing

## Summary

Parse mzPeak files—Parquet-based archives containing mass spectrometry spectra, chromatograms, and metadata—into structured tabular representations for downstream analysis. This skill enables reading of mzPeak's multi-file archive format (spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, etc.) using language-specific implementations.

## When to use

You have an mzPeak file (uncompressed ZIP archive containing Parquet files) and need to extract and work with spectrum metadata (scan descriptions, precursors, selected ions), spectrum signal data (profile or centroid m/z and intensity arrays), or chromatogram data. Use this skill when you require structured tabular access to these components—e.g., for visualization, statistical analysis, or format validation.

## When NOT to use

- Input is a legacy mzML or mzXML file rather than mzPeak format; use mzML/mzXML parsers (e.g., OpenMS) instead.
- You need to write or modify mzPeak files; Python and R implementations support reading only—use the Rust implementation for write access.
- Stability and long-term compatibility are critical requirements; the mzPeak format is work-in-progress with no stability guarantee at this point.

## Inputs

- mzPeak file (uncompressed ZIP archive)
- mzpeak_index.json (manifest listing Parquet files present)
- spectra_metadata.parquet (spectrum and file-level metadata with packed parallel tables)
- spectra_data.parquet (spectrum signal data in point or chunked layout)
- spectra_peaks.parquet (optional; explicit centroid data)
- chromatograms_metadata.parquet (chromatogram-level metadata)
- chromatograms_data.parquet (chromatogram signal data)

## Outputs

- Tabular representation of spectrum metadata (data frame / table)
- Tabular representation of spectrum signal data (mz and intensity arrays)
- Tabular representation of chromatogram metadata (data frame / table)
- Tabular representation of chromatogram signal data (mz/time and intensity arrays)
- Reconstructed null-marked m/z values (using spacing model when applicable)

## How to apply

Identify the appropriate language-specific mzPeak reader implementation (Rust library has full read/write support; Python pyarrow and R arrow implementations support reading only). Open the mzPeak file as a ZIP archive and parse the mzpeak_index.json manifest to identify which Parquet files are present. Use the language's Parquet reader (arrow for Python/R, or the native Rust mzPeak library) to load each required Parquet file (e.g., spectra_metadata.parquet for spectrum-level metadata and file-level metadata, spectra_data.parquet for signal arrays). For spectra_metadata.parquet and chromatograms_metadata.parquet, handle the packed parallel table structure where multiple schemas (spectrum descriptions, scans, precursors, selected ions) are stored as parallel struct/group columns that may be null at any nesting level. Reconstruct null-marked m/z values using either the local median spacing or the stored m/z spacing model (quadratic form: δ mz ~ β₀ + β₁ mz + β₂ mz²) to recover lossless or near-lossless spectrum precision. Convert the resulting Parquet columns into native tabular formats (data frames in R/Python, or structs in Rust) for analysis.

## Related tools

- **arrow** (Parquet reading for R; enables loading mzPeak Parquet files into R data frames) — https://arrow.apache.org/docs/r/
- **pyarrow** (Parquet reading for Python; enables loading mzPeak Parquet files into pandas DataFrames) — https://arrow.apache.org/docs/python/index.html
- **Rust mzPeak library** (Native mzPeak reader and writer with full read/write support; primary implementation with command-line tools) — https://github.com/HUPO-PSI/mzPeak
- **OpenMS** (Holds the mzPeak trademark and provides interoperability context for mass spectrometry data formats)

## Evaluation signals

- Successfully extracted mzpeak_index.json and verified all expected Parquet files (spectra_metadata.parquet, spectra_data.parquet, etc.) are readable and non-empty.
- Spectrum metadata table contains all expected fields for spectrum descriptions, scans, precursors, and selected ions without null-only rows or missing mandatory fields.
- Spectrum signal data (m/z and intensity arrays) can be retrieved and have matching lengths for each spectrum; null-marked m/z values are reconstructed using the stored spacing model or local median with quantifiable error < instrument resolution.
- Chromatogram metadata and signal data (if present) parse correctly with consistent time/m/z axes and intensity values in expected physical units.
- Cross-check parsed file contents against the draft mzPeak specification (https://hupo-psi.github.io/mzPeak-specification/) to confirm presence of mandatory fields and structural elements; generate compliance report with 100% mandatory field presence for valid files.

## Limitations

- Python and R implementations support reading only; writing mzPeak files requires the Rust implementation.
- Null-marked m/z reconstruction relies on a quadratic spacing model (δ mz ~ β₀ + β₁ mz + β₂ mz²); reconstruction accuracy depends on goodness-of-fit of this model and is not suitable for spectra with highly irregular m/z spacing.
- Zero run stripping removes all but first and last zero-intensity points in profile data; this is lossy for sparse data regions and not reversible.
- The mzPeak format is work-in-progress with no stability guarantee; Parquet schemas and archive structure may change, breaking backwards compatibility.
- Packed parallel table structure (spectra_metadata.parquet, chromatograms_metadata.parquet) requires careful null-handling; nested struct/group columns may be null at any level, which some tools may not handle gracefully.

## Evidence

- [readme] mzPeak is a archive of multiple Parquet files, stored directly in an uncompressed ZIP archive. Each Parquet file describes a different facet of the stored mass spectrometry run.: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP](<https://en.wikipedia.org/wiki/ZIP_(file_format)>) archive."
- [readme] The mzPeak archive contains mzpeak_index.json, spectra_metadata.parquet with spectrum metadata and file-level metadata, spectra_data.parquet with signal data, and optional spectra_peaks.parquet with explicit centroids.: "- `mzpeak_index.json`: Definition of the files present in the archive, encoded as JSON. - `spectra_metadata.parquet`: Spectrum level metadata and file-level metadata. - `spectra_data.parquet`:"
- [readme] Spectrum metadata files store multiple schemas in parallel using packed parallel tables (struct/group columns that may be null at any level).: "the `spectra_metadata.parquet` and `chromatograms_metadata.parquet` store multiple schemas in parallel. In these Parquet files, the root schema is made up of several branched "group" or "struct""
- [readme] Null-marked m/z values are reconstructed using a learned m/z spacing model (quadratic form) to achieve lossless or near-lossless reconstruction.: "fit a simple m/z spacing model using weighted least squares of the form: δ mz ~ β₀ + β₁ mz + β₂ mz² + ϵ. Then when reading the the null-marked data, use either the local median δ mz or the learned"
- [readme] Python and R implementations provide read-only access using pyarrow and arrow respectively.: "There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`]. There is also an R implementation in `R/`, which is also a"
- [readme] The mzPeak format is work-in-progress with no stability guarantee.: "**NOTE**: This is a **work in progress**, no stability is guaranteed at this point."
