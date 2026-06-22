---
name: web-application-server-logic-mapping
description: Use when you are wrapping an existing R package or analytical library in a web interface and need to connect UI form inputs (file uploads, parameter selections, configuration checkboxes) to the backend computation functions and render their outputs reactively.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3070
  tools:
  - R
  - Shiny
  - R package Amanida
  - R package webchem
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

# web-application-server-logic-mapping

## Summary

Map reactive handlers in web frameworks (e.g., Shiny) to underlying computational functions, ensuring data flows from user interface inputs through backend computation to reactive output displays. This skill bridges the gap between interactive UI controls and the statistical or analytical R packages they wrap.

## When to use

You are wrapping an existing R package or analytical library in a web interface and need to connect UI form inputs (file uploads, parameter selections, configuration checkboxes) to the backend computation functions and render their outputs reactively. Specifically when you have discrete input controls that should trigger and parameterize a computation, and results must update without page reloads.

## When NOT to use

- The analytical library is stateless and does not accept user-configurable parameters—no mapping layer needed.
- You do not have access to the underlying package's function signatures or documentation.
- The UI inputs and outputs are static (no reactivity required); use static rendering instead.

## Inputs

- R package source code (target analytical library)
- Shiny UI definition files (input control specifications)
- User-supplied form inputs (file uploads, numeric/categorical parameters)
- Package function documentation (signatures, parameter names, expected types)

## Outputs

- Shiny server.R file with reactive handlers
- Mapped input–function–output chains
- Rendered output components (HTML tables, plots, downloadable results)
- Reactive expressions linking UI to backend computation

## How to apply

Examine the target R package's function signatures and parameters to identify which inputs are exposed in the UI. For each UI input control (e.g., file upload, dropdown, slider), define a Shiny reactive handler that extracts the user-supplied value and passes it to the corresponding package function. Map the package function's return values to Shiny reactive outputs (typically render* functions like renderTable or renderPlot). Ensure the data flow chain is explicit: UI input → reactive expression → package function call → reactive output → rendered display (table, plot, or downloadable file). Validate that parameter types and ranges match the package's expectations (e.g., numeric thresholds, file formats for metabolomic data).

## Related tools

- **Shiny** (Web framework for reactive server-side handlers and reactive output rendering)
- **R package Amanida** (Backend analytical library exposing meta-analysis functions wrapped by server logic)
- **R package webchem** (Companion package used by Amanida for compound name harmonization)

## Evaluation signals

- Each UI input control has a corresponding reactive handler that extracts and validates user input.
- Each package function call within a handler receives parameters with correct types and within expected ranges (e.g., p-value columns named correctly, fold-change as numeric).
- Reactive outputs update immediately when UI inputs change, with no stale data persisted.
- Package function return values (data frames, plots, results objects) are correctly mapped to Shiny render* functions (renderTable, renderPlot, downloadHandler).
- Data flow from input → handler → function → output produces results consistent with running the package function directly in R.

## Limitations

- The skill assumes the underlying R package has well-defined, documented function signatures; undocumented or variable parameter lists complicate mapping.
- Reactivity depends on Shiny's reactive graph; circular dependencies or complex interdependencies between inputs can cause infinite loops or stale outputs.
- Performance bottlenecks may arise if package functions are slow; reactivity will delay UI responsiveness, and large result sets may not render efficiently in HTML tables.

## Evidence

- [other] Core method: reactive handler mapping: "Reconstruct the server logic by mapping Shiny reactive handlers to Amanida's meta-analysis functions, ensuring data flows from UI inputs through Amanida computation to reactive output displays."
- [other] Output rendering requirement: "Implement output rendering components (tables, plots, downloadable results) that display Amanida's meta-analysis results within the Shiny dashboard."
- [readme] Dual-package workflow rationale: "Easy-Amanida is a new tool that combines two R packages, `amanida` and `webchem`, to enable meta-analysis of aggregate statistical data, like p-value and fold-change, while ensuring the compounds"
- [readme] Interactive web framework context: "The Easy-Amanida app is implemented in Shiny, an R package add-on for interactive web apps, and provides a workflow to optimize naming combination."
