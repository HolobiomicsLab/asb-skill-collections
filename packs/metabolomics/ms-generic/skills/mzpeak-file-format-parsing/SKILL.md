---
name: mzpeak-file-format-parsing
description: Use when when you have mass spectrometry data stored in mzPeak format (ZIP archive containing Parquet files) and need to read spectrum metadata, chromatogram metadata, and signal data (m/z and intensity arrays) for analysis. Use this skill if your input is an .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pyarrow
  - R
  - arrow (R package)
  - Rust mzPeak library
  - mzPeak specification
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- complete re-implementation for _reading_ mzPeak files using [`pyarrow`]
- There is also an R implementation in `R/`
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

# mzPeak File Format Parsing

## Summary

Parse mass spectrometry spectral and chromatographic data from mzPeak archives—a Parquet-based, ZIP-containerized format—using language-specific libraries (Rust, Python/pyarrow, R/arrow) to extract decoded spectra, metadata, and signal arrays for downstream analysis.

## When to use

When you have mass spectrometry data stored in mzPeak format (ZIP archive containing Parquet files) and need to read spectrum metadata, chromatogram metadata, and signal data (m/z and intensity arrays) for analysis. Use this skill if your input is an .mzpeak file or an uncompressed ZIP containing mzpeak_index.json and parquet files like spectra_metadata.parquet, spectra_data.parquet, and chromatograms_data.parquet.

## When NOT to use

- Input is in a different mass spectrometry format (mzML, mzXML, netCDF, vendor proprietary formats)—use format-specific parsers instead.
- You need write access to the mzPeak file—current Python and R implementations support read-only access; use the Rust implementation for writing.
- Your goal is to convert FROM mzPeak to another format—use the separate mzPeak conversion tools rather than this parsing skill alone.

## Inputs

- mzPeak archive file (.mzpeak or ZIP containing mzpeak_index.json and Parquet files)
- mzpeak_index.json (JSON definition of archive contents)
- spectra_metadata.parquet (spectrum-level metadata with packed parallel tables)
- spectra_data.parquet (signal arrays in point or chunked layout)
- spectra_peaks.parquet (optional centroid data)
- chromatograms_metadata.parquet (chromatogram-level metadata)
- chromatograms_data.parquet (chromatogram signal data)

## Outputs

- Decoded spectrum metadata (scan descriptions, precursors, selected ions)
- Decoded chromatogram metadata
- m/z and intensity arrays (Python: NumPy arrays or pandas DataFrames; R: data frames or lists; Rust: native structures)
- File-level metadata (instrument description, software, data transformation pipeline) as JSON or structured objects
- Spectrum and chromatogram indices and descriptors

## How to apply

First, verify the mzPeak archive structure by checking for mzpeak_index.json and expected Parquet files (spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, chromatograms_data.parquet). Open the ZIP container and load each Parquet file using your language's Arrow implementation (pyarrow for Python, arrow for R, or the Rust library). Decode packed parallel table structures in metadata files—these contain nested groups (spectrum descriptions, scans, precursors, selected ions) that may be null at any level. For signal data, reconstruct m/z and intensity arrays; if null-marked data is present, use the stored m/z spacing model or local median delta-mz to recover null positions. Validate that decoded arrays match the expected schema and that spectrum indices align across metadata and signal tables.

## Related tools

- **pyarrow** (Parse and decode Parquet files in Python; read Apache Arrow columnar format and return decoded spectra as NumPy arrays or pandas DataFrames) — https://arrow.apache.org/docs/python/index.html
- **arrow (R package)** (Read and decode mzPeak files in R using Arrow columnar format; return decoded contents as R data structures (lists or S3 objects)) — https://arrow.apache.org/docs/r/
- **Rust mzPeak library** (Native Rust implementation for reading and writing mzPeak files; includes command-line tools for converting existing formats into mzPeak) — https://github.com/HUPO-PSI/mzPeak
- **mzPeak specification** (Reference documentation for mzPeak format schema, Parquet layouts, zero-run stripping, null-marking, and point/chunked layout data array schemas) — https://github.com/HUPO-PSI/mzPeak-specification

## Evaluation signals

- Verify that parsed spectrum indices are contiguous and match row counts across spectra_metadata.parquet and spectra_data.parquet
- Confirm that m/z and intensity arrays are non-empty and have matching lengths within each spectrum
- For null-marked data, validate that reconstructed m/z values fall within expected range and follow delta-mz spacing model; check that peak apexes remain unchanged after null reconstruction
- Confirm that all packed parallel table branches (spectrum descriptions, scans, precursors, selected ions) deserialize correctly and nested nulls are preserved as expected
- Cross-check file-level metadata JSON schema against the corresponding JSONSchema in schema/ directory for compliance

## Limitations

- Python and R implementations support read-only access; writing is not currently available (Rust implementation supports both read and write).
- The mzPeak format is a work in progress with no stability guaranteed; API and schema may change between versions.
- Zero-run stripping and null-marking are lossy transformations; reconstructed m/z for null-marked data may have minute angle changes if only 3 points compose a peak.
- Numpress compression (when applied) requires chunked layout and carries slightly larger loss of accuracy than null-marking alone.

## Evidence

- [readme] mzPeak is a archive of multiple Parquet files, stored directly in an uncompressed ZIP archive: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP]"
- [intro] Complete re-implementation for reading mzPeak files using pyarrow and PyData stack: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`]"
- [intro] R implementation also complete re-implementation using arrow package for reading only: "re-implementation using the [`arrow`](https://arrow.apache.org/docs/r/) for _reading_ only"
- [readme] Packed parallel tables store multiple schemas in parallel with potential nulls at any level: "the root schema is made up of several branched "group" or "struct" (Parquet vs. Arrow nomenclature) that may be null at any level"
- [readme] Null-marked data uses m/z spacing model to reconstruct null positions while preserving peak apex: "use either the local median $δ mz$ or the learned model for that spectrum to compute the m/z spacing for singleton points to achieve an very accurate reconstruction. Because the non-zero m/z points"
- [readme] Components include mzpeak_index.json, spectra_metadata.parquet, spectra_data.parquet, and optional spectra_peaks.parquet: "- `mzpeak_index.json`: Definition of the files present in the archive, encoded as JSON. - `spectra_metadata.parquet`: Spectrum level metadata - `spectra_data.parquet`: Spectrum signal data -"
- [intro] Python implementation does not support writing; read-only functionality available: "The Python codebase does not support writing at this time"
