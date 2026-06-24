---
name: hdf5-format-support-validation
description: Use when when you need to work with mzMLb (HDF5-based) proteomics data
  in pyteomics and want to confirm that the required h5py and hdf5plugin libraries
  are installed and accessible, or when troubleshooting ImportError or missing format
  handler issues related to mzMLb modules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pip
  - h5py
  - hdf5plugin
  - Python
  license_tier: restricted
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

# hdf5-format-support-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate that HDF5-dependent proteomics data formats (mzMLb) are correctly supported in pyteomics by installing and testing conditional dependencies (h5py, hdf5plugin). This skill ensures that optional format handlers are properly resolved and functional before attempting mzMLb file access.

## When to use

When you need to work with mzMLb (HDF5-based) proteomics data in pyteomics and want to confirm that the required h5py and hdf5plugin libraries are installed and accessible, or when troubleshooting ImportError or missing format handler issues related to mzMLb modules.

## When NOT to use

- You are working only with mzML (non-HDF5) or other proteomics formats that do not require h5py or hdf5plugin.
- Your pyteomics installation is already verified to support mzMLb and you do not suspect dependency issues.
- You only need to read metadata about mzMLb support without actually importing or using the mzMLb module.

## Inputs

- pyteomics package specification (with mzMLb extra)
- Python environment
- network access to PyPI (for pip installation)

## Outputs

- pyteomics.mzmlb module loaded in Python runtime
- confirmation that h5py and hdf5plugin are accessible to pyteomics
- absence of ImportError (success signal)

## How to apply

Install pyteomics with the mzMLb extra specifier using pip to resolve h5py and hdf5plugin as conditional dependencies. Launch a Python interpreter and execute `import pyteomics.mzmlb` to trigger module loading and dependency resolution. If the import completes without raising ImportError, the optional dependencies have been correctly resolved and the mzMLb module is functional. If ImportError is raised, inspect the error message to identify which dependency (h5py or hdf5plugin) is missing, then install it explicitly and retry the import. This workflow validates both the presence and accessibility of the HDF5 ecosystem required for mzMLb support.

## Related tools

- **pip** (Install pyteomics with mzMLb extra and resolve conditional dependencies h5py and hdf5plugin) — https://pypi.org/project/pyteomics/
- **Python** (Execute import statement to validate module loading and dependency resolution)
- **h5py** (Enable HDF5 file I/O operations required by pyteomics.mzmlb) — https://pypi.org/project/h5py/
- **hdf5plugin** (Provide optional HDF5 compression filters and codec support for mzMLb) — https://pypi.org/project/hdf5plugin/

## Examples

```
pip install pyteomics[mzMLb] && python -c "import pyteomics.mzmlb; print('mzMLb support validated')"
```

## Evaluation signals

- Import statement `import pyteomics.mzmlb` completes without raising ImportError or ModuleNotFoundError
- Python sys.modules contains entry for 'pyteomics.mzmlb' after successful import
- No exception trace references missing h5py or hdf5plugin packages in error output
- mzMLb module attributes are accessible (e.g., dir(pyteomics.mzmlb) returns expected class/function names)
- pip freeze or pip show confirms h5py and hdf5plugin are installed in the active environment

## Limitations

- This skill validates only that the mzMLb module imports successfully; it does not verify that actual mzMLb files can be read or parsed without errors.
- The skill requires network access during initial installation to download h5py and hdf5plugin from PyPI; offline environments will require pre-cached wheels or alternative distribution methods.
- Platform-specific issues (e.g., missing system HDF5 libraries) may cause h5py installation to fail even when pip succeeds, which this skill will not detect until the import is attempted.
- The article does not provide guidance on resolving version conflicts if h5py or hdf5plugin versions are incompatible with the installed version of pyteomics.

## Evidence

- [other] The mzMLb module in pyteomics requires h5py and hdf5plugin as conditional dependencies to provide access to mzMLb proteomics data format.: "The mzMLb module in pyteomics requires h5py and hdf5plugin as conditional dependencies to provide access to mzMLb proteomics data format."
- [other] Install h5py and hdf5plugin using pip with the mzMLb extra specifier: pip install pyteomics[mzMLb].: "Install h5py and hdf5plugin using pip with the mzMLb extra specifier: pip install pyteomics[mzMLb]."
- [other] Launch a Python interpreter and execute import pyteomics.mzmlb to confirm the module loads without ImportError.: "Launch a Python interpreter and execute import pyteomics.mzmlb to confirm the module loads without ImportError."
- [other] Verify that the mzMLb module is accessible and functional by checking that the import completes successfully.: "Verify that the mzMLb module is accessible and functional by checking that the import completes successfully."
- [other] The main way to obtain Pyteomics is via `pip Python package manager: "The main way to obtain Pyteomics is via `pip Python package manager"
