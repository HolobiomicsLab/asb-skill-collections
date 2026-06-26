---
name: multi-dimensional-data-encoding
description: Use when you have loaded LC-MS feature tables or peak detection output
  containing internal standard identifications with retention times, m/z values, and
  intensity measurements across multiple samples, and you need to detect anomalies
  such as retention time drift, m/z shifts, or intensity loss that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Plotly
  - MSConvert
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-dimensional-data-encoding

## Summary

Encode three or more LC-MS internal standard dimensions (retention time, m/z, intensity) into a single interactive plot using point size, color, position, and faceting to enable rapid visual assessment of internal standard behavior across samples. This skill is essential for quality control workflows where simultaneous monitoring of retention time drift, mass accuracy, and ionization consistency across replicate samples identifies instrument performance issues.

## When to use

You have loaded LC-MS feature tables or peak detection output containing internal standard identifications with retention times, m/z values, and intensity measurements across multiple samples, and you need to detect anomalies such as retention time drift, m/z shifts, or intensity loss that would indicate instrument degradation or column contamination during an untargeted metabolomics run.

## When NOT to use

- Input is raw vendor mass spectrometry data (.raw, .d, .ms) that has not yet been converted to open format (mzML) and processed through peak detection — use MSConvert and MS-DIAL first.
- You are visualizing only a single dimension (e.g., retention time alone or m/z alone) — simpler univariate plots are more appropriate.
- The number of samples is extremely large (>10,000) such that point overplotting renders interactive exploration impractical without aggregation.

## Inputs

- Processed LC-MS feature table (CSV, TSV, or tabular format) containing internal standard identifications
- Internal standard m/z and retention time reference windows (for filtering/subsetting)
- Peak detection output with retention time, m/z, and intensity measurements across samples

## Outputs

- Interactive HTML visualization (Plotly)
- Static image export (PNG or PDF)

## How to apply

After filtering or subsetting processed LC-MS data to isolate internal standard peaks by matching known m/z and retention time windows, construct an interactive plot using Plotly or equivalent framework with retention time on the x-axis, m/z on the y-axis, intensity encoded as point size or color intensity, and sample identity as a grouping or faceting dimension. Implement interactive hover tooltips to display sample name, retention time, m/z, and intensity for each internal standard measurement. This multi-dimensional encoding allows a single glyph to convey four variables simultaneously, enabling rapid detection of clusters, outliers, or temporal drift patterns that would require separate univariate plots. Export the interactive visualization as an HTML file to preserve interactivity for real-time monitoring or as PNG/PDF for static reporting.

## Related tools

- **Plotly** (Interactive plotting framework used to construct multi-dimensional scatter plots with retention time, m/z, intensity, and sample faceting)
- **MSConvert** (Vendor format data conversion to open mzML format, prerequisite for downstream peak detection) — https://proteowizard.sourceforge.io/tools/msconvert.html
- **MS-DIAL** (Data processing and peak detection to generate feature tables with internal standard identifications, retention times, m/z, and intensities) — http://prime.psc.riken.jp/compms/msdial/main.html

## Evaluation signals

- Interactive plot renders without errors and all four dimensions (retention time, m/z, intensity, sample identity) are visually distinguishable.
- Hover tooltips display correct sample name, retention time (±0.1 min precision), m/z (±0.01 m/z precision), and intensity values matching the input table.
- Internal standard peaks cluster tightly in retention time and m/z space across replicates; significant outliers or drift patterns are visually apparent and correspond to known instrument events (e.g., column change, solvent lot change).
- Exported HTML file is interactive and facets or filters can be applied; PNG/PDF exports preserve all visual encodings.
- Point size or color gradation accurately reflects relative intensity differences; no intensity values are visually clipped or distorted.

## Limitations

- Rapid QC-MS has been tested extensively only on Thermo Fisher mass spectrometers and Thermo RAW files; other vendor formats may have undiscovered bugs.
- Interactive performance degrades with very large sample sets (>10,000 samples); point overplotting reduces discernibility of individual observations.
- Visualization assumes internal standard m/z and retention time reference windows are correctly specified; misspecified windows will result in empty or spurious plots.
- Color and size encoding can introduce perceptual bias; colorblind users may struggle to distinguish intensity gradations if color alone is used without accompanying size encoding.

## Evidence

- [other] Construct an interactive plot (using Plotly or similar framework) with retention time on the x-axis, m/z on the y-axis, and intensity encoded as point size or color, with sample identity as a grouping or faceting dimension.: "Construct an interactive plot (using Plotly or similar framework) with retention time on the x-axis, m/z on the y-axis, and intensity encoded as point size or color, with sample identity as a"
- [other] Implement interactive hover tooltips displaying sample name, retention time, m/z, and intensity for each internal standard measurement.: "Implement interactive hover tooltips displaying sample name, retention time, m/z, and intensity for each internal standard measurement."
- [intro] Interactive data visualization of internal standard retention time, _m/z_, and intensity across samples: "Interactive data visualization of internal standard retention time, _m/z_, and intensity across samples"
- [readme] Python packages, including: Pandas, SQLAlchemy, Plotly Dash, Bootstrap, Watchdog, Google API, Slack API: "Python packages, including: Pandas, SQLAlchemy, Plotly Dash, Bootstrap, Watchdog, Google API, Slack API"
- [other] Export the interactive visualization as an HTML or static image file (PNG/PDF) and save to the output directory.: "Export the interactive visualization as an HTML or static image file (PNG/PDF) and save to the output directory."
