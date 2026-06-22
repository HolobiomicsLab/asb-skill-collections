---
name: raw-file-format-parsing
description: Use when you have native Thermo Fisher RAW files and need to recover file-level metadata (instrument details, run statistics), scan headers (retention time, total ion current, scan mode for MS1 or MS2), or peak lists (m/z and intensity arrays) in tabular or array form suitable for computational.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MetaXtract
  - RawFileReader
  - Python
  - NumPy
  - Pandas
  - PyArrow
derived_from:
- doi: 10.1101/2025.11.12.687968v1
  title: MetaXtract
evidence_spans:
- MetaXtract is a hybrid tool for extracting, analysing, and visualising data from **Thermo Fisher RAW** mass spectrometry files.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaxtract_cq
    doi: 10.1101/2025.11.12.687968v1
    title: MetaXtract
  dedup_kept_from: coll_metaxtract_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.11.12.687968v1
  all_source_dois:
  - 10.1101/2025.11.12.687968v1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# raw-file-format-parsing

## Summary

Extract structured metadata, scan headers, and peak lists from native Thermo Fisher RAW mass spectrometry files using programmatic access to proprietary file formats. This skill enables reproducible, automated recovery of instrument configuration, MS1/MS2 scan details, and m/z–intensity arrays for downstream computational analysis.

## When to use

Apply this skill when you have native Thermo Fisher RAW files and need to recover file-level metadata (instrument details, run statistics), scan headers (retention time, total ion current, scan mode for MS1 or MS2), or peak lists (m/z and intensity arrays) in tabular or array form suitable for computational pipelines. The skill is necessary when GUI-based export or manual inspection is insufficient or when you need programmatic, reproducible access within Python workflows.

## When NOT to use

- Input is already in an open, vendor-neutral format (mzML, mzXML, netCDF). Use format-agnostic parsing instead.
- You require MS method or LC method extraction and are running on Linux (MetaXtract does not support these options on Linux).
- You need real-time streaming of spectra during acquisition; MetaXtract requires a closed, complete RAW file.

## Inputs

- Thermo Fisher RAW mass spectrometry file (.RAW)
- File path (string) to the RAW file

## Outputs

- File-based metadata TSV (instrument details, scan counts, run statistics, sample information)
- MS1 scan header CSV table (retention time, total ion current, scan mode, user-selectable columns)
- MS2 scan header CSV table (retention time, total ion current, scan mode, user-selectable columns)
- MS1 peak list Parquet table (one row per scan; columns: scan_number, mz_array, intensity_array)
- MS2 extended peak list Parquet table (one row per scan; columns: scan_number, mz_array, intensity_array, resolution_array, noises_array, baselines_array, charges_array)
- MS2 technical details CSV (per-scan metrics from GetMoreMSInfos)
- MS1 technical details CSV (per-scan metrics from GetMoreMSInfos)
- Interactive Plotly HTML reports (TIC, BPI, TNP trends; cross-sample overlays and boxplots)

## How to apply

Instantiate the MetaXtract Python library with the path to the target RAW file. Call the appropriate extraction methods: CountMS2() to enumerate scans, GetTICForScanNumber() or GetRetentionTimeFromScanNumber() to retrieve per-scan metadata, and ExportPeakList() or ExportMS1PeakList() to serialize peak arrays as Parquet or CSV tables with one row per scan. For MS2 extended peak lists, the output includes m/z, intensity, resolution, noise, baseline, and charge arrays; MS1 lists include m/z and intensity only. Validate output by verifying row counts match the observed scan count, confirming presence of expected columns (mz_array, intensity_array), and loading arrays back as NumPy to confirm data types and value ranges. Close the file handle with CloseRAWFile() to free resources.

## Related tools

- **MetaXtract** (Python library providing programmatic RAW file parsing, metadata extraction, and peak list export) — https://github.com/Rappsilber-Laboratory/MetaXtract
- **RawFileReader** (Underlying Thermo Fisher scientific software library used by MetaXtract to read native RAW file formats)
- **Python** (Runtime and scripting interface for MetaXtract library calls and downstream peak list processing)
- **NumPy** (Array manipulation library for loading and validating parsed peak m/z and intensity arrays)
- **Pandas** (Tabular data library for loading and manipulating scan header and metadata CSV/Parquet tables)
- **PyArrow** (Parquet serialization and deserialization for efficient peak list storage and retrieval)

## Examples

```
from raw_parser import MetaXtract
raw = MetaXtract("path/to/file.RAW")
raw.ExportPeakList("ms2_peaklist.parquet")
raw.CloseRAWFile()
```

## Evaluation signals

- Output scan count (from CountMS2() or row count in peak list table) matches the expected MS2 scan count in the RAW file metadata.
- Retention time values are monotonically increasing or clustered in expected ranges for LC-MS runs; TIC values are positive and non-zero.
- Peak list Parquet/CSV files contain all required columns (scan_number, mz_array, intensity_array) and MS2 extended lists contain resolution_array, noises_array, baselines_array, and charges_array when applicable.
- m/z arrays are numeric, non-empty, and fall within the expected m/z range (typically 50–2000 Da for proteomics); intensity arrays are numeric and non-negative.
- File-based metadata TSV reports non-zero scan counts and valid instrument model names consistent with the RAW file header.

## Limitations

- RawFileReader is redistributable only as part of MetaXtract to end users; users may not redistribute RawFileReader independently (per Thermo Fisher RawFileReader License section 3.3).
- MS method and LC method extraction is not supported on Linux; these options are Windows-only.
- MetaXtract requires Python ≥ 3.9 and explicit dependency installation (numpy, pandas, pyarrow, tqdm, plotly, etc.).
- Peak list export as Parquet requires PyArrow; CSV export is available as an alternative but is less efficient for large peak arrays.
- Extended MS2 peak list columns (resolution, noise, baseline, charge) are only populated if the RAW file contains this data; older or differently configured instruments may not populate all columns.

## Evidence

- [readme] MetaXtract is a hybrid tool for extracting, analysing, and visualising data from Thermo Fisher RAW mass spectrometry files: "MetaXtract is a hybrid tool for extracting, analysing, and visualising data from **Thermo Fisher RAW** mass spectrometry files"
- [readme] It can be used directly as a Python library for programmatic workflows: "directly as a **Python library** for programmatic workflows"
- [readme] Peak list export format and contents: "Export MS2 extended peak list (Parquet): Per scan; `mz_array`, `intensity_array`, `resolution_array`, `noises_array`, `baselines_array`, `charges_array`"
- [readme] Example Python library invocation: "raw = MetaXtract("path/to/file.RAW")
raw.CountMS2()
raw.ExportPeakList("ms2_peaklist.parquet")"
- [readme] MS method extraction limitation on Linux: "**MS Method:** Extracts the MS method (`*_MS_method.txt`). # this option is not supported on Linux"
- [readme] Helper function for loading peak lists as NumPy arrays: "loads such a file and returns a **dictionary**: key = scan number, value = tuple of NumPy arrays"
- [readme] File-based output metadata contents: "**Writes a TSV file containing:** Instrument details, Scan counts, Run statistics, Sample information"
- [readme] RawFileReader license restriction: "anyone recieving RawFileReader as part of a larger software distribution is considered an "end user" and is not granted rights to redistribute RawFileReader"
