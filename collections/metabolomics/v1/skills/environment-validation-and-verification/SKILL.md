---
name: environment-validation-and-verification
description: Use when after installing ENPKG or any component of the workflow via conda/pip dependency manifests and before executing workflow scripts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - ENPKG
  - conda
  - pip
  - uv
  - ENPKG (enpkg_full)
  - Sirius
derived_from:
- doi: 10.1021/acscentsci.3c00800
  title: enpkg
evidence_spans:
- Welcome to the ENPKG Full Workflow!
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enpkg
    doi: 10.1021/acscentsci.3c00800
    title: enpkg
  dedup_kept_from: coll_enpkg
schema_version: 0.2.0
---

# Environment validation and verification

## Summary

Verify that a computational environment (conda/pip, Python packages, external binaries) has been correctly installed and all declared dependencies are present at their specified versions before running a workflow. This skill ensures reproducibility and prevents runtime failures due to missing or mismatched package versions.

## When to use

After installing ENPKG or any component of the workflow via conda/pip dependency manifests and before executing workflow scripts. Apply this skill when you have just cloned a repository, created a fresh conda environment, or need to confirm that all runtime dependencies (including the Sirius binary) are correctly available at the versions declared in environment.yml, requirements.txt, or pyproject.toml.

## When NOT to use

- Environment is already running the workflow without errors — validation is only necessary after fresh installation or environment changes.
- You are updating a single package within an already-validated environment and have verified compatibility separately.
- The workflow is running in a containerized system (Docker/Singularity) where the environment is immutable and pre-tested.

## Inputs

- conda environment specification file (environment.yml)
- pip requirements file (requirements.txt or pyproject.toml)
- .env file containing paths to external binaries (e.g., PATH_TO_SIRIUS)
- activated conda/virtual environment

## Outputs

- validation report (pass/fail per package and binary check)
- console output from conda list and pip show commands
- successful import of core ENPKG modules
- confirmation that external binaries (Sirius, etc.) are callable

## How to apply

First, check the conda environment specification file (environment.yml or requirements.txt) at the repository root or in setup documentation to identify declared dependency versions. Second, activate the target conda/virtual environment. Third, run `conda list` and `pip show <package_name>` for each critical package to confirm installation and version match the manifest. Fourth, run a lightweight diagnostic script or test import that exercises core modules (e.g., importing ENPKG submodules, checking that Sirius binary is callable via the PATH_TO_SIRIUS environment variable stored in .env). Fifth, verify that external binaries required by the workflow (such as the Sirius executable at the path specified in .env) are executable and respond to a version check. Success is indicated when all declared packages appear at correct pinned versions and core imports complete without error.

## Related tools

- **conda** (Create and manage isolated Python environments; parse and apply environment specification files (environment.yml) to install pinned dependency versions.) — https://docs.anaconda.com/free/anaconda/install/index.html
- **pip** (Install and verify Python package versions within the activated conda environment using `pip show` to confirm installed versions match declared specifications.)
- **uv** (Modern dependency manager for ENPKG full workflow; replaces conda/pip for syncing project dependencies and creating isolated .venv environments with version pinning.) — https://docs.astral.sh/uv/latest/
- **ENPKG (enpkg_full)** (The target workflow framework whose core modules are imported during validation; environment must support all declared submodules and dependencies.) — https://github.com/enpkg/enpkg_full
- **Sirius** (External binary required by ENPKG for compound annotation (SIRIUS/CSI:FingerID/CANOPUS); validation must confirm the executable at PATH_TO_SIRIUS is present and callable.) — https://boecker-lab.github.io/docs.sirius.github.io/install/

## Examples

```
conda activate enpkg_env && conda list && pip show enpkg && python -c 'import enpkg; print("ENPKG imported successfully")' && $PATH_TO_SIRIUS --version
```

## Evaluation signals

- All packages listed in `conda list` match the versions and packages declared in environment.yml or requirements.txt with no version mismatches or missing packages.
- `pip show <package>` returns version and location for each critical Python package without errors.
- Import statements for core ENPKG modules (e.g., `import enpkg` or submodule imports) execute without ImportError, ModuleNotFoundError, or version conflict warnings.
- External binary check succeeds: `$PATH_TO_SIRIUS --version` or equivalent returns the installed Sirius version without 'command not found' or permission errors.
- Test diagnostic script or lightweight workflow invocation completes without dependency-related runtime errors (e.g., AttributeError, ImportError, or missing module warnings).

## Limitations

- Validation does not detect transitive dependency conflicts or version incompatibilities that only arise at runtime during complex operations; a successful import test may not guarantee full workflow stability.
- External binary validation (e.g., Sirius version check) depends on the binary being in PATH or the environment variable PATH_TO_SIRIUS being correctly set in .env; misconfiguration of .env will cause validation to fail even if the binary is installed.
- Platform-specific dependencies (e.g., shared libraries, system packages) are not checked by `conda list` or `pip show`; validation is limited to Python and explicitly declared conda packages.
- No changelog is provided in the repository, so version pinning information may become outdated if dependencies are updated without documentation of breaking changes.

## Evidence

- [other] Verify environment integrity by checking that all declared packages are installed at the correct versions using conda list and pip show.: "Verify environment integrity by checking that all declared packages are installed at the correct versions using conda list and pip show."
- [other] Validate the environment by running a lightweight test import or diagnostic script that exercises core ENPKG modules.: "Validate the environment by running a lightweight test import or diagnostic script that exercises core ENPKG modules."
- [readme] With uv installed, sync the project dependencies into an isolated `.venv`... install runtime dependencies and create .venv: "With uv installed, sync the project dependencies into an isolated `.venv`"
- [readme] identify the full path to the `sirius` binary... and store it in `.env` as `PATH_TO_SIRIUS`. The workflow reads that variable when launching Sirius.: "identify the full path to the `sirius` binary... and store it in `.env` as `PATH_TO_SIRIUS`. The workflow reads that variable when launching Sirius."
- [readme] Runtime secrets and machine-specific paths (e.g., `PATH_TO_SIRIUS`, `SIRIUS_USERNAME`, `SIRIUS_PASSWORD`) live in a `.env` file that is ignored by git.: "Runtime secrets and machine-specific paths (e.g., `PATH_TO_SIRIUS`, `SIRIUS_USERNAME`, `SIRIUS_PASSWORD`) live in a `.env` file that is ignored by git."
