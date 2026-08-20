---
name: conda-environment-setup-and-activation
description: Use when preparing a fresh system or user account to run MSIGen for mass
  spectrometry imaging data processing, or when you need to isolate MSIGen installation
  from other Python projects to avoid dependency conflicts.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - pyBaf2Sql
  - ProteoWizard MSConvert
  - MSIGen
  - Python
  - Anaconda
  - Miniconda
  - Git
  techniques:
  - MS-imaging
  license_tier: open
derived_from:
- doi: 10.1021/jasms.4c00178
  title: MSIGen
evidence_spans:
- If you are planning on using Bruker .d data in the .baf format, you will also need
  to install pyBaf2Sql from GitHub
- you can convert it to the open-source .mzML format using ProteoWizard's MSConvert
  tool. You can download ProteoWizard from https://proteowizard.sourceforge.io/download.html
- You can download ProteoWizard from https://proteowizard.sourceforge.io/download.html.
- MSIGen provides tools for processing mass spectrometry imaging data acquired in
  line-scan mode into images and figures.
- from MSIGen import msigen
- Using an environment with python version >=3.9 and <=3.11
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msigen_cq
    doi: 10.1021/jasms.4c00178
    title: MSIGen
  dedup_kept_from: coll_msigen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00178
  all_source_dois:
  - 10.1021/jasms.4c00178
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# conda-environment-setup-and-activation

## Summary

Create and activate a isolated Conda Python environment with pinned version constraints to ensure reproducible installation of MSIGen and its dependencies (Python >=3.9 and <=3.11). This skill is essential before installing MSIGen or its optional prerequisites like pyBaf2Sql.

## When to use

Apply this skill when preparing a fresh system or user account to run MSIGen for mass spectrometry imaging data processing, or when you need to isolate MSIGen installation from other Python projects to avoid dependency conflicts. Specifically required before installing MSIGen via pip or before installing pyBaf2Sql for Bruker .baf data support.

## When NOT to use

- MSIGen is already installed in a working environment and you are only running analysis code — activation of an existing environment is not a 'setup' operation.
- You are using a different package manager (pip venv, Poetry, Docker) as the primary environment isolation strategy; mixing conda create with non-Conda virtual environments can cause confusion.
- Your system Python version is already 3.11 and you have manually installed all MSIGen dependencies globally — environment isolation is then optional (but not recommended for reproducibility).

## Inputs

- Anaconda or Miniconda installation on system PATH
- Command-line interface (Anaconda Prompt on Windows, Terminal on macOS/Linux)

## Outputs

- Activated Conda environment named 'MSIGen' with Python 3.11 (or specified 3.9–3.11 version)
- Shell/prompt prefix indicating active environment (e.g., '(MSIGen) C:\>')

## How to apply

Using Anaconda or Miniconda, execute conda create with explicit Python version pinning (3.9–3.11 range; 3.11 is recommended) and environment name 'MSIGen', then activate the environment using conda activate. The version constraint ensures compatibility with MSIGen's codebase and avoids breaking changes in Python 3.12+. After activation, the prompt will prefix with (MSIGen), confirming the environment is active. All subsequent pip install commands for MSIGen, pyBaf2Sql, Jupyter Notebook, or other tools must be run within this activated environment to install packages into the isolated namespace rather than the system Python.

## Related tools

- **Anaconda** (Conda distribution and package manager; provides conda create and conda activate commands to build isolated Python environments) — https://www.anaconda.com/download
- **Miniconda** (Lightweight alternative to Anaconda; provides only Conda and Python without pre-bundled packages; smaller download for environment setup) — https://www.anaconda.com/download/success

## Examples

```
conda create --name MSIGen python=3.11 -y && conda activate MSIGen && python --version
```

## Evaluation signals

- Conda environment 'MSIGen' is listed in `conda env list` output.
- Command-line prompt displays '(MSIGen)' prefix after running `conda activate MSIGen`, confirming environment is active.
- Running `python --version` within the active environment returns Python 3.9–3.11 (e.g., 'Python 3.11.x'), not the system Python version.
- Subsequent `pip install MSIGen` or `pip install git+https://github.com/gtluu/pyBaf2Sql` commands complete without version constraint conflicts.
- Running `conda list` in the active environment shows installed packages are isolated to that environment, not the base or system Python.

## Limitations

- Python 3.12+ is not supported; MSIGen requires <=3.11 due to potential breaking changes in newer Python major versions.
- Anaconda and Miniconda must be installed and available on system PATH before conda commands can be executed; users without prior Conda installation must download and install it separately.
- Environment activation is terminal/shell-specific and does not persist across new terminal sessions; users must re-run `conda activate MSIGen` in each new shell or configure a shell profile to auto-activate.
- Creating the environment requires network access to download Python packages from Conda repositories; offline or air-gapped systems may require pre-cached package archives.

## Evidence

- [methods] Using an environment with python version >=3.9 and <=3.11: "Using an environment with python version >=3.9 and <=3.11"
- [methods] If you do not have Python installed, we recommend installing the Anaconda distribution of Python: "If you do not have Python installed, we recommend installing the Anaconda distribution of Python"
- [readme] conda create --name MSIGen python=3.11 -y; conda activate MSIGen: "conda create --name MSIGen python=3.11 -y
conda activate MSIGen"
- [methods] you can instead download Miniconda from https://www.anaconda.com/download/success: "you can instead download Miniconda from https://www.anaconda.com/download/success"
