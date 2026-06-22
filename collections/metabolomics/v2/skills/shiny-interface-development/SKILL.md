---
name: shiny-interface-development
description: Use when you have a complete R package (e.g., pmartR) implementing a multi-step omics analysis pipeline (upload → transform → filter → normalize → test → visualize), and you want to make those steps accessible to scientists who lack R expertise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3168
  tools:
  - pmartR
  - Shiny
  - R
  - renv
  - Docker
  - shinytest2
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pmart_cq
    doi: 10.1021/acs.jproteome.3c00512
    title: PMart
  dedup_kept_from: coll_pmart_cq
schema_version: 0.2.0
---

# shiny-interface-development

## Summary

Build a Shiny GUI wrapper around an R analytical package to expose complex omics analysis workflows—data upload, transformation, filtering, normalization, statistical testing, and visualization—without requiring end users to know R or the underlying package API. This skill applies when you have a mature R package with rich functionality that would benefit from point-and-click accessibility for domain scientists.

## When to use

You have a complete R package (e.g., pmartR) implementing a multi-step omics analysis pipeline (upload → transform → filter → normalize → test → visualize), and you want to make those steps accessible to scientists who lack R expertise. Apply this skill when the analysis workflow is iterative (users need to explore data, adjust parameters, and re-run tests), when users must select among multiple statistical methods (ANOVA vs. G-test, FDR vs. no correction), and when interactive exploratory data analysis (PCA, heatmaps, missing-value plots) is critical to decision-making.

## When NOT to use

- The underlying R package is immature, poorly documented, or lacks validation—a Shiny wrapper will amplify usability problems and give a false impression of robustness.
- Users have deep R expertise and need fine-grained control over package internals; forcing them through a GUI constrains reproducibility and scripting.
- The analysis is one-off and non-iterative; a command-line interface or script is faster and more transparent than building a GUI.
- Real-time collaboration or large-scale batch processing is required; Shiny is optimized for single-session interactivity, not concurrent multi-user workflows or high-throughput submission.

## Inputs

- Expression data matrix (raw or log-transformed abundance measurements)
- Sample information table (grouping variables, covariates, pairing structure)
- Biomolecule metadata (e.g., gene/protein identifiers, annotation)
- User parameter selections (transformation method, filtering thresholds, statistical test, p-value adjustment method)

## Outputs

- Transformed and filtered omics data object
- Exploratory analysis visualizations (PCA plots, heatmaps, missing-value plots, correlation matrices)
- Normalized data with selected centering method
- Protein-level quantification (rolled-up from peptides where applicable)
- Statistical test results with raw and adjusted p-values, biomarker rankings
- Interactive UI elements (plots, tables, downloadable results)

## How to apply

Structure the Shiny application into modular tabs that mirror the natural omics analysis workflow: data upload (expression, metadata, sample information), data transformation (log2 conversion), group assignment (factors, covariates, pairing), exploratory analysis (PCA, correlation heatmaps, missing-value visualization), filtering (by non-missing values and coefficient of variation thresholds), normalization (with automated SPANS procedure for proteomics), protein quantification (peptide roll-up), and statistical testing (ANOVA, G-test, combined analyses with p-value adjustment options like FDR). Organize Shiny code into folders (observers, reactive_variables, UI_elements, tabs_UI) to maintain modularity as complexity grows. Use reactive variables to track user selections (e.g., filtering thresholds, statistical method, p-value adjustment strategy) and pass them to the backend R package functions. Render output dynamically (renderUI, renderPlot, renderTable) so that downstream UI elements (e.g., statistical test parameters) respond to upstream choices (e.g., group assignments). Validate intermediate outputs (adjusted p-values match expected distributions, filtered biomolecule counts are reasonable) before displaying results. Deploy via Docker with renv-managed dependencies to ensure reproducibility across environments.

## Related tools

