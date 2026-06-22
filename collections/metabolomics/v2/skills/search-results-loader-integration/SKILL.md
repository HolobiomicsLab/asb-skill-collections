---
name: search-results-loader-integration
description: Use when you have search result files from one or more DIA-MS analysis tools and need to load them into a unified environment for Q-value filtering, cross-tool comparison (upset plots), and interactive visualization of identifications, quantifications, and coefficient of variation metrics across.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Streamlit
  - ResultsLoader
  - OSWDataAccess
  - InteractivePlotter
  - Bokeh
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

# search-results-loader-integration

## Summary

Load and parse feature identification results from multiple DIA-MS search tools (e.g., DIA-NN, OpenSwath) into a unified data structure for downstream filtering, comparison, and visualization. This skill enables interoperability between heterogeneous proteomics search outputs by ingesting tool-specific file formats and metadata.

## When to use

You have search result files from one or more DIA-MS analysis tools and need to load them into a unified environment for Q-value filtering, cross-tool comparison (upset plots), and interactive visualization of identifications, quantifications, and coefficient of variation metrics across analytes.

## When NOT to use

- Input is already a feature table or quantification matrix; use this skill only when raw search result files require parsing.
- Search results are from targeted quantification workflows (SRM/MRM) rather than DIA-MS; this skill is optimized for DIA search tool outputs.
- Only a single search tool's results are available and no cross-tool comparison is required; simpler loaders may suffice.

## Inputs

- Search result file path (containing feature identification results from DIA-MS analysis tool)
- Tool metadata (software identifier, experiment label)
- Q-value cutoff threshold (e.g., 0.01 for 1% FDR)

## Outputs

- Parsed feature identifications per analyte (unified data structure)
- Log2 quantification values for each identified feature
- Coefficient of variation values for identified features
- Filtered results at specified Q-value cutoff
- Comparison summary table (feature scores, variables) exportable as CSV

## How to apply

Instantiate the appropriate results loader (ResultsLoader for generic formats or tool-specific accessors like OSWDataAccess for OpenSwath) with the file path and tool metadata (software identifier, experiment label). The loader parses feature identification results, log2 quantifications, and coefficient of variation values into a standardized internal representation. Q-value filtering at a specified cutoff (e.g., 1%) is then applied to retain only high-confidence identifications. The filtered results are extracted as feature sets per analyte, enabling downstream construction of comparison plots (upset, bar, violin) and export to CSV summaries. Success is indicated by: (1) no parsing errors on input files, (2) post-filtering analyte counts matching expected thresholds, and (3) consistent feature overlap across tools in upset plots.

## Related tools

- **ResultsLoader** (Generic loader interface for parsing search result files and extracting feature identification, quantification, and quality metrics into unified data structures.) — https://github.com/Roestlab/massdash
- **OSWDataAccess** (Tool-specific loader for OpenSwath search results; handles OpenSwath-formatted output files and metadata.) — https://github.com/Roestlab/massdash
- **InteractivePlotter** (Downstream consumer of loaded and filtered results; generates upset plots, violin plots, and bar plots for comparison and visualization.) — https://github.com/Roestlab/massdash
- **Streamlit** (Web-based GUI framework through which ResultsLoader and OSWDataAccess are exposed to users for interactive file path input and tool selection.) — https://github.com/Roestlab/massdash
- **Bokeh** (Rendering backend for interactive figures generated from loaded and filtered search results.) — https://github.com/Roestlab/massdash

## Evaluation signals

- No parsing or file format errors occur when loading search result files from specified tools.
- Post-Q-value-filter analyte count matches expected high-confidence subset (typically 1% FDR or stricter).
- Feature overlap in upset plots shows logical consistency: analytes identified by both tools appear at expected intersection counts.
- Log2 quantification and coefficient of variation distributions are populated for all filtered analytes; no missing or NaN values in exported CSV.
- Cross-tool comparisons reveal expected patterns (e.g., if tools are similar, high overlap; if complementary, lower overlap but no contradictions in Q-values).

## Limitations

- Tool-specific loaders (e.g., OSWDataAccess) are required for each search tool; format mismatch between input file and loader causes silent data loss or parsing failure.
- Q-value filtering is applied uniformly across all loaded tools; if tool-specific cutoffs are required, additional filtering logic must be implemented.
- Loader does not validate that log2 quantifications are comparable across tools (e.g., normalization or scale differences); user must assess commensurability.
- Large result files may require significant memory for parsing; no streaming or chunked I/O is mentioned in the article.

## Evidence

- [other] MassDash accepts the file path for search result files containing feature identification results, enabling users to load outputs from different tools (such as DIA-NN and OpenSwath) for comparison and visualization.: "MassDash accepts the file path for search result files containing feature identification results, enabling users to load outputs from different tools"
- [other] Load search results file paths and tool metadata (software identifier, experiment label) for each search tool via ResultsLoader or tool-specific loaders (e.g., OSWDataAccess for OpenSwath results).: "Load search results file paths and tool metadata (software identifier, experiment label) for each search tool via ResultsLoader or tool-specific loaders (e.g., OSWDataAccess for OpenSwath results)"
- [other] Apply Q-value filtering at the specified cutoff threshold using results filtering at Q-value to select high-confidence identifications.: "Apply Q-value filtering at the specified cutoff threshold using results filtering at Q-value to select high-confidence identifications"
- [other] Extract feature identifications, log2 quantifications, and coefficient of variation values for each analyte.: "Extract feature identifications, log2 quantifications, and coefficient of variation values for each analyte"
- [other] The sidebar provides settings to control results at a specified Q-value cutoff: "The sidebar provides settings to control results at a specified Q-value cutoff"
- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
