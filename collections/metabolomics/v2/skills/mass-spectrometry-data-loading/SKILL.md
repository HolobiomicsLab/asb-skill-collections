---
name: mass-spectrometry-data-loading
description: Use when you have raw MS data files from supported instruments (Agilent, Thermo, Bruker, or mzML format) and need to ingest them into IonToolPack for visualization, quality control, targeted extraction, or spectral library matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - IonToolPack
  - PeakQuant
  - Mirador
  - PeakQC
  - TandemMatch
  - Comparador
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- IonToolPack is a software suite housing tools for mass spectrometry data
- IonToolPack is a software suite housing tools for mass spectrometry data.
- 'PeakQuant: Targeted MS1 peak abundance extraction for quantitation.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakqc_cq
    doi: 10.1021/jasms.4c00146
    title: PeakQC
  dedup_kept_from: coll_peakqc_cq
schema_version: 0.2.0
---

# mass-spectrometry-data-loading

## Summary

Load raw mass spectrometry data from multiple instrument formats into a software suite for downstream analysis. This skill is essential as the first step in any MS-based omics workflow, enabling access to data regardless of acquisition platform or MS method.

## When to use

You have raw MS data files from supported instruments (Agilent, Thermo, Bruker, or mzML format) and need to ingest them into IonToolPack for visualization, quality control, targeted extraction, or spectral library matching. Applies to LC-MS, LC-IMS-MS, DDA, DIA, and direct infusion acquisition methods.

## When NOT to use

- Input data is already in a processed feature table or quantitation matrix format (CSV with m/z and abundance columns) — use PeakQuant only if you have raw data and a target list.
- Raw data file is corrupted, incomplete, or in an unsupported instrument format not listed in the README.
- You are working with already-exported spectra (e.g., MGF, MSP library files) rather than raw instrument output — use TandemMatch for library matching instead.

## Inputs

- Raw MS data file (Agilent '.d' directory)
- Raw MS data file (Thermo '.raw' file)
- Raw MS data file (Bruker '.d' directory)
- Raw MS data file (mzML file)

## Outputs

- In-memory parsed MS dataset accessible to IonToolPack tools
- MS data object containing LC-MS, LC-IMS-MS, DDA, DIA, or direct infusion spectra

## How to apply

Download and decompress the latest IonToolPack.exe from the GitHub Releases page. Launch IonToolPack.exe without installation. In the GUI, select the raw MS data file in one of the supported formats (Agilent '.d', Thermo '.raw', Bruker '.d', or mzML). The software automatically detects the instrument format and parses the raw data into memory. Once loaded, the data becomes available to all downstream tools (Mirador, PeakQC, TandemMatch, PeakQuant, Comparador) for the next processing step. The file must be a complete, non-corrupted raw data archive.

## Related tools

- **Mirador** (Downstream visualization and export of loaded MS data as XIC, XIM heatmaps, and MS/MS mirror plots) — github.com/pnnl/IonToolPack
- **PeakQC** (Automated quality control pipeline applied to loaded MS1 data via PCA analysis) — github.com/pnnl/IonToolPack
- **PeakQuant** (Targeted MS1 peak abundance extraction from loaded raw data using user-supplied target lists) — github.com/pnnl/IonToolPack
- **TandemMatch** (MS/MS spectral library matching applied to loaded fragmentation spectra) — github.com/pnnl/IonToolPack
- **Comparador** (Comparison of feature lists derived from loaded MS data across different acquisition methods) — github.com/pnnl/IonToolPack

## Evaluation signals

- File parsing succeeds without error and the GUI displays the data source filename in the active tab
- The loaded data object contains valid MS1 and (if present) MS/MS spectra accessible to downstream tools
- Downstream tools (Mirador, PeakQC, PeakQuant) execute without 'no data loaded' errors when triggered after loading
- Metadata (instrument type, acquisition mode, m/z range, retention time range) is correctly identified and displayed
- Sample data from test_data directory loads and produces expected outputs consistent with README examples

## Limitations

- Requires installation-free executable; users on restricted systems may lack permission to run .exe files.
- Only supports four instrument vendor formats (Agilent, Thermo, Bruker) plus mzML; other proprietary formats are not supported.
- No changelog provided in documentation, so users cannot assess backward compatibility or breaking changes between versions.
- GUI-driven loading may not support batch or scripted ingestion of multiple files in automated workflows.

## Evidence

- [readme] IonToolPack is a software suite housing tools for mass spectrometry data. It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "IonToolPack is a software suite housing tools for mass spectrometry data. It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities"
- [readme] Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode, Direct infusion: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode,"
- [readme] Download the latest version (Release section, right panel) and decompress it. Double click IonToolPack.exe. Import raw MS files and click 'Process': "Download the latest version (Release section, right panel) and decompress it. Double click IonToolPack.exe. Import raw MS files and click 'Process'"
- [intro] Load raw MS data in a supported instrument format using IonToolPack.: "Load raw MS data in a supported instrument format using IonToolPack."
