---
name: optional-dependency-extra-specifier-usage
description: Use when when a Python package provides optional support for specialized
  data formats or functionality (e.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_3375
  tools:
  - pip
  - h5py
  - hdf5plugin
  - Python
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.8b00717
  title: pyteomics
evidence_spans:
- The main way to obtain Pyteomics is via `pip Python package manager
- h5py <https://www.h5py.org/> and optionally hdf5plugin
- h5py and optionally hdf5plugin <https://hdf5plugin.readthedocs.io/en/latest/>
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

# optional-dependency-extra-specifier-usage

## Summary

Install optional feature-specific dependencies in a Python package using pip's extra specifier syntax (e.g., `pip install package[extra_name]`). This skill enables conditional loading of modules that require external libraries for specialized functionality—such as mzMLb format support in proteomics—without forcing all dependencies on base installations.

## When to use

When a Python package provides optional support for specialized data formats or functionality (e.g., mzMLb proteomics files, HDF5-backed structures) that requires external compiled libraries (h5py, hdf5plugin), and you want to enable that specific capability without installing unrelated dependencies. Use this when an import fails with ImportError and the error suggests missing optional dependencies.

## When NOT to use

- The desired functionality is already available with the base package installation — extra specifiers are only needed when optional features are gated behind missing dependencies.
- The package's documentation does not declare an extra specifier for your use case — manual dependency discovery and installation may be required instead.
- You are using conda or another package manager as your primary installation tool and the package's conda-forge recipe does not expose the same extra specifier naming.

## Inputs

- package name with extra specifier (string: 'package[extra_name]')
- pip package manager (CLI tool)
- Python interpreter (for verification import)

## Outputs

- installed base package with optional dependencies resolved
- importable Python module confirmed working (no ImportError)
- access to specialized functionality (e.g., mzMLb reader module)

## How to apply

Identify the extra specifier name documented for the desired capability (e.g., 'mzMLb' for mzMLb format support in pyteomics). Use pip with bracket notation: `pip install package_name[extra_name]`. This installs both the base package and the conditional dependencies required for that feature. After installation, verify the feature works by importing the module in a Python interpreter (e.g., `import pyteomics.mzmlb`) and confirming the import completes without ImportError. The extra specifier approach centralizes dependency declaration in the package's setup configuration, avoiding manual multi-tool installation.

## Related tools

- **pip** (Package manager that resolves and installs base package and declared optional dependencies using extra specifier syntax) — https://pip.pypa.io/
- **h5py** (Optional dependency providing HDF5 file access required for mzMLb format support in pyteomics) — https://github.com/h5py/h5py
- **hdf5plugin** (Optional dependency enabling compression codec support for mzMLb files in pyteomics)
- **Python** (Runtime environment for importing and verifying the installed optional module) — https://www.python.org/

## Examples

```
pip install pyteomics[mzMLb]; python -c "import pyteomics.mzmlb; print('mzMLb support enabled')"
```

## Evaluation signals

- Installation command completes without error and reports successful dependency resolution
- Import statement (e.g., `import pyteomics.mzmlb`) executes in Python REPL without ImportError
- Package version and installed dependencies match expected pinned or compatible versions declared in the extra specifier
- Specialized module is present and callable (e.g., `pyteomics.mzmlb.MzMLb()` for mzMLb reader instantiation)
- No version conflicts between optional dependencies and base package or other installed packages (verify via `pip show` or dependency graph)

## Limitations

- Extra specifiers are only as discoverable as the package's documentation; poorly documented extras may require reading setup.py or pyproject.toml directly.
- Different package managers (pip, conda, poetry) may use different syntax or naming for the same extra; conda-forge recipes may not expose all pip extras.
- Optional dependencies may have conflicting version constraints with other packages in the environment, requiring manual resolution.
- Installing an extra does not guarantee backward compatibility if the optional library updates to a breaking version; pin versions explicitly if reproducibility is critical.

## Evidence

- [other] The mzMLb module in pyteomics requires h5py and hdf5plugin as conditional dependencies to provide access to mzMLb proteomics data format.: "The mzMLb module in pyteomics requires h5py and hdf5plugin as conditional dependencies to provide access to mzMLb proteomics data format."
- [other] Install h5py and hdf5plugin using pip with the mzMLb extra specifier: pip install pyteomics[mzMLb].: "Install h5py and hdf5plugin using pip with the mzMLb extra specifier: pip install pyteomics[mzMLb]."
- [other] Verify that the mzMLb module is accessible and functional by checking that the import completes successfully.: "Verify that the mzMLb module is accessible and functional by checking that the import completes successfully."
- [other] The main way to obtain Pyteomics is via `pip Python package manager: "The main way to obtain Pyteomics is via `pip Python package manager"
