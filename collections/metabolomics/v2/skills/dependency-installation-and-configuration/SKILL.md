---
name: dependency-installation-and-configuration
description: Use when when setting up a fresh clone of the ENPKG workflow repository or when onboarding to a new machine. Use this skill before attempting to run any workflow stages (data organization, taxonomical enhancement, MN generation, SIRIUS annotation, or graph building).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - uv
  - Sirius
  - Anaconda / Miniconda
  - Git
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Dependency Installation and Configuration

## Summary

Install and configure Python runtime dependencies and external tools (e.g., Sirius, MZmine) required to execute the ENPKG computational workflow. This skill ensures all project dependencies are isolated in a managed virtual environment and all machine-specific paths and credentials are correctly configured before workflow execution.

## When to use

When setting up a fresh clone of the ENPKG workflow repository or when onboarding to a new machine. Use this skill before attempting to run any workflow stages (data organization, taxonomical enhancement, MN generation, SIRIUS annotation, or graph building). Indicated when you have cloned the repository but have not yet verified that all dependencies are installed and environment variables are set.

## When NOT to use

- When the virtual environment is already activated and all external tools (Sirius, MZmine) are already installed and verified to work; re-running installation will be redundant.
- When you do not have system-level permissions to install Git, Anaconda/Miniconda, or to write to the .venv directory; work with your system administrator first.
- When the ENPKG workflow is being run within a pre-built Docker container or managed cloud environment that already includes all dependencies; skip manual setup and proceed directly to parameter configuration and workflow launch.

## Inputs

- Git repository clone (enpkg/enpkg_full directory)
- .env.example template file
- System package manager (apt, brew, etc.) with Git and Anaconda/Miniconda pre-installed
- Internet access for downloading dependencies and external tools

## Outputs

- Isolated Python virtual environment (.venv) with all runtime dependencies installed
- Installed Sirius binary at user-specified <install_dir>
- Configured .env file with populated PATH_TO_SIRIUS, SIRIUS_USERNAME, SIRIUS_PASSWORD, and other machine-specific variables
- Verified shell environment with .env variables loaded and accessible to subprocess calls

## How to apply

First, install the uv package manager (a modern Python dependency resolver), then use `uv sync` to install Python runtime dependencies into an isolated `.venv` virtual environment in the project root. Optionally add the dev dependency group with `uv sync --group dev` if development tools (pytest, linters) are needed. Next, install external tools: run `src/install_sirius.sh <install_dir>` to download and unpack the Sirius binary for your platform, recording the full path to the executable. Create a `.env` file by copying `.env.example` and populate machine-specific secrets and paths (e.g., `PATH_TO_SIRIUS`, `SIRIUS_USERNAME`, `SIRIUS_PASSWORD`), then load it into your shell session with `set -a; source .env; set +a` before launching the workflow. Finally, verify installation by activating the environment (`source .venv/bin/activate`) or running `uv run pytest` to confirm all components are correctly configured.

## Related tools

- **uv** (Python dependency resolver and virtual environment manager; used to install all runtime Python packages into an isolated .venv) — https://docs.astral.sh/uv/latest/
- **Sirius** (External tool for molecular formula prediction and CSI:FingerID annotation; installed via install_sirius.sh script and referenced via PATH_TO_SIRIUS environment variable) — https://boecker-lab.github.io/docs.sirius.github.io/install/
- **Anaconda / Miniconda** (System-level package manager prerequisite for managing non-Python dependencies; mentioned as alternative to uv for environment setup) — https://docs.anaconda.com/free/anaconda/install/index.html
- **Git** (Version control system used to clone the enpkg/enpkg_full repository to the local machine) — https://github.com/git-guides/install-git

## Examples

```
curl -LsSf https://astral.sh/uv/install.sh | sh && cd enpkg_full && uv sync && uv python install 3.11 && bash src/install_sirius.sh /opt/sirius && cp .env.example .env && set -a && source .env && set +a && uv run pytest
```

