---
name: dockerfile-dependency-management
description: Use when when deploying a Shiny application with mixed R and Python dependencies
  (e.g., pmartR backend with Kaleido for plot export) to production or CI/CD pipelines,
  and when some dependencies are under active development alongside the application.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0092
  tools:
  - pmartR
  - orca
  - R
  - Docker
  - renv
  - mapDataAccess
  - Kaleido
  - Shiny
  license_tier: open
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

# dockerfile-dependency-management

## Summary

Manage R package, Python library, and system-level dependencies across layered Docker containers to ensure reproducible omics analysis environments. This skill separates base container construction (system libraries and stable dependencies) from application container construction (source code deployment), reducing build times and enabling parallel development of frequently-updated packages.

## When to use

When deploying a Shiny application with mixed R and Python dependencies (e.g., pmartR backend with Kaleido for plot export) to production or CI/CD pipelines, and when some dependencies are under active development alongside the application. Use this skill if you need to (1) reduce Docker image rebuild times by caching stable dependencies in a base layer, (2) manage private package installation credentials separately, or (3) coordinate updates to tightly-coupled packages (pmartR, mapDataAccess) without rebuilding all system libraries.

## When NOT to use

- If your application has only R dependencies and no Python libraries (overhead of two-stage build may not justify reduced rebuild time).
- If all upstream dependencies are stable, released packages not under active development alongside your application (single-stage Dockerfile is simpler).
- If you do not have access to private Git repositories or do not need credential-based package installation (secrets management adds complexity).

## Inputs

- Dockerfile-base (system and R package installation recipe)
- Dockerfile (top-level application deployment recipe)
- renv.lock (R package dependency snapshot with versions and sources)
- DESCRIPTION file (R package metadata and direct dependency list)
- requirements.txt (Python package list with versions)
- GitLab/GitHub personal access tokens (for private repository access)
- .dockerignore file (to exclude large files from build context)

## Outputs

