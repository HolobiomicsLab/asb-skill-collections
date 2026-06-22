---
name: package-manager-environment-setup
description: Use when when you need to establish a working installation of a Python package in a fresh or isolated environment, particularly when the package is available through multiple distribution channels (PyPI, Bioconda, AUR) and you want to verify that the installation is complete and functional before.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_0121
  tools:
  - conda
  - pip
  - Bioconda
  - Python
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- 'using `conda <https://docs.conda.io/projects/conda/en/latest/index.html>`_::'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyteomics
    doi: 10.1021/acs.jproteome.8b00717
    title: pyteomics
  dedup_kept_from: coll_pyteomics
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00717
  all_source_dois:
  - 10.1021/acs.jproteome.8b00717
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# package-manager-environment-setup

## Summary

Install and verify a scientific Python package via a package manager (conda or pip) and confirm that core modules import without errors. This skill ensures reproducible, documented environment setup and validates that all critical dependencies resolve correctly before downstream analysis.

## When to use

When you need to establish a working installation of a Python package in a fresh or isolated environment, particularly when the package is available through multiple distribution channels (PyPI, Bioconda, AUR) and you want to verify that the installation is complete and functional before integrating it into a larger workflow or analysis pipeline.

## When NOT to use

- The package is already successfully installed and imported in the current environment with verified version compatibility.
- You are installing into a locked or production environment where package installation is prohibited or managed by a separate system administrator.
- The package is only needed as a transitive dependency and will be installed automatically by another package manager during a parent package installation.

## Inputs

- package name and version specification (string)
- package manager configuration (e.g., channel specification for conda)
- Python interpreter availability (system or environment)

## Outputs

- installation verification report (text/markdown documenting Python version, package version, and import success/failure)
- installed package in active Python environment
- confirmation that core modules are importable

## How to apply

First, identify the appropriate package manager and distribution channel for your target package—conda via Bioconda is preferred for scientific packages with complex compiled dependencies, while pip is suitable for pure Python packages. Install the package using the standard package manager command (e.g., `conda install -c bioconda pyteomics` for Bioconda). After installation completes, launch a Python interpreter and attempt to import each of the package's core modules in sequence. Record the Python interpreter version, the installed package version, and the success or failure of each import attempt. If all critical imports execute without errors, the installation is verified and documented; if any import fails, diagnose the missing dependency or version conflict and reinstall or update as needed.

## Related tools

- **conda** (package manager for installing packages from Bioconda and other conda channels with dependency resolution)
- **pip** (alternative Python package manager for installing packages from PyPI)
- **Bioconda** (conda distribution channel providing pre-built binaries for scientific Python packages) — http://bioconda.github.io/
- **Python** (runtime interpreter for executing import statements and verifying package functionality)

## Examples

```
conda install -c bioconda pyteomics && python -c "import pyteomics.mass; import pyteomics.pepxml; import pyteomics.mzid; print('All imports successful')"
```

## Evaluation signals

- All specified core module import statements execute without ImportError, ModuleNotFoundError, or AttributeError.
- Installed package version matches or exceeds the minimum required version specified in the installation command or documentation.
- Python interpreter version is recorded and is compatible with the package's stated requirements (e.g., Python 3.6+).
- Installation verification report is generated and archived, containing timestamp, environment info, and the output of version introspection (e.g., `pyteomics.__version__`).
- No dependency conflicts or warnings are reported during the installation phase.

## Limitations

- Installation success does not guarantee that all optional submodules or extra features are available; some functionality may require additional dependencies not installed by the base package.
- Import verification only confirms that module files exist and top-level code executes; it does not test the correctness or functionality of individual functions or classes.
- Package availability and version constraints vary by distribution channel; the same package may have different versions, dependencies, or build options across PyPI, Bioconda, and AUR.
- The skill assumes network access to the package repository and does not address offline installation scenarios or private/corporate package mirrors.

## Evidence

- [other] Use conda to install Pyteomics from the Bioconda channel with the command `conda install -c bioconda pyteomics`: "Use conda to install Pyteomics from the Bioconda channel with the command `conda install -c bioconda pyteomics`"
- [other] After installation completes, launch a Python interpreter and attempt to import pyteomics.mass: "After installation completes, launch a Python interpreter and attempt to import pyteomics.mass"
- [other] If all three imports execute without errors, record the success and the Python and Pyteomics versions in an installation verification report: "If all three imports execute without errors, record the success and the Python and Pyteomics versions in an installation verification report"
- [other] The main way to obtain Pyteomics is via `pip Python package manager: "The main way to obtain Pyteomics is via `pip Python package manager"
- [other] You can also install Pyteomics from `Bioconda` using `conda`: "You can also install Pyteomics from `Bioconda` using `conda`"