## Evaluation signals

- Virtual environment `.venv/bin/activate` exists and successfully activates without errors; `which python` returns a path inside `.venv`.
- Running `uv run pytest` or `pytest` (after activation) executes without ImportError or missing-module exceptions, indicating all Python dependencies are installed.
- Sirius binary is present at the path specified in `.env` (e.g., `ls /opt/sirius/sirius/bin/sirius` on Linux returns success); `$PATH_TO_SIRIUS --version` returns the installed version number.
- Environment variables from `.env` are loaded into the shell session; `echo $PATH_TO_SIRIUS` and `echo $SIRIUS_USERNAME` return non-empty values after `source .env`.
- Attempting to import core ENPKG Python modules (e.g., `python -c 'import enpkg'` or equivalent) completes without ModuleNotFoundError.

## Limitations

- Installation is OS/CPU-specific: the `install_sirius.sh` script auto-detects the platform but may fail on unsupported architectures; users must manually override OS/CPU flags if needed.
- The `.env` file is ignored by git and must be created and populated manually; no template substitution is automated, so typos in `PATH_TO_SIRIUS` or credentials will cause runtime failures later.
- Sirius requires valid credentials (username/password) to function; users without a Sirius account must register separately, and the workflow will fail silently if credentials are incorrect or missing.
- Virtual environment isolation is broken if the system Python is removed or major version is upgraded after installation; users must re-run `uv sync` if system Python changes.
- No changelog is provided in the repository, so users cannot easily identify breaking changes in dependency versions when upgrading between ENPKG releases.

## Evidence

- [readme] This guide will walk you through the installation, setup, and execution of the ENPKG full workflow.: "This guide will walk you through the installation, setup, and execution of the ENPKG full workflow"
- [readme] We now rely on uv for dependency management. Install it if needed (see the uv docs for alternative methods): curl -LsSf https://astral.sh/uv/install.sh | sh: "We now rely on uv for dependency management. Install it if needed"
- [readme] With uv installed, sync the project dependencies into an isolated `.venv`: # install runtime dependencies and create .venv uv sync: "sync the project dependencies into an isolated `.venv`"
- [readme] If you also want the development tooling (pytest, linters, etc.), add the dev dependency group: uv sync --group dev: "If you also want the development tooling (pytest, linters, etc.), add the dev dependency group"
- [readme] Run `src/install_sirius.sh <install_dir>` to download and unpack the latest release for your platform, e.g.: bash src/install_sirius.sh /opt/sirius: "Run `src/install_sirius.sh <install_dir>` to download and unpack the latest release for your platform"
- [readme] The script auto-detects the OS/CPU, but you can override them (e.g. `macos x64`) if needed. After installation, identify the full path to the `sirius` binary and store it in `.env` as `PATH_TO_SIRIUS`.: "identify the full path to the `sirius` binary (`/opt/sirius/sirius/bin/sirius` on Linux, `/opt/sirius/sirius.app/Contents/MacOS/sirius` on macOS, etc.) and store it in `.env` as `PATH_TO_SIRIUS`"
- [readme] Runtime secrets and machine-specific paths (e.g., `PATH_TO_SIRIUS`, `SIRIUS_USERNAME`, `SIRIUS_PASSWORD`) live in a `.env` file that is ignored by git.: "Runtime secrets and machine-specific paths (e.g., `PATH_TO_SIRIUS`, `SIRIUS_USERNAME`, `SIRIUS_PASSWORD`) live in a `.env` file that is ignored by git"
- [readme] Because `.env` is ignored by git, you can safely customize it without leaking credentials.: "Because `.env` is ignored by git, you can safely customize it without leaking credentials"
- [readme] Before running the workflow, load the file into your shell session: set -a; source .env; set +a: "Before running the workflow, load the file into your shell session"
- [readme] You will need to have Git and Anaconda (or Miniconda) installed.: "You will need to have Git and Anaconda (or Miniconda) installed"
