---
name: parameter-range-filtering-for-chromatographic-data
description: Use when you have raw MS data in instrument-native or mzML format (Agilent .d, Thermo .raw, Bruker .d) and need to isolate specific analyte regions defined by precise m/z windows, RT windows (in seconds or minutes), and/or ion mobility arrival-time windows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Mirador
  - IonToolPack
  - PeakQuant
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- 'Mirador: Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots'
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
---

# parameter-range-filtering-for-chromatographic-data

## Summary

Filter and extract mass spectrometry chromatographic and mobility data using user-specified m/z, retention time (RT), and arrival time (mobility) ranges and tolerances. This skill isolates regions of interest from raw multi-dimensional MS acquisitions (LC-MS, LC-IMS-MS) for targeted visualization and export.

## When to use

Apply this skill when you have raw MS data in instrument-native or mzML format (Agilent .d, Thermo .raw, Bruker .d) and need to isolate specific analyte regions defined by precise m/z windows, RT windows (in seconds or minutes), and/or ion mobility arrival-time windows. Use it when the analysis goal is to visualize, compare, or export targeted extracted ion chromatograms (XIC), ion mobility heatmaps (XIM), or MS/MS spectra for validation, library building, or quantitative reporting.

## When NOT to use

- Input is already a processed feature table or peak list without raw MS data access — use targeted quantitation (PeakQuant) instead.
- Analysis goal is global untargeted feature detection or peak-finding — use automated peak picking and PCA-based quality control (PeakQC) instead.
- Retention time or mobility values are unknown or not measured (e.g., direct infusion without separation, or instrument does not record IMS data) — adjust workflow to omit RT or arrival-time filtering steps.

## Inputs

- Raw MS data file (Agilent .d, Thermo .raw, Bruker .d, or mzML format)
- m/z range (numeric, Da or ppm; e.g., [500.0, 501.0] or [500.0±5ppm])
- Retention time (RT) range (numeric, minutes or seconds; e.g., [2.5, 4.0])
- Arrival time (mobility) range (numeric, milliseconds; e.g., [15, 25])
- m/z tolerance (numeric, Da or ppm; e.g., 5 ppm or 0.01 Da)
- RT tolerance (numeric, minutes or seconds; optional buffer around specified window)
- Arrival-time tolerance (numeric, milliseconds; optional buffer)
- MS/MS precursor ion list (optional; CSV or feature table for mirror plot extraction)

## Outputs

- Extracted ion chromatogram (XIC) matrix (retention time vs. intensity)
- Extracted ion mobility (XIM) heatmap (arrival time vs. m/z vs. intensity, 2D or 3D)
- MS/MS mirror plot data (precursor m/z, fragment m/z, intensity pairs)
- Filtered feature table (CSV; m/z, RT, arrival time, max intensity per feature)
- PDF report (visualizations of XIC, XIM, MS/MS mirror plots)
- CSV export (tabular data for XIC, XIM, and MS/MS with parameter metadata)

## How to apply

Load raw MS data into Mirador using the multi-format data reader (step 1). Parse user-specified m/z range (e.g., ±5 ppm or ±0.01 m/z Da tolerance), RT range (e.g., 2.5–4.0 min), and arrival-time (mobility) range (e.g., 15–25 ms) parameters (step 2). Extract ion chromatograms by filtering MS1 scans to the m/z and RT ranges, and optionally summing intensities across the m/z tolerance window (step 3). For IMS data, generate extracted ion mobility heatmaps by filtering on both m/z and arrival time, producing 2D intensity arrays (step 4). If MS/MS data are present (DDA or DIA), extract and format mirror plots for precursor ions matching the specified m/z and RT ranges (step 5). Export all filtered data and plots as PDF and CSV files with metadata (step 6). The rationale is that precise parameter filtering on high-dimensional data (m/z, RT, mobility) reduces noise and improves signal-to-noise for visual inspection and downstream quantitation.

## Related tools

