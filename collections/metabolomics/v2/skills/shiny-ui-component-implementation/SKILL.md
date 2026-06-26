---
name: shiny-ui-component-implementation
description: Use when you have an existing R package with statistical or data-processing
  functions and need to expose its functionality through an interactive web interface
  where end users (non-R programmers) can upload datasets, configure analysis parameters
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0091
  tools:
  - Shiny
  - R
  - R package Amanida
  - R package webchem
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

# shiny-ui-component-implementation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct interactive web application user interfaces in Shiny by mapping R package functions to reactive input controls, data upload mechanisms, and parameter configuration fields. This skill bridges statistical R packages and web-based interactivity by exposing computation parameters through dashboard UI components.

## When to use

You have an existing R package with statistical or data-processing functions and need to expose its functionality through an interactive web interface where end users (non-R programmers) can upload datasets, configure analysis parameters (e.g., meta-analysis settings, compound naming options), and download results without writing code.

## When NOT to use

- The R package does not have a clear, documented public API or function interface — UI implementation requires reverse-engineering or undocumented behavior.
- The analysis requires real-time streaming data or continuous updates; Shiny is reactive but not designed for high-frequency streaming pipelines.
- End users are expected to be R programmers — a wrapper adds unnecessary abstraction; direct R package use is more efficient.

## Inputs

- R package source code with documented function signatures and parameters
- User-uploaded metabolomic or statistical datasets (CSV, TSV, or proprietary formats)
- Analysis configuration parameters specified through UI controls (fold-change thresholds, p-value cutoffs, naming harmonization options)

## Outputs

- Interactive Shiny web application dashboard
- Rendered result tables and visualizations within the dashboard
- Downloadable result files (CSV, plots, summary reports) generated from R package output

## How to apply

Begin by examining the target R package's function signatures and parameter requirements. Design UI input controls (file upload widgets, text fields, dropdown menus, checkboxes) that correspond to each function parameter. Map these UI inputs to Shiny reactive handlers that capture user selections and pass them to the underlying R package functions. Implement output rendering components (tables, plots, downloadable files) that receive results from reactive expressions, ensuring the data flow path is: UI input → reactive capture → R function call → reactive output display. Deploy the Shiny application locally (via `shinyApp()`) or to a Shiny Server instance to verify interactivity and correct data binding.

## Related tools

- **Shiny** (Framework for building interactive reactive web applications that expose R package functions through UI controls and real-time output rendering) — https://shiny.rstudio.com
- **R package Amanida** (Underlying statistical package providing meta-analysis computation functions that are wrapped and exposed via the Shiny UI)
- **R package webchem** (Companion R package used in concert with Amanida for compound naming harmonization within the Easy-Amanida workflow)

## Examples

```
# In R console, after cloning mariallr/easy-amanida:
library(shiny); runApp('/path/to/easy-amanida')
# Then upload a CSV with p-values and fold-changes, configure meta-analysis parameters, and view harmonized results in the dashboard.
```

## Evaluation signals

- UI input controls correctly map to R package function parameters with appropriate data types (numeric, character, logical, file paths).
- Reactive expressions properly capture and transmit user inputs to R package function calls without type errors or missing parameter validation.
- Output rendering (tables, plots, file downloads) displays results that match the expected output schema from direct R package invocation.
- The application runs without errors when deployed locally via `shinyApp()` and accepts realistic user inputs (e.g., metabolomic datasets with metadata).
- Downloadable results files are correctly formatted and contain the computed meta-analysis results from Amanida with harmonized compound names from webchem.

## Limitations

- Compound naming harmonization relies on the webchem package; if external chemical database lookups fail or are incomplete, UI users will not see corrected identifiers.
- Shiny applications are single-threaded by default; large metabolomic datasets or computationally intensive meta-analyses may cause UI unresponsiveness or timeout.
- No version control or changelog tracking is mentioned in the repository, making it difficult for users to identify which features or bug fixes are available in deployed instances.

## Evidence

- [readme] Easy-Amanida is a web-based app, developed with Shiny, that implements the R package Amanida.: "Easy-Amanida is a web-based app, developed with Shiny, that implements the R package Amanida."
- [readme] Easy-Amanida combines two R packages, amanida and webchem, to enable meta-analysis of aggregate statistical data, like p-value and fold-change, while ensuring the compounds naming harmonization.: "combines two R packages, `amanida` and `webchem`, to enable meta-analysis of aggregate statistical data, like p-value and fold-change, while ensuring the compounds naming harmonization."
- [other] Reconstruct the user interface (UI) layer by examining the repository's UI definition files to expose input controls for uploading metabolomic datasets and configuring meta-analysis parameters.: "Reconstruct the user interface (UI) layer by examining the repository's UI definition files to expose input controls for uploading metabolomic datasets and configuring meta-analysis parameters."
- [other] Reconstruct the server logic by mapping Shiny reactive handlers to Amanida's meta-analysis functions, ensuring data flows from UI inputs through Amanida computation to reactive output displays.: "Reconstruct the server logic by mapping Shiny reactive handlers to Amanida's meta-analysis functions, ensuring data flows from UI inputs through Amanida computation to reactive output displays."
- [other] Implement output rendering components (tables, plots, downloadable results) that display Amanida's meta-analysis results within the Shiny dashboard.: "Implement output rendering components (tables, plots, downloadable results) that display Amanida's meta-analysis results within the Shiny dashboard."
