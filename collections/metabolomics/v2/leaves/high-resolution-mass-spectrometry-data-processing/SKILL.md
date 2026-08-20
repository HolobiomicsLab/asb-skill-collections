---
name: high-resolution-mass-spectrometry-data-processing
description: Use when you have uploaded a delimited data file (CSV, TSV, or semicolon-separated)
  containing at least m/z values and intensity columns from HRMS analysis of a complex
  sample, and you need to (1) verify that column keywords are correctly recognized,
  (2) compute derived metrics such as Normalized.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Punc'data
  - d3.js
  - PCA-JS
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.5c00151
  title: Punc’data
evidence_spans:
- Punc'data is an interactive attribution and vizualization tool made for high resolution
  mass spectrometry results.
- Punc'data is an interactive attribution and vizualization tool made for high resolution
  mass spectrometry results
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_punc_data_cq
    doi: 10.1021/jasms.5c00151
    title: Punc’data
  dedup_kept_from: coll_punc_data_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00151
  all_source_dois:
  - 10.1021/jasms.5c00151
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# high-resolution-mass-spectrometry-data-processing

## Summary

Interactive filtering, selection, and visualization of high-resolution mass spectrometry (HRMS) results from complex samples via keyword-based column recognition and multi-tab analysis workflows. This skill enables practitioners to load peak lists with m/z and intensity data, automatically map column semantics, and generate interactive Kendrick mass plots, statistical summaries, and comparative visualizations (PCA, Venn, network).

## When to use

Apply this skill when you have uploaded a delimited data file (CSV, TSV, or semicolon-separated) containing at least m/z values and intensity columns from HRMS analysis of a complex sample, and you need to (1) verify that column keywords are correctly recognized, (2) compute derived metrics such as Normalized Kendrick Mass (NKM), or (3) select alternative x-axis representations (m/z vs. NKM) for Kendrick mass plots before generating publication-quality visualizations.

## When NOT to use

- Input file lacks clear column headers or does not follow delimited format (non-tabular structure)
- Data is already pre-processed into a feature matrix or aggregated format; use this skill for raw peak list curation, not post-hoc matrix analysis
- Analysis goal is purely statistical (e.g., univariate testing on pre-assigned features) rather than exploratory visualization or column mapping

## Inputs

- Delimited data file (CSV, TSV, semicolon-separated) with first line containing column headers
- Column containing m/z values (keyword-recognized or manually specified)
- Column containing intensity values
- Optional: formula column for molecular formula assignment

## Outputs

- Parsed peak list with recognized m/z and intensity columns
- Computed Normalized Kendrick Mass (NKM) column (if Kendrick analysis selected)
- Interactive Kendrick mass plot with selectable x-axis (m/z or NKM)
- Interactive Canvas A/B visualization with configurable axes and data representations
- Statistical summaries (Stats tab)
- Comparison matrices, Venn diagrams, or PCA plots (for multi-sample analysis)

## How to apply

Upload a data file with column delimiters (`;`, `,`, or tab) specified via the gear icon in the Data Manager tab. Punc'data automatically recognizes columns by keyword (m/z, intensity, formula); verify or manually edit these mappings in the Parameters tab. Once column semantics are confirmed, navigate to Canvas or Stats tabs and select your visualization type. For Kendrick mass analysis specifically: (1) load the parsed peak list with m/z values; (2) compute NKM for each peak using NKM = round(m/z × base mass) − (m/z × base mass rounded), where base mass is typically 14.0157 for CH₂ homolog series; (3) create a selector control to choose x-axis ('m/z' or 'NKM'); (4) pass the selected abscissa and corresponding intensity values to the plot renderer. Use the Premade Canvas option to quickly validate your workflow on test data before proceeding to analysis-specific visualizations.

## Related tools

- **Punc'data** (Primary interactive tool for filtering, selecting, visualizing, and comparing HRMS results; handles column recognition, Kendrick mass computation, and multi-tab canvas/stats/network generation) — https://github.com/WTVoe/puncdata
- **d3.js** (JavaScript library underlying all interactive plot rendering in Canvas and Stats tabs)
- **PCA-JS** (Library used for principal component analysis computation in PCA comparison tab) — https://github.com/bitanath/pca

## Evaluation signals

- Column keywords (m/z, intensity, formula) are correctly recognized and displayed in the Parameters tab; manual edits (if needed) are persisted across tabs.
- Computed Normalized Kendrick Mass values satisfy the invariant: NKM = round(m/z × 14.0157) − (m/z × 14.0157 rounded) for each row, producing decimal values in the range [0, 1).
- Kendrick mass plot x-axis toggle between 'm/z' and 'NKM' modes correctly switches the abscissa without corrupting intensity (y-axis) data; intensity ordering and point positions update dynamically.
- Interactive features (ctrl+click to pinpoint tooltip, shift+click to zoom, double-click to unzoom) respond as documented; chart state is invertible.
- Exported visualizations (PNG via html2canvas, or saved Punc'data session) preserve all user selections (axis choice, data filters, tooltip configurations) and can be reloaded without loss of metadata.

## Limitations

- Keyword-based column recognition depends on exact keyword presence (m/z, intensity, formula); columns with synonyms or non-English labels require manual mapping in Parameters tab.
- No explicit documentation of supported data formats beyond CSV or delimited files; binary formats (mzML, mzXML, NetCDF) are not mentioned and likely not directly supported.
- No validation criteria, quality control metrics, or statistical benchmarks are documented; users must manually inspect plotted data for anomalies (e.g., negative intensities, out-of-range m/z values).
- Kendrick mass plot assumes a single homolog series base mass (typically 14.0157); heterogeneous samples with multiple base masses require manual re-computation or post-hoc filtering.
- Performance and scalability limits are not specified; no guidance on maximum file size, number of peaks, or visualization responsiveness on large datasets.

## Evidence

- [readme] Punc'data recognizes column information based on keywords such as m/z value, intensity, and formula.: "Punc'data recognizes which column corresponds to which information based on keywords."
- [other] Normalized Kendrick Mass computation using base mass formula for homolog series analysis.: "NKM = round(m/z × base mass) − (m/z × base mass rounded), where base mass is the mass unit of interest (typically 14.0157 for CH₂ homolog series)."
- [readme] File upload and delimiter specification workflow.: "To vizualise data, you need to upload a file with separation (; , ...) between the columns. You can change the separator with the gear icon"
- [readme] Multi-tab analysis and visualization framework.: ""Tools" Tab allows automatized edition tools of your inputs. "Table", "Stats", "Canvas A/B" and "Network" allow different types of tables and charts"
- [other] Kendrick mass plot x-axis selector control implementation.: "Create a selector control (dropdown or toggle) that stores the user's choice of x-axis coordinate ('m/z' or 'NKM')."
