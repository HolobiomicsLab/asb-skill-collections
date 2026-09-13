---
name: command-line-software-installation-from-github
description: Use when you need to install a Python package that is distributed via
  GitHub but not yet (or only occasionally) published to PyPI, such as pyBaf2Sql for
  Bruker .baf/.d mass spectrometry imaging data conversion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3675
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pyBaf2Sql
  - ProteoWizard MSConvert
  - MSIGen
  - Python
  - Anaconda
  - Miniconda
  - Git
  - pip
  - Anaconda/Miniconda
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
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

# command-line-software-installation-from-github

## Summary

Install Python packages directly from GitHub repositories using pip and git, enabling access to development versions and dependencies not yet published to PyPI. This is essential for mass spectrometry data processing workflows that depend on specialized tools like pyBaf2Sql for Bruker .baf file conversion.

## When to use

You need to install a Python package that is distributed via GitHub but not yet (or only occasionally) published to PyPI, such as pyBaf2Sql for Bruker .baf/.d mass spectrometry imaging data conversion. This skill is required when the primary installation pathway directs users to GitHub and git is available in the environment.

## When NOT to use

- The package is already available on PyPI with a stable release; use `pip install <package_name>` instead for reproducibility and version pinning.
- You need a specific release version with long-term support guarantees; GitHub development branches may be unstable or subject to breaking changes.
- Git is not installed or network access to GitHub is unavailable; fall back to manual download and local installation.

## Inputs

- GitHub repository URL (HTTPS or SSH)
- Active Python virtual environment (Anaconda/Miniconda)
- Git command-line tool installed and in system PATH

## Outputs

- Installed Python package in the virtual environment site-packages
- Package importable via `import <package_name>` or `from <package_name>.<module> import <function>`
- Dependency resolution and installation of transitive requirements

## How to apply

Activate a Python virtual environment (Anaconda/Miniconda) with Python >=3.9 and <=3.11 to avoid compatibility issues. Run `pip install git+https://github.com/<username>/<repo>` in the command line or Anaconda Prompt, replacing username and repo with the target GitHub path. The git command automatically clones the repository and installs it in editable or standard mode. Verify installation by importing the package in Python (e.g., `from pyBaf2Sql.init_baf2sql import init_baf2sql_api`). If installation fails, ensure git is installed and accessible from the command line, and that the target repository is publicly available.

## Related tools

- **Git** (Version control and repository cloning system required by pip to download source code from GitHub) — https://git-scm.com/downloads
- **pip** (Python package installer that parses `git+` URLs and delegates to git for repository cloning)
- **Anaconda/Miniconda** (Python distribution and virtual environment manager used to create isolated Python environments with compatible versions (>=3.9, <=3.11)) — https://www.anaconda.com/download
- **pyBaf2Sql** (Example target package for GitHub installation; Python wrapper for Bruker Baf2Sql library for reading .baf mass spectrometry data) — https://github.com/gtluu/pyBaf2Sql

## Examples

```
conda create --name MSIGen python=3.11 -y && conda activate MSIGen && pip install git+https://github.com/gtluu/pyBaf2Sql
```

## Evaluation signals

- Package can be successfully imported in Python without ImportError or ModuleNotFoundError
- pip list output includes the package name and a commit hash or development version string (e.g., pyBaf2Sql@<hash>)
- Example code from the package's README or documentation (e.g., `from pyBaf2Sql.classes import BafData`) runs without AttributeError or missing module errors
- pip show <package_name> displays a location path pointing to the virtual environment's site-packages directory, not a system-wide or conda-managed path
- All declared dependencies (transitive requirements) are installed; verify with `pip check` returns no broken dependencies

## Limitations

- GitHub development branches may contain undocumented APIs, breaking changes, or unfinished features; stability is not guaranteed until a formal release.
- Python version compatibility constraints (e.g., >=3.9 and <=3.11 for pyBaf2Sql) must be enforced at the virtual environment creation step; installing into an incompatible base Python will fail at runtime with cryptic C extension or binary compatibility errors.
- Network latency and GitHub availability affect installation time; if GitHub is unreachable, the command will fail and require manual retry or fallback to a previously cached wheel.
- Platform-specific dependencies (e.g., .dll or .so files packaged with pyBaf2Sql for Windows vs. Linux) are included in the repository; ensure the GitHub branch matches your operating system.

## Evidence

- [methods] If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub: "If you are planning on using Bruker .d data in the .baf format, you will also need to install pyBaf2Sql from GitHub"
- [methods] pip install git+https://github.com/gtluu/pyBaf2Sql: "pip install git+https://github.com/gtluu/pyBaf2Sql"
- [readme] This package can be installed to a Python virtual environment using pip: "This package can be installed to a Python virtual environment using `pip`"
- [methods] Using an environment with python version >=3.9 and <=3.11: "Using an environment with python version >=3.9 and <=3.11"
- [methods] If you do not have Python installed, we recommend installing the Anaconda distribution of Python: "If you do not have Python installed, we recommend installing the Anaconda distribution of Python"
