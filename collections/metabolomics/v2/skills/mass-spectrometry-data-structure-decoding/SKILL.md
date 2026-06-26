---
name: mass-spectrometry-data-structure-decoding
description: Use when when you have a mzPeak file (uncompressed ZIP archive containing
  Parquet tables) and need to access decoded spectral data arrays (m/z, intensity),
  spectrum metadata (scan descriptors, precursors), or chromatogram data in a form
  suitable for Python/R analysis pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - pyarrow
  - arrow (R package)
  - Rust mzPeak library
  - mzPeak.NET
  - mzpeakts
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- There is also an R implementation in `R/`
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

# mass-spectrometry-data-structure-decoding

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Decode mass spectrometry spectral and chromatographic data from columnar Apache Arrow/Parquet storage formats (mzPeak) into language-native arrays and metadata structures. This skill extracts m/z values, intensities, spectrum-level metadata, and instrument parameters from binary-packed mzPeak archives for downstream analysis.

## When to use

When you have a mzPeak file (uncompressed ZIP archive containing Parquet tables) and need to access decoded spectral data arrays (m/z, intensity), spectrum metadata (scan descriptors, precursors), or chromatogram data in a form suitable for Python/R analysis pipelines. Use this skill when read-only access suffices; do not use if you need to write or modify the mzPeak archive.

## When NOT to use

- You need to write or modify the mzPeak file; current Python and R implementations support reading only.
- Input is in a different mass spectrometry format (mzML, mzXML, NetCDF); use format-specific parsers instead.
- You require streaming or lazy evaluation of spectra on a very large archive; point layout is fully in-memory.

## Inputs

- mzPeak archive file (.zip containing Parquet tables)
- mzpeak_index.json manifest (defines file layout and controlled vocabulary references)
- spectra_metadata.parquet (spectrum descriptors, scans, precursors, selected ions)
- spectra_data.parquet (m/z and intensity arrays in point or chunked layout)
- chromatograms_metadata.parquet (optional, chromatogram descriptors)
- chromatograms_data.parquet (optional, time and intensity arrays)

## Outputs

- Decoded spectrum metadata as pandas DataFrame or R data.frame (scan index, retention time, precursor m/z, charge, isolation window)
- m/z array (float array, 32- or 64-bit)
- intensity array (float array, 32- or 64-bit)
- Spectrum-level metadata as list or S3 object keyed by spectrum index
- Reconstructed signal arrays with null-marked gaps filled using learned m/z spacing model (if applicable)
- Chromatogram data as time-series arrays (optional)

## How to apply

Load the mzPeak archive and parse the `mzpeak_index.json` manifest to locate the relevant Parquet files. Use pyarrow (Python) or arrow (R) to read the columnar schema from `spectra_metadata.parquet` and `spectra_data.parquet` (or `chromatograms_metadata.parquet` / `chromatograms_data.parquet` for chromatograms). Decode spectrum-level metadata (scan index, precursor m/z, charge state) from packed parallel table structures in the metadata file. Extract signal arrays (m/z and intensity, or time and intensity for chromatograms) from the data file, respecting the layout (point or chunked) and applying null-marking reconstruction or zero-run stripping reversal if present. Return the decoded contents as native data structures: Python NumPy arrays or pandas DataFrames, or R lists/data.frames. Validate that reconstructed spectra match reference test files to confirm lossless or acceptable lossy recovery.

## Related tools

- **pyarrow** (Read Apache Arrow columnar format from Parquet tables and decode mzPeak binary/columnar data structures into Python-native NumPy and pandas objects) — https://arrow.apache.org/docs/python/index.html
- **arrow (R package)** (Read Apache Arrow columnar format from Parquet tables and decode mzPeak structures into R lists, data.frames, or S3 objects) — https://arrow.apache.org/docs/r/
- **Rust mzPeak library** (Reference implementation with full read and write support; provides CLI tools for converting legacy formats (mzML, mzXML) into mzPeak) — https://github.com/HUPO-PSI/mzPeak
- **mzPeak.NET** (C# implementation for reading mzPeak files in .NET environments) — https://github.com/HUPO-PSI/mzPeak.NET
- **mzpeakts** (TypeScript/JavaScript implementation with online interactive demo for browser-based mzPeak visualization and decoding) — https://github.com/HUPO-PSI/mzpeakts

## Examples

```
import pyarrow.parquet as pq; import json; index = json.load(open('mzpeak_index.json')); metadata = pq.read_table('spectra_metadata.parquet'); data = pq.read_table('spectra_data.parquet'); spectra = {idx: {'mz': data.column('mz').slice(start, end).to_pylist(), 'intensity': data.column('intensity').slice(start, end).to_pylist()} for idx, (start, end) in enumerate(zip(data.column('spectrum_index').to_pylist()[:-1], data.column('spectrum_index').to_pylist()[1:]))}
```

## Evaluation signals

- Decoded m/z and intensity arrays match reference mzPeak test files (lossless or within documented lossy bounds for null-marked spectra using learned m/z spacing model)
- Spectrum metadata (scan index, precursor m/z, charge state, isolation window) are correctly extracted and align with spectra_metadata.parquet schema
- Null-marked gaps in point-layout data are correctly reconstructed using the fitted m/z spacing model δmz ~ β₀ + β₁·mz + β₂·mz²; reconstruction error on the thresholds shown in Thermo and Sciex figures
- Zero-run stripping is correctly reversed: isolated non-zero intensity points are recovered without spurious intensity values in the gaps
- Parquet validity buffer bits (null flags) are honored: m/z and intensity values marked null are not materialized during decoding

## Limitations

- Read-only access: Python and R implementations do not support writing or modifying mzPeak archives (Rust implementation is the reference for write support).
- No stability guaranteed: mzPeak is a work in progress and the format specification may change; no version-level backward compatibility is assured.
- Null-marking reconstruction depends on a learned polynomial model; very sparse spectra or non-smooth m/z spacing may produce reconstruction artifacts that exceed the model fit error shown in reference figures.
- Point layout loads entire spectrum arrays into memory; very large spectra or archives may exceed available RAM.
- Parquet metadata extraction is sensitive to correct JSON encoding in the Parquet metadata segment; malformed file-level metadata will cause decoding failures.

## Evidence

- [intro] The Python implementation is a complete re-implementation for reading mzPeak files using pyarrow and the PyData stack, with read-only functionality and no writing support currently available.: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`] and the PyData stack. The Python codebase does not support writing at this time"
- [intro] The R implementation uses the arrow package to read and decode mzPeak files for read-only access.: "re-implementation using the [`arrow`] for _reading_ only at this time"
- [readme] mzPeak archives contain multiple Parquet files that encode spectrum metadata, data arrays, and metadata in packed parallel table structures.: "archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP] archive. Each Parquet file describes a different facet of the stored mass spectrometry run."
- [readme] The spectra_metadata.parquet and chromatograms_metadata.parquet use packed parallel tables with branched struct groups that may be null.: "root schema is made up of several branched "group" or "struct" (Parquet vs. Arrow nomenclature) that may be null at any level"
- [readme] Null-marked data uses a learned m/z spacing model to reconstruct gaps during decoding.: "fit a simple m/z spacing model using weighted least squares... Then when reading the the null-marked data, use either the local median δ mz or the learned model for that spectrum to compute the m/z"
- [readme] Zero-run stripping removes most zero intensity points, leaving only the first and last in each gap.: "all but the first and last zero intensity points are removed. This is only meaningful for profile data."
- [readme] mzPeak is a work in progress with no stability guaranteed.: "This is a **work in progress**, no stability is guaranteed at this point"
