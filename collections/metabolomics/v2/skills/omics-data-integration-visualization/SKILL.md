---
name: omics-data-integration-visualization
description: Use when you have completed statistical analysis of omics data (proteomics,
  metabolomics, transcriptomics, or multi-omic) and possess both abundance/expression
  measurements and computed statistical metrics (p-values, effect sizes, fold-changes).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3391
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

# omics-data-integration-visualization

## Summary

Transform omics abundance/expression measurements and their corresponding statistical results (p-values, effect sizes, fold-changes) into shareable, interactive trelliscope displays that enable exploratory analysis and communication of multi-omic findings. This skill bridges raw statistical output to publication-ready interactive visualizations.

## When to use

You have completed statistical analysis of omics data (proteomics, metabolomics, transcriptomics, or multi-omic) and possess both abundance/expression measurements and computed statistical metrics (p-values, effect sizes, fold-changes). You need to communicate results to collaborators or stakeholders in an interactive, filterable format that allows exploration of individual features (proteins, metabolites, genes) in context of their statistical significance and functional annotations.

## When NOT to use

- Input is preliminary or unfiltered raw omics data without statistical testing—apply quality control and statistical analysis first.
- Statistical results are incomplete or use inconsistent thresholds across feature groups—standardize and validate statistical outputs before visualization.
- Collaboration requires real-time dynamic recomputation or parameter tuning—consider interactive R/Python environments instead for exploratory workflows.

## Inputs

- Omics abundance or expression matrix (rows=features, columns=samples)
- Statistical results table (p-values, effect sizes, fold-changes per feature)
- Feature annotation table (protein/metabolite/gene identifiers, functional categories, pathway membership)

## Outputs

- Shareable HTML trelliscope display with embedded data and interactive controls
- Interactive panels organized by omics feature with filterable statistical metrics
- Browsable output suitable for communication with non-computational collaborators

## How to apply

Load omics abundance data and statistical results (p-values, effect sizes, fold-changes) into the MODE ShinyApp environment. Map omics features (proteins, metabolites, genes) to individual trelliscope panel rows, with statistical metrics and feature annotations as cognate variables available for filtering and sorting. Define interactive filters and sort keys on statistical thresholds (e.g., p-value cutoffs) and feature metadata. The application generates an embedded HTML trelliscope output with interactive controls, allowing users to navigate panels, sort by statistical metrics, and filter by annotation criteria without requiring computational infrastructure. This approach prioritizes reproducibility and accessibility by embedding data within the shareable output artifact.

## Related tools

- **trelliscope** (Core visualization framework that organizes omics features into interactive panels with cognate statistical metrics and filterable annotations)
- **MODE ShinyApp** (Web application wrapper that ingests omics data and statistical results, configures trelliscope display parameters, and generates shareable HTML output) — https://github.com/pmartR/MODE_ShinyApp

## Evaluation signals

- Trelliscope HTML output is generated without errors and contains embedded omics data and statistical metrics.
- Each feature (protein/metabolite/gene) is represented as an individual panel with cognate variables (p-value, effect size, fold-change) displayed and sortable.
- Interactive filters respond correctly when applied to statistical thresholds (e.g., p < 0.05) and feature annotations; filtered panels update dynamically.
- Output file is shareable and self-contained (no external data dependencies); collaborators can open and interact with panels in a standard web browser without computational setup.
- Feature sorting and filtering operations preserve data integrity and do not introduce rank or statistical artifacts in the resulting visualization.

## Limitations

- Trelliscope display interactivity is limited to client-side filtering and sorting; real-time recalculation of statistics is not supported.
- Large feature sets (>10,000 unique omics features) may result in long load times or reduced responsiveness in web browsers.
- Cognate variables must be pre-computed and provided in structured tabular format; the application does not perform statistical testing internally.
- Feature annotations and metadata must be manually curated and aligned with omics feature identifiers before ingestion.

## Evidence

- [readme] Defines application purpose and core output: "Create shareable and interactive trelliscope displays for visualizing omics data and statistics results."
- [other] Specifies the complete workflow from data ingestion through display generation: "Load omics data (abundance/expression measurements) and corresponding statistical results (p-values, effect sizes, fold-changes) into the MODE ShinyApp environment. Configure trelliscope display"
- [intro] Confirms feature-to-panel and metric-to-cognate-variable mapping: "Create shareable and interactive trelliscope displays for visualizing omics data and statistics results."
- [readme] Describes deployment and accessibility of the output: "Within our Website: Go to our application website or Using the Docker Container or Locally in RStudio: Clone the git repo, open the global.R, ui.R, or server.R file in RStudio, and click the 'Run"
