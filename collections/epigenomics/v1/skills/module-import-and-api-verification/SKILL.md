---
name: module-import-and-api-verification
description: Use when before invoking any Python module in a multi-step Hi-C processing pipeline, or when a dependency has been freshly installed or reinstalled.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0224
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3169
  tools:
  - MultiQC 1.8
  - iced
  - numpy (>=1.18.1)
  - scipy (>=1.4.1)
  - numpy
  - scipy
  - Python
derived_from:
- doi: 10.1186/s13059-015-0831-x
  title: hicpro
evidence_spans:
- iced module is also required (https://github.com/hiclib/iced)
- Note that the iced module is also required (https://github.com/hiclib/iced)
- numpy (>=1.18.1) - http://www.scipy.org/scipylib/download.html
- scipy (>=1.4.1) - http://www.scipy.org/scipylib/download.html
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hicpro
    doi: 10.1186/s13059-015-0831-x
    title: hicpro
  dedup_kept_from: coll_hicpro
schema_version: 0.2.0
---

# module-import-and-api-verification

## Summary

Validate that required Python modules (e.g., iced for Hi-C ICE normalization) are correctly installed, importable, and expose the expected API before downstream pipeline steps depend on them. This skill detects installation failures, version mismatches, and missing transitive dependencies early.

## When to use

Before invoking any Python module in a multi-step Hi-C processing pipeline, or when a dependency has been freshly installed or reinstalled. Specifically required in HiC-Pro when iced is needed for iterative correction and normalization of Hi-C contact matrices, since iced is no longer bundled with HiC-Pro source code and must be independently installed.

## When NOT to use

- Module is already known to be installed and verified in a frozen, containerized environment (Docker, Singularity) where dependencies are immutable.
- Performing only static code analysis or linting that does not require runtime import.
- Installing dependencies for the first time — use standard package manager installation (pip install, conda install) as the primary step before verification.

## Inputs

- Python interpreter (>3.7) with PATH to installation directory
- Module name (string) to import
- Optional: expected version string or API function name to probe

## Outputs

- Boolean or exit code indicating successful import and API availability
- Version string of successfully imported module
- Configuration file documenting module path and PYTHONPATH for downstream steps

## How to apply

After installing the target module (e.g., iced) and its transitive dependencies (numpy ≥1.18.1, scipy ≥1.4.1) via pip or setup.py, open a Python interpreter within the same environment and attempt to import the module by name. Check the module's version attribute or docstring to confirm it is present. Call a representative function or method from the module's public API (e.g., iced's normalization functions) to verify that the API surface is accessible and not corrupted. Document the import path, version, and any environment variables (e.g., PYTHONPATH) in a configuration file for reproducibility across cluster nodes or container restarts. If import or API check fails, diagnose the root cause: missing transitive dependencies, version incompatibility, incorrect PYTHONPATH, or conflicting installed packages.

## Related tools

- **iced** (ICE (iterative correction and eigenvector decomposition) normalization module for Hi-C contact matrix balancing; must be imported and verified before HiC-Pro normalization pipeline invocation) — https://github.com/hiclib/iced
- **numpy** (Transitive dependency of iced (≥1.18.1); required for numerical array operations in normalization)
- **scipy** (Transitive dependency of iced (≥1.4.1); required for scientific computing primitives)
- **Python** (Runtime interpreter (>3.7) that executes the import and API verification check)

## Examples

```
python -c "import iced; print(iced.__version__); from iced.normalization import ICE; print('iced API verified')"
```

## Evaluation signals

- Module import succeeds without ImportError, ModuleNotFoundError, or AttributeError in Python interpreter.
- Version attribute or __version__ string is accessible and matches or exceeds minimum required version (e.g., iced from https://github.com/hiclib/iced).
- Representative API function (e.g., iced's main normalization callable) is callable without TypeError or NameError.
- PYTHONPATH environment variable is correctly set and documented in configuration file for reproducibility across execution environments.
- No conflicting or duplicate installations of the module exist in the Python path that would mask the intended installation.

## Limitations

- Verification only confirms import success and basic API presence; does not validate correctness of algorithmic output (e.g., that ICE-normalized matrices are mathematically sound).
- Version check is static and does not account for API changes within the same semantic version that might break downstream steps.
- Import verification in one Python environment or conda/virtualenv does not guarantee availability in other shells or containerized execution contexts unless PYTHONPATH is explicitly propagated.
- Transitive dependency conflicts (e.g., numpy version incompatibility with iced) may not be caught until runtime function invocation, not just import.

## Evidence

- [methods] Iced is no longer part of the HiC-Pro source code, and must be independently installed: "Iced is no longer part of the HiC-Pro source code, and should be independantly installed"
- [methods] Install iced and its transitive dependencies using pip or setup.py, then validate in Python interpreter: "Install iced and its transitive dependencies (numpy >=1.18.1, scipy >=1.4.1) using pip or the iced setup.py. Validate the iced installation by importing the module and checking version/API"
- [methods] Document module installation path and PYTHONPATH for downstream pipeline steps: "Document the iced installation path and Python environment variables (e.g., PYTHONPATH) in a configuration file for downstream HiC-Pro normalization steps."
- [readme] ICE normalization is required for contact matrix normalization in HiC-Pro: "HiC-Pro includes a fast implementatation of the iterative correction method (see the [iced python package](https://github.com/hiclib/iced) for more information)."
- [readme] Python version and dependency version requirements: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries."