- **pmartR** (Backend R package implementing the core omics analysis methods (ANOVA, G-test, filtering, normalization, peptide roll-up); called by Shiny server functions) — https://github.com/pmartR/
- **Shiny** (GUI framework for building reactive, interactive web interface; handles UI rendering, event observers, and reactive variable propagation) — https://shiny.rstudio.com/
- **R** (Programming language in which pmartR and Shiny are written; runs all statistical computations and data transformations) — https://www.r-project.org/
- **renv** (Dependency management tool; locks package versions in renv.lock and ensures reproducible environment across local, Docker, and cloud deployments) — https://rstudio.github.io/renv/articles/renv.html
- **Docker** (Containerization; Dockerfile-base installs system libraries and R packages; top Dockerfile copies app code; enables consistent deployment and testing) — github.com/pmartR/PMart_ShinyApp
- **shinytest2** (Testing framework for Shiny apps; validates UI behavior, parameter passing, and output correctness before release)

## Examples

```
shiny::runApp() # After installing dependencies with renv::restore() and setting Sys.setenv("MAP_CONFIG" = "<path-to-yml-file>")
```

## Evaluation signals

- All workflow steps are accessible from the UI without requiring R code: user can upload data → assign groups → filter → normalize → run statistical test → visualize results by clicking buttons and selecting dropdowns.
- Reactive dependencies are correct: changing an upstream parameter (e.g., filter threshold or statistical method) immediately triggers recomputation and updates all dependent downstream UI elements and outputs.
- P-value adjustment logic is validated: adjusted p-values computed by FDR correction match the expected distribution across multiple test scenarios and are correctly displayed alongside raw p-values.
- Exploratory visualizations (PCA, heatmaps, missing-value plots) reflect the filtered and normalized data, and their content updates when filtering or normalization parameters change.
- Docker container builds without errors, installs all dependencies from renv.lock, and the Shiny app launches and responds to user input in the containerized environment; shinytest2 tests pass for critical workflows (data upload → filtering → statistical testing).

## Limitations

- The Shiny interface is designed for single-session interactivity; it does not support real-time multi-user collaboration or batch processing of hundreds of datasets.
- Complex statistical method selection (e.g., choosing between ANOVA and G-test, or between FDR and other p-value adjustments) relies on the UI adequately explaining the assumptions and trade-offs; poor UI design can lead to incorrect method selection by non-statistical users.
- Performance may degrade with very large omics datasets (e.g., >100,000 biomolecules or >10,000 samples) due to in-memory computation and rendering limitations of Shiny; such datasets may require cloud scaling or batch-mode processing.
- The quality and correctness of results depends entirely on the underlying pmartR package; Shiny does not validate mathematical correctness, only UI/UX correctness.
- Deployment requires knowledge of Docker, renv, environment variables (MAP_CONFIG, SHINY_DEBUG), and optional Python virtual environments for certain modules (e.g., Kaleido for image export); this complexity may limit accessibility for small teams.

## Evidence

- [readme] The aim is for the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself.: "The aim is for the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself."
- [readme] Data upload. Upload expression data, sample information, and biomolecule metadata. ... Data transformation (raw to log2). ... Group assignment (main effects, covariates, pairing structure). ... Statistical analysis. ANOVA, G-test, and combined analyses to determine biomarkers.: "Data upload. Upload expression data, sample information, and biomolecule metadata... Data transformation (raw to log2)... Group assignment... Statistical analysis. ANOVA, G-test, and combined"
- [readme] Within each folder are the corresponding elements for that particular tab. ... observers, reactive_variables, UI_elements (reactive elements usually constructed with renderUI), tabs_UI (Higher level, usually non-reactive elements).: "Within each folder are the corresponding elements for that particular tab... observers, reactive_variables, UI_elements, tabs_UI"
- [readme] We use renv to track dependencies... The renv.lock file contains a list of dependencies and various details about them.: "We use renv to track dependencies. The renv.lock file contains a list of dependencies and various details about them."
- [other] Shiny GUI implementation of the pmartR R package... [that enables] omics data analysis without requiring R familiarity: "A Shiny GUI implementation of pmartR enables omics data analysis without requiring R familiarity"
- [readme] To run the MAP tests from the local project but pulling project and midpoint files from minio, set `Sys.setenv("MAP_SHINYTEST" = 1)` before running `shinytest2::test_app()`: "To run the MAP tests from the local project but pulling project and midpoint files from minio, set `Sys.setenv("MAP_SHINYTEST" = 1)` before running `shinytest2::test_app()`"
