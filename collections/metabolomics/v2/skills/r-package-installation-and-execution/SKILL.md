---
name: r-package-installation-and-execution
description: Use when when you have a new or updated R package available via a non-CRAN repository (such as r-universe) and need to verify it installs cleanly, passes R-CMD-check compliance, and is ready for downstream workflow execution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - R
  - r-universe
  - R-CMD-check
  - GitHub Actions
  - Docker
derived_from:
- doi: 10.3389/fpls.2019.01329
  title: tima
evidence_spans:
- The initial work is available at <https://doi.org/10.3389/fpls.2019.01329>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tima
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_tima
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fpls.2019.01329
  all_source_dois:
  - 10.3389/fpls.2019.01329
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# R Package Installation and Execution

## Summary

Install an R package from a custom repository and verify successful execution through package loading and validation checks. This skill ensures the package meets build standards and can be reliably invoked in an R environment.

## When to use

When you have a new or updated R package available via a non-CRAN repository (such as r-universe) and need to verify it installs cleanly, passes R-CMD-check compliance, and is ready for downstream workflow execution. Use this before attempting to run domain-specific analyses that depend on the package.

## When NOT to use

- Package is already installed and loaded in your current session and you only need to use it (no installation step required).
- Package is already available on CRAN; use standard `install.packages()` without custom repos instead.
- You are working in a containerized environment (Docker or Singularity) where dependencies may be pre-built; prefer pulling the pre-built image.

## Inputs

- R installation with network access
- Package repository URL (e.g., r-universe host)
- Package name and desired version (optional)

## Outputs

- Installed R package in library path
- Loaded package namespace in R session
- R-CMD-check validation report (from CI badge or local run)
- Optional: example data files and minimal execution output

## How to apply

Configure R to use the target repository URL in its package sources (via the `repos` parameter in `install.packages()`). Install the package using `install.packages()` and verify with `library()` that it loads without errors. If the package provides a secondary setup function (e.g., `tima::install_tima()`), invoke it to ensure all optional dependencies are available. Confirm that the package has passed R-CMD-check on its CI pipeline (check the README badge or GitHub Actions workflow). Load example data if available (e.g., via `tima::get_example_files()`) and attempt a minimal function call to confirm runtime execution succeeds.

## Related tools

- **r-universe** (Package repository hosting the compiled R package binaries and source) — https://taxonomicallyinformedannotation.r-universe.dev/tima
- **R-CMD-check** (Automated validation workflow that verifies package compliance with CRAN submission standards) — https://github.com/taxonomicallyinformedannotation/tima/actions/workflows/R-CMD-check.yaml
- **GitHub Actions** (CI/CD platform that runs R-CMD-check on commits and publishes status badge) — https://github.com/taxonomicallyinformedannotation/tima
- **Docker** (Optional containerized environment with pre-installed R package and all dependencies) — https://hub.docker.com/r/adafede/tima-r/

## Examples

```
install.packages('tima', repos = c('https://taxonomicallyinformedannotation.r-universe.dev', 'https://bioconductor.org/packages/release/bioc', 'https://cloud.r-project.org')); tima::install_tima(); library(tima); tima::get_example_files()
```

## Evaluation signals

- Package loads in R session with no errors or warnings when invoked as `library(package_name)`
- R-CMD-check badge in repository README shows passing status (green badge), indicating compliance with CRAN submission checklist
- Example data can be retrieved via the package's helper function (e.g., `tima::get_example_files()`) without file-not-found or permission errors
- A minimal function call from the package (e.g., `validate_inputs()` or equivalent) executes successfully and produces expected output structure
- Package namespace and exported functions are visible when running `ls('package:package_name')` or similar introspection

## Limitations

- Package lifecycle is 'experimental' (as indicated by lifecycle badge), meaning API and behavior may change without deprecation notice in future releases.
- Secondary dependency installation via a helper function (e.g., `tima::install_tima()`) may fail if upstream package repositories are unavailable or if system-level dependencies (e.g., build tools, system libraries) are not present.
- Custom column names in input files are configurable but require manual parameter specification; mismatched column names will cause runtime errors, not installation errors.
- No changelog is published in the repository, so version-to-version breaking changes may not be documented; users must inspect GitHub commit history or release notes to track changes.

## Evidence

- [readme] Installation method and repository configuration: "install.packages(
  "tima",
  repos = c(
    "https://taxonomicallyinformedannotation.r-universe.dev",
    "https://bioconductor.org/packages/release/bioc",
    "https://cloud.r-project.org"
  )
)"
- [readme] Secondary dependency setup function: "Then, you should be able to install the rest with:

``` r
tima::install_tima()
```"
- [readme] Package loading verification: "Load the installed package into the R environment using library(tima) and confirm no errors occur."
- [readme] R-CMD-check validation workflow: "Run R-CMD-check on the installed package to validate against the CRAN submission checklist and verify all tests pass as indicated by the CI badge in the README."
- [readme] Example data retrieval for verification: "In case you do not have your data ready, you can obtain some example data using:

``` r
tima::get_example_files()
```"
- [readme] Lifecycle and experimental status: "[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)]"
