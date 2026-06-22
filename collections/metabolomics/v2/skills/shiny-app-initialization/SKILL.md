---
name: shiny-app-initialization
description: Use when you have developed an R-based workflow (e.g., data processing, peak detection, quality review) that is complex enough to warrant interactive parameter tuning and visual feedback, and you need to distribute it to collaborators or end-users who prefer a graphical interface over scripting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0121
  tools:
  - Shiny
  - R
  - metScribeR
  - roxygen2
derived_from:
- doi: 10.1021/acs.jproteome.5c00548
  title: metScribeR
evidence_spans:
- The process is implemented in a Shiny app, which can be launched using a function exported by this package
- This package... can be launched using a function exported by this package
- can be launched using a function exported by this package
- This package provides an automated workflow for processing in-house metabolite library standards data
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
---

# shiny-app-initialization

## Summary

Export and launch an interactive Shiny web application from an R package to enable end-users to run a computational workflow through a graphical interface. This skill is essential when an automated analysis pipeline (e.g., metabolite library building) must be made accessible to non-programmers via point-and-click controls rather than command-line scripting.

## When to use

You have developed an R-based workflow (e.g., data processing, peak detection, quality review) that is complex enough to warrant interactive parameter tuning and visual feedback, and you need to distribute it to collaborators or end-users who prefer a graphical interface over scripting. The trigger is the desire to encapsulate multi-step computational logic (input upload, parameter adjustment, result review, export) into a single, self-contained web interface.

## When NOT to use

- Your workflow is purely command-line and does not benefit from interactive parameter exploration or visual feedback during execution.
- You are distributing a package to users who will only invoke the underlying functions programmatically and do not need a graphical launcher.
- The computational pipeline requires real-time streaming data or server-scale infrastructure beyond Shiny's single-R-process model.

## Inputs

- R package with Shiny modules (ui.R / server.R or shinyApp() structure)
- package NAMESPACE or roxygen2 @export directives
- optional: input data CSV/TSV files (e.g., standards_df.csv, adduct_df.csv) to be uploaded via the app UI
- optional: mzML or other raw data files referenced by input CSVs

## Outputs

- Running Shiny application session (web interface accessible in R or browser)
- Exported package function callable via library(packageName); runFunction()
- User-generated outputs from the app workflow (e.g., exported_metScribeR_library.csv, PNG peak figures, RDS storage objects)

## How to apply

Define an R function within your package that wraps Shiny's `shinyApp()` or `runApp()` functions to instantiate the interactive user interface. Register the function in your package's NAMESPACE file or use roxygen2 directives (e.g., `@export`) so users can call it directly via `package::functionName()`. The function should accept optional parameters (e.g., host, port, or data paths) and pass them to Shiny's initialization. Ensure dependencies (Shiny and any UI/server modules) are listed in the package DESCRIPTION file. At launch time, the function opens a browser window or server session in which users can upload input files (e.g., CSV standards tables, adduct definitions, mzML mass spectrometry data), adjust noise thresholds and m/z/RT tolerances via sliders or text inputs, click submit buttons to trigger backend computations, review tabular results (peaks, library entries), and export final outputs (CSV library files, PNG figures, RDS state snapshots).

## Related tools

- **Shiny** (Framework for building interactive web applications within R; provides ui and server functions to define interface elements and reactive computations triggered by user inputs.) — https://shiny.posit.co/
- **roxygen2** (R documentation and namespace management tool; @export directives register package functions for public use, including Shiny app launchers.) — https://roxygen2.r-lib.org/
- **metScribeR** (Example package demonstrating Shiny app initialization for metabolite library building workflow; exports runMetScribeRShinyApp() function.) — https://github.com/ncats/metScribeR

## Examples

```
library(metScribeR); runMetScribeRShinyApp()
```

## Evaluation signals

- Function is successfully exported from package namespace and callable without ::: operator (e.g., library(metScribeR); runMetScribeRShinyApp() works).
- Shiny app launches without errors and displays the expected UI tabs/input controls (file upload boxes, sliders, buttons) in a browser or RStudio Viewer.
- User can upload input files (CSV standards/adduct tables, mzML data), adjust parameters (noise threshold, m/z/RT tolerance), and click submit without crashing.
- App computes results and displays interactive outputs (drop-down peak selectors, plots with peak boundaries, result tables) that respond to user interactions (tab switches, toggle filters).
- App allows users to export final library CSV, PNG figures, and RDS state snapshots as described in the workflow documentation.

## Limitations

- Shiny applications run in a single R process; large submissions (e.g., 12,000 mzML files in metScribeR) can take ~30 minutes and block the R session until computation completes.
- MoNA MS/MS data collection depends on external server availability and can be slow; no built-in timeout or fallback mechanism if the server is unreachable.
- The app's state is lost if the R session is terminated unexpectedly; users must rely on saved RDS storage objects to recover partial progress.
- Input CSV files must have exact column names and correct case (e.g., 'common_name', 'monoisotopic_mass'); misspellings or case mismatches cause errors without detailed guidance.

## Evidence

- [readme] Export and launch mechanism: "The process is implemented in a Shiny app, which can be launched using a function exported by this package."
- [readme] Function registration and invocation: "Launch the metScribeR Shiny application in R with metScribeR::runMetScribeRShinyApp()"
- [readme] User interface workflow steps: "Upload the standards and adduct csv files to the appropriate input boxes and select an output directory for results. Use the noise plot figure on the right side of the screen to find and input the"
- [readme] Interactive result review and export: "Here, each peak that passed filtering must be manually reviewed for inclusion in the final library. Toggle between peaks with the drop-down menu and arrow buttons... Use the Export Library csv button"
- [readme] Computational performance and output types: "For large submissions, this computation will take some time (~30 min for 12000 mzML files)."
