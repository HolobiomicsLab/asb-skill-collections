---
name: visualization-format-conversion
description: Use when you have generated exploratory data analysis plots (PCA, correlation heatmaps, missing-variable plots) in the pmartR Shiny interface and need to download them as static images for inclusion in reports, manuscripts, or presentations with specific width, height, and resolution requirements.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3561
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - pmartR
  - orca
  - R
  - Docker
  - Kaleido
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
---

# visualization-format-conversion

## Summary

Convert omics visualizations from interactive plot objects to static image files in multiple formats (PNG, JPEG, SVG) with configurable dimensions and scale parameters. This skill enables users to export publication-ready figures from the pmartR Shiny application without requiring external plotting software.

## When to use

Apply this skill when you have generated exploratory data analysis plots (PCA, correlation heatmaps, missing-variable plots) in the pmartR Shiny interface and need to download them as static images for inclusion in reports, manuscripts, or presentations with specific width, height, and resolution requirements.

## When NOT to use

- The plot is intended for interactive exploration or dashboard embedding—use interactive export formats instead.
- The visualization is already in a static format (PDF, PNG, etc.)—skip conversion.
- Real-time rendering or streaming output is required—Kaleido produces static snapshots only.

## Inputs

- plot object from pmartR/Shiny (e.g., PCA plot, heatmap, missing-value plot)
- export parameters (width in pixels, height in pixels, scale factor)
- target output format specification (png, jpeg, or svg)

## Outputs

- PNG image file (raster, configurable resolution)
- JPEG image file (raster, compressed)
- SVG image file (vector, scalable)

## How to apply

Configure Kaleido (not orca) as the static image rendering backend in the Shiny application, specifying export parameters including width, height, and scale. When a user triggers the download action for a plot visualization, pass the plot object to the configured backend with the desired output format (PNG, JPEG, or SVG). Kaleido renders the interactive plot as a static raster or vector image at the specified dimensions. Test the exported image to verify correct rendering, accurate dimension scaling, and format-specific quality (raster resolution for PNG/JPEG, vector fidelity for SVG).

## Related tools

- **Kaleido** (Static image rendering backend; replaces orca for converting plot objects to PNG, JPEG, or SVG formats with configurable width, height, and scale parameters)
- **orca** (Deprecated predecessor static image renderer; no longer used in updated pmartR Shiny application)
- **pmartR** (R package providing plot objects (PCA, heatmaps, missing-value plots) that are passed to Kaleido for export) — https://github.com/pmartR/pmartR
- **Shiny** (Web framework hosting the interactive application; manages plot rendering and user-triggered export actions)
- **R** (Language runtime in which pmartR, Shiny, and Kaleido integration are implemented)
- **Docker** (Containerization tool; Dockerfile updated to remove orca and add Kaleido as a Python dependency for deployment)

## Evaluation signals

- All three output formats (PNG, JPEG, SVG) are successfully generated from the same input plot object with no errors.
- Exported image dimensions match the specified width and height parameters (verify pixel dimensions in image metadata or file properties).
- Visual content and layout are identical between output formats; no clipping, misalignment, or rendering artifacts appear.
- SVG files maintain vector fidelity and are scalable without quality loss; PNG/JPEG files render at specified resolution with consistent color and annotation rendering.
- Download functionality completes without timeout or memory errors; file sizes are within expected ranges for the chosen format and resolution.

## Limitations

- Kaleido requires a Python environment with the kaleido package installed; this dependency must be included in the Docker image or local virtual environment (requirements.txt).
- SVG export may not fully preserve interactive Shiny features (e.g., hover tooltips) in the static output; SVG is suitable for publication but not for interactive consumption.
- Large plots or high-resolution exports (large width/height/scale values) may consume significant memory or CPU; timeout or resource limits may apply in containerized deployments.
- Fonts and styling defined in the Shiny application may render differently in the static export if the fonts are not available in the Kaleido rendering environment.

## Evidence

- [other] The pmartR Shiny application supports downloading plots in multiple formats (png/jpeg/svg) with configurable export parameters through replacement of orca with Kaleido and associated Python dependencies.: "supports downloading plots in multiple formats (png/jpeg/svg) with configurable export parameters through replacement of orca with Kaleido"
- [other] Update the Dockerfile to remove orca installation and add Kaleido as a Python dependency; modify the Shiny application R code to configure Kaleido (instead of orca) as the plotting backend with width, height, and scale parameters for export functions.: "Update the Dockerfile to remove orca installation and add Kaleido as a Python dependency. 2. Modify the Shiny application R code to configure Kaleido (instead of orca) as the plotting backend with"
- [other] Test plot export functionality by generating PNG, JPEG, and SVG output files from sample omics visualizations in the PMart ShinyApp interface; verify that all exported plots render correctly across the three formats and that the configurable dimensions are applied as expected.: "Test plot export functionality by generating PNG, JPEG, and SVG output files from sample omics visualizations in the PMart ShinyApp interface. 4. Verify that all exported plots render correctly"
- [readme] Visualize and download all resources: "Visualize and download all resources."
- [full_text] Remove orca in favor of Kaleido: "Remove orca in favor of Kaleido"
