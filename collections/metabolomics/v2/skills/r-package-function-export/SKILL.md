---
name: r-package-function-export
description: Use when you have built a reusable workflow function (e.g., a Shiny app
  launcher, automated analysis routine) within an R package and need to make it available
  to package users.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - R
  - metScribeR
  - roxygen2
  - devtools
  - Shiny
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.5c00548
  title: metScribeR
evidence_spans:
- This package... can be launched using a function exported by this package
- can be launched using a function exported by this package
- This package provides an automated workflow for processing in-house metabolite library
  standards data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metscriber_cq
    doi: 10.1021/acs.jproteome.5c00548
    title: metScribeR
  dedup_kept_from: coll_metscriber_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.5c00548
  all_source_dois:
  - 10.1021/acs.jproteome.5c00548
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# R Package Function Export

## Summary

Export an R function from a package namespace so end users can invoke it directly without internal qualification. This skill is essential when wrapping user-facing workflows (e.g., Shiny app launchers, analysis pipelines) that must be callable via `package::function()` or `function()` after `library(package)`.

## When to use

Apply this skill when you have built a reusable workflow function (e.g., a Shiny app launcher, automated analysis routine) within an R package and need to make it available to package users. Triggers include: the function is intended as a public entry point, users should call it directly after installation, or the function orchestrates a complete analysis stage (e.g., `runMetScribeRShinyApp()` launches the metabolite library-building interface).

## When NOT to use

- The function is internal-only (helper, not a user entry point) — use roxygen2 `@keywords internal` instead.
- The workflow is a one-off analysis or script, not a reusable package — export is unnecessary.
- The function must be hidden or is under active development and not ready for user access — defer export until the API is stable.

## Inputs

- R source file containing the function definition (e.g., R/run_app.R)
- roxygen2 or NAMESPACE directives specifying export intent
- Package metadata (DESCRIPTION, NAMESPACE files)

## Outputs

- Function registered in package NAMESPACE
- Function callable as `package::function_name()` after installation
- Function callable as `function_name()` after `library(package)` attach
- roxygen2-generated documentation (.Rd file)

## How to apply

Define the function in an R file within the package source (e.g., `R/run_app.R`). Use roxygen2 directives (e.g., `#' @export`) or add the function name to the NAMESPACE file to register it in the package namespace. Ensure the function wraps or calls internal package machinery (e.g., Shiny app initialization, workflow orchestration). Document parameters and return value using roxygen2 comments (`#' @param`, `#' @return`). Verify export by rebuilding the package and confirming the function is listed in the NAMESPACE file and accessible via `::` qualification or after `library()` attach.

## Related tools

- **roxygen2** (Generates NAMESPACE entries and .Rd documentation from inline @export directives; automates export declaration when rebuilding package)
- **devtools** (Provides `load_all()`, `check()`, and `install()` functions to rebuild package, verify export, and test user-facing function accessibility)
- **Shiny** (In metScribeR context, the framework whose app-launching function is wrapped and exported; users call the exported function to initialize the interactive interface)

## Examples

```
library(metScribeR)
runMetScribeRShinyApp()
```

## Evaluation signals

- Function name appears in NAMESPACE file with `export(function_name)` directive.
- After package installation, `?function_name` returns documentation and does not throw 'object not found' error.
- Function is callable as `package::function_name()` without error.
- After `library(package)`, function is callable as `function_name()` without namespace qualification.
- Function accepts expected parameters and returns or displays the intended object (e.g., running Shiny app session, workflow result).

## Limitations

- Function must exist and be syntactically valid; export directives do not create or validate the underlying function.
- Export makes the function public; breaking changes to the function signature or behavior will affect users' code.
- roxygen2 export directives are lost if package is rebuilt without roxygen2 processing; manual NAMESPACE edits may be overwritten.
- Function dependencies (e.g., imported packages, internal helper functions) must be properly declared in DESCRIPTION and NAMESPACE; missing dependencies will cause runtime errors for users.

## Evidence

- [other] The metScribeR package exports a function that launches a Shiny app in which the automated workflow for processing metabolite library standards data is implemented and run.: "The metScribeR package exports a function that launches a Shiny app in which the automated workflow for processing metabolite library standards data is implemented and run."
- [other] Define an exported R function within the metScribeR package that wraps the Shiny app launch.: "Define an exported R function within the metScribeR package that wraps the Shiny app launch."
- [other] Ensure the function is exported in the package namespace (via NAMESPACE or roxygen2 directives) so users can call it directly from the package.: "Ensure the function is exported in the package namespace (via NAMESPACE or roxygen2 directives) so users can call it directly from the package."
- [readme] Launch the metScribeR Shiny application in R with metScribeR::runMetScribeRShinyApp(): "Launch the metScribeR Shiny application in R with metScribeR::runMetScribeRShinyApp()"
- [readme] The process is implemented in a Shiny app, which can be launched using a function exported by this package.: "The process is implemented in a Shiny app, which can be launched using a function exported by this package."
