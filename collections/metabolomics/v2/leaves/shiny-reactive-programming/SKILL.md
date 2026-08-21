---
name: shiny-reactive-programming
description: Use when you have an R package with analytical functions (e.g., meta-analysis,
  statistical modeling, visualization) and need to expose it as an interactive web
  interface where end-users can upload data, adjust parameters, and view results in
  real time without rewriting backend logic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0634
  tools:
  - Shiny
  - R
  - R package Amanida
  - webchem
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1002/jrsm.1713
  title: Easy-Amanida
evidence_spans:
- developed with Shiny
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# shiny-reactive-programming

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Build interactive web applications in R by mapping user interface inputs to reactive expressions and server-side handlers that trigger computational workflows and render outputs. This skill enables wrapping complex R analytical packages (like Amanida for meta-analysis) into responsive web dashboards where parameter changes automatically propagate through analysis pipelines.

## When to use

You have an R package with analytical functions (e.g., meta-analysis, statistical modeling, visualization) and need to expose it as an interactive web interface where end-users can upload data, adjust parameters, and view results in real time without rewriting backend logic. The trigger is: existing R package + need for point-and-click web UI + reactive data flow.

## When NOT to use

- The analytical backend is already a REST API or web service; wrap it via HTTP client libraries instead of rebuilding in Shiny.
- Real-time data streaming with sub-second latencies; Shiny's reactive model is optimized for user-driven interactions, not continuous sensor feeds.
- The analysis is a one-off batch job with no need for interactive parameter tuning; a simple R script or command-line tool is simpler and more maintainable.

## Inputs

- R package source code with analytical functions (e.g., Amanida)
- User interface specification (input controls: file uploads, parameters, selectors)
- Input data format that the underlying R package accepts (e.g., metabolomic datasets with p-values and fold-change)

## Outputs

- Interactive Shiny web application (local or server-deployed)
- Rendered output components (HTML tables, ggplot/base R plots, downloadable result files)
- Reactive expression graph linking UI inputs to package function calls to rendered outputs

## How to apply

First, decompose the analytical workflow into UI inputs (file uploads, parameter sliders, dropdown selectors) and corresponding server outputs (tables, plots, downloadable results). Second, install Shiny and structure the application with separate UI and server functions. Third, in the server logic, map Shiny reactive handlers (e.g., `reactive()`, `observeEvent()`) to the underlying R package functions, ensuring that whenever UI inputs change, dependent expressions re-run automatically. Fourth, wrap the package's output objects in Shiny render functions (e.g., `renderTable()`, `renderPlot()`, `downloadHandler()`) to display results in the browser. Finally, test locally with `shinyApp(ui, server)` or deploy to Shiny Server to verify data flows correctly from UI → R package computation → reactive output display.

## Related tools

- **Shiny** (Interactive web application framework for R; provides reactive programming primitives (reactive, observeEvent, render*) and deployment infrastructure) — https://shiny.posit.co/
- **R package Amanida** (Backend analytical package exposing meta-analysis functions (e.g., compound harmonization, p-value aggregation) invoked via Shiny server handlers)
- **webchem** (Companion R package used alongside Amanida for compound naming harmonization within the Shiny workflow)

## Examples

```
shinyApp(ui = fluidPage(fileInput('data', 'Upload metabolomic data'), actionButton('run', 'Run meta-analysis'), tableOutput('results')), server = function(input, output) { results <- reactive({ amanida::metaanalysis(input$data$datapath) }); output$results <- renderTable(results()) })
```

## Evaluation signals

- UI inputs (file upload, parameter sliders) successfully trigger server-side reactive expressions and re-computation without page reload.
- Output components (tables, plots) update automatically and display the correct result from the underlying R package function when inputs change.
- Downloaded result files contain the expected meta-analysis output (harmonized compounds, aggregated p-values, fold-changes) matching what the R package produces directly.
- No JavaScript errors in browser console; all Shiny session messages indicate successful reactive graph evaluation.
- Deployment to Shiny Server or shinyapps.io succeeds; external users can access the app and reproduce outputs locally obtained during development.

## Limitations

- Shiny's reactive model works best for latency-tolerant interactive analysis (seconds to minutes per recomputation); not suitable for real-time or streaming analytics.
- Large dataset uploads and computationally intensive R package functions may cause UI freezing; async/background job patterns require additional complexity.
- No built-in version control or changelog for the web app itself; reproducibility depends on tracking changes in the repository (as noted in the source card: 'No changelog found').
- Deployment and scaling require Shiny Server infrastructure or a paid platform like shinyapps.io; not suitable for fully offline or embedded use cases.

## Evidence

- [intro] Shiny framework for interactive web interface: "Easy-Amanida is a web-based app, developed with Shiny, that implements the R package Amanida."
- [other] Reactive mapping of UI inputs to package functions: "Reconstruct the server logic by mapping Shiny reactive handlers to Amanida's meta-analysis functions, ensuring data flows from UI inputs through Amanida computation to reactive output displays."
- [other] Output rendering and display components: "Implement output rendering components (tables, plots, downloadable results) that display Amanida's meta-analysis results within the Shiny dashboard."
- [readme] Meta-analysis workflow with compound harmonization: "Easy-Amanida is a new tool that combines two R packages, `amanida` and `webchem`, to enable meta-analysis of aggregate statistical data, like p-value and fold-change, while ensuring the compounds"
- [other] UI layer for data input and parameter configuration: "Reconstruct the user interface (UI) layer by examining the repository's UI definition files to expose input controls for uploading metabolomic datasets and configuring meta-analysis parameters."
