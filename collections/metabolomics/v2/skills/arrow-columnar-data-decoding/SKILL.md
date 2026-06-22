---
name: arrow-columnar-data-decoding
description: Use when when reading mzPeak files or other Parquet-backed mass spectrometry archives where spectral m/z and intensity arrays are stored in columnar layouts (point or chunked format) and you need to reconstruct them into Python NumPy arrays, pandas DataFrames, or equivalent in-memory structures for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pyarrow
  - arrow
  - Rust mzPeak implementation
  - mzPeak specification
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- complete re-implementation for _reading_ mzPeak files using [`pyarrow`]
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

# arrow-columnar-data-decoding

## Summary

Decode mass spectrometry spectral data (m/z values, intensities) from Apache Arrow columnar storage formats (Parquet) using language-specific Arrow libraries. This skill reconstructs spectrum arrays and metadata from scalable, interoperable columnar archives.

## When to use

When reading mzPeak files or other Parquet-backed mass spectrometry archives where spectral m/z and intensity arrays are stored in columnar layouts (point or chunked format) and you need to reconstruct them into Python NumPy arrays, pandas DataFrames, or equivalent in-memory structures for downstream analysis or visualization.

## When NOT to use

- Input is already in memory-resident format (e.g., NumPy array, pandas DataFrame) — skip columnar decoding and proceed directly to analysis.
- You need to write or modify mzPeak files — Python and R implementations support read-only access; use the Rust implementation for write operations.
- The mzPeak archive uses unsupported Parquet compression or data types not yet available in your Arrow library version — check schema compatibility before decoding.

## Inputs

- mzPeak archive (ZIP containing Parquet files)
- spectra_data.parquet (Parquet file with m/z, intensity, spectrum_index columns)
- spectra_metadata.parquet (Parquet file with spectrum metadata and m/z spacing models)
- Apache Arrow binary data in columnar layout

## Outputs

- Decoded spectrum arrays as NumPy arrays or pandas DataFrame
- In-memory columnar representation (Arrow RecordBatch or Table)
- Reconstructed m/z and intensity point clouds per spectrum
- Spectrum-level metadata linked to decoded data

## How to apply

Use the appropriate Apache Arrow language binding (pyarrow for Python, arrow for R) to open the Parquet file(s) within the mzPeak archive (e.g., `spectra_data.parquet`). Read the columnar data using Arrow's table API, which loads the data into memory-mapped or native column-oriented structures. Decode the spectrum_index column alongside the parallel m/z and intensity arrays to reconstruct individual spectrum signals; for spectra with null-marked gaps or zero-run stripping, use the spectrum metadata (e.g., m/z spacing model parameters stored in spectra_metadata.parquet) to accurately impute missing values. Finally, convert the Arrow table columns into NumPy arrays or pandas Series for compatibility with existing proteomics workflows. Validation should confirm that centroid or profile peak positions and intensities match reference spectra and that no data loss occurs beyond the intentional lossless compression applied (zero-run stripping, null marking).

## Related tools

- **pyarrow** (Python library for reading Parquet columnar data and decoding Arrow-backed mzPeak spectra arrays) — https://arrow.apache.org/docs/python/index.html
- **arrow** (R library for reading Parquet columnar data and decoding Arrow-backed mzPeak spectra arrays) — https://arrow.apache.org/docs/r/
- **Rust mzPeak implementation** (Reference library for reading and writing mzPeak files; supports both columnar decoding and format specification) — https://github.com/HUPO-PSI/mzPeak
- **mzPeak specification** (HUPO-PSI specification document defining Parquet schemas, columnar layouts, and metadata structures for decoding) — https://github.com/HUPO-PSI/mzPeak-specification

## Examples

```
import pyarrow.parquet as pq; table = pq.read_table('spectra_data.parquet'); spectra_df = table.to_pandas(); m_z_array = spectra_df[spectra_df['spectrum_index'] == 0]['mz'].to_numpy(); intensity_array = spectra_df[spectra_df['spectrum_index'] == 0]['intensity'].to_numpy()
```

## Evaluation signals

- Decoded m/z and intensity arrays match the dimensionality and value ranges in the source Parquet columns (e.g., no truncation or type conversion errors).
- For null-marked or zero-run-stripped spectra, reconstructed m/z spacing using the stored model parameters recovers original peak positions and centroids within machine precision (floating-point rounding only).
- Spectrum-level metadata (e.g., scan number, precursor m/z, retention time) correctly links to decoded data via spectrum_index.
- Conversion to NumPy or pandas preserves column order, data types (float32/float64), and null/NaN semantics from Arrow representation.
- Round-trip validation: decode, re-encode to Arrow, and confirm bitwise or numerical equivalence with original Parquet (post-lossy compression).

## Limitations

- Python and R implementations are read-only; writing or modifying decoded spectra and re-encoding to mzPeak requires the Rust implementation or manual Parquet writing code.
- mzPeak format is a work in progress with no stability guarantee; schema and API may change between versions, potentially breaking backward compatibility of archived files.
- Large archives with many spectra may exceed available RAM if loaded entirely into memory; streaming or chunked decoding strategies needed for production pipelines.
- Reconstruction of null-marked spectra relies on accurate m/z spacing model coefficients (β₀, β₁, β₂) stored in metadata; model fit errors propagate into imputed m/z values.
- Parquet compression (Snappy, Gzip) and zero-run stripping are lossless, but Numpress compression (if applied) introduces intentional lossy compression; users must choose encoding strategy upfront.

## Evidence

- [intro] Python re-implementation for reading mzPeak using pyarrow: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`]"
- [readme] Arrow-backed spectrum data decoding workflow: "When storing data arrays, the point layout stores the data as-is in parallel arrays alongside a repeated index column."
- [readme] Columnar Parquet structure for spectra_data: "`spectra_data.parquet`: Spectrum signal data in either profile or centroid mode. May be in point layout or chunked layout"
- [readme] Read-only scope for Python implementation: "The Python codebase does not support writing at this time although this is subject to change in the future."
- [readme] Null marking and m/z spacing model reconstruction: "Then when reading the the null-marked data, use either the local median δ mz or the learned model for that spectrum to compute the m/z spacing for singleton points"
- [readme] Work-in-progress format stability caveat: "**NOTE**: This is a **work in progress**, no stability is guaranteed at this point."
