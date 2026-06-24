---
name: python-conda-environment-management
description: Use when when setting up a multi-language data analysis pipeline that
  requires both R and Python components to coexist with exact version constraints,
  especially when deep learning (keras) and machine learning (caret, pROC) packages
  must share a common Python backend.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - R
  - reticulate
  - keras
  - pROC
  - caret
  - Python
  - numpy
  - r-miniconda
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo13080944
  title: SERDA
evidence_spans:
- R version 3.6.3 (2020-02-29)
- packageVersion("reticulate") [1] ‘1.19’
- packageVersion("keras") [1] ‘2.7.0’
- packageVersion("pROC") [1] ‘1.17.0.1’
- packageVersion("caret") [1] ‘6.0.86’
- 'version: 3.6.10 |Anaconda, Inc.| (default, May 7 2020, 19:46:08)'
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo13080944
  all_source_dois:
  - 10.3390/metabo13080944
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# python-conda-environment-management

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Establish and document a reproducible Python environment pinned to specific versions (Python 3.6.10, numpy 1.18.1) via r-miniconda, integrated with R via reticulate for cross-language interoperability in SERDA normalization workflows. This skill ensures that deep learning (keras), statistical analysis (pROC, caret), and numerical computation dependencies are locked and portable.

## When to use

When setting up a multi-language data analysis pipeline that requires both R and Python components to coexist with exact version constraints, especially when deep learning (keras) and machine learning (caret, pROC) packages must share a common Python backend. Specifically applicable when reproducing SERDA normalization or similar R-Python hybrid workflows where version mismatches cause keras or numpy interoperability failures.

## When NOT to use

- When using modern Python (≥3.8) or R versions; this skill is locked to legacy stacks (R 3.6.3, Python 3.6.10) and should not be applied to current-generation analyses.
- When R and Python components are deployed separately with no cross-language calls; conda environment management is overhead-heavy for monolingual pipelines.
- When a container (Docker/Singularity) is already the reproducibility vehicle; lock files are redundant if the image is versioned and archived.

## Inputs

- R 3.6.3 installation with package management capability
- System access to conda/Anaconda repository for Python 3.6.10
- List of required R packages (reticulate, keras, pROC, caret) and Python dependencies (numpy 1.18.1)

## Outputs

- Reproducible lock file (environment.yml or renv.lock) with version pinning
- Configured r-miniconda environment with Python 3.6.10 and numpy 1.18.1
- Verified R environment with reticulate bridging to Python backend
- py_config() and py_discover_config() output confirming interoperability

## How to apply

1. Install r-miniconda and configure a dedicated conda environment pinned to Python 3.6.10 (Anaconda distribution) with numpy 1.18.1. 2. In R 3.6.3, install reticulate 1.19 and configure it to point to the r-miniconda Python environment via py_config() and py_discover_config() verification. 3. Install keras 2.7.0 (which routes through the Python backend), pROC 1.17.0.1, and caret 6.0.86 in R, ensuring reticulate bridges all Python dependencies. 4. Build a lock file (environment.yml for conda or renv.lock for R) that captures the complete dependency graph including version pins and the r-miniconda path constraint. 5. Validate the environment by executing py_config() in R and confirming the numpy path and version match the conda environment specification.

## Related tools

- **reticulate** (R–Python interoperability bridge; routes keras, numpy, and other Python packages into R environments) — https://rstudio.github.io/reticulate/index.html
- **r-miniconda** (Anaconda-based Python distribution manager; provides isolated conda environment with Python 3.6.10 and numpy 1.18.1)
- **keras** (Deep learning backend for SERDA normalization; accessed via reticulate from R)
- **caret** (Machine learning framework in R; integrates with keras via reticulate for model training and evaluation)
- **pROC** (ROC curve analysis and AUC computation in R; used for classifier performance evaluation in SERDA workflow)
- **numpy** (Numerical array backend; version 1.18.1 pinned for compatibility with Python 3.6.10 and keras 2.7.0)

## Examples

```
# In R: Rscript -e "library(reticulate); py_config(); packageVersion('keras'); packageVersion('caret'); packageVersion('pROC')"
```

## Evaluation signals

- py_config() output confirms libpython path points to r-miniconda environment and numpy_version is exactly 1.18.1
- py_discover_config() returns identical Python configuration to py_config(), indicating consistent discovery
- packageVersion() in R returns reticulate='1.19', keras='2.7.0', pROC='1.17.0.1', caret='6.0.86' without version conflicts
- Lock file (environment.yml or renv.lock) contains all pinned versions and can reproduce identical environment on clean system without version resolution errors
- SERDA runner.R executes without Python ImportError, version mismatch, or reticulate bridging failures when data_file is set and script is sourced

## Limitations

- Python 3.6.10 and R 3.6.3 are end-of-life; security patches and dependency updates are unavailable. This skill is suitable only for reproducing archived analyses, not new development.
- Windows-specific configuration shown in README (x86_64-w64-mingw32 platform); Linux/macOS paths to r-miniconda may differ and require manual adjustment.
- No changelog documented in the repository, so breaking changes in upstream packages (numpy, keras) are not tracked; environment may degrade if r-miniconda or conda channels rebuild old package versions with incompatible dependencies.
- keras 2.7.0 with Python 3.6 has known compatibility issues with modern TensorFlow backends; recommend validating model training before production use.

## Evidence

- [other] SERDA normalization requires R 3.6.3 with packages reticulate 1.19, keras 2.7.0, pROC 1.17.0.1, and caret 6.0.86, integrated with Python 3.6.10 (via r-miniconda) and numpy 1.18.1.: "SERDA normalization requires R 3.6.3 with packages reticulate 1.19, keras 2.7.0, pROC 1.17.0.1, and caret 6.0.86, integrated with Python 3.6.10 (via r-miniconda) and numpy 1.18.1."
- [other] Define the dependency graph and version pinning constraints, noting that reticulate must route to Python 3.6.10 via r-miniconda.: "Define the dependency graph and version pinning constraints, noting that reticulate must route to Python 3.6.10 via r-miniconda."
- [other] Export the environment specification as a reproducible lock file (either renv.lock for R or environment.yml for conda/pip).: "Export the environment specification as a reproducible lock file (either renv.lock for R or environment.yml for conda/pip)."
- [readme] R version 3.6.3 (2020-02-29) Platform: x86_64-w64-mingw32/x64 (64-bit) Running under: Windows 10 x64 (build 19043): "R version 3.6.3 (2020-02-29)
Platform: x86_64-w64-mingw32/x64 (64-bit)
Running under: Windows 10 x64 (build 19043)"
- [readme] version:        3.6.10 |Anaconda, Inc.| (default,  May  7 2020, 19:46:08) [MSC v.1916 64 bit (AMD64)]: "version:        3.6.10 |Anaconda, Inc.| (default,  May  7 2020, 19:46:08) [MSC v.1916 64 bit (AMD64)]"
- [readme] pythonhome:     C:/Users/pcname/AppData/Local/r-miniconda/envs/r-reticulate numpy_version:  1.18.1: "pythonhome:     C:/Users/pcname/AppData/Local/r-miniconda/envs/r-reticulate numpy_version:  1.18.1"
