---
name: spectral-array-extraction-and-reconstruction
description: Use when your input is an mzPeak archive (ZIP of Parquet files) and you
  need to recover spectrum signal data (m/z values and intensities) for downstream
  analysis, visualization, or format conversion. Use this skill when working with
  profile or centroid mode spectra stored in `spectra_data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyarrow
  - arrow (R)
  - Rust mzPeak library
  - NumPy
  - pandas
  techniques:
  - mass-spectrometry
  license_tier: restricted
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.5c00435
  all_source_dois:
  - 10.1021/acs.jproteome.5c00435
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-array-extraction-and-reconstruction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract m/z and intensity arrays from mzPeak Parquet-based mass spectrometry archives and reconstruct the original spectral signal using Arrow-backed columnar storage, with support for point or chunked layouts and optional null-marking restoration. This skill is essential for reading scalable, interoperable mzPeak files in Python, R, or Rust environments.

## When to use

Your input is an mzPeak archive (ZIP of Parquet files) and you need to recover spectrum signal data (m/z values and intensities) for downstream analysis, visualization, or format conversion. Use this skill when working with profile or centroid mode spectra stored in `spectra_data.parquet` or `spectra_peaks.parquet`, especially when the data has been subjected to zero-run stripping or null-marking compression to reduce file size.

## When NOT to use

- Input is not an mzPeak file (e.g., mzML, mzXML, NetCDF, or raw vendor formats) — use format-specific readers instead.
- You only need spectrum-level metadata without signal data — use `spectra_metadata.parquet` directly without invoking array reconstruction.
- You require write access to mzPeak files — the Python and R implementations support reading only; use the Rust implementation for write operations.

## Inputs

- mzPeak archive (ZIP file containing Parquet files)
- spectra_metadata.parquet (spectrum index and metadata)
- spectra_data.parquet (m/z and intensity arrays in point or chunked layout)
- spectra_peaks.parquet (optional centroid data)
- mzpeak_index.json (file resolution and schema definitions)

## Outputs

- Decoded spectrum signal arrays (m/z values, intensity values)
- Spectrum index / run information
- NumPy arrays or pandas DataFrames or Arrow Tables with reconstructed spectra
- Metadata for peak layout (profile vs. centroid mode)

## How to apply

Load the mzPeak archive using Arrow/pyarrow libraries to read the Parquet metadata index (`mzpeak_index.json`) and identify the data layout (point vs. chunked). For point layout, read parallel m/z and intensity arrays with a repeated spectrum index column; for chunked layout, unpack the columnar chunks. If null-marking is present, fit or retrieve a learned m/z spacing model (quadratic polynomial: δmz ~ β₀ + β₁·mz + β₂·mz²) and use the local median or model to reconstruct the m/z values for null-marked points. Return decoded spectra as Arrow Tables or convert to NumPy arrays / pandas DataFrames for downstream use. Validate reconstruction against reference test files to confirm peak apex and centroid accuracy remain unaffected by the compression.

## Related tools

- **pyarrow** (Read and deserialize Parquet columnar data structures from mzPeak archives; decode Arrow-backed m/z and intensity arrays into Python objects) — https://arrow.apache.org/docs/python/index.html
- **arrow (R)** (Read and deserialize Parquet data from mzPeak archives; decode spectra into R data structures (Arrow Tables or tibbles)) — https://arrow.apache.org/docs/r/
- **Rust mzPeak library** (Native read and write support for mzPeak files; command-line tools for format conversion and array extraction) — https://github.com/HUPO-PSI/mzPeak
- **NumPy** (Convert reconstructed spectral arrays to NumPy array objects for numerical analysis and visualization)
- **pandas** (Convert reconstructed spectral arrays to DataFrame format for tabular manipulation and export)

## Examples

```
import pyarrow.parquet as pq; table = pq.read_table('spectra_data.parquet', filters=[('spectrum_index', '==', 1)]); mz = table.column('mz').to_numpy(); intensity = table.column('intensity').to_numpy()
```

## Evaluation signals

- Reconstructed m/z and intensity arrays have non-null values for all signal points and match the spectrum index dimensions.
- Peak apex (maximum intensity point) and centroid (intensity-weighted mean m/z) of reconstructed spectra are numerically identical to reference mzPeak test files (within floating-point tolerance).
- For null-marked spectra, the refitted m/z spacing model (quadratic fit residuals) is < 1 ppm RMSE; reconstructed signal shows no visible distortion in mass accuracy plots.
- Data type consistency: m/z values are 64-bit or 32-bit floats (as per schema), intensities are unsigned integers or floats; no type mismatches or NaN propagation except at intentional null locations.
- File reading completes without schema validation errors; Parquet metadata checksums pass and no corrupt columns are detected.

## Limitations

- The Python and R implementations support reading mzPeak files only; write functionality is not yet available (Rust implementation required for format conversion or authoring).
- Null-marking reconstruction accuracy depends on the quality of the learned m/z spacing model; if the spectrum m/z axis deviates substantially from the quadratic model (e.g., due to instrument calibration drift), reconstruction error may exceed 1 ppm.
- Zero-run stripping is only meaningful for profile mode data; centroid mode spectra stored in `spectra_peaks.parquet` bypass this optimization.
- The mzPeak format is currently a HUPO-PSI working draft with no stability guarantee; future schema changes may break compatibility with older implementations.
- Random access to individual spectral arrays in large archives may require scanning the entire Parquet file's row groups; chunked layout offers better access characteristics than point layout but at the cost of larger file size.

## Evidence

- [intro] complete re-implementation for _reading_ mzPeak files using [`pyarrow`]: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`], and the PyData stack"
- [readme] mzPeak is a archive of multiple [Parquet] files stored in an _uncompressed_ [ZIP] archive: "mzPeak is a archive of multiple [Parquet] files, stored directly in an _uncompressed_ [ZIP] archive"
- [readme] Point layout stores data as-is in parallel arrays alongside a repeated index column: "the point layout stores the data as-is in parallel arrays alongside a repeated index column"
- [readme] Null marking replaces flanking zero intensity points with null m/z and intensity values: "replace the flanking zero intensity points with `null` m/z and intensity values"
- [readme] use either the local median δ mz or the learned model for that spectrum to compute m/z spacing: "use either the local median δ mz or the learned model for that spectrum to compute the m/z spacing for singleton points"
- [readme] The Python codebase does not support writing at this time: "The Python codebase does not support writing at this time although this is subject to change in the future"
- [other] Decode spectral data arrays (m/z values, intensities) from Arrow-backed storage: "Decode spectral data arrays (m/z values, intensities) from Arrow-backed storage"
