---
name: group-stratified-curve-generation
description: Use when you have omics data with group labels (e.g., treatment vs. control,
  disease vs. healthy) and need to visualize how the cumulative distribution of a
  continuous variable (e.g., gene expression, abundance) differs between groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_0203
  tools:
  - R Shiny
  - GraphBio
  - Docker
  license_tier: open
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fgene.2022.957317
  all_source_dois:
  - 10.3389/fgene.2022.957317
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# group-stratified-curve-generation

## Summary

Generate cumulative distribution curves stratified by experimental group from omics data, enabling visual comparison of distributions across multiple sample cohorts or conditions. This skill partitions input data by group membership and overlays or facets the resulting curves to reveal group-level differences in distribution patterns.

## When to use

Apply this skill when you have omics data with group labels (e.g., treatment vs. control, disease vs. healthy) and need to visualize how the cumulative distribution of a continuous variable (e.g., gene expression, abundance) differs between groups. Use when exploratory comparison of distribution shapes and percentiles across cohorts is the analysis goal.

## When NOT to use

- Input contains only single-group data without group stratification labels — use single-group CDC instead.
- Cumulative distributions have already been pre-computed and exported; this skill is for generation from raw or aggregated distribution values.
- Sample size per group is < 2 or group membership is missing for >10% of records — insufficient data for reliable group-level curve estimation.

## Inputs

- Multi-group CSV file with columns for distribution values and group identifiers (e.g., cdc_multiple_group.csv)
- Group assignment labels or metadata column

## Outputs

- Overlaid or faceted cumulative distribution curve figure(s) showing distributions by group
- PNG or PDF export of stratified CDC visualization

## How to apply

Load the multi-group CSV file containing both distribution values and group assignment columns. Parse the data structure to extract distribution values stratified by group identifier. Compute cumulative distribution functions separately for each group using the stratified values. Render cumulative distribution curves overlaid or faceted by group using R Shiny visualization, ensuring curves are visually distinguishable (e.g., by color or panel). Export the resulting figure(s) as PNG or PDF. Verify that all unique groups in the input are represented and that curve endpoints align with expected cumulative probabilities (0–1 range).

## Related tools

- **R Shiny** (interactive web framework for rendering and exporting stratified cumulative distribution curve visualizations) — https://github.com/databio2022/GraphBio
- **GraphBio** (modular R Shiny dashboard application that implements cumulative distribution curves module with both single-group and multi-group analysis modes) — https://github.com/databio2022/GraphBio
- **Docker** (containerization for reproducible deployment of GraphBio application with pre-installed dependencies)

## Evaluation signals

- All unique group identifiers from the input CSV are represented as distinct curves or facets in the output figure.
- Cumulative probability values for each group curve range from 0 to 1 across the distribution axis.
- Overlaid or faceted layout allows visual distinction between group curves (e.g., different colors, line styles, or separate panels).
- Exported PNG or PDF file is generated without errors and renders legibly on standard displays.
- Curve shapes and percentile positions differ visually between groups in a manner consistent with the underlying distribution data.

## Limitations

- Requires explicit group column in input CSV; missing or inconsistent group labels will cause parsing failures or undefined group assignment.
- Performance may degrade with very large numbers of groups (>10–20) due to visual clutter in overlaid displays; faceting is recommended for high group counts.
- Single-file input format (CSV) does not support hierarchical or nested group structures; only flat group partitioning is supported.
- Curve smoothness and resolution depend on the granularity of the input distribution values; sparse or coarse-grained data may produce stepped or jagged curves.

## Evidence

- [other] GraphBio implements cumulative distribution curves using two separate demo CSV files: cdc_example.csv for single-group analysis and cdc-mutiple-group.csv for multiple-group analysis.: "GraphBio implements cumulative distribution curves using two separate demo CSV files: cdc_example.csv for single-group analysis and cdc-mutiple-group.csv for multiple-group analysis."
- [other] Parse the multi-group data structure and compute cumulative distributions stratified by group, then generate cumulative distribution curve figures for the multiple-group dataset, displaying curves overlaid or faceted by group.: "Parse the multi-group data structure and compute cumulative distributions stratified by group. 6. Generate the cumulative distribution curve figures for the multiple-group dataset, displaying curves"
- [other] Export both single-group and multiple-group CDC figures as PNG or PDF outputs.: "Export both single-group and multiple-group CDC figures as PNG or PDF outputs."
- [readme] GraphBio---A modular and scalable R Shiny dashboard providing visualization analysis capabilities for omics data.: "GraphBio---A modular and scalable R Shiny dashboard"
- [readme] cdc_example.csv and cdc-mutiple-group.csv are demo files provided for Cumulative Distribution Curves functionality.: "cdc_example.csv and cdc-mutiple-group.csv for Cumulative Distribution Curves"
