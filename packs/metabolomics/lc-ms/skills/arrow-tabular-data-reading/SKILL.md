---
name: arrow-tabular-data-reading
description: Use when when you have Parquet-encoded tabular data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0945
  tools:
  - OpenMS
  - arrow
  - R
  - arrow (R package)
  - pyarrow (Python library)
  - mobiusklein/mzpeak_prototyping
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- complete re-implementation using the [`arrow`] for _reading_ only
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# arrow-tabular-data-reading

## Summary

Read and parse binary tabular data (Parquet files) into structured in-memory columnar representations using Apache Arrow's language bindings. This skill enables efficient, schema-aware loading of mass spectrometry metadata and signal arrays without materializing the entire dataset into memory.

## When to use

When you have Parquet-encoded tabular data (e.g., mzPeak spectrum metadata or chromatogram signal tables) that needs to be loaded into R or Python for downstream analysis, and you want to leverage Arrow's zero-copy, columnar memory layout and lazy evaluation to handle large files efficiently.

## When NOT to use

- Input is already a native in-memory data frame or table—avoid unnecessary Arrow round-trip conversion.
- You need to write or modify Parquet files—R and Python Arrow implementations support read-only access at this time.
- File is in a non-Parquet format (mzML, raw vendor formats, etc.); use format-specific readers instead.

## Inputs

- Parquet file (binary columnar format)
- File path to mzPeak archive component (e.g., spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet)
- Optional: Parquet schema or column selection filter

## Outputs

- Arrow Table (zero-copy columnar in-memory representation)
- Converted data frame (R data.frame or pandas.DataFrame if row-oriented access needed)
- Structured representation of spectrum or chromatogram metadata and signal arrays with validated schema

## How to apply

Load the Arrow library for your language (arrow R package or pyarrow Python package). Open the Parquet file using the library's read function, which automatically infers or respects the Parquet schema. The resulting object is a columnar table (Arrow Table or RecordBatch collection) with named columns corresponding to the Parquet schema fields (e.g., spectrum_index, mz, intensity for spectra_data.parquet in mzPeak archives). Convert to a language-native data frame (R data.frame or Python pandas.DataFrame) only if row-oriented access or further transformation is required. Validate that the loaded table has the expected column names, data types, and row count matching the file's Parquet metadata.

## Related tools

- **arrow (R package)** (Parquet reading and columnar in-memory representation for R; provides zero-copy data access and lazy evaluation) — https://arrow.apache.org/docs/r/
- **pyarrow (Python library)** (Parquet reading and columnar in-memory representation for Python; integrates with PyData stack) — https://arrow.apache.org/docs/python/index.html
- **mobiusklein/mzpeak_prototyping** (Reference R implementation demonstrating arrow-based mzPeak file reading workflow) — https://github.com/mobiusklein/mzpeak_prototyping

## Examples

```
library(arrow)
spectra_data <- read_parquet('spectra_data.parquet')
spectra_df <- as.data.frame(spectra_data)
```

## Evaluation signals

- Loaded table schema matches the Parquet file's declared schema (column names, data types, nullability).
- Column count and row count match the Parquet metadata (number of spectra/chromatograms × points per spectrum).
- Expected spectrum fields are present and non-empty (e.g., spectrum_index, mz, intensity for signal tables).
- Data types are appropriate (numeric for m/z and intensity; integer for indices; struct for nested metadata like precursors).
- No unexpected null or missing values in non-nullable columns; null values only in optional grouped fields (e.g., precursor data for spectra without MS/MS).

## Limitations

- R and Python Arrow implementations support reading only; writing mzPeak files requires the Rust implementation.
- Arrow's lazy evaluation may defer error detection until data is explicitly materialized; always validate schema before assuming correctness.
- Memory overhead scales with uncompressed Parquet data size; for very large spectra_data.parquet files, consider reading by column or using chunked access rather than loading the entire table.
- Project is work-in-progress with no stability guarantee; API and file format may change.

## Evidence

- [readme] There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`]: "There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`]"
- [readme] There is also an R implementation in `R/`, which is also a complete re-implementation using the [`arrow`] for _reading_ only at this time.: "There is also an R implementation in `R/`, which is also a complete re-implementation using the [`arrow`] for _reading_ only at this time."
- [other] Use the R read function from the R/ implementation to open a valid mzPeak file. Extract spectrum data and convert to a structured tabular format (data frame). Validate that the output contains expected spectrum fields and rows.: "Use the R read function from the R/ implementation to open a valid mzPeak file. Extract spectrum data and convert to a structured tabular format (data frame). Validate that the output contains"
- [readme] mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP] archive. Each Parquet file describes a different facet of the stored mass spectrometry run.: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP] archive. Each Parquet file describes a different facet of the stored mass"
- [readme] spectra_data.parquet: Spectrum signal data in either profile or centroid mode. May be in point layout or chunked layout: "spectra_data.parquet: Spectrum signal data in either profile or centroid mode. May be in point layout or chunked layout"
