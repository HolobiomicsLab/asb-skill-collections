---
name: kaleido-backend-integration
description: Use when when a Shiny application currently uses orca for static plot
  export but requires a lighter-weight, Python-native alternative that avoids Node.js/Electron
  runtime overhead.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pmartR
  - Kaleido
  - orca
  - R
  - Docker
  - Shiny
  - Python
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- Remove orca in favor of Kaleido
- the bulk of the functionality of the package to be available to the user without
  the need for familiarity with R or the package itself
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

# kaleido-backend-integration

## Summary

Replace the orca plotting backend with Kaleido to enable static image export (PNG, JPEG, SVG) from interactive Shiny visualizations without external system dependencies. This integration provides configurable export parameters (width, height, scale) for omics data plots in web applications.

## When to use

When a Shiny application currently uses orca for static plot export but requires a lighter-weight, Python-native alternative that avoids Node.js/Electron runtime overhead. Specifically indicated when deploying containerized omics analysis pipelines that need to reduce Docker image size and dependency complexity while maintaining multi-format export (PNG/JPEG/SVG) from R/ggplot2 visualizations.

## When NOT to use

- Input plots are already in static raster format (PNG/JPEG/SVG); no conversion is needed.
- The application requires interactive/dynamic export features (e.g., hover tooltips in exported files); Kaleido produces static snapshots only.
- Downstream workflows depend on orca-specific output metadata or vector graphics properties not preserved by Kaleido.

## Inputs

- Dockerfile (with orca installation and Python environment setup)
- R/Shiny application code with orca-based export functions
- requirements.txt or equivalent Python dependency manifest
- ggplot2 or plotly R plot objects from omics visualization modules
- Configuration parameters: export width (pixels), height (pixels), scale factor

## Outputs

- Updated Dockerfile (orca removed, Kaleido added)
- Modified R code with Kaleido backend configuration
- PNG, JPEG, SVG image files exported from Shiny downloadHandler
- Docker image with reduced size and simplified Python dependency graph

## How to apply

First, update the Dockerfile to remove orca installation and add Kaleido as a Python package dependency in requirements.txt. Second, configure the Shiny application's R plotting backend to use Kaleido (via reticulate or plotly/kaleido integration) with explicit width, height, and scale parameters for each export function call. Third, replace all orca-specific export calls in the Shiny UI with Kaleido-compatible syntax, ensuring that downstream code paths (e.g., downloadHandler reactives) invoke the new backend. Finally, validate multi-format output by generating representative PNG, JPEG, and SVG files from sample omics visualizations (e.g., PCA plots, heatmaps) and verify pixel dimensions and rendering fidelity match the configured parameters.

## Related tools

- **Kaleido** (Static image export backend for converting R/plotly plots to PNG, JPEG, SVG formats with configurable dimensions and scale)
- **orca** (Legacy image export backend being replaced; uses Node.js/Electron runtime)
- **Shiny** (Web framework hosting the interactive plotting UI and downloadHandler reactive elements) — https://github.com/rstudio/shiny
- **pmartR** (Backend R package providing omics analysis and visualization functions (PCA, heatmaps, etc.) whose outputs are exported via Kaleido) — https://github.com/pmartR/pmartR
- **Docker** (Containerization tool; Dockerfile updated to install Kaleido Python package and remove orca system dependencies)
- **Python** (Runtime for Kaleido; configured in requirements.txt and invoked by R via reticulate or embedded in Shiny server)
- **R** (Language in which Shiny app and pmartR plot objects are written; coordinates Kaleido backend calls)

## Examples

```
# In Dockerfile: RUN pip install -r requirements.txt (with Kaleido listed); # In R/Shiny server.R: kaleido::save_image(p, 'plot.png', width=800, height=600, scale=2)
```

## Evaluation signals

- Dockerfile build succeeds without orca installation; resulting image is smaller in size than orca-based variant.
- R code executes without errors when calling plot export functions; no fallback to orca or undefined backend warnings.
- PNG, JPEG, and SVG files are generated from sample omics plots (e.g., PCA, heatmap) with correct pixel dimensions matching configured width and height parameters.
- Exported images render correctly in standard viewers (e.g., image browser, web browser) with expected visual fidelity and color accuracy.
- Shiny downloadHandler reactive triggers successfully on user request; file download completes without timeout or corruption.

## Limitations

- Kaleido produces static snapshots; interactive features (tooltips, hover information) present in plotly HTML are lost in exported PNG/JPEG/SVG.
- Font rendering and fine graphical details may differ between screen display and exported raster formats due to anti-aliasing and DPI conversion.
- Large-scale batch export of many plots may require careful tuning of Python process pooling and memory limits to avoid resource exhaustion in containerized environments.
- SVG export quality and text handling depend on Kaleido version; compatibility with very large or complex R plots (thousands of data points) is not explicitly validated in the article.

## Evidence

- [discussion] Remove orca in favor of Kaleido: "Remove orca in favor of Kaleido"
- [other] The pmartR Shiny application supports downloading plots in multiple formats (png/jpeg/svg) with configurable export parameters through replacement of orca with Kaleido: "supports downloading plots in multiple formats (png/jpeg/svg) with configurable export parameters through replacement of orca with Kaleido"
- [other] Update the Dockerfile to remove orca installation and add Kaleido as a Python dependency: "Update the Dockerfile to remove orca installation and add Kaleido as a Python dependency"
- [other] Modify the Shiny application R code to configure Kaleido (instead of orca) as the plotting backend with width, height, and scale parameters for export functions: "Modify the Shiny application R code to configure Kaleido (instead of orca) as the plotting backend with width, height, and scale parameters"
- [other] Test plot export functionality by generating PNG, JPEG, and SVG output files from sample omics visualizations in the PMart ShinyApp interface: "Test plot export functionality by generating PNG, JPEG, and SVG output files from sample omics visualizations"
- [other] Verify that all exported plots render correctly across the three formats and that the configurable dimensions are applied as expected: "Verify that all exported plots render correctly across the three formats and that the configurable dimensions are applied"
- [readme] You will also need a Python virtual environment with the packages from requirements.txt installed: "You will also need a Python virtual environment with the packages from requirements.txt installed"
