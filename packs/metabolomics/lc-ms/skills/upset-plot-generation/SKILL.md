---
name: upset-plot-generation
description: Use when after loading and filtering search results from two or more DIA-MS analysis tools at a specified Q-value cutoff, when you need to summarize which analytes are identified by all tools, by specific subsets, or uniquely by individual tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
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

# upset-plot-generation

## Summary

Generate upset plots to visualize overlaps and unique identifications across multiple DIA-MS search tools (e.g., DIA-NN, OpenSwath). This skill enables comparative proteomics analysis by showing which analytes are consistently identified, tool-specific, or missed across different algorithms.

## When to use

After loading and filtering search results from two or more DIA-MS analysis tools at a specified Q-value cutoff, when you need to summarize which analytes are identified by all tools, by specific subsets, or uniquely by individual tools. Use this when comparing algorithm performance or consensus across DIA-NN, OpenSwath, or similar tools.

## When NOT to use

- When comparing results from only a single DIA-MS tool—upset plots require ≥2 tool outputs to show intersections.
- When analytes have not been pre-filtered by Q-value or other confidence threshold, as low-confidence identifications will obscure genuine tool agreement.
- When the research goal is tool-specific optimization rather than cross-tool consensus; use individual tool performance metrics instead.

## Inputs

- Search results files from DIA-MS tools (e.g., DIA-NN native format, OpenSwath .osw)
- Q-value filtering threshold (e.g., 0.01 for 1% FDR)
- Tool metadata (software identifier, experiment label for each search tool)
- Feature identification table with analyte names and tool membership

## Outputs

- Interactive upset plot (Bokeh figure) showing analyte intersection sizes across tools
- Intersection summary table with set membership and counts
- CSV export with feature scores and tool membership variables

## How to apply

Extract feature identifications for each analyte from pre-filtered search results files (Q-value filtered at your chosen threshold, typically 1%). Organize identifications by tool name as separate binary presence/absence columns. Pass this data to MassDash's InteractivePlotter with upset plot configuration enabled. The upset plot renders intersection sizes and prevalence patterns using Bokeh, allowing users to identify overlapping and tool-specific identifications. Interpret the plot by examining the intersection bars (sorted by size) to rank discovery commonality and the dots along the left margin to show which tools contributed to each intersection.

## Related tools

- **MassDash** (Orchestrates loading of multi-tool search results, applies Q-value filtering, and renders upset plot via InteractivePlotter module) — https://github.com/Roestlab/massdash
- **Streamlit** (Provides web-based graphical user interface for interactive upset plot visualization and parameter adjustment)
- **Bokeh** (Renders interactive upset plot figures with zoom, pan, and hover inspection capabilities)
- **ResultsLoader** (Generic loader for search result file paths and tool metadata (software identifier, experiment label)) — https://github.com/Roestlab/massdash
- **OSWDataAccess** (Tool-specific loader for OpenSwath .osw result files) — https://github.com/Roestlab/massdash
- **InteractivePlotter** (Constructs upset comparisons plot and other interactive visualizations using Bokeh rendering) — https://github.com/Roestlab/massdash

## Evaluation signals

- Upset plot displays all expected tool names as binary columns on the left sidebar and all possible non-empty intersections.
- Intersection bar heights are proportional to the number of analytes shared across the corresponding tool subset.
- Analytes are correctly classified as tool-specific (single bar) or shared (multiple intersecting bars); totals match the cardinality of each input tool's filtered identifications.
- CSV export contains one row per analyte with tool membership columns (0/1 indicator) and feature score columns; row count equals the union of all tool identifications.
- Interactive hover tooltips display analyte counts for each intersection; plot responds to zoom/pan controls without data loss.

## Limitations

- Upset plots scale poorly when more than ~10 tools are compared; intersection bar legibility degrades and dominant patterns may become obscured.
- The upset plot does not indicate which specific analytes belong to each intersection—use the CSV export or drill-down table for detailed analyte-level membership queries.
- Q-value filtering is a hard cutoff; analytes just above or below the threshold (e.g., Q-value 0.011 when threshold is 0.01) will dramatically appear/disappear from the plot, potentially masking near-threshold detections.
- Tool-specific biases in identification patterns (e.g., retention time prediction accuracy, window construction) are not corrected by the upset plot; interpretation requires knowledge of tool parameterization and input data characteristics.

## Evidence

- [other] Construct an upset comparisons plot to show overlaps in identified analytes across different search tools.: "Construct an upset comparisons plot to show overlaps in identified analytes across different search tools."
- [other] The sidebar provides settings to control results at a specified Q-value cutoff: "The sidebar provides settings to control results at a specified Q-value cutoff"
- [other] Load search results file paths and tool metadata (software identifier, experiment label) for each search tool via ResultsLoader or tool-specific loaders (e.g., OSWDataAccess for OpenSwath results).: "Load search results file paths and tool metadata (software identifier, experiment label) for each search tool via ResultsLoader or tool-specific loaders (e.g., OSWDataAccess for OpenSwath results)."
- [other] The main area will be populated with interactive Bokeh figures: "The main area will be populated with interactive Bokeh figures"
- [other] Compile results into a summary table with feature scores and variables, then export as CSV.: "Compile results into a summary table with feature scores and variables, then export as CSV."
