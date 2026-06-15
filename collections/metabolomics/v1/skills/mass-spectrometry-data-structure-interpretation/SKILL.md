---
name: mass-spectrometry-data-structure-interpretation
description: Use when you have received an mzPeak archive (a ZIP file containing Parquet tables) and need to understand its internal structure, validate that spectrum metadata aligns with signal data, reconstruct m/z and intensity arrays (especially when null marking or zero-run stripping is present), or verify.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - OpenMS
  - R
  - arrow (R package)
  - pyarrow (Python library)
  - Rust mzPeak implementation
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
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

# mass-spectrometry-data-structure-interpretation

## Summary

Interpret and validate mass spectrometry spectral data organized within mzPeak's Parquet-based archive format, which stores spectra metadata, signal arrays, and instrument metadata in separate structured tables. This skill is essential when working with next-generation MS data that must preserve both profile/centroid modes, handle sparse m/z arrays via zero-run stripping, and reconstruct signal from null-marked gaps.

## When to use

You have received an mzPeak archive (a ZIP file containing Parquet tables) and need to understand its internal structure, validate that spectrum metadata aligns with signal data, reconstruct m/z and intensity arrays (especially when null marking or zero-run stripping is present), or verify that the archive conforms to the mzPeak specification before downstream analysis. This is especially critical when the archive uses lossless compression techniques like null marking with learned m/z spacing models, requiring knowledge of the packing scheme to correctly interpret gaps.

## When NOT to use

- Input is already a conventional mzML or NetCDF file—use format-specific readers (e.g., mzMLreader) instead before converting to mzPeak.
- Your analysis requires write access to the mass spectrometry archive (Python and R implementations only support reading; the Rust implementation is required for writing).
- You do not need the full structured metadata and are only interested in raw m/z–intensity pairs; a simpler text export may suffice.

## Inputs

- mzPeak archive (ZIP containing mzpeak_index.json and Parquet files: spectra_metadata.parquet, spectra_data.parquet, optional spectra_peaks.parquet)
- spectra_metadata.parquet (Parquet table with packed parallel struct columns for spectrum descriptions, scans, precursors, selected ions)
- spectra_data.parquet (Parquet table with m/z and intensity arrays in point or chunked layout, possibly null-marked or zero-run-stripped)
- mzpeak_index.json (JSON manifest of archive contents)

## Outputs

- Validated spectrum-by-spectrum tabular representation (data frame or table) with reconstructed m/z arrays, intensity values, and associated metadata (scan ID, precursor m/z, retention time, etc.)
- Interpretable signal data with gaps and null values correctly resolved using spacing models
- Metadata validation report confirming alignment between spectra_metadata and spectra_data indices and field integrity

## How to apply

Open the mzPeak archive and inspect its JSON index (`mzpeak_index.json`) to identify which Parquet files are present. Load `spectra_metadata.parquet` to examine the packed parallel table structure—note that multiple schemas (spectrum descriptions, scans, precursors, selected ions) are branched as struct/group columns that may be null at any level. Next, load `spectra_data.parquet` and determine whether data is in point layout (parallel m/z and intensity arrays with a repeated spectrum_index) or chunked layout (which may carry Numpress compression). For point layout with zero-run stripping, verify that consecutive zero-intensity values have been stripped except at boundaries; for null-marked spectra, use the stored m/z spacing model (or fitted polynomial: δmz ~ β₀ + β₁·mz + β₂·mz²) to reconstruct the null-marked m/z values before peak detection. Validate that each spectrum_index in the data table matches a corresponding spectrum in metadata. Cross-check file-level metadata stored in Parquet JSON segments against the specification's controlled vocabulary terms.

## Related tools

- **arrow (R package)** (Parquet file reader for R; enables loading and parsing spectra_metadata.parquet and spectra_data.parquet into R data frames with correct struct/list column handling) — https://arrow.apache.org/docs/r/
- **pyarrow (Python library)** (Parquet file reader and query interface for Python; provides read-only access to mzPeak Parquet tables and supports nested struct column inspection) — https://arrow.apache.org/docs/python/index.html
- **Rust mzPeak implementation** (Full read and write support; provides reference implementation for interpreting null marking, zero-run stripping, point vs. chunked layouts, and m/z spacing models) — https://github.com/HUPO-PSI/mzPeak
- **OpenMS** (Trusted holder of mzPeak trademark and potential integration point for format validation and inter-conversion with mzML)

## Examples

```
library(arrow); mz_data <- read_parquet('spectra_data.parquet'); metadata <- read_parquet('spectra_metadata.parquet'); spectrum_ids <- unique(mz_data$spectrum_index); validated <- merge(mz_data, metadata[, c('spectrum_id', 'scan_id', 'precursor_mz')], by.x='spectrum_index', by.y='spectrum_id')
```

## Evaluation signals

- Spectrum indices in spectra_data.parquet match exactly with spectrum_index values in spectra_metadata.parquet; no orphaned or missing spectra.
- For null-marked spectra, reconstructed m/z values using the fitted polynomial model deviate from the true m/z by less than the manufacturer's quoted mass accuracy tolerance.
- Zero-run-stripped spectra retain all non-zero intensity points and both flanking zero boundaries; interior zero runs are absent.
- Packed parallel struct columns (precursor, scan, selected_ion) unpack correctly without data loss, and null branches do not corrupt downstream table joins.
- File-level metadata (instrument description, software, data processing pipeline) parse as valid JSON and resolve against the mzPeak JSON schema in the specification's `schema/` directory.

## Limitations

- The mzPeak format is currently work-in-progress with no stability guarantee; file structure or column schemas may change.
- Python and R implementations support reading only; write/update operations require the Rust implementation.
- Zero-run stripping and null marking introduce lossless reconstruction requirements; peak apex and centroid errors are expected to be minute but can accumulate under low-intensity or high-noise conditions.
- Parquet's struct columns require language-specific unnesting/flattening; naive row iteration may treat struct fields as opaque objects rather than individual columns.
- Numpress-compressed data (when present in chunked layout) requires separate decompression before m/z reconstruction; mzPeak readers must explicitly handle this.
- The specification is still a living document (draft); check the latest version at https://hupo-psi.github.io/mzPeak-specification/ for schema updates.

## Evidence

- [readme] Archive index and Parquet structure: "mzPeak is a archive of multiple Parquet files, stored directly in an _uncompressed_ ZIP archive. Each Parquet file describes a different facet of the stored mass spectrometry run."
- [readme] Packed parallel table schema in metadata: "the root schema is made up of several branched 'group' or 'struct' (Parquet vs. Arrow nomenclature) that may be null at any level"
- [readme] Zero-run stripping process: "When storing spectrum data, some vendors will produce arrays with lots of 'empty' regions filled with zero intensity values along a semi-regularly spaced m/z axis. These regions hold little"
- [readme] Null marking and m/z spacing reconstruction: "we can instead replace the flanking zero intensity points with `null` m/z and intensity values and use either the local median δmz or the learned model for that spectrum to compute the m/z spacing"
- [intro] R implementation capability: "There is also an R implementation in `R/`, which is also a complete re-implementation using the [`arrow`] for _reading_ only at this time"
- [readme] Point vs. chunked layout definitions: "Spectrum signal data in either profile or centroid mode. May be in point layout or chunked layout which have different size and random access characteristics."
- [intro] Work-in-progress status and stability: "This is a **work in progress**, no stability is guaranteed at this point."
