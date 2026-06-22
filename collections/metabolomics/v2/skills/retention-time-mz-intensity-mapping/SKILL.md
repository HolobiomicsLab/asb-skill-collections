---
name: retention-time-mz-intensity-mapping
description: Use when you have processed LC-MS run data (feature table or peak detection output) containing internal standard identifications with retention times, m/z values, and intensity measurements across multiple samples, and you need to rapidly detect instrumental drift, retention time shifts, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Plotly
  - MSConvert
  - MS-DIAL
  techniques:
  - LC-MS
  - tandem-MS
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

# retention-time-mz-intensity-mapping

## Summary

Create an interactive multi-dimensional visualization of internal standard quality metrics (retention time, m/z, and intensity) across LC-MS samples to monitor instrumental performance and identify drift or failures during data acquisition. This skill is essential for real-time QC assessment in untargeted metabolomics workflows.

## When to use

Apply this skill when you have processed LC-MS run data (feature table or peak detection output) containing internal standard identifications with retention times, m/z values, and intensity measurements across multiple samples, and you need to rapidly detect instrumental drift, retention time shifts, or intensity degradation that indicate QC failure.

## When NOT to use

- Input is raw vendor format data (.raw, .d, .ms) — must first convert to mzML using MSConvert and process with MS-DIAL or equivalent peak detection
- Internal standards have not yet been identified or annotated in the feature table
- Goal is to visualize all metabolic features, not specifically internal standards — use general feature heatmap or chromatogram instead

## Inputs

- processed LC-MS feature table (CSV or tabular format) with internal standard peak identifications
- internal standard reference m/z values and retention time windows
- peak intensity measurements across all samples
- sample metadata (sample name, acquisition order, date)

## Outputs

- interactive HTML visualization (Plotly-based dashboard)
- static image export (PNG or PDF) of retention-time-mz-intensity plot
- visualization dataset with hover tooltip data (sample name, RT, m/z, intensity)

## How to apply

Load the processed LC-MS feature table or peak detection output and filter or subset the data to isolate internal standard peaks by matching known m/z and retention time windows. Construct an interactive plot using Plotly or equivalent framework with retention time on the x-axis, m/z on the y-axis, and intensity encoded as point size or color, grouping or faceting by sample identity. Implement interactive hover tooltips that display sample name, retention time, m/z, and intensity for each internal standard measurement to enable rapid diagnosis of anomalies. The multi-dimensional encoding allows simultaneous monitoring of three critical QC metrics; deviations in any dimension (e.g., retention time shift >0.5 min, intensity drop >30%, or unexpected m/z clustering) signal instrumental issues requiring intervention.

## Related tools

- **Plotly** (interactive plotting library for constructing multi-dimensional retention-time–m/z–intensity scatter plots with hover tooltips and sample grouping)
- **MSConvert** (prerequisite vendor format data conversion to mzML before peak detection and internal standard filtering) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **MS-DIAL** (upstream peak detection and internal standard identification to produce feature table input) — http://prime.psc.riken.jp/compms/msdial/main.html

## Evaluation signals

- Hover tooltips correctly display all four dimensions (sample name, retention time, m/z, intensity) without truncation or missing values
- Sample grouping or faceting accurately segregates internal standard measurements by sample identity; no cross-contamination or mislabeling
- Retention time values fall within expected reference window (e.g., ±0.3–0.5 min of expected RT) for all samples; outliers are visually distinct
- Intensity values show expected consistency across replicates or technical replicates; intensity trends (e.g., gradual decline across run order) are visible and interpretable
- Interactive features (zoom, pan, hover, filtering by sample) respond smoothly and preserve data integrity; exported HTML or static image maintains visual fidelity

## Limitations

- Skill is specific to Rapid QC-MS workflow and depends on prior MS-DIAL peak detection; performance degrades if internal standards are not reliably identified or if peak detection has high false-positive rate
- Visualization assumes m/z and retention time measurements are accurate and that internal standard reference windows are correctly specified; misaligned or outdated reference data will produce misleading plots
- Interactive dashboard requires Plotly Dash and web browser (or Jupyter environment); deployment on Windows with MSConvert and MS-DIAL dependencies is the primary tested configuration; MacOS users can view results but cannot run acquisition pipeline
- Real-time visualization during instrument acquisition requires continuous file system monitoring (Watchdog); interruptions or file locks will delay or block updates

## Evidence

- [other] Construct an interactive plot (using Plotly or similar framework) with retention time on the x-axis, m/z on the y-axis, and intensity encoded as point size or color, with sample identity as a grouping or faceting dimension.: "Construct an interactive plot (using Plotly or similar framework) with retention time on the x-axis, m/z on the y-axis, and intensity encoded as point size or color, with sample identity as a"
- [other] Implement interactive hover tooltips displaying sample name, retention time, m/z, and intensity for each internal standard measurement.: "Implement interactive hover tooltips displaying sample name, retention time, m/z, and intensity for each internal standard measurement."
- [readme] Interactive data visualization of internal standard retention time, m/z, and intensity across samples: "Interactive data visualization of internal standard retention time, _m/z_, and intensity across samples"
- [other] Load processed LC-MS run data (feature table or peak detection output) containing internal standard identifications, retention times, m/z values, and intensity measurements across samples.: "Load processed LC-MS run data (feature table or peak detection output) containing internal standard identifications, retention times, m/z values, and intensity measurements across samples."
- [other] Filter or subset data to isolate internal standard peaks by matching known m/z and retention time windows.: "Filter or subset data to isolate internal standard peaks by matching known m/z and retention time windows."
