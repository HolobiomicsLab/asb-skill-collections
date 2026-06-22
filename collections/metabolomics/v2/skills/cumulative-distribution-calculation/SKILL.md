---
name: cumulative-distribution-calculation
description: Use when you have numeric distribution data (e.g., gene expression, abundance, or measurement values) in CSV format and need to compare cumulative empirical distributions either within a single cohort or across multiple sample groups (e.g., control vs. treatment, disease subtype vs. healthy).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_2269
  tools:
  - R Shiny
  - GraphBio
  - Docker
derived_from:
- doi: 10.3389/fgene.2022.957317
  title: GraphBio
evidence_spans:
- GraphBio---A modular and scalable R Shiny dashboard
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphbio_cq
    doi: 10.3389/fgene.2022.957317
    title: GraphBio
  dedup_kept_from: coll_graphbio_cq
schema_version: 0.2.0
---

# cumulative-distribution-calculation

## Summary

Compute and visualize cumulative distribution curves (CDCs) from omics data using GraphBio's R Shiny interface, supporting both single-group and multiple-group stratified analyses. This skill transforms raw distribution values into overlaid or faceted CDC figures suitable for comparing empirical distributions across experimental conditions or sample groups.

## When to use

Use this skill when you have numeric distribution data (e.g., gene expression, abundance, or measurement values) in CSV format and need to compare cumulative empirical distributions either within a single cohort or across multiple sample groups (e.g., control vs. treatment, disease subtype vs. healthy). It is particularly valuable when the research question requires visual assessment of whether distributions differ in central tendency, spread, or shape.

## When NOT to use

- Input data is categorical or ordinal without quantifiable numeric values; use categorical distribution plots (e.g., bar charts or pie plots) instead.
- Distribution has extreme outliers or heavy tails that make visual comparison misleading without log-transformation or robust scaling; consider preprocessing or alternative visualizations.
- Sample size is very small (n < 10 per group), making empirical CDFs sparse and unreliable; consider parametric or smoothed alternatives.

## Inputs

- cdc_example.csv (single-group CDC demo file with numeric distribution values)
- cdc_multiple_group.csv (multiple-group CDC demo file with distribution values and group labels)
- Numeric vector or matrix of distribution values
- Group assignment vector (for stratified analysis)

## Outputs

- Cumulative distribution curve figure (PNG or PDF) for single-group analysis
- Cumulative distribution curve figure (PNG or PDF) for multiple-group analysis with overlaid or faceted curves
- R data frame or list object containing computed CDF values and quantiles

## How to apply

Load the single-group or multiple-group CDC demo CSV file into R via GraphBio's Shiny UI. Parse the data structure to extract numeric distribution values; for multiple-group analyses, ensure group membership is explicitly encoded as a column or inferred from file naming convention (e.g., cdc_example.csv vs. cdc_multiple_group.csv). Compute cumulative distribution functions (CDFs) using R's built-in methods (e.g., ecdf()) for each group or stratum. Generate CDC figures using R Shiny visualization, overlaying curves for direct comparison or faceting by group for clarity. Export final figures as PNG or PDF. Validate that the cumulative proportions increase monotonically from 0 to 1 and that curve ordering and separation match biological expectations.

## Related tools

- **R Shiny** (Interactive web framework for loading demo CSV files, parsing data structure, computing cumulative distribution functions, and rendering overlaid or faceted CDC figures with real-time parameter control) — https://github.com/databio2022/GraphBio
- **GraphBio** (Modular R Shiny dashboard that encapsulates CDC computation and visualization workflows, providing pre-configured demo data (cdc_example.csv and cdc_multiple_group.csv) and export functionality) — https://github.com/databio2022/GraphBio
- **Docker** (Container runtime for deploying GraphBio to a web server without manual dependency installation; simplifies reproducible CDC analysis across platforms)

## Evaluation signals

- Cumulative proportions increase monotonically from 0 to 1 across the entire distribution range with no inversions or discontinuities.
- For multiple-group analyses, curves are visually separated or overlaid in a manner consistent with underlying data distributions; groups with larger median values should show rightward shifts.
- Exported PNG or PDF files display readable axes, legend, and curve labels; resolution and formatting meet publication standards.
- Quantile values extracted from CDC (e.g., median, quartiles) match independently computed R quantile() function outputs within floating-point precision.
- Data parsing correctly identifies and handles group labels, missing values, and numeric column types without throwing errors or silently coercing non-numeric values.

## Limitations

- GraphBio's CDC module relies on pre-structured CSV files (cdc_example.csv or cdc_multiple_group.csv); custom data formats or relational databases require manual reformatting before loading.
- Cumulative distribution curves assume independent observations; data with repeated measures or hierarchical structure may require blocking or stratification not natively supported in the demo interface.
- Visual overlay of many groups (>5–6) becomes cluttered and difficult to interpret; faceting is recommended but may not scale well for very large sample sizes or many strata.
- CDC figures do not include confidence bands or statistical hypothesis tests; users must rely on external tools (e.g., Kolmogorov–Smirnov, Anderson–Darling tests) to formally test distribution differences.

## Evidence

- [other] GraphBio implements cumulative distribution curves using two separate demo CSV files: cdc_example.csv for single-group analysis and cdc-mutiple-group.csv for multiple-group analysis.: "GraphBio implements cumulative distribution curves using two separate demo CSV files: cdc_example.csv for single-group analysis and cdc-mutiple-group.csv for multiple-group analysis."
- [other] Generate the cumulative distribution curve figures for the multiple-group dataset, displaying curves overlaid or faceted by group.: "Generate the cumulative distribution curve figures for the multiple-group dataset, displaying curves overlaid or faceted by group."
- [other] Export both single-group and multiple-group CDC figures as PNG or PDF outputs.: "Export both single-group and multiple-group CDC figures as PNG or PDF outputs."
- [readme] cdc_example.csv and cdc-mutiple-group.csv for Cumulative Distribution Curves: "cdc_example.csv and cdc-mutiple-group.csv for Cumulative Distribution Curves"
- [readme] GraphBio---A modular and scalable R Shiny dashboard: "GraphBio---A modular and scalable R Shiny dashboard"
