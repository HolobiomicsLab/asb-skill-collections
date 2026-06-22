---
name: r-package-loading-and-diagnostics
description: Use when when deploying an R package from a non-CRAN repository (e.g., r-universe, Bioconductor, GitHub), or when verifying that a package build is reproducible and meets CRAN submission standards prior to integration into a larger analysis pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3355
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_0605
  tools:
  - R
  - r-universe
  - R-CMD-check GitHub Actions workflow
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
---

# r-package-loading-and-diagnostics

## Summary

Install an R package from a custom repository (such as r-universe) and validate that it loads without errors and passes R-CMD-check compliance testing. This skill ensures package integrity before downstream use in a computational workflow.

## When to use

When deploying an R package from a non-CRAN repository (e.g., r-universe, Bioconductor, GitHub), or when verifying that a package build is reproducible and meets CRAN submission standards prior to integration into a larger analysis pipeline.

## When NOT to use

- Package is already installed and verified in your environment; skip re-installation.
- Package is available on official CRAN and you have no reason to use a development or alternative repository.
- You are only interested in querying package metadata without loading it into memory.

## Inputs

- R package source code (GitHub repository)
- r-universe repository URL (or equivalent custom CRAN-like repository)
- R version (≥3.x recommended)

## Outputs

- Loaded R package object in global environment
- R-CMD-check report (HTML or text) documenting test results
- Installation log confirming successful library() call

## How to apply

First, configure R to use the target repository by passing a vector of repository URLs to install.packages(), prioritizing the custom repository (e.g., r-universe) and falling back to Bioconductor and CRAN. Install the package using install.packages() with the configured repos argument. Load the package into the R environment using library() and verify no errors or warnings occur. Finally, run R-CMD-check (either via R's check() function or via the CLI) against the installed package to validate against the CRAN submission checklist; all tests must pass. Monitor the package's GitHub Actions R-CMD-check badge to confirm CI passes on the latest commit.

## Related tools

- **r-universe** (Custom CRAN-compatible repository hosting development versions of R packages with automated R-CMD-check CI) — https://taxonomicallyinformedannotation.r-universe.dev
- **R-CMD-check GitHub Actions workflow** (Continuous integration pipeline that validates package build and test suite compliance against CRAN standards) — https://github.com/taxonomicallyinformedannotation/tima/actions/workflows/R-CMD-check.yaml
- **R** (Core runtime environment for package installation, loading, and diagnostic validation)

## Examples

```
install.packages("tima", repos=c("https://taxonomicallyinformedannotation.r-universe.dev", "https://bioconductor.org/packages/release/bioc", "https://cloud.r-project.org")); library(tima)
```

## Evaluation signals

- library(package_name) executes without errors, warnings, or startup messages indicating missing dependencies.
- R-CMD-check report shows 0 errors, 0 warnings, and 0 notes (or acceptable notes per CRAN policy).
- GitHub Actions R-CMD-check badge on the repository README displays a passing status (green check).
- Installation log from install.packages() confirms 'package successfully unpacked and MD5 sums checked'.
- Namespace and exported functions are accessible via ls('package:package_name') and match the DESCRIPTION file.

## Limitations

- R-CMD-check may pass in a development environment but fail in restricted CRAN submission due to undeclared system dependencies or platform-specific issues not caught by the developer's CI environment.
- Package loading succeeds but downstream function calls may fail if required external resources (e.g., LOTUS database, SIRIUS executables) are not installed separately; install_tima() helper is provided but may require manual troubleshooting.
- r-universe builds are automated but can be delayed or fail if upstream dependencies on Bioconductor or CRAN are temporarily unavailable or have breaking API changes.

## Evidence

- [readme] Configure R to use the r-universe repository: "As the package is not (yet) available on CRAN, you will need to install with: install.packages( "tima", repos = c( "https://taxonomicallyinformedannotation.r-universe.dev","
- [other] Load the installed package and confirm no errors: "Load the installed package into the R environment using library(tima) and confirm no errors occur."
- [readme] Verify R-CMD-check test suite passes: "The tima package has an active R-CMD-check workflow configured on GitHub that validates the package build and check status."
- [readme] R-CMD-check badge indicates CI validation: "[![R-CMD-check](https://github.com/taxonomicallyinformedannotation/tima/actions/workflows/R-CMD-check.yaml/badge.svg)](https://github.com/taxonomicallyinformedannotation/tima/actions/workflows/R-CMD-c"
