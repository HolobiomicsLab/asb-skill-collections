---
name: metabolomic-meta-analysis-workflow-design
description: Use when you have multiple metabolomic studies with aggregate summary statistics (p-values, fold-change estimates) and need to perform meta-analysis while harmonizing compound nomenclature across datasets. Use this skill when the underlying R package (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3172
  tools:
  - R
  - Shiny
  - R package Amanida
  - R package webchem
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1002/jrsm.1713
  title: Easy-Amanida
evidence_spans:
- R package Amanida
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_easy_amanida_cq
    doi: 10.1002/jrsm.1713
    title: Easy-Amanida
  dedup_kept_from: coll_easy_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/jrsm.1713
  all_source_dois:
  - 10.1002/jrsm.1713
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-meta-analysis-workflow-design

## Summary

Design and implement a Shiny-based web interface that wraps R metabolomic packages to enable harmonized meta-analysis of aggregate statistical data (p-values, fold-change) across multiple studies while ensuring compound name standardization. This skill bridges computational metabolomics with interactive web deployment to lower barriers to complex meta-analytic workflows.

## When to use

You have multiple metabolomic studies with aggregate summary statistics (p-values, fold-change estimates) and need to perform meta-analysis while harmonizing compound nomenclature across datasets. Use this skill when the underlying R package (e.g., Amanida) exists but lacks a user-friendly interface, or when you need to expose a multi-step workflow (data upload, parameter tuning, result visualization) to non-programmatic users via a web browser.

## When NOT to use

- Raw mass spectrometry data (mzML, NetCDF) requiring spectral processing or feature extraction—this skill assumes pre-computed aggregate statistics as input.
- Single-study metabolomic analysis without multi-study aggregation—meta-analysis infrastructure is unnecessary.
- Scenarios where compound harmonization is not required or compounds are already canonically named.

## Inputs

- Metabolomic aggregate statistical data files (p-values, fold-change per compound)
- Compound name or identifier lists (subject to harmonization)
- Meta-analysis parameter specifications (statistical thresholds, study weights)
- Installed R package environment (Amanida, webchem, Shiny)

## Outputs

- Meta-analysis summary tables (harmonized compound identifiers, combined p-values, effect sizes)
- Visualization plots (forest plots, volcano plots, compound rankings)
- Downloadable result files (CSV, PDF reports)
- Shiny web application (local or Shiny Server deployment)

## How to apply

Begin by identifying and installing the core R metabolomic package and its dependencies (here: Amanida and webchem). Clone or inspect the source repository to understand the package's function signatures, input data structures, and output formats. Design the Shiny UI layer to expose key inputs as reactive controls—file upload widgets for metabolomic datasets, parameter sliders or text inputs for meta-analysis settings (e.g., statistical thresholds, compound matching criteria). Map Shiny reactive handlers (reactive(), observeEvent()) to the underlying package functions, ensuring data flows from UI input through computation to reactive output displays. Implement output rendering components (renderTable, renderPlot, downloadHandler) that transform package results into human-readable tables, plots, and downloadable files. Deploy locally or to Shiny Server and verify that the web interface correctly exposes the package's workflow without data loss or parameter distortion.

## Related tools

- **Shiny** (Framework for building interactive web application UI and reactivity layer wrapping metabolomic computation)
- **R package Amanida** (Core computational engine implementing meta-analysis algorithms on metabolomic summary statistics)
- **R package webchem** (Provides compound name harmonization and chemical nomenclature standardization utilities)

## Examples

```
# In R: load Shiny app from cloned repository and run locally
shiny::runApp('~/easy-amanida', port=3838)
```

## Evaluation signals

- Web interface successfully loads and renders without console errors; Shiny reactive graph is acyclic and responsive to UI input changes.
- Uploaded metabolomic datasets are parsed correctly and passed to Amanida functions without data corruption or format mismatches.
- Compound names from multiple input files are harmonized to a unified identifier space (verified by spot-checking name mappings).
- Meta-analysis results (combined p-values, effect size estimates) are computed and displayed in output tables and plots; results match standalone R package execution on the same input.
- Downloadable result files (CSV, PDF) contain all expected columns and metadata; file formats are valid and machine-readable.

## Limitations

- Easy-Amanida provides workflow optimization for compound naming but does not automatically resolve all ambiguous or novel compound identifiers—manual curation may still be required for edge cases.
- The Shiny application is resource-constrained on free deployment tiers (e.g., shinyapps.io); large meta-analyses across many studies or high-dimensional compound lists may experience latency or timeout.
- No changelog or version history was documented in the repository, complicating reproducibility and tracking of methodological changes.

## Evidence

- [readme] Easy-Amanida is a web-based app, developed with Shiny, that implements the R package Amanida.: "Easy-Amanida is a web-based app, developed with Shiny, that implements the R package Amanida."
- [readme] Easy-Amanida combines two R packages, amanida and webchem, to enable meta-analysis of aggregate statistical data, like p-value and fold-change, while ensuring the compounds naming harmonization.: "Easy-Amanida is a new tool that combines two R packages, `amanida` and `webchem`, to enable meta-analysis of aggregate statistical data, like p-value and fold-change, while ensuring the compounds"
- [other] Reconstruct the server logic by mapping Shiny reactive handlers to Amanida's meta-analysis functions, ensuring data flows from UI inputs through Amanida computation to reactive output displays.: "Reconstruct the server logic by mapping Shiny reactive handlers to Amanida's meta-analysis functions, ensuring data flows from UI inputs through Amanida computation to reactive output displays."
- [other] Implement output rendering components (tables, plots, downloadable results) that display Amanida's meta-analysis results within the Shiny dashboard.: "Implement output rendering components (tables, plots, downloadable results) that display Amanida's meta-analysis results within the Shiny dashboard."
- [readme] The Easy-Amanida app is implemented in Shiny, an R package add-on for interactive web apps, and provides a workflow to optimize naming combination.: "The Easy-Amanida app is implemented in Shiny, an R package add-on for interactive web apps, and provides a workflow to optimize naming combination."
