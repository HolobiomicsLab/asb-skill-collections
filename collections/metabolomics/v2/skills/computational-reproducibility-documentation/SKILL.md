---
name: computational-reproducibility-documentation
description: Use when when releasing or archiving a computational workflow (e.g., an R or Python-based normalization pipeline) and you need to ensure that future users or reviewers can re-run the analysis in an identical computational environment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3314
  tools:
  - R
  - reticulate
  - keras
  - pROC
  - caret
  - numpy
  - Python
  - renv
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo13080944
  all_source_dois:
  - 10.3390/metabo13080944
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# computational-reproducibility-documentation

## Summary

Document and lock all computational dependencies (R, Python, packages, versions) required to execute a scientific workflow, enabling future reproducibility across environments. This skill captures the exact software stack at a moment in time and exports it as machine-readable lock files or environment specifications.

## When to use

When releasing or archiving a computational workflow (e.g., an R or Python-based normalization pipeline) and you need to ensure that future users or reviewers can re-run the analysis in an identical computational environment. Specifically trigger this skill when you have a working analysis involving multiple languages (R + Python interop), cross-language package dependencies, or pinned versions that are critical to numerical reproducibility.

## When NOT to use

- Workflow involves only a single language with no cross-language dependencies (consider simpler environment specs instead).
- Dependencies are already locked in a published, immutable artifact (e.g., Docker image, conda-lock file) and no new documentation is required.
- Analysis is exploratory or temporary, with no expectation of future re-execution or archival.

## Inputs

- Running R and Python environments with all packages installed
- Session metadata (R version, platform, running system)
- Package version queries (packageVersion() outputs, pip list, conda list)
- Python configuration discovery (reticulate::py_config() output or equivalent)
- Project source code or analysis script

## Outputs

- renv.lock (R dependency lock file)
- environment.yml or requirements.txt (Conda/pip dependency lock file)
- README or supplementary document listing all tool versions and configurations
- py_config() / py_discover_config() output documenting Python interop setup

## How to apply

First, identify and document the primary language runtime version (e.g., R 3.6.3) and retrieve its system requirements and available package repositories for that release. Second, document any secondary runtime (e.g., Python 3.6.10 via r-miniconda) and its key dependencies (e.g., numpy 1.18.1). Third, enumerate all packages in the primary language with exact version pins, noting which packages bridge to the secondary runtime (e.g., reticulate 1.19 routes R to Python). Fourth, define the complete dependency graph and version pinning constraints, ensuring that cross-language imports are explicitly configured (e.g., reticulate must point to the correct Anaconda environment). Finally, export the environment specification in both a language-native lock file (renv.lock for R, environment.yml for conda/pip for Python) and as human-readable documentation (e.g., README section with packageVersion() outputs and py_config() output) to facilitate transparent communication and automated environment reconstruction.

## Related tools

- **R** (Primary runtime for statistical normalization and machine learning workflows)
- **reticulate** (R package bridging R–Python interoperability and routing to r-miniconda Python environment) — https://rstudio.github.io/reticulate/index.html
- **keras** (Deep learning framework executed via Python backend, pinned to version 2.7.0)
- **pROC** (ROC analysis for classification model evaluation)
- **caret** (Machine learning framework providing training and cross-validation infrastructure)
- **Python** (Secondary runtime managed via r-miniconda, providing numpy and deep learning backends)
- **numpy** (Numerical computing library required by keras and deep learning operations)
- **renv** (R package manager for generating and managing renv.lock dependency lock files)

## Examples

```
# In R: capture and document the exact environment
R> packageVersion('reticulate')
[1] '1.19'
R> py_config()
python: C:/Users/pcname/AppData/Local/r-miniconda/envs/r-reticulate/python.exe
version: 3.6.10 |Anaconda, Inc.| (default, May 7 2020, 19:46:08) [MSC v.1916 64 bit (AMD64)]
numpy_version: 1.18.1
# Then export lock files:
R> renv::snapshot('renv.lock')
```

## Evaluation signals

- All R packages resolve to exact versions matching those in packageVersion() output (e.g., reticulate 1.19, keras 2.7.0, pROC 1.17.0.1, caret 6.0.86).
- Python runtime is correctly configured via reticulate; py_config() output shows Python 3.6.10 from r-miniconda with numpy 1.18.1.
- Lock files (renv.lock, environment.yml) contain no missing or ambiguous version specifications and are machine-readable by renv::renv_restore() or conda env create.
- README or supplementary documentation reproduces the full environment specification and matches the actual py_config() / py_discover_config() outputs from the execution platform.
- A fresh environment reconstructed from lock files produces identical package versions and py_config() output, confirming bit-for-bit reproducibility (or at least functional equivalence).

## Limitations

- Version pinning does not account for breaking changes in upstream dependencies; archived lock files may become obsolete or incompatible with future operating systems (e.g., Windows 10 x64 build 19043 dependencies may not install on newer Windows versions).
- Python versions and conda environments managed via r-miniconda are platform-specific (Windows x64 shown in README) and may not be reproducible on Linux or macOS without additional tooling.
- No changelog or version history provided in the repository, limiting visibility into why specific versions were chosen or how they interact with SERDA normalization algorithm assumptions.
- Documentation does not specify the r-miniconda initialization or activation workflow, potentially causing failures if users do not properly configure reticulate to point to the correct conda environment.

## Evidence

- [intro] SERDA normalization requires R 3.6.3 with packages reticulate 1.19, keras 2.7.0, pROC 1.17.0.1, and caret 6.0.86, integrated with Python 3.6.10 (via r-miniconda) and numpy 1.18.1.: "SERDA normalization requires R 3.6.3 with packages reticulate 1.19, keras 2.7.0, pROC 1.17.0.1, and caret 6.0.86, integrated with Python 3.6.10 (via r-miniconda) and numpy 1.18.1."
- [intro] Define the dependency graph and version pinning constraints, noting that reticulate must route to Python 3.6.10 via r-miniconda.: "Define the dependency graph and version pinning constraints, noting that reticulate must route to Python 3.6.10 via r-miniconda."
- [intro] Export the environment specification as a reproducible lock file (either renv.lock for R or environment.yml for conda/pip).: "Export the environment specification as a reproducible lock file (either renv.lock for R or environment.yml for conda/pip)."
- [readme] R version 3.6.3 (2020-02-29) Platform: x86_64-w64-mingw32/x64 (64-bit) Running under: Windows 10 x64 (build 19043): "R version 3.6.3 (2020-02-29) Platform: x86_64-w64-mingw32/x64 (64-bit) Running under: Windows 10 x64 (build 19043)"
- [readme] version:        3.6.10 |Anaconda, Inc.| (default,  May  7 2020, 19:46:08) [MSC v.1916 64 bit (AMD64)] Architecture:   64bit numpy_version:  1.18.1: "version:        3.6.10 |Anaconda, Inc.| (default,  May  7 2020, 19:46:08) [MSC v.1916 64 bit (AMD64)] Architecture:   64bit numpy_version:  1.18.1"
