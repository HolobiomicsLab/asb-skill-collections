---
name: virtual-environment-creation
description: Use when before installing ENPKG dependencies for the first time, or
  when setting up the workflow on a new machine or user account. Trigger when you
  have cloned enpkg_full or enpkg_workflow and need to install runtime and optional
  development dependencies in isolation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - uv
  - Anaconda / Miniconda
  - Git
  license_tier: open
derived_from:
- doi: 10.1021/acscentsci.3c00800
  title: enpkg
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enpkg_cq
    doi: 10.1021/acscentsci.3c00800
    title: enpkg
  dedup_kept_from: coll_enpkg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.3c00800
  all_source_dois:
  - 10.1021/acscentsci.3c00800
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# virtual-environment-creation

## Summary

Create an isolated Python virtual environment using uv or conda to manage dependencies and avoid conflicts when installing ENPKG workflow components. This ensures reproducible, project-specific package versions without contaminating the system Python installation.

## When to use

Before installing ENPKG dependencies for the first time, or when setting up the workflow on a new machine or user account. Trigger when you have cloned enpkg_full or enpkg_workflow and need to install runtime and optional development dependencies in isolation.

## When NOT to use

- If the ENPKG workflow is already installed and environment is active (re-activation suffices).
- If you are running via a container (Docker, Singularity) that already provides dependency isolation.
- If system-wide Python package management is enforced by institutional policy and project-level isolation is forbidden.

## Inputs

- Project root directory (enpkg_full or enpkg_workflow cloned repository)
- pyproject.toml or requirements file with pinned dependencies
- System with Git and Anaconda/Miniconda or uv pre-installed

## Outputs

- .venv directory (isolated Python virtual environment)
- Activated shell session with environment variables pointing to .venv/bin
- Installed runtime and optional development packages in .venv/lib/pythonX.Y/site-packages

## How to apply

Use the uv package manager (recommended over conda for ENPKG) to create and sync an isolated .venv in the project root by running `uv sync` to install runtime dependencies, or `uv sync --group dev` to include development tools like pytest and linters. If uv is not installed, first install it via the documented curl command. Optionally specify a Python version (e.g., `uv python install 3.11`) before syncing. Activate the environment with `source .venv/bin/activate` on Linux/macOS or use `uv run` as a prefix to execute commands without manual activation. The rationale is that ENPKG calls multiple external tools (MZmine, Sirius, GraphDB connectors) and requires precise version pinning; isolation prevents dependency conflicts and ensures reproducibility across environments.

## Related tools

- **uv** (Primary dependency manager for creating and syncing isolated Python environment with pinned versions) — https://docs.astral.sh/uv/latest/
- **Anaconda / Miniconda** (Alternative package manager and environment creation tool; prerequisite if uv is not used) — https://docs.anaconda.com/free/anaconda/install/index.html
- **Git** (Required to clone enpkg_full and enpkg_workflow repositories before environment setup) — https://github.com/git-guides/install-git

## Examples

```
curl -LsSf https://astral.sh/uv/install.sh | sh && cd enpkg_full && uv python install 3.11 && uv sync --group dev && source .venv/bin/activate
```

## Evaluation signals

- Verify .venv directory exists in project root and contains bin/, lib/, and include/ subdirectories.
- Confirm environment activation succeeds: `source .venv/bin/activate` returns no errors and shell prompt changes to show (enpkg_full) or similar.
- Run `python --version` and `pip list` within activated environment; verify Python version and installed packages match pyproject.toml or requirements.
- Test environment isolation: `which python` should point to .venv/bin/python, not system Python.
- Run provided validation checks (e.g., `uv run pytest` or test suite commands) to confirm all components are correctly configured.

## Limitations

- uv must be installed separately before running `uv sync`; installation requires curl and internet access.
- The .venv directory is not portable across different OS or CPU architectures; re-sync is needed on new machines.
- Optional development dependencies (pytest, linters) are only installed if `--group dev` is explicitly passed; omitting this flag will not include them.
- Environment variables and machine-specific paths (e.g., PATH_TO_SIRIUS, SIRIUS_USERNAME) are not automatically configured by virtual environment creation; users must separately configure .env file and source it before running workflows.

## Evidence

- [readme] We now rely on uv for dependency management. Install it if needed: "We now rely on [uv](https://docs.astral.sh/uv/latest/) for dependency management. Install it if needed (see the [uv docs](https://docs.astral.sh/uv/latest/#installation) for alternative methods)"
- [readme] uv sync creates a .venv in the project root with dependencies: "With uv installed, sync the project dependencies into an isolated `.venv`"
- [readme] Optional dev dependencies included with --group dev flag: "If you also want the development tooling (pytest, linters, etc.), add the dev dependency group: uv sync --group dev"
- [readme] Activate environment or use uv run prefix: "`uv sync` creates a `.venv` in the project root. Activate it with: source .venv/bin/activate. You can also run commands without activating by prefixing them with `uv run`, e.g.: uv run pytest"
- [readme] Prerequisites include Git and Anaconda or Miniconda: "You will need to have [Git](https://github.com/git-guides/install-git) and [Anaconda](https://docs.anaconda.com/free/anaconda/install/index.html) (or [Miniconda](https://docs.conda.io/en/latest/minico"
