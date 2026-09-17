---
name: mass-spectrometry-data-extraction
description: Use when you have native Thermo Fisher RAW mass spectrometry files and
  need to extract scan-level metadata (retention time, total ion current, scan mode),
  MS1/MS2 peak lists with m/z and intensity arrays, or instrument/LC/MS method details
  for downstream computational analysis, QC, or cross-sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MetaXtract
  - RawFileReader
  - Python
  - Pandas
  - PyArrow / Parquet
  - Centwave
  - SLAW
  - FeatureFinderMetabo
  - ADAP
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.11.12.687968v1
  title: MetaXtract
- doi: 10.1021/acs.analchem.1c02687
  title: ''
evidence_spans:
- MetaXtract is a hybrid tool for extracting, analysing, and visualising data from
  **Thermo Fisher RAW** mass spectrometry files.
- Complete processing including peak picking, sample alignment, pick picking, grouping
  of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated
  MS2 spectra and isotopic
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaxtract_cq
    doi: 10.1101/2025.11.12.687968v1
    title: MetaXtract
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_metaxtract_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.11.12.687968v1
  all_source_dois:
  - 10.1101/2025.11.12.687968v1
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-extraction

## Summary

Extract metadata, scan headers, peak lists, and technical details from Thermo Fisher RAW mass spectrometry files using MetaXtract, which provides programmatic Python access alongside GUI and CLI interfaces. This skill is essential for converting proprietary binary RAW files into tabular, analysis-ready formats (CSV, TSV, Parquet) with m/z, intensity, resolution, noise, baseline, and charge information.

## When to use

Apply this skill when you have native Thermo Fisher RAW mass spectrometry files and need to extract scan-level metadata (retention time, total ion current, scan mode), MS1/MS2 peak lists with m/z and intensity arrays, or instrument/LC/MS method details for downstream computational analysis, QC, or cross-sample comparison. Use it as your initial data ingestion step when working with high-resolution or data-dependent acquisition (DDA) experiments.

## When NOT to use

- Input is already a vendor-neutral format (mzML, mzXML, NetCDF) — use those formats directly instead of re-converting through RAW extraction.
- You only need precursor m/z and retention time for simple filtering tasks — metadata extraction overhead is unnecessary; use a lightweight CLI query tool instead.
- Working on Linux and require MS or LC method extraction — those outputs are not supported on Linux; GUI/CLI on Windows or pre-export methods on Windows before transfer.

## Inputs

- Thermo Fisher RAW file (native binary format)
- Configuration YAML file (optional, for automated CLI runs)

## Outputs

- TSV file with file-based details (instrument metadata, scan counts, run statistics)
- CSV tables of MS1 and MS2 scan headers (selected columns)
- Parquet files containing MS1 peak lists (mz_array, intensity_array)
- Parquet files containing MS2 peak lists (mz_array, intensity_array, resolution_array, noises_array, baselines_array, charges_array)
- CSV files with MS1/MS2 technical details (optional)
- Interactive Plotly HTML reports (TIC, BPI, TNP plots; cross-sample overlays)
- MS method and LC method text files (Windows only)

## How to apply

Initialize MetaXtract with the path to your Thermo RAW file, then call extraction methods to retrieve file-level metadata (instrument details, run statistics), MS1 and MS2 scan headers (selecting columns such as Total Ion Current or Retention Time), and peak lists. Export peak lists as Parquet files where each row represents one scan and contains arrays for m/z, intensity, and optionally resolution, noise, baseline, and charge. Validate that output tables contain expected columns (scan_number, mz_array, intensity_array) and non-empty rows; for MS2 data, confirm the presence of extended peak list columns if needed for advanced analysis. If using programmatic workflows, load exported Parquet/CSV into NumPy arrays using helper functions to enable efficient downstream analysis in Python.

## Related tools

- **MetaXtract** (Primary tool for extracting, analyzing, and visualizing Thermo RAW files via Python library, CLI, or GUI) — https://github.com/Rappsilber-Laboratory/MetaXtract
- **RawFileReader** (Underlying Thermo Fisher library (included in MetaXtract distribution) that enables native RAW file reading on Windows and Linux)
- **Python** (Host language for programmatic MetaXtract workflows, data manipulation, and NumPy array handling)
- **Pandas** (DataFrame manipulation for scan headers and metadata tables after export)
- **PyArrow / Parquet** (Format for efficient storage and retrieval of peak list arrays (m/z, intensity, resolution, noise, baseline, charge))

## Examples

```
from raw_parser import MetaXtract; raw = MetaXtract("path/to/file.RAW"); raw.ExportPeakList("ms2_peaklist.parquet"); raw.ExportMS1PeakList("ms1_peaklist.parquet"); raw.CloseRAWFile()
```

## Evaluation signals

- Output Parquet/CSV files contain expected columns: scan_number, mz_array, intensity_array (MS1); mz_array, intensity_array, resolution_array, noises_array, baselines_array, charges_array (MS2 extended).
- All rows are non-empty; no null or zero-length arrays in peak list exports.
- Scan numbers are monotonically increasing and correspond to the input RAW file's scan count (verified via CountMS2() or metadata TSV).
- Retention time and total ion current values fall within physically plausible ranges (e.g., RT ≥ 0, TIC > 0).
- Interactive HTML reports display TIC and BPI chromatograms without rendering errors; cross-sample overlays correctly normalize intensities for comparison.

## Limitations

- MS method and LC method extraction are not supported on Linux; Windows is required for full metadata recovery.
- Thermo Fisher RAW access depends on included DLLs; compatibility with non-standard or very recent RAW file versions may be limited.
- Technical details export (GetMoreMSInfos) can be memory-intensive or slow for large files with many MS2 scans; consider selective export or batch processing.
- Python version must be ≥ 3.9; older environments cannot use MetaXtract.
- Parquet export of peak lists requires sufficient disk space proportional to the number of scans and peak density; very large DDA experiments may produce multi-gigabyte files.

## Evidence

- [readme] MetaXtract is a hybrid tool for extracting, analysing, and visualising data from Thermo Fisher RAW mass spectrometry files: "MetaXtract is a hybrid tool for extracting, analysing, and visualising data from **Thermo Fisher RAW** mass spectrometry files"
- [readme] It can be used via GUI, CLI, or directly as a Python library for programmatic workflows: "It can be used via a **Graphical User Interface (GUI)**, a **Command Line Interface (CLI)**, or directly as a **Python library** for programmatic workflows"
- [readme] Extracts MS1 and MS2 peak lists with m/z, intensity, resolution, noise, baseline, and charge arrays: "MS1 and MS2 peak lists with the extended peak list of MS2"
- [readme] Exports data as CSV, Parquet, and interactive Plotly HTML reports: "Exports data as: CSV / TSV, Parquet (peak lists), Interactive Plotly HTML reports"
- [readme] Peak lists stored as Parquet where each row is a scan and columns store arrays: "MetaXtract exports MS1/MS2 peak lists as **Parquet** (or CSV) where each row represents one scan and stores arrays (m/z, intensities, etc.)"
- [readme] Python method to load Parquet peak lists and convert to scan-indexed NumPy array dictionary: "loads such a file and returns a **dictionary**: - **key** = scan number - **value** = tuple of NumPy arrays - MS1: `(mz, intensity)` - MS2: `(mz, intensity, resolution, noise, baseline, charge)`"
- [readme] Programmatic API example showing initialization, extraction, and export: "raw = MetaXtract("path/to/file.RAW") raw.CountMS2() tic = raw.GetTICForScanNumber(100) raw.ExportPeakList("ms2_peaklist.parquet")"
