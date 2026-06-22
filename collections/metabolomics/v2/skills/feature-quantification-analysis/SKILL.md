---
name: feature-quantification-analysis
description: Use when when you have loaded search result files from one or more DIA-MS analysis tools and need to assess the quantitative performance of identified features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Streamlit
  - ResultsLoader
  - OSWDataAccess
  - InteractivePlotter
  - Bokeh
  - MassDash
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- streamlit graphical user interface (GUI)
- ResultsLoader
- OSWDataAccess
- InteractivePlotter
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massdash_cq
    doi: 10.1021/acs.jproteome.4c00026
    title: MassDash
  dedup_kept_from: coll_massdash_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00026
  all_source_dois:
  - 10.1021/acs.jproteome.4c00026
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-quantification-analysis

## Summary

Extract and visualize log₂ quantifications and coefficient of variation (CV) metrics for identified peptide features across DIA-MS search results, enabling comparison of quantitative accuracy and reproducibility between different analysis tools (e.g., DIA-NN vs. OpenSwath).

## When to use

When you have loaded search result files from one or more DIA-MS analysis tools and need to assess the quantitative performance of identified features. Specifically, use this skill when: (1) you want to compare log₂ quantification distributions across tools or experimental conditions, (2) you need to evaluate feature stability via coefficient of variation, or (3) you aim to identify high-confidence analytes based on consistent quantification and low variance.

## When NOT to use

- Input already contains pre-summarized (e.g., aggregated protein-level) quantifications; extract feature-level data first.
- Search results are from a single tool with no comparative goal; use basic visualization instead.
- Q-value filtering has already been applied upstream; re-filtering may introduce bias or exclude valid data.

## Inputs

- Search result file paths (DIA-NN, OpenSwath, or other DIA-MS tool outputs)
- Tool metadata (software identifier, experiment label)
- Q-value cutoff threshold (numeric, e.g., 0.01 for 1% FDR)
- Feature identification records with log₂ quantifications and coefficient of variation

## Outputs

- Log₂ quantifications violin plot (interactive Bokeh figure)
- Coefficient of variation violin plot (interactive Bokeh figure)
- Summary table with feature scores, quantification values, and CV metrics (CSV export)
- Analyte comparison metadata for downstream analysis

## How to apply

Load search results containing feature identification and log₂ quantification values using ResultsLoader or tool-specific loaders (e.g., OSWDataAccess for OpenSwath). Apply Q-value filtering at your chosen cutoff threshold (e.g., 1% FDR) to retain only high-confidence identifications. Extract the log₂ quantification and coefficient of variation values for each identified analyte. Generate violin plots using InteractivePlotter with Bokeh rendering to visualize distributions of log₂ quantifications across tool groups or conditions; coefficient of variation plots show feature stability. Compile results into a summary table with feature scores and variables, then export as CSV for downstream statistical analysis or reporting.

## Related tools

- **ResultsLoader** (Load and parse search result files, extracting feature identification and quantification records) — https://github.com/Roestlab/massdash
- **OSWDataAccess** (Tool-specific loader for OpenSwath search result files (OSW format)) — https://github.com/Roestlab/massdash
- **InteractivePlotter** (Generate violin plots and other interactive visualizations of quantification and CV distributions) — https://github.com/Roestlab/massdash
- **Bokeh** (Render interactive web-based violin and comparison plots for exploration)
- **Streamlit** (Host interactive GUI dashboard for loading data, setting parameters, and viewing quantification plots) — https://github.com/Roestlab/massdash
- **MassDash** (Modular Python package integrating all loaders, filters, and plotters for DIA-MS quantification analysis) — https://github.com/Roestlab/massdash

## Examples

```
from massdash.loaders import ResultsLoader; from massdash.plotters import InteractivePlotter; loader = ResultsLoader('path/to/diaNN_results.tsv'); features = loader.load(q_value_cutoff=0.01); plotter = InteractivePlotter(features); plotter.plot_log2_quantifications_violin('condition'); plotter.plot_cv_violin(); features.to_csv('quantification_summary.csv')
```

## Evaluation signals

- Violin plots show expected distribution shapes (e.g., unimodal or multimodal) with no rendering errors or missing values.
- Summary table contains one row per identified analyte with non-null log₂ quantification and CV values; row counts match the number of features passing Q-value cutoff.
- CV values lie within reasonable biological range (typically 0.05–1.0 for DIA features); values outside this range warrant investigation of outlier features.
- Comparing two tools: upset plot and summary table show concordance in identified analytes; tools identifying the same analyte should have comparable quantification distributions.
- CSV export is valid and parseable; column headers match expected schema (feature ID, log₂ quantification, coefficient of variation, tool identifier, Q-value).

## Limitations

- Coefficient of variation calculation requires multiple replicates per feature; single-injection or sparse data may yield unreliable CV estimates.
- Q-value filtering at very stringent thresholds (e.g., <0.001) may exclude true features with borderline scores, reducing sample size for downstream comparisons.
- Visualization of violin plots is most effective with ≥50 features per group; smaller datasets may appear sparse or uninterpretable.
- Log₂ transformation assumes all quantification values are positive; zero or negative values from upstream processing will cause failures or undefined logarithms.

## Evidence

- [other] Extract feature identifications, log2 quantifications, and coefficient of variation values for each analyte: "Extract feature identifications, log2 quantifications, and coefficient of variation values for each analyte."
- [other] Generate an identifications bar plot, log2 quantifications violin plot, and coefficient of variation violin plot using InteractivePlotter with Bokeh rendering: "Generate an identifications bar plot, log2 quantifications violin plot, and coefficient of variation violin plot using InteractivePlotter with Bokeh rendering."
- [other] Apply Q-value filtering at the specified cutoff threshold using results filtering at Q-value to select high-confidence identifications: "Apply Q-value filtering at the specified cutoff threshold using results filtering at Q-value to select high-confidence identifications."
- [other] The sidebar provides settings to control results at a specified Q-value cutoff: "The sidebar provides settings to control results at a specified Q-value cutoff"
- [other] Compile results into a summary table with feature scores and variables, then export as CSV: "Compile results into a summary table with feature scores and variables, then export as CSV."
