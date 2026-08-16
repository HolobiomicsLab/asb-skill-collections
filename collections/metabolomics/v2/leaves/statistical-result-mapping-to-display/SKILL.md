---
name: statistical-result-mapping-to-display
description: Use when you have omics abundance or expression measurements paired with
  corresponding statistical results (p-values, effect sizes, fold-changes) and need
  to create an interactive, exploratory display where each omics feature (protein,
  metabolite, gene) occupies its own panel and can be filtered or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0531
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MODE ShinyApp
  - trelliscope
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.4c00650
  title: MODE
evidence_spans:
- github.com__pmartR__MODE_ShinyApp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mode_cq
    doi: 10.1021/acs.jproteome.4c00650
    title: MODE
  dedup_kept_from: coll_mode_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00650
  all_source_dois:
  - 10.1021/acs.jproteome.4c00650
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# statistical-result-mapping-to-display

## Summary

Map omics statistical results (p-values, effect sizes, fold-changes) as cognate variables onto individual trelliscope display panels, enabling interactive filtering and sorting of omics features by statistical thresholds. This skill transforms tabular statistical outputs into interactive, shareable visualizations suitable for exploratory data analysis.

## When to use

You have omics abundance or expression measurements paired with corresponding statistical results (p-values, effect sizes, fold-changes) and need to create an interactive, exploratory display where each omics feature (protein, metabolite, gene) occupies its own panel and can be filtered or sorted by statistical metrics. Use this when stakeholders need to browse large feature sets interactively rather than review static summary tables.

## When NOT to use

- Statistical results are already summarized into a single ranked list (e.g., volcano plot data); use simple ranking or threshold filtering instead of panel-based exploration.
- Number of omics features is very small (< 10); static plots or tables are more appropriate than interactive panel displays.
- End users cannot access a web browser or ShinyApp instance; export to static PDF or image format instead.

## Inputs

- Omics abundance/expression measurements (feature matrix with samples as columns, omics features as rows)
- Statistical results table (p-values, effect sizes, fold-changes, feature annotations aligned to omics features)

## Outputs

- Interactive trelliscope HTML display with embedded omics data and cognate statistical variables
- Shareable display object (ready for distribution or hosting on web application)

## How to apply

Load both the omics feature abundance data and the statistical results table (containing p-values, effect sizes, fold-changes, and feature annotations) into the MODE ShinyApp environment. Map each omics feature to a trelliscope panel row and assign statistical metrics as cognate variables—these become sortable/filterable columns in the display. Define interactive filters and sort keys on the statistical thresholds (e.g., p-value cutoff, minimum fold-change magnitude) and feature annotations (e.g., protein ID, metabolite class). Generate the shareable trelliscope HTML output, which embeds both data and interactive controls, allowing end users to dynamically explore the feature space without re-running analysis code.

## Related tools

- **trelliscope** (Generates shareable, interactive small-multiple displays from omics feature panels and cognate statistical variables; provides the core visualization and interactivity engine.)
- **MODE ShinyApp** (Web application framework that orchestrates loading of omics data and statistical results, configures trelliscope display panels, defines interactive filters and sort keys, and renders the final shareable HTML output.) — https://github.com/pmartR/MODE_ShinyApp

## Evaluation signals

- Verify that each omics feature appears as a distinct panel row in the trelliscope display and is not duplicated or missing.
- Confirm that statistical metrics (p-values, effect sizes, fold-changes) are correctly mapped as cognate variables and sortable/filterable without data loss or transformation.
- Check that interactive filters (e.g., p-value < 0.05, fold-change > 1.5) produce correctly subset displays when applied.
- Validate that the generated HTML output is self-contained, loads without external dependencies, and maintains interactivity when shared or hosted.
- Spot-check a sample of feature annotations and statistical values in the display against the source data table to ensure fidelity and no data corruption.

## Limitations

- Scalability depends on browser performance; very large feature sets (> 100,000) may cause slowdowns in interactive filtering or rendering.
- Requires alignment between omics feature identifiers in the abundance matrix and the statistical results table; mismatched or missing identifiers will lead to missing panels or orphaned statistics.
- The skill assumes statistical results are pre-computed and properly formatted; it does not perform statistics internally—upstream quality control of p-values, effect sizes, and annotations is essential.
- End users must have basic familiarity with interactive filtering and sorting; no automated statistical interpretation or recommendation is provided.

## Evidence

- [other] Configure trelliscope display panels to map omics features (e.g., proteins, metabolites, genes) to individual panel rows, with statistical metrics as cognate variables.: "Configure trelliscope display panels to map omics features (e.g., proteins, metabolites, genes) to individual panel rows, with statistical metrics as cognate variables."
- [other] Define interactive filters and sort keys on statistical thresholds and feature annotations.: "Define interactive filters and sort keys on statistical thresholds and feature annotations."
- [readme] Create shareable and interactive trelliscope displays for visualizing omics data and statistics results.: "Create shareable and interactive trelliscope displays for visualizing omics data and statistics results."
- [other] Load omics data (abundance/expression measurements) and corresponding statistical results (p-values, effect sizes, fold-changes) into the MODE ShinyApp environment.: "Load omics data (abundance/expression measurements) and corresponding statistical results (p-values, effect sizes, fold-changes) into the MODE ShinyApp environment."
- [other] Generate the shareable trelliscope HTML output with embedded data and interactive controls.: "Generate the shareable trelliscope HTML output with embedded data and interactive controls."
