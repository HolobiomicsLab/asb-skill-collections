---
name: installation-verification-and-validation
description: Use when after cloning the ENPKG repository and installing dependencies using uv sync or conda, before executing the workflow on metabolomics datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - uv
  - Sirius
  - pytest
  - Anaconda / Miniconda
  - Git
  techniques:
  - LC-MS
  - tandem-MS
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

# Installation Verification and Validation

## Summary

Verify that all ENPKG workflow dependencies, Python environment, and external tools (uv, Sirius, conda/anaconda) are correctly installed and configured by running setup validation checks and confirming environment variables are properly sourced. This skill ensures the computational environment is ready for LC-MS/MS metabolomics data processing before launching the full workflow.

## When to use

After cloning the ENPKG repository and installing dependencies using uv sync or conda, before executing the workflow on metabolomics datasets. Use this skill when environment setup is complete but you need to confirm that all runtime requirements (Python version, Sirius binary path, environment variables, virtual environment isolation) are functional and correctly configured.

## When NOT to use

- When the workflow has already been executed successfully on this machine — re-validation is unnecessary unless dependencies are updated or environment is reset.
- If you are only reading or modifying workflow configuration files (params/user.yml) without intent to execute — validation adds no value to static code review.
- When working with a pre-configured container or cluster environment where installation is managed by administrators — individual verification may conflict with centralized package management.

## Inputs

- Cloned enpkg/enpkg_full repository directory
- .env configuration file with PATH_TO_SIRIUS and Sirius credentials
- System PATH with Git and Anaconda/Miniconda
- Project pyproject.toml or uv.lock dependency specification

## Outputs

- Active isolated Python virtual environment (.venv)
- Setup validation report documenting Python version, Sirius path, platform, and all dependency versions
- Sourced environment variables (PATH_TO_SIRIUS, SIRIUS_USERNAME, SIRIUS_PASSWORD)
- Test execution logs confirming pytest or equivalent validation commands pass

## How to apply

First, activate or verify the isolated .venv environment created by uv sync, and confirm the Python version matches the workflow requirements (e.g., Python 3.11). Second, verify that the Sirius binary is correctly installed by checking the PATH_TO_SIRIUS variable in the .env file and confirming the binary exists at that absolute path (e.g., /opt/sirius/sirius/bin/sirius on Linux, /opt/sirius/sirius.app/Contents/MacOS/sirius on macOS). Third, load the .env file into your shell session using source .env to make runtime secrets and machine-specific paths available. Fourth, run provided test commands such as uv run pytest to execute validation checks that confirm all components are correctly configured. Finally, verify that Git and Anaconda/Miniconda are installed and accessible in the PATH, as these are listed prerequisites. Document the environment configuration details including Python version, Sirius installation path, and OS/CPU platform in a setup report for reproducibility.

## Related tools

- **uv** (Dependency manager for creating isolated Python environment and installing runtime dependencies into .venv) — https://docs.astral.sh/uv/latest/
- **Sirius** (External binary for fragmentation annotation; verification requires checking absolute path to sirius executable and confirming credentials in .env) — https://boecker-lab.github.io/docs.sirius.github.io/install/
- **pytest** (Test runner invoked via uv run pytest to validate that all dev dependencies and runtime configuration are correct) — https://github.com/enpkg/enpkg_full
- **Anaconda / Miniconda** (Python distribution listed as prerequisite; verification confirms installation and accessibility in system PATH) — https://docs.anaconda.com/free/anaconda/install/index.html
- **Git** (Version control tool listed as prerequisite; verification confirms installation and accessibility in system PATH) — https://github.com/git-guides/install-git

## Examples

```
uv sync && uv run pytest && source .env && set -a && source .env && set +a && echo "Setup validation complete"
```

## Evaluation signals

- uv sync completes without errors and creates a .venv directory containing Python executable and installed packages
- uv run pytest executes successfully with all tests passing, indicating dev dependencies (pytest, linters) are correctly installed
- Sirius binary is accessible at the path stored in PATH_TO_SIRIUS environment variable; running the binary without error confirms installation and platform detection
- Environment variables are properly sourced: source .env followed by echo $PATH_TO_SIRIUS returns the absolute path without empty output
- Python version check via python --version or uv python show matches the minimum required version (e.g., 3.11); virtual environment isolation is confirmed by checking $(which python) points to .venv/bin/python

## Limitations

- The setup validation workflow assumes user has write permissions in the project directory to create .venv and download/install packages; insufficient permissions will cause silent or explicit failures.
- Sirius installation requires platform auto-detection (Linux, macOS, Windows) via the install_sirius.sh script; users on unsupported CPU architectures or OS variants may need manual intervention or platform override flags.
- Environment variables in .env are user-specific and machine-specific (absolute paths, credentials); they are not version-controlled (git-ignored), so validation on a different machine or after .env deletion will fail until .env is reconfigured.
- The README does not specify expected runtime duration or system resource requirements for validation; validation on resource-constrained systems may timeout or fail indirectly due to slow dependency resolution.
- No changelog is provided in the repository, so there is no clear record of which environment changes or package version updates might cause previously-passing validation to fail; users must rely on GitHub release notes and issue tracking.

## Evidence

- [readme] With uv installed, sync the project dependencies into an isolated `.venv`: uv sync: "With uv installed, sync the project dependencies into an isolated `.venv`"
- [readme] You can also run commands without activating by prefixing them with `uv run`, e.g.: uv run pytest: "You can also run commands without activating by prefixing them with `uv run`, e.g.: `uv run pytest`"
- [readme] Activate it with: source .venv/bin/activate: "Activate it with: `source .venv/bin/activate`"
- [readme] Before running the workflow, load the file into your shell session: set -a; source .env; set +a: "Before running the workflow, load the file into your shell session"
- [readme] You will need to have Git and Anaconda (or Miniconda) installed.: "You will need to have Git and Anaconda (or Miniconda) installed."
- [readme] Run `src/install_sirius.sh <install_dir>` to download and unpack the latest release for your platform: "Run `src/install_sirius.sh <install_dir>` to download and unpack the latest release for your platform"
- [readme] After installation, identify the full path to the `sirius` binary and store it in `.env` as `PATH_TO_SIRIUS`.: "After installation, identify the full path to the `sirius` binary and store it in `.env` as `PATH_TO_SIRIUS`"
- [other] Verify the installation by running provided setup validation checks or test commands to confirm all components are correctly configured.: "Verify the installation by running provided setup validation checks or test commands to confirm all components are correctly configured."
