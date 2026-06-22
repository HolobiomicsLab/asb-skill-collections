---
name: module-import-verification
description: 'Use when after installing a Python package (especially one with optional dependencies) to confirm that: (1) core modules are accessible and importable;'
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_0121
  tools:
  - pip
  - h5py
  - hdf5plugin
  - sqlalchemy
  - psims
  - conda
  - Python
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- The main way to obtain Pyteomics is via `pip Python package manager
- h5py <https://www.h5py.org/> and optionally hdf5plugin
- h5py and optionally hdf5plugin <https://hdf5plugin.readthedocs.io/en/latest/>
- '- `sqlalchemy <https://www.sqlalchemy.org/>`_ (used by :py:mod:`pyteomics.mass.unimod`);'
- '- `psims <https://mobiusklein.github.io/psims/docs/build/html/>`_ (used py :py:mod:`pyteomics.proforma`)'
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
---

# module-import-verification

## Summary

Verify that installed Python packages and their optional-dependency modules can be successfully imported without errors, confirming installation completeness and functional availability. This skill validates both core and conditionally-dependent submodules across different installation methods (pip, conda).

## When to use

Apply this skill after installing a Python package (especially one with optional dependencies) to confirm that: (1) core modules are accessible and importable; (2) conditionally-dependent modules (requiring extra packages like h5py, sqlalchemy, or psims) are available only after their respective dependencies are installed; (3) the installed package version matches expectations. Use this particularly when validating proteomics data analysis tools like Pyteomics that expose functionality through nested module hierarchies (e.g., pyteomics.mass.unimod, pyteomics.mzmlb).

## When NOT to use

- The package is already imported and in active use in a running Python session; re-importing to verify is redundant unless you suspect module corruption.
- Your goal is to test package *functionality* (e.g., actual mzML parsing or mass calculation); import verification only confirms availability, not correctness or performance.
- The package is being installed in an air-gapped or offline environment where PyPI or Bioconda cannot be reached; the installation will fail before import can be tested.

## Inputs

- Python environment (version ≥3)
- Package manager (pip or conda) with network access to PyPI or Bioconda
- Package name and optional extra specifiers (e.g., 'pyteomics[mzMLb]')
- List of expected module paths to import (e.g., 'pyteomics.mass', 'pyteomics.pepxml')

## Outputs

- Installation verification report documenting module-by-module import success/failure status
- Python version and installed package version
- ImportError messages (if any) for failed imports
- Confirmation of conditional dependency resolution (e.g., h5py availability for mzMLb support)

## How to apply

Install the target package using your chosen package manager (pip or conda). For core module availability, sequentially import each documented module (e.g., pyteomics.mass, pyteomics.pepxml, pyteomics.mzid) in a Python interpreter or script and log success/failure status. For optional-dependency modules, install the package with the appropriate extra specifier (e.g., `pip install pyteomics[mzMLb]`) or install the dependency separately (e.g., `pip install sqlalchemy`), then attempt to import the module and instantiate relevant classes if applicable. Document the Python version, package version, import status for each module, and any ImportError messages. The skill succeeds when all expected modules import without exception and are accessible to downstream code.

## Related tools

- **pip** (Primary package manager for installing Pyteomics and its optional dependencies from PyPI) — https://github.com/pypa/pip
- **conda** (Alternative package manager for installing Pyteomics from the Bioconda channel) — https://github.com/conda/conda
- **Python** (Runtime environment in which modules are imported and verified)
- **h5py** (Conditional dependency for mzMLb format module support in Pyteomics) — https://github.com/h5py/h5py
- **sqlalchemy** (Conditional dependency for Unimod database access via pyteomics.mass.unimod) — https://www.sqlalchemy.org/
- **psims** (Conditional dependency enabling ProForma module functionality in Pyteomics)
- **hdf5plugin** (Conditional dependency required alongside h5py for mzMLb format support)

## Examples

```
pip install pyteomics && python -c "import pyteomics.mass; import pyteomics.pepxml; import pyteomics.mzid; print('Core modules imported successfully')"
```

## Evaluation signals

- All expected core modules (pyteomics.mass, pyteomics.pepxml, pyteomics.mzid, pyteomics.tandem, pyteomics.auxiliary) import without raising ImportError
- Conditional-dependency modules only import successfully after their stated dependencies are installed; import fails with clear error message if dependency is absent
- Instantiation of module-specific classes (e.g., Unimod database accessor) completes without exceptions
- Package version string matches the installed version number reported by pip or conda
- Sequential imports produce consistent results across multiple invocations in the same Python session

## Limitations

- Module import verification does not test functional correctness (e.g., whether pyteomics.mass actually calculates masses correctly); it only confirms availability.
- Some modules may have nested optional dependencies not fully documented in the README (e.g., hdf5plugin alongside h5py for mzMLb); trial-and-error or detailed error messages may be needed.
- No changelog is provided in the repository, making it difficult to diagnose which module changes occurred between versions without consulting GitHub commit history or release notes on PyPI.

## Evidence

- [other] Pyteomics provides a growing set of modules designed to facilitate common proteomics data analysis tasks: "Pyteomics provides a growing set of modules to facilitate the most common tasks in proteomics data analysis"
- [readme] Installation via pip from PyPI is the primary documented method: "The main way to obtain Pyteomics is via `pip Python package manager"
- [other] mzMLb module requires h5py and hdf5plugin as conditional dependencies: "The mzMLb module in pyteomics requires h5py and hdf5plugin as conditional dependencies"
- [readme] Installation from Bioconda via conda is an alternative method: "You can also install Pyteomics from `Bioconda` using `conda`"
- [other] sqlalchemy is a conditional dependency for Unimod module: "The pyteomics.mass.unimod module depends on sqlalchemy as a conditional dependency for accessing the Unimod database"
- [other] psims enables ProForma module support: "Pyteomics provides a growing set of modules to facilitate the most common tasks in proteomics data analysis, including calculation of basic physico-chemical properties of polypeptides"
