---
name: repository-environment-setup
description: Use when when you have received a GitHub repository URL for a computational
  workflow (e.g., ENPKG full workflow) and need to prepare your local machine to execute
  the workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - git
  - uv
  - Anaconda or Miniconda
  - Sirius
  techniques:
  - mass-spectrometry
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

# Repository Environment Setup

## Summary

Initialize and configure a computational workflow repository by cloning source code, installing a modern dependency manager (uv), resolving Python and package dependencies into an isolated virtual environment, and validating the setup with test commands. This skill ensures reproducible execution of multi-tool scientific pipelines across different machines and operating systems.

## When to use

When you have received a GitHub repository URL for a computational workflow (e.g., ENPKG full workflow) and need to prepare your local machine to execute the workflow. Apply this skill at the start of any new analysis session, when onboarding to a new machine, or when the workflow's dependency specifications have been updated.

## When NOT to use

- The workflow is already fully installed and validated on your machine in a previous session.
- You are running the workflow in a containerized environment (Docker/Singularity) where dependencies are pre-packaged.
- You only need to read or inspect the workflow source code without executing it.

## Inputs

- GitHub repository URL (e.g., https://github.com/enpkg/enpkg_full)
- README or setup documentation file
- .env.example template (if present in repository)
- Project dependency specification file (pyproject.toml or equivalent for uv)

## Outputs

- Cloned local repository directory
- Isolated Python virtual environment (.venv)
- Configured .env file with machine-specific paths and credentials
- Validated environment with all dependencies installed and verified

## How to apply

Begin by cloning the repository from GitHub to a local directory using git. Review the README for runtime dependencies and tool requirements (e.g., external binaries like Sirius). Use the project's declared dependency manager (uv) to install Python and all package dependencies into an isolated .venv directory, which prevents conflicts with system packages. Activate the virtual environment or use uv run to execute commands. Configure machine-specific settings (e.g., PATH_TO_SIRIUS, credentials) in a .env file by copying the .env.example template and editing with absolute paths and authentication tokens. Load the .env variables into your shell session before executing the workflow. Validate the setup by running provided test commands (e.g., pytest) or by invoking a small test dataset to confirm all components are correctly installed and accessible.

## Related tools

- **git** (Version control system used to clone the repository to local machine) — https://github.com/git-guides/install-git
- **uv** (Fast Python package installer and dependency resolver; replaces pip/conda for this workflow) — https://docs.astral.sh/uv/latest/
- **Anaconda or Miniconda** (Alternative Python distribution manager; listed as prerequisite if uv not available) — https://docs.anaconda.com/free/anaconda/install/index.html
- **Sirius** (External mass spectrometry annotation tool; installed separately via install_sirius.sh script) — https://boecker-lab.github.io/docs.sirius.github.io/install/

## Examples

```
git clone https://github.com/enpkg/enpkg_full.git && cd enpkg_full && uv sync && cp .env.example .env && echo 'Edit .env with PATH_TO_SIRIUS and credentials, then:' && set -a && source .env && set +a && uv run pytest
```

## Evaluation signals

- Virtual environment (.venv) is created and contains a complete Python installation with all transitive dependencies listed in pyproject.toml.
- All import statements in the workflow (e.g., pytest, workflow modules) resolve without ImportError when the environment is activated.
- The .env file contains non-empty values for all required machine-specific variables (PATH_TO_SIRIUS, SIRIUS_USERNAME, SIRIUS_PASSWORD) without syntax errors.
- Running uv sync --group dev completes without errors and all development tools (pytest, linters) are available.
- A provided test command (e.g., uv run pytest or sh workflow/00_workflow_all.sh on a small test dataset) executes without dependency-related failures.
- External binary (Sirius) is correctly located at the path specified in .env and returns a version string when called.

## Limitations

- The setup procedure assumes Git and a Python runtime (3.11 or later) are already installed on the host machine; it does not provide system-level package installation.
- Machine-specific paths (PATH_TO_SIRIUS, database credentials) must be manually configured in .env; this introduces the risk of typos or stale credentials if not kept in sync with actual system configuration.
- The .env file must be kept synchronized with the actual environment; if Sirius is reinstalled or credentials change, the .env file will become invalid.
- No changelog is provided in the repository, so breaking changes in dependencies or the workflow may not be immediately visible to users upgrading between versions.

## Evidence

- [readme] First, clone the repository to your local machine: ```bash git clone https://github.com/enpkg/enpkg_full.git ```: "First, clone the repository to your local machine: ```bash git clone https://github.com/enpkg/enpkg_full.git ```"
- [readme] We now rely on uv for dependency management. Install it if needed (see the uv docs for alternative methods): "We now rely on uv for dependency management. Install it if needed"
- [readme] With uv installed, sync the project dependencies into an isolated `.venv`: uv sync: "With uv installed, sync the project dependencies into an isolated `.venv`"
- [readme] Runtime secrets and machine-specific paths (e.g., `PATH_TO_SIRIUS`, `SIRIUS_USERNAME`, `SIRIUS_PASSWORD`) live in a `.env` file that is ignored by git. Configure it as follows: ```bash cp .env.example .env ```: "Runtime secrets and machine-specific paths live in a `.env` file that is ignored by git"
- [readme] Edit `.env` with your editor of choice and provide the correct values (absolute path to the Sirius executable, Sirius account credentials, etc.). Before running the workflow, load the file into your shell session: ```bash set -a source .env set +a ```: "Before running the workflow, load the file into your shell session"
- [other] Verify the installation by running provided setup validation checks or test commands to confirm all components are correctly configured.: "Verify the installation by running provided setup validation checks or test commands"
- [readme] The workflow reads that variable when launching Sirius.: "The workflow reads that variable when launching Sirius"
