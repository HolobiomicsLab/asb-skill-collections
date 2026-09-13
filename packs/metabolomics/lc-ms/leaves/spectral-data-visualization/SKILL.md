---
name: spectral-data-visualization
description: Use when you have executed MassQL queries on mzML mass spectrometry data
  and need to communicate query results visually—particularly when comparing peak
  shapes across multiple files, assessing retention time distributions, or validating
  precursor/product ion matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MassQLab
  - MassQL
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1002/rcm.10132
  title: MassQLab
evidence_spans:
- github.com__JohnsonDylan__MassQLab
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massqlab_cq
    doi: 10.1002/rcm.10132
    title: MassQLab
  dedup_kept_from: coll_massqlab_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/rcm.10132
  all_source_dois:
  - 10.1002/rcm.10132
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Data Visualization

## Summary

Generate visual representations of mass spectrometry spectral data (MS1 and MS2) queried from mzML files, including peak traces, Gaussian fits, and scan intensity plots. This skill enables rapid interpretation of complex query results across large repositories of mass spectrometry data.

## When to use

Apply this skill when you have executed MassQL queries on mzML mass spectrometry data and need to communicate query results visually—particularly when comparing peak shapes across multiple files, assessing retention time distributions, or validating precursor/product ion matches. Use it when tabular results alone are insufficient to assess spectral pattern quality or consistency.

## When NOT to use

- Input is raw mzML data that has not yet been queried or filtered—use MassQL query execution first.
- Query results are empty or contain no matching scans—visualization will be uninformative.
- Analysis flag is set to false in configuration—downstream statistical visualization will not be generated.

## Inputs

- mzML mass spectrometry files (MS1 and/or MS2 data)
- MassQL query results in tabular format (CSV: ms1_raw_df.csv or ms2_raw_df.csv)
- Metadata: retention times, m/z values, scan intensities, precursor/product ion assignments

## Outputs

- MS1 visualization PDFs: ms1_traces.pdf (all Gaussian fits per query/file), ms1_summary_traces.pdf (summary across queries), ms1_summary_areas.pdf (peak areas per query)
- MS2 visualization PDFs: ms2_plots.pdf (scan intensities), ms2_summary_plots.pdf (top scan per query), ms2_cluster_plots.pdf (clustered by energy level)
- Consolidated PNG images: ms1_consolidated_traces.png (all MS1 traces with Gaussian fit overlay)

## How to apply

After MassQLab has executed MassQL queries and produced raw tabulated results (ms1_raw_df.csv or ms2_raw_df.csv), generate complementary visualizations. For MS1 data, fit Gaussian peaks to retention-time-aligned query hits and render peak traces with fitted curves overlaid; summarize areas and traces per query and per file. For MS2 data, plot scan intensities (with lines connecting shared MS1 precursor scans) and cluster by energy level or query group if applicable. Save outputs as multi-page PDFs and consolidated PNG images. Use the analysis module to extract peak areas, retention-time statistics, and intensity distributions before plotting, ensuring visual summaries reflect underlying statistical distributions rather than raw counts alone.

## Related tools

- **MassQLab** (executes MassQL queries and orchestrates spectral visualization pipeline; manages output directory structure and file naming for all trace, area, and cluster plots) — https://github.com/JohnsonDylan/MassQLab
- **MassQL** (query engine that filters and tabulates mass spectrometry data; output tables (ms1_raw_df.csv, ms2_raw_df.csv) feed into visualization module) — https://github.com/mwang87/MassQueryLanguage

## Examples

```
py src\MassQLab_console.py  # Executes full pipeline including query execution and spectral visualization with analysis=true in massqlab_config.json
```

## Evaluation signals

- All queried scans are represented in output plots with no dropped or missing entries; spot-check a high-intensity query result against corresponding trace in PDF.
- MS1 Gaussian fits visually align with actual peak shape in retention-time domain; R² or residual plots confirm goodness of fit.
- MS2 plots correctly link scans sharing the same MS1 precursor (verify line colors/grouping match precursor m/z and retention time).
- Peak area values in summary PDFs match integrated intensity values in raw result CSV (within rounding tolerance).
- Output file timestamps and query names appear correctly in plot titles and legends, confirming correct file and query linkage.

## Limitations

- Visualization quality depends on query specificity; overly broad queries may produce cluttered, uninterpretable plots with hundreds of overlapping traces.
- Gaussian peak fitting assumes unimodal, symmetric peak shapes; multi-modal or highly skewed chromatographic peaks may fit poorly and produce misleading visualizations.
- Large datasets (many files × many queries) generate multiple PDFs and PNG images that consume significant disk space; consolidation into single images may reduce resolution.
- Clustering by energy level (MS2) assumes metadata field is populated; missing or mislabeled energy annotations will result in incorrect plot grouping.

## Evidence

- [readme] Results are tabulated and saved as images and csv files: "MassQLab applies a series of queries (written in the language of MassQL) to a directory containing mass spectrometry data in mzML format. Results are tabulated and saved as images and csv files."
- [readme] MS1 and MS2 output files include both raw data and analysis-derived visualizations: "**MS1 Outputs**
- `ms1_raw_df.csv`: Raw query results + metadata  
- `ms1_analysis_df.csv`: Peak fitting analysis  
- `ms1_traces.pdf`: All Gaussian fits per query/file"
- [readme] Peak fitting and multi-level summarization strategy: "- `ms1_summary_traces.pdf`: Summary of Gaussian fits per query
- `ms1_summary_traces_inverse.pdf`: Summary of Gaussian fits per file
- `ms1_summary_areas.pdf`: Peak areas per query"
- [readme] MS2 visualization clustering and grouping: "- `ms2_cluster_plots.pdf`: Summary of MS2 analysis clustered by energy level if applicable
- `ms2_cluster_plots_group.pdf`: Summary of MS2 analysis by query group (if defined)"
- [readme] Analysis flag controls visualization generation: "- **`analysis`**  
  Whether to run downstream analysis on results returned from the MassQL queries (`true` or `false`)."
