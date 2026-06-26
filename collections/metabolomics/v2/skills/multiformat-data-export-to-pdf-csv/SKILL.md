---
name: multiformat-data-export-to-pdf-csv
description: Use when you have raw MS data in vendor formats (Agilent .d, Thermo .raw,
  Bruker .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3957
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - Mirador
  - IonToolPack
  techniques:
  - LC-MS
  - direct-infusion-MS
  - ion-mobility-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- 'Mirador: Raw MS data visualization and export (PDF, CSV) including extracted ion
  chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots'
- IonToolPack is a software suite housing tools for mass spectrometry data
- IonToolPack is a software suite housing tools for mass spectrometry data.
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00146
  all_source_dois:
  - 10.1021/jasms.4c00146
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multiformat-data-export-to-pdf-csv

## Summary

Export raw mass spectrometry visualizations and tabular data (extracted ion chromatograms, ion mobility heatmaps, MS/MS mirror plots) from multiple instrument formats (Agilent, Thermo, Bruker, mzML) into standardized PDF and CSV formats with user-specified parameter ranges. This skill enables portable archival and downstream sharing of MS data products across platforms.

## When to use

You have raw MS data in vendor formats (Agilent .d, Thermo .raw, Bruker .d, mzML) from LC-MS, LC-IMS-MS, or direct infusion experiments and need to extract and publish specific m/z, retention time, or mobility windows as both visual (PDF) and tabular (CSV) outputs for reporting, comparison across instruments, or integration into publication workflows.

## When NOT to use

- Input data are already in processed feature table format (e.g., aligned peak matrices, mzmine output); use this skill only on raw vendor MS data.
- Your goal is spectral library matching or quantitative peak integration across cohorts; use TandemMatch (for library matching) or PeakQuant (for targeted quantitation) instead.
- You need global quality control or outlier detection across multiple samples; use PeakQC for PCA-based QC metrics instead.

## Inputs

- Raw mass spectrometry data files (Agilent .d, Thermo .raw, Bruker .d, mzML)
- User-specified m/z range and tolerance (ppm or Da)
- User-specified retention time (RT) range (min)
- User-specified arrival time (mobility) range and tolerance (optional, for IMS-MS data)
- Precursor ion targets for MS/MS mirror plot extraction

## Outputs

- PDF document(s) containing XIC plots, XIM heatmaps, and MS/MS mirror plots
- CSV file(s) with tabular XIC intensities indexed by RT and m/z
- CSV file(s) with tabular XIM heatmap data indexed by m/z and arrival time
- CSV file(s) with MS/MS spectral peak lists and mirror plot metadata

## How to apply

Load raw MS data via Mirador's multi-format data reader, then specify extraction parameters: m/z range and tolerance, retention time (RT) range, and arrival-time (mobility) range if IMS data are present. Mirador generates three classes of outputs: (1) extracted ion chromatograms (XIC) for the specified m/z and RT windows, (2) extracted ion mobility (XIM) heatmaps for m/z and arrival-time ranges, and (3) MS/MS mirror plots for precursor ions within the ranges. All visualizations and underlying tabular data are then exported simultaneously as PDF documents (for visual inspection and publication) and CSV files (for numerical reuse and interoperability). Parameter selection should match your research question: narrow m/z tolerances (e.g., ±5 ppm) for targeted verification of known compounds, broader ranges for exploratory visualization of feature clusters.

## Related tools

- **Mirador** (Primary tool for multi-format raw MS data reading, XIC/XIM/MS/MS extraction, and PDF/CSV export with customizable m/z, RT, and arrival-time range parameters) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Container suite providing unified GUI and cross-tool data workflow integration; Mirador is one of its five modular tools) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- PDF outputs are readable and contain correctly scaled XIC, XIM, and MS/MS plots with axis labels matching user-specified ranges.
- CSV files contain numeric intensity or peak data with headers (m/z, RT, intensity for XIC; m/z, arrival_time, intensity for XIM) and row counts consistent with the specified parameter windows.
- Number and m/z values of extracted precursor ions in MS/MS mirror plots fall within user-specified m/z range and tolerance.
- Exported RT and mobility ranges in both PDF plots and CSV tables match the user input parameters exactly (no silent truncation or extrapolation).
- Files are created without errors and can be opened in standard PDF viewers and spreadsheet or data analysis software (e.g., Excel, Python pandas) without corruption.

## Limitations

- Export granularity and parameter customization depend on Mirador's GUI options; scripted parameter sweeps across many m/z windows may require repeated manual invocations or external batch-calling.
- PDF plots are static images; interactive re-zooming or parameter refinement requires re-export from Mirador.
- Performance and memory footprint may be limited by raw file size and number of simultaneous extraction windows; very large datasets or fine-grained tolerance windows may require splitting into batches.
- MS/MS mirror plot export requires presence of fragmentation spectra (DDA or DIA mode); direct infusion data without fragmentation cannot produce mirror plots.

## Evidence

- [other] Mirador exports raw MS visualizations in PDF and CSV formats, including XIC, XIM heatmaps, and MS/MS mirror plots, with user-customizable m/z, retention time, and arrival time ranges and tolerances.: "Mirador exports raw MS visualizations in PDF and CSV formats, including XIC, XIM heatmaps, and MS/MS mirror plots, with user-customizable m/z, retention time, and arrival time ranges and tolerances."
- [readme] Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots: "Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots"
- [readme] It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities (metabolomics, lipidomics, proteomics, etc.): "It reads data from multiple instrument formats, requires no installation and provides omics agnostic functionalities"
- [readme] Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS, With/without fragmentation spectra in DDA or DIA mode, Direct infusion: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS"
- [other] Extract ion chromatograms (XIC) for the specified m/z and RT ranges. Generate extracted ion mobility (XIM) heatmaps for the specified m/z and arrival-time ranges. Extract and format MS/MS mirror plots for precursor ions within the specified ranges.: "Extract ion chromatograms (XIC) for the specified m/z and RT ranges. Generate extracted ion mobility (XIM) heatmaps for the specified m/z and arrival-time ranges."
