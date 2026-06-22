---
name: python-package-dependency-installation
description: Use when you need to enable optional modules in Pyteomics that depend on external libraries not bundled with the core package—such as h5py and hdf5plugin for mzMLb format access, sqlalchemy for Unimod database queries, or psims for ProForma parsing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pip
  - Python
  - h5py
  - hdf5plugin
  - sqlalchemy
  - psims
  - conda
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- The main way to obtain Pyteomics is via `pip Python package manager
- Pyteomics supports recent versions of Python 3
- Pyteomics supports recent versions of Python 3.
- h5py <https://www.h5py.org/> and optionally hdf5plugin
- h5py and optionally hdf5plugin <https://hdf5plugin.readthedocs.io/en/latest/>
- '- `sqlalchemy <https://www.sqlalchemy.org/>`_ (used by :py:mod:`pyteomics.mass.unimod`);'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# python-package-dependency-installation

## Summary

Install Python packages and their conditional dependencies using pip or conda to enable specific functionality modules. This skill is essential when a proteomics analysis workflow requires optional features (e.g., mzMLb format support, Unimod database access) that are not included in the base package installation.

## When to use

Apply this skill when you need to enable optional modules in Pyteomics that depend on external libraries not bundled with the core package—such as h5py and hdf5plugin for mzMLb format access, sqlalchemy for Unimod database queries, or psims for ProForma parsing. Trigger on ImportError exceptions or when planning an analysis that targets a data format or functionality known to require conditional dependencies.

## When NOT to use

- Your analysis uses only core Pyteomics modules (pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, pyteomics.auxiliary) that are included in the base installation—the base pip install pyteomics is sufficient.
- The required conditional dependency is already installed in your environment and the module imports successfully—skip reinstallation.
- You are working in a locked or sandboxed environment (e.g., read-only container, air-gapped system) where pip cannot fetch or install packages from PyPI or Bioconda.

## Inputs

- Python 3 environment
- pip or conda package manager available in PATH
- Pyteomics package name and optional extra specifier (e.g., 'pyteomics[mzMLb]')
- Optional: list of conditional dependency package names (e.g., 'h5py', 'hdf5plugin', 'sqlalchemy')

## Outputs

- Installed Pyteomics package in site-packages
- Installed conditional dependency packages (h5py, hdf5plugin, sqlalchemy, psims, pynumpress, etc.)
- Import validation report documenting success/failure status of target modules
- Accessible Python module namespace with functional proteomics data accessors and analysis functions

## How to apply

First, identify the optional module or feature required for your analysis task (e.g., pyteomics.mzmlb for mzMLb files, pyteomics.mass.unimod for Unimod database). Install the base package and its conditional dependency using pip with the appropriate extra specifier (e.g., `pip install pyteomics[mzMLb]`) or by installing the dependency package directly (e.g., `pip install sqlalchemy`). Launch a Python interpreter and attempt to import the target module (e.g., `import pyteomics.mzmlb`). Verify successful initialization by checking that the import completes without raising ImportError and, where applicable, by instantiating key classes or calling diagnostic functions (e.g., checking that the Unimod database accessor initializes without exception). Document the success or failure status of each import to confirm module readiness before proceeding with your analysis.

## Related tools

- **pip** (Package manager used to install Pyteomics and conditional dependencies from PyPI) — https://pypi.org/project/pyteomics/
- **conda** (Alternative package manager to install Pyteomics from Bioconda distribution) — http://bioconda.github.io/recipes/pyteomics/README.html
- **h5py** (Conditional dependency enabling mzMLb format support in pyteomics.mzmlb module) — https://pypi.org/project/h5py/
- **hdf5plugin** (Conditional dependency providing HDF5 codec plugins required alongside h5py for mzMLb access) — https://pypi.org/project/hdf5plugin/
- **sqlalchemy** (Conditional dependency enabling Unimod database initialization and queries in pyteomics.mass.unimod) — https://www.sqlalchemy.org/
- **psims** (Conditional dependency for ProForma parsing functionality in pyteomics.proforma module)
- **Python** (Interpreter environment for executing import statements and validation scripts) — https://www.python.org/

## Examples

```
pip install 'pyteomics[mzMLb]' && python -c 'import pyteomics.mzmlb; print("mzMLb module loaded successfully")'
```

## Evaluation signals

- Import statement completes without raising ImportError or ModuleNotFoundError for the target module (e.g., `import pyteomics.mzmlb` succeeds).
- Class instantiation or function call from the imported module executes without exception (e.g., Unimod database accessor initializes; mzMLb file reader is callable).
- pip show <package> or pip list output confirms presence and correct version of the installed conditional dependency.
- Python sys.modules dictionary contains the target module name after successful import.
- No version conflicts or unmet transitive dependencies reported by pip check or conda list.

## Limitations

- Some conditional dependencies (e.g., hdf5plugin for mzMLb) may require system-level HDF5 libraries to be installed beforehand; pip installation alone may fail on environments without development headers.
- conda installation from Bioconda may have different version availability or platform support than PyPI pip installation.
- Changelog is not available for Pyteomics, making it difficult to track which versions introduced or removed support for specific conditional dependencies.
- Installing multiple optional extras simultaneously (e.g., `pip install pyteomics[mzMLb,ims]`) may introduce transitive dependency conflicts if they require different versions of shared libraries.

## Evidence

- [readme] The main way to obtain Pyteomics is via `pip Python package manager: "The main way to obtain Pyteomics is via `pip Python package manager"
- [other] Install h5py and hdf5plugin using pip with the mzMLb extra specifier: pip install pyteomics[mzMLb]: "Install h5py and hdf5plugin using pip with the mzMLb extra specifier: pip install pyteomics[mzMLb]"
- [other] Launch a Python interpreter and execute import pyteomics.mzmlb to confirm the module loads without ImportError: "Launch a Python interpreter and execute import pyteomics.mzmlb to confirm the module loads without ImportError"
- [other] The mzMLb module in pyteomics requires h5py and hdf5plugin as conditional dependencies to provide access to mzMLb proteomics data format: "The mzMLb module in pyteomics requires h5py and hdf5plugin as conditional dependencies to provide access to mzMLb proteomics data format"
- [other] The pyteomics.mass.unimod module depends on sqlalchemy as a conditional dependency for accessing the Unimod database: "The pyteomics.mass.unimod module depends on sqlalchemy as a conditional dependency for accessing the Unimod database"
- [readme] You can also install Pyteomics from `Bioconda` using `conda`: "You can also install Pyteomics from `Bioconda` using `conda`"
