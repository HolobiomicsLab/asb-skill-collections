---
name: apache-arrow-columnar-format-parsing
description: Use when you have mzPeak files stored as Parquet tables within a ZIP archive and need to load spectrum metadata, chromatogram metadata, signal data (profile or centroid), or peaks into memory for analysis in R, Python, or another Arrow-supported language.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - arrow
  - R
  - pyarrow
  - arrow (R package)
  - Parquet
  - mzPeak Rust implementation
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- R implementation in `R/`, which is also a complete re-implementation using the [`arrow`](https://arrow.apache.org/docs/r/) for _reading_ only
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Apache Arrow Columnar Format Parsing

## Summary

Parse and decode Apache Arrow columnar data files (such as Parquet archives) to extract structured mass spectrometry metadata and signal arrays for downstream analysis. This skill enables read-only access to mzPeak files through language-specific Arrow bindings that handle the columnar schema, packed parallel table groups, and optional data transformations like zero run stripping and null marking.

## When to use

You have mzPeak files stored as Parquet tables within a ZIP archive and need to load spectrum metadata, chromatogram metadata, signal data (profile or centroid), or peaks into memory for analysis in R, Python, or another Arrow-supported language. The file format uses packed parallel tables with branched struct groups and optional null marking for sparse m/z arrays, requiring columnar parsing rather than row-oriented deserialization.

## When NOT to use

- Input is in a legacy format (mzML, mzXML, or netCDF) — use format-specific parsers or conversion tools first.
- You need write access to mzPeak files — R and Python implementations support read-only access; use the Rust implementation for read-write capability.
- Data must be analyzed in a tool that does not support Apache Arrow libraries or Parquet deserialization.
- File is a work-in-progress or unstable version of mzPeak (no stability guaranteed until release); validate schema compatibility before committing to production pipelines.

## Inputs

- mzPeak file (ZIP archive containing Parquet tables and mzpeak_index.json)
- Parquet table files (spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, chromatograms_data.parquet)
- mzpeak_index.json (file index with controlled vocabulary mappings)
- JSON Schemas (from schema/ directory for validation)

## Outputs

- In-memory Arrow Tables or language-specific columnar structures (e.g., R data.frame, Python pandas.DataFrame or pyarrow.Table)
- Decoded spectrum metadata (scan descriptions, precursor info, selected ions as nested structs)
- Decoded signal data arrays (m/z, intensity; point or chunked layout)
- Reconstructed m/z values for null-marked sparse regions (if applicable)
- Decoded chromatogram metadata and signal data

## How to apply

Load the mzPeak file (an uncompressed ZIP containing Parquet tables) using the Apache Arrow library for your language (pyarrow for Python, arrow for R). Use the Arrow schema reader to identify the available tables (spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, chromatograms_data.parquet, and optional spectra_peaks.parquet). Parse the mzpeak_index.json file to resolve controlled vocabulary terms and locate specific data files within the archive. Read each Parquet table into an in-memory columnar representation (e.g., Arrow Table or RecordBatch). For tables using packed parallel structs (e.g., precursors, selected_ions), navigate the branched group hierarchy to extract nested fields. If null marking is present in sparse m/z arrays, reconstruct the full m/z spacing using either the local median δmz or a fitted model (polynomial of degree ≤2 in m/z) before returning decoded data structures. Verify schema consistency against the JSON Schemas in schema/ and confirm that all expected columns are present and correctly typed.

## Related tools

- **pyarrow** (Columnar data format parser for reading mzPeak Parquet files in Python; implements Apache Arrow specification for high-performance columnar deserialization) — https://arrow.apache.org/docs/python/index.html
- **arrow (R package)** (Columnar data format parser for reading mzPeak Parquet files in R; binds to Apache Arrow C++ library for efficient column-based access and schema navigation) — https://arrow.apache.org/docs/r/
- **Parquet** (Underlying columnar storage format used in mzPeak; all metadata and signal data are stored as Parquet tables with schema definitions) — https://parquet.apache.org/
- **mzPeak Rust implementation** (Reference implementation with read and write support; can convert legacy formats to mzPeak and validate schemas during parsing) — https://github.com/HUPO-PSI/mzPeak

## Examples

```
library(arrow); mzpeak_file <- open_dataset('sample.mzPeak'); spectra_meta <- read_parquet(file.path(mzpeak_file, 'spectra_metadata.parquet')); spectra_data <- read_parquet(file.path(mzpeak_file, 'spectra_data.parquet'))
```

## Evaluation signals

- All Parquet tables load without schema errors and column types match the JSON Schema definitions in the mzPeak specification.
- Nested struct groups (e.g., precursors, selected_ions) resolve correctly and all non-null leaf fields are accessible.
- For null-marked m/z arrays, reconstructed m/z spacing errors remain below measurement instrument precision (typically <5 ppm RMS after polynomial model fitting).
- Row counts across parallel metadata and data tables are consistent (spectrum indices map to row indices in data tables); no orphaned or duplicate entries.
- Output data structures preserve column-oriented access patterns and can be serialized/validated against the mzpeak_index.json controlled vocabulary mappings without loss.

## Limitations

- R and Python implementations support read-only access; write operations require the Rust implementation or manual schema authoring.
- mzPeak is a work-in-progress specification with no stability guaranteed; breaking changes may occur before official release, requiring schema migration.
- Zero run stripping and null marking are optional transformations; parsers must check metadata flags to determine which reconstruction method to apply; errors in model fitting can introduce small m/z spacing artifacts.
- Packed parallel table groups may contain null values at any level, requiring defensive null-checking when extracting nested fields; missing precursors or selected ions do not indicate file corruption but reflect sparse experimental metadata.
- Large mzPeak archives may exceed available RAM when loaded entirely into columnar format; chunked iteration or lazy evaluation strategies are not yet standardized across Arrow bindings.

## Evidence

- [intro] using the [`arrow`](https://arrow.apache.org/docs/r/) for _reading_ only at this time: "There is also an R implementation in `R/`, which is also a complete re-implementation using the [`arrow`](https://arrow.apache.org/docs/r/) for _reading_ only at this time."
- [intro] complete re-implementation for _reading_ mzPeak files using [`pyarrow`]: "There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`](https://arrow.apache.org/docs/python/index.html)"
- [readme] mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP]: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP](<https://en.wikipedia.org/wiki/ZIP_(file_format)>) archive."
- [readme] mzpeak_index.json: Definition of the files present in the archive, encoded as JSON: "- `mzpeak_index.json`: Definition of the files present in the archive, encoded as JSON. This makes resolving files by controlled terms easier than matching file names."
- [readme] spectra_metadata and chromatograms_metadata store multiple schemas in parallel using branched struct groups: "In these Parquet files, the root schema is made up of several branched "group" or "struct" (Parquet vs. Arrow nomenclature) that may be null at any level."
- [readme] null-marked data uses learned polynomial model for m/z spacing reconstruction: "Then when reading the the null-marked data, use either the local median δ mz or the learned model for that spectrum to compute the m/z spacing"
- [readme] This is a **work in progress**, no stability is guaranteed at this point: "**NOTE**: This is a **work in progress**, no stability is guaranteed at this point."
