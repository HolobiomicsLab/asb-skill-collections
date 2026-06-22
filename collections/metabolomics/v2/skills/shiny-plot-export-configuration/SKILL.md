---
name: shiny-plot-export-configuration
description: Use when when building or maintaining a Shiny GUI for omics data analysis that must support interactive visualization download in multiple raster and vector formats, and when the current plot export backend (orca) is deprecated, unmaintained, or incompatible with your deployment environment (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pmartR
  - orca
  - Shiny
  - R
  - Docker
  - Kaleido
  - plotly
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# shiny-plot-export-configuration

## Summary

Configure and deploy a Shiny application backend for multi-format static image export (PNG, JPEG, SVG) of omics visualizations using Kaleido instead of orca. This skill enables end-users to download publication-ready plots with customizable dimensions and scaling parameters without requiring R or command-line expertise.

## When to use

When building or maintaining a Shiny GUI for omics data analysis that must support interactive visualization download in multiple raster and vector formats, and when the current plot export backend (orca) is deprecated, unmaintained, or incompatible with your deployment environment (e.g., Docker containers, cloud platforms). Specifically triggered when users report export failures or when you need to reduce Docker image build time by switching to a lighter-weight Python-based plotting backend.

## When NOT to use

- Input plots are already static PNG/JPEG/SVG files; export configuration is only needed for reactive, dynamically generated plots in Shiny.
- Users require interactive PDF export with embedded JavaScript; Kaleido produces static PDFs and does not support interactive vector features.
- The application runs in an environment where Python is unavailable or where pip/conda package installation is blocked; Kaleido requires Python runtime.

## Inputs

- Shiny application R code (server.R, ui.R, or modular observer/UI files)
- Dockerfile and Dockerfile-base (base container definition)
- Python requirements.txt (dependency specification)
- MAP_CONFIG yml file (Python virtual environment path configuration)
- plotly objects or ggplot2 objects rendered in Shiny (reactive plot outputs)

## Outputs

- Updated Dockerfile with Kaleido Python dependency (orca removed)
- Modified Shiny R code with Kaleido backend configuration and export parameters
- PNG export files (raster, configurable width/height/scale)
- JPEG export files (raster with quality tuning)
- SVG export files (vector format)
- Docker container image with Kaleido runtime available

## How to apply

Replace orca with Kaleido by: (1) updating the Dockerfile to remove orca system installation and add Kaleido as a Python dependency in requirements.txt; (2) modifying Shiny R code to configure Kaleido (instead of orca) as the plotting backend via the plotly/kaleido R bindings, setting width, height, and scale parameters for each export format (PNG typically 800–1200 px width, JPEG with quality 90–95%, SVG for vector output); (3) ensuring a Python virtual environment with kaleido installed is available and referenced in the application configuration (via MAP_CONFIG yml file with python_venv path); (4) testing all three export formats (PNG, JPEG, SVG) from representative omics plots (e.g., PCA, heatmaps, scatter plots) within the Shiny interface to confirm correct rendering, applied dimensions, and file integrity. Rationale: Kaleido is a lightweight, actively maintained alternative to orca that reduces Docker image size and improves compatibility across environments while preserving multi-format export capability.

## Related tools

- **Kaleido** (Static image generation backend replacing orca; converts plotly/ggplot2 objects to PNG, JPEG, SVG with configurable dimensions and scaling)
- **orca** (Deprecated static image export backend; being replaced by Kaleido in this workflow)
- **Shiny** (R web framework hosting the interactive omics GUI and managing plot export UI controls)
- **pmartR** (R package providing omics data processing and visualization functions whose outputs are exported via Shiny) — https://github.com/pmartR/pmartR
- **plotly** (R package for interactive plotting; integrates with Kaleido for static export)
- **Docker** (Containerization platform; Dockerfile specifies Kaleido installation and Python virtual environment setup)

## Examples

```
# In Dockerfile-base, replace: RUN apt-get install orca with: RUN echo 'kaleido' >> requirements.txt
# In Shiny server.R, configure: knitr::opts_knit$set(kaleido.path = Sys.getenv('KALEIDO_PATH')); plotly::orca(config = list(kaleido = list(width = 800, height = 600, scale = 2)))
```

## Evaluation signals

- All three export formats (PNG, JPEG, SVG) render successfully from the same plotly/ggplot2 object without errors or timeouts in the Shiny application.
- Exported PNG and JPEG files match the configured width and height parameters (±1–2 px tolerance for rendering engines); SVG files contain valid XML markup and scale without distortion.
- File sizes are reasonable: PNG/JPEG should be < 500 KB for typical omics plots; SVG may be larger but should remain < 2 MB.
- Kaleido backend is confirmed active by inspecting Docker container runtime logs or R console output (e.g., 'using kaleido' message, no orca fallback attempts).
- Docker image build succeeds without orca installation errors; `docker run` confirms Python virtual environment is sourced and kaleido is importable (e.g., `python -c 'import kaleido'` succeeds).

## Limitations

- Kaleido export performance may be slower than orca for very large, complex plots (> 100k data points) due to Python subprocess overhead; users may experience delays on slower hardware.
- SVG output may not preserve all interactive features (tooltips, click handlers) from the original Shiny plot; SVG is static by design.
- Python environment must be correctly configured and accessible; misconfigured MAP_CONFIG yml or missing requirements.txt dependencies will cause export failures at runtime.
- Export quality depends on Kaleido version and font availability in the Docker container; missing system fonts may cause text rendering differences between local R and containerized environments.

## Evidence

- [discussion] Remove orca in favor of Kaleido: "Remove orca in favor of Kaleido"
- [other] Multi-format export from Shiny: "supports downloading plots in multiple formats (png/jpeg/svg) with configurable export parameters"
- [other] Kaleido backend configuration in Shiny R code: "Modify the Shiny application R code to configure Kaleido (instead of orca) as the plotting backend with width, height, and scale parameters for export functions."
- [readme] Python virtual environment setup: "You will also need a Python virtual environment with the packages from requirements.txt installed. Then, add a .yml file with `python_venv: <path-to-your-venv>` in it."
- [other] Testing plot export across formats: "Test plot export functionality by generating PNG, JPEG, and SVG output files from sample omics visualizations in the PMart ShinyApp interface."
