---
name: r-environment-dependency-specification
description: Use when when developing or reproducing an R-based analysis that integrates Python dependencies (e.g., via reticulate), particularly in contexts where deep learning (keras) or complex machine-learning frameworks (caret) depend on specific numpy versions or Python minor releases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3577
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3361
  tools:
  - R
  - reticulate
  - keras
  - pROC
  - caret
  - numpy
  - renv
  - conda / r-miniconda
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

# R environment dependency specification

## Summary

Document and pin exact versions of R, Python, and interdependent packages (especially those bridging R–Python interoperability) to ensure reproducible execution of cross-language scientific workflows. This skill is critical when R code calls Python libraries through reticulate, as version mismatches between R packages, Python interpreters, and compiled dependencies can silently break normalization or machine-learning pipelines.

## When to use

When developing or reproducing an R-based analysis that integrates Python dependencies (e.g., via reticulate), particularly in contexts where deep learning (keras) or complex machine-learning frameworks (caret) depend on specific numpy versions or Python minor releases. Apply this skill before committing code or sharing environments, and whenever downstream users report 'works on my machine' failures.

## When NOT to use

- Input is a pure R workflow with no Python dependencies — use standard R dependency management (renv or packrat) instead.
- Python environment is already containerized (e.g., Docker image with pinned dependencies) — leverage container rather than re-specifying in renv/conda syntax.
- Development environment is ephemeral or one-off; reproducibility is not a priority and users accept 'latest available' versions.

## Inputs

- Session metadata (R version, platform, system configuration)
- R package versions (from packageVersion() calls or DESCRIPTION files)
- Python configuration output (from py_config() and py_discover_config())
- Package dependency trees and version constraints

## Outputs

- renv.lock file (R package snapshot with resolved versions and hashes)
- environment.yml file (conda-compatible Python environment specification)
- Documented dependency graph (version pinning constraints, interdependencies)
- Reproducible environment specification artifact (for version control and sharing)

## How to apply

1. Capture the R version (e.g., R 3.6.3) and retrieve its release date and available package repositories. 2. Document the Python interpreter location, version (e.g., Python 3.6.10 via r-miniconda), and base-level packages like numpy (e.g., 1.18.1). 3. Enumerate all R packages with pinned versions, noting which ones bridge to Python (reticulate 1.19) and which depend on the Python backend (keras 2.7.0). 4. Explicitly specify the reticulate routing mechanism (e.g., via r-miniconda managed by R) to guarantee Python 3.6.10 is invoked, not a system Python. 5. Build a dependency graph documenting constraints (e.g., keras 2.7.0 requires numpy ≥ 1.16, caret 6.0.86 requires R ≥ 3.5). 6. Export to a machine-readable lock file (renv.lock for R package snapshots, environment.yml for conda/pip specifications) to enable one-command environment reconstruction.

## Related tools

- **reticulate** (R–Python bridge; routes R code to specified Python interpreter (e.g., r-miniconda) and manages session state) — https://rstudio.github.io/reticulate/index.html
- **renv** (R package version management; generates and restores renv.lock snapshots of all R dependencies)
- **conda / r-miniconda** (Supplies isolated Python interpreter (e.g., Python 3.6.10) and base packages (numpy 1.18.1); managed by R via reticulate)
- **keras** (Deep-learning backend in R; depends on Python 3.6.10 and numpy 1.18.1 via reticulate)
- **caret** (Machine-learning framework in R; version 6.0.86 pinned to R 3.6.3 compatibility)
- **pROC** (ROC curve and AUC analysis in R; included in environment snapshot)

## Examples

```
renv::snapshot(lockfile='renv.lock'); # in R session with all dependencies loaded. Then: renv::restore() # in fresh environment to reproduce.
```

## Evaluation signals

- renv.lock or environment.yml file is syntactically valid and contains all declared packages with exact version strings.
- Reconstruction step (renv::restore() or conda env create) completes without version conflicts or dependency resolution failures.
- py_config() and packageVersion() calls in a fresh environment reproduce the exact same versions (R 3.6.3, Python 3.6.10, numpy 1.18.1, keras 2.7.0, reticulate 1.19, pROC 1.17.0.1, caret 6.0.86).
- Cross-language interop test (e.g., calling keras or numpy from R via reticulate) executes without import errors or version mismatch warnings.
- Lock file is checked into version control and documented in README with reproduction instructions (e.g., 'Run renv::restore() to install all dependencies').

## Limitations

- Version pinning is OS-specific (e.g., Windows x86_64 binaries differ from Linux); specify platform in lock file or document platform-specific variants.
- r-miniconda paths are user-machine-dependent (e.g., C:/Users/pcname/AppData/Local/...); relative paths or environment variable substitution needed for portability.
- Archived R versions (e.g., R 3.6.3 from 2020) and Python 3.6 (EOL Jan 2021) may have limited package repository mirrors; verify repository availability before long-term archival.
- Dynamic Python package dependencies (e.g., packages installed via pip inside R) are not captured in renv.lock alone; requires complementary pip freeze or environment.yml for complete snapshot.
- No changelog or migration path provided in the repository; pin versions conservatively and test upgrades in isolation before applying to production workflows.

## Evidence

- [other] SERDA normalization requires R 3.6.3 with packages reticulate 1.19, keras 2.7.0, pROC 1.17.0.1, and caret 6.0.86, integrated with Python 3.6.10 (via r-miniconda) and numpy 1.18.1.: "SERDA normalization requires R 3.6.3 with packages reticulate 1.19, keras 2.7.0, pROC 1.17.0.1, and caret 6.0.86, integrated with Python 3.6.10 (via r-miniconda) and numpy 1.18.1."
- [other] Export the environment specification as a reproducible lock file (either renv.lock for R or environment.yml for conda/pip).: "Export the environment specification as a reproducible lock file (either renv.lock for R or environment.yml for conda/pip)."
- [readme] R version 3.6.3 (2020-02-29) Platform: x86_64-w64-mingw32/x64 (64-bit): "R version 3.6.3 (2020-02-29) Platform: x86_64-w64-mingw32/x64 (64-bit)"
- [readme] python:         C:/Users/pcname/AppData/Local/r-miniconda/envs/r-reticulate/python.exe version:        3.6.10 |Anaconda, Inc.| (default, May  7 2020, 19:46:08) [MSC v.1916 64 bit (AMD64)] numpy_version:  1.18.1: "python:         C:/Users/pcname/AppData/Local/r-miniconda/envs/r-reticulate/python.exe version:        3.6.10 |Anaconda, Inc.| (default, May  7 2020, 19:46:08) [MSC v.1916 64 bit (AMD64)]"
- [other] reticulate must route to Python 3.6.10 via r-miniconda.: "reticulate must route to Python 3.6.10 via r-miniconda."
