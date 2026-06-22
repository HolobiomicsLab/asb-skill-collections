---
name: interactive-filter-definition-trelliscope
description: Use when you have omics statistical results (p-values, effect sizes, fold-changes) mapped to individual trelliscope panel rows and need to allow end users to interactively explore subsets of features (proteins, metabolites, genes) by thresholds or annotations without re-running the visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3678
  tools:
  - trelliscope
  - MODE ShinyApp
derived_from:
- doi: 10.1021/acs.jproteome.4c00650
  title: MODE
evidence_spans:
- Create shareable and interactive trelliscope displays for visualizing omics data
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

# interactive-filter-definition-trelliscope

## Summary

Define interactive filters and sort keys on statistical thresholds and feature annotations within trelliscope displays to enable exploratory filtering of omics features by p-values, effect sizes, fold-changes, and metadata. This skill transforms static visualizations into interactive tools where users can dynamically subset and rank proteomics, metabolomics, or genomics results without regenerating the display.

## When to use

You have omics statistical results (p-values, effect sizes, fold-changes) mapped to individual trelliscope panel rows and need to allow end users to interactively explore subsets of features (proteins, metabolites, genes) by thresholds or annotations without re-running the visualization pipeline. This is essential when sharing results with collaborators who need to apply domain-specific filtering criteria (e.g., 'show only significant features with |fold-change| > 2' or 'rank by adjusted p-value').

## When NOT to use

- Input is a static summary table or report that does not require interactive subsetting.
- Statistical results lack sufficient metadata or annotation columns to support meaningful filtering criteria.
- The analysis is exploratory only and results will not be shared with collaborators who need independent filtering capability.

## Inputs

- Omics abundance or expression measurements (abundance table)
- Statistical results table (p-values, adjusted p-values, effect sizes, fold-changes)
- Feature annotations (protein names, gene identifiers, pathway assignments, mass-to-charge ratios)
- Trelliscope panel configuration (mapping features to rows, metrics to cognate variables)

## Outputs

- Interactive trelliscope HTML display with embedded filter widgets
- Shareable trelliscope object with predefined filter and sort specifications
- Filtered subsets of feature panels (dynamically rendered in browser)

## How to apply

After loading omics data and statistical results into the MODE ShinyApp environment, configure cognate variables (statistical metrics and feature annotations) on the trelliscope panel specification. Define filter keys by mapping statistical columns (p-value, adjusted p-value, effect size, fold-change) and annotation fields (protein name, pathway membership, mass) to interactive filter widgets. Assign sort keys to allow users to rank panels by these same metrics. The MODE app embeds these filter and sort specifications in the generated trelliscope HTML output, enabling users to dynamically subset and reorder panels via browser controls without recompiling the visualization. Rationale: interactive filtering reduces cognitive load during exploratory analysis by letting users focus on feature subsets matching their statistical or biological criteria in real time.

## Related tools

- **trelliscope** (Underlying visualization framework that renders panels and interactive controls; MODE configures filter and sort specifications on trelliscope displays.)
- **MODE ShinyApp** (Shiny-based wrapper that ingests omics data and statistics, configures trelliscope cognate variables, and generates shareable HTML output with embedded interactive filters and sort keys.) — https://github.com/pmartR/MODE_ShinyApp

## Evaluation signals

- Generated trelliscope HTML contains filter widget elements corresponding to mapped statistical columns and annotations (verifiable via browser inspector or HTML source).
- Users can dynamically apply filter thresholds (e.g., p < 0.05, fold-change > 2) and observe real-time panel subset changes without page reload.
- Sort order changes when users select alternate sort keys; panels re-rank by the chosen metric.
- Shared trelliscope output preserves filter and sort specifications across recipients and browsers (reproducible filtering behavior).
- No statistical recomputation or data loss occurs; filtering operates only on the display layer, with all original feature panels still accessible when filters are cleared.

## Limitations

- Interactive filters are most effective when the input statistical results table is complete and contains no missing p-values or annotation fields; sparse or incomplete metadata reduces filter utility.
- Filter performance may degrade if the trelliscope display contains very large numbers of panels (>10,000 features) due to browser rendering constraints.
- Filter definitions are fixed at display generation time; adding new statistical metrics or annotations requires regenerating the trelliscope HTML output rather than modifying filters post hoc.
- No changelog or versioning is currently tracked for filter configurations (as noted in the MODE application documentation), limiting audit trails for collaborative filtering decisions.

## Evidence

- [other] Define interactive filters and sort keys on statistical thresholds and feature annotations.: "Define interactive filters and sort keys on statistical thresholds and feature annotations."
- [other] Configuration of cognate variables on panel specification.: "Configure trelliscope display panels to map omics features (e.g., proteins, metabolites, genes) to individual panel rows, with statistical metrics as cognate variables."
- [intro] Embedding of interactive controls in shareable output.: "Create shareable and interactive trelliscope displays for visualizing omics data and statistics results."
- [readme] Application enables interactive exploration of omics data.: "Create shareable and interactive trelliscope displays for visualizing omics data and statistics results."
- [readme] How to run the MODE app locally or within a Docker container.: "Clone the git repo, open the global.R, ui.R, or server.R file in RStudio, and click the "Run App" button."
