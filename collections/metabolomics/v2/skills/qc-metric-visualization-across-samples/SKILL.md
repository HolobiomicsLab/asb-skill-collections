---
name: qc-metric-visualization-across-samples
description: Use when you have processed LC-MS peak detection output or feature tables containing internal standard identifications with retention times, m/z values, and intensity measurements across multiple samples, and you need to visually monitor whether internal standards are within acceptable QC.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Plotly
  - MS-DIAL
  - MSConvert
derived_from:
- doi: 10.1021/acs.analchem.4c00786
  title: Rapid QC-MS
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapid_qc_ms_cq
    doi: 10.1021/acs.analchem.4c00786
    title: Rapid QC-MS
  dedup_kept_from: coll_rapid_qc_ms_cq
schema_version: 0.2.0
---

# qc-metric-visualization-across-samples

## Summary

Create interactive visualizations of internal standard QC metrics (retention time, m/z, intensity) across LC-MS samples to identify instrument performance drift and detect QC failures in real time. This skill enables rapid assessment of whether internal standards meet expected retention time windows, mass accuracy, and signal intensity thresholds across a cohort of runs.

## When to use

You have processed LC-MS peak detection output or feature tables containing internal standard identifications with retention times, m/z values, and intensity measurements across multiple samples, and you need to visually monitor whether internal standards are within acceptable QC tolerances (retention time window, m/z accuracy, intensity range) to flag instrument drift or performance degradation before downstream analysis.

## When NOT to use

- Input is already a validated, post-QC feature table with all samples confirmed to pass retention time, m/z, and intensity thresholds — visualization adds no diagnostic value.
- You have raw vendor mass spectrometry data (.raw, .d, .ms) that has not yet been converted to open format (mzML) and processed for peak detection — convert and process first.
- You lack internal standard reference data (expected m/z, retention time window, or intensity baseline) to define which peaks are internal standards and what constitutes acceptable variation.

## Inputs

- Processed LC-MS feature table or peak detection output (e.g., MS-DIAL export or mzML-derived feature matrix)
- Internal standard reference table (known m/z, expected retention time, intensity baseline or range)
- Sample metadata or run sequence information (sample names, run order)

## Outputs

- Interactive HTML visualization (Plotly) with retention time, m/z, intensity, and sample identity
- Static image export (PNG or PDF) of the interactive plot
- Tabular summary of internal standard measurements across samples (optional CSV or TSV export)

## How to apply

Load processed LC-MS run data (feature table or peak detection output from MS-DIAL or equivalent) containing internal standard identifications with retention times, m/z values, and intensity measurements across samples. Filter or subset the data to isolate internal standard peaks by matching known m/z and retention time windows. Construct an interactive plot using Plotly or similar framework with retention time on the x-axis, m/z on the y-axis, and intensity encoded as point size or color, with sample identity as a grouping or faceting dimension. Implement interactive hover tooltips displaying sample name, retention time, m/z, and intensity for each internal standard measurement. Export the interactive visualization as an HTML or static image file (PNG/PDF) and save to the output directory. Use this visualization to detect systematic drift in retention time or m/z across the run sequence, and identify samples where internal standard intensity falls below acceptable thresholds.

## Related tools

- **Plotly** (Interactive plotting library for constructing retention time vs. m/z vs. intensity scatter plots with hover tooltips and faceting by sample)
- **MS-DIAL** (Data processing and peak detection to generate feature tables with retention time, m/z, and intensity measurements) — http://prime.psc.riken.jp/compms/msdial/main.html
- **MSConvert** (Vendor format data conversion to open mzML format prior to peak detection) — https://proteowizard.sourceforge.io/tools/msconvert.html

## Evaluation signals

- Interactive HTML or static image displays all internal standard peaks across samples with correct axis labels (retention time, m/z, intensity) and no missing or incorrectly filtered data points.
- Hover tooltips on interactive plot correctly display sample name, retention time (±0.1 min or per user tolerance), m/z (±5 ppm or per user tolerance), and intensity value for each point.
- Internal standard m/z and retention time values match reference table expectations (within user-defined windows); outliers or drift are visually apparent as systematic shifts or outliers in the plot.
- Intensity measurements across samples show expected variation (e.g., no sample has >50% intensity drop relative to baseline) or flag problematic samples that deviate significantly from cohort mean.
- Exported HTML or image file is generated without errors and renders correctly in a web browser or image viewer.

## Limitations

- Rapid QC-MS has been tested extensively only on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and .raw files; other vendor formats (Agilent, Bruker, Sciex, Waters) may have bugs or processing issues.
- Visualization requires pre-processed feature tables or peak detection output; it does not directly consume raw vendor data—MSConvert and MS-DIAL conversion and processing must complete first.
- Interactive Plotly visualization requires a web browser or Jupyter environment to render; static exports (PNG/PDF) may lose interactivity and drill-down capability.
- No automated QC decision or alert generation from the visualization alone; interpretation of drift or intensity loss must be manual or coupled with downstream alert logic (e.g., Slack notifications triggered by thresholds).

## Evidence

- [readme] Interactive data visualization of internal standard retention time, m/z, and intensity across samples: "Interactive data visualization of internal standard retention time, _m/z_, and intensity across samples"
- [other] Workflow for constructing interactive plot with retention time on x-axis, m/z on y-axis, intensity encoded as point size or color, and sample identity as grouping dimension: "Construct an interactive plot (using Plotly or similar framework) with retention time on the x-axis, m/z on the y-axis, and intensity encoded as point size or color, with sample identity as a"
- [other] Implementation of hover tooltips and export of interactive visualization as HTML or static image: "Implement interactive hover tooltips displaying sample name, retention time, m/z, and intensity for each internal standard measurement. 5. Export the interactive visualization as an HTML or static"
- [readme] Rapid QC-MS dependency on MSConvert for vendor format data conversion prior to visualization: "its dependency on MSConvert for vendor format data conversion"
- [readme] Scope limitation to Thermo Fisher instruments with caveats for other vendors: "Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files. As such, it is expected that there may be bugs and issues with"
