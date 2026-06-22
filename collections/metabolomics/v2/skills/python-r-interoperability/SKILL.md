---
name: python-r-interoperability
description: Use when when a Shiny R application needs to use Python libraries that lack R equivalents or are more mature in Python (e.g., Kaleido for plot export), and users should not need to manually configure Python environments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3755
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pmartR
  - orca
  - R
  - Docker
  - reticulate
  - Kaleido
  - renv
  - Shiny
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- Remove orca in favor of Kaleido
- the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself
- '#### Docker Containers'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.3c00512
  all_source_dois:
  - 10.1021/acs.jproteome.3c00512
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Python-R interoperability

## Summary

Enable a Shiny R application to call Python dependencies and manage their lifecycle through environment configuration and virtual environment setup. This skill allows R-based omics analysis workflows to leverage Python packages (e.g., Kaleido for static image rendering) without requiring users to manage Python separately.

## When to use

When a Shiny R application needs to use Python libraries that lack R equivalents or are more mature in Python (e.g., Kaleido for plot export), and users should not need to manually configure Python environments. Specifically use this skill when replacing R-native plotting backends (orca) with superior Python alternatives that improve export robustness or performance.

## When NOT to use

- When equivalent, well-maintained R packages exist for the required functionality (e.g., use R's native plotting libraries instead of Python for simple plots).
- When deployment environment cannot support Python virtual environments or when user system policies prohibit dual language runtimes.
- When the Python dependency requires system libraries not available in the target Docker or deployment container.

## Inputs

- R Shiny application source code
- Python requirements.txt file listing dependencies (e.g., kaleido==5.x.x)
- YAML configuration file mapping python_venv path
- Omics visualization objects (e.g., ggplot2 or plotly objects to be exported)

## Outputs

- Configured Shiny application with Python backend connectivity
- Python virtual environment linked to R runtime
- Static export files in multiple formats (PNG, JPEG, SVG) rendered via Python backend
- Environment variable MAP_CONFIG set and validated

## How to apply

Create a Python virtual environment with required packages listed in requirements.txt. Configure the Shiny application to discover this environment via a YAML configuration file (e.g., minio_config.yml or .yml with `python_venv: <path>`) and set the MAP_CONFIG environment variable to point to it. In R code, use the reticulate package or equivalent Python-calling mechanism to invoke Python functions from the virtual environment. Document the Python dependency list in a requirements.txt file that mirrors the R package dependencies tracked in renv.lock, ensuring both dependency systems remain in sync. Test that Python function calls execute successfully within the Shiny reactive context and that exported outputs (e.g., PNG/JPEG/SVG files from Kaleido) match expected quality and format specifications.

## Related tools

- **reticulate** (R package enabling Python function calls and environment management from R/Shiny context)
- **Kaleido** (Python library for static image export of plots (replaces orca backend for PNG/JPEG/SVG rendering with configurable width, height, scale))
- **renv** (R dependency management system tracking R package versions in renv.lock; used in parallel with Python requirements.txt) — https://rstudio.github.io/renv/articles/renv.html
- **Docker** (Container platform enabling reproducible setup of both R and Python environments; Dockerfile-base installs system libraries and Python dependencies) — https://github.com/pmartR/PMart_ShinyApp
- **Shiny** (R web framework hosting the interactive omics application that calls Python functions for plot export) — https://github.com/pmartR/PMart_ShinyApp

## Examples

```
Sys.setenv('MAP_CONFIG' = '/path/to/config.yml'); renv::restore(); shiny::runApp()
```

## Evaluation signals

- MAP_CONFIG environment variable is set and points to a valid YAML file containing `python_venv: <path>` entry.
- Python virtual environment at the specified path contains all packages from requirements.txt (verified via `pip list` or venv introspection).
- Shiny application starts without Python import errors and reactive functions invoking Python code execute without exception.
- Plot export functions generate PNG, JPEG, and SVG files with correct dimensions matching configured width and height parameters; visual inspection confirms plots render correctly and are not corrupted.
- Docker build completes successfully with Kaleido installed as a Python dependency and orca references removed from Dockerfile-base.

## Limitations

- Virtual environment path must be absolute; relative paths may fail across different user systems or container contexts.
- Python version compatibility must be maintained between requirements.txt and the R reticulate package's Python expectations; mismatches can cause runtime crashes.
- Docker image build complexity increases; base container must install Python and system libraries (e.g., libpython-dev) before Kaleido can be installed, extending build time and image size.
- Users running the app locally must manually create and activate a Python virtual environment; this adds a setup step beyond standard R package installation via renv::restore().
- Export performance depends on Kaleido's rendering speed; very large or complex plots may incur longer export times compared to lightweight bitmap backends.

## Evidence

- [readme] You will also need a Python virtual environment with the packages from requirements.txt installed. Then, add a .yml file with `python_venv: <path-to-your-venv>` in it. Finally, set the MAP_CONFIG environment variable to point to that yml file.: "You will also need a Python virtual environment with the packages from requirements.txt installed. Then, add a .yml file with `python_venv: <path-to-your-venv>` in it. Finally, set the MAP_CONFIG"
- [discussion] Remove orca in favor of Kaleido: "Remove orca in favor of Kaleido"
- [other] Modify the Shiny application R code to configure Kaleido (instead of orca) as the plotting backend with width, height, and scale parameters for export functions.: "Modify the Shiny application R code to configure Kaleido (instead of orca) as the plotting backend with width, height, and scale parameters for export functions."
- [readme] Some in-development packages are not being tracked in renv.lock (to reduce Docker image build times). These can be seen in the `install commonly updated packages` section of Dockerfile-base.: "Some in-development packages are not being tracked in renv.lock (to reduce Docker image build times). These can be seen in the `install commonly updated packages` section of Dockerfile-base."
- [readme] We use renv to manage the details about dependencies, but try keep track of them manually in DESCRIPTION as well.: "We use renv to manage the details about dependencies, but try keep track of them manually in DESCRIPTION as well."
