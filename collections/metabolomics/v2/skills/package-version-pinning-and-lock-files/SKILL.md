---
name: package-version-pinning-and-lock-files
description: Use when when a multi-language analysis pipeline (R + Python) has been validated and you need to document the exact dependency tree so that other researchers or systems can recreate the same computational environment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3546
  edam_topics:
  - http://edamontology.org/topic_0769
  tools:
  - R
  - reticulate
  - keras
  - pROC
  - caret
  - numpy
  - renv
  - conda/environment.yml
  - r-miniconda
derived_from:
- doi: 10.3390/metabo13080944
  title: SERDA
evidence_spans:
- R version 3.6.3 (2020-02-29)
- packageVersion("reticulate") [1] ‘1.19’
- packageVersion("keras") [1] ‘2.7.0’
- packageVersion("pROC") [1] ‘1.17.0.1’
- packageVersion("caret") [1] ‘6.0.86’
- 'numpy_version: 1.18.1'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_serda_cq
    doi: 10.3390/metabo13080944
    title: SERDA
  dedup_kept_from: coll_serda_cq
schema_version: 0.2.0
---

# package-version-pinning-and-lock-files

## Summary

Capture and document exact versions of R, Python, and all transitive dependencies required to execute a computational analysis pipeline reproducibly. This skill ensures that future executions of SERDA normalization (or similar multi-language workflows) produce identical results by freezing the software environment at the point of validation.

## When to use

When a multi-language analysis pipeline (R + Python) has been validated and you need to document the exact dependency tree so that other researchers or systems can recreate the same computational environment. Specifically use this when you have a working SERDA normalization setup and want to prevent silent failures or results drift caused by automatic package updates.

## When NOT to use

- Input is a development environment where frequent package updates are desired or package versions are intentionally left unpinned for exploration.
- The pipeline is a one-off analysis that will never be re-run or shared; overhead of lock-file maintenance outweighs benefit.
- Cross-language integration is not required; pure R or pure Python workflows may use simpler versioning approaches (e.g., just renv or just pip freeze without coordinating interop layer).

## Inputs

- Working R installation (e.g. R 3.6.3)
- Working Python environment (e.g. Python 3.6.10 via r-miniconda)
- Validated analysis script (e.g. SERDA runner.R)
- Package interop configuration (reticulate py_config() output)

## Outputs

- renv.lock file (R dependency lock file with pinned versions)
- environment.yml file (conda/pip dependency specification)
- Documented version manifest (e.g., README System section listing all tool versions)
- Reproducible environment specification suitable for deployment

## How to apply

First, identify the primary language runtime versions (e.g., R 3.6.3, Python 3.6.10) and confirm the distribution source (e.g., Anaconda for Python, CRAN for R packages). Second, extract all direct and transitive dependency versions using language-native introspection tools (packageVersion() in R, pip freeze in Python). Third, document the cross-language binding layer explicitly (e.g., reticulate 1.19 pinned to route through r-miniconda to Python 3.6.10). Fourth, resolve the full dependency graph and version constraints, noting that some packages (like keras 2.7.0) may depend on specific versions of upstream packages (pROC 1.17.0.1, caret 6.0.86). Finally, export the pinned specification as a machine-readable lock file (renv.lock for R or environment.yml for conda) so that installation tools can replay the exact versions without ambiguity.

## Related tools

- **renv** (R-side lock file generator and environment manager; captures R package versions and creates renv.lock for reproducible R library states)
- **reticulate** (R–Python interop bridge; must be version-pinned (1.19 in SERDA) to ensure stable routing from R to the correct Python environment and numpy version) — https://rstudio.github.io/reticulate/index.html
- **conda/environment.yml** (Python-side lock file; specifies Python version (3.6.10), numpy version (1.18.1), and conda-managed dependencies in declarative format for reproducible environment creation)
- **r-miniconda** (Self-contained Python distribution bundled with R via reticulate; provides isolated Python 3.6.10 and numpy 1.18.1 independent of system Python)
- **keras** (Deep learning framework pinned to version 2.7.0; depends on pinned reticulate and Python backend versions to ensure consistent model training and inference)
- **caret** (Machine learning framework pinned to 6.0.86; coordinate this version with pROC 1.17.0.1 to avoid API breaks in model evaluation workflows)

## Examples

```
# In R: install packages from lock file and verify versions
renv::restore()
py_config()
packageVersion('keras')
packageVersion('reticulate')
# Then source and run: source('SERDA runner.R')
```

## Evaluation signals

- Lock file (renv.lock or environment.yml) can be parsed without syntax errors and contains no unresolved version specifiers (e.g., no floating-point version constraints like '>= 1.0').
- Installation from lock file on a fresh system produces py_config() and packageVersion() output matching the documented System section exactly (e.g., reticulate 1.19, keras 2.7.0, numpy 1.18.1).
- Cross-language integration verified: reticulate correctly discovers Python 3.6.10 via r-miniconda, and numpy 1.18.1 is accessible from R via reticulate::py_run_string('import numpy; print(numpy.__version__)').
- SERDA runner.R executes without package version conflicts and produces normalization output with identical schema and numeric precision as the validated baseline.
- Lock file contains all transitive dependencies with no gaps; attempting to install one package at a time without the lock file should fail or produce warnings about unmet dependencies.

## Limitations

- Lock files are environment-specific: renv.lock may differ between Windows (x86_64-w64-mingw32), macOS, and Linux due to platform-dependent binary packages and architecture flags. SERDA README documents Windows 10 x64 explicitly; porting to other OS may require regeneration.
- Python 3.6.10 and numpy 1.18.1 are obsolete (end-of-life) as of 2024; security patches and compatibility with modern systems (e.g., M1 Macs, CUDA >11) may not be available. Pinning these old versions ensures reproducibility but sacrifices security and forward compatibility.
- r-miniconda isolation can mask system-level issues (missing system libraries, mismatched BLAS/LAPACK) that may surface when migrating to different hardware or OS distributions.
- No changelog or version history is documented in the SERDA repository, making it difficult to understand why these specific versions were chosen or which versions are known to be broken.

## Evidence

- [readme] R-version-and-packages-specification: "R version 3.6.3 (2020-02-29) Platform: x86_64-w64-mingw32/x64 (64-bit) Running under: Windows 10 x64 (build 19043) Packages: > packageVersion("reticulate") [1] '1.19' > packageVersion("keras") [1]"
- [readme] Python-version-and-numpy-via-py-config: "python:         C:/Users/pcname/AppData/Local/r-miniconda/envs/r-reticulate/python.exe version:        3.6.10 |Anaconda, Inc.| (default, May  7 2020, 19:46:08) [MSC v.1916 64 bit (AMD64)] numpy:"
- [readme] reticulate-as-cross-language-bridge: "[Python Version Configuration](https://rstudio.github.io/reticulate/index.html)"
- [other] lock-file-export-recommendation: "Define the dependency graph and version pinning constraints, noting that reticulate must route to Python 3.6.10 via r-miniconda. Export the environment specification as a reproducible lock file"
