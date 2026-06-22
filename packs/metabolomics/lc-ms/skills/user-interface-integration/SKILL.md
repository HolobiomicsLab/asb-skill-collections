---
name: user-interface-integration
description: Use when when you have a multi-step computational workflow (e.g., peak detection, filtering, manual review) implemented in R and need to expose it to end-users who lack R expertise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - metScribeR
  - Shiny
  - mzR
  - chromatographR
  - roxygen2
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jproteome.5c00548
  title: metScribeR
evidence_spans:
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.5c00548
  all_source_dois:
  - 10.1021/acs.jproteome.5c00548
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# user-interface-integration

## Summary

Exporting a wrapped Shiny application function from an R package to provide an interactive graphical interface for an automated computational workflow. This skill bridges backend data-processing logic with user-accessible UI controls, enabling non-programmers to execute complex analyses through interactive forms, visualizations, and parameter tuning.

## When to use

When you have a multi-step computational workflow (e.g., peak detection, filtering, manual review) implemented in R and need to expose it to end-users who lack R expertise. Specifically, when the workflow involves iterative parameter refinement (noise threshold, m/z tolerance, RT tolerance), visual inspection of intermediate results (peak boundaries, chromatograms, boxplots), and manual decision-making (peak quality assessment) that benefit from interactive feedback rather than scripted batch processing.

## When NOT to use

- Workflow requires only programmatic, non-interactive execution with fixed parameters — use direct R function calls instead of Shiny wrapping.
- Input data do not fit the metScribeR schema (e.g., only MS2 spectra available, or missing mzML files) — MS2 data is not used or required for library construction in metScribeR.
- User has sufficient R expertise and prefers scripting; Shiny UI overhead outweighs benefit of interactive parameter tuning.

## Inputs

- standards_df.csv (or .tsv) with required columns: common_name, monoisotopic_mass, pos_mode_mzML_file_path, neg_mode_mzML_file_path, optional inchiKey and additional_identifiers
- adduct_df.csv (or .tsv) with required columns: adduct, change_from_neutral, mode (POS or NEG)
- mzML files corresponding to LC-MS runs in positive and negative ESI modes
- Storage object (RDS) from a previous metScribeR session (optional, for resuming analysis)

## Outputs

- exported_metScribeR_library.csv (final library with 'good' adducts and identification-relevant metrics)
- exported_metScribeR_library_with_metrics.csv (all peaks including 'bad' and 'multimodal/indeterminate' with peak metrics)
- exported_metScribeR_MoNA_MSMS.csv (MS/MS spectral data retrieved from MassBank of North America)
- storage_object.RDS (serialized state of Shiny session for resuming analysis)
- storage_object_initial.RDS (state after initial computation, for restarting without re-computation)
- Figures/ directory containing .png images of manually reviewed peaks

## How to apply

Define an exported R function (e.g., `runMetScribeRShinyApp()`) that wraps Shiny's `shinyApp()` or `runApp()` calls to initialize the interactive UI session. Use roxygen2 directives or explicit NAMESPACE entries to export the function so users can invoke it directly via `package::function()`. Structure the Shiny app with multiple tabbed or sequential interfaces corresponding to workflow stages (e.g., 'Upload & Configure', 'Find Peaks', 'Review Results', 'View/Export Library'). Wire reactive elements (drop-down menus, sliders for noise/tolerance thresholds, toggle switches for filtering options) to backend R functions that process mzML files, compute peaks, and generate diagnostic plots. Implement state persistence (save/load via RDS storage objects) to allow users to resume long-running computations without restarting. Document the launch function, required input file formats (standards_df.csv with columns: common_name, monoisotopic_mass, pos_mode_mzML_file_path, neg_mode_mzML_file_path; adduct_df.csv with columns: adduct, change_from_neutral, mode), and expected output directory structure in the package README with code examples.

## Related tools

- **Shiny** (Framework for building the interactive web-based user interface that wraps the metabolite library workflow) — https://shiny.rstudio.com/
- **metScribeR** (R package containing the automated workflow logic (peak detection, filtering, library building) and exporting the Shiny launcher function) — https://github.com/ncats/metScribeR
- **mzR** (R package for reading mzML mass spectrometry data files)
- **chromatographR** (R package (dependency) providing chromatographic data handling utilities) — https://github.com/ethanbass/chromatographR
- **roxygen2** (R documentation and NAMESPACE management tool to export the Shiny launcher function)

## Examples

```
library(metScribeR)
setwd('C:/Users/user123/Downloads/metScribeR_extdata_folder')
runMetScribeRShinyApp()
```

## Evaluation signals

- Function is callable directly from the package namespace (e.g., `metScribeR::runMetScribeRShinyApp()` succeeds without error after installation).
- Shiny app launches an interactive browser window with expected tabs/panels (Upload & Configure, Find Peaks, Review Results, View/Export Library) and responds to user inputs (file upload, parameter sliders, button clicks).
- Noise threshold slider and m/z/RT tolerance inputs correctly filter peaks and update diagnostic plots (chromatograms, density plots, boxplots) in real time.
- Manual review workflow (drop-down menu, arrow buttons, Good/Bad/Indeterminate classification buttons) successfully records user decisions and persists them when Export Library or Save Session buttons are clicked.
- Output files (exported_metScribeR_library.csv, storage_object.RDS) are generated in the specified output directory with correct schema and non-empty rows for 'good' peaks; RDS file can be reloaded to resume analysis.
- Storage object contains deterministic state that reproduces identical library results when reloaded, confirming session state was correctly serialized.

## Limitations

- For large submissions (>10,000 mzML files), initial computation can exceed 30 minutes, requiring patient users or background job scheduling.
- MassBank of North America MS/MS lookup is server-dependent and can be slow; availability/speed not guaranteed.
- MS2 data is not used or required for library construction, limiting spectral annotation to MS1 + RT + MoNA external lookup; users seeking full de novo MS2 identification cannot rely on internal spectra.
- Manual review step (step 7 in README workflow) is mandatory and non-parallelizable; no batch-mode quality assessment for large peak sets.
- Inchikey lookup for MoNA requires pre-population in standards_df.csv; if missing, no MSMS retrieval occurs for that standard.

## Evidence

- [readme] Exported function and Shiny launch mechanism: "Launch the metScribeR Shiny application in R with metScribeR::runMetScribeRShinyApp()"
- [readme] Workflow stages and interactive parameter tuning: "Use the noise plot figure on the right side of the screen to find and input the level of the background noise, below which all MS observations are not included in processing. Finally, choose an m/z"
- [readme] Manual review and visual inspection in UI: "Toggle between peaks with the drop-down menu and arrow buttons. In each figure, the blue and red vertical lines indicate the beginning and ending boundaries of the peak. The dashed vertical line"
- [readme] State persistence and session recovery: "Alternatively, in lieu of starting a new experiment, a saved metScribeR storage object can be loaded to resume progress on a previously started analysis."
- [readme] Required input file schema: "Create standards_df.csv (or .tsv) with the following required, identically spelled column names: common_name, with the name of each standard; monoisotopic_mass, the neutral mass of each standard;"
- [readme] Scope: MS1 and RT data only: "metScribeR focuses library building on MS1 & RT data, and MS2 data is not used or required for library construction"
- [readme] Interactive filtering and visualization workflow: "Use the drop-down menu to tab between a subset of 50 peaks found in your data, and toggle the density filter and data smoothing to assess the best settings for your data."
- [readme] Output file generation and export: "The exported_metScribeR_library.csv file is the primary library including all 'good' adducts and information relevant for making identifications with your new library."
