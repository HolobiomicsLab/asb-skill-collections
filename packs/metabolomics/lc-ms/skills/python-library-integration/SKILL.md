---
name: python-library-integration
description: Use when when you have Thermo Fisher RAW mass spectrometry files and need to extract mass-to-charge ratios, intensities, scan metadata, and peak lists within a Python script or notebook for downstream computational analysis, and you require programmatic control over extraction parameters rather.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - MetaXtract
  - pandas
  - numpy
  - pyarrow
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2025.11.12.687968v1
  title: MetaXtract
evidence_spans:
- directly as a **Python library** for programmatic workflows
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

# python-library-integration

## Summary

Import and programmatically interface with domain-specific Python libraries to automate data extraction and analysis workflows in scientific applications. This skill enables direct library calls and method invocation rather than relying on graphical or command-line interfaces, supporting reproducible, scriptable analysis pipelines.

## When to use

When you have Thermo Fisher RAW mass spectrometry files and need to extract mass-to-charge ratios, intensities, scan metadata, and peak lists within a Python script or notebook for downstream computational analysis, and you require programmatic control over extraction parameters rather than manual GUI operation.

## When NOT to use

- Input data is already in tabular format (CSV, Parquet, or pandas DataFrame); use direct DataFrame operations instead.
- RAW file access via Thermo DLLs is not available on your platform (note: Thermo method extraction not supported on Linux).
- You need cross-sample visual comparisons or interactive HTML reports; use MetaXtract GUI or CLI with visualisation enabled instead.

## Inputs

- Thermo Fisher RAW mass spectrometry file (.RAW)
- Python ≥ 3.9 environment with numpy, pandas, pyarrow dependencies installed

## Outputs

- Parquet or CSV file containing MS1 peak lists (mz_array, intensity_array per scan)
- Parquet or CSV file containing MS2 peak lists (mz_array, intensity_array, resolution_array, noises_array, baselines_array, charges_array per scan)
- Python dictionary mapping scan numbers to NumPy array tuples (MS1: (mz, intensity); MS2: (mz, intensity, resolution, noise, baseline, charge))
- Scalar values (Total Ion Current, Retention Time, scan counts) returned by library method calls

## How to apply

Import the MetaXtract library and instantiate it with the path to a Thermo Fisher RAW file. Call library methods such as CountMS2(), GetTICForScanNumber(), GetRetentionTimeFromScanNumber() to query specific data, then invoke ExportPeakList() or ExportMS1PeakList() to serialize MS1 and MS2 peak lists (m/z array, intensity array, and optionally resolution, noise, baseline, and charge arrays) to Parquet or CSV format. Validate that exported tables contain expected columns and scan numbers match input file metadata. Use the helper function load_peaklist_as_dict() to convert exported peak lists into a Python dictionary keyed by scan number with NumPy array values, enabling in-memory array operations without re-parsing the RAW file.

## Related tools

- **MetaXtract** (Python library for programmatic extraction of metadata, scan headers, and peak lists from Thermo Fisher RAW mass spectrometry files) — https://github.com/Rappsilber-Laboratory/MetaXtract
- **pandas** (DataFrame manipulation and I/O for reading Parquet/CSV peak list exports into memory)
- **numpy** (Array operations on m/z, intensity, and metadata arrays extracted from peak lists)
- **pyarrow** (Parquet file format support for efficient peak list serialization and deserialization)

## Examples

```
from raw_parser import MetaXtract
import pandas as pd

raw = MetaXtract("sample.RAW")
raw.ExportPeakList("ms2_peaklist.parquet")
raw.CloseRAWFile()

df = pd.read_parquet("ms2_peaklist.parquet")
print(df.columns, len(df))
```

## Evaluation signals

- Exported Parquet/CSV file contains non-empty rows and expected columns (mz_array, intensity_array, and optional extended columns for MS2).
- Scan numbers in exported peak lists match the range reported by CountMS2() or file metadata; no gaps or duplicates.
- load_peaklist_as_dict() successfully parses the exported file and returns a dictionary with scan numbers as keys and NumPy array tuples as values; array shapes match scan-level peak counts.
- Retention time and TIC values retrieved via GetRetentionTimeFromScanNumber() and GetTICForScanNumber() are within expected ranges for the instrument and sample type (e.g., RT > 0, TIC > 0).
- CloseRAWFile() is called to release file handles; subsequent script execution does not report resource leaks or locking errors.

## Limitations

- Thermo RAW file reading requires platform-specific DLLs and is limited to Windows and Linux; macOS is not supported.
- MS method and LC method extraction options are not supported on Linux; only available on Windows via GUI or CLI.
- MetaXtract reads native Thermo RAW files only; conversion from other vendor formats (Waters, Bruker, ABSciex) requires upstream format conversion.
- Large RAW files may consume significant memory when loading entire peak lists into Python dictionaries; consider processing scans in batches or using Parquet lazy-read paradigms.
- Extended peak list fields (resolution, noise, baseline, charge arrays) are only available for MS2; MS1 peak lists contain only mz_array and intensity_array.

## Evidence

- [other] MetaXtract provides programmatic access to extract data from Thermo Fisher RAW mass spectrometry files by offering a Python library interface alongside GUI and CLI alternatives.: "It can be used via a Graphical User Interface (GUI), a Command Line Interface (CLI), or directly as a Python library for programmatic workflows"
- [readme] The workflow step of importing and instantiating the library with a file path.: "from raw_parser import MetaXtract

raw = MetaXtract("path/to/file.RAW")"
- [readme] Methods for extracting scan-level quantitative data.: "raw.CountMS2()

tic = raw.GetTICForScanNumber(100)
rt = raw.GetRetentionTimeFromScanNumber(100)"
- [readme] Output format and peak list export capabilities.: "raw.ExportPeakList("ms2_peaklist.parquet")
raw.ExportMS1PeakList("ms1_peaklist.parquet")"
- [readme] Programmatic loading of exported peak lists into NumPy arrays.: "MetaXtract exports MS1/MS2 peak lists as Parquet (or CSV) where each row represents one scan and stores arrays (m/z, intensities, etc.)"
- [readme] Extended data available for MS2 scans.: "MS2: (mz, intensity, resolution, noise, baseline, charge) if those columns exist"
- [readme] Dependency requirements for Python library usage.: "Python ≥ 3.9
Thermo Fisher RAW access (DLLs included in the repository)"
