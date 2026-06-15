---
name: spectral-data-table-conversion
description: Use when when you have mzPeak format spectrum files and need to work with spectrum metadata, intensity/m/z arrays, or precursor information in a tabular, columnar, or vectorized computing environment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - OpenMS
  - Python
  - pyarrow
  - pandas
  - Python (mzPeak reader module)
  - Rust (mzPeak CLI tools)
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- There is a separate Python implementation in `python/`
- complete re-implementation for _reading_ mzPeak files using [`pyarrow`]
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

# spectral-data-table-conversion

## Summary

Convert mass spectrometry spectrum data from mzPeak file format into structured tabular representations (pandas DataFrame, pyarrow Table, or Parquet/CSV exports) compatible with PyData analysis workflows. This skill enables downstream statistical, machine learning, and exploratory analyses on spectrum metadata and signal arrays.

## When to use

When you have mzPeak format spectrum files and need to work with spectrum metadata, intensity/m/z arrays, or precursor information in a tabular, columnar, or vectorized computing environment. Use this skill when your analysis pipeline requires pandas, polars, DuckDB, or other PyData-stack tools that expect DataFrames or Arrow tables rather than binary spectrum archives.

## When NOT to use

- Input is raw vendor data (mzML, .raw, .d); use vendor-specific readers or mzPeak conversion tools first.
- You need to write or modify mzPeak files; the Python implementation is read-only. Use the Rust implementation for write support.
- Your analysis requires access to chromatogram data; use chromatograms_metadata.parquet and chromatograms_data.parquet tables instead (same workflow applies).

## Inputs

- mzPeak file (uncompressed ZIP archive containing mzpeak_index.json and Parquet files)
- Parquet file paths from within mzPeak archive (spectra_metadata.parquet, spectra_data.parquet, spectra_peaks.parquet)
- Spectrum index or spectrum ID selection (optional filter)

## Outputs

- pandas.DataFrame (in-memory tabular representation of spectrum metadata and/or signal data)
- pyarrow.Table (columnar Arrow table, supports lazy evaluation)
- Parquet file (compressed columnar archive of converted spectrum data)
- CSV file (human-readable flat table export)

## How to apply

Import the Python mzPeak reader module and pyarrow library from the mobiusklein/mzpeak_prototyping repository's `python/` subdirectory. Load the mzPeak archive (an uncompressed ZIP containing Parquet files) using the Python read implementation, which automatically parses the mzpeak_index.json manifest and loads the relevant Parquet tables (spectra_metadata.parquet, spectra_data.parquet, and optional spectra_peaks.parquet). Convert the loaded spectrum data into either a pandas DataFrame for in-memory analysis or a pyarrow Table for lazy/streaming evaluation. Export the result to Parquet for efficient columnar storage or CSV for human inspection and tool interoperability. Key decision: if your workflow requires random-access reads of individual spectra, prefer the point layout representation; if you need compression or streaming, use chunked layout (which may include Numpress compression and requires decoding).

## Related tools

- **pyarrow** (Read mzPeak Parquet files and provide columnar data access; enables conversion to pandas DataFrames and Arrow tables.) — https://arrow.apache.org/docs/python/index.html
- **pandas** (Convert pyarrow tables into in-memory DataFrames for statistical analysis, filtering, and aggregation.)
- **Python (mzPeak reader module)** (Parse mzPeak archive structure, load Parquet manifests, and handle zero-run stripping and null-marking reconstruction.) — https://github.com/mobiusklein/mzpeak_prototyping
- **Rust (mzPeak CLI tools)** (Pre-convert vendor formats (mzML, Thermo, Sciex) into mzPeak archives before Python ingestion.) — https://github.com/HUPO-PSI/mzPeak

## Examples

```
from python.mzpeak import MzPeakReader; import pandas as pd; reader = MzPeakReader('sample.mzpeak'); spectra_meta = reader.spectra_metadata(); spectra_data = reader.spectra_data(); df = pd.concat([spectra_meta, spectra_data.to_pandas()], axis=1); df.to_parquet('converted_spectra.parquet')
```

## Evaluation signals

- Parquet schema validation: verify spectra_metadata.parquet contains expected columns (spectrum_index, precursor, selected_ion groups) and spectra_data.parquet contains mz and intensity arrays with matching dimensions.
- Data shape consistency: row counts in spectra_metadata.parquet match the number of unique spectrum_index values in spectra_data.parquet; no orphaned indices.
- Null reconstruction accuracy: for null-marked m/z values (where the validity buffer indicates missing data), verify reconstructed m/z spacing using the learned polynomial model stays within ±1 ppm of true centroid positions.
- Zero-run stripping preservation: profile data should have removed interior zero-intensity runs while retaining at least the first and last zero point in each gap region.
- Export format completeness: exported Parquet or CSV files contain all spectrum_index values from the original archive with no row loss or duplication.

## Limitations

- Python implementation is read-only; cannot write or modify mzPeak files. Users requiring write capability must use the Rust implementation.
- Null reconstruction accuracy depends on fitting a weighted least-squares polynomial model (δmz ~ β₀ + β₁·mz + β₂·mz²) to non-null points; sparse spectra with < 5 data points may yield unreliable spacing estimates.
- Project is work-in-progress with no stability guarantee; API and file format may change between releases.
- Zero-run stripping and null-marking are lossless only for profile data; centroid or already-processed data may not benefit from these compression techniques.

## Evidence

- [intro] The Python implementation provides a complete re-implementation for reading mzPeak files using the pyarrow library, enabling conversion of mzPeak spectrum data into structured tabular artifacts compatible with the PyData stack.: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`]"
- [intro] Workflow steps documented in task_id=task_002 on reading and exporting spectrum data.: "1. Clone or access the mobiusklein/mzpeak_prototyping repository and navigate to the python/ subdirectory. 2. Import the Python mzPeak reader module and pyarrow library. 3. Load the mzPeak file using"
- [readme] mzPeak archive structure and Parquet file organization.: "mzPeak is a archive of multiple Parquet files, stored directly in an _uncompressed_ ZIP archive. Each Parquet file describes a different facet of the stored mass spectrometry run."
- [readme] Null-marking reconstruction method for sparse profile data.: "we can instead replace the flanking zero intensity points with `null` m/z and intensity values and Parquet will skip storing the expensive 32- and/or 64-bit values, retaining only the validity buffer"
- [readme] Python implementation read-only limitation.: "The Python codebase does not support writing at this time although this is subject to change in the future."
- [readme] mzPeak components and metadata structure.: "`spectra_metadata.parquet`: Spectrum level metadata and file-level metadata. Includes spectrum descriptions, scans, precursors, and selected ions using packed parallel tables."
