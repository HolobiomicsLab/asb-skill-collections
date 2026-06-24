---
name: python-binary-io-and-serialization
description: Use when when you have mzPeak files (Parquet-based archives in uncompressed
  ZIP containers) or other PyArrow-compatible columnar formats containing mass spectrometry
  spectra, and you need to extract and decode spectral data arrays (m/z values, intensities)
  into Python memory for downstream.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyarrow
  - Python
  - PyArrow
  - NumPy
  - pandas
  - mzPeak Rust implementation
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- complete re-implementation for _reading_ mzPeak files using [`pyarrow`]
- There is a separate Python implementation in `python/`
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

# Python Binary I/O and Serialization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse and reconstruct mass spectrometry spectral data from binary or columnar file formats using PyArrow and the PyData stack, enabling read-only access to mzPeak files and conversion of raw spectra into Python-native data structures. This skill addresses the need to deserialize compact, archive-based MS data formats into analysis-ready NumPy arrays and pandas DataFrames.

## When to use

When you have mzPeak files (Parquet-based archives in uncompressed ZIP containers) or other PyArrow-compatible columnar formats containing mass spectrometry spectra, and you need to extract and decode spectral data arrays (m/z values, intensities) into Python memory for downstream analysis, filtering, or visualization. Use this when read-only access is acceptable and you want to avoid implementing format-specific binary parsing logic.

## When NOT to use

- Writing or modifying mzPeak files—the Python implementation supports reading only; use the Rust implementation for write operations.
- Working with already-decoded spectral data or feature tables in memory—this skill is for initial deserialization from archive format, not downstream processing.
- Formats other than mzPeak or Arrow-compatible columnar storage—use format-specific parsers for mzML, mzXML, or netCDF.
- Real-time or streaming applications requiring random access to individual spectra without full archive decompression—mzPeak supports point layout for this, but architecture must account for ZIP constraints.

## Inputs

- mzPeak archive (ZIP file containing Parquet tables and mzpeak_index.json)
- Parquet files (spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, chromatograms_data.parquet)
- mzPeak file format specification (HUPO-PSI reference or inline schema documentation)

## Outputs

- Decoded spectral data as NumPy arrays (m/z and intensity parallel arrays)
- Spectrum metadata as pandas DataFrames (spectrum descriptions, scan indices, precursor info)
- Reconstructed m/z spacing models for null-marked regions (polynomial coefficients or local medians)
- Python-native spectrum objects or tabular representations ready for analysis

## How to apply

Set up a Python environment with pyarrow and PyData stack dependencies (NumPy, pandas). Open the mzPeak archive and locate the relevant Parquet files (spectra_metadata.parquet, spectra_data.parquet, or spectra_peaks.parquet) using the mzpeak_index.json manifest. Use PyArrow's Table and RecordBatch readers to deserialize columnar data, then decode spectral arrays by handling packed parallel table schemas, zero run stripping, null marking, and point/chunked layouts as appropriate to your data. Validate reconstruction by comparing decoded m/z spacing and intensity distributions against reference spectra or expected signal properties (peak apex positions, centroid calculations should be unaffected by lossless transformations).

## Related tools

- **PyArrow** (Core library for reading and deserializing Parquet columnar data from mzPeak archives; handles null marking, array decoding, and schema validation) — https://arrow.apache.org/docs/python/index.html
- **NumPy** (Host and manipulate decoded m/z and intensity arrays after PyArrow deserialization; supports mathematical operations and peak detection on spectral data)
- **pandas** (Convert Parquet metadata tables to DataFrames for spectrum-level annotations, filtering by scan properties, and joining spectral data with metadata)
- **mzPeak Rust implementation** (Reference implementation providing conversion tools and write support for creating mzPeak files; Python implementation is a read-only re-implementation based on this) — https://github.com/HUPO-PSI/mzPeak

## Examples

```
import pyarrow.parquet as pq; import zipfile; z = zipfile.ZipFile('sample.mzpeak'); metadata = pq.read_table(z.open('spectra_metadata.parquet')); data = pq.read_table(z.open('spectra_data.parquet')); df = metadata.to_pandas(); spectra = {row['spectrum_id']: data.filter(data['spectrum_index'] == row['spectrum_index']).to_pandas() for _, row in df.iterrows()}
```

## Evaluation signals

- Decoded m/z and intensity arrays match reference test spectra in shape, data type, and value ranges (peak positions, centroid calculations invariant under lossless transformations)
- Null-marked regions reconstruct correctly: repopulated m/z values fall within tolerance of original or fitted m/z spacing model; intensity values match non-null points
- Zero run stripping validation: reconstructed spectra contain original non-zero intensity points and flanking zeros, with no missing peaks or artifacts
- Parquet schema validation: spectrum_index, mz, intensity columns successfully read; packed parallel table structures (scan, precursor, selectedIon groups) parse without null type errors
- Metadata-data joins succeed: spectrum count in metadata matches row count in spectra_data; scan indices and precursor references are consistent across files

## Limitations

- Read-only access: The Python implementation does not support writing mzPeak files; writing operations require the Rust implementation.
- Work-in-progress format: mzPeak specification is still in draft status; no stability is guaranteed, and breaking changes to the Parquet schema or ZIP structure may require code updates.
- Zero run stripping and null marking introduce lossy approximations: m/z spacing is reconstructed using a polynomial model (δmz ~ β₀ + β₁·mz + β₂·mz²), which may not hold for all instruments or m/z ranges; edge cases with only 1–2 non-zero points cannot be meaningfully modeled.
- Large file handling: ZIP-based archives do not support true streaming; entire file must be decompressed into memory or temporary storage before Parquet reading.
- Chunked layout complexity: Numpress-compressed data (available in chunked layout) requires additional decompression logic beyond standard Parquet column reading; not all compressions may be supported in the Python implementation.

## Evidence

- [intro] The Python implementation is a complete re-implementation for reading mzPeak files using pyarrow and the PyData stack, with read-only functionality.: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`](https://arrow.apache.org/docs/python/index.html), and the PyData stack. The Python codebase does not support writing at this"
- [readme] mzPeak is a Parquet-based archive format with specific file structure including metadata and spectral data tables.: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP](<https://en.wikipedia.org/wiki/ZIP_(file_format)>)"
- [readme] Spectral data is stored using point or chunked layouts with zero run stripping and optional null marking to compress sparse m/z regions.: "When storing spectrum data, some vendors will produce arrays with lots of "empty" regions filled with zero intensity values... all but the first and last zero intensity points are removed. This is"
- [readme] Null-marked m/z values are reconstructed using a polynomial model fitted to non-null points in order to recover near-lossless representation.: "fit a simple m/z spacing model using weighted least squares of the form: δ mz ∼ β₀ + β₁ mz + β₂ mz² + ϵ"
- [other] The core workflow involves parsing the mzPeak specification and implementing file I/O to return decoded spectra.: "Parse the mzPeak file format specification from the HUPO-PSI repository. Implement file I/O using pyarrow to read mzPeak binary/columnar data structures. Decode spectral data arrays (m/z values,"
- [other] Validation requires comparing reconstructed spectra to reference test files.: "Validate that the implementation correctly reproduces spectra from reference mzPeak test files."
