---
name: spectral-data-format-validation
description: Use when after converting existing mass spectrometry formats (mzML, vendor formats) into mzPeak using command-line tools or when receiving mzPeak files from external sources.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - OpenMS
  - pyarrow
  - arrow (R)
  - Rust mzPeak library
  - MkDocs Material specification site
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans: []
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
---

# Spectral Data Format Validation

## Summary

Validate mass spectrometry spectral data files against the mzPeak format specification, ensuring correct Parquet schema structure, archive integrity, and metadata compliance. This skill confirms that converted or newly produced mzPeak files conform to the HUPO-PSI specification before downstream analysis.

## When to use

After converting existing mass spectrometry formats (mzML, vendor formats) into mzPeak using command-line tools or when receiving mzPeak files from external sources. Apply this skill before loading spectral data into downstream analysis pipelines to catch schema mismatches, missing required Parquet tables, corrupted ZIP archive structure, or metadata non-compliance early.

## When NOT to use

- Input is already validated and certified conformant by the producing tool.
- You are performing exploratory data analysis and do not require formal compliance certification.
- The mzPeak file is being used only for read-only visualization and does not need to interoperate with other tools.

## Inputs

- mzPeak file (ZIP archive containing Parquet tables and JSON index)
- mzPeak specification JSON Schemas (from schema/ directory)
- File-level metadata JSON documents embedded in Parquet metadata segments

## Outputs

- Validation report (pass/fail per table and schema constraint)
- List of schema violations or missing required fields
- Parquet table structure summary (column names, dtypes, row counts)
- Archive integrity status (completeness, ZIP structure)

## How to apply

Validate the mzPeak file as an uncompressed ZIP archive containing the required Parquet files: mzpeak_index.json, spectra_metadata.parquet, and spectra_data.parquet (with optional spectra_peaks.parquet). Check that mzpeak_index.json correctly enumerates all present files using controlled vocabulary terms. Verify Parquet schema conformance for each table against the JSON Schemas in the specification's schema/ directory, ensuring spectrum-level metadata tables use packed parallel struct layouts for precursors and selected ions, and that data arrays follow either point layout (parallel m/z and intensity columns with repeated spectrum_index) or chunked layout according to the file's metadata declaration. Confirm file-level metadata in Parquet JSON segments are present and decode without error. For profile data, inspect whether zero run stripping and null marking have been applied as declared in metadata. Use pyarrow (Python), arrow (R), or the Rust library to programmatically read Parquet tables and validate column dtypes and non-null constraints match specification.

## Related tools

- **pyarrow** (Python library for reading and validating Parquet schema and column structure in mzPeak files) — https://arrow.apache.org/docs/python/index.html
- **arrow (R)** (R package for reading and inspecting Parquet table schemas and metadata) — https://arrow.apache.org/docs/r/
- **Rust mzPeak library** (Native Rust library with read/write support and built-in schema validation for mzPeak archives) — https://github.com/HUPO-PSI/mzPeak
- **MkDocs Material specification site** (Canonical reference for mzPeak format structure, schemas, and metadata requirements) — https://hupo-psi.github.io/mzPeak-specification/

## Examples

```
python -c "import pyarrow.parquet as pq; import zipfile; z = zipfile.ZipFile('sample.mzpeak'); idx = z.read('mzpeak_index.json'); meta = pq.read_table('spectra_metadata.parquet'); print(meta.schema)"
```

## Evaluation signals

- ZIP archive opens without corruption and contains all required Parquet files listed in mzpeak_index.json
- Each Parquet table (spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, etc.) loads without read errors and matches expected column names and data types from schema/
- File-level metadata JSON in Parquet footer decodes successfully and contains required keys for instrumentation, software, and data transformation pipeline
- For point layout data: spectrum_index column repeats correctly across rows, m/z and intensity arrays have matching row counts per spectrum, no NaN values in non-nullable columns
- For profile data: zero run stripping and null marking declarations in metadata match observed m/z spacing patterns (gaps marked as null m/z/intensity pairs, consecutive zero intensities removed)
- No orphaned or undeclared Parquet files exist in the ZIP archive beyond those enumerated in mzpeak_index.json

## Limitations

- The mzPeak specification is a working draft with no stability guarantee; validation rules may change as the standard evolves.
- Rust, Python, and R implementations have differing maturity: only Rust supports writing mzPeak files; Python and R are read-only, limiting validation breadth in those languages.
- Validation of downstream data integrity (e.g., whether peak centroids correctly match profile signal or precursor m/z values fall within expected ranges) requires domain-specific logic beyond schema conformance.
- Zero-run stripping and null marking reconstruction accuracy depends on the m/z spacing model parameters stored in metadata; validation does not verify reconstruction fidelity.
- Conversion from legacy formats (mzML, vendor binary) may introduce subtle metadata loss; validation confirms structural compliance but not semantic correctness of all controlled vocabulary terms.

## Evidence

- [readme] Components of an mzPeak archive: `mzpeak_index.json`: Definition of the files present in the archive, encoded as JSON.: "mzpeak_index.json`: Definition of the files present in the archive, encoded as JSON."
- [readme] Each Parquet file describes a different facet of the stored mass spectrometry run.: "Each Parquet file describes a different facet of the stored mass spectrometry run."
- [readme] The specification is written in Markdown and built into a static website with MkDocs and the Material for MkDocs theme.: "The specification is written in Markdown and built into a static website with MkDocs and the Material for MkDocs theme."
- [readme] In these Parquet files, the root schema is made up of several branched group or struct that may be null at any level.: "In these Parquet files, the root schema is made up of several branched "group" or "struct" (Parquet vs. Arrow nomenclature) that may be null at any level."
- [readme] The point layout stores the data as-is in parallel arrays alongside a repeated index column.: "When storing data arrays, the point layout stores the data as-is in parallel arrays alongside a repeated index column."
- [readme] mzPeak file-level metadata are stored in the Parquet metadata segment as JSON documents.: "mzPeak file-level metadata, including descriptions of the file's contents, the instrumentation, software, and data transformation pipeline are stored in the Parquet metadata segment as JSON documents."
- [readme] JSON Schemas that govern the file formats live in schema/ directory.: "JSON Schemas that govern the file formats live in [`schema/`](schema/)"
- [readme] mzPeak is a archive of multiple Parquet files, stored directly in an uncompressed ZIP archive.: "mzPeak is a archive of multiple [Parquet](https://parquet.apache.org/) files, stored directly in an _uncompressed_ [ZIP]"
