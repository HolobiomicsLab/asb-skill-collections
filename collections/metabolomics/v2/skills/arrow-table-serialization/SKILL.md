---
name: arrow-table-serialization
description: Use when you have loaded mzPeak spectrum or chromatogram metadata and signal data into PyArrow Table structures (via the Python mzPeak reader or equivalent) and need to persist them to disk in Parquet format for downstream analysis, interoperability with other languages (R, .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - OpenMS
  - Python
  - pyarrow
  - Python mzPeak reader
  - ZIP archive utility
  - mzPeak specification JSON Schemas
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- There is a separate Python implementation in `python/`
- complete re-implementation for _reading_ mzPeak files using [`pyarrow`]
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# arrow-table-serialization

## Summary

Serialize mass spectrometry spectrum or chromatogram data from in-memory Arrow Table structures into Parquet files within an mzPeak archive. This skill bridges tabular data representation and persistent storage in a Parquet-based format compatible with the PyData stack.

## When to use

You have loaded mzPeak spectrum or chromatogram metadata and signal data into PyArrow Table structures (via the Python mzPeak reader or equivalent) and need to persist them to disk in Parquet format for downstream analysis, interoperability with other languages (R, .NET, TypeScript), or long-term archival. Use this skill when your workflow requires conversion of in-memory Arrow Tables into the mzPeak archive structure.

## When NOT to use

- Input is already a complete mzPeak archive file — no re-serialization is needed.
- Python implementation is being used and write support is required — the Python codebase does not support writing at this time.
- Data is in a non-Arrow columnar format (e.g., raw NumPy arrays or Pandas DataFrames without Arrow conversion) — convert to Arrow first.
- The target environment requires R or .NET interoperability but cannot handle ZIP archives — use language-specific Arrow writers instead.

## Inputs

- PyArrow Table (spectra_metadata schema)
- PyArrow Table (spectra_data schema)
- PyArrow Table (spectra_peaks schema, optional)
- PyArrow Table (chromatograms_metadata schema)
- PyArrow Table (chromatograms_data schema)

## Outputs

- mzPeak archive (ZIP containing .parquet files and mzpeak_index.json)
- spectra_metadata.parquet
- spectra_data.parquet
- spectra_peaks.parquet (optional)
- chromatograms_metadata.parquet
- chromatograms_data.parquet
- mzpeak_index.json

## How to apply

After loading mzPeak files using the Python pyarrow-based reader, the resulting Arrow Tables representing spectrum metadata, spectrum signal data, and optional peaks data are already in the native columnar format. Serialize each Table to its corresponding Parquet file (spectra_metadata.parquet, spectra_data.parquet, spectra_peaks.parquet, chromatograms_metadata.parquet, chromatograms_data.parquet) using pyarrow's write_table() function, then bundle all Parquet files into an uncompressed ZIP archive with the mzpeak_index.json manifest. The key rationale is that Parquet's column-oriented storage and built-in compression (via Snappy, gzip, or Zstandard codecs) provides efficient size reduction for sparse spectrum arrays while maintaining lossless access to signal data and metadata. Verify that the resulting mzPeak archive preserves schema validity by confirming schema compliance against the JSON Schemas in the mzPeak specification's schema/ directory.

## Related tools

- **pyarrow** (In-memory columnar data format and write_table() API for serializing Arrow Tables to Parquet files within the mzPeak archive) — https://arrow.apache.org/docs/python/index.html
- **Python mzPeak reader** (Loads mzPeak files and returns data as PyArrow Table structures ready for downstream serialization or analysis) — https://github.com/HUPO-PSI/mzPeak
- **ZIP archive utility** (Bundles Parquet files and mzpeak_index.json manifest into an uncompressed ZIP container)
- **mzPeak specification JSON Schemas** (Defines valid schemas for spectra_metadata, spectra_data, and chromatograms tables to validate serialized output) — https://github.com/HUPO-PSI/mzPeak-specification

## Examples

```
import pyarrow.parquet as pq; import zipfile; pq.write_table(spectra_metadata_table, 'spectra_metadata.parquet'); pq.write_table(spectra_data_table, 'spectra_data.parquet'); with zipfile.ZipFile('output.mzpeak', 'w', zipfile.ZIP_STORED) as z: z.write('spectra_metadata.parquet'); z.write('spectra_data.parquet'); z.write('mzpeak_index.json')
```

## Evaluation signals

- Output mzPeak archive unpacks without corruption and contains all required .parquet files (spectra_metadata.parquet, spectra_data.parquet, chromatograms_metadata.parquet, chromatograms_data.parquet) and mzpeak_index.json manifest.
- Round-trip read test: reopen the serialized mzPeak archive using the Python reader and verify that Arrow Tables can be loaded with matching row counts and column schemas to the original tables.
- Schema validation: each Parquet file's schema matches the corresponding JSON Schema in schema/ directory; inspect via pyarrow.parquet.read_schema().
- Data integrity: spectrum m/z and intensity values remain unchanged (lossless serialization); verify via field-by-field comparison of original and deserialized Arrow columns.
- Index completeness: mzpeak_index.json lists all Parquet files present and their locations; confirm no orphaned or missing file entries.

## Limitations

- Python implementation does not support writing mzPeak files — serialization must be performed via Rust implementation or external tooling.
- Zero run stripping and null marking reconstruction require careful handling of sparse array regions; reconstructed m/z spacing for singleton null-marked points depends on learned polynomial models and may introduce minute angle changes in peak shape.
- Parquet compression codec choice (Snappy, gzip, Zstandard) affects file size and read performance; no guidance provided in the article on optimal codec selection for mass spectrometry data.
- mzPeak format is work-in-progress with no stability guarantee; schema and serialization format may change in future releases.

## Evidence

- [readme] The Python codebase does not support writing at this time although this is subject to change in the future: "The Python codebase does not support writing at this time although this is subject to change in the future"
- [readme] mzPeak is an archive of multiple Parquet files, stored directly in an uncompressed ZIP archive.: "mzPeak is an archive of multiple Parquet files, stored directly in an _uncompressed_ ZIP archive. Each Parquet file describes a different facet of the stored mass spectrometry run."
- [intro] complete re-implementation for reading mzPeak files using pyarrow: "complete re-implementation for _reading_ mzPeak files using [`pyarrow`]"
- [other] Convert the loaded spectrum data into a pandas DataFrame or pyarrow Table structure. 5. Export the structured table to a Parquet file or CSV format for downstream use.: "Convert the loaded spectrum data into a pandas DataFrame or pyarrow Table structure. 5. Export the structured table to a Parquet file or CSV format for downstream use."
- [readme] mzpeak_index.json: Definition of the files present in the archive: "mzpeak_index.json: Definition of the files present in the archive, encoded as JSON. This makes resolving files by controlled terms easier than matching file names."
- [readme] NOTE: This is a work in progress, no stability is guaranteed at this point.: "**NOTE**: This is a **work in progress**, no stability is guaranteed at this point."
