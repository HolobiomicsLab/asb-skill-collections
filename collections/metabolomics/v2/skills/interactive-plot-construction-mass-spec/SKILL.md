---
name: interactive-plot-construction-mass-spec
description: Use when after LC-MS data has been converted to mzML format and processed through peak detection (e.g., MS-DIAL output) to yield a feature table with internal standard identifications, retention times, m/z values, and intensity measurements across multiple samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3520
  tools:
  - Plotly or equivalent interactive plotting library
  - Plotly
  - Plotly Dash
  - Pandas
  - MS-DIAL
derived_from:
- doi: 10.1021/acs.analchem.4c00786
  title: Rapid QC-MS
evidence_spans:
- '**Interactive data visualization** of internal standard retention time, _m/z_, and intensity across samples'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c00786
  all_source_dois:
  - 10.1021/acs.analchem.4c00786
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Interactive Plot Construction for Mass Spectrometry QC Data

## Summary

Construct interactive visualizations of internal standard retention time, m/z, and intensity measurements across LC-MS samples to enable rapid detection of QC anomalies and sample-to-sample variation. This skill bridges processed peak detection output to browser-accessible dashboards for real-time monitoring during untargeted metabolomics workflows.

## When to use

After LC-MS data has been converted to mzML format and processed through peak detection (e.g., MS-DIAL output) to yield a feature table with internal standard identifications, retention times, m/z values, and intensity measurements across multiple samples. Use this skill when you need to visually compare internal standard performance across a sample run to detect retention time drift, m/z shifts, or intensity degradation that may indicate instrument malfunction or contamination.

## When NOT to use

- Raw vendor mass spectrometry files (.raw, .d, .ms) before conversion to mzML and peak detection — first apply MSConvert and MS-DIAL preprocessing.
- Targeted or SRM/MRM datasets where internal standard response is manually curated — this skill assumes automated peak detection output with consistent m/z and retention time annotations across samples.
- Single-sample or quality-control-passed data where no cross-sample variation or anomaly detection is needed — interactive visualization is most valuable for multi-sample monitoring.

## Inputs

- Processed LC-MS feature table (CSV, TSV, or DataFrame) with peak detection results including internal standard identifications
- Internal standard metadata (m/z values, expected retention time windows, sample identifiers)
- LC-MS run data formatted as mzML or peak intensity matrix with sample replicates

## Outputs

- Interactive HTML visualization file (Plotly dashboard) with retention time, m/z, and intensity dimensions
- Static image export (PNG or PDF) of the internal standard QC plot
- Hover tooltip data structure mapping sample identifiers to QC measurements

## How to apply

Load the processed feature table or peak detection output containing internal standard identifications and their associated retention time, m/z, and intensity values for each sample. Filter or subset the data to isolate internal standard peaks by matching known m/z windows and retention time ranges specific to your internal standards. Construct a Plotly (or equivalent interactive plotting framework) scatter or point plot with retention time on the x-axis, m/z on the y-axis, and intensity encoded as point size or color intensity; use sample identity as a grouping, faceting, or hover dimension. Implement interactive tooltips that display sample name, retention time, m/z, and intensity upon hover to enable rapid inspection of individual measurements. Export the interactive plot as an HTML file (preserving interactivity) or static image (PNG/PDF) and save to a specified output directory. Validate the plot by confirming that all expected internal standards appear, that retention times cluster tightly across samples (indicating stable chromatography), and that intensity values fall within expected ranges for your instrument.

## Related tools

- **Plotly** (Interactive plotting framework for constructing multi-dimensional scatter plots with hover tooltips and real-time sample filtering)
- **Plotly Dash** (Web application framework for serving interactive visualizations and enabling Google Drive cloud sync and authenticated access to QC dashboards)
- **Pandas** (Data manipulation and filtering library for subsetting feature tables to isolate internal standard peaks by m/z and retention time windows)
- **MS-DIAL** (Peak detection and identification tool that produces the processed feature table and internal standard annotations consumed by this skill) — http://prime.psc.riken.jp/compms/msdial/main.html

## Evaluation signals

- All expected internal standard peaks (by m/z and retention time) appear in the visualization across all samples in the run.
- Retention time measurements for a given internal standard cluster tightly across samples (tight x-axis distribution), indicating stable chromatography; drift > 0.5 min or shift > 2× historical SD suggests instrument malfunction.
- Intensity values for internal standards remain within 3-fold of the run median across samples; outlier samples with 10× lower intensity or > 20% intensity drift may indicate ionization problems or contamination.
- Interactive hover tooltips correctly display sample name, exact retention time, m/z value, and intensity for each point without truncation or parsing errors.
- HTML export retains full interactivity (zoom, pan, toggle sample groups); PNG/PDF export produces a static image at ≥ 150 dpi suitable for publication or email reporting.

## Limitations

- Rapid QC-MS has been tested extensively on Thermo Fisher mass spectrometers and Thermo RAW files; bugs and issues may occur with Agilent, Bruker, Sciex, or Waters vendor formats despite MSConvert conversion.
- Interactive visualization performance may degrade with > 1000 samples or > 500 internal standards per plot; subset or aggregate samples into batches for large studies.
- Plotly Dash requires Python 3.8–3.11 and integration with Google API for cloud sync; on-premise or offline installations cannot access cloud-authenticated QC dashboards without manual export.
- Hover tooltips and color-encoding require adequate screen resolution and browser support; some legacy instruments or remote desktop environments may render poorly.

## Evidence

- [other] how_to_apply: "Load processed LC-MS run data (feature table or peak detection output) containing internal standard identifications, retention times, m/z values, and intensity measurements across samples."
- [readme] summary and when_to_use: "Interactive data visualization of internal standard retention time, _m/z_, and intensity across samples"
- [readme] when_not_to_use: "Rapid QC-MS was designed to run on Windows platforms because of its dependency on MSConvert for vendor format data conversion and MS-DIAL for data processing and identification."
- [readme] limitations: "Rapid QC-MS has only been tested extensively on Thermo Fisher mass spectrometers, Thermo acquisition sequences, and Thermo RAW files."
- [readme] related_tools: "Rapid QC-MS requires Python 3.8 to 3.11 and various Python packages, including: Pandas, SQLAlchemy, Plotly Dash, Bootstrap, Watchdog, Google API, Slack API"
