---
name: statistical-visualization-multi-group
description: Use when when you have loaded search results from two or more DIA-MS
  analysis tools (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3365
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

# Statistical Visualization of Multi-Group Comparisons

## Summary

Generate interactive visualizations (bar plots, violin plots, upset plots) to compare feature identification, quantification, and variation metrics across multiple DIA-MS search tools or experimental conditions. This skill enables rapid visual assessment of agreement and disagreement in analyte detection and measurement across different analysis pipelines.

## When to use

When you have loaded search results from two or more DIA-MS analysis tools (e.g., DIA-NN and OpenSwath) or multiple experimental replicates and need to visualize and compare their feature identifications, log2 quantifications, and coefficient of variation values to assess consistency and tool/condition effects.

## When NOT to use

- Input contains only a single search tool output (multi-group comparison requires ≥2 groups for meaningful visualization).
- Feature identifications have not been filtered to a high-confidence set (e.g., unfiltered all-hits list will obscure patterns).
- Analyte count is extremely large (>10,000 unique features) without prior aggregation or subset selection, as violin plots and upset plots become uninterpretable.

## Inputs

- Search results file paths from multiple DIA-MS tools (e.g., DIA-NN output, OpenSwath OSW format)
- Tool metadata (software identifier, experiment label)
- Q-value cutoff threshold (e.g., 0.01 for 1% FDR)
- Analyte or feature list for selection

## Outputs

- Identifications bar plot (Bokeh-rendered interactive plot)
- Log2 quantifications violin plot (per-tool distribution)
- Coefficient of variation violin plot (per-tool precision comparison)
- Upset comparisons plot (analyte overlap across tools)
- Summary table (CSV) with feature scores, Q-values, and tool-specific metadata

## How to apply

After filtering search results at a specified Q-value cutoff (e.g., 1% Q-value threshold) to retain high-confidence identifications, extract feature identification counts, log2 quantification values, and coefficient of variation statistics for each analyte per tool or group. Use an interactive plotting framework (Bokeh-based InteractivePlotter in MassDash) to generate three complementary visualizations: (1) an identifications bar plot showing detection frequency per analyte across tools; (2) log2 quantifications violin plots to display distribution shape and central tendency for each tool/group; and (3) coefficient of variation violin plots to compare measurement precision. Construct an upset comparisons plot to reveal which analytes are detected by all tools (core set) versus tool-specific or pairwise-specific detections. Export the summary table with feature scores and metadata as CSV for downstream analysis or publication.

## Related tools

- **MassDash** (Web-based dashboard that orchestrates search result loading, filtering, and interactive multi-group visualization using Bokeh plots and upset diagrams.) — https://github.com/Roestlab/massdash
- **Streamlit** (Graphical user interface framework that hosts the MassDash dashboard for interactive parameter control and real-time plot rendering.)
- **Bokeh** (Interactive plotting library that renders the main area visualizations including bar plots, violin plots, and upset plots with hover tools and legend interactivity.)
- **ResultsLoader** (MassDash module that loads search result file paths and tool metadata for each search tool to be compared.)
- **OSWDataAccess** (Tool-specific loader for OpenSwath (OSW) search results, enabling OpenSwath output integration into multi-group comparison workflows.)
- **InteractivePlotter** (MassDash module that generates identifications bar plots, log2 quantifications violin plots, coefficient of variation plots, and upset comparisons using Bokeh rendering.)

## Evaluation signals

- Each visualization panel renders without errors and displays data for all groups/tools included in the comparison.
- Q-value filtering correctly removes analytes above the specified cutoff; verify by checking that all identifications in the summary table have Q-value ≤ threshold.
- Violin plots show non-empty distributions for log2 quantification and CV values per tool/group; presence of NaN or missing data points should be logged and investigated.
- Upset plot correctly captures set overlaps: the sum of all individual and intersection counts should equal the total analyte count after filtering.
- CSV export is valid and contains all rows from the summary table with matching feature counts and no truncated or corrupted fields.

## Limitations

- Upset plots become difficult to interpret when the number of groups exceeds 4–5; consider subsetting or aggregating data.
- Performance may degrade if >10,000 analytes are included; pre-filtering to high-confidence or abundant features is recommended.
- Violin plots require sufficient replicates or measurements per group; groups with <3 observations may produce misleading visualizations.
- The visualization assumes that analytes are identified by the same naming convention across tools; mismatched identifiers will fragment the comparison.

## Evidence

- [other] MassDash accepts the file path for search result files containing feature identification results, enabling users to load outputs from different tools (such as DIA-NN and OpenSwath) for comparison and visualization.: "MassDash accepts the file path for search result files containing feature identification results, enabling users to load outputs from different tools (such as DIA-NN and OpenSwath) for comparison and"
- [other] Apply Q-value filtering at the specified cutoff threshold using results filtering at Q-value to select high-confidence identifications.: "Apply Q-value filtering at the specified cutoff threshold using results filtering at Q-value to select high-confidence identifications."
- [other] Generate an identifications bar plot, log2 quantifications violin plot, and coefficient of variation violin plot using InteractivePlotter with Bokeh rendering.: "Generate an identifications bar plot, log2 quantifications violin plot, and coefficient of variation violin plot using InteractivePlotter with Bokeh rendering."
- [other] Construct an upset comparisons plot to show overlaps in identified analytes across different search tools.: "Construct an upset comparisons plot to show overlaps in identified analytes across different search tools."
- [other] The main area will be populated with interactive Bokeh figures: "The main area will be populated with interactive Bokeh figures"
- [other] Compile results into a summary table with feature scores and variables, then export as CSV.: "Compile results into a summary table with feature scores and variables, then export as CSV."
