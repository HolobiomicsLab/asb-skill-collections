---
name: shiny-app-configuration-deployment
description: Use when you have built a Shiny application (global.R, ui.R, server.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3585
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3071
  tools:
  - MODE ShinyApp
  - Shiny
  - trelliscope
  - RStudio
  - Docker
derived_from:
- doi: 10.1021/acs.jproteome.4c00650
  title: MODE
evidence_spans:
- github.com__pmartR__MODE_ShinyApp
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mode_cq
    doi: 10.1021/acs.jproteome.4c00650
    title: MODE
  dedup_kept_from: coll_mode_cq
schema_version: 0.2.0
---

# Shiny App Configuration and Deployment

## Summary

Configure and deploy a Shiny-based interactive web application for omics data visualization, with support for local RStudio execution, Docker containerization, and hosted web server deployment. This skill ensures reproducible, shareable access to interactive statistical and exploratory analysis interfaces.

## When to use

You have built a Shiny application (global.R, ui.R, server.R) that visualizes omics data (abundance/expression measurements, statistical results) and need to make it accessible to collaborators or end users across multiple execution environments (local development, Docker, or production web hosting). Use this skill when reproducibility and ease of deployment across platforms are priorities.

## When NOT to use

- Your application logic is static or non-interactive (use standard HTML/markdown instead).
- The omics dataset is too large to embed in browser memory or transfer over HTTP without optimization (consider data subsetting or server-side filtering).
- You do not have access to a Shiny Server, Docker runtime, or RStudio environment for your target deployment platform.

## Inputs

- Shiny application source files (global.R, ui.R, server.R)
- omics data (abundance/expression measurements as data frames or matrices)
- statistical results (p-values, effect sizes, fold-changes)
- Dockerfile and Dockerfile-base specifications
- GitHub repository with application code

## Outputs

- Running Shiny application accessible in RStudio
- Docker container images ready for deployment
- Deployed web application accessible via HTTP(S) URL
- Interactive trelliscope displays with embedded data and controls

## How to apply

First, organize your Shiny application into modular files (global.R for shared objects, ui.R for user interface, server.R for reactive logic). For local execution, ensure the repo is cloned and accessible in RStudio; users can run the app via the 'Run App' button. For containerized deployment, create a Dockerfile-base (base image with R and dependencies) and a Dockerfile (application layer); build both containers in sequence, updating container names appropriately. For web hosting, deploy the application to a Shiny Server or equivalent platform (e.g., map.emsl.pnnl.gov). Document all three deployment paths in the README with clear instructions and example commands so end users can choose their preferred execution environment.

## Related tools

- **Shiny** (Web application framework for building interactive R-based interfaces to omics data)
- **trelliscope** (Interactive visualization library integrated into Shiny UI to render shareable statistical panel displays)
- **RStudio** (Integrated development environment for local Shiny app execution and testing via 'Run App' button)
- **Docker** (Containerization platform for reproducible application deployment across environments)
- **MODE ShinyApp** (Reference Shiny application for omics visualization; serves as template for configuration and deployment) — https://github.com/pmartR/MODE_ShinyApp

## Examples

```
# Local: In RStudio, open global.R or server.R and click 'Run App'
# Docker: docker build -f Dockerfile-base --no-cache -t mode-base && docker build -f Dockerfile --no-cache -t mode-app && docker run -p 3838:3838 mode-app
# Web: Navigate to https://map.emsl.pnnl.gov/app/mode-classic
```

## Evaluation signals

- Application runs without errors when 'Run App' button is clicked in RStudio after cloning the repo.
- Docker build commands complete successfully and produce container images with correct naming and layering.
- Web application loads and responds to user interactions (filters, sorts, panel navigation) when accessed via the hosted URL.
- Trelliscope displays render interactively with all cognate variables (p-values, effect sizes, annotations) accessible and sortable.
- README documents all three deployment paths (local, Docker, web) with working examples that a new user can follow without modification.

## Limitations

- Local RStudio execution requires R, Shiny, and all application dependencies installed on the user's machine.
- Docker deployment requires Docker runtime and may incur additional resource overhead compared to native execution.
- Web hosting deployment depends on external server availability and network connectivity; no changelog mechanism is currently tracked.
- Application performance may degrade with very large omics datasets (millions of features) due to browser rendering and data transfer constraints.

## Evidence

- [readme] Deployment methods documentation: "Clone the git repo, open the global.R, ui.R, or server.R file in RStudio, and click the 'Run App' button."
- [readme] Docker containerization approach: "First build the base docker file using Dockerfile-base, and then build the MODE dockerfile using Dockerfile. Make sure to update the dockerfiles with whatever you named your containers."
- [readme] Hosted web deployment option: "Go to our application website"
- [intro] Core application purpose and output: "Create shareable and interactive trelliscope displays for visualizing omics data and statistics results."
- [readme] Application architecture: "MODE:  An application to visualize omics data in trelliscope."