- **Mirador** (Core visualization and export engine; applies m/z, RT, and arrival-time range filters to raw MS data and generates XIC, XIM heatmaps, and MS/MS mirror plots in PDF and CSV formats.) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Suite container and data reader; loads multi-instrument formats (Agilent, Thermo, Bruker, mzML) and provides the GUI for parameter input and Mirador execution.) — https://github.com/pnnl/IonToolPack
- **PeakQuant** (Downstream tool for targeted peak abundance extraction; uses filtered m/z and RT ranges to quantify peak areas in targeted or untargeted metabolomics workflows.) — https://github.com/pnnl/IonToolPack

## Examples

```
Double-click IonToolPack.exe → select Mirador tab → import raw Thermo .raw file → enter m/z range [500.0, 501.0], m/z tolerance 5 ppm, RT range [2.5, 4.0] min, arrival time range [15, 25] ms → click Process → export to PDF and CSV.
```

## Evaluation signals

- Output XIC shows baseline separation and intensity peak(s) within the specified RT range; no intensity outside the RT boundaries.
- Output XIM heatmap displays intensity concentrated within the specified m/z and arrival-time ranges; off-target regions show background noise.
- MS/MS mirror plots contain only fragment ions from precursor m/z values within the specified m/z tolerance; precursor isolation window is respected.
- CSV export contains metadata columns (m/z_min, m/z_max, RT_min, RT_max, arrival_time_min, arrival_time_max, m/z_tolerance, RT_tolerance) matching the input parameters; no truncation or rounding errors.
- PDF visualizations render XIC/XIM/MS/MS data with axis labels, parameter values, and source file name; plots are publication-quality without artifacts.

## Limitations

- Arrival-time (ion mobility) filtering requires LC-IMS-MS or direct-infusion IMS data; LC-MS data without IMS dimension cannot be filtered on arrival time, only m/z and RT.
- Tolerance windows (m/z, RT, arrival time) are symmetric around the user-specified range; asymmetric or adaptive windows are not supported.
- MS/MS mirror plots are generated only if DDA or DIA fragmentation spectra are present in the raw file; DDA-only acquisitions may have sparse MS/MS coverage for user-specified m/z ranges.
- Parameter ranges must be within the instrument's native acquisition window; ranges outside the acquired m/z, RT, or mobility space will produce empty or near-zero results.
- No changelog available; version-to-version changes in parameter handling or export format are not documented.

## Evidence

- [other] Mirador exports raw MS visualizations in PDF and CSV formats, including XIC, XIM heatmaps, and MS/MS mirror plots, with user-customizable m/z, retention time, and arrival time ranges and tolerances.: "Mirador exports raw MS visualizations in PDF and CSV formats, including XIC, XIM heatmaps, and MS/MS mirror plots, with user-customizable m/z, retention time, and arrival time ranges and tolerances."
- [other] Workflow step 2: Parse user-specified m/z, retention time (RT), and arrival-time (mobility) range parameters.: "Parse user-specified m/z, retention time (RT), and arrival-time (mobility) range parameters."
- [other] Workflow step 3: Extract ion chromatograms (XIC) for the specified m/z and RT ranges.: "Extract ion chromatograms (XIC) for the specified m/z and RT ranges."
- [other] Workflow step 4: Generate extracted ion mobility (XIM) heatmaps for the specified m/z and arrival-time ranges.: "Generate extracted ion mobility (XIM) heatmaps for the specified m/z and arrival-time ranges."
- [readme] README feature: Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots with customizable m/z, RT, and arrival time ranges and tolerances.: "Raw MS data visualization and export (PDF, CSV) including extracted ion chromatograms (XIC), extracted ion mobility (XIM) heatmaps, and MS/MS mirror plots with customizable m/z, RT, and arrival time"
- [readme] README MS data support: Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS.: "Supported formats include Agilent 'd', Thermo '.raw', Bruker 'd', and mzML, and for different types of MS acquisition methods: LC-MS, LC-IMS-MS."