- Base Docker image (tagged, e.g. code-registry.emsl.pnl.gov/multiomics-analyses/pmart_standalone/base:1.0.0)
- Top Docker image (tagged, e.g. code-registry.emsl.pnl.gov/multiomics-analyses/pmart_standalone:1.0.0)
- Deployed container with reproducible R, Python, and system environment
- Runnable Shiny application accessible at specified port (e.g. https://127.0.0.1:8300)

## How to apply

Construct a two-stage Dockerfile hierarchy: (1) Build a base container (Dockerfile-base) that installs all system libraries, R packages via renv lockfile, and in-development packages from private Git repositories using build secrets (GitLab and GitHub PATs). Use `renv::settings$package.dependency.fields("Depends", "Imports")` to restrict lockfile tracking to direct and transitive 'Depends'/'Imports' fields only, then snapshot with `renv::snapshot(type="implicit")`. (2) Build a top container that references the base image, copies application source code, and exposes the application port. When updating dependencies, modify DESCRIPTION and renv.lock, then rebuild only the base container if core dependencies change; rebuild only the top container if application code changes. For Python dependencies (e.g., Kaleido replacing orca), list them in requirements.txt and install during base container build. Document which packages are tracked in renv.lock versus installed directly in Dockerfile-base comments, since actively-developed packages may be excluded from the lockfile to reduce build times.

## Related tools

- **renv** (R dependency lockfile management and reproducible environment restoration; snapshots package versions and sources into renv.lock for base container installation) — https://rstudio.github.io/renv/articles/renv.html
- **Docker** (Container orchestration and layered image build system for base and top container construction and versioning)
- **pmartR** (R package for omics analysis; installed in base container, remains under active development so tracked separately in Dockerfile-base rather than renv.lock) — https://github.com/pmartR/pmartR
- **mapDataAccess** (Private R package for data access layer; installed via GitLab PAT in base container, excluded from renv.lock due to active development)
- **Kaleido** (Python library for static image export (PNG, JPEG, SVG) from plots; listed in requirements.txt and installed in base container to replace orca)
- **Shiny** (R package for interactive web application framework; managed via renv.lock in base container)

## Examples

```
docker build -f Dockerfile-base --secret id=access_tokens,src=.mysecret -t code-registry.emsl.pnl.gov/multiomics-analyses/pmart_standalone/base:1.0.0 . && docker build --build-arg base_tag=code-registry.emsl.pnl.gov/multiomics-analyses/pmart_standalone/base:1.0.0 -t code-registry.emsl.pnl.gov/multiomics-analyses/pmart_standalone:1.0.0 .
```

## Evaluation signals

- Base and top Docker images build successfully with no package installation errors or version conflicts when running `docker build -f Dockerfile-base --secret id=access_tokens,src=.mysecret` and `docker build --build-arg base_tag=<image>`.
- renv.lock contains only packages with 'Depends' and 'Imports' fields (no 'Suggests'); verify by confirming renv.settings includes `package.dependency.fields("Depends", "Imports")` in renv/settings.json.
- Actively-developed packages (pmartR, mapDataAccess) are installed directly in Dockerfile-base via Git clone/install.packages() and do NOT appear in renv.lock; confirm by checking for their absence in renv.lock and presence in Dockerfile-base source.
- The Shiny application starts and responds to HTTP requests at the mapped port (e.g., https://127.0.0.1:8300) when launched from the top container; verify with `curl -k https://127.0.0.1:8300` or browser navigation.
- Plot export functionality generates PNG, JPEG, and SVG files with correct dimensions (width, height, scale parameters applied); verify by uploading sample omics data, generating plots, and downloading all three formats from the web UI, then checking image properties and file sizes.

## Limitations

- Private package installation requires valid GitLab and GitHub personal access tokens (PATs) passed as build secrets; token expiration or revocation will break base container builds and must be rotated and re-supplied.
- renv lockfile becomes stale if upstream packages release breaking changes; the lockfile captures a point-in-time snapshot and does not auto-update. Developers must manually call `renv::snapshot()` to refresh locked versions.
- Actively-developed packages (pmartR, mapDataAccess) excluded from renv.lock must be manually managed in Dockerfile-base; if these packages introduce incompatibilities with renv-locked dependencies, resolution is manual and may require pinning specific versions in both Dockerfile-base and renv.lock.
- Two-stage build process introduces additional maintenance burden: changes to base dependencies require base container rebuild and version increment, which must then be referenced in the top Dockerfile `--build-arg base_tag`. Mismatched base/top versions can cause subtle runtime failures.
- Python virtual environment setup (requirements.txt + venv) for local development is separate from Docker and must be manually configured; the README requires users to create a .yml configuration file pointing to the venv path and set MAP_CONFIG environment variable, adding friction for local development.

## Evidence

- [readme] We build a base container which has all the system libraries and R packages installed, and then build a container on top of it that simply copies the app source code and exposes the correct port.: "We build a base container which has all the system libraries and R packages installed, and then build a container on top of it that simply copies the app source code and exposes the correct port."
- [readme] Some in-development packages are not being tracked in renv.lock (to reduce Docker image build times). These can be seen in the `install commonly updated packages` section of Dockerfile-base.: "Some in-development packages are not being tracked in renv.lock (to reduce Docker image build times). These can be seen in the `install commonly updated packages` section of Dockerfile-base."
- [readme] To build the base container, you must provide a gitlab PAT in order to install mapDataAccess and other private git repos.: "To build the base container, you must provide a gitlab PAT in order to install mapDataAccess and other private git repos."
- [readme] Set renv to only install sub-dependencies in the "Depends" and "Imports" field of installed packages. renv::settings$package.dependency.fields("Depends", "Imports"). This should get recorded in ./renv/settings.json: "Set renv to only install sub-dependencies in the "Depends" and "Imports" field of installed packages. renv::settings$package.dependency.fields("Depends", "Imports"). This should get recorded in"
- [discussion] Remove orca in favor of Kaleido: "Remove orca in favor of Kaleido"
