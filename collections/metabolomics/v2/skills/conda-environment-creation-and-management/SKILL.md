---
name: conda-environment-creation-and-management
description: Use when when setting up a new computational workflow (e.g., ENPKG) that depends on pinned versions of Python packages and system libraries, or when collaborating across machines where package availability or versions may differ.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - ENPKG
  - uv
  - conda
  - pip
  - Miniconda
derived_from:
- doi: 10.1021/acscentsci.3c00800
  title: enpkg
evidence_spans:
- Welcome to the ENPKG Full Workflow!
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enpkg
    doi: 10.1021/acscentsci.3c00800
    title: enpkg
  dedup_kept_from: coll_enpkg
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.3c00800
  all_source_dois:
  - 10.1021/acscentsci.3c00800
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# conda-environment-creation-and-management

## Summary

Create and validate isolated conda environments from dependency manifests to ensure reproducible, version-pinned execution of complex multi-tool workflows like ENPKG. This skill isolates runtime dependencies and prevents library conflicts across system Python installations.

## When to use

When setting up a new computational workflow (e.g., ENPKG) that depends on pinned versions of Python packages and system libraries, or when collaborating across machines where package availability or versions may differ. Apply this skill before running any workflow steps that depend on conda-managed tools.

## When NOT to use

- The target system already has all required packages globally installed and tested—isolation adds no value and may slow startup.
- The workflow has no published dependency manifest or pinned versions—manual dependency hunting is required before environment creation is possible.
- You are running a single lightweight script with no external dependencies beyond standard library—conda overhead is unnecessary.

## Inputs

- Repository root directory containing environment.yml, pyproject.toml, or requirements.txt
- Pinned dependency manifest (YAML, TOML, or text format)
- Target Python version specification (optional; uv can install via uv python install 3.11)

## Outputs

- Isolated conda/venv environment in .venv or named conda environment
- Environment verification report (conda list output or pip show checksums)
- Successful import or diagnostic test results confirming module availability

## How to apply

Clone the target workflow repository (e.g., enpkg/enpkg_full). Locate the dependency specification file at the repository root (environment.yml, pyproject.toml, or uv.lock). Use the modern uv package manager or classical conda/pip toolchain to create a fresh isolated environment from the manifest, which pins all transitive dependencies to ensure reproducibility. After environment creation, verify integrity by listing installed packages and versions (conda list, pip show, or uv pip freeze), then validate by importing core modules or running lightweight diagnostic tests. If using uv, activate the generated .venv or prefix commands with uv run to execute within the environment.

## Related tools

- **uv** (Modern Python package and dependency manager; used to install runtime and dev dependencies and create isolated .venv environments with locked transitive dependency versions.) — https://docs.astral.sh/uv/latest/
- **conda** (Alternative package manager for creating isolated environments from environment.yml specifications; used in workflows that predate uv adoption.) — https://docs.anaconda.com/free/anaconda/install/index.html
- **pip** (Python package installer; used within conda environments to install packages not available via conda or to supplement conda dependency resolution.)
- **Miniconda** (Lightweight conda distribution; alternative to full Anaconda for managing conda environments.) — https://docs.conda.io/en/latest/miniconda.html

## Examples

```
cd enpkg_full && curl -LsSf https://astral.sh/uv/install.sh | sh && uv python install 3.11 && uv sync && source .venv/bin/activate && python -c 'import enpkg; print(enpkg.__version__)'
```

## Evaluation signals

- All packages listed in dependency manifest appear in conda list / uv pip freeze output at declared versions.
- Diagnostic import test executes without ImportError or version mismatch warnings (e.g., `python -c 'import enpkg; print(enpkg.__version__)'`).
- Environment-specific package paths (conda list --json or .venv/lib/pythonX.Y/site-packages) confirm isolation from system Python.
- Pinned transitive dependencies (e.g., from uv.lock or conda-lock.yml) are consistent across runs; re-creating the environment yields identical package set.
- Optional: Run workflow test step (e.g., ENPKG's 00_workflow_all.sh on test dataset) completes without import or version resolution errors.

## Limitations

- uv requires explicit Python version installation via uv python install if the target version is not already available; this adds a one-time download (~100 MB).
- Platform-specific binary packages (e.g., SIRIUS) must be installed separately outside the conda/uv environment and linked via environment variables (PATH_TO_SIRIUS); conda environment creation alone does not handle compiled native tools.
- Dependency manifests must be manually maintained and version-pinned upstream; out-of-date or conflict-ridden manifests will cause environment creation to fail or produce incompatible combinations.
- Large environments (e.g., ENPKG with SIRIUS + metabolomics tools) can require 5–10 GB disk space and 10+ minutes to resolve and install transitive dependencies.

## Evidence

- [readme] We now rely on uv for dependency management. Install it if needed, then sync the project dependencies into an isolated .venv with uv sync.: "We now rely on [uv](https://docs.astral.sh/uv/latest/) for dependency management. Install it if needed (see the [uv docs](https://docs.astral.sh/uv/latest/#installation) for alternative"
- [other] Verify environment integrity by checking that all declared packages are installed at the correct versions using conda list and pip show.: "Verify environment integrity by checking that all declared packages are installed at the correct versions using conda list and pip show."
- [readme] You will need to have Git and Anaconda (or Miniconda) installed as prerequisites for the ENPKG workflow.: "You will need to have [Git](https://github.com/git-guides/install-git) and [Anaconda](https://docs.anaconda.com/free/anaconda/install/index.html) (or [Miniconda](https://docs.conda.io/en/latest/minico"
- [other] Clone the repository and locate the dependency specification file at the repository root or setup documentation.: "Locate and parse the conda environment specification file (environment.yml or requirements.txt) at the repository root or setup documentation."
- [readme] If you also want development tools (pytest, linters), add the dev dependency group with uv sync --group dev.: "If you also want the development tooling (pytest, linters, etc.), add the dev dependency group:

```bash
uv sync --group dev
```"
