---
name: multi-tool-results-comparison
description: Use when you have feature identification outputs from two or more DIA-MS
  search tools (e.g., DIA-NN and OpenSwath result files) and need to assess their
  agreement on analyte detection, quantification, and scoring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Streamlit
  - ResultsLoader
  - OSWDataAccess
  - InteractivePlotter
  - MassDash
  - Bokeh
  techniques:
  - LC-MS
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Multi-tool Results Comparison

## Summary

Load and compare search results from different DIA-MS analysis tools (e.g., DIA-NN, OpenSwath) within a unified visualization framework, enabling quantitative assessment of tool agreement and feature identification overlap. This skill is essential for validating DIA-MS workflows and understanding concordance between independent computational pipelines.

## When to use

Apply this skill when you have feature identification outputs from two or more DIA-MS search tools (e.g., DIA-NN and OpenSwath result files) and need to assess their agreement on analyte detection, quantification, and scoring. Use it to benchmark tool performance, validate pipeline robustness, or identify analytes with high vs. low cross-tool confidence.

## When NOT to use

- Input data are already merged or aggregated from a single consensus pipeline — use this skill only when you have independent, unmerged outputs from two or more separate search tools.
- Search result files lack Q-value or feature score annotations — Q-value filtering is a core step; files without quality metrics cannot be reliably compared.
- The goal is merely to visualize raw spectra or chromatograms rather than compare tool identifications and quantifications — use single-tool chromatogram visualization instead.

## Inputs

- Search result files from DIA-MS tool 1 (e.g., DIA-NN output with feature scores and Q-values)
- Search result files from DIA-MS tool 2 (e.g., OpenSwath .osw SQLite database or equivalent)
- Tool metadata (software identifier, experiment label) for each search tool
- Q-value filtering threshold (e.g., 0.01 for 1% FDR cutoff)

## Outputs

- Identifications bar plot (Bokeh interactive) showing analyte detection counts per tool
- Log2 quantifications violin plot (Bokeh interactive) comparing distribution across tools
- Coefficient of variation violin plot (Bokeh interactive) comparing precision across tools
- Upset plot (Bokeh interactive) showing overlap and unique identifications per tool
- Summary table (CSV export) with feature scores, Q-values, log2 quantifications, and coefficient of variation from each tool

## How to apply

Load search result file paths and tool metadata (software identifier, experiment label) for each tool via ResultsLoader or tool-specific loaders such as OSWDataAccess for OpenSwath results. Apply Q-value filtering at a specified cutoff threshold (e.g., 1% FDR) using the results filtering module to select high-confidence identifications from each tool independently. Extract feature identifications, log2 quantifications, and coefficient of variation values for each analyte. Generate comparative visualizations including an identifications bar plot (count of detected analytes per tool), log2 quantifications violin plots (to assess quantification distribution), and coefficient of variation violin plots (to assess precision). Construct an upset plot to show overlaps and tool-specific-only identifications. Compile results into a summary table with feature scores and variables from all tools, then export as CSV for downstream statistical testing or integration.

## Related tools

- **MassDash** (Web-based dashboard and Python package that implements multi-tool results loading, Q-value filtering, and interactive visualization via Bokeh) — https://github.com/Roestlab/massdash
- **ResultsLoader** (MassDash module for loading and normalizing search result file paths and tool metadata) — https://github.com/Roestlab/massdash
- **OSWDataAccess** (Tool-specific loader for OpenSwath .osw SQLite database results) — https://github.com/Roestlab/massdash
- **InteractivePlotter** (MassDash module that generates bar plots, violin plots, and upset plots using Bokeh rendering) — https://github.com/Roestlab/massdash
- **Streamlit** (Web framework providing the graphical user interface (GUI) for MassDash)
- **Bokeh** (Interactive visualization library used to render and populate comparative plots in the main panel)

## Evaluation signals

- All tools successfully load their respective search result files without file format or parsing errors.
- Q-value filtering is applied consistently across all tools at the specified cutoff threshold (e.g., 1% FDR); verify that the count of analytes after filtering matches the query applied.
- Upset plot shows non-empty overlap regions and tool-specific regions; at least two tools agree on some subset of identifications, indicating true consensus rather than complete disagreement.
- Summary table row count matches the union of all identified analytes across tools; each tool's quantifications and Q-values are populated without NaN or sentinel values where expected.
- Coefficient of variation and log2 quantification distributions in violin plots show non-trivial variation across tools (i.e., not all identical), indicating that the comparison is meaningful; tools with systematically lower CV suggest higher precision.

## Limitations

- Comparison requires that all input search result files contain Q-value or equivalent feature confidence scores; files lacking these annotations cannot be filtered reliably.
- The upset plot assumes that analytes are uniquely identifiable across tools by their identifier (e.g., peptide sequence, mass, retention time); misaligned identifiers or naming conventions between tools may lead to false negatives in overlap detection.
- Q-value filtering is applied independently per tool before comparison; this can lead to different sets of high-confidence analytes per tool and may obscure true discordance between tools on borderline features.
- Visualization of large numbers of analytes (>10,000) may degrade interactivity due to Bokeh rendering overhead; performance is not quantified in the article.
- The workflow does not implement automated outlier detection or tool-specific bias correction; practitioners must interpret violin plots and summary statistics manually to identify systematic differences.

## Evidence

- [other] MassDash accepts the file path for search result files containing feature identification results, enabling users to load outputs from different tools (such as DIA-NN and OpenSwath) for comparison and visualization.: "MassDash accepts the file path for search result files containing feature identification results, enabling users to load outputs from different tools (such as DIA-NN and OpenSwath) for comparison and"
- [other] Load search results file paths and tool metadata (software identifier, experiment label) for each search tool via ResultsLoader or tool-specific loaders (e.g., OSWDataAccess for OpenSwath results).: "Load search results file paths and tool metadata (software identifier, experiment label) for each search tool via ResultsLoader or tool-specific loaders (e.g., OSWDataAccess for OpenSwath results)."
- [other] Apply Q-value filtering at the specified cutoff threshold using results filtering at Q-value to select high-confidence identifications.: "Apply Q-value filtering at the specified cutoff threshold using results filtering at Q-value to select high-confidence identifications."
- [other] Extract feature identifications, log2 quantifications, and coefficient of variation values for each analyte.: "Extract feature identifications, log2 quantifications, and coefficient of variation values for each analyte."
- [other] Generate an identifications bar plot, log2 quantifications violin plot, and coefficient of variation violin plot using InteractivePlotter with Bokeh rendering.: "Generate an identifications bar plot, log2 quantifications violin plot, and coefficient of variation violin plot using InteractivePlotter with Bokeh rendering."
- [other] Construct an upset comparisons plot to show overlaps in identified analytes across different search tools.: "Construct an upset comparisons plot to show overlaps in identified analytes across different search tools."
- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] The sidebar provides settings to control results at a specified Q-value cutoff: "The sidebar provides settings to control results at a specified Q-value cutoff"
- [other] MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI): "MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)"
- [other] The main area will be populated with interactive Bokeh figures: "The main area will be populated with interactive Bokeh figures"
